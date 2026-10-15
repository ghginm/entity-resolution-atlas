---
id: DEC-08-001
type: decision
title: Choosing the resolution output and membership policy
domain: "08"
summary: >-
  Choose independent pair decisions, partial one-to-one assignment, accepted-link
  closure, or constrained entity membership from the task's identity and
  cardinality contract. Distinguish semantic transitivity from noisy observed
  links, genuine cannot-links from weak or absent evidence, and pair-level
  objectives from entity-level harm. The comparison identifies credible
  baselines, prerequisites, incompatible configurations, downstream master
  responsibilities, and controlled evaluations without assuming clustering is
  required or universally safer.
tags: [entity-agnostic, pairwise, assignment, clustering, constraints, asymmetric-costs, uncertainty, source-aware]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  complements: [DEC-09-001]
  evaluated_by: [EVAL-11-003, EVAL-11-004]
---

# Choosing the resolution output and membership policy

## Decision question

What output is authorized: independently actionable pair links, a partial cross-source matching, or a partition representing entities? Choose its admissible structures before optimizing scores. A convenient clustering implementation does not establish that the application needs clusters.

## Problem context

**Atlas synthesis:** downstream users may need correspondence between two registries, deduplicated entities, or relationship edges. These are different contracts. Clustering is wrong for related-to, household membership, asymmetric attribution, or overlapping categories presented as strict same-as identity. It is also unnecessary when only separable pair decisions are consumed and no persistent entity membership is asserted.

Membership and canonical attribute construction are separate responsibilities. A coherent partition can still contain erroneous entities; a plausible master name cannot justify merging them. Define [master representation](master-representation.md) after deciding membership, with evidence and unresolved cases retained.

## Relevant assumptions

Fix [identity semantics](identity-semantics.md), entity type, source namespaces, record eligibility, and time scope. Strict same-as is transitive within that contract: if two assertions are true, their implication follows. Measured similarities and accepted noisy edges need not be transitive. Taking their closure therefore adds identity assertions, not measurements.

Duplicate-free two-file linkage implies at most one counterpart at **each** endpoint; two files alone do not justify this assumption.[11] Multifile partitioning can distinguish within-file duplication from cross-file overlap instead of imposing the same cardinality everywhere.[14]

**Atlas synthesis:** a cannot-link is a trustworthy semantic prohibition, with provenance and scope. Low scores are fallible evidence; missing candidates or unmeasured pairs are unknown. Rejection means no link under the current policy unless separately justified as a durable prohibition. Must-links need the same trust audit.

## Available solution families

- **Independent pair decisions:** [thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md) choose actions without enforcing membership or shared-endpoint competition.
- **Partial assignment:** [one-to-one matching](../solutions/decision-resolution/one-to-one-assignment.md) chooses compatible edges and explicit unmatched alternatives across two eligible sets.
- **Unconstrained closure:** [connected components](../solutions/decision-resolution/connected-components.md) returns components of accepted links; its graph-fragility/repair section distinguishes bridge diagnostics from verified corrections. This partitioning mechanism is described in duplicate-detection research.[12]
- **Constrained membership:** [constrained clustering](../solutions/decision-resolution/constrained-clustering.md) compares local feasible merges and partition-level objectives; hard feasibility and soft evidence preference have different roles. Must-link propagation does not make cannot-link transitive, and typed related-to edges do not become identity constraints.

The remaining comparisons and proposed experiments are Atlas synthesis, not reported source rankings.

## Criteria for choosing

Declare objective **units**: false pair decisions, incorrect record assignments, contaminated entities, affected records, financial loss, or review effort. State their denominator and whether costs are additive. Summing edge scores optimizes a numerical surrogate, not automatically any of these losses. A probability-based expected-loss interpretation requires probabilities appropriate to the decision information and loss structure; pair calibration alone does not establish coherent assignment or partition uncertainty.

Ask whether a false bridge can expose many records, whether unlinked means genuinely absent or unresolved, and whether corrections must preserve external IDs. Review uncertainty at the decision unit, including competing matches or disputed cluster merges.

## Trade-off comparison

Independent policies are transparent but can produce contradictory membership implications. Assignment prevents endpoint reuse but suppresses legitimate links when within-source duplicates exist. Closure is simple and deterministic for a fixed graph but cannot weigh contrary evidence once edges are accepted. Constrained membership can block specific harmful unions but systematically undermerge if its constraints misdescribe repeated observations or temporal identity.

Compatibility is conditional: any scorer can supply evidence to any suitable resolver through a documented artifact. Interaction risks include candidate omissions removing competition, calibration shifts after retrieval changes, and false positives amplified by closure. Exclude unconstrained closure when it can violate mandatory source/type/time restrictions; do not declare probabilistic scoring itself incompatible with clustering.

## Good baseline candidates

Use independent threshold/review decisions for truly separable actions; partial maximum-utility matching for audited duplicate-free bipartite linkage; closure for an eligible equivalence task without additional restrictions. With trustworthy restrictions, compare conservative feasible merging against a partition-level objective. A more complex resolver must demonstrate value beyond constraint satisfaction.

## Prerequisites

Supply record and source identifiers, candidate provenance, score meaning, cost assumptions, constraint ownership, and an explicit unresolved-state contract. Optional relational evidence may help but is not a prerequisite. Independent evaluation labels are required to estimate quality, not to execute every unsupervised baseline.

## Open questions

Which observations genuinely establish impossibility? Can repeated records be collapsed safely before assignment? What must be replayed after deletion, evidence revision, or a constraint correction? Who approves high-impact unions?

## Related evaluations

Freeze candidates, scores, records, and semantics when comparing resolution mechanisms. Use [final-output diagnostics](../evaluation/entity-resolution-quality.md) for overmerge tails, fragmentation, assignment accuracy, review coverage, and cost. Audit [retrieval blind spots](../evaluation/retrieval-blind-spots.md) separately; unknown omitted pairs cannot become negative labels. Predeclare practical gains and catastrophic-error guardrails on independent, entity-aware holdouts.

## Links to Solution Cards

Follow the four families above for their mechanisms and tests. Sources [11], [12], and [14] support the specific structural contexts cited, not universal rankings. No Atlas ER experiment or validated project operating point is claimed.

For implementing conditions, overrides and fallbacks, use the separate [rule-composition decision](rule-composition.md). It compares an explicit ordered policy with declarative tables; it does not change the identity/cardinality contract selected here. A pre-merge guard must inspect the proposed cluster union where that is its scope. A post-merge contradiction alarm does not reverse an unsafe union without an authorized repair path.

## Sources

[11] https://arxiv.org/abs/1601.06630 — Bayesian Estimation of Bipartite Matchings for Record Linkage
[12] https://www.vldb.org/pvldb/vol2/vldb09-1025.pdf — Framework for Evaluating Clustering Algorithms in Duplicate Detection
[14] https://arxiv.org/abs/2110.03839 — Multifile Partitioning for Record Linkage and Duplicate Detection
