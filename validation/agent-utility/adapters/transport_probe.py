#!/usr/bin/env python3
"""NON-BENCHMARK transport probe for the AU-v1 adapter (operator-runnable evidence).

Drives validation/agent-utility/adapters/hermes_cli_jsonl_adapter.py under a
harness-shaped stripped environment against a hand-built miniature broker and a
synthetic, fictional task. This is NOT an AU scenario: never score it, never place it
in a results cohort directory. It answers one question: does a real authorized model,
through the real CLI, correctly attest, drive broker reads, quote broker content it
could not otherwise know, and emit a clean protocol final + exit 0?

Usage:
  python3 transport_probe.py --provider openrouter --model <model-id> \
      --hermes-bin /ABS/path/to/hermes --hermes-home /ABS/path/to/real/hermes/home \
      [--out /abs/result.json]

Cost: a handful of small API calls (probe transcript ~1k chars, 3 turns).
"""
import argparse
import hashlib
import json
import os
import pathlib
import selectors
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
ADAPTER = HERE / "hermes_cli_jsonl_adapter.py"

FILES = {
    "index/L0.json": json.dumps({"description": "probe index", "cards": [
        {"id": "PROBE-1", "title": "Station merge rule", "path": "runbook/merge-rule.md"}]}),
    "runbook/merge-rule.md": (
        "---\nid: PROBE-1\ntitle: Station merge rule\ntype: solution\ndomain: ops\n"
        "summary: Only merge station logs when clock drift is bounded.\n---\n"
        "SAFE MERGE RULE: merge two station logs only when measured clock drift is under "
        "2 seconds and both logs use the UTC namespace; otherwise abstain and keep them "
        "separate. The marker token for this rule is QUARTZ-771.\n"),
}
BUDGETS = {"max_read_attempts": 24, "max_reads": 16, "max_read_chars": 64000,
           "max_chunk_chars": 8000, "max_initial_chars": 24000, "max_final_chars": 24000,
           "max_message_bytes": 65536, "timeout_seconds": 170}


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--hermes-bin", required=True)
    ap.add_argument("--hermes-home", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    settings = {"protocol_version": "atlas-utility-jsonl-1",
                "model_settings": {"model": a.model, "temperature": 0, "seed": 1729,
                                   "max_output_tokens": 4500},
                "budgets": BUDGETS, "layers": ["L0", "L1", "L2", "L3"]}
    inv = [{"path": k, "layer": "L0" if k.startswith("index") else "L2",
            "bytes": len(v.encode())} for k, v in FILES.items()]
    start = {"type": "start", "protocol_version": settings["protocol_version"],
             "scenario": {"scenario_id": "TRANSPORT-PROBE-NOT-BENCHMARK",
                          "project": "Fictional station-log runbook check.",
                          "known_facts": ["The answer marker exists only inside the corpus file."],
                          "question": "Read the runbook file named in the index and quote the exact "
                                      "safe merge rule including its marker token."},
             "prompt": "TRANSPORT PROBE (not a benchmark scenario): use only the broker read_file tool "
                       "to locate and quote the rule; answer nothing you did not read.",
             "settings": settings, "settings_sha256": hashlib.sha256(canonical(settings)).hexdigest(),
             "inventory": inv, "read_file": {"request": {"type": "read_file"}, "response": "read_result"}}

    work = pathlib.Path(tempfile.mkdtemp(prefix="au-e2e-probe-"))
    child_home = work / "home"
    child_home.mkdir()
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8",
           "HOME": str(child_home), "TMPDIR": str(child_home), "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.Popen([sys.executable, str(ADAPTER), "--provider", a.provider,
                             "--hermes-bin", a.hermes_bin, "--hermes-home", a.hermes_home],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            cwd=str(work), env=env, start_new_session=True)
    proc.stdin.write(canonical(start))
    proc.stdin.flush()
    buf, attempts, successes, chars = b"", 0, 0, 0
    ids, reads_log, messages = set(), [], []
    reader = selectors.DefaultSelector()
    reader.register(proc.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + BUDGETS["timeout_seconds"]

    def read_line():
        nonlocal buf
        while True:
            if b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                return line
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not reader.select(remaining):
                raise TimeoutError("adapter line timeout")
            chunk = os.read(proc.stdout.fileno(), 8192)
            if not chunk:
                return None
            buf += chunk

    t0, final, exit_code = time.monotonic(), None, None
    try:
        while True:
            line = read_line()
            if line is None:
                break
            msg = json.loads(line.decode())
            messages.append(msg)
            if msg.get("type") == "read_file":
                attempts += 1
                name, rid = msg["path"], msg["request_id"]
                ok = (rid not in ids and name in FILES and isinstance(msg["offset"], int)
                      and msg["offset"] >= 0 and isinstance(msg["length"], int)
                      and 1 <= msg["length"] <= BUDGETS["max_chunk_chars"])
                body = FILES[name][msg["offset"]:msg["offset"] + msg["length"]] if ok else ""
                err = None if ok else "denied (id/path/bounds)"
                if ok:
                    successes += 1
                    chars += len(body)
                ids.add(rid)
                reads_log.append({"path": name, "offset": msg["offset"], "length": msg["length"],
                                  "returned_chars": len(body), "error": err})
                result = {"type": "read_result", "request_id": rid, "path": name, "content": body,
                          "error": err,
                          "remaining": {"read_attempts": BUDGETS["max_read_attempts"] - attempts,
                                        "reads": BUDGETS["max_reads"] - successes,
                                        "read_chars": BUDGETS["max_read_chars"] - chars}}
                proc.stdin.write(canonical(result))
                proc.stdin.flush()
            elif msg.get("type") == "final":
                final = msg
                proc.stdin.close()
                break
        exit_code = proc.wait(timeout=max(1, deadline - time.monotonic()))
    except Exception as exc:
        exit_code = f"driver error: {type(exc).__name__}: {exc}"
    finally:
        if proc.poll() is None:
            proc.kill()
        reader.close()
        stderr_text = proc.stderr.read().decode("utf-8", "replace")
    ready = next((m for m in messages if m.get("type") == "ready"), None)
    out = {"probe": "AU-v1 adapter transport probe (NON-BENCHMARK — never scored)",
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "provider": a.provider, "model": a.model,
           "wall_seconds": round(time.monotonic() - t0, 1),
           "adapter_exit_code": exit_code,
           "ready_attestation": ready, "model_reads": reads_log,
           "attempts": attempts, "successful_reads": successes, "read_chars": chars,
           "final_chars": len(final["text"]) if final else 0,
           "final_text": final["text"] if final else None,
           "marker_in_final": bool(final and "QUARTZ-771" in final["text"]),
           "adapter_stderr_tail": stderr_text[-2500:]}
    dest = pathlib.Path(a.out) if a.out else work / "probe-result.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"result_file": str(dest), "adapter_exit_code": exit_code,
                      "wall_seconds": out["wall_seconds"], "marker_in_final": out["marker_in_final"],
                      "message_types": [m.get("type") for m in messages]}, indent=2))
    return 0 if isinstance(exit_code, int) and exit_code == 0 and out["marker_in_final"] else 1


if __name__ == "__main__":
    sys.exit(main())
