---
id: SOL-10-001
type: solution
title: Independent entity-centric reference construction
domain: "10"
summary: >-
  Build evaluation references that can expose identities missed by production
  retrieval rather than certifying only its candidates. Sample seed records or
  independently framed entities, search across a declared record universe, and
  adjudicate supported memberships with provenance and unresolved cases retained.
  Separate training, calibration and evaluation uses; audit inclusion probabilities,
  completeness and reviewer errors. External identifiers and stratified pair review
  are alternatives when their assumptions fit. Search cost, rare positives, length
  bias and hidden members limit population claims even after apparent saturation.
tags: [entity-agnostic, few-labels, human-review, provenance, source-aware, uncertainty, evaluation, governance]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-10-001]
  evaluated_by: [EVAL-11-003, EVAL-11-004, EVAL-11-005]
  complements: [EVAL-11-002]
---

# Independent entity-centric reference construction

## Short summary

Construct an auditable reference artifact, not a new matcher. Entity-centric labeling seeks fully resolved sampled entities; Binette and colleagues connect that design to performance estimation.[4] This card proposes stricter independence and completeness checks, not a claim that their labeling procedure excludes prediction-assisted search.

## Problem addressed

Candidate-only review cannot discover identities absent from its review frame. More reviewed production pairs therefore need not improve reference coverage. Training truth can favor informative difficult cases; calibration truth must support its claimed deployment population; evaluation truth must remain untouched by method and threshold selection. These responsibilities need separate samples or documented, leakage-safe partitions, not one reusable pool called gold.

## Core mechanism

1. Declare identity semantics, record universe, source namespaces, time boundary and admissible evidence. Freeze the reference version and intended sampling estimand.
2. Draw probability-sampled seed records, or entities from an independently maintained frame. Preserve draw probabilities, strata, repeated seeds and review nonresponse. Do not select only production clusters. Define whether the sampling unit is a seed occurrence or a unique entity before deduplication; an external list must itself have audited coverage and multiplicity.
3. Search for each seed's complete entity membership throughout that universe using independently configured name variants, identifiers, source searches and temporal/contextual evidence. Follow newly supported members into additional searches; inspect similar nonmembers and conflicting observations. Production suggestions may be an optional aid, never the search boundary or label authority.
4. Adjudicate membership through written evidence rules. Store record IDs, evidence provenance, search queries, reviewer decisions, timestamps and unresolved possibilities. Independently re-review a probability subsample, including apparently easy/completed entities, and escalate disagreements. The second reviewer should independently repeat membership search before seeing the first result where feasible; checking only its included records cannot detect common omissions. Store additions, removals and reversals separately. Unsupported predictions remain unknown.
5. Publish supported memberships with a completeness status and search boundary. Only a genuinely complete entity supports treating every outside record as a nonmember under the declared equivalence semantics and universe. Otherwise retain supported positives and separately supported negatives without closing unknown gaps. Failure to retrieve a record is not a nonmember judgment; neither is its absence from a partially resolved entity.

## Theoretical explanation

Uniform record sampling selects larger entities more often; the source describes probability-proportional-to-size entity draws.[4] With one uniformly drawn record from $N$ records, entity $e$ of size $m_e$ has draw probability $m_e/N$. Under $k$ independent draws with replacement, its probability of appearing at least once is $1-(1-m_e/N)^k$. These mathematical consequences distinguish per-draw weights from unique-entity inclusion weights: deduplication changes the estimator. Stratified or unequal record sampling needs its actual induced entity probabilities, not these formulas. Averaging sampled entities without inverse-probability weights therefore overrepresents long histories, while pair-weighted objectives emphasize them differently again.

More generally, for independent seed draws with fixed record probabilities $q_r$, an entity's draw probability is $q_e=\sum_{r\in e}q_r$ and its unique-entity inclusion is $1-(1-q_e)^k$. Uniform record sampling without replacement instead gives $1-\binom{N-m_e}{k}/\binom{N}{k}$, with a zero numerator when too few outside records exist. These are derived sampling identities, not alternative search algorithms. Unknown true membership makes $m_e$ or $q_e$ unknown: supported size is not silently the complete size. Keep repeat-draw contributions or derive the unique-entity estimator; do not attach record probabilities to discovered pairs. The source's with-replacement ratio-estimation framework does not make every deduplicated estimator exactly unbiased.[4]

## Important variants

- **External identifiers:** inexpensive reference linkage when namespace, validity, reuse and coverage are independently verified. Identifier-less entities may be excluded systematically; equality alone is not universal truth.
- **Reviewed entities:** recover memberships and support entity-level diagnostics, but exhaustive search is costly and ambiguity persists.
- **Stratified outside-candidate pairs:** estimate missed-link totals with known nonzero inclusion probabilities and a broad residual stratum. Enrichment can reduce rare-positive search cost; pair labels alone do not establish complete entities. See the [blind-spot audit](../../evaluation/retrieval-blind-spots.md).

The [acquisition decision](../../decisions/ground-truth-acquisition.md) compares these purposes; [probability-sampled review](probability-sampled-review.md) owns the separate evaluation/learning-pool design. Entity search here is a complementary route when pair review cannot establish membership completeness, not a duplicated active-selection mechanism.

Choose by required output and accessible evidence, not assumed superiority.

## Assumptions and prerequisites

Prerequisites are authorized access, identity rules, reviewer expertise and reproducible sampling/search records. For new-identity transfer, hold out whole entities across training, calibration and evaluation. For existing-identity continuation, use forward-time evaluation with only the historical state and as-of evidence promised by deployment; prohibit future-label feedback. Add source holdouts for source transfer. Audit uncertain identity overlap, future edges, learned neighborhoods and shared graph context. Follow the [split contract](../experimentation/controlled-comparison.md#applicability-conditions); recompute restricted features when deployment would lack them.

## Applicability conditions

Use when retrieval completeness or final entity quality matters and candidate-biased labels cannot answer the question. For inaccessible sources, limit claims to the accessible universe rather than silently extrapolating.

## Advantages

One supported entity can expose multiple missed links and membership errors. Versioned evidence makes disputes and later corrections traceable without treating model outputs as reference identities.

## Trade-offs and failure modes

Search and review costs grow with entity size, aliases and cross-source histories. Common names, correlated reviewer errors, copied identifiers and scarce evidence can create false completeness. Track marginal new-member discovery and query coverage: saturation is an audit signal, not proof of exhaustive search. Unknown selection probabilities prevent defensible population reweighting; no weighting repairs unseen zero-probability strata. Retain failed searches and unresolved entities as nonresponse, not replacement seeds or presumed singletons. A probability-sampled seed can still have an unknown chance of successful resolution; response-weight adjustments require additional assumptions about resolved versus unresolved units, not just known seed weights.[15] Large, costly entities may be disproportionately abandoned.

## Relationships with other methods

Compatibility: supply independent labels to [pair calibration](../../evaluation/pairwise-calibration.md) and complete memberships to [entity evaluation](../../evaluation/entity-resolution-quality.md), with their different sampling contracts. Interaction risk: using the evaluated generator as the only search tool makes its failures invisible. Conditional exclusion: incomplete memberships cannot be passed as a complete partition; training predictions cannot substitute for adjudication.

## How to evaluate

Compare identifier-based, entity-review and pair-review designs at matched total review costs, counting search, repeat annotation and escalation as well as supported labels. Measure second-search member additions, adjudication reversals, unresolved rates, source/time coverage and cost per supported entity or missed positive, not just candidate recall. Preserve sampling weights when estimating re-review error; targeted disputes alone do not estimate its prevalence. Predeclare tolerated reference error and completeness risk. Adopt when these checks and decision precision meet the declared requirements; material additions or systematic reversals beyond those tolerances reject readiness, while weak evidence remains inconclusive. Carry reference uncertainty into [incomplete-reference evaluation](../../evaluation/incomplete-reference-quality.md). Sampling variance must follow the actual seed/entity design; additional reviewer-error or population-transfer uncertainty is distinct and cannot be repaired by an automatic repeated-pair bootstrap.

## Research opportunities

Test whether diversified search or blinded review reduces omission and anchoring errors under the same budget.

## References and evidence limitations

Binette and colleagues, arXiv v1, sections 3.2–3.4, support entity sampling and estimation, with inventor-disambiguation and simulation applications; section 3.2 permits prediction-assisted labeling.[4] Statistics Canada's manual, section 7.1.3, makes the assumptions behind nonresponse adjustment explicit.[15] Independence safeguards here are Atlas protocol recommendations, not demonstrated universal improvements. No reference dataset or measured outcome is produced here.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
