---
id: AR-06
type: architecture
title: Incremental/Continuous Entity Resolution
domain: "02"
summary: >-
  Versioned changes to observations, models, or policies trigger recomputation of
  affected candidates, evidence, decisions, and entity views instead of routinely
  restarting every stage. The lifecycle pattern can wrap linear, multi-pass,
  cascaded, ensemble, or consistency-aware matching. It requires explicit event
  semantics, dependency tracking, stable identity handling, and reversible updates.
  Locality may lower update cost, but deletions, long-range dependencies, drift,
  and accumulated historical mistakes can force wider repair or replay; full
  recomputation is a comparator, not ground truth.
tags: [entity-agnostic, incremental, streaming, provenance, governance, monitoring, constraints, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [SOL-05-002, SOL-08-001]
  evaluated_by: [EVAL-11-001, EVAL-11-003]
---

# AR-06 — Incremental/Continuous Entity Resolution

## Philosophy and four dimensions

Maintain identity decisions as revisable conclusions over versioned observations, not append-only facts. Primary research on online collective ER studies adaptive query-time relational resolution in publication databases, not a generic guarantee for continuously maintained entities.[10] The maintenance design here is theoretically motivated Atlas synthesis.

- **Topology:** event ingestion, dependency invalidation, selective recomputation, and versioned publication; the inner matching topology remains independently chosen.
- **Scoring paradigm:** deterministic, additive, probabilistic, supervised, neural, or hybrid, with model-version tracking.
- **Resolution:** pairwise, assignment, constrained membership, or collective inference, each with different dependency closure.
- **Lifecycle:** incremental micro-batches or streaming updates, with replay/full-recompute comparison. Federated privacy/access restrictions separately constrain state ownership, propagation, and permitted exchanges.

## Pipeline and modules

`New/changed/deleted observations or configuration → invalidate state/indexes → affected dependency closure → retrieval/evidence/scoring → resolution repair → versioned entities and lineage`.

Required modules include a change feed or snapshot differencing, source-scoped versioned observations, candidate/index maintenance, dependency tracking, scoring/resolution, atomic publication, and reversible membership history. Optional modules include caches, review, checkpoints, temporal master views, and golden-record survivorship. Replay capability and correction procedures are necessary for auditable maintenance, even if frequent full recomputation is unaffordable.

## Conceptual input/output contracts

Extend the [module contracts](../taxonomy/module-contracts.md) with event and state semantics.

- **Event input:** observation key, insert/update/delete operation, source version, event time, ingestion time, and payload or tombstone. **Output:** accepted versioned change or quarantined conflict; duplicate events are idempotent and late events follow an explicit ordering policy.
- **Invalidation input:** change plus dependency/model/policy versions. **Output:** stale representations, index entries, candidate pairs, evidence, scores, and memberships requiring repair. Deletion removes evidence, not necessarily the underlying real entity.
- **Closure input:** invalidated artifacts and dependencies. **Output:** affected records, candidates, competing assignments, clusters, or relational neighborhoods, with a boundary justification. A fixed neighborhood radius is a resource limit, not a correctness guarantee.
- **Recompute input:** consistent observation snapshot and affected closure. **Output:** refreshed candidates, versioned evidence/scores, and proposed resolution changes with unresolved cases.
- **Publication input:** validated proposals and prior entity state. **Output:** committed entity version, membership deltas, stable IDs, merge/split lineage, and correction/rollback references. Avoid exposing half-applied merges or dangling memberships.

An address correction can alter competitors for an unchanged record; deleting a bridging observation can require splitting a cluster. Both cases extend beyond matching the newly arriving record.

## Assumptions and compatible alternatives

Use where changes are frequent, freshness matters, and affected state is often smaller than the full snapshot. Stable observation keys, detectable deletions, reproducible versions, and manageable dependencies are prerequisites. Unknown change history or broad schema/model revisions may require wider recomputation.

A [linear pipeline](linear-modular.md) can provide the inner modules. [Multi-pass blocking](../solutions/candidate-generation/multi-pass-blocking.md) complements lifecycle maintenance when all pass indexes and union provenance are refreshed. [Thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md) complement provisional decisions and reopening policies. Scorers may be [additive](../solutions/matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), or [logistic](../solutions/matching-scoring/logistic-regression.md); resolvers retain task-specific cardinalities.

No labels are needed to define event handling, but temporally representative adjudication is needed to assess quality and drift. Historical labels can become stale after corrected observations. Supervised updates require temporal/entity-disjoint validation and distinct observation-time versus decision-time semantics.

## Mechanism, costs, and failures

Selective repair may save work when dependency closure remains small and cached artifacts are valid. It can approach full recomputation when common keys, assignment competitors, or relational feedback connect many records. Index maintenance, lineage storage, concurrency control, and repair complexity add overhead.

Stale indexes miss candidates; incomplete closure leaves outdated decisions. Arrival order, duplicate delivery, concurrent updates, or mixed model versions can create divergent states. Stable IDs require explicit merge/split policy: retain lineage and aliases rather than treating arbitrary renumbering as identity change. A split must reopen supporting evidence and downstream consequences, not merely create another ID. Permanent early merges accumulate errors unless rollback is possible.

## Interactions, evaluation, and research

Cascades need event-triggered reopening; ensembles need branch and fusion invalidation. [Consistency-aware resolution](collective-consistency.md) may require competitor or relationship closure beyond local pairs. These interactions change repair scope, not the scoring paradigm.

Evaluate [candidate recall](../evaluation/candidate-recall.md) and [entity quality](../evaluation/entity-resolution-quality.md) over adjudicated temporal snapshots. Replay insertions, corrections, deletions, late/duplicate events, and model migrations. Report freshness, update/tail latency, repair size, overmerges, splits, ID stability, and correction cost. Periodic full recomputation is a comparator, not truth; inspect divergences against labels and explicit objectives. Variations include micro-batches and query-time resolution. Research can test bounded versus adaptive closure and correction policies under matched budgets. No generic incremental superiority is asserted.

## Sources

[10] https://cdn.aaai.org/AAAI/2007/AAAI07-255.pdf — Online Collective Entity Resolution
