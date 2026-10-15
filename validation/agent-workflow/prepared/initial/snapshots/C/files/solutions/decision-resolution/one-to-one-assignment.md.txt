---
id: SOL-08-002
type: solution
title: Partial one-to-one assignment for bipartite linkage
domain: "08"
summary: >-
  Resolve competing cross-source candidates through a maximum-utility partial
  bipartite matching with at most one match at both endpoints and explicit
  unmatched alternatives. The method requires defensible source cardinality,
  comparable utilities, and sufficient candidate coverage; it does not turn
  arbitrary scores into probabilities. A derived greedy counterexample,
  uncertainty handling, duplicate-related exclusions, and controlled comparisons
  explain when joint assignment is useful and how to hand off stable membership
  without making master-record or accuracy guarantees.
tags: [entity-agnostic, assignment, source-aware, constraints, asymmetric-costs, uncertainty, batch]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-08-001]
  alternative_to: [SOL-08-004]
  complements: [SOL-08-001, SOL-09-001]
  evaluated_by: [EVAL-11-003, EVAL-11-004]
---

# Partial one-to-one assignment for bipartite linkage

## Short summary

Choose links jointly rather than independently when records compete for counterparts. Sadinle formulates duplicate-free two-file linkage as a bipartite matching, with at most one selected edge in every row and column.[11] Unmatched and unresolved must remain distinguishable outputs.

## Problem addressed

Thresholding may accept two records against the same counterpart. If both files contain at most one observation per entity in the declared scope, those decisions contradict the contract. Conversely, a forced complete assignment manufactures links when sources overlap only partially. The following utility specification and operational guidance are **Atlas synthesis**, not a claim that all assignment scores are calibrated probabilities.

## Core mechanism

Let $A,B$ be eligible record sets and $E\subseteq A\times B$ the allowed candidates. Binary $x_{ij}$ selects an edge; binary $z_i,w_j$ select each endpoint's unmatched alternative. Choose a feasible maximum of

$$
\sum_{(i,j)\in E}u_{ij}x_{ij}+\sum_{i\in A}a_i z_i+\sum_{j\in B}b_j w_j,
$$

subject to

$$
\sum_{j:(i,j)\in E}x_{ij}+z_i=1,\qquad
\sum_{i:(i,j)\in E}x_{ij}+w_j=1.
$$

Here $u_{ij}$ is link utility and $a_i,b_j$ are unmatched utilities, all in the same declared units. These equalities encode **at most one real counterpart on both sides**, not mandatory real links. Dedicated dummy choices can represent unmatched actions; a single shared dummy would incorrectly limit their capacity. Relative to the all-unmatched baseline, selecting an edge gains $u_{ij}-a_i-b_j$.

**Derived illustrative counterexample, not measured data:** with zero unmatched utility, let $u_{ax}=9$, $u_{ay}=8$, $u_{bx}=8$, and $u_{by}=0$. Descending greedy selection takes $ax$ and achieves 9, whether it also takes the zero edge or leaves endpoints unmatched. Joint selection of $ay,bx$ achieves 16. Exhaustive enumeration of the seven feasible partial matchings verifies the optimum; greedy's first choice blocks both useful alternatives.

## Theoretical explanation

Joint optimization maximizes the stated additive utility **on the supplied feasible graph**; it does not prove identity accuracy. Sadinle derives a log-likelihood-ratio assignment interpretation under conditional independence of comparison vectors given the matching, and distinguishes it from posterior expected-loss decisions.[11]

Choose utilities from documented operational value, a justified likelihood objective, or expected loss under a coherent model. A heuristic score sum is permissible as a declared surrogate, but its scale and unmatched offset determine link count. Independent calibrated pair probabilities need not obey competition constraints; they are not automatically posterior assignment probabilities.

## Important variants

Compare greedy feasible matching, exact maximum-utility matching, and loss-based partial decisions with deferral. Sadinle's rejection option permits uncertain matching decisions to remain undeclared, separately from explicit nonmatches.[11] Review is not an unmatched assertion; it needs a cost and a feasible completion policy for competing records.

## Assumptions and prerequisites

Audit both sources for within-source duplication in the relevant time/type scope. If two $A$ records genuinely represent the entity in one $B$ record, the desired truth is infeasible under one-to-one constraints. Use validated within-source entity units or a different membership model; never remove duplicates silently merely to fit the solver. Define utility provenance, candidate eligibility, and evidence versions.

## Applicability conditions

Appropriate for duplicate-free registry correspondence, including incomplete overlap. Conditionally exclude raw-record assignment for repeated events or longitudinal observations of the same entity. Multifile partitioning explicitly models source-specific duplication and overlap rather than assuming universal uniqueness.[14]

## Advantages

Endpoint competition becomes explicit and auditable. Unmatched alternatives avoid filling weak links merely to exhaust a source. A stable tie rule makes repeated optimization reproducible for identical inputs.

## Trade-offs and failure modes

Missing true candidates cannot be selected; missing rivals can make a weak candidate appear unopposed. Candidate caps and independent block processing can alter the global optimum when competition crosses boundaries. Exact ties and near-optimal alternatives signal decision ambiguity: compare objective gaps and perturbation sensitivity, not just the selected edge's score. These are diagnostics, not uncertainty probabilities.

## Relationships with other methods

[Threshold/review policy](thresholds-abstention.md) supplies admissibility or actions but cannot undo competition by thresholding blindly after optimization. [Constrained clustering](constrained-clustering.md) is an alternative when source duplication requires larger memberships. Export record-to-membership decisions, unmatched/deferred status, alternatives, and versions to [provenance and survivorship](../master-records/provenance-survivorship.md). Deterministic assignment does not create persistent master IDs; preserve identity history across reassignment.

## How to evaluate

Freeze candidates, utilities, and cardinality across greedy and joint comparisons. On independently adjudicated eligible entities, measure wrong-counterpart rate, missed links, unmatched correctness, review coverage, constraint violations, and declared cost. Use [final-output quality](../../evaluation/entity-resolution-quality.md) and [retrieval-blind-spot audits](../../evaluation/retrieval-blind-spots.md); add candidate-omission and competing-neighbor stress tests without treating unknown pairs as negatives.

## Research opportunities

Test whether ambiguity-directed review reduces assignment loss at a fixed budget. Require an independent holdout and a predeclared harm guardrail; improvement in objective value alone is insufficient.

## References and evidence limitations

Verified January 2016 arXiv v1 supports bipartite structure and model/loss-specific decisions, not blanket probability interpretation or universal superiority.[11] All numerical examples are derived illustrations; no Atlas ER outcomes are reported.

## Sources

[11] https://arxiv.org/abs/1601.06630 — Bayesian Estimation of Bipartite Matchings for Record Linkage
[14] https://arxiv.org/abs/2110.03839 — Multifile Partitioning for Record Linkage and Duplicate Detection
