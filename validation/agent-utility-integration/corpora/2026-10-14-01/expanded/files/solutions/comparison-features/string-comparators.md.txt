---
id: SOL-06-002
type: solution
title: Choose character, token and phonetic string comparisons
domain: "06"
summary: >-
  Compare name strings with mechanisms matched to observed error patterns: exact
  agreement, edit costs, Jaro-style character alignment, token overlap, frequency
  weighting or phonetic codes. Requires declared representations and explicit
  missing-value behavior. More tolerant comparators can recover variations but
  also inflate similarity between distinct names, discard order or confuse shared
  prefixes. Treat similarity as evidence rather than match probability, preserve
  dependency lineage, and test changes on fixed candidates before changing
  retrieval or decision thresholds.
tags: [person, organization, noisy, pairwise, evidence-engineering, frequency-aware, interpretable]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-06-001]
  complements: [SOL-04-001, SOL-06-001, HYP-06-001]
  evaluated_by: [EVAL-11-002, EVAL-11-006]
---

# Choose character, token and phonetic string comparisons

## Summary and problem addressed

Exact equality misses typographic and formatting variations. A tolerant comparator exposes *how* strings agree rather than deciding identity. Choose it together with a [representation contract](../normalization/name-representations.md): the same algorithm on raw, tokenized or transliterated text answers different questions. A value in a unit interval is not automatically a calibrated match probability.

## Core mechanisms, theoretical explanation and variants

### Exact and edit-based baselines

Start with raw equality and equality after an explicitly declared conservative transform. Keep missing or invalid comparison separate from measured zero similarity. Unit-cost Levenshtein distance counts the least number of insertions, deletions and substitutions to transform one string into the other. With lengths $m,n$, its standard dynamic program has $O(mn)$ time; a row-wise implementation avoids retaining the whole alignment matrix when only distance is needed. A normalized score must specify its denominator and empty-string behavior rather than assume all implementations agree.

Adaptive edit costs can represent frequent transcription confusions differently from rare substitutions. Yancey derives variable edit-step costs from training data and compares them on Census first/last-name data against fixed-cost and Jaro–Winkler comparators.[30] Costs learned from one error process need not transfer to another language or source. Do not call an arbitrary weighted edit score a metric without verifying its symmetry and triangle properties.

### Jaro-style alignment and adjustments

Jaro-style comparison aligns agreeing characters within a bounded positional window and penalizes order differences. A prefix-adjusted variant raises similarity for an agreeing initial segment; particular Census variants additionally adjust similar characters and long strings.[31] Library names do not uniquely specify these details: pin the matching window, transposition convention and enabled adjustments.

**Atlas synthesis:** prefix emphasis is plausible when initial letters are reliable and suffixes are noisy. It can instead favor distinct organizational names with a shared boilerplate prefix. Double names, inversions and long common strings warrant direct counterexamples. Yancey's 2005 report compares variants using Census name files and also examines downstream Bigmatch linkage; differences depend on data and the linkage comparison is not a universal superiority result.[31] Comparator-level classification and final accepted links are different evaluation targets.

### Token and frequency-aware comparison

**Mathematical definitions and Atlas synthesis:** for nonempty token-set union, Jaccard similarity is

$$
J(A,B)=\frac{|A\cap B|}{|A\cup B|}.
$$

Define the empty-union case explicitly. Set overlap is insensitive to token order and repeated occurrences; that helps reorderings but can remove sequence or multiplicity needed for discrimination. Token multisets, component alignment or an ordered comparator are alternatives. An acronym may have no token overlap with its expanded name even if an externally verified alias exists.

Frequency-weighted token vectors can emphasize rarer shared terms; cosine similarity compares vector direction after a declared weighting/normalization. The frequency population and version matter: retrieval-selected records and a full source can have different frequencies. Common tokens are not necessarily disposable, and rare OCR errors are not automatically authoritative. Winkler discusses frequency-based name weights and adjustments for joint dependencies; that supports contextual weighting, not a universal TF-IDF recipe or independence of all derived features.[29] The [frequency hypothesis](../../research/hypotheses/frequency-aware-evidence.md) owns the untested improvement question.

### Phonetic encoding

Soundex maps a surname to an initial letter plus a short digit sequence using grouped consonants, suppression and padding rules. NARA documents the specific historical surname-indexing rules, including prefix and letter-separation cases.[34] Code equality is a coarse feature or blocking key, not identity. Its compression causes collisions and the preserved first letter makes some initial-letter errors unrecoverable. Applicability to arbitrary languages, scripts or company names is not established by that historical guide; do not call it a universal pronunciation model. Other phonetic systems require their own verified specification before detailed adoption.

## Assumptions, applicability and advantages

Require known text units (code points, graphemes, tokens or parsed components), compatible representations, quality masks and versioned comparator parameters. A code-point edit on decomposed accents can count differently from an edit on canonically normalized text. Decide that behavior before training or calibrating downstream weights.

Use character edits for local corruption, token views for reorderings, and phonetic codes only for a supported sound/spelling regime. Multi-valued aliases need an aggregation rule: retain winning values, collection sizes and conflicting observations, not just a maximum. No feature family is universally preferred. Exact flags are cheap; edit alignments and alias Cartesian products cost more. Token indexes and phonetic keys can also generate candidates, but candidate generation does not supply a comparison result for excluded pairs.

## Trade-offs, failure modes and relationships

A high similarity can connect a subsidiary to its parent, a numbered legal vehicle to another series, or two common person names. Several comparators computed from the same spelling are correlated; adding their scores does not create independent corroboration. Learned edit costs or frequency statistics can leak holdout information if estimated on future or evaluation labels. Changes to representation or retrieval can invalidate previously learned feature weights and thresholds.

The [evidence-state solution](evidence-states.md) records unavailable comparisons and qualified contradictions separately. The scorer owns aggregation and probability semantics; [threshold policy](../decision-resolution/thresholds-abstention.md) owns action. Broad string similarity must not override a required, unresolved admissibility guard by accident.

## How to evaluate and interpret findings

Use a fixed-candidate [controlled comparison](../experimentation/controlled-comparison.md): keep representation, labels, scorer capacity and policy controls explicit; replace one comparator family, then assess integrated effects separately. Test disagreement slices (edit versus token, prefix-heavy names, reordered/double names, aliases, scripts and source pairs) rather than only average similarity. Compare against exact and normalized equality, then a simple fixed-cost edit baseline. [Pairwise evaluation](../../evaluation/pairwise-calibration.md) measures discrimination and calibration using independent evidence; missing reference labels remain unknown. Measure cost and final entities when score changes alter graph membership.

Predeclare practical gains and harm margins. Better comparator discrimination with unchanged final decisions may not justify maintenance cost; a gain on an unrepresentative name set is inconclusive for transfer. [Synthetic/metamorphic tests](../../evaluation/synthetic-metamorphic.md) exercise empty inputs, transpositions, repeated tokens and identity-changing qualifiers under declared semantics, but do not certify accuracy.

## Research opportunities and evidence limits

Can source-specific edit costs outperform global costs on independently held-out sources? Does token weighting add discrimination after controlling for candidate selection? The Census sources support their particular mechanisms and experiments, not universal multilingual or organization matching gains.[29][30][31] Token/metric definitions and the selection menu are Atlas synthesis; no Atlas ER experiment ran.

## Sources

[29] https://www.stat.cmu.edu/NCRN/PUBLIC/RLClassFiles/HW/Winkler1990.pdf — String Comparator Metrics and Enhanced Decision Rules in the Fellegi-Sunter Model of Record Linkage
[30] https://www.census.gov/content/dam/Census/library/working-papers/2004/adrm/rrs2004-02.pdf — An Adaptive String Comparator for Record Linkage
[31] https://www.census.gov/content/dam/Census/library/working-papers/2005/adrm/rrs2005-05.pdf — Evaluating String Comparator Performance for Record Linkage
[34] https://www.archives.gov/research/census/soundex.html — NARA Soundex Coding Guide
