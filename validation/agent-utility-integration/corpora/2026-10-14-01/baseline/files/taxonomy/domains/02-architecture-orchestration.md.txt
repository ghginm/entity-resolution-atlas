# 02 — Pipeline Architecture & Orchestration

**Design question:** How should components interact, route work and revise decisions?

## Decisions and coverage
- Linear, cascaded/multi-stage, parallel/multi-branch and iterative/collective topologies.
- Single matcher, hybrid rules/statistics/ML and ensembles are composition choices, not unique topologies.
- Adaptive compute routing and human-in-the-loop workflows need escalation, review-capacity and correction contracts.
- Batch, incremental and streaming orchestration share logical matching components but differ in state, timing and replay requirements. Intermediate artifacts need explicit versioned contracts.

## Solution families and useful baselines
- Linear modular baseline; recall-oriented multi-pass; precision-first adaptive cascade.
- Parallel multi-model fusion; collective/consistency-aware resolution; incremental/continuous processing.

## Ownership and limitations
Describe topology here; scorer internals belong in 07, membership logic in 08, distributed execution in 13.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for [expansion review](../../guides/expansion-plan.md); mature names are not automatic recommendations.

## Cross-domain dependencies
- [05 — Candidate Generation & Retrieval](05-candidate-retrieval.md).
- [07 — Matching & Scoring](07-matching-scoring.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [13 — Scalability & Execution](13-scalability-execution.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
