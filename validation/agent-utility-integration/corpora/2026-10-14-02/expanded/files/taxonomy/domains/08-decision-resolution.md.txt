# 08 — Decision Policies & Entity Resolution

**Design question:** When should a score trigger a link, abstention, assignment or entity-membership change?

## Decisions and coverage
- Binary decisions, single/context-dependent thresholds, match/non-match/abstain and cost-sensitive policies require declared operating populations and error costs.
- Independent pairwise outputs may suffice. Bipartite assignment needs justified cardinality and an unmatched alternative; a low score is not automatically a cannot-link constraint.
- Connected components, must-link/cannot-link constraints, constrained clustering, collective inference and global optimization enforce different notions of consistency.
- Uncertainty-aware resolution, reversible merges/splits and incremental membership changes must distinguish absence of a scored edge from evidence of nonidentity.

## Solution families and useful baselines
- Pairwise threshold/review baseline; connected components only where transitive closure is defensible.
- Assignment with unmatched options; explicit constrained partitions; relational joint inference with feedback controls.

## Ownership and limitations
Final entity resolution quality differs from pair-scoring quality. Membership belongs here; constructing the consumer master view belongs in 09.

For rule-heavy implementations, [composition choice](../../decisions/rule-composition.md) compares [ordered policies](../../solutions/decision-resolution/ordered-rule-policies.md) and [declarative tables](../../solutions/decision-resolution/declarative-decision-tables.md). Use the [refactor guide](../../guides/rule-policy-refactoring.md) for shadowing, conflict and override witnesses. This is separate from choosing membership output or proving identity correctness.

For graph contamination, [closure fragility/repair](../../solutions/decision-resolution/connected-components.md#graph-fragility-selective-verification-and-repair) separates topology from identity truth; [constraint composition](../../solutions/decision-resolution/constrained-clustering.md) compares local feasibility and global objectives. Typed related-to relations do not authorize identity closure. This is not complete specialist collective-optimization or operational graph-engine coverage; those remain bounded gaps.

## Cross-domain dependencies
- [01 — Problem Formulation & Identity Semantics](01-problem-identity.md).
- [07 — Matching & Scoring](07-matching-scoring.md).
- [09 — Master Entity Construction & Maintenance](09-master-maintenance.md).
- [11 — Evaluation & Diagnostics](11-evaluation-diagnostics.md).
- [14 — Explainability, Governance & Monitoring](14-governance-monitoring.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
