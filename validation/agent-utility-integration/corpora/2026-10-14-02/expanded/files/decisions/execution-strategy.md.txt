---
id: DEC-13-001
type: decision
title: Execution placement, skew and bounded work
domain: "13"
summary: >-
  Choose a bounded single-process, database/vectorized, or partitioned execution
  plan for the same declared ER semantics before changing retrieval budgets.
  Distinguish physical tiling that preserves comparisons from logical truncation
  that changes the population. Requires measured workload tails, resource limits,
  dependency versions and output-equivalence contracts. Compare total index,
  shuffle, comparison, resolution and recovery costs; distributed execution is
  not automatically faster, more complete or reproducible.
tags: [entity-agnostic, large-scale, low-cost, batch, incremental, candidate-generation, blocking, provenance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [DEC-05-001, DEC-02-001]
  evaluated_by: [EVAL-11-007, EVAL-11-001, EVAL-11-003]
---

# Execution placement, skew and bounded work

## Decision question

Where should ER work run, and which intermediate products should be streamed,
materialized or partitioned, without silently changing which pairs or entities
are considered? Separate a physical implementation comparison from an authorized
quality–budget experiment.

## Problem context

A common key can dominate work even when mean block size is small. Within-source
all-pairs comparison of a block of size $b$ has $b(b-1)/2$ unordered pairs;
a cross-source block has $b_L b_R$ eligible pairs before additional eligibility
filters. Multiple passes can generate the same pair repeatedly. Cheap key lookup
does not make enumeration, deduplication, feature construction or graph resolution
cheap. Tails and intermediate expansion matter more than raw record count alone.

## Relevant assumptions

Specify within/cross-source eligibility, pair orientation, duplicate semantics,
missing-key treatment, retrieval rules, score semantics, resolution scope and
required equivalence. Require a consistent snapshot or declared evolving-state
boundary. Physical partitioning cannot assume predicted entities are correct or
independent. A database query plan is an execution mechanism, not an identity
policy. A failed partition is incomplete work, not a population with no matches.

## Available solution families

- **Bounded single-process baseline:** stream canonical pairs in chunks, batch
  comparisons, spill/deduplicate when necessary, and materialize costly boundaries.
  It minimizes coordination and exposes a useful capacity reference.
- **Database or vectorized execution:** push exact filters, joins, aggregation and
  compatible comparison primitives toward resident data. Contrast with batched
  application comparators when language-specific logic, external calls or runtime
  isolation dominate. Query planners do not know undeclared ER semantics.
- **Partitioned parallel execution:** distribute independent pair-comparison work
  and reconcile duplicates before global decisions. Split hot blocks into tiles
  covering the required Cartesian product, not disjoint same-tile comparisons only.
- **Quality-affecting limits:** caps, sampled pairs, smaller windows or top-k
  retrieval can reduce work by removing candidates. These are separate
  [retrieval choices](candidate-strategy.md), not equivalent execution plans.

The [execution solution](../solutions/scalability/skew-aware-execution.md) gives
coverage-preserving tiling and accounting. [Artifact reuse](../solutions/architecture/versioned-artifact-runs.md)
owns semantic cache validity; this decision owns placement and resource cost.

## Criteria for choosing

Measure hot-block and per-record degree tails, task bytes, comparison cost by
feature route, spill, index build/update time, graph size, and available memory.
Use current resident-data location and access restrictions. Choose distribution
only when useful work and parallel slack can outweigh serialization, replication,
shuffle, scheduling, recovery and operational complexity. Resolve cross-partition
assignments or membership at a sufficient scope; local resolution can change the
answer even if every pair was scored.

## Trade-off comparison

| Plan | Potential advantage | Main cost or failure |
|---|---|---|
| Chunked local | Simple trace and controlled state | Long hot tasks; disk spill; single-host ceiling |
| Resident-data SQL/vectorized | Less transfer and per-pair interpreter overhead | Collation/null/UDF differences; poor estimates; large intermediates |
| Partitioned parallel | Distributes independent work | Hot shards, replication, retries and global reconciliation |
| Logical budget reduction | Avoids comparisons rather than moving them | Lost candidates; changed calibration and graph outcomes |

A broadcast plan copies one side to workers; ensure its realized size fits each
worker, including overhead. A chunked nested enumeration can fit memory while
retaining quadratic time. Materialization exchanges repeated CPU/network work for
storage, I/O, retention and invalidation responsibility. No plan removes inherent
pair count while preserving all comparisons merely by adding workers.

## Good baseline candidates

Start with the existing resident execution engine or a measured bounded local
runner, fixed snapshots and explicit spill/failure reporting. First batch expensive
application calls and remove redundant physical recomputation without changing
features or candidates. Optimize a demonstrated bottleneck; do not introduce a
workflow engine or distributed store solely because the corpus is large.

## Prerequisites

Need lawful data placement, a capacity limit, stage contracts, stable pair keys,
complete task manifests and enough observability to distinguish slow from omitted
work. Distribution adds retry/commit ownership and a global reconciliation boundary.
Labels are optional for equivalence testing but necessary for quality claims;
[behavioral checks](../evaluation/synthetic-metamorphic.md) cannot establish recall.

## Open questions

Which bottleneck survives warm-cache and cold-build measurements? Does a global
resolver dominate after comparisons are parallelized? How often do updates
invalidate an expensive index? If skew disappears only after truncation, did
capacity improve or did the system stop considering difficult records?

## Related evaluations

Use [EVAL-11-007](../evaluation/execution-cost-replay.md) for equivalent-output
cost and completion, plus [candidate recall](../evaluation/candidate-recall.md)
and [entity quality](../evaluation/entity-resolution-quality.md) for changed
budgets or algorithms. Adopt when complete equivalent outputs meet project
resource/freshness margins at worthwhile total cost. Reject unexplained omissions
or divergent global decisions. Unknown workload tails or unavailable reference
quality make proposed capacity/accuracy claims inconclusive.

## Links to Solution Cards

[Skew-aware bounded execution](../solutions/scalability/skew-aware-execution.md),
[versioned artifact runs](../solutions/architecture/versioned-artifact-runs.md),
and [approximate retrieval](../solutions/candidate-generation/approximate-blocking.md)
are complementary only when their semantic and budget contracts are explicit.
