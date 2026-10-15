#!/usr/bin/env python3
"""AU-v2 data integrity verifier. Stdlib only; never a model or ER runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import NoReturn

class IntegrityError(Exception):
    pass

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def load_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise IntegrityError("duplicate_json_key")
            result[key] = value
        return result
    def invalid_constant(_):
        raise IntegrityError("nonfinite_json_number")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant)

SCHEMA_KEYWORDS = {"$schema", "$id", "type", "properties", "required", "additionalProperties", "items", "minItems", "maxItems", "uniqueItems", "enum", "const", "minimum", "maximum", "minLength", "pattern"}
TYPE_NAMES = {"object", "array", "string", "integer", "number", "boolean", "null"}

def schema_error(path, keyword) -> NoReturn:
    raise IntegrityError("schema_error: " + path + ": " + keyword)

def matches_type(value, kind):
    return {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str), "integer": type(value) is int, "number": type(value) in (int, float), "boolean": type(value) is bool, "null": value is None}[kind]

def json_equal(left, right):
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(right, sort_keys=True, separators=(",", ":"))

def check_schema(schema, path):
    import re
    if not isinstance(schema, dict) or set(schema) - SCHEMA_KEYWORDS:
        schema_error(path, "unsupported_schema_shape_or_keyword")
    kinds = schema.get("type", [])
    if isinstance(kinds, str):
        kinds = [kinds]
    if not isinstance(kinds, list) or any(k not in TYPE_NAMES for k in kinds):
        schema_error(path, "schema_type")
    if "properties" in schema:
        if not isinstance(schema["properties"], dict):
            schema_error(path, "schema_properties")
        for name, sub in schema["properties"].items():
            check_schema(sub, path + "/" + name)
    if "required" in schema:
        req = schema["required"]
        if not isinstance(req, list) or any(not isinstance(k, str) for k in req) or len(set(req)) != len(req):
            schema_error(path, "schema_required")
    if "additionalProperties" in schema:
        sub = schema["additionalProperties"]
        if isinstance(sub, dict):
            check_schema(sub, path + "/additionalProperties")
        elif type(sub) is not bool:
            schema_error(path, "schema_additionalProperties")
    if "items" in schema:
        check_schema(schema["items"], path + "/items")
    for bound in ("minItems", "maxItems", "minLength"):
        if bound in schema and (type(schema[bound]) is not int or schema[bound] < 0):
            schema_error(path, "schema_bound")
    for bound in ("minimum", "maximum"):
        if bound in schema and type(schema[bound]) not in (int, float):
            schema_error(path, "schema_numeric_bound")
    if "uniqueItems" in schema and type(schema["uniqueItems"]) is not bool:
        schema_error(path, "schema_uniqueItems")
    if "enum" in schema and (not isinstance(schema["enum"], list) or not schema["enum"]):
        schema_error(path, "schema_enum")
    if "pattern" in schema:
        if not isinstance(schema["pattern"], str):
            schema_error(path, "schema_pattern")
        try:
            re.compile(schema["pattern"])
        except re.error:
            schema_error(path, "schema_pattern")

def validate(value, schema, path):
    import re
    kinds = schema.get("type")
    if kinds is not None:
        kinds = [kinds] if isinstance(kinds, str) else kinds
        if not any(matches_type(value, k) for k in kinds):
            schema_error(path, "type")
    if "const" in schema and not json_equal(value, schema["const"]):
        schema_error(path, "const")
    if "enum" in schema and not any(json_equal(value, candidate) for candidate in schema["enum"]):
        schema_error(path, "enum")
    if isinstance(value, dict):
        if set(schema.get("required", [])) - set(value):
            schema_error(path, "required")
        props = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for name, item in value.items():
            if name in props:
                validate(item, props[name], path + "/" + name)
            elif extra is False:
                schema_error(path, "additionalProperties")
            elif isinstance(extra, dict):
                validate(item, extra, path + "/" + name)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", len(value)):
            schema_error(path, "array_length")
        if schema.get("uniqueItems"):
            normalized = [json.dumps(x, sort_keys=True, separators=(",", ":")) for x in value]
            if len(normalized) != len(set(normalized)):
                schema_error(path, "uniqueItems")
        if "items" in schema:
            for i, item in enumerate(value):
                validate(item, schema["items"], path + "/" + str(i))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            schema_error(path, "minLength")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            schema_error(path, "pattern")
    if type(value) in (int, float):
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            schema_error(path, "numeric_bound")

def validate_shapes(root, manifest):
    schema_files = sorted(p for p in manifest["files"] if p.startswith("schemas/") and p.endswith(".schema.json"))
    schemas = {Path(p).name.removesuffix(".schema.json"): load_json((root / p).read_bytes()) for p in schema_files}
    for name, schema in schemas.items():
        check_schema(schema, "schemas/" + name)
    validate(manifest, schemas["freeze"], "freeze-manifest.json")
    json_count = 0
    for p in sorted(manifest["files"]):
        if not p.endswith(".json"):
            continue
        value = load_json((root / p).read_bytes())
        json_count += 1
        if p in schema_files:
            continue
        if p.startswith("inputs/"):
            name = "scenario"
        elif p.startswith("evaluator-only/keys/"):
            name = "key"
        else:
            name = {"settings.json":"settings", "package.json":"package", "evaluator-only/rubric.json":"rubric", "evaluator-only/coverage.json":"coverage"}.get(p)
        if name is None:
            schema_error(p, "unregistered_json_artifact")
        validate(value, schemas[name], p)
    return json_count, len(schemas)

def validate_references(root, manifest, json_count):
    def read(relative):
        return load_json((root / relative).read_bytes())
    def require(condition, code):
        if not condition:
            raise IntegrityError("reference_error: " + code)
    if manifest["frozen_file_count"] != len(manifest["files"]) or manifest["json_file_count"] != json_count:
        raise IntegrityError("count_mismatch")
    ids = ["AUv2-" + str(i).zfill(2) for i in range(1, 9)]
    inputs = ["inputs/" + sid + ".json" for sid in ids]
    keys = ["evaluator-only/keys/" + sid + ".json" for sid in ids]
    metadata = read("package.json")
    require(metadata["scenarios"] == inputs and metadata["keys"] == keys, "package_inventory")
    actual_inputs = sorted(p for p in manifest["files"] if p.startswith("inputs/"))
    actual_keys = sorted(p for p in manifest["files"] if p.startswith("evaluator-only/keys/"))
    require(actual_inputs == inputs and actual_keys == keys, "case_inventory")
    rubric = read("evaluator-only/rubric.json")
    dimensions = [d["id"] for d in rubric["dimensions"]]
    require(len(dimensions) == len(set(dimensions)) == metadata["dimension_count"], "rubric_dimensions")
    require(len(inputs) == metadata["scenario_count"] and len(keys) == metadata["key_count"], "package_counts")
    all_findings, all_failures = set(), set()
    failures = 0
    for sid, input_path, key_path in zip(ids, inputs, keys):
        require(read(input_path)["scenario_id"] == sid, "input_identity")
        key = read(key_path)
        require(key["scenario_id"] == sid, "key_identity")
        for finding in key["findings"]:
            fid = finding["finding_id"]
            require(fid.startswith(sid + "-F") and fid not in all_findings, "finding_identity")
            require(set(finding["dimensions"]) <= set(dimensions), "finding_dimensions")
            all_findings.add(fid)
        for failure in key["critical_failures"]:
            fid = failure["failure_id"]
            require(fid.startswith(sid + "-CF-") and fid not in all_failures, "failure_identity")
            require(bool(failure["caps"]) and set(failure["caps"]) <= set(dimensions), "failure_caps")
            require(failure["endorsement_required"] is True, "failure_endorsement")
            all_failures.add(fid)
            failures += 1
    settings = read("settings.json")
    require(settings["scenario_order"] == ids, "scenario_order")
    arms = ["baseline-atlas", "expanded-atlas", "no-atlas"]
    require(settings["arms"] == arms, "arms")
    require(settings["arm_order_cycle"] == [arms[i:] + arms[:i] for i in range(3)], "counterbalance")
    require(metadata["planned_cells"] == len(ids) * len(arms) * settings["repetitions_per_cell"], "planned_cells")
    require(set(read("evaluator-only/coverage.json")["cases"]) == set(ids), "coverage_cases")
    budgets = settings["budgets"]
    require(budgets["successful_reads"] <= budgets["read_attempts"] and budgets["read_chunk_characters"] <= budgets["retrieved_characters"] and budgets["evaluator_wall_seconds"] > budgets["solver_wall_seconds"], "budget_consistency")
    return {"scenarios":len(inputs), "keys":len(keys), "dimensions":len(dimensions), "semantic_findings":len(all_findings), "critical_failure_rules":failures, "planned_cells":metadata["planned_cells"], "actual_runs":metadata["actual_runs"], "actual_scores":metadata["actual_scores"], "preparation_status":metadata["status"], "runtime_integration":metadata["runtime_integration"]}

def canonical(relative):
    import re
    from pathlib import PurePosixPath
    if not isinstance(relative, str) or not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_-][A-Za-z0-9_.-]*)*", relative) or any(part in (".", "..") for part in PurePosixPath(relative).parts):
        raise IntegrityError("noncanonical_path")
    return relative

def inventory(root):
    import os
    import stat
    root = root.absolute()
    if any(p.is_symlink() for p in (root, *root.parents)):
        raise IntegrityError("symlink_root")
    paths = set()
    for current, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            canonical(relative)
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise IntegrityError("symlink_entry")
            if name in files:
                if not stat.S_ISREG(mode):
                    raise IntegrityError("nonregular_entry")
                paths.add(relative)
    return paths

def verify(root, expected):
    import re
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise IntegrityError("invalid_expected_manifest_sha256")
    actual_paths = inventory(root)
    raw = (root / "freeze-manifest.json").read_bytes()
    if digest(raw) != expected:
        raise IntegrityError("manifest_anchor_mismatch")
    manifest = load_json(raw)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), dict):
        raise IntegrityError("invalid_manifest_shape")
    for relative, wanted in manifest["files"].items():
        canonical(relative)
        if relative == "freeze-manifest.json" or not isinstance(wanted, str) or not re.fullmatch(r"[0-9a-f]{64}", wanted):
            raise IntegrityError("invalid_manifest_entry")
    if actual_paths != set(manifest["files"]) | {"freeze-manifest.json"}:
        raise IntegrityError("inventory_mismatch")
    for relative, wanted in manifest["files"].items():
        if digest((root / relative).read_bytes()) != wanted:
            raise IntegrityError("file_hash_mismatch: " + relative)
    json_count, schema_count = validate_shapes(root, manifest)
    references = validate_references(root, manifest, json_count)
    return {"benchmark_id":"AU-v2", "integrity":"verified", "frozen_files":len(manifest["files"]), "json_files_excluding_manifest":json_count, "schemas":schema_count, **references}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        summary = verify(args.package_root, args.expected_manifest_sha256)
    except (IntegrityError, OSError, ValueError, KeyError, TypeError) as exc:
        print("integrity_error: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
