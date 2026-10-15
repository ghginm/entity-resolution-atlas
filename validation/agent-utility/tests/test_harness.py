import importlib.util
import json
import pathlib
import sys
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
BASELINE_FILES = ROOT / "corpora/v1/files"

class FreezeTests(unittest.TestCase):
    def test_frozen_manifest_verified_before_use(self):
        self.assertIsNotNone(importlib.util.find_spec("harness"), "freeze verifier must exist")
        import harness
        manifest = harness.verify_freeze()
        self.assertEqual(len(manifest["files"]), 24)
        self.assertEqual(manifest["benchmark_id"], "AU-v1")

class SchemaTests(unittest.TestCase):
    def test_all_scenarios_validate(self):
        import harness
        self.assertTrue(hasattr(harness, "validate_schema"), "schema validator missing")
        for sid in harness.SCENARIOS:
            harness.validate_schema(harness.load(ROOT / "inputs" / (sid + ".json")),
                                    harness.load(ROOT / "schemas/scenario.schema.json"))

    def test_schema_rejects_bool_as_integer_and_extra_fields(self):
        import harness
        self.assertTrue(hasattr(harness, "validate_schema"), "schema validator missing")
        for value in [True, -1, 4, 1.5]:
            with self.assertRaises(harness.BenchmarkError):
                harness.validate_schema(value, {"type": "integer", "minimum": 0, "maximum": 3})
        with self.assertRaises(harness.BenchmarkError):
            harness.validate_schema({"x": 1}, {"type": "object", "additionalProperties": False, "properties": {}})

class CorpusTests(unittest.TestCase):
    def test_allowlist_uses_only_supported_layers(self):
        import harness
        self.assertTrue(hasattr(harness, "layer_for"), "corpus allowlist missing")
        good = {"decisions/a.md": "L2", "research/hypotheses/a.md": "L2",
                "taxonomy/domains/01-a.md": "L1", "deep-dives/a.md": "L3"}
        for path, layer in good.items():
            self.assertEqual(harness.layer_for(path), layer)
        for path in ["guides/scenario-stress-tests.md", "validation/a.md", "tests/a.md", "tools/a.md",
                     "dev_docs/a.md", "CATALOG.md", "research/answers/a.md", "research/opportunities-index.md",
                     "decisions/coverage-matrix.md", "solutions/implementation-plan.md", "references/source-ledger.json"]:
            self.assertIsNone(harness.layer_for(path), path)

    def test_prepare_verify_and_tamper(self):
        import tempfile
        import harness
        self.assertTrue(hasattr(harness, "prepare"), "packaging missing")
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp) / "corpus"
            baseline = BASELINE_FILES
            manifest = harness.prepare(baseline, out, "v1.1")
            self.assertEqual(len(manifest["card_ids"]), 21)
            self.assertTrue(all(not path.startswith("guides/") for path in manifest["files"]))
            harness.verify_corpus(out)
            first = next(iter(manifest["files"]))
            (out / "files" / first).write_text("tampered")
            with self.assertRaises(harness.BenchmarkError):
                harness.verify_corpus(out)

class BrokerTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        import harness
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = pathlib.Path(self.tmp.name) / "corpus"
        harness.prepare(BASELINE_FILES, self.out, "v1.1")

    def test_agent_start_excludes_keys_and_version(self):
        import harness
        self.assertTrue(hasattr(harness, "make_start"), "start context missing")
        start = harness.make_start(self.out, "AU-01", harness.load(ROOT / "settings.json"))
        serialized = json.dumps(start)
        for forbidden in ["expected_findings", "critical_failures", "evaluator-only", "atlas-v1-baseline", "corpus_label"]:
            self.assertNotIn(forbidden, serialized)
        self.assertNotIn("rubric", start)
        self.assertNotIn("/home/", serialized)

    def test_broker_denies_keys_traversal_and_repeated_reads_count(self):
        import harness
        self.assertTrue(hasattr(harness, "ReadBroker"), "read broker missing")
        broker = harness.ReadBroker(self.out, harness.load(ROOT / "settings.json")["budgets"])
        for i, name in enumerate(["../evaluator-only/rubric.json", "/etc/passwd", "evaluator-only/keys/AU-01.json", "index\\L0.json", "."]):
            response = broker.read({"request_id": str(i), "path": name, "offset": 0, "length": 5})
            self.assertIsNotNone(response["error"])
        for i in range(2):
            result = broker.read({"request_id": "ok" + str(i), "path": "index/L0.json", "offset": 0, "length": 20})
            self.assertEqual(len(result["content"]), 20)
        self.assertEqual(broker.chars, 40)
        self.assertEqual(broker.attempts, 7)
        self.assertEqual(len(broker.logs), 7)

    def test_read_budget_fails_closed(self):
        import harness
        self.assertTrue(hasattr(harness, "ReadBroker"), "read broker missing")
        budgets = dict(harness.load(ROOT / "settings.json")["budgets"], max_reads=1)
        broker = harness.ReadBroker(self.out, budgets)
        broker.read({"request_id": "1", "path": "index/L0.json", "offset": 0, "length": 10})
        with self.assertRaises(harness.BenchmarkError):
            broker.read({"request_id": "2", "path": "index/L0.json", "offset": 0, "length": 10})
        self.assertEqual(broker.chars, 10)
        self.assertEqual(len(broker.logs), 2)

    def test_real_process_fixture_is_fresh_and_failures_recorded(self):
        import harness
        self.assertTrue(hasattr(harness, "run_scenario"), "process execution missing")
        fixture = ROOT / "tests/fixture_adapter.py"
        settings = harness.load(ROOT / "settings.json")
        settings["budgets"]["timeout_seconds"] = 0.5  # fixture-only deadline
        first = harness.run_scenario(self.out, "AU-01", settings, [sys.executable, str(fixture), "ok"])
        second = harness.run_scenario(self.out, "AU-02", settings, [sys.executable, str(fixture), "ok"])
        self.assertEqual(first["status"], "completed")
        self.assertEqual(second["status"], "completed")
        self.assertNotEqual(first["response"], second["response"])
        self.assertEqual(len(first["reads"]), 1)
        for mode in ["crash", "no-ready", "bad-json", "extra-output", "oversize"]:
            result = harness.run_scenario(self.out, "AU-01", settings, [sys.executable, str(fixture), mode])
            self.assertEqual(result["status"], "failed", mode)
            self.assertIsNotNone(result["error"])
        dry = harness.run_scenario(self.out, "AU-01", settings, None, dry_run=True)
        self.assertEqual(dry["status"], "prepared")
        missing = harness.run_scenario(self.out, "AU-01", settings, None)
        self.assertEqual(missing["status"], "unexecuted")
        self.assertIsNone(missing["response"])

class ScoringTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        import harness
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = pathlib.Path(self.tmp.name)
        corpus = self.directory / "corpus"
        harness.prepare(BASELINE_FILES, corpus, "v1.1")
        self.artifact = harness.run_scenario(corpus, "AU-01", harness.load(ROOT / "settings.json"),
                                       [sys.executable, str(ROOT / "tests/fixture_adapter.py"), "ok"])
        self.artifact_path = self.directory / "run.json"
        harness.write_new(self.artifact_path, self.artifact)

    def request(self):
        import harness
        packet = harness.evaluator_packet(self.artifact_path)
        score = {key: packet[key] for key in ["run_sha256", "manifest_sha256", "corpus_sha256", "settings_sha256"]}
        score.update(schema_version="1.0", scenario_id="AU-01", evaluated_at=harness.utc_now(),
                     evaluator={"identity": "INDEPENDENT_TEST_FIXTURE_EVALUATOR", "role": "human",
                                "independent": True, "blinded": True, "conflicts": "fixture test only"},
                     critical_failures=[], dimensions={d: {"raw_score": 3, "effective_score": 3,
                     "rationale": "Harness validation fixture, not a substantive evaluation.",
                     "evidence_quotes": [self.artifact["response"]], "omitted_findings": []} for d in harness.DIMENSIONS})
        return score

    def test_packet_blinds_arm_and_refuses_nonresults(self):
        import harness
        self.assertTrue(hasattr(harness, "evaluator_packet"), "separate evaluator packet missing")
        packet = harness.evaluator_packet(self.artifact_path)
        for hidden in ["corpus_label", "adapter", "started_at", "finished_at", "harness_sha256"]:
            self.assertNotIn(hidden, packet)
        self.assertIn("expected_findings", packet["answer_key"])
        self.artifact["status"] = "unexecuted"
        path = self.directory / "unexecuted.json"
        harness.write_new(path, self.artifact)
        with self.assertRaises(harness.BenchmarkError):
            harness.evaluator_packet(path)

    def test_caps_preserve_other_dimensions_no_aggregate(self):
        import harness
        self.assertTrue(hasattr(harness, "apply_score"), "cap scoring missing")
        score = self.request()
        score["critical_failures"] = [{"failure_id": "AU-01-unsafe_transitive_merge",
                                       "evidence_quote": self.artifact["response"], "rationale": "Fixture cap test only."}]
        actual = harness.apply_score(self.artifact_path, score)
        self.assertEqual(actual["dimensions"]["risk_identification"]["effective_score"], 1)
        self.assertEqual(actual["dimensions"]["evidence_discipline"]["effective_score"], 3)
        self.assertEqual(actual["dimensions"]["risk_identification"]["raw_score"], 3)
        self.assertEqual(len(actual["dimensions"]), 8)
        self.assertNotIn("aggregate", actual)

    def test_cli_score_and_report_provenance(self):
        import harness
        import subprocess
        score = self.request()
        request_path = self.directory / "request.json"
        scored_dir = self.directory / "scores"
        scored_path = scored_dir / "score.json"
        harness.write_new(request_path, score)
        result = subprocess.run([sys.executable, str(ROOT / "harness.py"), "score", "--run", str(self.artifact_path),
                                 "--evaluation", str(request_path), "--out", str(scored_path)],
                                check=True, capture_output=True, text=True)
        self.assertEqual(len(json.loads(result.stdout)["effective_dimensions"]), 8)
        with self.assertRaises(harness.BenchmarkError):
            harness.report(self.directory, scored_dir)  # refuses orphan scores
        target = self.directory / "AU-01.json"
        target.write_bytes(self.artifact_path.read_bytes())
        report = harness.report(self.directory, scored_dir)
        self.assertEqual(report["runs"][0]["evaluation_status"], "scored")
        self.assertEqual(report["runs"][0]["score_sha256"], harness.digest(scored_path.read_bytes()))

    def test_global_cap_and_no_atlas_null_retrieval(self):
        import harness
        score = self.request()
        score["critical_failures"] = [{"failure_id": "GLOBAL-fabrication", "evidence_quote": self.artifact["response"],
                                       "rationale": "Fixture global-cap test, not semantic evaluation."}]
        capped = harness.apply_score(self.artifact_path, score)
        self.assertEqual(capped["dimensions"]["evidence_discipline"]["effective_score"], 0)
        corpus = self.directory / "noatlas"
        harness.prepare(None, corpus, "no-atlas")
        self.artifact = harness.run_scenario(corpus, "AU-01", harness.load(ROOT / "settings.json"),
                                           [sys.executable, str(ROOT / "tests/fixture_adapter.py"), "noatlas"])
        self.artifact_path = self.directory / "noatlas-run.json"
        harness.write_new(self.artifact_path, self.artifact)
        score = self.request()
        score["dimensions"]["retrieval_relevance"].update(raw_score=None, effective_score=None,
                                                         rationale="not_applicable: no-Atlas fixture")
        checked = harness.apply_score(self.artifact_path, score)
        self.assertIsNone(checked["dimensions"]["retrieval_relevance"]["effective_score"])

    def test_invalid_scoring_rejected(self):
        import harness
        self.assertTrue(hasattr(harness, "apply_score"), "cap scoring missing")
        import copy
        base = self.request()
        mutations = [lambda s: s.update(run_sha256="0" * 64),
                     lambda s: s["evaluator"].update(independent=False),
                     lambda s: s["evaluator"].update(identity="HARNESS_TEST_FIXTURE_NOT_A_MODEL"),
                     lambda s: s["dimensions"]["problem_understanding"].update(raw_score=True),
                     lambda s: s["dimensions"]["problem_understanding"].update(evidence_quotes=["fabricated quotation"]),
                     lambda s: s["dimensions"]["problem_understanding"].update(omitted_findings=["AU-01-F999"]),
                     lambda s: s.update(critical_failures=[{"failure_id": "MADE_UP", "evidence_quote": self.artifact["response"], "rationale": "wrong"}])]
        for mutate in mutations:
            score = copy.deepcopy(base)
            mutate(score)
            with self.assertRaises(harness.BenchmarkError):
                harness.apply_score(self.artifact_path, score)

class CliTests(unittest.TestCase):
    def test_paired_order_equivalent_settings_and_failed_runs_retained(self):
        import harness
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            directory = pathlib.Path(tmp)
            v11 = directory / "v11"
            harness.prepare(BASELINE_FILES, v11, "v1.1")
            settings = harness.load(ROOT / "settings.json")
            summary = harness.run_batch([ROOT / "corpora/v1", v11], directory / "paired", settings)
            self.assertEqual(summary["statuses"], {"unexecuted": 16})
            registration = harness.load(directory / "paired/registration.json")
            self.assertEqual([row["corpus_label"] for row in registration["order"][:4]], ["v1", "v1.1", "v1.1", "v1"])
            rows = harness.report(directory / "paired")["runs"]
            self.assertEqual(len({row["settings_sha256"] for row in rows}), 1)
            settings["model_settings"]["model"] = "TEST_FIXTURE_MODEL_ONLY"
            failed = harness.run_batch([v11], directory / "failed", settings,
                                       [sys.executable, str(ROOT / "tests/fixture_adapter.py"), "crash"],
                                       author_identity="BENCHMARK_AUTHOR_TEST_ONLY")
            self.assertEqual(failed["statuses"], {"failed": 8})
            self.assertEqual(len(list((directory / "failed").glob("AU-*.json"))), 8)
            with self.assertRaises(harness.BenchmarkError):
                harness.run_batch([v11], directory / "failed", settings)

    def test_cli_prepare_dry_run_and_unexecuted(self):
        import subprocess
        import tempfile
        import harness
        self.assertTrue(hasattr(harness, "main"), "CLI missing")
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            command = [sys.executable, str(ROOT / "harness.py")]
            subprocess.run(command + ["prepare", "--source", str(BASELINE_FILES),
                           "--label", "v1.1", "--out", str(base / "corpus")], check=True, capture_output=True)
            for action, status in [("dry-run", "prepared"), ("run", "unexecuted")]:
                out = base / action
                completed = subprocess.run(command + [action, "--corpus", str(base / "corpus"), "--out", str(out)],
                                           check=True, capture_output=True, text=True)
                self.assertEqual(json.loads(completed.stdout)["statuses"], {status: 8})
                results = sorted(out.glob("AU-*.json"))
                self.assertEqual(len(results), 8)
                for path in results:
                    harness.validate_result(harness.load(path))

class HardeningTests(unittest.TestCase):
    def test_freeze_rejects_changed_manifest_or_input(self):
        import harness
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            frozen = harness.verify_freeze()
            for name in ["freeze-manifest.json", *frozen["files"]]:
                dest = target / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, dest)
            (target / "inputs/AU-01.json").write_text("{}")
            with self.assertRaises(harness.BenchmarkError):
                harness.verify_freeze(target)

    def test_degenerate_and_traversal_paths_are_denied(self):
        import harness
        for name in [".", "", "./solutions/a.md", "solutions//a.md", "../a.md", "/a.md", "a\\b.md"]:
            self.assertIsNone(harness.layer_for(name), name)

    def test_folded_metadata_does_not_swallow_relations(self):
        import harness
        text = "---\nid: DEC-01-001\ntitle: Test\ntype: decision\ndomain: '01'\nsummary: >-\n  First summary line.\n  Second summary line.\ntags: []\nrelations:\n  complements: [AR-01]\n---\nbody"
        metadata = harness.card_metadata(text, "decisions/test.md")
        self.assertEqual(metadata["applicability"], "First summary line. Second summary line.")

    def test_timeout_kills_real_fixture_and_missing_command_fails(self):
        import harness
        settings = harness.load(ROOT / "settings.json")
        settings["budgets"]["timeout_seconds"] = 0.2
        result = harness.run_scenario(ROOT / "corpora/v1", "AU-01", settings,
                                     [sys.executable, str(ROOT / "tests/fixture_adapter.py"), "timeout"])
        self.assertEqual(result["status"], "failed")
        self.assertIn("timeout", result["error"])
        result = harness.run_scenario(ROOT / "corpora/v1", "AU-01", settings, ["/nonexistent/adapter"])
        self.assertEqual(result["status"], "failed")

    def test_initial_context_budget_is_a_recorded_failure(self):
        import harness
        settings = harness.load(ROOT / "settings.json")
        settings["budgets"]["max_initial_chars"] = 10
        result = harness.run_scenario(ROOT / "corpora/v1", "AU-01", settings, None, dry_run=True)
        self.assertEqual(result["status"], "failed")
        self.assertIn("initial context", result["error"])
        self.assertIsNone(result["response"])

    def test_chunk_attempt_and_character_budgets(self):
        import harness
        for mode, settings, requests in [
            ("chunk", {}, [{"request_id": "1", "path": "index/L0.json", "offset": 0, "length": 8001}]),
            ("attempt", {"max_read_attempts": 1}, [{"request_id": "1", "path": "absent", "offset": 0, "length": 1},
                                                       {"request_id": "2", "path": "absent", "offset": 0, "length": 1}]),
            ("chars", {"max_read_chars": 2}, [{"request_id": "1", "path": "index/L0.json", "offset": 0, "length": 3}])]:
            budgets = dict(harness.load(ROOT / "settings.json")["budgets"], **settings)
            broker = harness.ReadBroker(ROOT / "corpora/v1", budgets)
            with self.assertRaises(harness.BenchmarkError, msg=mode):
                for request in requests:
                    broker.read(request)
            self.assertTrue(broker.logs[-1]["error"])

    def test_layer_selection_and_symlink_rejection(self):
        import harness
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            source = pathlib.Path(tmp) / "source"
            source.mkdir()
            (source / "deep-dives").mkdir()
            (source / "deep-dives/bad.md").symlink_to(ROOT / "prompt.txt")
            with self.assertRaises(harness.BenchmarkError):
                harness.prepare(source, pathlib.Path(tmp) / "bad", "v1.1")
            target = pathlib.Path(tmp) / "layers"
            result = harness.prepare(BASELINE_FILES, target, "v1.1", ("L0", "L1"))
            self.assertTrue(all(meta["layer"] in {"L0", "L1"} for meta in result["files"].values()))
            with self.assertRaises(harness.BenchmarkError):
                harness.verify_baseline(BASELINE_FILES)

    def test_timeout_also_bounds_adapter_not_reading_stdin(self):
        import harness
        import time
        settings = harness.load(ROOT / "settings.json")
        settings["model_settings"]["model"] = "test-only-" + "x" * 100000
        settings["budgets"]["max_initial_chars"] = 200000  # fixture stress only
        settings["budgets"]["timeout_seconds"] = 0.2
        started = time.monotonic()
        result = harness.run_scenario(ROOT / "corpora/v1", "AU-01", settings, ["/bin/sleep", "2"])
        self.assertEqual(result["status"], "failed")
        self.assertLess(time.monotonic() - started, 1.0)

    def test_baseline_corpus_manifest_cannot_bless_tampering(self):
        import harness
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "v1"
            shutil.copytree(ROOT / "corpora/v1", target)
            manifest_path = target / "corpus-manifest.json"
            manifest = harness.load(manifest_path)
            name = "decisions/candidate-strategy.md"
            data = b"tampered"
            (target / "files" / name).write_bytes(data)
            manifest["files"][name].update(sha256=harness.digest(data), bytes=len(data))
            manifest_path.write_bytes(harness.canonical(manifest))
            with self.assertRaises(harness.BenchmarkError):
                harness.verify_corpus(target)

    def test_pinned_settings_disallow_budget_tuning(self):
        import harness
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            settings = harness.load(ROOT / "settings.json")
            settings["model_settings"]["model"] = "operator-selected-model"
            valid = pathlib.Path(tmp) / "valid.json"
            harness.write_new(valid, settings)
            self.assertEqual(harness.execution_settings(valid), settings)
            settings["budgets"]["max_reads"] = 100
            invalid = pathlib.Path(tmp) / "invalid.json"
            harness.write_new(invalid, settings)
            with self.assertRaises(harness.BenchmarkError):
                harness.execution_settings(invalid)

if __name__ == "__main__":
    unittest.main()
