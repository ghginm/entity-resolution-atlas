# Compare alternatives and design the next experiment

This guide links knowledge objects; it is not a sixth card type or an executable experiment system.

## Choose only the missing context

For scarce/absent truth, start with [acquisition choice](../decisions/ground-truth-acquisition.md) and [incomplete-reference evaluation](../evaluation/incomplete-reference-quality.md); retrieve entity-search or targeted/weak-supervision details only when those alternatives apply. For an actual comparison, use [experiment-design choice](../decisions/experiment-design.md), its [controlled protocol](../solutions/experimentation/controlled-comparison.md) and the reusable [experiment-plan template](experiment-plan-template.md). For label-free policy regressions, use [behavioral testing](er-behavioral-testing.md), without calling it an accuracy test. The [estimation deep dive](../deep-dives/incomplete-reference-estimation.md) is optional for unresolved denominator, bound or variance questions.

## A contextual decision matrix
For each candidate method, record: decision ID; problem mechanism; required data; available versus missing prerequisites; identity/label assumptions; expected failure segments; compute/state/review cost; compatible upstream/downstream components; evidence scope; and the experiment that could reject it. Do not replace this matrix with an ungrounded overall numerical ranking.

## Interpretable soft-matching path
1. Preserve interpretable [evidence states](../solutions/comparison-features/evidence-states.md). Missing, invalid and reliable disagreement are different observations. Group dependent representations before counting their contributions.
2. Compare [expert additive matching](../solutions/matching-scoring/additive-soft-matching.md) against [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md) and, when representative labels exist, [regularized logistic regression](../solutions/matching-scoring/logistic-regression.md). Keep the evidence definition and candidate population fixed for the first comparison. This is a choice of weight-estimation assumptions, not a required upgrade ladder.
3. Inspect contribution stability, shared-attribute false positives, trusted conflicts, segment errors and label-sampling bias. Likelihood-ratio or logistic interpretations require their own assumptions; do not turn arbitrary weights into probabilities by applying a sigmoid.
4. Separate [probability/calibration measurement](../evaluation/pairwise-calibration.md) from [threshold/abstention actions](../solutions/decision-resolution/thresholds-abstention.md). Changes to retrieval/routing may invalidate an old probability map; see the [deep dive](../deep-dives/selection-and-calibration.md).
5. Evaluate [final entities](../evaluation/entity-resolution-quality.md) if the output includes membership. A better pairwise ranking may still produce a damaging bridge merge.

## A minimal experiment specification
- **Question and comparator:** name a precise hypothesis or component replacement, one credible baseline, and one challenger.
- **Controls:** source snapshot, eligible universe, normalization/features, candidate pool when isolating the scorer, fitting/tuning protocol, downstream policy/resolver, compute/review accounting.
- **Data:** independently adjudicated labels, inclusion design, entity-disjoint/temporal split as appropriate. Do not leak labels or graph context across partitions.
- **Metrics:** select [candidate coverage](../evaluation/candidate-recall.md), pairwise operating/calibration, and final entity/cost metrics by the actual output. Declare the integration and averaging conventions.
- **Decision rule:** choose minimum worthwhile improvement, segment/false-merge guardrails and experiment precision/power before the final test. An interval spanning material improvement and harm is inconclusive, not proof of benefit or falsification.
- **Reproducibility:** data/reference/configuration/component versions, candidate provenance, routing versions, calibration population, confidence-interval design and negative results.
- **Next step:** replicate a positive mechanism on held-out sources/time; diagnose mechanism/estimation/redundancy after a negative result; collect targeted evidence after an inconclusive result.

## Do not miss interactions
A new retrieval pass changes both coverage and the nonmatch distribution. To isolate its value, measure marginal true-match recovery/cost, then check downstream score/policy validity. A new normalization may change both blocking keys and similarity features; use a small factorial comparison when those effects cannot be separated. An oracle component replacement is a diagnostic on known reference support, not an achievable production score or a universal upper bound.

[Frequency evidence](../research/hypotheses/frequency-aware-evidence.md) and [contextual reliability](../research/hypotheses/contextual-reliability.md) provide concrete untested comparisons. Use the scenario tests (source repository only) to see alternative compositions, not to infer measured results.
