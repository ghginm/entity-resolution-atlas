---
id: SOL-06-001
type: solution
title: Explicit comparison evidence states
domain: "06"
summary: >-
  Represent field comparisons with explicit states and supporting context instead
  of treating all non-agreement as the same numeric value. Separate observed
  agreement, partial agreement, disagreement, missingness, invalidity, and
  semantic incomparability. Requires attribute-specific comparison rules and
  provenance; strong contradictions additionally require credible incompatible
  observations. The representation supports interpretable scoring and review,
  but does not prescribe evidence weights, guarantee independence, or make
  missing values identity evidence.
tags: [evidence-engineering, missingness, source-aware, provenance, interpretable, conflicting, uncertainty]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-06-001]
  complements: [SOL-07-001, SOL-07-002, SOL-07-003]
  evaluated_by: [EVAL-11-002]
---

# Explicit comparison evidence states

## Summary and problem addressed

Explicit states prevent a comparator from conflating absent information, noisy disagreement, and credible contradiction. Fellegi–Sunter comparison codes already distinguish missingness, agreement, disagreement, and partial agreement.[1] The state vocabulary and context contract below are **Atlas synthesis**, not a standardized taxonomy from that paper. They describe observations for scoring, not final match dispositions.

## Core mechanism

For each attribute, first establish semantic comparability: field meaning, representation, identifier namespace, and relevant time scope. Then record availability and validity on each side. Only compare values when the applicable prerequisites hold. Preserve the observed outcome, optional similarity, source/time provenance, and reasons for unavailable or unreliable comparison.

Use separate dimensions where states can coexist: lexical agreement can occur between invalid placeholders, and partial agreement can coexist with conflicting components. Do not force one label to erase quality context. An unobserved similarity should remain unavailable, rather than become a measured zero.

**Proposed vocabulary:**

- **Agreement:** comparable observed values agree under the declared representation; normalization-induced agreement remains distinguishable from raw equality.
- **Partial agreement:** observed values share specified components or graded similarity. Describe what agrees and what differs.
- **Observed disagreement:** comparable values differ; the comparison alone does not establish identity incompatibility.
- **Qualified contradiction:** credible observations violate an explicit identity constraint within a compatible namespace and time scope. Record the constraint and reliability rationale.
- **One-sided missing / both missing:** value comparison is unavailable, with side-specific missingness reasons retained.
- **Invalid or unreliable:** the observation or transformation fails a quality requirement; apparent equality need not be meaningful.
- **Incomparable:** meanings, namespaces, granularities, or temporal semantics do not permit the requested comparison.

Illustrative synthesis: two absent birth dates are both missing, not an agreement; a malformed date is invalid, not a different birth date. Different local identifiers from different issuers are not automatically contradictory. Historical addresses can disagree while remaining consistent with one person's movement.

## Theoretical explanation

A representation that maps missingness and valid disagreement to one value prevents every downstream scorer using only that representation from distinguishing those cases. Keeping states retains that information, though a larger feature space may require more estimation evidence. This is an information-preservation argument, not proof of better prediction.

Under likelihood-ratio scoring, a state contributes support according to how often it occurs among matches relative to nonmatches, not its label alone.[1] Thus observed agreement is not automatically strong support, and missingness is not inherently neutral or negative statistically. Treating missingness as identity evidence requires population-specific justification; its observational meaning remains absence of comparison. The additive simplification additionally requires conditional independence between evidence groups.[1]

## Variants, prerequisites, and applicability

**Atlas synthesis:** variants include categorical states, continuous similarities with availability masks, ordinal agreement levels, and component-level vectors for structured attributes. Multi-valued histories need explicit aggregation: best-pair agreement alone can hide contradictory observations. Preserve which values generated each outcome.

Prerequisites are attribute-specific semantics, trustworthy quality indicators, and accessible provenance. The approach is especially useful for sparse, heterogeneous, or conflicting records, but also makes clean-data defaults auditable. Several normalized forms of one value should share a dependency lineage, not count as independent facts.

## Advantages, trade-offs, and failure modes

States make explanations, missingness diagnostics, and controlled scorer comparisons possible. Costs include vocabulary design, sparse combinations, and maintaining consistent meaning across sources. A falsely declared contradiction can become an unjustified veto; a missingness feature can learn collection practices that fail under source shift. Copies and correlated transformations can still double-count evidence. The literature discusses practical dependency limitations; explicit states do not resolve them automatically.[5]

## Relationships and evaluation

This solution [addresses comparison evidence](../../decisions/comparison-evidence.md) and complements [additive soft matching](../matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../matching-scoring/fellegi-sunter.md), and [logistic regression](../matching-scoring/logistic-regression.md). Each supplies a different combination mechanism; no state is a prescribed weight. [Name representations](../normalization/name-representations.md), [string comparators](string-comparators.md) and [namespace-qualified identifiers](identifier-namespaces.md) supply observations and compatibility context rather than automatic weights or policy actions.

**Atlas synthesis:** use [pairwise quality and calibration evaluation](../../evaluation/pairwise-calibration.md). Compare collapsed versus explicit states on the same candidates with controlled scorer capacity. Audit state assignment before measuring prediction; inspect missing, invalid, contradictory, source-pair, and temporal segments. Assess robustness after source shifts and retrieval changes, since candidate admission conditions observed evidence.

## Research opportunities and evidence limits

Test whether quality-qualified contradictions reduce harmful rejections, or source-specific missingness improves transfer rather than shortcuts. Ablate representation families and dependency groups. The precise contract remains synthesis informed by comparison-vector theory; no Atlas result establishes superiority.[1][5]

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
