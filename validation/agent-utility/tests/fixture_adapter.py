"""Deterministic protocol fixture ONLY, never an independent agent/model result."""
import json
import os
import sys
import time
start = json.loads(sys.stdin.readline())
mode = sys.argv[1]
def send(value):
    print(json.dumps(value), flush=True)
if mode == "crash":
    sys.exit(7)
if mode == "bad-json":
    print("not json", flush=True)
    sys.exit(0)
if mode == "oversize":
    print("x" * 70000, flush=True)
    sys.exit(0)
if mode == "timeout":
    time.sleep(5)
    sys.exit(0)
if mode != "no-ready":
    send({"type": "ready", "identity": "HARNESS_TEST_FIXTURE_NOT_A_MODEL", "fresh_context": True,
          "broker_only": True, "settings_sha256": start["settings_sha256"]})
if mode in {"ok", "extra-output"}:
    send({"type": "read_file", "request_id": "r1", "path": "index/L0.json", "offset": 0, "length": 100})
    response = json.loads(sys.stdin.readline())
    assert response["error"] is None
send({"type": "final", "text": "HARNESS FIXTURE ONLY; NO MODEL RESULT. PID=" + str(os.getpid())})
if mode == "extra-output":
    print("extra", flush=True)
