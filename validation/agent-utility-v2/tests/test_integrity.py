"""Synthetic integrity/schema mutations only; no solver/model/ER execution."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        sources = [p for p in ROOT.rglob("*") if p.is_file() and not any(part.startswith(".integrity-test-") or part == "__pycache__" for part in p.relative_to(ROOT).parts) and p.relative_to(ROOT).as_posix() != "freeze-manifest.json"]
        self.temp = tempfile.TemporaryDirectory(prefix=".integrity-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.fixture = Path(self.temp.name) / "package"
        self.fixture.mkdir()
        for source in sources:
            dest = self.fixture / source.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
        self.refreeze_fixture()

    def refreeze_fixture(self):
        files = {p.relative_to(self.fixture).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(self.fixture.rglob("*")) if p.is_file() and p.name != "freeze-manifest.json"}
        manifest = {"benchmark_id":"AU-v2", "package_version":"2.0.0", "created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(), "files":files, "frozen_file_count":len(files), "json_file_count":sum(p.endswith(".json") for p in files), "manifest_self_excluded":True, "integrity_mode":"exclusive-create; external manifest SHA256 anchor"}
        raw = (json.dumps(manifest, sort_keys=True, indent=2)+"\n").encode()
        (self.fixture / "freeze-manifest.json").write_bytes(raw)
        self.anchor = hashlib.sha256(raw).hexdigest()

    def verify(self, anchor=None):
        return subprocess.run([sys.executable, "-B", str(ROOT / "verify.py"), "--package-root", str(self.fixture), "--expected-manifest-sha256", anchor or self.anchor], capture_output=True, text=True, check=False)

    def test_wrong_anchor_is_rejected(self):
        result = self.verify("0" * 64)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("manifest_anchor_mismatch", result.stderr)

    def test_anchor_argument_is_mandatory(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "verify.py")], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--expected-manifest-sha256", result.stderr)

    def test_symlinked_directory_is_rejected(self):
        outside = Path(self.temp.name) / "outside-dir"
        outside.mkdir()
        (self.fixture / "linked").symlink_to(outside, target_is_directory=True)
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("symlink", result.stderr)

    def test_absolute_manifest_path_is_rejected(self):
        path = self.fixture / "freeze-manifest.json"
        value = json.loads(path.read_text())
        value["files"][str(self.fixture / "prompt.txt")] = value["files"]["prompt.txt"]
        raw = json.dumps(value).encode()
        path.write_bytes(raw)
        self.anchor = hashlib.sha256(raw).hexdigest()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("noncanonical_path", result.stderr)

    def test_unlisted_file_is_rejected(self):
        (self.fixture / "extra.txt").write_text("synthetic extra")
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("inventory_mismatch", result.stderr)

    def test_traversal_in_manifest_is_rejected(self):
        path = self.fixture / "freeze-manifest.json"
        value = json.loads(path.read_text())
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("synthetic outside")
        value["files"]["../outside.txt"] = hashlib.sha256(outside.read_bytes()).hexdigest()
        raw = (json.dumps(value)+"\n").encode()
        path.write_bytes(raw)
        self.anchor = hashlib.sha256(raw).hexdigest()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("noncanonical_path", result.stderr)

    def test_symlinked_file_is_rejected(self):
        path = self.fixture / "prompt.txt"
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("symlink", result.stderr)

    def test_duplicate_json_keys_are_rejected(self):
        path = self.fixture / "inputs/AUv2-01.json"
        raw = path.read_text()
        path.write_text(raw.replace('"cohort": "AU-v2",', '"cohort": "AU-v2", "cohort": "AU-v2",', 1))
        self.refreeze_fixture()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("duplicate_json_key", result.stderr)

    def test_cross_case_reference_is_rejected(self):
        path = self.fixture / "evaluator-only/keys/AUv2-01.json"
        value = json.loads(path.read_text())
        value["scenario_id"] = "AUv2-02"
        path.write_text(json.dumps(value))
        self.refreeze_fixture()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("reference_error", result.stderr)

    def test_duplicate_rubric_dimension_is_rejected(self):
        path = self.fixture / "evaluator-only/rubric.json"
        value = json.loads(path.read_text())
        value["dimensions"][1]["id"] = value["dimensions"][0]["id"]
        path.write_text(json.dumps(value))
        self.refreeze_fixture()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("reference_error", result.stderr)

    def test_false_manifest_count_is_rejected(self):
        path = self.fixture / "freeze-manifest.json"
        value = json.loads(path.read_text())
        value["frozen_file_count"] += 1
        raw = json.dumps(value).encode()
        path.write_bytes(raw)
        self.anchor = hashlib.sha256(raw).hexdigest()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("count_mismatch", result.stderr)

    def test_substantive_score_null_is_invalid(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("au_v2_verify", ROOT / "verify.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        schema = json.loads((self.fixture / "schemas/score.schema.json").read_text())
        dimension = schema["properties"]["dimensions"]["properties"]["evidence_and_scope"]
        with self.assertRaises(module.IntegrityError):
            module.validate(None, dimension["properties"]["raw"], "synthetic/raw")

    def test_schema_engine_constraints(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("au_v2_verify", ROOT / "verify.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        invalid = [(True,{"type":"integer"}), (False,{"const":0}), ("a",{"type":"string","minLength":2}), ("x",{"pattern":"^a$"}), ([1,1],{"uniqueItems":True}), ([],{"minItems":1}), ([1,2],{"maxItems":1}), (4,{"maximum":3}), (-1,{"minimum":0}), ({},{"required":["x"]}), ({"x":1},{"additionalProperties":False}), ("z",{"enum":["a","b"]})]
        for value, constraint in invalid:
            with self.subTest(constraint=constraint):
                module.check_schema(constraint, "synthetic/schema")
                with self.assertRaises(module.IntegrityError):
                    module.validate(value, constraint, "synthetic/value")
        with self.assertRaises(module.IntegrityError):
            module.check_schema({"unknownKeyword":True}, "synthetic/schema")
        module.validate(None, {"type":["integer","null"]}, "synthetic/nullable")
        module.validate({"x":2}, {"type":"object","additionalProperties":{"type":"integer"}}, "synthetic/map")

    def test_nonfinite_json_is_rejected(self):
        path = self.fixture / "schemas/score.schema.json"
        path.write_text(path.read_text().replace('"maximum": 3', '"maximum": NaN', 1))
        self.refreeze_fixture()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("nonfinite_json_number", result.stderr)

    def test_pristine_package_is_accepted(self):
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["benchmark_id"], "AU-v2")

    def test_schema_invalid_but_rehashed_input_is_rejected(self):
        path = self.fixture / "inputs/AUv2-01.json"
        value = json.loads(path.read_text())
        value["background"] = 42
        path.write_text(json.dumps(value))
        self.refreeze_fixture()
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("schema_error", result.stderr)

    def test_tampered_file_is_rejected(self):
        path = self.fixture / "prompt.txt"
        path.write_bytes(path.read_bytes()+b"\n")
        result = self.verify()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("integrity_error", result.stderr)

if __name__ == "__main__":
    unittest.main()
