# 09 — Master Entity Construction & Maintenance

**Design question:** How should resolved entities be represented, updated and corrected without hiding evidence?

## Decisions and coverage
- Golden records, linked-record/virtual entities and hybrid master representations offer different consumer simplicity and provenance visibility.
- Attribute survivorship can use source precedence, recency, field confidence or multiple values; observation time is not necessarily validity time.
- Stable entity identifiers, temporal histories and field/source/decision lineage must survive incremental membership maintenance.
- Reversible merges and entity splits need ID redirection/versioning and downstream correction semantics. Identity relationships must remain distinct from other relationships. Entity confidence cannot be inferred by multiplying dependent edge scores.

## Solution families and useful baselines
- Membership-preserving virtual entities with a derived canonical view; a documented golden-record policy.
- Versioned entities, uncertainty-preserving attribute alternatives and explicit merge/split histories.

## Ownership and limitations
08 decides membership. This domain decides representation and identity-maintenance consequences; audit/control permissions remain in 14.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for expansion review (source repository only); mature names are not automatic recommendations.

## Cross-domain dependencies
- [03 — Data Understanding & Integration](03-data-integration.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [13 — Scalability & Execution](13-scalability-execution.md).
- [14 — Explainability, Governance & Monitoring](14-governance-monitoring.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
