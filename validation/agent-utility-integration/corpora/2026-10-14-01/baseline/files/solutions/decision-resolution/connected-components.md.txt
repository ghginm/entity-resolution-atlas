---
id: SOL-08-003
type: solution
title: Connected components of accepted identity links
domain: "08"
summary: >-
  Form a partition by closing accepted identity links under graph connectivity,
  including isolated records. This transparent baseline has linear traversal
  cost on a fixed materialized graph, but does not assess the truth of implied
  pair memberships. A false bridge can contaminate entire components despite
  high accepted-edge precision. The card separates missing evidence from
  negatives, explains graph and lifecycle prerequisites, and compares closure
  with constrained membership using entity-level tail-risk and rollback tests.
tags: [entity-agnostic, clustering, pairwise, high-recall, asymmetric-costs, uncertainty, batch, incremental]
maturity: established
evidence: supported-by-external-literature
relations:
  addresses: [DEC-08-001]
  alternative_to: [SOL-08-004]
  complements: [SOL-08-001]
  evaluated_by: [EVAL-11-003, EVAL-11-004]
---

# Connected components of accepted identity links

## Short summary

Treat each connected component of an undirected accepted-link graph as one entity. Hassanzadeh and colleagues describe this partitioning/transitive-closure baseline and warn that it can group records that are not directly similar.[12] Connectivity is a membership policy, not extra evidence that every implied pair matches.

## Problem addressed

Pairwise evidence may connect different observations of an entity without comparing every member directly. Closure supplies a complete partition without specifying its cluster count. It also amplifies mistakes. The resource derivation, risk examples, operational rules, and proposed experiments below are **Atlas synthesis**, rather than empirical findings from the cited study.

## Core mechanism

For a fixed eligible record universe $V$, define $G=(V,E^+)$ with one undirected edge per accepted same-as link. Start from an unvisited vertex, traverse every reachable vertex, emit that component, and repeat. Include isolated vertices as singletons; they may still be unresolved rather than proven unique.

Membership asserts $i\sim j$ whenever a path connects them. If $a-b$ and $b-c$ are accepted, closure groups $a,b,c$ even when $a-c$ was unscored, scored weakly, or rejected. An absent candidate edge means unknown evidence, not a cannot-link. An explicit valid cannot-link inside a component is a policy conflict that unconstrained closure cannot repair.

**Resource derivation:** on an already materialized adjacency-list graph, breadth/depth-first traversal visits each vertex and each adjacency entry once, taking $O(|V|+|E^+|)$ time. Graph storage takes $O(|V|+|E^+|)$ space, with $O(|V|)$ worst-case traversal state. These bounds exclude candidate generation, comparison, scoring, and storing evidence. They do not promise linear cost for the whole ER pipeline or for dense all-pairs graphs.

## Theoretical explanation

Strict identity is transitive within a valid semantic scope; noisy similarity and acceptance decisions are not logical identity facts. Closure enforces an equivalence-shaped output without guaranteeing the correct equivalence relation. Cluster confidence cannot be obtained by relabeling edge scores, taking their average/minimum, or multiplying them without a justified joint model.

A false bridge between otherwise correct components of sizes $m,n$ creates $mn$ false cross-component co-memberships, including the bridge pair. **Derived illustration:** sizes 20 and 30 create 600 false co-clustered pairs from one erroneous accepted edge, 599 beyond that edge itself. No independence assumption or probability estimate is needed for this counting consequence. High accepted-edge precision can therefore coexist with unacceptable final overmerge damage.

## Important variants

A stricter acceptance policy changes the graph; it does not change closure's rule. Streaming edge additions can maintain connectivity through unions, but the fixed-graph traversal bound above is a separate claim. Center-based grouping or partition objectives need different admissibility rules, not merely new names for connected components.

## Assumptions and prerequisites

Require [same-as semantics](../../decisions/identity-semantics.md), a fixed eligibility/time scope, stable record identifiers, and accepted-edge provenance. Verify that no mandatory cardinality/type constraint is being ignored. Optional supporting comparisons can reveal contradictory members, but they must not silently become required complete-graph evidence.

## Applicability conditions

Useful as a transparent deduplication baseline when closure is the intended output and there are no additional membership restrictions. Conditionally exclude it for related-to edges, mandatory one-to-one linkage, or high-harm irreversible unions without an acceptable review and correction policy. These exclusions concern configurations, not every scorer family.

## Advantages

The output is reproducible and independent of edge processing order for the same graph. Every co-membership has a witness path. Sparse graph traversal is inexpensive relative to separately computing many comparisons.

## Trade-offs and failure modes

Chains and hubs can connect distinct entities through weak or erroneous bridges. Missing within-entity paths cause fragmentation. Accepted-edge quality should be inspected by source, degree, and bridge exposure, not only aggregate precision.

Deleting an accepted edge does not necessarily split a component because another path may remain. Ordinary union-only state cannot undo unions. Retain the versioned edge graph and recompute affected connectivity, or use an explicitly deletion-capable design. Rollback must revise memberships and downstream masters while preserving audit history; persistent entity IDs cannot be equated with transient traversal labels.

## Relationships with other methods

[Thresholds and abstention](thresholds-abstention.md) produce accepted, rejected, and deferred edges; reducing edge errors helps but does not establish acceptable cluster risk. [Constrained clustering](constrained-clustering.md) can veto whole-cluster unions using trusted incompatibilities. [Partial assignment](one-to-one-assignment.md) is the relevant alternative for audited bipartite uniqueness. [Master representation](../../decisions/master-representation.md) consumes versioned memberships, not graph labels as permanent identities.

## How to evaluate

Freeze records, candidates, and scores; compare closure with feasible merging and alternative acceptance policies on independent complete entities or design-aware sampled references. Use [entity quality](../../evaluation/entity-resolution-quality.md): induced-pair and record/entity views, fragmentation, largest erroneous merge, affected records, foreign entities swallowed, and application cost. Separately audit [omitted candidates](../../evaluation/retrieval-blind-spots.md). Unknown omitted pairs stay unknown.

## Research opportunities

Inject a single false bridge between independently verified components at varying sizes; remove it and replay corrections. Test tail-risk, membership churn, and rollback latency alongside aggregate quality. Predeclare catastrophic-merge limits before selecting thresholds.

## References and evidence limitations

Source [12], section 2.1, supports the closure mechanism and chaining warning. Its string-based duplicate-detection evaluations do not guarantee performance on a new population. The Atlas reports no measured ER improvement.

## Sources

[12] https://www.vldb.org/pvldb/vol2/vldb09-1025.pdf — Framework for Evaluating Clustering Algorithms in Duplicate Detection
