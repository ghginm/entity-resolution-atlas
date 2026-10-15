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
  evaluated_by: [EVAL-11-001, EVAL-11-003, EVAL-11-006, EVAL-11-007]
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

Required responsibilities include a change feed or snapshot differencing, source-scoped versioned observations, maintenance of any retrieval indexes, dependency tracking, the selected scoring/resolution contracts, consistent publication, and reversible membership history. They may be fused physically; no fixed stage count or scorer/partitioner is imposed. Optional context includes caches, review routing, checkpoints, temporal master views and golden-record survivorship. Review authorization becomes a hard prerequisite when a correction requires it; otherwise an optional review queue cannot supply that authority. Replay capability and correction procedures are necessary for auditable maintenance, even if frequent full recomputation is unaffordable. Unavailable retained evidence limits the replay claim explicitly.

### Event history versus materialized current state

An event-sourced design records state-changing events as the basis for reconstructing state; materialized current state can coexist with that log. Fowler's essay distinguishes application state from event history and discusses rebuild, temporal queries and replay, including the use of stored current state or snapshots.[28] It is a general architecture essay in draft form, not ER performance evidence.[28]

**Atlas synthesis:** a credible simple baseline is versioned current observations/memberships with a change journal and periodic snapshot recomputation. An alternative makes an accepted event history authoritative and derives current indexes, memberships and views. A journal is not automatically event sourcing: it must capture every state-changing input and the processing dependencies needed for its claimed reconstruction. Either choice can support incremental repair; neither proves identity accuracy or complete replayability.

Declare what is authoritative and what can be rebuilt. A replay uses specified observation revisions, rules/models, reference data, constraints and any external-query responses; using today's versions instead reconstructs a different conclusion. Distinguish **historical replay** of what was published from **corrected replay** under revised evidence or logic. Checkpoints must name the history boundary and artifact versions; they do not excuse gaps in subsequent changes. Retention/deletion permissions constrain both log and views, so an immutable-log aspiration cannot override authorized erasure.

## Conceptual input/output contracts

Extend the [module contracts](../taxonomy/module-contracts.md) with event and state semantics.

- **Event input:** source-scoped observation key, delivery/event key, insert/update/delete operation, source revision, valid/observation time where known, ingestion time, and payload or tombstone. **Output:** accepted versioned change, duplicate acknowledgment or quarantined conflict. Duplicate delivery has no second state effect; a duplicate key with a different payload is a conflict, not idempotent success. Late events follow an explicit revision/ordering policy, not unconditional last-arrival-wins.
- **Invalidation input:** accepted change plus artifact dependencies and component versions. **Output:** stale representations, index entries, candidate pairs, comparisons, scores/fusion, policy decisions, memberships and selected fields requiring repair. Deletion retracts source evidence, not necessarily the underlying real entity. Schema/normalizer/model/rule/reference changes enter the same invalidation mechanism at their relevant boundary.
- **Closure input:** invalidated artifacts and dependencies. **Output:** affected records, old/new candidates, competing assignments, clusters or relational neighborhoods, with a boundary justification and incomplete-scope flags. A fixed neighborhood radius is a resource limit, not a correctness guarantee.
- **Recompute input:** a consistent observation/configuration snapshot and affected closure. **Output:** refreshed artifacts and proposed policy, membership or field changes, preserving unresolved cases. Unknown evidence, failed retrieval or infeasible constraints cannot be published as confident negatives. Retain which valid artifacts were reused and why.
- **Publication input:** validated proposals, prior published state and required authorization. **Output:** a consistent committed entity version, membership/attribute deltas, stable IDs, merge/split lineage, and correction/rollback references. Check the proposal's base version before applying it; concurrent correction can make it stale. Avoid half-applied merges or dangling memberships, and distinguish local publication from downstream adoption.

An address correction can alter competitors for an unchanged record; deleting a bridging observation can require splitting a cluster. Both cases extend beyond matching the newly arriving record.

### Affected closure versus full replay

The dependency chain is `observation revision → representations → indexes/candidates → evidence/scores/fusion → policy → resolution/assignment → entity views/publication`. Follow reverse dependencies and any feedback from predicted memberships or entity context; an iterative snapshot is a dependency, not independent evidence. A policy-only change may reuse valid scores, a resolver-only change may reuse pair evidence, and a survivorship-only change normally revises fields without reopening identity. Explicit upstream feedback is the exception, not an excuse to collapse these responsibilities.

Saved candidate edges are not the complete dependency graph. Updated frequency statistics or source priors can change scores for unchanged pairs. An index insertion can displace a top-k candidate, and deletion can reveal a previously truncated neighbor. Repair old and new retrieval neighborhoods, pass unions, assignment competitors and whole affected components when needed. Approximate retrieval, block caps and early exits expose uncertainty about what was never stored; a bounded local repair must report that uncertainty.

Choose wider recomputation when dependency scope cannot be justified, a global model/reference/index revision invalidates many artifacts, or accumulated divergence warrants reconciliation. Full event replay and full recomputation of a selected snapshot are different comparators: snapshot computation need not reproduce a path-dependent historical policy. Fix input/configuration and declared equivalence before comparing them. Recomputing everything is not ground truth, and selective repair is not intrinsically cheaper after index, lineage and closure costs.

### Temporal revisions, deletions and continuity

Use [time-scoped identity evidence](../solutions/identity-semantics/temporal-identity.md) to separate validity from source observation, ingestion and decision/publication times. A late historical address does not become current merely by arriving last. Unknown intervals remain unknown; do not invent precise validity from processing order. A retroactive correction can revise past-valid evidence while retaining what was previously known, subject to authorized retention.

Define source-revision precedence for out-of-order updates, explicit tombstone semantics, and treatment of incomparable revisions. A stale update must not silently resurrect a newer deletion; reinstatement is a separately accepted revision under the source contract. A source purge, a record withdrawal, an expired attribute and evidence of real-world entity cessation are distinct assertions. Deleting a source record can orphan or split memberships and invalidate field choices, but is not proof of entity death. Correction traces identify whether the change concerns an observation, pair policy, membership or field truth.

Identity continuity is a domain decision, not a lifecycle optimization. A changed name/address may preserve identity; recurring identifiers, organizational succession or reused accounts may not. [Master representation and identifier lifecycle](../decisions/master-representation.md) owns these identifier choices; [survivorship](../solutions/master-records/provenance-survivorship.md) selects fields under the resulting membership. Attribute continuity cannot establish identity continuity.

### Stable IDs, reversible history and consumer consistency

Allocate entity IDs at the declared assertion/publication boundary, independently of source record keys, display fields or enumeration order; never recycle a retired ID. On merge, retain the designated ID and explicitly redirect the retired ID, with effective versions and both histories, following the master-representation contract. On split, record all children and the authorized retain-one-versus-all-new choice. A one-to-many split is not a silent single-target redirect: expose ambiguity or a scoped historical resolver. Previously published references may require an as-of ID/version rather than today's successor.

Reversible history records prior memberships, supporting decisions, chosen fields, ID transitions and supersession/correction links, or retains enough authorized inputs for reconstruction. Removing the last explicit bridge is not by itself a repair of transitive membership, master fields or external joins. Reversal is a new traced correction/publication, not an erasure of what consumers previously saw. Review stale correction proposals against the actual state version before changing it.

Publish membership, redirect and derived-view changes under a declared consistency boundary. Downstream contracts specify version visibility, pending/acknowledged deltas and correction responsibility; a local atomic commit does not promise instantaneous agreement across consumers. Scope who may correct observations, approve merges/splits, publish IDs and propagate changes under privacy/access restrictions. The Atlas grants none of those permissions.

Fowler highlights replay hazards for external updates and the need to recover historical external-query results rather than use current ones.[28] **Atlas synthesis:** reconstruction should suppress ordinary external effects, then separately authorize reconciliation/compensating actions against what was actually delivered. Rolling back internal state cannot undo a notification, billing action or other already external effect. Do not replay external writes blindly or claim reversible membership makes every downstream consequence reversible.

## Assumptions and compatible alternatives

Use where changes are frequent, freshness matters, and affected state is often smaller than the full snapshot. Stable observation keys, detectable deletions, reproducible versions, and manageable dependencies are prerequisites. Unknown change history or broad schema/model revisions may require wider recomputation.

A [linear pipeline](linear-modular.md) can provide the inner modules. [Multi-pass blocking](../solutions/candidate-generation/multi-pass-blocking.md) complements lifecycle maintenance when all pass indexes and union provenance are refreshed. [Thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md) complement provisional decisions and reopening policies. Scorers may be [additive](../solutions/matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), or [logistic](../solutions/matching-scoring/logistic-regression.md); resolvers retain task-specific cardinalities.

No labels are needed to define event handling, but temporally representative adjudication is needed to assess quality and drift. Historical labels can become stale after corrected observations. Supervised updates require temporal/entity-disjoint validation and distinct observation-time versus decision-time semantics.

## Mechanism, costs, and failures

Selective repair may save work when dependency closure remains small and cached artifacts are valid. It can approach full recomputation when common keys, assignment competitors, or relational feedback connect many records. Index maintenance, lineage storage, concurrency control, and repair complexity add overhead.

Stale indexes miss candidates; incomplete closure leaves outdated decisions. Arrival order, duplicate delivery, concurrent updates or mixed model versions can create divergent states. Check ID redirections, orphaned values and stale consumer views alongside membership. Permanent early merges accumulate errors unless correction is possible; even replayable history cannot recover evidence that was never recorded or is no longer available.

## Interactions, evaluation, and research

Cascades need event-triggered reopening; ensembles need branch and fusion invalidation. [Consistency-aware resolution](collective-consistency.md) may require competitor or relationship closure beyond local pairs. These interactions change repair scope, not the scoring paradigm.

Evaluate [candidate recall](../evaluation/candidate-recall.md) and [entity quality](../evaluation/entity-resolution-quality.md) over adjudicated temporal snapshots. Replay insertions, corrections, deletions, late/duplicate events, and model migrations. Report freshness, update/tail latency, repair size, overmerges, splits, ID stability, and correction cost. Periodic full recomputation is a comparator, not truth; inspect divergences against labels and explicit objectives. Variations include micro-batches and query-time resolution. Research can test bounded versus adaptive closure and correction policies under matched budgets. No generic incremental superiority is asserted.

[EVAL-11-006 behavioral contract evaluation](../evaluation/synthetic-metamorphic.md) adds controlled checks for duplicate delivery, stale-update/tombstone precedence, unknown-time handling, split lineage, unmatched options and replay without repeated external effects. Test order invariance only when the source ordering and resolver contract promise it; compare membership/field equivalence separately from exact ID bytes when allocation legitimately differs. Report eligible/evaluated, execution-error and unknown-oracle counts. Synthetic success does not establish temporal real-world accuracy.

Compare the versioned-current-state baseline with event-sourced or selective-repair alternatives on matched inputs/configurations and adjudicated snapshots. Adoption needs acceptable identity/field harm and consumer consistency with practical repair/freshness costs. Contract violations or harmful unexplained divergence reject the proposed boundary; insufficient labels, unavailable replay inputs or unbounded dependencies leave claims inconclusive rather than prove equivalence.

The [versioned-artifact run solution](../solutions/architecture/versioned-artifact-runs.md), [run-manifest template](../guides/run-manifest-template.md) and [decision-provenance guide](../guides/decision-provenance.md) specify reproducible artifact/decision traces. The [operational repair guide](../guides/incremental-operations.md) adds concurrency/version checks, index-epoch visibility, temporal/delete witnesses and consumer recovery boundaries; [execution-cost evaluation](../evaluation/execution-cost-replay.md) compares complete history-qualified repair with rebuild. These are bounded conceptual contracts, not an exhaustive delivery, recovery or external-compensation protocol. All ER lifecycle recommendations remain Atlas synthesis, not guarantees from the event-sourcing essay or measured Atlas results.

## Sources

[10] https://cdn.aaai.org/AAAI/2007/AAAI07-255.pdf — Online Collective Entity Resolution
[28] https://martinfowler.com/eaaDev/EventSourcing.html — Event Sourcing
