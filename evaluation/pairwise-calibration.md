---
id: EVAL-11-002
type: evaluation
title: Pairwise discrimination and probability calibration
domain: "11"
summary: >-
  Evaluate pairwise ranking, threshold decisions, and the reliability of claimed
  match probabilities as separate properties. The protocol requires held-out
  labels, a declared candidate-conditioned or population estimand, and sampling
  weights where review selection changes prevalence. Precision–recall curves,
  proper probability scores, reliability diagrams, and cost diagnostics support
  comparison without treating arbitrary evidence scores as probabilities.
  Entity dependence, selective labels, changing retrieval, and downstream
  constraints limit interpretation; final entity quality needs its own evaluation.
tags: [evaluation, pairwise, calibration, uncertainty, asymmetric-costs, entity-agnostic]
maturity: established
evidence: supported-by-external-literature
relations:
  tests: [SOL-07-001, SOL-07-002, SOL-07-003, SOL-08-001]
  complements: [EVAL-11-003]
---

# Pairwise discrimination and probability calibration

## Scope and estimand

Distinguish three questions: does a score rank true matches above nonmatches, does a chosen decision policy meet operational requirements, and do claimed probabilities reflect observed match rates? An additive score or likelihood ratio is not automatically a probability; posterior interpretation additionally needs a compatible prior and distributional assumptions.[1] Compare [additive matching](../solutions/matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), and [logistic regression](../solutions/matching-scoring/logistic-regression.md) without forcing their raw outputs onto one probability scale.

Declare whether p_i estimates P(match | evidence, pair selected as candidate) or a probability over the full eligible pairspace. Retrieval changes prevalence and evidence distributions, so candidate-conditioned calibration need not transfer to excluded pairs. Also declare whether metrics describe reviewed pairs, all candidates, or the eligible population. Unknown labels remain unknown, never default nonmatches.

## Discrimination and decisions

For threshold t, use adjudicated y_i in {0,1}, sampling weights w_i, and decision d_i = 1(score_i ≥ t). Compute TP = sum w_i y_i d_i, FP = sum w_i(1−y_i)d_i, and FN = sum w_i y_i(1−d_i). Precision is TP/(TP+FP), recall TP/(TP+FN), and F1 their harmonic mean. Mark empty denominators undefined. These are weighted ratio estimates for a specified target population, not automatic corrections for unknown selection mechanisms.

Plot precision–recall curves and record the integration convention. Here average precision (AP) means sum over threshold groups of (R_k−R_previous)P_k, ordered by decreasing score, with tied scores evaluated together. Trapezoidal PR-AUC is a different summary; do not compare values without naming the convention and weighting. Prevalence affects precision, so compare methods on the same evaluation population.

Report conditional recall among candidate true pairs separately from accepted-pair end-to-end recall over independently established true pairs, using [candidate recall](candidate-recall.md). Inspect precision at a predefined recall target, recall at a precision floor, threshold sensitivity, and review volume. For [thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md), disclose coverage and unresolved labels rather than improving accuracy by silently dropping abstentions.

## Probability diagnostics

For genuine match probabilities p_i, binary calibration means E[y | p] = p within the target population. Guo and colleagues describe calibration and post-processing in image/document classification, not ER; their findings do not establish a preferred linkage calibrator.[3] The following weighted definitions adapt that diagnostic principle:

- Brier score = sum w_i(p_i−y_i)^2 / sum w_i.
- Log loss = −sum w_i[y_i log p_i + (1−y_i)log(1−p_i)] / sum w_i. State any numerical clipping convention; do not hide confidently wrong predictions.
- For prespecified bins b, report weighted mean probability p_bar_b and positive fraction y_bar_b, with counts and uncertainty. Weighted ECE = sum_b (W_b/W)|p_bar_b−y_bar_b|, where W_b sums bin weights.

Brier and log loss reflect both calibration and the informativeness of the probability predictions; neither alone isolates calibration. Here statistical probability resolution is distinct from entity-membership resolution. ECE depends on binning and can conceal local errors, especially in sparse high-confidence tails. Include reliability diagrams, alternative bin boundaries, source-pair segments, and near-threshold diagnostics. A strictly increasing recalibration can preserve ranking yet alter threshold outcomes; a non-strict map may introduce ties.

## Data design, comparisons, and uncertainty

Keep final labels outside fitting, calibration and threshold selection. For new-identity transfer separate whole entities; for existing-identity continuation use forward-time evaluation with only admissible historical state, never future-label feedback. Follow the [split contract](../solutions/experimentation/controlled-comparison.md#applicability-conditions). Ambiguous-only or balanced review distorts operational prevalence; inclusion weights need known positive probabilities and cannot repair zero support. Independent negatives and missed matches matter more than label volume.

Freeze candidates, features, splits, and downstream policy for a scorer comparison. Compare uncalibrated outputs with separately fitted calibration variants; isotonic and sigmoid methods are supporting methods unexpanded in this pilot. Choose practical improvement thresholds and precision/cost guardrails before testing. Expected policy cost can be estimated as weighted false-merge cost plus missed-match cost plus review cost, with cost assumptions stated rather than treated as objective facts.

Choose uncertainty for the actual claim. Under finite-population probability sampling, use the sampling design with fixed pair outcomes; sharing a record does not invalidate a genuine simple random pair design. For future-population inference, pairs sharing endpoints are dependent: use justified paired entity/cluster or multiway methods, preserving both endpoints of cross-entity pairs rather than an iid pair bootstrap. Small effective samples mean inconclusive intervals, not proven equivalence. Better pairwise scores can still produce worse global merges, so complement this evaluation with [entity-resolution quality](entity-resolution-quality.md).

[Incomplete-reference evaluation](incomplete-reference-quality.md) explains precision bounds when unknowns remain inside the accepted output, and why a positive-only list cannot certify precision/calibration. A model evaluated against its own rule-derived labels measures imitation, even if rows are held out; use independently adjudicated outcomes for the [weak-supervision comparison](../solutions/ground-truth/weak-supervision.md). Abstention should report selective error together with coverage/review burden on the declared population. No Atlas calibration experiment has been performed.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[3] https://proceedings.mlr.press/v70/guo17a.html — On Calibration of Modern Neural Networks
