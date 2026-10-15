---
id: SOL-05-001
type: solution
title: Exact-key blocking
domain: "05"
summary: >-
  Admit record pairs that share a declared blocking key, using equality on a
  single attribute or a composite of attributes. This creates an interpretable
  candidate baseline when key values are available, stable, and comparable
  across sources. Requires explicit normalization, missing-value handling, and
  identifier semantics. The main risks are complete exclusion after key errors
  and candidate explosion from common values; equality proposes comparison,
  not identity.
tags: [candidate-generation, blocking, interpretable, low-cost, clean, identifiers, entity-agnostic]
maturity: established
evidence: supported-by-external-literature
relations:
  addresses: [DEC-05-001]
  complements: [SOL-06-001, SOL-05-003]
  evaluated_by: [EVAL-11-001]
---

# Exact-key blocking

## Summary and problem addressed

Exact-key blocking narrows the pair space by admitting records sharing a selected value or tuple. It separates inexpensive candidate admission from substantive identity comparison. Traditional blocking groups records on selected fields and compares within those groups; errors in those fields can exclude true matches.[2][5] This card explains equality-based admission, not hard deterministic matching.

## Core mechanism

**Atlas synthesis:** define a key contract specifying attributes, representations, source compatibility, and eligibility. Assign eligible records to their key values. For deduplication, admit distinct unordered record pairs within each block; for cross-source linkage, admit only permitted cross-source combinations. Collapse repeated pair emissions while retaining the block and key reasons.

A composite key such as normalized organization name plus locality requires equality on both components. Exact equality after a phonetic or transliteration transformation is still exact blocking on that representation; transformation tolerance belongs to normalization, and its collisions remain retrieval ambiguity. Never interpret the transformed value as a verified original identifier.

Missing or invalid required components should produce an explicit unavailable-key state, not a shared placeholder block. A separate fallback policy may retrieve such records elsewhere. If multiple aliases create several keys, declare that expansion and preserve their common observation lineage.

## Theoretical explanation

**Mathematical reasoning:** exhaustive within-block comparisons expose a true matching pair precisely when both records are eligible and share at least one admitted key. Equality therefore buys selectivity by assuming the chosen representation survives relevant variation. Adding conjunctive components can only retain or remove candidates when inputs and eligibility remain unchanged; it cannot recover pairs rejected by the broader key.

Large blocks generate many pair combinations: cross-source work depends on both source-specific block sizes, while deduplication work depends on combinations within a block.[2] Total record count alone consequently hides skew. Splitting or dropping large blocks changes coverage unless a verified condition shows that removed pairs cannot be matches.

## Variants, assumptions, and applicability

- **Single key:** useful for a populated, stable attribute; common values may be weakly selective.
- **Composite key:** reduces collisions but compounds missingness and corruption sensitivity.
- **Hierarchical refinement:** subdivides oversized blocks; a conjunction-only hierarchy is stricter, whereas fallback branches define a broader strategy.
- **Multi-valued keys:** admit overlap across aliases or historical values, with greater candidate volume and temporal ambiguity.

These variant descriptions are synthesis grounded in the blocking framework.[2] Preconditions include aligned attribute semantics, documented transformations, and known key availability. Identifier keys additionally require namespace compatibility and consideration of reuse or validity periods. Person, organization, and address examples differ in semantics; no attribute is universally identity-preserving.

## Advantages, trade-offs, and failure modes

**Atlas synthesis:** advantages are inspectable admission reasons, reproducible behavior, and a simple baseline for diagnosing downstream errors. Failure modes include typographical variation, stale values, incomplete composites, incompatible source conventions, placeholders, household-shared contact details, and many-to-one normalization collisions. Shared values need not identify one entity; different values need not prove different entities.

Key agreement also conditions the candidate population. For a pass requiring exact surname agreement, surname agreement is unsurprising among that pass's candidates. Treating it as independent new evidence using unrestricted-pair estimates can misstate its weight. Fellegi–Sunter explicitly discusses blocking's impact on the comparison setting.[1]

## Relationships and evaluation

This solution [addresses candidate strategy](../../decisions/candidate-strategy.md). [Multi-pass blocking](multi-pass-blocking.md) can use exact blocks as constituent routes rather than treating them as incompatible alternatives. [Evidence states](../comparison-features/evidence-states.md) complement retrieval by separating subsequent agreement, missingness, and conflict from admission reasons.

**Atlas synthesis:** use [candidate recall evaluation](../../evaluation/candidate-recall.md) with independent truth coverage. Compare single and composite keys on unique pair volume, segment recall, block-size tails, unavailable-key rates, and total generation plus scoring cost. Audit matches excluded by each additional component. Report capped or refined variants separately from exhaustive blocks, with losses attributed to the exact policy.

## Research opportunities and evidence limits

Test whether source-specific representations or selective fallback keys recover observed exclusions without unacceptable volume. Hold truth scope and downstream scoring fixed; distinguish a new normalization from a new admission rule. The literature establishes blocking mechanisms and risks, not this project's best key.[2][5] Examples and proposed tests are synthesis; no measured Atlas improvement is claimed.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
