---
id: SOL-05-003
type: solution
title: Approximate retrieval under explicit candidate budgets
domain: "05"
summary: >-
  Compare sorted neighborhoods, shingle indexes, canopy prefilters, MinHash/LSH
  and bounded vector retrieval against exact and multi-pass blocking. Preserve
  representation, admission and truncation provenance. Requires a declared pair
  universe, cost budget and independent missed-match evidence. Approximate
  mechanisms tolerate different errors but can lose matches through keys,
  similarity mismatch, skew or caps. Measure a coverage–cost frontier rather
  than equate more candidates with more true matches; retrieved similarity is
  not identity and filter guarantees need their exact predicate assumptions.
tags: [candidate-generation, blocking, multi-pass, high-recall, large-scale, noisy, experimentation, uncertainty]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-05-001]
  alternative_to: [SOL-05-001]
  complements: [SOL-05-002, SOL-07-005]
  evaluated_by: [EVAL-11-001, EVAL-11-004, EVAL-11-005]
---

# Approximate retrieval under explicit candidate budgets

## Short summary and problem addressed

An exact key may exclude an identity after one corrupted field; a broad key may exhaust comparison budgets. Approximate retrieval changes which plausible pairs reach comparison. It does not establish same-as identity or rank every pair omitted by the generator. The [candidate decision](../../decisions/candidate-strategy.md) owns admissible scope, [exact blocking](exact-blocking.md) supplies the simple baseline, and [multi-pass union](multi-pass-blocking.md) owns composition.

## Core mechanisms, theoretical explanation and variants

### Sorted neighborhood

Construct a sorting key, sort records, and compare records inside a sliding window. Key choice aims to keep plausible variants nearby, not necessarily equal. Hernández and Stolfo describe this sequence and multi-pass keys.[39] With $n$ records and window size $w$, a comparison-sort/scan implementation has $O(n\log n+nw)$ work before expensive pair scoring; permitted source filtering can reduce comparisons. This is a qualified algorithmic bound, not total-pipeline runtime.

A misspelled leading key component can move a true partner beyond the window. Large tied-key groups can exceed it even when keys agree. Define stable tie handling and whether a window crosses partitions; arbitrary input order within ties can otherwise change candidates. Several keys can recover different misses but share correlated errors. Increasing a window expands coverage only under the same ordering, eligibility and no displacing downstream cap.

### Shingle or token inverted indexes

Represent each record as a set or multiset of tokens or fixed-length character shingles; use postings to enumerate records sharing elements, then verify the selected similarity predicate. Author-hosted MMDS chapter 3 explains shingling and set-similarity indexing/filtering.[38] Short shingles tolerate some local errors while generating frequent postings; long shingles are selective but fragile on short or heavily corrupted names. Token sets discard order and multiplicity unless these are retained explicitly.

For set Jaccard and a positive threshold, set-cardinality bounds can safely rule out impossible similarity values: the intersection cannot exceed the smaller cardinality and the union is at least the larger. Those are **token-set cardinalities**, not raw name lengths.[38] A filter proved for that predicate is not a guarantee of ER recall. Specialist edit-distance q-gram filter theorems were not verified here; do not transfer their advertised bounds to another tokenizer, edit model or masking policy. Empty sets and unavailable representations need separate handling.

### Overlapping canopies

Use a cheap distance to form overlapping neighborhoods, and reserve expensive distance work for points sharing a canopy. The primary canopy paper uses a wider inclusion radius and a tighter radius removing centers from future selection; this produces overlapping rather than strictly disjoint blocks.[35] Skipping cross-canopy comparisons saves work if the cheap distance keeps relevant partners together. That condition is not automatic: a cheap measure unrelated to identity variation can exclude the needed pairs. Center order, thresholds and high-frequency regions can affect coverage and work. The paper's reference-matching experiments are context-specific, not universal lossless retrieval.

### MinHash and locality-sensitive hashing

For a nonempty shingle set, an ideal uniform random-permutation MinHash selects its least-ranked element. Equality probability for two sets equals their Jaccard similarity; Broder supplies primary resemblance/sampling foundations and MMDS gives the MinHash/banding construction.[40][38] With independent MinHash rows, $b$ bands of $r$ rows, and exact within-band signature equality, a pair of set similarity $s$ becomes a candidate with probability

$$
1-(1-s^r)^b.
$$

This is a probability over the stated random construction, **not** population ER recall. Approximate hash families, accidental finite-bucket collisions, empty sets, correlated rows and downstream caps require separate analysis. More permissive banding can admit extra dissimilar pairs as well as recover missed similar pairs. Retain seeds/hash versions and test stability; do not call one favorable seed representative.

### Vector, hybrid and adaptive roles

**Atlas synthesis, bounded coverage:** an encoder plus nearest-neighbor index can return a limited set of neighbors; index approximation is distinct from whether vector neighbors represent identity. Compare an exact vector scan on a feasible audit subset to the approximate index to isolate index loss, then use independent identity evidence to assess representation loss. [Learned/neural comparators](../matching-scoring/learned-neural-comparators.md) owns embedding/pair-model interpretation; no particular ANN implementation is endorsed here.

Union symbolic and vector routes while retaining their reasons and budget effects. Frequency-aware keys or adaptive budgets may allocate work to ambiguous records, but can also starve sparse or unfamiliar source slices. Learned blocking requires representative training and independently observed misses, not positives only from current admission. Specialist learned-blocking algorithms and ANN index internals remain deferred pending selected primary mechanisms and a concrete consumer need; this card defines their interfaces and experiments, not invented guarantees.

## Assumptions, prerequisites and applicability

Declare the eligible pair universe, source permissions, representation/version, generator configuration, random state, deduplication and per-record/global budget. Preserve unavailable keys, skipped passes, pre-cap candidates and final admitted candidates as distinct states. A broad fallback for missing fields is optional but its absence is a measurable coverage limitation.

Use approximate routes where a diagnosed miss pattern is not served by a cheap exact pass. Clean stable identifiers can make exact blocking preferable. Skew changes both postings work and pair volume; dropping oversized blocks or truncating neighbors changes the population. Physical partitioning, distributed execution and index-maintenance engineering remain Wave 4 responsibilities, not solved by naming an algorithm here.

## Advantages, trade-offs, failure modes and relationships

As a standalone generator this family can substitute for exact blocking; as an additional route it can complement exact admission inside a multi-pass union. These mechanisms trade different invariances for selectivity: nearby sort positions, shared shingles, cheap-distance neighborhoods, random set collisions or vector proximity. None is inherently identity-preserving. Correlated passes add work without new matches; similarity can recover relatives, subsidiaries or product variants rather than identical entities. Index building, emissions, pair deduplication and representation generation cost work even if few pairs are eventually scored.

New candidates are not newly recovered true matches. Candidate coverage, scoring quality on candidates and final accepted-match/entity quality need separate denominators. New retrieval can change class priors and comparison dependence, making old calibration or thresholds inapplicable; use [selection/calibration analysis](../../deep-dives/selection-and-calibration.md), not an automatic prior correction.

## How to evaluate and research opportunities

Compare exact/multi-pass baseline with a small configuration grid, immutable inputs and independent missed-match evidence. Report unique candidates, true matches recovered outside the baseline where known, omissions after each cap/filter, skew, generation/index/scoring cost and source/script/sparsity slices. Use [candidate recall](../../evaluation/candidate-recall.md), [outside-set auditing](../../evaluation/retrieval-blind-spots.md) and [incomplete truth limits](../../evaluation/incomplete-reference-quality.md). Unreviewed pairs remain unknown.

Measure a coverage–cost frontier and equal-budget contrasts, including variation across random seeds. A fixed-candidate scorer experiment cannot estimate retrieval improvement; [controlled comparisons](../experimentation/controlled-comparison.md) separates isolated scoring from end-to-end retrieval effects. Predeclare practical coverage benefit, resource limits and harmful downstream-merge constraints. Reject a pass that adds cost without supported useful coverage; call rare omitted-match uncertainty inconclusive rather than certify recall from a candidate-selected test set.

## References and evidence limitations

Sources support specific mechanisms, not a best ER configuration. MMDS is author-maintained textbook exposition, not an original theorem paper; Broder and Hernández–Stolfo provide selected primary foundations, and canopy claims retain their distance assumptions.[35][38][39][40] No local retrieval algorithm, index, processed dataset or ER benchmark has been executed.

## Sources

[35] http://www.kamalnigam.com/papers/canopy-kdd00.pdf — Efficient Clustering of High-Dimensional Data Sets with Application to Reference Matching
[38] http://infolab.stanford.edu/~ullman/mmds/ch3.pdf — Mining of Massive Datasets: Finding Similar Items (author-hosted chapter 3)
[39] https://creatingfutureus.org/wp-content/uploads/2021/10/Hernandez-and-Stolfo-1998.pdf — Real-world Data is Dirty: Data Cleansing and The Merge/Purge Problem
[40] https://www.cs.princeton.edu/courses/archive/spring13/cos598C/broder97resemblance.pdf — On the resemblance and containment of documents
