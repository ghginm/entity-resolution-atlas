"""Adapter protocol tests — broker-side simulation of the frozen AU-v1 JSONL contract.

These exercise validation/agent-utility/adapters/hermes_cli_jsonl_adapter.py against a
scripted FAKE transport (test-only stand-in for the model). No provider calls, no model
results; fixture replies validate framing/attestation/budget behavior only.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters" / "hermes_cli_jsonl_adapter.py"
STUB = pathlib.Path(__file__).parent / "transport_stub.py"

BUDGETS = {"max_read_attempts": 24, "max_reads": 16, "max_read_chars": 64000,
           "max_chunk_chars": 8000, "max_initial_chars": 24000, "max_final_chars": 24000,
           "max_message_bytes": 65536, "timeout_seconds": 60}


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def make_start(budgets=BUDGETS):
    settings = {"protocol_version": "atlas-utility-jsonl-1",
                "model_settings": {"model": "stub/stub-model", "temperature": 0,
                                   "seed": 1729, "max_output_tokens": 4500},
                "budgets": budgets, "layers": ["L0", "L1", "L2", "L3"]}
    start = {"type": "start", "protocol_version": settings["protocol_version"],
             "scenario": {"scenario_id": "STUB-01", "project": "fictional probe", "known_facts": ["x"]},
             "prompt": "FROZEN STUB PROMPT", "settings": settings,
             "settings_sha256": hashlib.sha256(canonical(settings)).hexdigest(),
             "inventory": [{"path": "index/L0.json", "layer": "L0", "bytes": 20},
                           {"path": "solutions/a.md", "layer": "L2", "bytes": 12}],
             "read_file": {"request": {"type": "read_file"}, "response": "read_result"}}
    return start


class FakeBroker:
    """Minimal harness-protocol counterparty: start in, ready/reads/final out."""

    def __init__(self, replies, inventory=None, budgets=BUDGETS):
        # replies: list of transport stdout strings consumed one per model call
        workdir = tempfile.mkdtemp(prefix="au-adapter-test-")
        (pathlib.Path(workdir) / "replies.json").write_text(json.dumps(replies), encoding="utf-8")
        self.inventory = inventory if inventory is not None else {
            "index/L0.json": "L0-INDEX-CONTENT", "solutions/a.md": "CARD-CONTENT"}
        self.budgets = budgets
        self.attempts = self.chars = self.successes = 0
        self.ids = set()
        proc_env = dict(os.environ, AU_STUB_REPLIES=str(pathlib.Path(workdir) / "replies.json"),
                        AU_STUB_LOG=str(pathlib.Path(workdir) / "calls.jsonl"))
        self.stub_log = proc_env["AU_STUB_LOG"]
        # transport template: real python + stub, model/provider placeholders ignored by stub
        proc_env["AU_ADAPTER_TRANSPORT_CMD"] = json.dumps(
            [sys.executable, str(STUB), "$QUERY_FILE", "$RUN_BUDGET", "$MODEL"])
        self.proc = subprocess.Popen(
            [sys.executable, str(ADAPTER), "--provider", "stub", "--hermes-bin", str(STUB)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=proc_env, text=True, encoding="utf-8")
        self.start = make_start(budgets)
        self.proc.stdin.write(canonical(self.start).decode("utf-8"))
        self.proc.stdin.flush()

    def read_line(self):
        line = self.proc.stdout.readline()
        if not line:
            raise AssertionError("adapter stdout closed unexpectedly; stderr=" + self.proc.stderr.read())
        assert len(line.encode("utf-8")) <= self.budgets["max_message_bytes"], "outgoing line over byte budget"
        return json.loads(line)

    def serve(self, content=None, error=None, path="index/L0.json", offset=0, length=10):
        self.attempts += 1
        got = content if content is not None else self.inventory.get(path, "")
        body = got[offset:offset + length]
        if error is None:
            self.successes += 1
            self.chars += len(body)
        result = {"type": "read_result", "request_id": self.pending_id, "path": path, "content": body,
                  "error": error, "remaining": {"read_attempts": self.budgets["max_read_attempts"] - self.attempts,
                                                "reads": self.budgets["max_reads"] - self.successes,
                                                "read_chars": self.budgets["max_read_chars"] - self.chars}}
        self.proc.stdin.write(canonical(result).decode("utf-8"))
        self.proc.stdin.flush()

    def wait(self, timeout=30):
        try:
            return self.proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            return "TIMEOUT"

    def stderr_text(self):
        try:
            return self.proc.stderr.read()
        except Exception:
            return ""

    def calls(self):
        if not os.path.exists(self.stub_log):
            return []
        with open(self.stub_log, encoding="utf-8") as handle:
            return [json.loads(l) for l in handle if l.strip()]

    def query_text(self, index):
        with open(self.calls()[index]["query_file"], encoding="utf-8") as handle:
            return handle.read()


class ReadyAttestation(unittest.TestCase):
    def test_ready_attestation_matches_start(self):
        replies = [json.dumps({"action": "final", "text": "done"})]
        b = FakeBroker(replies=replies)
        ready = b.read_line()
        self.assertEqual(ready["type"], "ready")
        self.assertIs(ready["fresh_context"], True)
        self.assertIs(ready["broker_only"], True)
        self.assertEqual(ready["settings_sha256"], b.start["settings_sha256"])
        self.assertIsInstance(ready["identity"], str)
        self.assertTrue(ready["identity"].strip())
        self.assertNotEqual(ready["identity"], "atlas-v11-author-hermes")
        # honest attestation extras required by the frozen independence clause
        extras = json.dumps(ready)
        self.assertIn("stub/stub-model", extras)
        self.assertEqual(b.wait(), 0)

    def test_cli_model_substitution_against_pinned_start_is_refused(self):
        start = make_start()
        work = tempfile.mkdtemp(prefix="au-sub-")
        proc = subprocess.Popen(
            [sys.executable, str(ADAPTER), "--provider", "stub", "--hermes-bin", "x",
             "--model", "attacker/model"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=dict(os.environ, AU_ADAPTER_TRANSPORT_CMD="[]"), text=True, encoding="utf-8")
        proc.stdin.write(canonical(start).decode("utf-8"))
        proc.stdin.close()
        self.assertNotEqual(proc.wait(timeout=15), 0)
        self.assertEqual(proc.stdout.read().strip(), "")  # dies before any attestation


class HappyPath(unittest.TestCase):
    def test_read_relay_and_final(self):
        replies = [json.dumps({"action": "read_file", "request_id": "m1", "path": "index/L0.json",
                               "offset": 0, "length": 5}),
                   json.dumps({"action": "final", "text": "RECOMMENDATION BODY"})]
        b = FakeBroker(replies=replies)
        b.read_line()  # ready
        req = b.read_line()
        self.assertEqual(set(req), {"type", "request_id", "path", "offset", "length"})
        self.assertEqual(req["type"], "read_file")
        self.assertEqual(req["path"], "index/L0.json")
        b.pending_id = req["request_id"]
        b.serve()
        fin = b.read_line()
        self.assertEqual(fin, {"type": "final", "text": "RECOMMENDATION BODY"})
        self.assertEqual(b.wait(), 0)
        # broker read result must have been fed back to the model transcript (2 transport calls)
        self.assertEqual(len(b.calls()), 2)


class ModelTurnContext(unittest.TestCase):
    def test_start_json_and_read_result_visible_to_model(self):
        replies = [json.dumps({"action": "read_file", "request_id": "m1", "path": "solutions/a.md",
                               "offset": 0, "length": 4}),
                   json.dumps({"action": "final", "text": "ok"})]
        b = FakeBroker(replies=replies)
        b.read_line()
        req = b.read_line()
        b.pending_id = req["request_id"]
        b.serve(content="CARD-CONTENT", path="solutions/a.md")
        b.read_line()
        b.wait()
        first_query = b.query_text(0)
        self.assertIn("FROZEN STUB PROMPT", first_query)
        self.assertIn("index/L0.json", first_query)  # inventory visible
        self.assertIn(b.start["settings_sha256"], first_query)
        second_query = b.query_text(1)
        self.assertIn("CARD", second_query)  # broker excerpt relayed
        self.assertNotIn("evaluator-only", second_query.lower())


class BudgetGuard(unittest.TestCase):
    def test_oversize_chunk_not_forwarded(self):
        replies = [json.dumps({"action": "read_file", "request_id": "m1", "path": "index/L0.json",
                               "offset": 0, "length": BUDGETS["max_chunk_chars"] + 1}),
                   json.dumps({"action": "final", "text": "after correction"})]
        b = FakeBroker(replies=replies)
        b.read_line()
        fin = b.read_line()  # no read_file forwarded; error fed back to model, then final
        self.assertEqual(fin["type"], "final")
        self.assertEqual(len(b.calls()), 2)
        self.assertEqual(b.wait(), 0)

    def test_exhausted_success_budget_steers_to_final(self):
        tiny = dict(BUDGETS, max_reads=1, max_read_attempts=2)
        replies = [json.dumps({"action": "read_file", "request_id": "m1", "path": "index/L0.json",
                               "offset": 0, "length": 2}),
                   json.dumps({"action": "read_file", "request_id": "m2", "path": "index/L0.json",
                               "offset": 2, "length": 2}),
                   json.dumps({"action": "final", "text": "steered"})]
        b = FakeBroker(replies=replies, budgets=tiny)
        b.read_line()
        req = b.read_line()
        b.pending_id = req["request_id"]
        b.serve(content="ABCD", length=2)          # success 1 of 1
        fin = b.read_line()                        # second read must NOT hit the broker fatally
        self.assertEqual(fin["type"], "final")
        self.assertEqual(b.wait(), 0)


class DeniedReadRelay(unittest.TestCase):
    def test_broker_error_returned_to_model_and_retry_works(self):
        replies = [json.dumps({"action": "read_file", "request_id": "m1", "path": "evil/../../keys.json",
                               "offset": 0, "length": 3}),
                   json.dumps({"action": "read_file", "request_id": "m2", "path": "index/L0.json",
                               "offset": 0, "length": 3}),
                   json.dumps({"action": "final", "text": "recovered"})]
        b = FakeBroker(replies=replies)
        b.read_line()
        bad = b.read_line()
        b.pending_id = bad["request_id"]
        b.serve(error="path not in allowlisted inventory")
        good = b.read_line()
        b.pending_id = good["request_id"]
        b.serve()
        fin = b.read_line()
        self.assertEqual(fin["text"], "recovered")
        self.assertEqual(b.wait(), 0)


class ProtocolErrors(unittest.TestCase):
    def test_garbage_reply_gets_one_correction_then_fails(self):
        replies = ["I will just chat normally, no JSON.", "still not json {", "never"]
        b = FakeBroker(replies=replies)
        b.read_line()
        code = b.wait()
        self.assertNotEqual(code, 0)
        self.assertNotIn("final", [c for c in b.calls()])  # no final line was ever emitted
        out = b.proc.stdout.read()
        self.assertTrue(all(not json.loads(l).get("type") == "final" for l in out.splitlines() if l.strip()))

    def test_final_over_char_budget_fails_closed(self):
        huge = "字" * (BUDGETS["max_final_chars"] + 1)
        b = FakeBroker(replies=[json.dumps({"action": "final", "text": huge})])
        b.read_line()
        code = b.wait()
        self.assertNotEqual(code, 0)
        remaining = b.proc.stdout.read().strip()
        self.assertTrue(all(json.loads(l).get("type") != "final" for l in remaining.splitlines()) if remaining else True)

    def test_final_over_line_byte_budget_fails_closed(self):
        # 21850 CJK chars: under max_final_chars (24000) but >65536 UTF-8 bytes on the wire line
        wide = "\u5b57" * 21850
        b = FakeBroker(replies=[json.dumps({"action": "final", "text": wide})])
        b.read_line()
        code = b.wait()
        self.assertNotEqual(code, 0)
        remaining = b.proc.stdout.read().strip()
        self.assertTrue(all(json.loads(l).get("type") != "final" for l in remaining.splitlines())
                        if remaining else True)


class TransportFailure(unittest.TestCase):
    def test_nonzero_transport_aborts_not_fakes(self):
        # stub exits nonzero when reply text starts with "__TRANSPORT_FAIL__"
        b = FakeBroker(replies=["__TRANSPORT_FAIL__ provider 429"])
        b.read_line()
        code = b.wait()
        self.assertNotEqual(code, 0)
        out = b.proc.stdout.read()
        self.assertTrue(all(json.loads(l).get("type") != "final" for l in out.splitlines() if l.strip()))

    def test_silent_model_fallback_aborts(self):
        # real stream-json shape, but init reports a DIFFERENT model than pinned
        reply = ('{"type":"system","subtype":"init","model":"someone/elses-model"}\n'
                 '{"type":"result","exit_code":0,"text":"{\\"action\\":\\"final\\",\\"text\\":\\"ok\\"}","tokens":{}}')
        b = FakeBroker(replies=[reply])
        b.read_line()
        code = b.wait()
        self.assertNotEqual(code, 0)
        out = b.proc.stdout.read()
        self.assertTrue(all(json.loads(l).get("type") != "final" for l in out.splitlines() if l.strip()))

    def test_matching_model_stream_events_happy_path(self):
        reply = ('{"type":"system","subtype":"init","model":"stub/stub-model"}\n'
                 '{"type":"result","exit_code":0,"text":"{\\"action\\":\\"final\\",\\"text\\":\\"clean\\"}","tokens":{"input":9,"output":2}}')
        b = FakeBroker(replies=[reply])
        b.read_line()
        fin = b.read_line()
        self.assertEqual(fin["text"], "clean")
        self.assertEqual(b.wait(), 0)


if __name__ == "__main__":
    unittest.main()
