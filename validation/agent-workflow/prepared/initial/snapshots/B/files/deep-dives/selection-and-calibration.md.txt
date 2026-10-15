# Selection, dependence, and calibration in candidate scoring

**L3 purpose.** Candidate conditioning can change class priors, comparison-state frequencies, and evidence dependence at once. This deserves a shared deep dive because treating it as merely a threshold adjustment produces contradictory probability interpretations across [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), [logistic regression](../solutions/matching-scoring/logistic-regression.md), and [expert additive scoring](../solutions/matching-scoring/additive-soft-matching.md). This document adds conditioning identities and diagnostic implications, not another scorer tutorial. Mathematical statements below are reasoning under explicit assumptions; no empirical improvements are claimed.

## 1. Name the statistical population

Let $Y\in\{M,U\}$ denote true match status, $X$ the available pair information, $\gamma=g(X)$ the retained comparison vector, and $C=1$ candidate inclusion. Distinguish all allowable pairs, retrieved candidates, sampled labeled pairs, and eventual decisions. Probabilities for one population do not automatically describe another.

A scorer trained after blocking often targets $P(M\mid\gamma,C=1)$. Its evaluation must name the retrieval version and source mixture. Candidate-only evaluation cannot reveal matches never retrieved. Classical linkage explicitly discusses blocking; the landscape distinguishes statistical pair linkage from broader entity resolution.[1][5]

## 2. Selection changes more than the prior

**Bayes reasoning:** write $m(\gamma)=P(\gamma\mid M)$, $u(\gamma)=P(\gamma\mid U)$, and $q_y(\gamma)=P(C=1\mid\gamma,Y=y)$. Where denominators and support are positive,

$$
m_C(\gamma)=\frac{q_M(\gamma)m(\gamma)}{P(C=1\mid M)},\qquad
u_C(\gamma)=\frac{q_U(\gamma)u(\gamma)}{P(C=1\mid U)}.
$$

Consequently,

$$
\frac{m_C(\gamma)}{u_C(\gamma)}
=\frac{m(\gamma)}{u(\gamma)}
\frac{q_M(\gamma)}{q_U(\gamma)}
\frac{P(C=1\mid U)}{P(C=1\mid M)}.
$$

The candidate prior odds acquire the inverse final factor. Here $\pi=P(M)$ and $\pi_C=P(M\mid C=1)$:

$$
\frac{\pi_C}{1-\pi_C}
=\frac{\pi}{1-\pi}\frac{P(C=1\mid M)}{P(C=1\mid U)}.
$$

Multiplying shows exactly which factors cancel. Changing only a prior while retaining incompatible likelihoods can double-count retrieval evidence. Conversely, a valid full-information posterior need not be refitted solely because some pairs are discarded: if inclusion is determined by the complete retained $X$, then $P(M\mid X,C=1)=P(M\mid X)$ on included support. Conditioning is not universally a posterior distortion.

The practical exception matters: retrieval may use a phonetic key, embedding, or pass-specific field omitted from $\gamma$. Then inclusion can contain extra information about match status at fixed $\gamma$; $q_M/q_U$ need not cancel. Validate the deployed representation, not an imagined complete one.

## 3. Fixed features and induced dependence

**Reasoning:** under exact surname-agreement blocking, the blocking agreement state has candidate-conditioned probability one in both classes. Its candidate-conditioned marginal likelihood ratio is one, hence its log contribution is zero. This does not mean surname agreement is universally uninformative: selection has already incorporated that evidence into the population and prior. Reusing an unconditional agreement weight with a candidate-conditioned prior can count it again.

Multi-pass inclusion can induce dependence even from class-conditionally independent comparisons. Let binary states $A$ and $B$ indicate two blocking agreements, with inclusion $C=A\lor B$. Suppose both have nondegenerate probabilities within each class. Among candidates, $P(A=0,B=0\mid Y,C=1)=0$, although both marginal disagreement probabilities remain positive. Their joint distribution therefore cannot factor into candidate-conditioned marginals. Logging which passes retrieved a pair aids diagnosis; it does not itself restore independence.

Keep three dependencies separate: dependence between fields within a pair; dependence between different pairs sharing records; and constraints between feasible global links. Fellegi–Sunter's joint likelihood ratio does not require independent fields, whereas its additive fieldwise simplification does.[1] Logistic regression does not factor the predictor distribution, but a misspecified conditional basis can still fail.[7] Shared records also affect evaluation uncertainty, even when predictions are individually useful.[5]

## 4. Labeled selection is a second conditioning step

Let $R=1$ denote entry into the labeled fitting sample and $s_y(x)=P(R=1\mid X=x,Y=y,C=1)$. **Bayes reasoning on common support:**

$$
\operatorname{odds}(M\mid x,C=1,R=1)
=\operatorname{odds}(M\mid x,C=1)\frac{s_M(x)}{s_U(x)}.
$$

If sampling depends only on class, this multiplier is constant. Under a correctly specified logistic model, unchanged class-conditional feature distributions, and compatible estimation, an intercept shift can recover target odds; the adjustment is target prior log-odds minus sample prior log-odds. This is a restricted case, not permission to “fix imbalance” with any intercept.

Hard-negative sampling, active review, source quotas, and score-based adjudication often produce feature-dependent inclusion. Use known inclusion probabilities where valid, or obtain representative labels; neither strategy fixes zero support. Unknown outcomes outside reviewed regions remain unknown. Entity-disjoint splits address leakage, not sampling bias. Oversampling difficult cases can support diagnosis while requiring a different sample for population risk estimation.

## 5. Probability interpretation is a hierarchy

A raw additive sum is a ranking specification. A correctly estimated likelihood ratio describes comparative evidence. Adding compatible prior log-odds and applying the logistic map yields a model-based posterior. A logistic model directly proposes a conditional probability function. None of these operations proves empirical reliability.

Guo et al. define confidence calibration and evaluate post-processing for neural image and document classifiers; their study is not ER evidence and does not establish universal superiority of temperature scaling.[3] **Binary ER adaptation:** score-level calibration means $P(M\mid\hat p=t,C=1)=t$. It is weaker than correctness of $P(M\mid X,C=1)$: groups with different error rates may average to the same reliability curve. A constant prevalence predictor can be calibrated while providing no ranking discrimination.

Separate discrimination, calibration, and resolution feasibility. Preserving order under a strictly increasing recalibration can leave ranking metrics unchanged while changing risk-based actions. Segment-dependent costs require reliability at the action's conditioning level. A single global curve cannot validate every source pair, retrieval route, or missingness pattern.

## 6. What to carry into experiments and decisions

For [pairwise assessment](../evaluation/pairwise-calibration.md), record candidate and labeling designs; reserve representative calibration labels and an independent test set. Inspect reliability with uncertainty, proper scoring rules, ranking, and operational slices. Sparse tail bins are not evidence of certainty. Reassess after changing blocking or source composition; reweighting needs overlap and a justified shift model.

The [cost-based policy](../solutions/decision-resolution/thresholds-abstention.md) assumes validated probabilities and specified losses. Pairwise calibration does not make independent thresholds satisfy one-to-one constraints or produce coherent entity partitions. Use [entity-resolution assessment](../evaluation/entity-resolution-quality.md) separately, and preserve unresolved cases when the evidence contract cannot justify a decision. No implementation, fitted model, or measured calibration result accompanies this deep dive.

## Evidence limitations

The original linkage theory supports joint-ratio and factorization distinctions; the landscape supports broader modeling caveats.[1][5]
ESL supplies the conditional logistic model, and Guo supplies non-ER calibration context.[7][3]
Selection identities and diagnostic recommendations here are explicit Atlas reasoning, not claimed benchmark findings.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[3] https://proceedings.mlr.press/v70/guo17a.html — On Calibration of Modern Neural Networks
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
[7] https://hastie.su.domains/ElemStatLearn/main.html — The Elements of Statistical Learning, second edition
