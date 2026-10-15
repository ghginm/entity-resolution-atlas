#!/usr/bin/env python3
"""Operator evaluator orchestration for the frozen AU-v1 cohort.

Runs after the paired cohort finishes. For each completed run it:
  1. creates a blinded evaluator packet via harness.py `packet`;
  2. spawns one fresh, authorized Hermes CLI model process
     (--safe-mode, default toolsets; evaluator reads only its packet/template
     paths given in the prompt and writes one evaluation JSON draft);
  3. stamps `evaluated_at` mechanically with the actual finish time (a model
     cannot observe wall-clock time; this is provenance bookkeeping, never a
     scoring input) and validates the copy-back of neutral provenance keys;
  4. applies deterministic caps via harness.py `score`.

Evaluator identity is fixed to a fresh-process string distinct from the
benchmark author and from the tested model identity. Invalid or rejected
evaluations are retained as attempt files; nothing is overwritten, and no
aggregate or improvement claim is produced here. Exit nonzero only on setup
errors; per-run outcomes are summarized in the JSON report printed at the end.
"""
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = str(ROOT / "harness.py")
PACKETS_DIR = ROOT / "evaluator-only/packets"
EVALS_DIR = ROOT / "evaluator-only/evaluations"
RUNS_DIR = ROOT / "results/model-cohort-01"
SCORED_DIR = ROOT / "results/scored-cohort-01"
HERMES = "/home/ghgin/.local/bin/hermes"
EVAL_MODEL = "anthropic/claude-sonnet-4.5"
EVAL_PROVIDER = "openrouter"
EVAL_IDENTITY = "eval-claude-sonnet-45-fresh-process"
PROVENANCE_KEYS = ("scenario_id", "run_sha256", "manifest_sha256", "corpus_sha256", "settings_sha256")


def sh(argv, timeout):
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout)


def packet_paths(neutral_id):
    return (PACKETS_DIR / (neutral_id + ".json"),
            PACKETS_DIR / (neutral_id + ".pretty.json"),
            EVALS_DIR / (neutral_id + ".template.json"))


def evaluator_prompt(packet_pretty, template_path, draft_path):
    return f"""You are a blinded, independent evaluator for one Entity-Resolution design-recommendation response. You are not the benchmark author, not the agent that produced the answer, and not the author of the reference corpus. Score decision quality, not style or length.

Read these two JSON files completely before judging (pretty packet + empty evaluation template):
- {packet_pretty}
- {template_path}

Packet fields: scenario = the fictional project brief given to the tested agent; response = the agent's final recommendation; read_logs = exactly which corpus excerpts the agent actually retrieved; answer_key = semantic expected findings (ids AU-xx-Fyyy) and conditional critical failures (ids AU-xx-* and GLOBAL-*); rubric = eight ordinal dimensions 0..3 with anchors and per-dimension caps; plus neutral provenance hashes.

Rules:
1. For each of the eight dimensions in the template, fill raw_score (integer 0..3 strictly following the rubric anchors), a concrete rationale, and evidence: either EXACT verbatim substrings of `response` (copy character-for-character; short quotes are better) and/or omitted_findings listing answer_key finding ids the response genuinely missed. A dimension needs at least one real quote or one valid omitted-finding id.
2. Judge only what the response endorses. Discussing a dangerous baseline in order to reject it is NOT a critical failure. Set critical_failures only for failures actually present, each with exact evidence_quote and rationale. Apply GLOBAL-* failures only for fabrication or recommending an unauthorized irreversible action without safeguards.
3. retrieval_relevance is judged against what read_logs show the agent actually retrieved from its own corpus; honest identification of a genuine corpus gap is not penalized as the agent's error. If packet no_atlas is true, retrieval_relevance raw_score and effective_score MUST be null and its rationale MUST contain the word not_applicable; judge the other seven dimensions normally.
4. Do not invent an aggregate, mean or winner. Do not assume which corpus version was supplied.
5. evaluator object: identity "{EVAL_IDENTITY}", role "fresh_model_process", independent true, blinded true, conflicts: "none; fresh automated process distinct from benchmark author, tested agent and corpus authors".
6. Keep scenario_id and the four provenance hash fields exactly as given in the template. Leave evaluated_at as the literal string FILL_BY_OPERATOR.
7. Write the completed single JSON object (the filled template, nothing else) to this exact path:
{draft_path}
Use a file-writing tool; do not paste the JSON back to the chat."""


def stamp_and_check(draft_path, template_path):
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    template = json.loads(template_path.read_text(encoding="utf-8"))
    for key in PROVENANCE_KEYS:
        if draft.get(key) != template.get(key):
            raise ValueError(f"provenance field altered: {key}")
    if draft.get("evaluated_at") == "FILL_BY_OPERATOR":
        draft["evaluated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    draft_path.write_text(json.dumps(draft, ensure_ascii=False, sort_keys=True, indent=1), encoding="utf-8")
    return draft


def main():
    global RUNS_DIR, SCORED_DIR, EVAL_MODEL, EVAL_PROVIDER, EVAL_IDENTITY
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cohort", default="01")
    ap.add_argument("--provider", default=EVAL_PROVIDER,
                    help="authorized Hermes provider for the fresh evaluator process")
    ap.add_argument("--model", default=EVAL_MODEL,
                    help="evaluator model; pass '-' for the provider default; must differ from author and tested agent")
    ap.add_argument("--run-dir", default=None, help="override run records directory")
    ap.add_argument("--score-dir", default=None, help="override scored output directory")
    args = ap.parse_args()
    EVAL_PROVIDER = args.provider
    EVAL_MODEL = args.model
    EVAL_IDENTITY = ("eval-" + (args.model if args.model != "-" else args.provider + "-default")
                     .replace("/", "-") + "-fresh-process")
    tag = "c" + args.cohort.lstrip("0")
    RUNS_DIR = pathlib.Path(args.run_dir) if args.run_dir else ROOT / f"results/model-cohort-{args.cohort}"
    SCORED_DIR = pathlib.Path(args.score_dir) if args.score_dir else ROOT / f"results/scored-cohort-{args.cohort}"
    runs = sorted(RUNS_DIR.glob("AU-*.json"))
    if not runs:
        print(json.dumps({"error": "no run files"}), file=sys.stderr)
        return 2
    summary = []
    for index, run_path in enumerate(runs, start=1):
        run = json.loads(run_path.read_text(encoding="utf-8"))
        neutral_id = f"neutral-{tag}-{index:03d}"
        if run["status"] != "completed":
            summary.append({"run": run_path.name, "evaluation_status": "skipped-noncompleted",
                            "run_status": run["status"]})
            continue
        packet_file, pretty_file, template_file = packet_paths(neutral_id)
        prompt_file = PACKETS_DIR / (neutral_id + ".prompt.txt")
        for directory in (PACKETS_DIR, SCORED_DIR):
            directory.mkdir(parents=True, exist_ok=True)
        proc = sh([sys.executable, HARNESS, "packet", "--run", str(run_path),
                   "--out", str(packet_file), "--template", str(template_file)], 60)
        if proc.returncode != 0 and not (packet_file.exists() and template_file.exists()):
            summary.append({"run": run_path.name, "packet": neutral_id,
                            "evaluation_status": "packet-error", "error": proc.stderr[-300:]})
            continue
        if proc.returncode != 0:
            pass  # reuse packet/template created by the earlier aborted attempt (same deterministic order)
        pretty_file.write_text(json.dumps(json.loads(packet_file.read_text(encoding="utf-8")),
                                         ensure_ascii=False, sort_keys=True, indent=1), encoding="utf-8")
        attempts = []
        final_score = None
        for attempt in (1, 2):
            draft_file = EVALS_DIR / f"{neutral_id}.attempt{attempt}.draft.json"
            if draft_file.exists():
                summary.append({"run": run_path.name, "packet": neutral_id,
                                "evaluation_status": "setup-error", "error": "attempt draft already exists"})
                break
            prompt_file.write_text(evaluator_prompt(pretty_file, template_file, draft_file), encoding="utf-8")
            spawn = sh([HERMES, "chat", "--query-file", str(prompt_file), "--oneshot", "-Q",
                        "--provider", EVAL_PROVIDER]
                       + ([] if EVAL_MODEL == "-" else ["-m", EVAL_MODEL])
                       + ["--safe-mode", "--run-budget", "600", "--source", "tool"], 640)
            if spawn.returncode != 0 or not draft_file.exists():
                attempts.append({"attempt": attempt, "transport_exit": spawn.returncode,
                                 "draft_present": draft_file.exists()})
                continue
            try:
                stamp_and_check(draft_file, template_file)
            except (ValueError, OSError, json.JSONDecodeError) as exc:
                attempts.append({"attempt": attempt, "draft_invalid": str(exc)[:200]})
                continue
            out_score = SCORED_DIR / (run_path.name.replace(".json", f".eval{attempt}.json"))
            scored = sh([sys.executable, HARNESS, "score", "--run", str(run_path),
                         "--evaluation", str(draft_file), "--out", str(out_score)], 60)
            if scored.returncode != 0:
                attempts.append({"attempt": attempt, "score_rejected": scored.stderr[-300:]})
                continue
            final_score = {"attempt": attempt, "score_file": str(out_score)}
            break
        summary.append({"run": run_path.name, "packet": neutral_id,
                        "evaluation_status": "scored" if final_score else "unscored",
                        "attempts": attempts, "scored": final_score})
        print(json.dumps(summary[-1], ensure_ascii=False), flush=True)
    print(json.dumps({"evaluator_model": EVAL_MODEL, "evaluations_scored":
                      sum(1 for s in summary if s.get("evaluation_status") == "scored"),
                      "runs": summary}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
