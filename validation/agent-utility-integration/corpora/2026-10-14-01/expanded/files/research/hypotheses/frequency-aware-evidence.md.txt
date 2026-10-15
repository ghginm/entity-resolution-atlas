---
id: HYP-06-001
type: hypothesis
title: Frequency-aware agreement evidence under population shift
domain: "06"
summary: >-
  Test whether population-aware agreement evidence improves held-out matching
  recall at a fixed precision requirement compared with the same scorer using
  frequency-blind comparisons. The mechanism is established likelihood-ratio
  reasoning, not a novelty claim or observed Atlas result. A valid experiment
  needs independently labeled entities, leakage-safe frequency estimation,
  unchanged candidates and policies, and predeclared practical effect and cost
  limits. Rare errors, copied values, sparse estimates, and population shifts
  may erase gains or increase false merges.
tags: [experimentation, frequency-aware, evidence-engineering, pairwise, uncertainty, high-precision, entity-agnostic]
maturity: experimental
evidence: theoretically-motivated
relations:
  tests: [SOL-07-002, SOL-07-003]
  evaluated_by: [EVAL-11-002, EVAL-11-003]
  complements: [SOL-06-001, HYP-07-001]
---

# Frequency-aware agreement evidence under population shift

## Question and explicitly untested hypothesis

Does replacing a frequency-blind agreement feature with a smoothed, population-aware evidence feature improve useful discrimination without increasing harmful merges? **This hypothesis is untested in the Atlas.** It predicts a practically meaningful increase in candidate-conditioned recall at a project-specific precision floor, on independently labeled held-out entities, relative to an otherwise identical baseline. It does not predict improvement for every field, population, or architecture and has no universal research priority.

## Mechanism and scope

[Fellegi–Sunter](../../solutions/matching-scoring/fellegi-sunter.md) ranks comparison patterns by the match/nonmatch likelihood ratio.[1] For observing agreement on value v, define m_v = P(agreement on v | match) and u_v = P(agreement on v | nonmatch). Its evidence contribution is log(m_v/u_v), or part of a joint comparison-pattern ratio if fields are dependent. Rarity is informative when it reduces accidental agreement u_v more than it reduces m_v; rarity alone is not proof of identity.

As illustrative mathematical reasoning, independent nonmatch draws from source distributions q_A and q_B give u_v = q_A(v)q_B(v). Shared households, copied records, eligibility restrictions, and blocking can violate that independence. Conditional on a particular left-side value, the appropriate accidental-agreement term differs from the joint event above. Estimate the quantity matching the model's conditioning, not a generic inverse-frequency weight.

The underlying principle is established, not an invention of this card. The proposed research concerns operational frequency estimates, smoothing, conditioning, and transfer. Counts from an entire heterogeneous corpus may be inappropriate for a particular source pair, namespace, language, or time period. Extremely rare transcription errors can be unique without being reliable. Normalization can also collapse formerly rare variants into common values.

## Baseline, intervention, and controlled variables

Choose one scorer family before testing: a frequency-blind [logistic model](../../solutions/matching-scoring/logistic-regression.md) with fixed comparison states, or an FS baseline with global agreement parameters. The intervention adds smoothed frequency-conditioned evidence for prespecified fields; do not simultaneously change model family or candidate generation. Keep normalization, eligible pairs, candidates, training labels, tuning budget, missingness encoding, resolution policy, and cost assumptions identical. Hold contextual reliability features fixed to avoid attributing their effect to frequency.

Ablate individual fields, pooled versus source-conditioned counts, and smoothing strength using development data only. Preserve [evidence states](../../solutions/comparison-features/evidence-states.md): missing or invalid values are not rare agreements. Avoid counting transformed aliases repeatedly as independent evidence. Estimate frequencies from a documented reference population; record observation multiplicity and sensitivity to entities with many records.

## Required data and proposed test

Separate entity-disjoint training, calibration/threshold-selection, and untouched evaluation cohorts. Include a later temporal holdout and source/population-shift segments if transfer is the intended use. Obtain independently adjudicated candidate positives and negatives plus complete reference entities for final-output checks; incomplete labels cannot identify all nonmatches.

Fit frequency tables on training/reference records available before the test horizon, never on evaluation identities or labels. An online frequency update is a separate, prespecified deployment regime using only observations available at each decision time. Cross-fit training features when their own observations would leak into estimates. Use smoothing and minimum-support fallback rules fixed during development; frequency-table uncertainty is part of the intervention, not hidden preprocessing.

## Metrics, guardrails, and decision rule

Primary metric: difference in held-out candidate-conditioned recall at precision floor P_min, using thresholds selected on separate calibration data. Before opening evaluation outcomes, register numerical P_min, minimum worthwhile gain δ, maximum latency/memory increase, and catastrophic-overmerge limit from application requirements. These are required protocol parameters, not universal constants. Follow [pairwise evaluation](../../evaluation/pairwise-calibration.md) for probability-weighted metrics and calibration, and [entity quality](../../evaluation/entity-resolution-quality.md) for false merges. Report AP convention, Brier/log loss for claimed probabilities, and rare/common-value segments as secondary diagnostics.

Use paired entity/cluster, design-aware intervals and a power calculation for δ. Support practical benefit only when the lower confidence bound exceeds δ and all guardrails hold. Falsify the practical benefit in the specified population if an adequately powered upper confidence bound lies below δ, or a prespecified safety guardrail fails. A wide interval spanning δ is inconclusive, not evidence of no effect. Confounders include label-selection bias, shifted prevalence, candidate conditioning, copied attributes, normalization changes, and count instability.

After a positive result, replicate on another time/source cohort and test smoothing sensitivity and entity-level harm. After a negative result, distinguish redundant baseline evidence, poor counts, unsupported conditioning, and genuinely absent benefit; report the negative result without escalating complexity automatically.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
