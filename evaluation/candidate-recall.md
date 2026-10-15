---
id: EVAL-11-001
type: evaluation
title: Candidate recall and retrieval efficiency
domain: "11"
summary: >-
  Measure whether candidate generation retains independently established true
  matches while reducing eligible comparisons. This evaluation separates
  retrieval completeness from conditional scoring recall and final entity
  quality, and compares complementary passes through deduplicated marginal
  yield. It requires an explicit pairspace, independently assembled reference
  matches, and a defensible sampling design. Budget limits, incomplete labels,
  population shifts, and entity dependence can invalidate apparently strong
  results; cost and segment diagnostics therefore accompany aggregate recall.
tags: [evaluation, candidate-generation, blocking, multi-pass, high-recall, uncertainty, entity-agnostic]
maturity: established
evidence: supported-by-external-literature
relations:
  tests: [SOL-05-001, SOL-05-002]
  complements: [EVAL-11-002, EVAL-11-003]
---

# Candidate recall and retrieval efficiency

## Measurement contract

Candidate selection restricts the comparisons offered to a matcher; blocking and similarity filtering are distinct mechanisms, not interchangeable guarantees.[2] Evaluate the final candidate set after cleaning, deduplication, truncation, and routing. A generous pre-budget set does not establish recall for the set actually scored.

Define an eligible pairspace U before inspecting outcomes: unordered distinct-record pairs for deduplication, cross-file pairs for bipartite linkage, or explicitly permitted source/time combinations. With no exclusions, their sizes are n(n−1)/2 and n_A n_B, respectively. Exclusions belong to identity semantics and must not silently remove difficult matches. Let C be unique emitted candidates and T the independently known true pairs in U. All following set formulas are mathematical definitions, not measured Atlas results.

## Metrics and interpretation

- Candidate recall, also called pair completeness, is |C ∩ T| / |T|. Its denominator must contain true matches found independently of C; labeling only emitted candidates cannot estimate missed-match recall.[2]
- Reduction ratio is 1 − |C| / |U|. Report |U|, |C|, pair ordering, eligibility rules, and repeated comparison executions separately. This card counts unique pairs; the survey also considers comparison multiplicity, which changes efficiency denominators.[2]
- Candidate pair quality is |C ∩ T| / |C| only when truth covers C. With incomplete truth, this ratio is merely known-positive yield, not precision: unknown pairs are not fabricated nonmatches.
- For pass j after union C_previous, define ΔC_j = C_j minus C_previous and ΔT_j = ΔC_j ∩ T. Marginal pass efficiency is |ΔT_j| / |ΔC_j|; incremental recall is |ΔT_j| / |T|. Mark zero-denominator cases undefined. Both depend on pass order; include leave-one-pass-out comparisons.

Under fixed U and T, an unrestricted candidate union cannot lower candidate recall. It can nevertheless increase runtime and false-positive exposure, while a shared top-k cap can evict previously retained matches. These are different claims: union monotonicity is not downstream quality monotonicity.

For a matcher whose accepted pair set A is a subset of C, conditional pairwise recall is |A ∩ T| / |C ∩ T|. End-to-end accepted-pair recall equals candidate recall times conditional recall when denominators are nonzero. This identity does not apply unchanged to clustering that infers unscored pairs; assess that output with [entity-resolution quality](entity-resolution-quality.md).

## Data and sampling requirements

Construct evaluation truth independently through external references or entity-centric adjudication searching outside the proposed blocks. Complete sampled entities can expose missed links under documented completeness/sampling assumptions.[4] For new-identity transfer separate evaluation entities from training; for existing-identity continuation use later observations with only deployment-admissible historical state and no future-label feedback. Follow the [split contract](../solutions/experimentation/controlled-comparison.md#applicability-conditions), recording adjudication uncertainty and the search boundary.

For a probability sample of true pairs with inclusion probability π_i, estimate recall by the ratio of weighted totals: sum of 1(i ∈ C)/π_i divided by sum of 1/π_i over sampled true pairs. This ratio is not generally exactly unbiased. For a probability sample spanning the whole pairspace, estimate candidate-true and outside-candidate-true totals separately; both enter the recall denominator. For entity sampling, derive the pair inclusion probabilities or aggregate entity-level totals under that design; do not assign arbitrary pair weights. [Probability-sampled review](../solutions/ground-truth/probability-sampled-review.md) constructs these samples. Without a defensible denominator, report benchmark recall with limited scope rather than population recall.

## Comparisons, uncertainty, and failure analysis

Compare [exact blocking](../solutions/candidate-generation/exact-blocking.md) with [multi-pass blocking](../solutions/candidate-generation/multi-pass-blocking.md) at matched budgets and on a recall–cost frontier. Keep normalization, eligibility, records, and evaluation labels fixed. Track index construction, memory, repeated work, latency tails, and the largest blocks, not just unique comparison counts. Diagnose misses by missing fields, script, source pair, common values, and time gap.

Use paired, design-aware intervals for differences. Entity/cluster sampling requires its actual primary units, strata and weights; a real simple random pair sample permits finite-population design variance with fixed outcomes even when pairs share records. An iid pair bootstrap is not justified for shared-entity future-population inference. Large entities contribute many true pairs, so add entity-balanced summaries rather than replacing the declared pair-weighted estimand. [Incomplete-reference evaluation](incomplete-reference-quality.md) separates these uncertainty targets and handles unresolved adjudications and rare zero-discovery strata.

A candidate oracle can add independently known missed true pairs within supported evaluation truth while leaving the matcher unchanged. It diagnoses retrieval loss, not attainable production gain: added edges can alter assignment or clustering adversely. Follow with [pairwise calibration](pairwise-calibration.md) and final-output evaluation. This Atlas supplies a protocol, not benchmark results; [approximate retrieval](../solutions/candidate-generation/approximate-blocking.md) has bounded method coverage, not a universal recall guarantee.

## Sources

[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
