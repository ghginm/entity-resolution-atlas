---
id: SOL-04-001
type: solution
title: Non-destructive multilingual name representations
domain: "04"
summary: >-
  Retain original names and generate a small, versioned set of canonical, parsed,
  and optional language-aware representations. Each form records its source,
  transformation, uncertainty and intended retrieval or comparison role. Requires
  explicit name semantics and tested transformation behavior. Multiple forms can
  expose otherwise hidden variants without forcing one lossy canonical string,
  but increase collisions, correlated features, storage and comparison cost.
  Script metadata and normalized equality do not establish language or identity.
tags: [person, organization, multilingual, multiscript, provenance, evidence-engineering, noisy]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-04-001]
  complements: [SOL-06-001]
  evaluated_by: [EVAL-11-002, EVAL-11-006]
---

# Non-destructive multilingual name representations

## Summary and problem addressed

A single cleaned string can make comparison convenient while discarding the distinctions needed to reject a merge. This solution keeps the observation and selected alternatives together. It supplies representations to retrieval and comparison, not a universal name canonicalizer or identity classifier. The [representation decision](../../decisions/name-representation.md) owns the choice of acceptable equivalences.

## Core mechanism and theoretical explanation

**Atlas synthesis:** store a representation bundle with the original text, provenance and explicit transformation graph. Each derived form identifies its input observation, transform/version, parameters, availability or failure reason, and purpose. Separate deterministic forms from uncertain parses and source-asserted aliases. Retaining a form does not mean downstream code must use it or count it as independent support.

A deterministic many-to-one transformation cannot distinguish values it maps to the same output. Keeping the original alongside the transformed output preserves the possibility of later discrimination. This information-preservation argument explains the design; it is not proof that more features improve a finite-data scorer. An overly flexible scorer can still learn shortcuts from extra forms.

Generate only justified forms:

- **Canonical Unicode form:** NFC resolves canonical-equivalent encodings. NFD decomposes canonically; NFKD/NFKC also apply compatibility mappings. Compatibility folding can remove meaningful distinctions, so it is not an unconditional cleaning step.[32]
- **Explicit lexical form:** separately version case, spacing and punctuation treatment. NFC does not lowercase, transliterate or remove accents. A lexical transform must have its own rationale and collision tests.
- **Structured form:** keep ordered tokens and optional name-part/organization-role parses with confidence or ambiguity. Do not overwrite unparsed text when a parser fails.
- **Optional variants:** accent-insensitive, alternate-script or phonetic forms can support a retrieval pass or feature. Preserve the scheme and original rather than make the variant a new authoritative observation.

Unicode Script and Script_Extensions describe character usage, including Common and Inherited cases. Mixed-script segmentation needs contextual handling; script-property assignments are version-sensitive.[33] Pin the Unicode data/runtime version in a reproducible bundle. Script is not a language classifier, and unusual scripts need not imply corruption.

## Worked examples and important variants

**Synthetic examples, not measured results:** `Jose\u0301` (a literal illustrative escape for an accent sequence) and precomposed `José` can be represented in one canonical form after decoding the actual code points. `Jose` without the accent is a different input; accent removal is a further, lossy operation. A source may use it consistently, but the system must not record that inferred equivalence as independent corroboration of a name match.

For organizations, keep `Harbor Research Series II Ltd` complete even when a retrieval form drops legal suffixes. `Series III` may distinguish another legal vehicle. A token-set view can aid retrieval after word-order changes while an ordered/typed view retains sequence and role. Neither view supplies the external task's identity definition.

Keep aliases as a collection of observations with source, validity time where known and relation to the named entity. `Formername → Newname` may be a name-change claim; it is not necessarily a merger or continuity proof. Historic aliases from a copied directory should not count as several independent witnesses. Multiple records sharing one acronym remain ambiguous.

Language-aware parsing can differ for particles, patronymics and name order. In the absence of reliable metadata, keep competing interpretations or use unparsed comparison rather than assume a universal Western first/last-name split. Transliteration can create a useful bridge across scripts but can be many-to-one and scheme-dependent. This wave did not verify a specialist transliteration primary source; a consumer must assess a concrete scheme on its languages before adoption.

## Assumptions, applicability and advantages

Hard prerequisites are a stable record/observation reference, access authorization, declared identity semantics and an ability to preserve raw lineage. Language annotations, authoritative aliases and parsers are optional context, not mandatory infrastructure. The approach is useful when representations change across sources or when loss of discriminative tokens is expensive. Clean data may need only original plus NFC.

A bundle makes transformation-induced agreement visible, allows ablation, and supports reprocessing without reconstructing an unavailable original. A retrieval key can deliberately be broad while comparison retains richer distinctions. The two roles exchange record references and transform versions; equality of retrieval keys must not silently become a match label.

## Trade-offs and failure modes

Costs include additional storage, parser maintenance, variant fanout and semantic cache invalidation. Comparing every alias against every alias creates a product of collection sizes, and maximum similarity favors larger collections. Budget or aggregate explicitly and retain the evidence that was skipped. Error or truncation is not evidence of disagreement.

Correlated forms can be double-counted by an additive scorer. Group their lineage and test the combined evidence mechanism rather than multiply each agreement as if obtained independently. Unknown language can route incorrectly; aggressive case/punctuation/diacritic folding can collapse unrelated names. Preserving raw text enables diagnosis but does not by itself prevent these errors or authorize retaining sensitive data indefinitely.

## Relationships and how to evaluate

The [string-comparator menu](../comparison-features/string-comparators.md) consumes forms, [evidence states](../comparison-features/evidence-states.md) records availability and comparability, and [artifact runs](../architecture/versioned-artifact-runs.md) tracks transform changes that may invalidate keys, features and calibration. Keep the bundle contract framework-neutral.

Compare original equality, original plus NFC, and one extra representation family on fixed candidate pairs and controlled scoring capacity. Use [pairwise evaluation](../../evaluation/pairwise-calibration.md), independent labels, source/script slices, qualifier collisions, alias multiplicity and downstream entity errors. Separately test retrieval coverage if variants change admission. Predeclare acceptable runtime, collision and high-cost merge margins; reject added complexity if it provides no practical advantage. Missing independent coverage makes an accuracy conclusion inconclusive.

Use [behavioral tests](../../evaluation/synthetic-metamorphic.md) for normalization idempotence, canonical-equivalent forms under the declared comparator, version/provenance preservation, parser failures and qualifier counterexamples. Permuting raw input order should not change a stateless bundle except declared ordering. These are contract checks, not real-world ER accuracy.

## Research opportunities and evidence limitations

Test which representation adds independent discriminative value rather than duplicate features, and whether cross-source transfer survives different transliteration conventions. Unicode specifies character-processing semantics, not name identity or ER gains.[32][33] All bundle, alias and evaluation recommendations here are Atlas synthesis, and no ER experiment has been run.

## Sources

[32] https://www.unicode.org/reports/tr15 — Unicode Normalization Forms (UAX 15)
[33] https://www.unicode.org/reports/tr24 — Unicode Script Extension Properties (UAX 24)
