# 07 — Matching & Scoring

**Design question:** How should evidence be aggregated into a score whose interpretation is clear?

## Decisions and coverage
- Hard deterministic rules; expert-weighted soft rules; additive evidence scoring. A score ranking is not automatically a posterior probability.
- Fellegi–Sunter and likelihood ratios give a statistical interpretation to comparison-state weights; conditional independence supports an additive simplification, not every LR model.
- Supervised logistic regression, GAMs, monotonic/constrained models, gradient boosting and neural record matching offer different feature interactions, interpretability and label/compute demands.
- Rule/ML hybrids, ensembles, weak/semi-supervised methods and source-dependent models need label-bias, transfer and calibration diagnostics.

## Solution families and useful baselines
- Manually assigned contributions → estimated likelihood weights or supervised coefficients, preserving interpretable features. This is a comparison space, not a mandatory upgrade ladder.
- Additive/GAM models with selected interactions; flexible models as controlled challengers when labels and error analysis justify them.

Compare [pooling/source-conditioned reliability](../../solutions/matching-scoring/source-aware-reliability.md) and [nonlinear/neural roles](../../solutions/matching-scoring/learned-neural-comparators.md) only after the interpretable baselines. Shrinkage, ranking and constrained-model roles include explicit specialist-evidence limits, not universal improvement claims.

## Ownership and limitations
Learn weights here; 06 owns evidence definitions and 08 owns actions. Candidate selection and label sampling change the population for probability interpretation.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for expansion review (source repository only); mature names are not automatic recommendations.

## Cross-domain dependencies
- [05 — Candidate Generation & Retrieval](05-candidate-retrieval.md).
- [06 — Comparison Features & Evidence Engineering](06-comparison-evidence.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [10 — Ground Truth & Labeling](10-ground-truth.md).
- [11 — Evaluation & Diagnostics](11-evaluation-diagnostics.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
