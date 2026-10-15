# 13 — Scalability & Execution

**Design question:** How can a logically valid ER design fit resource and update constraints without concealing quality loss?

## Decisions and coverage
- Single-machine/distributed execution models; hash/source/entity partitioning; blocking/inverted/vector indexes.
- Candidate explosion and workload skew need observed block-size and candidate-degree tails; splitting/salting must retain needed cross-partition comparisons or explicitly sacrifice recall.
- Selective computation, cheap-first scoring, caching/materialization and resource optimization trade CPU/GPU/memory/network/storage against quality and recomputation risk.
- Incremental processing tracks changed/deleted records and affected dependency closure. Scale tests report throughput, latency distributions, index-build/update cost, replay differences and quality–compute frontiers.

## Solution families and useful baselines
- Reusable intermediate artifacts and versioned indexes; bounded cheap-first routes with escalation.
- Skew-aware partitioning; adaptive budgets; delta updates plus periodic reconciliation; distributed/federated execution where access constraints permit.

## Ownership and limitations
05 owns retrieval logic and 02 owns routing topology; this domain owns physical work and capacity. A budget cap is a quality-affecting change, not merely an engineering optimization.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for [expansion review](../../guides/expansion-plan.md); mature names are not automatic recommendations.

## Cross-domain dependencies
- [02 — Pipeline Architecture & Orchestration](02-architecture-orchestration.md).
- [05 — Candidate Generation & Retrieval](05-candidate-retrieval.md).
- [09 — Master Entity Construction & Maintenance](09-master-maintenance.md).
- [11 — Evaluation & Diagnostics](11-evaluation-diagnostics.md).
- [14 — Explainability, Governance & Monitoring](14-governance-monitoring.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
