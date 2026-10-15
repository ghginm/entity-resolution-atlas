# AU-v1 measured agent-utility comparison — October 13, 2026

## Execution and selection
The background chain finished at **2026-10-13 11:05:57 EDT (15:05:57 UTC)**. Two paired cohorts produced 32 attempts: 25 completed and independently scored, seven transport failures retained and unscored. The later no-Atlas arm completed and scored all eight cases. **33 completed responses are scored; eight scenarios have complete v1/v1.1/no-Atlas coverage.**

The primary comparison uses the predeclared first-completed rule (cohort 01 preferred), not the best-scoring response. It selects 16 paired responses. Both AU-04 arms and AU-05-v1 come from cohort 02; remaining selected responses come from cohort 01. AU-05 therefore crosses cohorts. All second samples and failed attempts remain visible in the JSON and original per-cohort reports.

Tested model: `google/gemini-2.5-flash` via `openrouter`, fresh conversations/processes, zero-tool adapter and brokered reads. Evaluator: fresh `openai-codex` processes with provider default (`--model -`), declared independent and blinded. The exact evaluator model/version was **not pinned or wire-attested**. Earlier Sonnet evaluation was blocked by HTTP 402; those failed attempts are history, not scores. Scores are ordinal 0–3, with frozen deterministic critical-failure caps; no weighted total, overall winner, or significance claim.

## Per-dimension comparison
Each cell in the distributions lists counts at scores **0 / 1 / 2 / 3**. No-Atlas retrieval is not applicable, not zero. Higher/equal/lower compare v1.1 with v1 scenario by scenario.

| Dimension | v1 distribution | v1.1 distribution | No-Atlas distribution | v1.1 higher / equal / lower |
|---|---|---|---|---|
| Understanding | 0 / 2 / 4 / 2 | 0 / 1 / 2 / 5 | 0 / 1 / 3 / 4 | 4 / 3 / 1 |
| Retrieval | 0 / 0 / 8 / 0 | 0 / 0 / 8 / 0 | N/A (8 cases) | 0 / 8 / 0 |
| Alternatives | 0 / 1 / 6 / 1 | 0 / 0 / 7 / 1 | 0 / 0 / 8 / 0 | 1 / 7 / 0 |
| Technical reasoning | 0 / 3 / 5 / 0 | 0 / 2 / 6 / 0 | 0 / 6 / 2 / 0 | 2 / 5 / 1 |
| Risks | 0 / 2 / 6 / 0 | 0 / 0 / 8 / 0 | 0 / 1 / 7 / 0 | 2 / 6 / 0 |
| Experiments | 1 / 0 / 7 / 0 | 0 / 0 / 8 / 0 | 1 / 0 / 7 / 0 | 1 / 7 / 0 |
| Evidence discipline | 0 / 3 / 5 / 0 | 0 / 3 / 5 / 0 | 0 / 2 / 4 / 2 | 2 / 4 / 2 |
| Efficiency | 0 / 0 / 8 / 0 | 0 / 0 / 7 / 1 | 0 / 0 / 8 / 0 | 1 / 7 / 0 |

## Per-scenario effective score vectors
Order: Understanding / Retrieval / Alternatives / Technical reasoning / Risks / Experiments / Evidence / Efficiency. `—` means not applicable. These are dimension vectors, not aggregate scores.

| Scenario | v1 | v1.1 | No-Atlas |
|---|---|---|---|
| AU-01 | 2 / 2 / 2 / 1 / 2 / 2 / 1 / 2 | 3 / 2 / 2 / 1 / 2 / 2 / 1 / 2 | 3 / — / 2 / 1 / 2 / 2 / 2 / 2 |
| AU-02 | 1 / 2 / 2 / 1 / 1 / 0 / 2 / 2 | 3 / 2 / 2 / 2 / 2 / 2 / 2 / 2 | 1 / — / 2 / 1 / 1 / 0 / 1 / 2 |
| AU-03 | 3 / 2 / 2 / 2 / 2 / 2 / 2 / 2 | 1 / 2 / 2 / 1 / 2 / 2 / 1 / 2 | 3 / — / 2 / 2 / 2 / 2 / 3 / 2 |
| AU-04 | 2 / 2 / 2 / 2 / 2 / 2 / 1 / 2 | 2 / 2 / 2 / 2 / 2 / 2 / 2 / 2 | 3 / — / 2 / 2 / 2 / 2 / 2 / 2 |
| AU-05 | 2 / 2 / 2 / 2 / 2 / 2 / 1 / 2 | 3 / 2 / 2 / 2 / 2 / 2 / 2 / 2 | 2 / — / 2 / 1 / 2 / 2 / 2 / 2 |
| AU-06 | 1 / 2 / 1 / 1 / 1 / 2 / 2 / 2 | 3 / 2 / 2 / 2 / 2 / 2 / 2 / 2 | 2 / — / 2 / 1 / 2 / 2 / 2 / 2 |
| AU-07 | 2 / 2 / 2 / 2 / 2 / 2 / 2 / 2 | 2 / 2 / 2 / 2 / 2 / 2 / 1 / 3 | 2 / — / 2 / 1 / 2 / 2 / 1 / 2 |
| AU-08 | 3 / 2 / 3 / 2 / 2 / 2 / 2 / 2 | 3 / 2 / 3 / 2 / 2 / 2 / 2 / 2 | 3 / — / 2 / 1 / 2 / 2 / 3 / 2 |

## Critical failures and concrete findings
- **AU-02, v1 cohort 01 and no-Atlas:** both endorsed reference investigations limited to newly generated candidates and then proposed certifying overall recall. The evaluator flagged `AU-02-selected_recall_as_total`; the frozen caps reduced the applicable dimension scores. Calling the sample entity-centered did not make the search independent of admission.
- **AU-02, v1.1:** outside-candidate investigation avoided that critical failure. The evaluator still found unspecified within-candidate denominators, inclusion weighting, holdouts and uncertainty: experiment quality was 2, not 3.
- **AU-06:** v1.1 separated membership, temporal provenance and master construction better than the selected v1 response. Understanding rose from 1 to 3; alternatives, technical reasoning and risks each rose from 1 to 2. Field authority, replay and controlled survivorship testing remain incomplete.
- **AU-03 regression:** despite retrieving the new assignment and identity cards, v1.1 asserted that a license change implies a new entity and confused surrogate optimality with identity truth. Understanding fell from 3 to 1, technical reasoning from 2 to 1, and evidence discipline from 2 to 1. More relevant knowledge did not prevent misuse.
- No v1.1 response was flagged for a rubric critical failure across either cohort. This does **not** mean the responses were correct or complete: consequential omissions are recorded in dimension rationales. Retrieval relevance was 2 throughout the primary paired comparison; no highest-anchor retrieval improvement was measured.
- Results are mixed: v1.1 shows some scenario-specific gains but also regressions. No consistent evidence-discipline improvement or universal advantage over the no-Atlas arm is established.

## Validation and reproducibility
`summarize_results.py` calls the existing harness report validator for every cohort. Validation checks frozen hashes, score/run provenance, exact response quotes, finding/failure IDs, schema and deterministic caps. It does not establish the semantic correctness or sincerity of evaluator judgments. Reproduce into a **new output path**:

```bash
python3 validation/agent-utility/summarize_results.py --out validation/agent-utility/results/comparison-repeat.json
```

Machine-readable [comparison](comparison-2026-10-13.json) retains selected rows, all 32 paired attempts, eight no-Atlas rows, distributions, failures and source-report hashes. Original full reports: [cohort 01](scored-report-cohort-01-v2.json), [cohort 02](scored-report-cohort-02-v2.json), [no-Atlas](scored-report-no-atlas-01.json).

## Limitations
- Exploratory ordinal model judgments; no statistical significance or overall superiority claim.
- One tested model; second-cohort repetitions and seven transport failures are all retained.
- AU-05's first-completed pair combines different cohorts; paired arms are not all contemporaneous.
- Temperature, seed and output cap were declared but not wire-attestable through the CLI.
- Evaluator used openai-codex provider default (model '-'), not a pinned/version-attested model.
- Fresh-process and independence/blinding declarations do not prove model identity or isolation.
- Quoted corpus content may reveal coverage/version despite removal of explicit arm labels.
- One evaluator per response; no human adjudication or evaluator agreement measurement.
- No-Atlas ran later, not interleaved; timing/provider changes may confound its comparison.

## Evidence-led v1.2 priorities (proposal, not authorization)
1. Blind second-evaluator/human adjudication, pinned evaluator identity and enforceable sampling settings; repeat across models with interleaved no-Atlas and complete same-cohort pairs.
2. Regression-focused identity-continuity and assignment-utility guidance: license/attribute changes do not establish entity discontinuity; monotone pair rankings are not additive assignment utilities.
3. Operational outside-candidate reference designs: inclusion probabilities, within/outside denominators, entity-disjoint splits and uncertainty; the v1.1 recommendation still omitted these.
4. Master-field authority and copied-source dependence, unknown dates, revision replay and membership-versus-survivorship ablations.
5. Investigate remaining multilingual/retrieval gaps only after these decision-correctness failures, rather than expanding advanced methods for novelty.

Do not tune the frozen keys or corpus snapshots to these results. Any subsequent content experiment needs a new named cohort while retaining AU-v1.
