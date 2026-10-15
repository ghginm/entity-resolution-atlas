# 03 — Data Understanding & Integration

**Design question:** Which observations are semantically comparable and sufficiently reliable to use?

## Decisions and coverage
- Profile completeness, uniqueness, value distributions, validity, duplicates and changing source coverage; do not infer reliability solely from agreement with current ER predictions.
- Align schemas manually, with rules or learned suggestions; distinguish similarly named fields with different semantics. Canonical, flexible and hybrid representations trade comparison simplicity against retained source detail.
- Identifier semantics require namespaces, issuance authority, formatting rules, reuse and validity periods. Source and attribute reliability are not a single universal source ranking.
- Retain provenance, conflicting observations, temporal data histories and schema versions. Cross-source compatibility includes units, calendars, geography and observation granularity.

## Solution families and useful baselines
- Strict canonical schema; flexible attributes; canonical core plus source extensions.
- Preserve all observations; deferred reconciliation; documented source precedence for a consumer view.

## Ownership and limitations
Source profiling is owned here. Quality-derived pair features are 06; learned weighting is 07; selecting master attributes is 09.

This is a domain map, not complete L2 method coverage. Unexpanded families are retained for [expansion review](../../guides/expansion-plan.md); mature names are not automatic recommendations.

## Cross-domain dependencies
- [04 — Normalization & Enrichment](04-normalization-enrichment.md).
- [06 — Comparison Features & Evidence Engineering](06-comparison-evidence.md).
- [07 — Matching & Scoring](07-matching-scoring.md).
- [09 — Master Entity Construction & Maintenance](09-master-maintenance.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
