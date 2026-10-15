---
id: SOL-07-003
type: solution
title: Logistic regression for pairwise matching
domain: "07"
summary: >-
  Learn an interpretable conditional log-odds function from labeled comparison
  evidence and map it through the logistic link. Predictor independence is not
  required, but correlated features can destabilize individual coefficients and
  a restricted feature basis can miss interactions. Representative labels,
  candidate-population alignment, leakage-safe assessment, and calibration checks
  are central prerequisites. Regularization, constrained fitting, and richer
  additive functions are optional variants, not an inevitable progression
  beyond simpler expert or likelihood-ratio scoring.
tags: [entity-agnostic, few-labels, rich-labels, interpretable, pairwise, calibration, source-aware, evaluation]
maturity: established
evidence: supported-by-external-literature
relations:
  addresses: [DEC-07-001]
  evaluated_by: [EVAL-11-002]
  complements: [SOL-07-005]
  used_by: [AR-03]
---

# Logistic regression for pairwise matching

## Short summary

Estimate match probability conditionally on an explicit comparison feature basis. Logistic regression learns the weights jointly from labels instead of assigning points or separately estimating each feature's match and non-match distributions.[7]

## Problem addressed

Manual evidence weights may be poorly aligned with observed errors, and independent-field likelihood ratios may misrepresent overlapping signals. A discriminative model can estimate a conditional decision surface directly, provided labeled pairs describe the intended task and candidate population.

## Core mechanism

Let $y_i=1$ identify an adjudicated match and $x_i$ contain comparison states, similarities, and justified context features. Model

$$
p_\beta(x)=\sigma(\eta(x)),\qquad
\eta(x)=\beta_0+\sum_j\beta_jx_j,\qquad
\sigma(z)=\frac{1}{1+e^{-z}}.
$$

Fit coefficients using the conditional Bernoulli likelihood, equivalently minimizing

$$
-\sum_i\{y_i\log p_\beta(x_i)+(1-y_i)\log[1-p_\beta(x_i)]\}
+\lambda\Omega(\beta).
$$

The likelihood and logit formulation are standard; the optional penalty is a regularized variant.[7] Reference coding for categorical states and documented scaling for continuous features are part of the model contract. Missingness should be represented deliberately, not silently treated as zero similarity. The output can expose $\eta$, $p_\beta$, and each contribution.

## Theoretical explanation

With $C=1$ denoting candidate inclusion, logistic regression specifies $P(M\mid x,C=1)$, not a factorization of $P(x\mid M,C=1)$.[7] Therefore it does **not** require independent predictors. **Reasoning:** duplicate columns can make individual coefficients non-identifiable even when their combined prediction is determined; near-duplicates can make coefficients unstable. Joint fitting avoids assuming each marginal signal is independent evidence, but it does not guarantee robust predictions or meaningful isolated effects.

A coefficient describes a conditional log-odds contribution given the chosen representation. It is not a causal effect or a standalone likelihood ratio. Probabilities in the unit interval are model outputs; misspecification, sampling bias, regularization, or drift can invalidate their calibration. The feature basis imposes linearity on the log-odds, not on probability itself.

## Important variants

Optional ridge or lasso penalties shrink contributions; prespecified interactions or spline bases relax selected functional restrictions. Generalized additive models allow nonlinear feature functions, and justified monotonic constraints may encode defensible semantics.[7] The [learned comparator menu](learned-neural-comparators.md) compares these bounded extensions; none is mandatory evolution. Constraints can suppress genuine reversals caused by source context; increased flexibility introduces additional assessment requirements.

## Assumptions and prerequisites

Require sufficiently informative adjudicated matches and difficult non-matches across operational source pairs, missingness patterns, and candidate routes. There is no universal minimum label count. Reserve independent calibration and test labels, and document unresolved annotation states rather than forcing every ambiguous pair into a binary target.

For unseen-identity transfer, separate identities across splits; for existing-identity continuation, use declared historical state and forward-time/as-of evidence without future-label feedback. These target different claims, not a universal ban on historical identity overlap. Weighting or resampling changes the fitted population: arbitrary class balancing does not preserve deployment probabilities. A simple intercept correction is justified only under explicitly verified class-prior sampling assumptions; see the [conditioning deep dive](../../deep-dives/selection-and-calibration.md). Hard-negative or review-queue labels typically require more than a prevalence adjustment.

## Applicability conditions

Consider logistic regression when interpretable comparison features exist and representative supervision is feasible. A small prespecified basis can be a useful learned-weight baseline. Sparse source segments, weak labels, or large unmodeled interactions may undermine transfer; they do not automatically justify a more complex model.

## Advantages

Jointly learned coefficients retain explicit contribution accounting, allow controlled feature ablations, and avoid a conditional-independence requirement on predictors. The logistic link provides an explicit conditional-probability model, subject to assumptions and empirical assessment.[7]

## Trade-offs and failure modes

The following failure analysis is Atlas reasoning grounded in the conditional model. Perfect or near separation can make unpenalized estimates diverge or unstable.[7] Correlated features can exchange coefficients across samples. An omitted interaction can leave systematically wrong conditional probabilities despite good aggregate ranking. Review-biased labels can exaggerate ambiguity; easy random negatives can underrepresent real candidates. A source identifier can become a shortcut that fails on new sources. Penalization does not by itself repair any sampling bias or calibrate predictions.

**Atlas synthesis:** tune regularization only within development data and report coefficient/prediction stability separately. Ridge or lasso may stabilize predictions with correlated features without identifying a uniquely meaningful contribution for each name transform. Class weighting, source quotas or score-directed annotation can change the target fitted population. Neither a good rank ordering nor a constrained coefficient sign establishes probability calibration on deployed candidates; source-conditioned checks and a justified sampling model remain necessary.

## Relationships with other methods

Addresses the [scoring decision](../../decisions/scoring-strategy.md), complements [evidence states](../comparison-features/evidence-states.md), and can support a [precision cascade](../../architectures/precision-cascade.md). [Expert additive scoring](additive-soft-matching.md) is a label-light comparator; [Fellegi–Sunter](fellegi-sunter.md) supplies a different generative evidence interpretation. [Thresholds and abstention](../decision-resolution/thresholds-abstention.md) remain separate from model fitting.

## How to evaluate

Use [pairwise quality and calibration](../../evaluation/pairwise-calibration.md) with unchanged candidates. Compare ranking, log loss or Brier score, reliability, coefficient stability, and source-specific errors; aggregate calibration can hide segment failures. Fit any post-processing only on held-out calibration labels, then test independently. Guo et al. study calibration methods for neural classification, not logistic ER; their findings do not guarantee an improvement here.[3]

## Research opportunities

Test a prespecified interaction or [contextual reliability](../../research/hypotheses/contextual-reliability.md) feature against the same regularized baseline. Separate gains from label acquisition, feature changes, and penalty selection. Require held-out operational improvements and explicit uncertainty before retaining extra complexity.

## References and evidence limitations

ESL chapter 4.4 supplies the conditional logistic foundation, not linkage-specific superiority.[7] Calibration literature motivates assessment, but the cited neural study is non-ER and cannot validate this model or its transfer.[3]

## Sources

[3] https://proceedings.mlr.press/v70/guo17a.html — On Calibration of Modern Neural Networks
[7] https://hastie.su.domains/ElemStatLearn/main.html — The Elements of Statistical Learning, second edition
