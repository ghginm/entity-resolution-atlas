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
  evaluated_by: [EVAL-11-003, EVAL-11-004]
  complements: [EVAL-11-002]
---

# Independent entity-centric reference construction

## Short summary

Construct an auditable reference artifact, not a new matcher. Entity-centric labeling seeks fully resolved sampled entities; Binette and colleagues connect that design to performance estimation.[4] This card proposes stricter independence and completeness checks, not a claim that their labeling procedure excludes prediction-assisted search.

## Problem addressed

Candidate-only review cannot discover identities absent from its review frame. More reviewed production pairs therefore need not improve reference coverage. Training truth can favor informative difficult cases; calibration truth must support its claimed deployment population; evaluation truth must remain untouched by method and threshold selection. These responsibilities need separate samples or documented, leakage-safe partitions, not one reusable pool called gold.

## Core mechanism

1. Declare identity semantics, record universe, source namespaces, time boundary and admissible evidence. Freeze the reference version and intended sampling estimand.
2. Draw probability-sampled seed records, or entities from an independently maintained frame. Preserve draw probabilities, strata, repeated seeds and review nonresponse. Do not select only production clusters.
3. Search for each seed's complete entity membership throughout that universe using independently configured name variants, identifiers, source searches and temporal/contextual evidence. Follow newly supported members into additional searches; inspect similar nonmembers and conflicting observations. Production suggestions may be an optional aid, never the search boundary or label authority.
4. Adjudicate membership through written evidence rules. Store record IDs, evidence provenance, search queries, reviewer decisions, timestamps and unresolved possibilities. Independently re-review a probability subsample and escalate disagreements. Unsupported predictions remain unknown.
5. Publish supported memberships with a completeness status and search boundary. Only a genuinely complete entity supports treating every outside record as a nonmember. Otherwise retain supported positives and separately supported negatives without closing unknown gaps.

## Theoretical explanation

Uniform record sampling selects larger entities more often; the source describes probability-proportional-to-size entity draws.[4] With one uniformly drawn record from $N$ records, entity $e$ of size $m_e$ has draw probability $m_e/N$. Under $k$ independent draws with replacement, its probability of appearing at least once is $1-(1-m_e/N)^k$. These mathematical consequences distinguish per-draw weights from unique-entity inclusion weights: deduplication changes the estimator. Stratified or unequal record sampling needs its actual induced entity probabilities, not these formulas. Averaging sampled entities without inverse-probability weights therefore overrepresents long histories, while pair-weighted objectives emphasize them differently again.

## Important variants

- **External identifiers:** inexpensive reference linkage when namespace, validity, reuse and coverage are independently verified. Identifier-less entities may be excluded systematically; equality alone is not universal truth.
- **Reviewed entities:** recover memberships and support entity-level diagnostics, but exhaustive search is costly and ambiguity persists.
- **Stratified outside-candidate pairs:** estimate missed-link totals with known nonzero inclusion probabilities and a broad residual stratum. Enrichment can reduce rare-positive search cost; pair labels alone do not establish complete entities. See the [blind-spot audit](../../evaluation/retrieval-blind-spots.md).

Choose by required output and accessible evidence, not assumed superiority.

## Assumptions and prerequisites

Prerequisites are authorized access to the declared universe, explicit identity rules, reviewer expertise and reproducible sampling/search records. Hold out whole entities across training, calibration and evaluation. Add source and temporal holdouts when transfer is the target. Audit graph-context leakage: held-out labels, future edges, learned neighborhoods or shared entities can enter training indirectly. State whether unlabeled cross-split context is permitted; recompute restricted features when deployment would lack it.

## Applicability conditions

Use when retrieval completeness or final entity quality matters and candidate-biased labels cannot answer the question. For inaccessible sources, limit claims to the accessible universe rather than silently extrapolating.

## Advantages

One supported entity can expose multiple missed links and membership errors. Versioned evidence makes disputes and later corrections traceable without treating model outputs as reference identities.

## Trade-offs and failure modes

Search and review costs grow with entity size, aliases and cross-source histories. Common names, correlated reviewer errors, copied identifiers and scarce evidence can create false completeness. Track marginal new-member discovery and query coverage: saturation is an audit signal, not proof of exhaustive search. Unknown selection probabilities prevent defensible population reweighting; no weighting repairs unseen zero-probability strata.

## Relationships with other methods

Compatibility: supply independent labels to [pair calibration](../../evaluation/pairwise-calibration.md) and complete memberships to [entity evaluation](../../evaluation/entity-resolution-quality.md), with their different sampling contracts. Interaction risk: using the evaluated generator as the only search tool makes its failures invisible. Conditional exclusion: incomplete memberships cannot be passed as a complete partition; training predictions cannot substitute for adjudication.

## How to evaluate

Compare identifier-based, entity-review and pair-review designs at matched review budgets. Measure second-search member additions, adjudication reversals, unresolved rates, source/time coverage and cost per supported entity or missed positive, not just candidate recall. Predeclare tolerated reference error and completeness risk. Material new members in independent re-search or systematic reviewer reversals falsify readiness; weak evidence remains inconclusive. Carry reference uncertainty into downstream estimates.

## Research opportunities

Test whether diversified search or blinded review reduces omission and anchoring errors under the same budget.

## References and evidence limitations

Source [4] supports entity sampling and estimation, with inventor-disambiguation and simulation applications; its section 3.2 permits prediction-assisted labeling.[4] Independence safeguards here are Atlas protocol recommendations, not demonstrated universal improvements. No reference dataset or measured outcome is produced here.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
