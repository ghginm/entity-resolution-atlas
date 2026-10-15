# 06 — Comparison Features & Evidence Engineering

**Design question:** What similarities, contradictions and contextual observations should a scorer see?

## Decisions and coverage
- String similarities, phonetic/linguistic comparisons and attribute-specific name/address/date/phone features express different error tolerances. Identifier evidence distinguishes exact/partial agreement, namespace compatibility and trusted contradiction.
- Rarity/frequency-aware evidence, source-aware quality features and temporal compatibility change the interpretation of equal similarities.
- Missingness states distinguish both missing, one-sided missing, invalid values and reliable disagreement. Multi-valued aliases/histories require an aggregation policy and count/quality context.
- Embeddings and relationship/graph context may add information but can encode related-to rather than same-as. Feature interactions, provenance groups and dependency checks prevent double counting and label leakage.

## Solution families and useful baselines
- Explicit evidence-state comparison vectors with validity masks.
- Continuous/categorical similarities; grouped multi-representation features; frequency, source, temporal and relational context.

Current selected mechanisms are [character/token/phonetic comparisons](../../solutions/comparison-features/string-comparators.md) and [namespace-qualified identifiers](../../solutions/comparison-features/identifier-namespaces.md), composed with [evidence states](../../solutions/comparison-features/evidence-states.md). Weighting belongs downstream; copied/derived agreements are not independent corroboration.

## Ownership and limitations
Comparison computes evidence; 07 estimates its contribution. Graph features derived from predicted memberships require train/test separation and explicit feedback assumptions.

This is a domain map, not complete L2 method coverage. Families without applicable detailed cards remain coverage gaps; mature names are not automatic recommendations.

## Cross-domain dependencies
- [03 — Data Understanding & Integration](03-data-integration.md).
- [04 — Normalization & Enrichment](04-normalization-enrichment.md).
- [07 — Matching & Scoring](07-matching-scoring.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [10 — Ground Truth & Labeling](10-ground-truth.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
