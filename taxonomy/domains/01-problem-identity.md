# 01 — Problem Formulation & Identity Semantics

**Design question:** What does one entity mean, and what output constitutes a correct resolution?

## Decisions and coverage
- Deduplication within a source; cross-source linkage; multi-source identity resolution. Define the eligible record-pair universe, not just the observed candidate pool.
- Entity types and identity semantics: a person is not a household; an organization may be a legal entity, branch, or operating group. Same-as identity and related-to relationships require different labels.
- One-to-one, one-to-many, and many-to-many constraints depend on whether source rows are unique entities or repeated observations. Temporal identity specifies how name changes, identifier reuse and organizational succession are treated.
- Pairwise links, entity memberships and uncertain identity alternatives are distinct outputs. Specify asymmetric false-merge/missed-match costs and the unit of harm.

## Solution families and useful baselines
- Strict identity with validated identifiers; source-scoped identities; time-indexed identity definitions.
- Independent scored links; constrained assignment with an unmatched option; membership partitions; uncertainty-preserving links.

## Ownership and limitations
Incremental is a lifecycle choice, collective is an inference strategy, and neither changes the meaning of identity by itself.

This is a domain map, not complete L2 method coverage. Families without applicable detailed cards remain coverage gaps; mature names are not automatic recommendations.

## Cross-domain dependencies
- [03 — Data Understanding & Integration](03-data-integration.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [09 — Master Entity Construction & Maintenance](09-master-maintenance.md).
- [10 — Ground Truth & Labeling](10-ground-truth.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
