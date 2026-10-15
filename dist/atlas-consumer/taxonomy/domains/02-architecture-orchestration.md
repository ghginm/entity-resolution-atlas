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

The [modularity decision](../../decisions/pipeline-modularity.md) compares explicit functions, fixed skeletons, replaceable strategies, configuration and dependency DAGs without changing the four architecture dimensions. Follow [replaceable-stage pipelines](../../solutions/architecture/replaceable-stage-pipelines.md) for bounded substitutions and [versioned artifact runs](../../solutions/architecture/versioned-artifact-runs.md) for full-rebuild versus reuse choices. [Module contracts](../module-contracts.md) are semantic boundaries, not compulsory separate processes. The [manifest guide](../../guides/run-manifest-template.md) records a project run, not a sixth primary object type.

This map is not complete L2 method coverage. Distributed execution remains owned by 13; operational lifecycle depth continues in the tracker (source repository only). Mature pattern names are not automatic recommendations.

## Cross-domain dependencies
- [05 — Candidate Generation & Retrieval](05-candidate-retrieval.md).
- [07 — Matching & Scoring](07-matching-scoring.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [13 — Scalability & Execution](13-scalability-execution.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
