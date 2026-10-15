---
id: SOL-13-001
type: solution
title: Skew-aware bounded execution with complete pair coverage
domain: "13"
summary: >-
  Stream or tile candidate work while retaining declared eligibility, stable pair
  identity and complete comparison coverage. Profile hot blocks and expensive
  feature routes, choose resident-data batching before optional distribution,
  and reconcile retries and global resolution. Requires task coverage manifests,
  versioned indexes and resource accounting. Tiling bounds memory, not inherent
  pair count; caps, timeouts and incomplete tasks must remain distinguishable
  from valid non-matches and from equivalent physical optimization.
tags: [entity-agnostic, large-scale, batch, incremental, blocking, candidate-generation, provenance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  addresses: [DEC-13-001]
  complements: [SOL-05-003, SOL-02-002]
  evaluated_by: [EVAL-11-007, EVAL-11-001, EVAL-11-006]
---

# Skew-aware bounded execution with complete pair coverage

## Short summary

Turn an oversized pair workload into bounded tasks without confusing work
placement with candidate admission. Keep a complete manifest, reconcile duplicate
emissions and retain one consistent output version. This is Atlas engineering
synthesis, not an implemented distributed ER algorithm.

## Problem addressed

A frequent block key or costly name comparator can create a straggler, exhaust
memory or monopolize an external-model quota. Hashing the key puts all its work
on the same shard. Splitting records and comparing only within each new shard
misses cross-shard pairs. More workers cannot repair that logical omission.

## Core mechanism

1. Profile eligible block sizes, degree tails, emitted versus unique pairs and
   comparison routes on the intended workload. Include index build and input scan.
2. Give each unordered pair a canonical, source-scoped observation-key identity;
   preserve directed roles for asymmetric assignment or evidence. Record pass
   provenance separately from comparison multiplicity. Define required logical
   comparison units by pair/roles, observation revisions, required feature route
   and model/context versions. A pair can require several distinct units; optional
   or conditionally skipped routes follow the declared stage contract.
3. Tile a cross-source block into chunks $L_i,R_j$ and schedule **every required**
   $L_i	imes R_j$. For a within-source block, cover all off-diagonal chunk pairs
   once and only unordered distinct pairs in each diagonal chunk. Apply the same
   eligibility predicate as the baseline. Manifest expected tiles before execution.
4. Stream and batch features within memory limits; spill stable keyed products
   where required. Deduplicate at a valid comparison boundary while retaining
   distinct route-specific features when their semantics differ.
5. Commit task output by run/version/task identity, reject conflicting retry
   output, and reconcile required units against valid completed units, including
   authorized cache reuse. Task success or equal counts is insufficient: require
   set-level reconciliation or an independently justified enumeration/coverage
   argument. Detect missing internal routes as well as missing tiles, then resolve
   at the required global scope. A task timeout remains incomplete or explicitly
   escalated, never a successful empty comparison result.

**Illustration, not a measured result:** splitting a cross-source block into two
chunks on each side requires four cross-products. Comparing only corresponding
chunks omits two. Deterministic pair-to-task assignment or one-side partitioning
with replication can also retain coverage; account for replication and transfers.

## Theoretical explanation

Under exact tiling of the eligible Cartesian product, its union equals the
baseline candidate set. Chunking bounds resident work but leaves total pair count
unchanged; an external deduplication stage also needs its own capacity bound.
Conditional equivalence additionally requires identical evidence, model context,
policy and resolution. Floating-point reduction, tie-breaking and stateful order
can break equivalence even when pair coverage is complete.

## Important variants

Prefer resident SQL/vectorized filters and batched application comparison when
these match current semantics. PostgreSQL 17 distinguishes planner cost estimates
from observed execution, and explains that EXPLAIN ANALYZE executes the query.[42]
Use authorized read-only probes or isolated copies; profiling is not permission
to execute modifying queries.

Distribution can split hot work and replicate inputs. Spark 3.5.6 documents
adaptive skew-join splitting and replication, runtime-plan changes and shuffle
partition coalescing.[41] These are bounded execution examples, not proof that
ER candidate coverage or downstream membership remains unchanged.

A cheap-first cascade can avoid expensive comparisons only under its declared
admission/abstention semantics; test the skipped population. It is not merely
vectorization. Index maintenance and incremental closure remain
[AR-06](../../architectures/incremental-continuous.md) responsibilities.

## Assumptions and prerequisites

Need consistent accessible inputs, stable task/pair keys, explicit output
semantics, a complete coverage manifest, sufficient spill storage and retry
ownership. Optional distribution adds worker access, serialization and global
commit contracts. Pin index inputs, build configuration, deletion handling and
visibility boundary. A stale index is not a cheaper equivalent retrieval index.

## Applicability conditions

Useful when skew or resident memory, rather than average pair cost alone, limits
execution. Select distribution after measuring the local baseline. For an
execution-only contrast, freeze the realized candidate/required-comparison
workload, even if its producer was stochastic; use recorded stochastic outputs
or a justified coupling when the promised equivalence requires identical
realizations. Independent stochastic retrieval realizations change the workload
and belong to a separate expected-cost/output experiment, not a placement-only
comparison. [EVAL-11-007](../../evaluation/execution-cost-replay.md) requires named
joint output objects, project equivalence margins and uncertainty; failure to
detect a difference is not equivalence.

## Advantages

Coverage manifests expose omissions and repeated work. Batching can amortize
call overhead; tiling can prevent one block from exceeding memory. These are
mechanistic possibilities, not measured speedups or quality gains.

## Trade-offs and failure modes

A uniform record partition can lose eligible comparisons. Excessive small tiles
add scheduling and I/O; large tiles retain stragglers. Physical retries can
repeatedly bill external calls even if outputs deduplicate. Avoid claiming
exactly-once remote effects from local task keys. Whole-cluster constraints and
one-to-one competitors cross partitions. Logical caps, dropped hot keys and
failure-as-negative shortcuts change recall and possibly calibration.

Account for cold index construction, incremental insert/delete/update and
rebuild cost, retained bytes, compaction and query degradation. Approximate
indexes may change neighborhoods after updates; periodic rebuild is a comparator,
not automatically equivalent to maintenance. Privacy rules apply to replicated
features, intermediate spills and caches, not just the raw table.

## Relationships with other methods

[Artifact runs](../architecture/versioned-artifact-runs.md) own invalidation and
realized lineage; [retrieval alternatives](../candidate-generation/approximate-blocking.md)
own quality-affecting pruning. This solution exchanges a complete versioned
candidate/evidence product with scoring and resolution, not local entity truth.

## How to evaluate

Use [execution-cost evaluation](../../evaluation/execution-cost-replay.md) for
cold/warm/update runs with matched logical outputs, manifest completeness, peak
resources, task tails and total spend. Inject missing/duplicate/conflicting tasks
and successful tasks with missing internal comparison outputs under
[behavioral testing](../../evaluation/synthetic-metamorphic.md). Evaluate
changed budgets with [candidate recall](../../evaluation/candidate-recall.md),
including outside candidates, rather than only accepted-match counts. Adopt only
with required equivalence and worthwhile project costs; reject omissions or
unreconciled effects; unknown completion or output semantics is inconclusive.

## Research opportunities

Compare fixed-size tiling with cost-aware scheduling under the same candidate
set. Separate reduced duplicate work, better load balance and changed eligibility
as competing explanations for faster runs.

## References and evidence limitations

[41]–[42] support specific engine diagnostics and physical mechanisms. Pair-tiling
coverage and ER contracts above are conditional reasoning. No index was built,
ER workload run or speedup established here.

## Sources

[41] https://spark.apache.org/docs/3.5.6/sql-performance-tuning.html — Spark SQL Performance Tuning (3.5.6)
[42] https://www.postgresql.org/docs/17/using-explain.html — PostgreSQL 17: Using EXPLAIN
