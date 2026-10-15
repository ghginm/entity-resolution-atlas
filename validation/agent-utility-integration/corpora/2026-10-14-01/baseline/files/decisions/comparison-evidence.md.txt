---
id: DEC-06-001
type: decision
title: Design comparison evidence before choosing a scorer
domain: "06"
summary: >-
  Choose how two records become interpretable comparison evidence, keeping
  value agreement, absence, validity, contradiction, and contextual reliability
  distinct. Requires aligned attribute semantics, observation provenance, and
  declared comparison scope. Compare a compact state-based baseline with
  richer attribute, frequency, temporal, and representation features. More
  features can expose useful variation but also duplicate the same observation
  or encode source shortcuts; weighting and final action remain separate
  downstream decisions.
tags: [evidence-engineering, missingness, source-aware, frequency-aware, interpretable, uncertainty, entity-agnostic]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  complements: [DEC-07-001]
  evaluated_by: [EVAL-11-002]
---

# Design comparison evidence before choosing a scorer

## Decision question and problem context

What information should a pairwise comparison expose so downstream scoring can distinguish identity support, uncertainty, and genuine incompatibility? Fellegi–Sunter comparison vectors explicitly allow agreement, disagreement, missing values, and partial address agreement rather than requiring one generic similarity number.[1] Evidence engineering defines those observations; it does not itself choose weights, probabilities, thresholds, or entity assignments.

The same similarity can have different implications across sources, identifier systems, and observation times. Retrieval further selects which pairs reach comparison. The [candidate strategy decision](candidate-strategy.md) therefore supplies context, while the [scoring decision](scoring-strategy.md) determines how evidence will be combined.

## Assumptions and prerequisites

**Atlas synthesis:** establish comparable field meanings, normalization lineage, validity checks, source provenance, observation times, and identity semantics. Preserve raw values alongside derived forms. Identifier comparison requires a namespace, issuing authority where relevant, and reuse or validity rules. An identifier can be lexically different without contradiction if namespaces differ; identical local numbers can be unrelated.

Determine what absent values mean: uncollected, unknown, redacted, failed parsing, or genuinely inapplicable. Missingness is neither observed agreement nor observed contradiction. It can nevertheless carry population-specific predictive information; that inference belongs in an explicitly tested scorer, not an undocumented comparison default.

## Alternatives and solution links

- [Explicit evidence states](../solutions/comparison-features/evidence-states.md): separate comparability, observed agreement, partial agreement, disagreement, and unavailable information. This is the expanded pilot baseline.
- **Taxonomy-only, unexpanded:** attribute-specific string, token, phonetic, and linguistic comparisons expose different variation; continuous values retain resolution but need documented meaning and missing-value handling.
- **Taxonomy-only, unexpanded:** frequency/rarity, source-quality, and temporal features qualify observations with context rather than replacing value comparison.
- **Taxonomy-only, unexpanded:** embeddings, relational context, multi-valued comparisons, and interaction features offer richer representations, with additional provenance and dependency questions. These are not linked to nonexistent Solution Cards.

A raw exact-agreement flag remains a useful controlled comparator, but collapsing every other outcome to one value loses the distinction between no information and contradictory information. Richer alternatives should address observed ambiguity rather than accumulate features indiscriminately.

## Choice criteria and trade-offs

**Atlas synthesis:** assess semantic validity, interpretability, transfer across source pairs and languages, availability, acquisition cost, and resilience to normalization errors. Compare what each feature reveals that existing features do not. For multiple aliases, specify whether comparison uses best agreement, overlap, or observed conflicting histories; maximum similarity can conceal disagreements and favors records with more opportunities to match.

A contradiction should require meaningful comparability and credible incompatible observations. A changed address is not inherently incompatible with enduring person identity. Shared household contact details may agree without being entity-unique. Reliability is contextual: source reputation alone does not establish accuracy for every field or time period.

Multiple representations of one name, parsed address components, and copied observations are potentially dependent evidence. The additive Fellegi–Sunter simplification assumes comparison groups are independent conditional on match status; the general joint formulation does not require that factorization.[1] The landscape discusses limitations of practical independence assumptions.[5] Preserve dependency groups instead of treating every transformation as independent corroboration.

## Baseline and related evaluations

**Atlas synthesis:** begin with a small attribute-specific evidence vector: explicit states, observed similarities where applicable, validity, and source/time context that is already available. Keep derived weighting separate. Compare this baseline against a collapsed-state representation and then add one contextual feature family at a time.

Use [pairwise quality and calibration evaluation](../evaluation/pairwise-calibration.md) with fixed candidate pairs, controlled scorer capacity, and source/entity-disjoint assessment where appropriate. Diagnose errors by evidence pattern and missingness segment, not only aggregate discrimination. Repeat after retrieval changes: agreement required by admission is not fresh independent support, and candidate-conditional distributions may differ from unrestricted-pair estimates. No evidence representation alone guarantees calibrated scores.

## Open questions and evidence limits

Can reviewers distinguish unavailable evidence from true conflict? Which apparently separate features descend from one observation? Does context improve transfer or merely encode source identity? The [frequency-aware hypothesis](../research/hypotheses/frequency-aware-evidence.md) and [contextual-reliability hypothesis](../research/hypotheses/contextual-reliability.md) propose tests, not validated improvements. The literature supports comparison-vector theory and dependency cautions, not this card's exact feature contract.[1][5] Recommendations are Atlas synthesis; no Atlas experiment has been run.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
