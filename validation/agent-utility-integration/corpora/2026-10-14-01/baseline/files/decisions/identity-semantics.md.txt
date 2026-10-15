---
id: DEC-01-001
type: decision
title: Define identity before choosing resolution
domain: "01"
summary: >-
  Define the real-world object, granularity, namespace and time scope that a
  correct identity assertion denotes. Distinguish source records from entities
  and strict same-as from related-to edges before choosing labels, cardinality
  constraints or output structures. Compare enduring identity, time-scoped
  state identity and relationship-only linkage. The choice needs domain-owner
  adjudication of identifier reuse and continuity; neither similar attributes
  nor a convenient clustering algorithm supplies those rules. Ambiguous cases
  can remain unresolved rather than becoming false equivalences.
tags: [entity-agnostic, identifiers, constraints, uncertainty, governance, source-aware]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [DEC-09-001]
  evaluated_by: [EVAL-11-003]
---

# Define identity before choosing resolution

## Decision question

What does “the same entity” mean for this task, and which assertions may the system publish? Choose a semantic target before similarity, thresholds or graph closure. This card's definitions, examples and recommendations are **Atlas synthesis**, not universal laws for people, organizations or identifiers.

## Problem context

A record is a source observation or administrative representation, not the real-world entity itself. Several rows may describe one person; one household row may describe several people. A row containing payer and beneficiary cannot acquire one person identity without first separating roles. Schema alignment, identifying objects and fusing their attributes are distinct responsibilities in the data-fusion literature.[13]

Specify type and granularity: person versus household, legal organization versus operating brand, building versus dwelling, product model versus physical item. Compare records only for a declared role and type. Cross-type relations such as person-employed-by-organization may be useful without being same-as assertions.

## Relevant assumptions

Strict same-as, within a fixed target definition, is an equivalence relation: reflexive, symmetric and transitive. Fallible predicted links are not guaranteed to satisfy its truth conditions. Related-to predicates need their own direction and algebra; do not borrow transitivity from identity.

**Illustrative counterexample:** Alice and Bob share telephone T1; Bob and Carol share T2; Alice and Carol share neither. “Shares at least one telephone” holds for the first two pairs but not the third. Connected-component closure would assert the missing relationship and could incorrectly merge three distinct people. Shared contact is evidence or a typed relationship, not an identity definition.

An identifier needs issuer, namespace, type, validity interval and reuse policy. Equal local customer numbers in different systems are not global identity. A recycled identifier may denote different entities at different times. Unknown reuse is uncertainty, not permission to assume permanence.

## Available solution families

- **Enduring real-entity identity:** preserve continuity across attribute changes, with [time-scoped evidence](../solutions/identity-semantics/temporal-identity.md). It supports longitudinal histories but needs adjudicated continuity rules.
- **Snapshot/state identity:** identify entity-at-time or episode, explicitly linking states if needed. It suits state reconciliation but deliberately fragments enduring entities.
- **Source-scoped identity:** reconcile administrative accounts inside a namespace without claiming worldwide real-entity equivalence. Cross-source correspondences remain separate assertions.
- **Relationship-only linkage:** publish typed related-to edges or ranked alternatives without collapsing nodes. It preserves legitimate many-to-many associations at the cost of leaving deduplication unresolved.

These targets are competing task definitions, not interchangeable algorithms evaluated against one unlabeled notion of truth.

## Criteria for choosing

Ask which object a downstream action affects, whether past and present records must join, what false equivalence would harm, and which distinctions consumers must retain. Migration, renaming or changing contact information does not decide continuity by itself. Organizational succession may mean continuing operations but a different legal entity; obtain project-specific rules or retain an unresolved succession relationship.

## Trade-off comparison

Enduring identity enables longitudinal aggregation but can hide identifier reuse or succession boundaries. State identity makes time boundaries explicit but can underjoin a person history. Namespace identity avoids unsupported global claims but cannot directly answer global deduplication. Relationship graphs express richer associations but do not provide a partition for counting unique entities. Evaluate each against its declared purpose, not against another target's labels.

## Good baseline candidates

Start with typed, source-scoped observations and conservative identity assertions backed by audited identifier semantics; retain unknown cases. If the question is only current-state reconciliation, use a declared snapshot baseline rather than silently assuming lifetime continuity. Compare with enduring identity only after defining compatible longitudinal truth.

## Prerequisites

Domain-owner definitions, source-row multiplicity, eligible populations and adjudication examples are prerequisites. Optional timestamps help only when their meaning is known. Label guides must distinguish same-as, related-to, different and unknown, including the target role/time; unresolved evidence is not a negative label.

The [resolution decision](resolution-strategy.md) consumes this contract. One-to-one across two files is justified only if each has at most one eligible representation per target unit in scope. Repeated visits or accounts may require many-to-one membership instead. Pair links, assignments, partitions and uncertain alternatives are different output promises. Closure is conditionally excluded for a nontransitive relationship target; probabilistic scoring itself is not excluded.

## Open questions

Can a source key be reassigned? Does account migration preserve person identity, account identity, both or neither? Is a corporate successor the same object at the chosen granularity? Who can authorize changing a definition and relabeling history?

## Related evaluations

[Final output evaluation](../evaluation/entity-resolution-quality.md) must match the promised semantics and include ambiguity, source multiplicity and temporal boundary cases. Compare semantic-policy disagreements separately from retrieval/scorer errors. No Atlas performance result is asserted.

## Links to Solution Cards

[Temporal identity](../solutions/identity-semantics/temporal-identity.md) operationalizes enduring identity; [provenance-preserving survivorship](../solutions/master-records/provenance-survivorship.md) constructs values only after membership. [Master representation](master-representation.md) keeps persistent IDs independent of whichever attribute is displayed.

## Sources

[13] https://www.bioinf.jku.at/teaching/ss2011/se-inf/data_fusion_a1-bleiholder.pdf — Data fusion
