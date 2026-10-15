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
  augmentation. Unknown evaluation inclusion or zero review probabilities leave
  the estimand nonidentifiable, which must be reported rather than estimated away.
tags: [entity-agnostic, evaluation, candidate-generation, blocking, multi-pass, uncertainty, experimentation, human-review]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  tests: [SOL-05-001, SOL-05-002, SOL-10-001]
  complements: [EVAL-11-001, EVAL-11-003, EVAL-11-005]
---

# Retrieval blind-spot audit and missed-pair estimation

## What is measured

[EVAL-11-001](candidate-recall.md) measures recall over independently known true pairs and marginal pass yield inside a candidate workflow. This card adds the operational audit those formulas cannot supply: where the eligible pairspace loses true pairs before scoring — eligibility exclusions, top-k caps, routing, filtering — and how many missed true pairs a design-weighted sample outside the emitted candidate set reveals. The unit is an unordered pair in declared pairspace $U$; the estimand is a pair ratio (or entity analogue) for a frozen pipeline and record universe.

## Why it matters

A system can show high conditional recall on its own candidates while silently excluding most of its true matches: recall over $C\cap T$ stays near one as $C$ shrinks. Caps and aggressive blocking concentrate loss on long-tail entities, name variants and source pairs — precisely the difficult positives. Without an outside-pair design, retrieval loss is confounded with scorer performance and reference-coverage gaps, and architecture choices (multi-pass union versus capped single pass) rest on indistinguishable numbers.

## Definitions and formulas

Let $U$ be the frozen **semantically admissible** pairspace, $C\subseteq U$ the emitted candidates after production eligibility filters, deduplication, caps and routing, and $T\subseteq U$ the true pairs under independent reference semantics. A production eligibility rule is a stage inside $U$; do not redefine $U$ to hide matches excluded by that rule. Replay feasible stage variants to separate rule exclusions, caps and filtering. When a full uncapped replay is unaffordable, audit sampled records/blocks with known support and report that attribution boundary. Stage losses depend on order; matched-budget alternatives answer a different cost-effectiveness question.

Draw $S$ across disjoint within-$C$ and outside-$C$ strata with known inclusion probabilities $\pi_i>0$, and adjudicate sampled $y_i=1(i\in T)$. Estimate true-pair totals in region $B\subseteq U$ by $\widehat T_B=\sum_{i\in S\cap B}y_i/\pi_i$. These are design-unbiased with complete correct sampled outcomes.[15] Report the blind-spot ratio

$$
\widehat\rho=\frac{\widehat T_{U\setminus C}}{\widehat T_C+\widehat T_{U\setminus C}}.
$$

The missed total is $\widehat T_{U\setminus C}$; both true-pair totals enter the denominator. The ratio is generally biased in finite samples and needs adequate positive support for a useful approximation. An empty estimated denominator is undefined. Unknown labels remain unknown; unresolved sampled outcomes require a response design or sensitivity analysis, not silent exclusion.

## Data requirements

Independent reference coverage per [SOL-10-001](../solutions/ground-truth/independent-reference.md), a frozen emitted set with a reproducible candidate-membership check, and review partly outside candidates. Stage replay and eviction provenance are additional requirements for attributing loss to particular rules, not prerequisites for estimating total loss of a frozen black-box retriever.

## Sampling assumptions

Evaluation selection must have known positive inclusion on the claimed population. Score-based strata are valid when randomly sampled with known probabilities and residual support; entity sampling needs its induced probabilities. Unknown review inclusion or zero-support regions preclude this design-based total estimator. Unknown production internals can obstruct stage attribution, but independent probability review across $U$ can evaluate an observed frozen black-box $C$ without production selection probabilities.

## Interpretation

End-to-end accepted-pair recall over independently known $T$ equals candidate recall times conditional recall only for pair-output policies; clustering infers unscored pairs, so connect to [EVAL-11-003](entity-resolution-quality.md): a pair missed by retrieval can still be co-clustered correctly through closure, and cluster-induced pair recall can look sound while direct pair acceptance was capped. Candidate-graph recovery potential — whether $T$ sits inside the connected components of $C$, versus inside the accepted edges — separates what resolution could in principle recover from what retrieval ever surfaced; it presumes closure's overmerge risk, so it is an upper diagnostic, not attainable gain.

## Potential biases

Reference bias (truth assembled from the same candidate workflow), reviewer anchoring on model scores, entity-size weighting (large entities dominate HT pair totals; report entity-balanced views with distinct denominators), and saturation illusions — sampling outside $C$ until nothing new appears is a budget signal, not proof of exhaustive search.

## Known limitations

Cost grows with $|U\setminus C|$; rare positives need enrichment or outside-cluster sampling, which raises variance and depends on strata that themselves must keep $\pi_i>0$. The audit is pipeline-version-specific; any blocking, cap or routing change requires re-running it. It estimates retrieval loss for a declared population, not a universal guarantee.

## Recommended comparisons

Compare external-ID, entity-centric review[4] and [stratified pair review](../solutions/ground-truth/probability-sampled-review.md) at matched cost. Measure independently discovered missed positives, re-adjudication reversals and whether attribution changes the next action. Zero discoveries in a positive-probability stratum are possible, not proof of a defective design. Missing frame coverage, incorrect recorded probabilities or systematic review omissions invalidate the claimed estimator; a wide missed-total interval makes the audit inconclusive. Predeclare practical loss limits before using a defensible upper bound to accept retrieval risk.

## Statistical uncertainty

Use the actual pair/cluster/stratified design; joint inclusion or justified replicate structure matters, not just first-order weights.[15] Entity-sampled audits preserve primary units, strata and weights; genuine simple random pair samples permit finite-population variance with fixed outcomes. Shared-endpoint future-population inference needs additional dependence treatment. For zero discoveries, invert the actual rare-event design rather than reporting zero variance; the [estimation deep dive](../deep-dives/incomplete-reference-estimation.md) derives a finite-stratum upper-bound route. Report inconclusive bounds honestly.

## Related solutions and references

Operates on outputs of [exact blocking](../solutions/candidate-generation/exact-blocking.md) and [multi-pass union](../solutions/candidate-generation/multi-pass-blocking.md); consumes reference designs from [SOL-10-001](../solutions/ground-truth/independent-reference.md). The entity-centric framework supports fully-resolved sampled entities and estimator-side diagnostics under a defined design;[4] the blocking survey grounds candidate-space and filtering mechanisms.[2] This pilot specifies protocol only; no Atlas measurement is reported. Independent truth discovery is distinct from production oracle augmentation, which adds known missed pairs to diagnose ceilings, not attainable production gains.

## Sources

[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
