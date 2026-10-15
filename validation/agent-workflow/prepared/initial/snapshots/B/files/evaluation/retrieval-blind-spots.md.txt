---
id: EVAL-11-004
type: evaluation
title: Retrieval blind-spot audit and missed-pair estimation
domain: "11"
summary: >-
  Estimate how many true matches candidate retrieval misses, rather than only
  measuring recall over already-emitted candidates. The protocol attributes loss
  to eligibility rules, caps and routing, samples pairs from outside the candidate
  set with known nonzero inclusion probabilities, and reports a design-weighted
  missed-true-pair ratio with entity-cluster-aware uncertainty. It relates
  end-to-end accepted-pair recall to partition-induced pair measures, candidate
  graph recovery potential, and independent truth discovery versus oracle
  augmentation. Unknown selection mechanisms or zero inclusion probabilities leave
  the estimand nonidentifiable, which must be reported rather than estimated away.
tags: [entity-agnostic, evaluation, candidate-generation, blocking, multi-pass, uncertainty, experimentation, human-review]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  tests: [SOL-05-001, SOL-05-002, SOL-10-001]
  complements: [EVAL-11-001, EVAL-11-003]
---

# Retrieval blind-spot audit and missed-pair estimation

## What is measured

[EVAL-11-001](candidate-recall.md) measures recall over independently known true pairs and marginal pass yield inside a candidate workflow. This card adds the operational audit those formulas cannot supply: where the eligible pairspace loses true pairs before scoring — eligibility exclusions, top-k caps, routing, filtering — and how many missed true pairs a design-weighted sample outside the emitted candidate set reveals. The unit is an unordered pair in declared pairspace $U$; the estimand is a pair ratio (or entity analogue) for a frozen pipeline and record universe.

## Why it matters

A system can show high conditional recall on its own candidates while silently excluding most of its true matches: recall over $C\cap T$ stays near one as $C$ shrinks. Caps and aggressive blocking concentrate loss on long-tail entities, name variants and source pairs — precisely the difficult positives. Without an outside-pair design, retrieval loss is confounded with scorer performance and reference-coverage gaps, and architecture choices (multi-pass union versus capped single pass) rest on indistinguishable numbers.

## Definitions and formulas

Let $U$ be the frozen eligible pairspace, $C\subseteq U$ the emitted candidates after deduplication, caps and routing, and $T\subseteq U$ the true pairs under independent reference semantics. Decompose loss before sampling: replay a cap-free, filter-free emission on the same inputs to attribute excluded true pairs to (i) eligibility rules, (ii) cap eviction, (iii) filtering; report each stage's marginal loss at matched budget.

Draw $S$ from $U\setminus C$ (plus the within-$C$ review stratum) with known first-order inclusion probabilities $\pi_i>0$; adjudicate sampled pairs against the reference rules. With Horvitz–Thompson totals $\hat{T}(A)=\sum_{i\in S\cap A}\pi_i^{-1}$, report the blind-spot ratio

$$\widehat{\rho}=\frac{\hat{T}(T\cap S\cap(U\setminus C))}{\hat{T}(T\cap S)} ,$$

estimating the share of true pairs missing from candidates under the design, with implied missed total $\hat{T}(T\cap(U\setminus C))$. $\hat\rho$ is a ratio estimator: approximately, not exactly, unbiased under the stated design; it requires $\pi_i$ nonzero in every stratum where loss is claimed. Unknown labels outside $S$ remain unknown, never nonmatches.

## Data requirements

Independent reference coverage per [SOL-10-001](../solutions/ground-truth/independent-reference.md) (external IDs, reviewed entities, or stratified pair review), a frozen pipeline replayable stage by stage, provenance of which rule evicted which pair, and a review budget spent partly outside candidates.

## Sampling assumptions

Review selection must be design-based, not score-based alone: enrichment on ambiguous scores is legitimate only when every stratum keeps a nonzero base inclusion probability for missed true pairs. Entity sampling induces pair probabilities through the entity design — derive them; do not invent pair weights. If the production selection mechanism is unknown, or any stratum has $\pi_i=0$, $\rho$ is not identified there: report the unidentifiable region instead of estimating it.

## Interpretation

End-to-end accepted-pair recall over independently known $T$ equals candidate recall times conditional recall only for pair-output policies; clustering infers unscored pairs, so connect to [EVAL-11-003](entity-resolution-quality.md): a pair missed by retrieval can still be co-clustered correctly through closure, and cluster-induced pair recall can look sound while direct pair acceptance was capped. Candidate-graph recovery potential — whether $T$ sits inside the connected components of $C$, versus inside the accepted edges — separates what resolution could in principle recover from what retrieval ever surfaced; it presumes closure's overmerge risk, so it is an upper diagnostic, not attainable gain.

## Potential biases

Reference bias (truth assembled from the same candidate workflow), reviewer anchoring on model scores, entity-size weighting (large entities dominate HT pair totals; report entity-balanced views with distinct denominators), and saturation illusions — sampling outside $C$ until nothing new appears is a budget signal, not proof of exhaustive search.

## Known limitations

Cost grows with $|U\setminus C|$; rare positives need enrichment or outside-cluster sampling, which raises variance and depends on strata that themselves must keep $\pi_i>0$. The audit is pipeline-version-specific; any blocking, cap or routing change requires re-running it. It estimates retrieval loss for a declared population, not a universal guarantee.

## Recommended comparisons

Compare audit designs at matched review budget: external-ID-only, entity-centric full-resolution review,[4] and stratified outside-candidate pair sampling. Against a no-audit (candidate-only) baseline compare: missed-true-pair totals found, re-adjudication stability, and whether loss attribution changes a decision (adding a pass versus raising a cap). Falsification: if reviewed entities repeatedly expose missed true pairs in strata the audit assigned $\pi_i>0$ yet sampled none, the design is defective; if outside-$C$ sampling at a declared budget yields no design-weighted misses with tight intervals, retrieval loss is bounded — a result, not a proof.

## Statistical uncertainty

Use design-aware variance: stratified HT variance formulas or resampling that redraws whole entities/cluster sampling units, preserving strata and weights; pairs sharing records or entities are dependent; a naive pair bootstrap understates uncertainty. Small rare-positive samples yield wide intervals — report them; inconclusive is a finding.

## Related solutions and references

Operates on outputs of [exact blocking](../solutions/candidate-generation/exact-blocking.md) and [multi-pass union](../solutions/candidate-generation/multi-pass-blocking.md); consumes reference designs from [SOL-10-001](../solutions/ground-truth/independent-reference.md). The entity-centric framework supports fully-resolved sampled entities and estimator-side diagnostics under a defined design;[4] the blocking survey grounds candidate-space and filtering mechanisms.[2] This pilot specifies protocol only; no Atlas measurement is reported. Independent truth discovery is distinct from production oracle augmentation, which adds known missed pairs to diagnose ceilings, not attainable production gains.

## Sources

[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
