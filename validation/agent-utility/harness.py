#!/usr/bin/env python3
"""AU-v1 independent agent benchmark; Python standard library only."""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
FREEZE_SHA256 = "bd2e57dc2d96f40fb65a6fd4ac2d9a5e6000411b91a5dc1ca47071a8bed3104c"
DIMENSIONS = ("problem_understanding", "retrieval_relevance", "alternative_quality",
              "technical_reasoning", "risk_identification", "experiment_quality",
              "evidence_discipline", "efficiency")
SCENARIOS = tuple(f"AU-{i:02}" for i in range(1, 9))


class BenchmarkError(ValueError):
    """An invalid or ineligible artifact/protocol operation."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def verify_freeze(root=ROOT):
    root = pathlib.Path(root)
    path = root / "freeze-manifest.json"
    if digest(path.read_bytes()) != FREEZE_SHA256:
        raise BenchmarkError("freeze manifest changed: do not refreeze this cohort")
    manifest = load(path)
    for name, expected in manifest["files"].items():
        file = root / name
        if file.is_symlink() or not file.is_file() or digest(file.read_bytes()) != expected:
            raise BenchmarkError("frozen artifact changed: " + name)
    original = load(root / "baseline/atlas-v1-baseline-hashes.json")
    if digest(json.dumps(original, sort_keys=True).encode()) != manifest["baseline_sorted_manifest_sha256"]:
        raise BenchmarkError("original baseline manifest mismatches preserved anchor")
    return manifest


def validate_schema(value, schema, where="$",):
    """Validate the explicit JSON-schema subset used by the three frozen schemas."""
    import re
    types = {"object": dict, "array": list, "string": str, "integer": int,
             "boolean": bool, "null": type(None)}
    if "type" in schema:
        allowed = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(type(value) is types[t] for t in allowed):
            raise BenchmarkError(where + ": wrong JSON type")
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        raise BenchmarkError(where + ": const mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise BenchmarkError(where + ": invalid enum")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        if set(schema.get("required", [])) - set(value):
            raise BenchmarkError(where + ": required keys missing")
        if schema.get("additionalProperties") is False and set(value) - set(props):
            raise BenchmarkError(where + ": unexpected keys")
        if len(value) < schema.get("minProperties", 0):
            raise BenchmarkError(where + ": too few properties")
        for key, item in value.items():
            if key in props:
                validate_schema(item, props[key], where + "." + key)
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise BenchmarkError(where + ": too few items")
        for i, item in enumerate(value):
            validate_schema(item, schema.get("items", {}), f"{where}[{i}]")
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise BenchmarkError(where + ": string too short")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise BenchmarkError(where + ": pattern mismatch")
    elif type(value) is int:
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            raise BenchmarkError(where + ": integer outside bounds")


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_new(path, value):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as file:
        file.write(canonical(value))


def safe_path(name):
    p = pathlib.PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name and p.as_posix() == name


def layer_for(name):
    if not safe_path(name):
        return None
    parts = pathlib.PurePosixPath(name).parts
    if not name.endswith(".md"):
        return None
    if any(term in name.lower() for term in ("answer", "coverage", "change-log", "implementation-plan", "scenario-stress-test")):
        return None
    if parts[0] in {"decisions", "solutions", "architectures", "evaluation"} and len(parts) > 1:
        return "L2"
    if parts[:2] == ("research", "hypotheses") and len(parts) > 2:
        return "L2"
    if parts[:2] == ("taxonomy", "domains") or name in {
            "taxonomy/overview.md", "taxonomy/architecture-dimensions.md", "taxonomy/module-contracts.md"}:
        return "L1"
    if parts[0] == "deep-dives" or name in {"references/bibliography.md", "references/evidence-policy.md"}:
        return "L3"
    return None


def card_metadata(text, path):
    """Read only scalar discovery metadata, not arbitrary YAML (no dependency)."""
    import re
    if not text.startswith("---\n") or "\n---" not in text[4:]:
        raise BenchmarkError("not a card: " + path)
    front = text.split("\n---", 1)[0][4:]
    result = {"path": path}
    for key in ("id", "title", "type", "domain", "summary"):
        match = re.search(r"^" + key + r":\s*(.*)$", front, re.M)
        if not match:
            raise BenchmarkError("missing metadata " + key + ": " + path)
        val = match.group(1).strip()
        if val in {">", ">-", "|", "|-"}:
            lines = []
            for line in front[match.end():].splitlines()[1:]:
                if line and not line.startswith(" "):
                    break
                lines.append(line.strip())
            val = " ".join(lines).strip()
        elif val.startswith('"'):
            try:
                val = json.loads(val)
            except json.JSONDecodeError as exc:
                raise BenchmarkError("unsupported discovery scalar: " + path) from exc
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1].replace("''", "'")
        result["applicability" if key == "summary" else key] = val[:180] if key == "summary" else val
    return result


def verify_baseline(source):
    source = pathlib.Path(source)
    expected = load(ROOT / "baseline/atlas-v1-baseline-hashes.json")
    actual = {}
    for file in source.rglob("*"):
        if file.is_symlink():
            raise BenchmarkError("baseline symlink forbidden")
        if file.is_file():
            actual[file.relative_to(source).as_posix()] = digest(file.read_bytes())
    if actual != expected:
        raise BenchmarkError("v1 snapshot differs from preserved full baseline manifest")


def prepare(source, out, label, layers=("L0", "L1", "L2", "L3")):
    verify_freeze()
    out = pathlib.Path(out)
    if out.exists():
        raise BenchmarkError("new corpus output directory required; never overwrite")
    if not layers or set(layers) - {"L0", "L1", "L2", "L3"} or len(set(layers)) != len(layers):
        raise BenchmarkError("invalid layer selection")
    if label == "v1":
        verify_baseline(source)
    if label == "no-atlas" and source is not None:
        raise BenchmarkError("no-atlas must have no source")
    files, cards = {}, []
    if source is not None:
        source = pathlib.Path(source).resolve()
        if out.resolve().is_relative_to(source) and "validation" not in out.resolve().relative_to(source).parts:
            raise BenchmarkError("put output in validation/ or outside source")
        for file in sorted(source.rglob("*.md")):
            name = file.relative_to(source).as_posix()
            layer = layer_for(name)
            if layer is None:
                continue
            if any(parent.is_symlink() for parent in (file, *file.parents) if parent != source.parent):
                raise BenchmarkError("corpus symlink forbidden: " + name)
            data = file.read_bytes()
            if layer == "L2":
                cards.append(card_metadata(data.decode("utf-8"), name))
            if layer not in layers:
                continue
            target = out / "files" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            files[name] = {"layer": layer, "bytes": len(data), "sha256": digest(data), "generated": False}
    if len({card["id"] for card in cards}) != len(cards):
        raise BenchmarkError("duplicate corpus card IDs")
    if source is not None and "L0" in layers:
        name = "index/L0.json"
        data = canonical({"description": "Discovery metadata; applicability is not evidence. Follow canonical paths.",
                          "cards": sorted(cards, key=lambda card: card["id"])})
        target = out / "files" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        files[name] = {"layer": "L0", "bytes": len(data), "sha256": digest(data), "generated": True}
    manifest = {"schema_version": "1.0", "label": label, "layers": list(layers),
                "freeze_manifest_sha256": FREEZE_SHA256, "files": files,
                "card_ids": sorted(card["id"] for card in cards)}
    write_new(out / "corpus-manifest.json", manifest)
    verify_corpus(out)
    return manifest


def verify_corpus(out):
    out = pathlib.Path(out)
    manifest = load(out / "corpus-manifest.json")
    if (manifest["label"] == "v1" and manifest["layers"] == ["L0", "L1", "L2", "L3"]
            and digest((out / "corpus-manifest.json").read_bytes()) !=
            "e1ade517e405ac79fa93bc700dfe098848a1517dcbecf81080e307d2b30b8772"):
        raise BenchmarkError("preserved v1 corpus manifest changed")
    if manifest["freeze_manifest_sha256"] != FREEZE_SHA256:
        raise BenchmarkError("corpus has different freeze anchor")
    actual = {file.relative_to(out / "files").as_posix() for file in (out / "files").rglob("*") if file.is_file()}
    if actual != set(manifest["files"]):
        raise BenchmarkError("corpus files added or removed")
    for name, meta in manifest["files"].items():
        if not safe_path(name) or meta["layer"] not in manifest["layers"]:
            raise BenchmarkError("invalid corpus manifest entry")
        if name != "index/L0.json" and layer_for(name) != meta["layer"]:
            raise BenchmarkError("corpus allowlist violation: " + name)
        file = out / "files" / name
        if any(parent.is_symlink() for parent in (file, *file.parents)):
            raise BenchmarkError("corpus symlink forbidden")
        data = file.read_bytes()
        if digest(data) != meta["sha256"] or len(data) != meta["bytes"]:
            raise BenchmarkError("corpus file hash/size mismatch: " + name)
    return manifest



def execution_settings(path=None):
    base = load(ROOT / "settings.json")
    if path is None:
        return base
    chosen = load(path)
    permitted = json.loads(json.dumps(base))
    model = chosen.get("model_settings", {}).get("model")
    if not isinstance(model, str) or not model.strip() or model == "PARENT_SELECTS_BEFORE_RUN":
        raise BenchmarkError("pin a real model identity in execution settings")
    permitted["model_settings"]["model"] = model
    if chosen != permitted:
        raise BenchmarkError("this cohort allows only model identity selection; other settings are frozen")
    return chosen


def make_start(corpus, sid, settings):
    if sid not in SCENARIOS:
        raise BenchmarkError("unknown scenario")
    manifest = verify_corpus(corpus)
    scenario = load(ROOT / "inputs" / (sid + ".json"))
    validate_schema(scenario, load(ROOT / "schemas/scenario.schema.json"))
    start = {"type": "start", "protocol_version": settings["protocol_version"],
             "scenario": scenario, "prompt": (ROOT / "prompt.txt").read_text(encoding="utf-8"),
             "settings": {key: value for key, value in settings.items() if key != "adapter_contract"},
             "settings_sha256": digest(canonical(settings)),
             "inventory": [{"path": name, "layer": meta["layer"], "bytes": meta["bytes"]}
                           for name, meta in sorted(manifest["files"].items())],
             "read_file": {"request": {"type": "read_file", "request_id": "unique string", "path": "inventory path",
                                       "offset": "integer Unicode character offset >= 0",
                                       "length": "integer characters 1..max_chunk_chars"},
                           "response": "read_result with content/error and remaining budgets"}}
    if len(canonical(start).decode("utf-8")) > settings["budgets"]["max_initial_chars"]:
        raise BenchmarkError("initial context exceeds frozen character budget")
    return start


class ReadBroker:
    def __init__(self, corpus, budgets):
        self.corpus = pathlib.Path(corpus)
        self.manifest = verify_corpus(corpus)
        self.budgets = budgets
        self.logs = []
        self.attempts = self.chars = self.successes = 0
        self.ids = set()

    def read(self, request):
        self.attempts += 1
        name = request.get("path", "")
        rid = request.get("request_id", "")
        offset = request.get("offset", -1)
        length = request.get("length", -1)
        content, error, fatal = "", None, False
        if self.attempts > self.budgets["max_read_attempts"]:
            error, fatal = "read-attempt budget exceeded", True
        elif type(length) is int and length > self.budgets["max_chunk_chars"]:
            error, fatal = "read-chunk character budget exceeded", True
        elif (not isinstance(name, str) or not isinstance(rid, str) or not rid or rid in self.ids
              or type(offset) is not int or type(length) is not int or offset < 0
              or not 1 <= length <= self.budgets["max_chunk_chars"]):
            error = "invalid read request or repeated request_id"
        elif not safe_path(name) or name not in self.manifest["files"]:
            error = "path not in allowlisted inventory"
        elif self.successes >= self.budgets["max_reads"]:
            error, fatal = "successful-read budget exceeded", True
        else:
            file = self.corpus / "files" / name
            data = file.read_bytes()
            if file.is_symlink() or digest(data) != self.manifest["files"][name]["sha256"]:
                error, fatal = "corpus changed during run", True
            else:
                content = data.decode("utf-8")[offset:offset + length]
                if self.chars + len(content) > self.budgets["max_read_chars"]:
                    content, error, fatal = "", "read-character budget exceeded", True
                else:
                    self.successes += 1
                    self.chars += len(content)
        self.ids.add(str(rid))
        self.logs.append({"request_id": str(rid), "path": str(name),
                          "layer": self.manifest["files"][name]["layer"] if error is None else "denied",
                          "offset": offset if type(offset) is int else -1,
                          "requested_length": length if type(length) is int else -1,
                          "returned_chars": len(content), "content_sha256": digest(content.encode("utf-8")),
                          "content": content, "error": error})
        if fatal:
            raise BenchmarkError(error)
        return {"type": "read_result", "request_id": str(rid), "path": str(name), "content": content,
                "error": error, "remaining": {"read_attempts": max(0, self.budgets["max_read_attempts"] - self.attempts),
                                              "reads": self.budgets["max_reads"] - self.successes,
                                              "read_chars": self.budgets["max_read_chars"] - self.chars}}


class LineReader:
    """Bounded nonblocking JSONL read: no blocking readline on partial lines."""
    def __init__(self, stream, limit, deadline):
        import selectors
        self.stream, self.limit, self.deadline = stream, limit, deadline
        self.buffer = b""
        self.selector = selectors.DefaultSelector()
        self.selector.register(stream, selectors.EVENT_READ)

    def line(self):
        import os
        import time
        while True:
            if b"\n" in self.buffer:
                line, self.buffer = self.buffer.split(b"\n", 1)
                if len(line) > self.limit:
                    raise BenchmarkError("adapter message byte budget exceeded")
                return line
            if len(self.buffer) > self.limit:
                raise BenchmarkError("adapter message byte budget exceeded")
            remaining = self.deadline - time.monotonic()
            if remaining <= 0 or not self.selector.select(remaining):
                raise BenchmarkError("adapter wall timeout")
            data = os.read(self.stream.fileno(), 8192)
            if not data:
                if self.buffer:
                    raise BenchmarkError("unterminated JSONL message")
                return None
            self.buffer += data

    def close(self):
        self.selector.close()


def utc_now():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def run_scenario(corpus, sid, settings, command=None, dry_run=False):
    import os
    import signal
    import subprocess
    import tempfile
    import time
    import uuid
    verify_freeze()
    manifest = verify_corpus(corpus)
    broker = ReadBroker(corpus, settings["budgets"])
    result = {"schema_version": "1.0", "run_id": str(uuid.uuid4()), "scenario_id": sid,
              "corpus_label": manifest["label"], "status": "prepared" if dry_run else "unexecuted",
              "error": "dry-run; no adapter invoked" if dry_run else "no model adapter configured",
              "manifest_sha256": FREEZE_SHA256, "harness_sha256": digest(pathlib.Path(__file__).read_bytes()),
              "corpus_sha256": digest((pathlib.Path(corpus) / "corpus-manifest.json").read_bytes()),
              "settings_sha256": digest(canonical(settings)),
              "scenario_sha256": digest((ROOT / "inputs" / (sid + ".json")).read_bytes()),
              "prompt_sha256": digest((ROOT / "prompt.txt").read_bytes()),
              "started_at": utc_now(), "finished_at": "pending", "adapter": {"command": command, "settings": settings},
              "reads": broker.logs, "read_attempts": 0, "read_chars": 0, "response": None, "adapter_exit_code": None}
    process, reader = None, None
    try:
        start = make_start(corpus, sid, settings)
    except BenchmarkError as exc:
        result["status"], result["error"], start = "failed", str(exc), None
    if command and not dry_run and start is not None:
        try:
            if not isinstance(command, list) or not all(isinstance(arg, str) and arg for arg in command):
                raise BenchmarkError("adapter command must be a nonempty argv JSON list")
            deadline = time.monotonic() + settings["budgets"]["timeout_seconds"]
            with tempfile.TemporaryDirectory(prefix="atlas-agent-", dir=os.environ.get("TMPDIR")) as cwd:
                env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8",
                       "HOME": cwd, "TMPDIR": cwd, "PYTHONIOENCODING": "utf-8"}
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                           stderr=subprocess.DEVNULL, cwd=cwd, env=env, start_new_session=True)
                reader = LineReader(process.stdout, settings["budgets"]["max_message_bytes"], deadline)
                assert process.stdin is not None and process.stdout is not None
                os.set_blocking(process.stdin.fileno(), False)
                def send(message):
                    import selectors
                    data = memoryview(canonical(message))
                    with selectors.DefaultSelector() as writable:
                        writable.register(process.stdin, selectors.EVENT_WRITE)
                        while data:
                            remaining = deadline - time.monotonic()
                            if remaining <= 0 or not writable.select(remaining):
                                raise BenchmarkError("adapter wall timeout while writing stdin")
                            try:
                                written = os.write(process.stdin.fileno(), data)
                            except BlockingIOError:
                                continue
                            data = data[written:]
                send(start)
                ready, final = False, False
                while True:
                    line = reader.line()
                    if line is None:
                        break
                    if final:
                        raise BenchmarkError("adapter output after final")
                    message = json.loads(line.decode("utf-8"))
                    if not isinstance(message, dict):
                        raise BenchmarkError("protocol message must be object")
                    kind = message.get("type")
                    if kind == "ready" and not ready:
                        if (message.get("fresh_context") is not True or message.get("broker_only") is not True
                                or message.get("settings_sha256") != start["settings_sha256"]
                                or not isinstance(message.get("identity"), str) or not message["identity"].strip()):
                            raise BenchmarkError("missing/mismatched adapter isolation/settings attestation")
                        result["adapter"]["attestation"] = message
                        ready = True
                    elif kind == "read_file" and ready:
                        if set(message) != {"type", "request_id", "path", "offset", "length"}:
                            raise BenchmarkError("unexpected read_file fields")
                        send(broker.read(message))
                    elif kind == "final" and ready:
                        text = message.get("text")
                        if set(message) != {"type", "text"} or not isinstance(text, str) or not text.strip():
                            raise BenchmarkError("invalid/empty final response")
                        if len(text) > settings["budgets"]["max_final_chars"]:
                            raise BenchmarkError("final response character budget exceeded")
                        result["response"] = text
                        final = True
                        process.stdin.close()
                    else:
                        raise BenchmarkError("unexpected protocol message or absent ready attestation")
                exit_code = process.wait(timeout=max(0.01, deadline - time.monotonic()))
                result["adapter_exit_code"] = exit_code
                if exit_code != 0 or not final or not ready:
                    raise BenchmarkError("adapter nonzero exit, no final, or no ready")
                result["status"], result["error"] = "completed", None
        except (BenchmarkError, OSError, UnicodeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
            result["status"], result["error"] = "failed", type(exc).__name__ + ": " + str(exc)
        finally:
            if process is not None:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                result["adapter_exit_code"] = process.returncode
                if process.stdin and not process.stdin.closed:
                    try:
                        process.stdin.close()
                    except BrokenPipeError:
                        pass
                if process.stdout:
                    process.stdout.close()
            if reader is not None:
                reader.close()
    result["read_attempts"], result["read_chars"] = broker.attempts, broker.chars
    result["finished_at"] = utc_now()
    validate_schema(result, load(ROOT / "schemas/result.schema.json"))
    return result



def validate_result(result):
    validate_schema(result, load(ROOT / "schemas/result.schema.json"))
    if result["manifest_sha256"] != FREEZE_SHA256:
        raise BenchmarkError("result freeze provenance mismatch")
    if result["scenario_sha256"] != digest((ROOT / "inputs" / (result["scenario_id"] + ".json")).read_bytes()):
        raise BenchmarkError("result input provenance mismatch")
    if result["prompt_sha256"] != digest((ROOT / "prompt.txt").read_bytes()):
        raise BenchmarkError("result prompt provenance mismatch")
    if result["settings_sha256"] != digest(canonical(result["adapter"]["settings"])):
        raise BenchmarkError("result settings provenance mismatch")
    if result["read_attempts"] != len(result["reads"]) or result["read_chars"] != sum(r["returned_chars"] for r in result["reads"]):
        raise BenchmarkError("read counters disagree")
    for read in result["reads"]:
        if read["content_sha256"] != digest(read["content"].encode()) or read["returned_chars"] != len(read["content"]):
            raise BenchmarkError("read log integrity mismatch")
    if result["status"] == "completed":
        ready = result["adapter"].get("attestation", {})
        if (result["adapter_exit_code"] != 0 or not result["response"] or result["error"] is not None
                or ready.get("fresh_context") is not True or ready.get("broker_only") is not True
                or ready.get("settings_sha256") != result["settings_sha256"]):
            raise BenchmarkError("invalid completed result")
        budgets = result["adapter"]["settings"]["budgets"]
        if (result["read_attempts"] > budgets["max_read_attempts"] or result["read_chars"] > budgets["max_read_chars"]
                or sum(r["error"] is None for r in result["reads"]) > budgets["max_reads"]
                or len(result["response"]) > budgets["max_final_chars"]):
            raise BenchmarkError("completed result exceeds hard budgets")
    elif result["status"] in {"prepared", "unexecuted"} and (result["response"] is not None or result["reads"]):
        raise BenchmarkError("unexecuted/prepared result cannot contain response or reads")
    return result


def evaluator_packet(run_path):
    verify_freeze()
    result = validate_result(load(run_path))
    if result["status"] != "completed":
        raise BenchmarkError("only completed runs may be evaluated")
    return {"scenario_id": result["scenario_id"], "run_sha256": digest(pathlib.Path(run_path).read_bytes()),
            "manifest_sha256": result["manifest_sha256"], "corpus_sha256": result["corpus_sha256"],
            "settings_sha256": result["settings_sha256"],
            "scenario": load(ROOT / "inputs" / (result["scenario_id"] + ".json")),
            "response": result["response"], "read_logs": result["reads"],
            "read_attempts": result["read_attempts"], "read_chars": result["read_chars"],
            "no_atlas": result["corpus_label"] == "no-atlas",
            "answer_key": load(ROOT / "evaluator-only/keys" / (result["scenario_id"] + ".json")),
            "rubric": load(ROOT / "evaluator-only/rubric.json")}


def score_template(packet):
    return {"schema_version": "1.0", "scenario_id": packet["scenario_id"],
            **{key: packet[key] for key in ("run_sha256", "manifest_sha256", "corpus_sha256", "settings_sha256")},
            "evaluated_at": "FILL_ISO8601", "evaluator": {"identity": "FILL_INDEPENDENT_EVALUATOR", "role": "human",
            "independent": False, "blinded": False, "conflicts": "FILL_AUTHOR_AGENT_EVALUATOR_SEPARATION"},
            "dimensions": {d: {"raw_score": None, "effective_score": None, "rationale": "",
                               "evidence_quotes": [], "omitted_findings": []} for d in DIMENSIONS},
            "critical_failures": []}


def apply_score(run_path, request):
    import datetime
    packet = evaluator_packet(run_path)
    result = load(run_path)
    score = json.loads(json.dumps(request))
    validate_schema(score, load(ROOT / "schemas/score.schema.json"))
    for key in ("scenario_id", "run_sha256", "manifest_sha256", "corpus_sha256", "settings_sha256"):
        if score[key] != packet[key]:
            raise BenchmarkError("score provenance mismatch: " + key)
    try:
        when = datetime.datetime.fromisoformat(score["evaluated_at"].replace("Z", "+00:00"))
        if when.tzinfo is None:
            raise ValueError("timezone required")
    except ValueError as exc:
        raise BenchmarkError("score timestamp must be timezone-aware ISO8601") from exc
    if score["evaluator"]["identity"] in {result["adapter"]["attestation"]["identity"],
                                           result["adapter"].get("benchmark_author")}:
        raise BenchmarkError("benchmark author/tested agent cannot evaluate itself")
    findings = {item["finding_id"] for item in packet["answer_key"]["expected_findings"]}
    failures = {item["failure_id"]: item for item in packet["answer_key"]["critical_failures"]
                + packet["rubric"]["global_critical_failures"]}
    response = packet["response"]
    seen_failures = set()
    for failure in score["critical_failures"]:
        fid = failure["failure_id"]
        if fid not in failures or fid in seen_failures:
            raise BenchmarkError("unknown/duplicate critical failure: " + fid)
        if failure["evidence_quote"] not in response:
            raise BenchmarkError("critical-failure quote not in response")
        seen_failures.add(fid)
    for dimension, entry in score["dimensions"].items():
        if not entry["rationale"].strip():
            raise BenchmarkError("score needs nonempty rationale")
        if set(entry["omitted_findings"]) - findings:
            raise BenchmarkError("unknown omitted expected finding")
        if any(not quote.strip() or quote not in response for quote in entry["evidence_quotes"]):
            raise BenchmarkError("dimension evidence quote not in response")
        if dimension == "retrieval_relevance" and packet["no_atlas"]:
            if entry["raw_score"] is not None or "not_applicable" not in entry["rationale"]:
                raise BenchmarkError("no-atlas retrieval must be null/not_applicable")
            entry["effective_score"] = None
            continue
        if type(entry["raw_score"]) is not int:
            raise BenchmarkError("all applicable dimensions require ordinal integer scores")
        if not entry["evidence_quotes"] and not entry["omitted_findings"]:
            raise BenchmarkError("score needs response evidence or specific omitted finding")
        caps = [failures[fid]["caps"][dimension] for fid in seen_failures if dimension in failures[fid]["caps"]]
        entry["effective_score"] = min([entry["raw_score"], *caps])
    validate_schema(score, load(ROOT / "schemas/score.schema.json"))
    return score



def run_batch(corpora, out, settings, command=None, dry_run=False, author_identity=None):
    from collections import Counter
    out = pathlib.Path(out)
    if out.exists():
        raise BenchmarkError("new run directory required; never overwrite attempted runs")
    manifests = [verify_corpus(c) for c in corpora]
    if len(corpora) == 2 and [m["label"] for m in manifests] != ["v1", "v1.1"]:
        raise BenchmarkError("paired corpus arguments must be v1 then v1.1")
    if any(m["layers"] != settings["layers"] for m in manifests):
        raise BenchmarkError("run layer availability differs from frozen execution settings")
    if command and (not author_identity or settings["model_settings"]["model"] == "PARENT_SELECTS_BEFORE_RUN"):
        raise BenchmarkError("real runs require pinned model settings and benchmark author identity")
    order = []
    for i, sid in enumerate(SCENARIOS):
        indexes = list(range(len(corpora)))
        if len(indexes) == 2 and i % 2:
            indexes.reverse()
        order.extend((sid, index) for index in indexes)
    registration = {"benchmark_id": "AU-v1", "registered_at": utc_now(), "manifest_sha256": FREEZE_SHA256,
                    "harness_sha256": digest(pathlib.Path(__file__).read_bytes()),
                    "model_settings": settings, "settings_sha256": digest(canonical(settings)),
                    "adapter_command": command, "benchmark_author": author_identity,
                    "repetitions": 1, "exclusions": [], "dry_run": dry_run,
                    "corpora": [{"label": m["label"], "sha256": digest((pathlib.Path(c) / "corpus-manifest.json").read_bytes())}
                                for c, m in zip(corpora, manifests)],
                    "order": [{"scenario_id": sid, "corpus_label": manifests[index]["label"]} for sid, index in order]}
    write_new(out / "registration.json", registration)
    statuses = Counter()
    for sid, index in order:
        result = run_scenario(corpora[index], sid, settings, command, dry_run)
        result["adapter"]["benchmark_author"] = author_identity
        identity = result["adapter"].get("attestation", {}).get("identity")
        if identity is not None and identity == author_identity:
            result["status"], result["error"] = "failed", "benchmark author cannot be tested agent"
        validate_result(result)
        name = sid + ("-" + manifests[index]["label"] if len(corpora) > 1 else "") + ".json"
        write_new(out / name, result)
        statuses[result["status"]] += 1
    summary = {"runs": len(order), "statuses": dict(statuses), "independent_evaluations": 0,
               "improvement_claim": None, "registration_sha256": digest((out / "registration.json").read_bytes())}
    write_new(out / "summary.json", summary)
    return summary


def report(run_dir, score_dir=None):
    rows, matches = [], {}
    if score_dir is not None:
        for path in sorted(pathlib.Path(score_dir).glob("*.json")):
            score = load(path)
            validate_schema(score, load(ROOT / "schemas/score.schema.json"))
            if score["run_sha256"] in matches:
                raise BenchmarkError("multiple scores for run; report adjudications separately")
            matches[score["run_sha256"]] = (score, path)
    runs = sorted(pathlib.Path(run_dir).glob("AU-*.json"))
    for path in runs:
        run = validate_result(load(path))
        sha = digest(path.read_bytes())
        row = {"scenario_id": run["scenario_id"], "corpus_label": run["corpus_label"], "status": run["status"],
               "error": run["error"], "run_sha256": sha, "harness_sha256": run["harness_sha256"],
               "settings_sha256": run["settings_sha256"], "read_attempts": run["read_attempts"],
               "read_chars": run["read_chars"], "dimensions": None, "critical_failures": None,
               "evaluation_status": "unscored"}
        if sha in matches:
            score, score_path = matches.pop(sha)
            checked = apply_score(path, score)
            if checked != score:
                raise BenchmarkError("score effective caps were not applied")
            row.update(dimensions=score["dimensions"], critical_failures=score["critical_failures"],
                       evaluation_status="scored", score_sha256=digest(score_path.read_bytes()))
        rows.append(row)
    if matches:
        raise BenchmarkError("score files have no matching run")
    return {"benchmark_id": "AU-v1", "manifest_sha256": FREEZE_SHA256, "dimensions": list(DIMENSIONS),
            "runs": rows, "note": "No weighted aggregate. Unscored/failed/unexecuted rows are not evidence of improvement."}


def main(argv=None):
    import argparse
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("verify-freeze")
    verify = sub.add_parser("verify-corpus")
    verify.add_argument("--corpus", required=True)
    pin = sub.add_parser("pin-settings")
    pin.add_argument("--model", required=True)
    pin.add_argument("--out", required=True)
    package = sub.add_parser("prepare")
    package.add_argument("--source")
    package.add_argument("--label", choices=["v1", "v1.1", "no-atlas"], required=True)
    package.add_argument("--out", required=True)
    package.add_argument("--layers", default="L0,L1,L2,L3")
    for name in ("dry-run", "run", "run-paired"):
        run = sub.add_parser(name)
        if name == "run-paired":
            run.add_argument("--v1", required=True)
            run.add_argument("--v11", required=True)
        else:
            run.add_argument("--corpus", required=True)
        run.add_argument("--out", required=True)
        run.add_argument("--settings")
        run.add_argument("--adapter", help="JSON argv array; no shell parsing and no credentials")
        run.add_argument("--author-identity")
    packet = sub.add_parser("packet")
    packet.add_argument("--run", required=True)
    packet.add_argument("--out", required=True)
    packet.add_argument("--template")
    score = sub.add_parser("score")
    score.add_argument("--run", required=True)
    score.add_argument("--evaluation", required=True)
    score.add_argument("--out", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--kind", choices=["scenario", "result", "score"], required=True)
    validate.add_argument("--file", required=True)
    results = sub.add_parser("report")
    results.add_argument("--runs", required=True)
    results.add_argument("--scores")
    results.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        frozen = verify_freeze()
        if args.action == "verify-freeze":
            output = {"benchmark_id": frozen["benchmark_id"], "frozen_files": len(frozen["files"]), "manifest_sha256": FREEZE_SHA256}
        elif args.action == "verify-corpus":
            corpus = verify_corpus(args.corpus)
            output = {"label": corpus["label"], "files": len(corpus["files"]), "cards": len(corpus["card_ids"]),
                      "corpus_sha256": digest((pathlib.Path(args.corpus) / "corpus-manifest.json").read_bytes())}
        elif args.action == "pin-settings":
            value = execution_settings()
            if not args.model.strip() or args.model == "PARENT_SELECTS_BEFORE_RUN":
                raise BenchmarkError("choose an actual model identity")
            value["model_settings"]["model"] = args.model
            write_new(args.out, value)
            output = {"settings_sha256": digest(canonical(value)), "path": args.out}
        elif args.action == "prepare":
            if args.label != "no-atlas" and not args.source:
                raise BenchmarkError("source required for an Atlas arm")
            corpus = prepare(args.source, args.out, args.label, tuple(args.layers.split(",")))
            output = {"label": corpus["label"], "files": len(corpus["files"]), "cards": len(corpus["card_ids"]),
                      "corpus_sha256": digest((pathlib.Path(args.out) / "corpus-manifest.json").read_bytes())}
        elif args.action in {"run", "dry-run", "run-paired"}:
            corpora = [args.v1, args.v11] if args.action == "run-paired" else [args.corpus]
            command = json.loads(args.adapter) if args.adapter else None
            if command is not None and (not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command)):
                raise BenchmarkError("adapter must be nonempty argv array")
            output = run_batch(corpora, args.out, execution_settings(args.settings), command,
                               args.action == "dry-run", args.author_identity)
        elif args.action == "packet":
            value = evaluator_packet(args.run)
            write_new(args.out, value)
            if args.template:
                write_new(args.template, score_template(value))
            output = {"run_sha256": value["run_sha256"], "packet": args.out, "template": args.template}
        elif args.action == "score":
            value = apply_score(args.run, load(args.evaluation))
            write_new(args.out, value)
            output = {"run_sha256": value["run_sha256"], "score_sha256": digest(pathlib.Path(args.out).read_bytes()),
                      "effective_dimensions": {d: e["effective_score"] for d, e in value["dimensions"].items()},
                      "critical_failures": [e["failure_id"] for e in value["critical_failures"]]}
        elif args.action == "validate":
            value = load(args.file)
            validate_schema(value, load(ROOT / "schemas" / (args.kind + ".schema.json")))
            if args.kind == "result":
                validate_result(value)
            output = {"kind": args.kind, "schema_valid": True,
                      "note": "Score schema alone does not validate provenance/quotes/caps; use score with --run."}
        else:
            value = report(args.runs, args.scores)
            write_new(args.out, value)
            output = {"runs": len(value["runs"]), "scored": sum(row["evaluation_status"] == "scored" for row in value["runs"]), "report": args.out}
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (BenchmarkError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": type(exc).__name__ + ": " + str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
