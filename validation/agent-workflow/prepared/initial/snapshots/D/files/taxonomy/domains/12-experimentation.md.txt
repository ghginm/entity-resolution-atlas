# 12 — Experimentation & Research Methods

**Design question:** Which controlled test would distinguish mechanisms and reduce decision uncertainty?

## Decisions and coverage
- Baseline design; component replacement; feature/module ablations; factorial and interaction experiments.
- Hyperparameter optimization must not repeatedly exploit the final test set. Compare common candidate pools for scorer questions and the full pipeline for retrieval-policy questions.
- Explicit hypotheses, mechanisms, assumptions, falsification criteria and reproducibility through versions/snapshots/configurations/seeds.
- Research prioritization uses observed error opportunity, impact, uncertainty, experiment effort and information gain in a declared application context. Preserve negative results and distinguish insufficient power from falsification.

## Solution families and useful baselines
- Simple credible baseline plus one controlled challenger; grouped ablations for dependent features.
- Failure-driven research; interaction studies; budget-aware search; preregistered end-to-end confirmation.

## Ownership and limitations
10 constructs labels; 11 defines measurements; this domain owns comparison procedures and inference about hypotheses, not unbounded experiment automation.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for expansion review (source repository only); mature names are not automatic recommendations.

## Cross-domain dependencies
- [07 — Matching & Scoring](07-matching-scoring.md).
- [10 — Ground Truth & Labeling](10-ground-truth.md).
- [11 — Evaluation & Diagnostics](11-evaluation-diagnostics.md).
- [13 — Scalability & Execution](13-scalability-execution.md).

## Selective retrieval
Start from [experiment-design choice](../../decisions/experiment-design.md), then the [controlled-comparison protocol](../../solutions/experimentation/controlled-comparison.md) when implementing a test. The supporting [experiment-plan template](../../guides/experiment-plan-template.md) maps controls, reference design, uncertainty and adoption rules without adding a knowledge-object type. Use [behavioral examples](../../guides/er-behavioral-testing.md) only when contract testing is relevant; advanced sequential designs remain unexpanded.
