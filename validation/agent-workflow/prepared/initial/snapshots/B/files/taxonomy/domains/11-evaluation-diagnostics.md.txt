# 11 — Evaluation & Diagnostics

**Design question:** Which measurements reveal local quality, final identity quality and the cost of errors?

## Decisions and coverage
- Candidate recall/completeness, reduction ratio, candidate count and marginal coverage/cost.
- Pair precision/recall, PR-AUC with declared integration convention, calibration and threshold sensitivity; distinguish candidate-conditioned from eligible-population behavior.
- Entity/cluster metrics, pairwise closure, B-cubed, overmerge/undermerge, cost-sensitive and tail-risk diagnostics require suitable membership truth.
- Segment diagnostics, robustness/dataset shift, oracle component experiments, statistical uncertainty, error taxonomies and quality–cost frontiers separate different failure mechanisms.

## Solution families and useful baselines
- Common fixed candidates for scorer comparisons plus independent candidate coverage and final-resolution checks.
- Entity-centric diagnostics, cost/review operating points and design-aware intervals; oracle replacement restricted to known label support.

## Ownership and limitations
Metrics do not repair biased labels or prove causality. Unknown pairs are not negative labels; oracle gains are not population-wide upper bounds.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for [expansion review](../../guides/expansion-plan.md); mature names are not automatic recommendations.

## Cross-domain dependencies
- [05 — Candidate Generation & Retrieval](05-candidate-retrieval.md).
- [07 — Matching & Scoring](07-matching-scoring.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [10 — Ground Truth & Labeling](10-ground-truth.md).
- [12 — Experimentation & Research Methods](12-experimentation.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
