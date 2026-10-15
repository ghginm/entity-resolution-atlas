---
id: DEC-04-001
type: decision
title: Choose name representations without erasing identity evidence
domain: "04"
summary: >-
  Choose conservative normalization, parsed structure, and optional language-aware
  variants while retaining original names and transformation lineage. Compare
  exact or canonically normalized equality with multiple representations rather
  than one destructive cleaning function. Requires declared identity semantics,
  script and source context, and a distinction between retrieval keys and scoring
  evidence. Broader equivalence can recover plausible variants but also collapse
  subsidiaries, geographic qualifiers, and series distinctions; apparent string
  agreement is not proof of identity.
tags: [person, organization, multilingual, multiscript, noisy, evidence-engineering, provenance]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  complements: [DEC-06-001, DEC-05-001]
  evaluated_by: [EVAL-11-002, EVAL-11-006]
---

# Choose name representations without erasing identity evidence

## Decision question and problem context

Which transformations should make a name comparable, and which distinctions must remain available to decide identity? This domain transforms **one observation**; the [comparison decision](comparison-evidence.md) compares observations, and the [scoring decision](scoring-strategy.md) interprets their evidential contribution. Choosing a representation is therefore not choosing a match policy.

**Atlas synthesis:** start from the external project's identity definition. Legal entities, branches, brands, corporate groups and product series may require different distinctions. A geographic or organizational suffix that is irrelevant to one task can separate identities in another. Do not infer those semantics from a normalization dictionary.

## Relevant assumptions and prerequisites

Retain original text, source field meaning, observation time, encoding/decoding status and transformation version. Identify whether the input is a person name, legal organization name, trading name, historical name or uncertain mixture. Missing language or name-part metadata must remain unknown rather than be guessed as fact. Script metadata can guide processing but cannot uniquely determine language; one language can use several scripts and shared characters require context.[33]

Unicode normalization defines canonical and compatibility equivalence, not real-world identity. NFC preserves canonical equivalence; NFKC additionally folds compatibility distinctions that can matter semantically. Unicode explicitly cautions against applying compatibility normalization indiscriminately.[32] Whichever form is selected, original text remains necessary for review.

## Available solution families and trade-off comparison

1. **Raw equality:** minimal transformation and easy explanations. It misses encoding and typographic variants but exposes a useful control against over-cleaning.
2. **Conservative canonical representation:** [raw plus NFC and declared lexical transforms](../solutions/normalization/name-representations.md). This removes selected representational variation without claiming that every remaining difference is identity-relevant. Case folding, punctuation changes and accent stripping are separate operations, not automatic consequences of NFC.
3. **Parsed and multiple representations:** preserve full text, name parts, token sequences, optional token sets and each transformation's provenance. Parsing enables component comparisons, but an incorrect family/given-name assignment can introduce error. Keep uncertain parses separate rather than promote one interpretation to truth.
4. **Language-aware variants, aliases and transliteration:** potentially useful where cross-script variants prevent retrieval. They require a declared scheme, variant provenance and checks for collisions. A specialist primary transliteration method was not verified in this wave; this card does not endorse a particular system or promise transliteration accuracy.

The [string-comparator solution](../solutions/comparison-features/string-comparators.md) compares these forms using exact, edit, token or phonetic mechanisms. It does not require producing all variants. Broader representations increase storage, comparison opportunities, cache dependencies and maintenance cost. Extra forms generated from one observation remain dependent evidence, not corroborating sources.

## Criteria for choosing and counterexamples

**Illustrative synthesis:** `Northbank Holdings Ltd` and `Northbank Holdings East Ltd` might be distinct legal entities. Removing `Ltd` alone and retaining the full form differs materially from also deleting `East`. Likewise a parent `Northbank` and subsidiary `Northbank Services` are not made identical by high token overlap. Test qualifiers that distinguish geography, legal form, organizational role and numbered series before removing them. Some qualifiers are unstable noise; their removal must be justified by the task, not by increased similarity alone.

For people, token reordering can recover an inverted presentation but also confound given-name/family-name roles. An alias is a claim associated with a source and time, not necessarily an unconditional synonym. A name change may be consistent with enduring identity; a shared current name does not establish it. When aliases are numerous, best-of-all comparisons create more opportunities for accidental agreement. Preserve alias count, quality and conflicting evidence as context rather than expose only the maximum similarity.

Choose the smallest representation set addressing observed errors. On clean single-script data, a fixed conservative form may be cheaper and safer than language routing. On mixed-script data, failure to retrieve known transliterations may justify a separate variant pass while comparison retains the original script and identifiers. Visually similar cross-script letters are not automatically the same character or identity.

## Baselines, related evaluations and adoption rules

Use raw exact agreement and then conservative normalized equality as separate baselines. In the [controlled experiment](../solutions/experimentation/controlled-comparison.md), freeze candidates and scorer capacity while changing one representation family. This tests comparison behavior; rerun end-to-end retrieval separately if blocking keys also change. Otherwise an apparent scorer improvement could be caused by admission of easier pairs or loss of hard cases.

Use [pairwise evaluation](../evaluation/pairwise-calibration.md) on independently justified labels, sliced by source, script/language where known, entity type, rare names, qualifiers and alias multiplicity. Use entity-disjoint transfer splits for unseen identities, or declared forward-time continuation splits for existing identities. Measure false merges as well as recovered variants, review cost and runtime. A lower string distance is not an outcome metric. With incomplete truth, use the [incomplete-reference route](../evaluation/incomplete-reference-quality.md) rather than treat unknown pairs as nonmatches.

[Behavioral tests](../evaluation/synthetic-metamorphic.md) should cover canonical-equivalence behavior, preserving raw provenance, and identity-changing qualifiers as negative witnesses under declared semantics. A successful invariant suite does not establish population accuracy. Adopt broader variants only if independent evidence supports the predeclared practical benefit without unacceptable merge risk; retain the baseline after negative results. Sparse or unrepresentative evidence is inconclusive, not an invitation to select the representation with most matches.

## Open questions and evidence limits

Which qualifiers are stable identity distinctions, which alias claims are independent, and which language assumptions transfer to new sources? These remain project questions. Unicode sources support text semantics, not this card's ER performance. The menu, counterexamples and experiment are Atlas synthesis; no local ER result validates the configuration.

## Sources

[32] https://www.unicode.org/reports/tr15 — Unicode Normalization Forms (UAX 15)
[33] https://www.unicode.org/reports/tr24 — Unicode Script Extension Properties (UAX 24)
