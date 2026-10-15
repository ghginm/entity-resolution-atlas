#!/usr/bin/env python3
"""AU-v1 trusted JSONL broker adapter — real Hermes CLI transport, zero tools to model.

Protocol: reads the frozen start message on stdin, attests on stdout, relays model
read_file requests to the harness broker, and emits the model's final answer. Stdout is
exclusively protocol JSONL; every diagnostic goes to stderr (discarded by the harness).

Transport: one fresh `hermes chat --query-file ... --oneshot --format stream-json`
process per model decision, full scenario transcript re-supplied each turn (stateless
selection calls). `--safe-mode` drops user config/rules/memory/skills/plugins;
`--toolsets <disabler>` selects a registered toolset that resolves to zero tools, so
the model is given no callable tool at all: the only channel to corpus content is this
adapter's stdout read_file requests and the broker's read_result lines. The tested
model therefore sees exactly: frozen prompt, scenario, settings, inventory, the
read_file contract, and prior broker excerpts — plus the runtime's minimal identity
scaffold. No filesystem/network/shell is exposed to the model.

Operator credential access: the adapter passes HERMES_HOME (argv --hermes-home) to the
child so the CLI resolves the operator's own authorized credentials. It never reads,
copies, prints, or forwards credential values; the child environment is otherwise
minimized.

Test-only hook: AU_ADAPTER_TRANSPORT_CMD (JSON argv template with $QUERY_FILE,
$RUN_BUDGET, $MODEL). The harness strips this variable, so operator-launched cohort
runs always use the real transport. Do not set it for anything counted as a model run.

Exit codes: 0 ok; 3 bad start input; 4 model protocol unrecoverable; 5 wall budget;
6 output budget/transport failure; 7 missing operator configuration.
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
import uuid

def log(msg):
    sys.stderr.write("[au-adapter] " + str(msg) + "\n")
    sys.stderr.flush()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


class Adapter:
    def __init__(self, out, args):
        self.out = out
        self.args = args
        self.msg_seq = 0

    def send(self, message):
        data = canonical(message).encode("utf-8")
        self.msg_seq += 1
        self.out.buffer.write(data)
        self.out.buffer.flush()
        self.out.flush()
        return len(data)

    def readline(self, deadline):
        """Bounded line read from broker stdin; None on clean EOF."""
        sel = selectors.DefaultSelector()
        sel.register(sys.stdin, selectors.EVENT_READ)
        buf = b""
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("broker stdin wall timeout")
                if not sel.select(remaining):
                    continue
                chunk = os.read(sys.stdin.fileno(), 8192)
                if not chunk:
                    return None
                buf += chunk
                if b"\n" in buf:
                    line, extra = buf.split(b"\n", 1)
                    if extra:
                        raise ValueError("unexpected pipelined input beyond one line")
                    return line
        finally:
            sel.close()


def extract_action(text):
    """Parse the model's decision: first JSON object with an 'action' key."""
    candidates = []
    stripped = text.strip()
    lines = [stripped] + [ln.strip() for ln in text.splitlines()]
    for ln in lines:
        cleaned = ln
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`").strip()
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:]
        if cleaned.startswith("{"):
            candidates.append(cleaned)
            candidates.append(ln[ln.find("{"):])
    for cand in candidates:
        for end in range(len(cand), 0, -1):
            try:
                value = json.loads(cand[:end])
            except (json.JSONDecodeError, UnicodeError):
                continue
            if isinstance(value, dict) and isinstance(value.get("action"), str):
                return value
            break
    # single fallback: whole-text balanced scan for the first parseable object
    start = text.find("{")
    while start != -1:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        value = json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
                    if isinstance(value, dict) and isinstance(value.get("action"), str):
                        return value
                    break
        start = text.find("{", start + 1)
    return None


def parse_transport_output(raw):
    """Return (text, exit_code, error, model_reported, tokens) from stream-json or plain."""
    text_out, exit_code, error, model_reported, tokens = None, None, None, None, {}
    saw_jsonl = False
    for line in raw.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        saw_jsonl = True
        if event.get("type") == "system" and event.get("subtype") == "init":
            model_reported = event.get("model")
        elif event.get("type") == "result":
            text_out = event.get("text")
            exit_code = event.get("exit_code")
            error = event.get("error")
            tokens = event.get("tokens") or {}
        elif event.get("type") == "assistant" and isinstance(event.get("text"), str):
            if text_out is None:
                text_out = event["text"]
    if not saw_jsonl:
        return raw, None, None, None, {}
    if text_out is None:
        # stream events present but no terminal result: treat the raw output itself as
        # the reply body (test stubs and providers that echo plain text land here).
        text_out = raw.strip()
    return text_out, exit_code, error, model_reported, tokens


def run_transport(argv, query_file, run_budget, model, env):
    cmd = [token.replace("$QUERY_FILE", query_file)
               .replace("$RUN_BUDGET", str(int(run_budget)))
               .replace("$MODEL", model) for token in argv]
    proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=max(5, int(run_budget) + 5),
                          env=env, cwd=os.getcwd(), start_new_session=True)
    raw = proc.stdout.decode("utf-8", "replace")
    text, exit_code, error, model_reported, tokens = parse_transport_output(raw)
    if proc.returncode != 0:
        log(f"transport rc={proc.returncode} stderr_tail={proc.stderr.decode('utf-8','replace')[-400:]!r}")
        return proc.returncode, raw, model_reported, tokens, "transport nonzero exit"
    if error:
        return 1, raw or "", model_reported, tokens, f"transport result error: {error}"
    if text is None:
        return 1, raw, model_reported, tokens, "no result event in transport output"
    return 0, text, model_reported, tokens, None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, help="authorized Hermes provider id")
    parser.add_argument("--hermes-bin", default=None, help="absolute path to hermes CLI")
    parser.add_argument("--hermes-home", default=None,
                        help="operator Hermes home holding authorized credentials (never read here)")
    parser.add_argument("--toolsets-disabler", default="bot_room",
                        help="registered toolset that resolves to zero tools (verified)")
    parser.add_argument("--model", default=None, help="override; default is the pinned start settings model")
    parser.add_argument("--identity-prefix", default="au-hermes-cli-jsonl")
    args = parser.parse_args()

    transport_cmd = os.environ.get("AU_ADAPTER_TRANSPORT_CMD")
    if transport_cmd:
        argv = json.loads(transport_cmd)
        transport_name = "TEST-OVERRIDE-stub"
    else:
        import shutil
        hermes_bin = args.hermes_bin or shutil.which("hermes")
        if not hermes_bin or not pathlib.Path(hermes_bin).is_file():
            log("FATAL: --hermes-bin required (authorized hermes CLI not found on PATH)")
            return 7
        if not args.hermes_home:
            log("FATAL: --hermes-home required so the CLI can use operator-authorized credentials; "
                "refusing to run without a declared credential home")
            return 7
        argv = [hermes_bin, "chat", "--query-file", "$QUERY_FILE", "--oneshot", "-Q",
                "--format", "stream-json", "--provider", args.provider, "-m", "$MODEL",
                "-t", args.toolsets_disabler, "--safe-mode", "--run-budget", "$RUN_BUDGET",
                "--source", "tool"]
        transport_name = "hermes-cli-oneshot-stream-json"

    adapter = Adapter(sys.stdout, args)
    workdir = tempfile.mkdtemp(prefix="au-adapter-turn-")
    transcript_path = pathlib.Path(workdir) / "transcript.txt"

    line = adapter.readline(time.monotonic() + 60)
    if line is None:
        log("FATAL: no start message")
        return 3
    if len(line) > 65536:
        log("FATAL: start line exceeds byte budget")
        return 3
    start = json.loads(line.decode("utf-8"))
    if start.get("type") != "start" or "settings" not in start or "inventory" not in start:
        log("FATAL: malformed start message")
        return 3
    settings = start["settings"]
    budgets = settings["budgets"]
    pinned = settings.get("model_settings", {}).get("model", "")
    if args.model and pinned and pinned != "PARENT_SELECTS_BEFORE_RUN" and args.model != pinned:
        log(f"FATAL: --model {args.model!r} conflicts with model pinned in start settings "
            f"{pinned!r}; refusing mid-run model substitution")
        return 7
    model = args.model or pinned
    model_source = ("start-settings" if pinned and pinned != "PARENT_SELECTS_BEFORE_RUN"
                    else "cli-override-fixture-only")
    if not model or model == "PARENT_SELECTS_BEFORE_RUN":
        log("FATAL: no pinned model in start settings and no --model override")
        return 7
    deadline = time.monotonic() + budgets["timeout_seconds"]

    identity = f"{args.identity_prefix}/{args.provider}/{model}/pid{os.getpid()}-{uuid.uuid4().hex[:8]}"
    adapter.send({"type": "ready", "identity": identity, "fresh_context": True, "broker_only": True,
                  "settings_sha256": start["settings_sha256"],
                  "attest": {"transport": transport_name, "transport_argv": argv,
                             "provider_requested": args.provider, "model_pinned": model,
                             "model_source": model_source,
                             "toolsets_given_to_model": [], "toolsets_disabler": args.toolsets_disabler,
                             "safe_mode": True, "credential_home_declared": args.hermes_home or "stub",
                             "model_visible_context": "start JSON + adapter-authored protocol line + own prior replies + broker read_result excerpts only",
                             "settings_enforcement": {
                                 "model": "pinned via start settings and transport -m",
                                 "temperature": "NOT enforceable through the authorized Hermes CLI (no sampling flag; request_overrides require user config which --safe-mode ignores)",
                                 "seed": "NOT enforceable: Hermes CLI has no seed flag and the OpenAI Responses/Codex API exposes no seed parameter",
                                 "max_output_tokens": "NOT enforceable through the CLI; provider defaults apply"}}})
    log(f"ready; model={model} provider={args.provider} pid={os.getpid()}")

    instruction = (
        "You are an independently spawned benchmark agent with NO tools except a broker file reader. "
        "The next JSON object is the complete frozen start context (scenario, prompt, settings, budgets, "
        "inventory, read_file contract). Decide your next move and reply with EXACTLY one JSON object and "
        "nothing else, one of:\n"
        '{"action":"read_file","path":"<inventory path>","offset":<int chars >=0>,"length":<int 1..max_chunk_chars>}\n'
        '{"action":"final","text":"<complete recommendation, <=max_final_chars>"}\n'
        "No markdown fences, no prose outside the JSON string. After a broker result, continue with either "
        "another read_file or the final answer. You may read many files across turns; each read returns one chunk."
    )
    history = [instruction + "\n\nSTART_JSON:\n" + json.dumps(start, ensure_ascii=False, sort_keys=True)]
    last_remaining = None
    parse_failures = 0
    transport_failures = 0
    turn = 0
    usage_totals = {"input": 0, "output": 0, "total": 0, "calls": 0}
    last_model_reported = None

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 8:
            log("FATAL: wall budget exhausted before final")
            return 5
        if remaining <= 25:
            history.append("ADAPTER NOTE: wall budget nearly exhausted. Reply NOW with the final JSON object only.")
        transcript = "\n\n".join(history)
        transcript_path.write_text(transcript, encoding="utf-8")
        run_budget = max(6, int(remaining) - 6)
        turn += 1
        log(f"turn {turn}: transcript_chars={len(transcript)} run_budget={run_budget}")
        rc, text, model_reported, tokens, err = run_transport(
            argv, str(transcript_path), run_budget, model,
            dict(os.environ) if transport_cmd else build_child_env(args))
        if model_reported:
            last_model_reported = model_reported
            if model_reported != model:
                log(f"FATAL: transport resolved to {model_reported!r}, not the pinned {model!r} "
                    "(silent provider fallback); refusing to attest the wrong model")
                return 6
        for key in ("input", "output", "total"):
            usage_totals[key] += int(tokens.get(key) or 0)
        usage_totals["calls"] += 1
        if rc != 0:
            transport_failures += 1
            log(f"transport failure {transport_failures}: {err}")
            if transport_failures >= 2 or deadline - time.monotonic() <= 30:
                log("FATAL: transport unavailable; failing run honestly (no simulated output)")
                return 6
            time.sleep(2)
            continue
        transport_failures = 0
        history.append("MODEL_REPLY:\n" + text)
        action = extract_action(text)
        if action is None:
            parse_failures += 1
            if parse_failures > 2:
                log("FATAL: model never produced a valid action JSON")
                return 4
            history.append("ADAPTER NOTE: reply rejected — must be EXACTLY one JSON object "
                           '{"action":"read_file"...} or {"action":"final"...}. Try again.')
            continue
        act = action.get("action")
        if act == "final":
            body = action.get("text")
            if not isinstance(body, str) or not body.strip():
                parse_failures += 1
                if parse_failures > 2:
                    return 4
                history.append('ADAPTER NOTE: final text must be non-empty. {"action":"final","text":"..."}')
                continue
            if len(body) > budgets["max_final_chars"]:
                log(f"FATAL: final {len(body)} chars exceeds max_final_chars={budgets['max_final_chars']}; "
                    "trimming model output is not allowed")
                return 6
            nbytes = len(canonical({"type": "final", "text": body}).encode("utf-8"))
            if nbytes - 1 > budgets["max_message_bytes"]:
                log(f"FATAL: final line {nbytes} bytes exceeds max_message_bytes")
                return 6
            adapter.send({"type": "final", "text": body})
            log(f"final sent chars={len(body)} turns={turn} usage={usage_totals} "
                f"model_reported={last_model_reported}")
            return 0
        if act == "read_file":
            path = action.get("path")
            offset = action.get("offset")
            length = action.get("length")
            ok = (isinstance(path, str) and type(offset) is int and offset >= 0
                  and type(length) is int and 1 <= length <= budgets["max_chunk_chars"])
            if not ok:
                history.append("ADAPTER NOTE: read request rejected before the broker — path must be a "
                               "string, offset an int >= 0, length an int in 1..max_chunk_chars. "
                               "Send a corrected read_file or answer final.")
                continue
            if last_remaining is not None and (last_remaining.get("reads", 1) <= 0
                                               or last_remaining.get("read_attempts", 1) <= 0
                                               or last_remaining.get("read_chars", 1) <= 0):
                history.append("ADAPTER NOTE: broker read budget exhausted. Reply with the final JSON object only.")
                continue
            rid = f"r{turn}-{uuid.uuid4().hex[:6]}"
            nbytes = len(canonical({"type": "read_file", "request_id": rid, "path": path,
                                    "offset": offset, "length": length}).encode("utf-8"))
            if nbytes - 1 > budgets["max_message_bytes"]:
                log("FATAL: read request line exceeds byte budget")
                return 6
            adapter.send({"type": "read_file", "request_id": rid, "path": path,
                          "offset": offset, "length": length})
            rline = adapter.readline(deadline)
            if rline is None:
                log("FATAL: broker closed before read_result")
                return 6
            result = json.loads(rline.decode("utf-8"))
            if result.get("request_id") != rid:
                log(f"FATAL: read_result id mismatch {result.get('request_id')!r} != {rid!r}")
                return 6
            last_remaining = result.get("remaining") or {}
            history.append("BROKER_READ_RESULT:\n" + json.dumps(result, ensure_ascii=False))
            log(f"read {path} offset={offset} chars={len(result.get('content') or '')} "
                f"error={result.get('error')} remaining={last_remaining}")
            continue
        parse_failures += 1
        if parse_failures > 2:
            return 4
        history.append('ADAPTER NOTE: unknown action. Use "read_file" or "final".')


def build_child_env(args):
    env = {key: value for key, value in
           (("PATH", os.environ.get("PATH", "/usr/bin:/bin")),
            ("LANG", os.environ.get("LANG", "C.UTF-8")),
            ("HOME", os.environ.get("HOME", "/tmp")),
            ("TMPDIR", os.environ.get("TMPDIR", "/tmp")),
            ("PYTHONIOENCODING", "utf-8"))}
    if args.hermes_home:
        env["HERMES_HOME"] = args.hermes_home
    return env


if __name__ == "__main__":
    try:
        sys.exit(main())
    except TimeoutError as exc:
        log(f"FATAL: {exc}")
        sys.exit(5)
    except BrokenPipeError:
        log("FATAL: broker pipe closed")
        sys.exit(6)
    except json.JSONDecodeError as exc:
        log(f"FATAL: JSONL parse error: {exc}")
        sys.exit(3)
