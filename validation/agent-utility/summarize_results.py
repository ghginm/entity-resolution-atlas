#!/usr/bin/env python3
"""Validate existing AU-v1 scores and report dimensions, never a weighted total.

Run from any directory. No model calls or edits to frozen benchmark material.
The earlier-cohort-first coverage rule selects completed runs, not high scores.
"""
import argparse
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path

import harness

ROOT = Path(__file__).resolve().parent


def summarize():
    harness.verify_freeze()
    cohorts = []
    selected = {}
    samples = []
    failed = []
    for cohort in ("01", "02"):
        run_dir = ROOT / f"results/model-cohort-{cohort}"
        report = harness.report(run_dir, ROOT / f"results/scored-cohort-{cohort}")
        cohorts.append({"cohort": cohort, "statuses": dict(Counter(r["status"] for r in report["runs"])),
                        "scored": sum(r["evaluation_status"] == "scored" for r in report["runs"])})
        for row in report["runs"]:
            item = {"cohort": cohort, **row}
            samples.append(item)
            if row["status"] != "completed":
                failed.append(item)
                continue
            if row["evaluation_status"] != "scored":
                raise harness.BenchmarkError("completed response is not independently scored")
            selected.setdefault((row["scenario_id"], row["corpus_label"]), item)
    expected = {(sid, arm) for sid in harness.SCENARIOS for arm in ("v1", "v1.1")}
    if set(selected) != expected:
        raise harness.BenchmarkError("incomplete scenario-by-arm coverage")
    no_atlas = harness.report(ROOT / "results/no-atlas-cohort-01", ROOT / "results/scored-no-atlas-01")
    if len(no_atlas["runs"]) != len(harness.SCENARIOS) or any(
            row["evaluation_status"] != "scored" for row in no_atlas["runs"]):
        raise harness.BenchmarkError("no-Atlas arm is incomplete")
    distributions = {}
    pairwise = {}
    for dimension in harness.DIMENSIONS:
        distributions[dimension] = {}
        for arm in ("v1", "v1.1", "no-atlas"):
            rows = no_atlas["runs"] if arm == "no-atlas" else [
                row for (_, label), row in selected.items() if label == arm]
            scores = [row["dimensions"][dimension]["effective_score"] for row in rows]
            distributions[dimension][arm] = {str(score): scores.count(score) for score in (0, 1, 2, 3, None)}
        comparisons = Counter()
        for sid in harness.SCENARIOS:
            before = selected[(sid, "v1")]["dimensions"][dimension]["effective_score"]
            after = selected[(sid, "v1.1")]["dimensions"][dimension]["effective_score"]
            comparisons["higher" if after > before else "lower" if after < before else "equal"] += 1
        pairwise[dimension] = {key: comparisons[key] for key in ("higher", "equal", "lower")}
    source_paths = [ROOT / f"results/{name}" for name in (
        "scored-report-cohort-01-v2.json", "scored-report-cohort-02-v2.json", "scored-report-no-atlas-01.json")]
    return {
        "benchmark_id": "AU-v1", "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "freeze_sha256": harness.FREEZE_SHA256,
        "selection_rule": "First completed response per scenario and arm, cohort 01 preferred; never select by score.",
        "cohorts": cohorts, "no_atlas_statuses": dict(Counter(row["status"] for row in no_atlas["runs"])),
        "independently_scored_responses": sum(c["scored"] for c in cohorts) + len(no_atlas["runs"]),
        "selected_paired_responses": len(selected), "failed_attempts": failed,
        "selected": [selected[key] for key in sorted(selected)], "all_paired_attempts": samples,
        "no_atlas": no_atlas["runs"], "effective_score_distributions": distributions,
        "v11_vs_v1_per_dimension": pairwise,
        "critical_failures_all_scored_attempts": [
            {"scenario_id": row["scenario_id"], "corpus_label": row["corpus_label"],
             "cohort": row.get("cohort", "no-atlas-01"), "failures": row["critical_failures"]}
            for row in samples + no_atlas["runs"] if row["critical_failures"]],
        "source_report_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in source_paths},
        "limitations": [
            "Exploratory ordinal model judgments; no statistical significance or overall superiority claim.",
            "One tested model; second-cohort repetitions and seven transport failures are all retained.",
            "AU-05's first-completed pair combines different cohorts; paired arms are not all contemporaneous.",
            "Temperature, seed and output cap were declared but not wire-attestable through the CLI.",
            "Evaluator used openai-codex provider default (model '-'), not a pinned/version-attested model.",
            "Fresh-process and independence/blinding declarations do not prove model identity or isolation.",
            "Quoted corpus content may reveal coverage/version despite removal of explicit arm labels.",
            "One evaluator per response; no human adjudication or evaluator agreement measurement.",
            "No-Atlas ran later, not interleaved; timing/provider changes may confound its comparison."
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="new JSON file; never overwrite a prior report")
    args = parser.parse_args()
    result = summarize()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"report": str(out), "scored": result["independently_scored_responses"],
                      "selected": result["selected_paired_responses"],
                      "critical_failure_responses": len(result["critical_failures_all_scored_attempts"])}))


if __name__ == "__main__":
    main()
