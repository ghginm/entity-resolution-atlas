# 10 — Ground Truth & Labeling

**Design question:** What labeled evidence supports training, evaluation and diagnosis for the actual target population?

## Decisions and coverage
- Pairwise and entity-centric annotation; gold construction, independent expert review and adjudication with uncertainty rather than forced binary certainty.
- Random/stratified/entity sampling, hard negatives and outside-candidate search target different questions. Training, evaluation and diagnostic labels need not have the same sampling distribution.
- Weak supervision, active learning and semi-supervised methods can improve label efficiency but do not replace an independent test reference.
- Entity-disjoint, source-aware and temporal splits address different leakage/transfer risks. Record inclusion probabilities, representativeness, annotation disagreement and incomplete ground truth.

## Solution families and useful baselines
- Small independently adjudicated reference with explicit coverage; entity-centric sampling when memberships are the output.
- Diversity/disagreement/uncertainty sampling for training; design-aware evaluation sampling; weak-label audits.

## Ownership and limitations
Label acquisition and reference construction belong here; estimators and confidence intervals are 11; experiment controls are 12.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for [expansion review](../../guides/expansion-plan.md); mature names are not automatic recommendations.

## Cross-domain dependencies
- [01 — Problem Formulation & Identity Semantics](01-problem-identity.md).
- [05 — Candidate Generation & Retrieval](05-candidate-retrieval.md).
- [07 — Matching & Scoring](07-matching-scoring.md).
- [11 — Evaluation & Diagnostics](11-evaluation-diagnostics.md).
- [12 — Experimentation & Research Methods](12-experimentation.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
