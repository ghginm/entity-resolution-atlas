---
id: SOL-07-002
type: solution
title: Fellegi–Sunter evidence weighting
domain: "07"
summary: >-
  Compare the distribution of observed comparison evidence among true matches
  with its distribution among non-matches. The joint likelihood ratio is the
  theoretical foundation; additive field weights require conditional independence
  within both classes. State-specific probabilities may be estimated from
  labels or a constrained mixture model, but unlabeled estimation is not
  assumption-free. Candidate conditioning, prior odds, dependency, and estimation
  uncertainty determine whether likelihood-ratio scores can support credible
  posterior probabilities and operational decisions.
tags: [entity-agnostic, no-labels, few-labels, interpretable, pairwise, blocking, missingness, calibration, uncertainty]
maturity: established
evidence: supported-by-external-literature
relations:
  addresses: [DEC-07-001]
  alternative_to: [SOL-07-003]
  complements: [SOL-05-002]
  evaluated_by: [EVAL-11-002]
  used_by: [AR-01]
---

# Fellegi–Sunter evidence weighting

## Short summary

Score observed comparison patterns by how much more probable they are under matches than non-matches. Fellegi–Sunter orders patterns by their likelihood ratio and supports link, non-link, and possible-link dispositions under stipulated distributions and error constraints.[1]

## Problem addressed

Equal similarity values need not carry equal identity evidence. An agreement common among non-matches provides less support than one unusual among non-matches, relative to its occurrence among matches. Comparison-state probabilities replace arbitrary points with an explicit statistical evidence model.[1]

## Core mechanism

Let $M$ mean same entity, $U$ mean different entities, $\gamma$ be the comparison vector, and $C=1$ mean candidate inclusion. For the candidate population define

$$
m_C(\gamma)=P(\gamma\mid M,C=1),\quad
u_C(\gamma)=P(\gamma\mid U,C=1),\quad
W_C(\gamma)=\log\frac{m_C(\gamma)}{u_C(\gamma)}.
$$

The joint likelihood ratio is foundational; it does not itself assume field independence.[1] **Candidate-conditioned adaptation:** only when evidence groups are conditionally independent within both $M,C=1$ and $U,C=1$ does

$$
W_C(\gamma)=\sum_j\log\frac{m_{j,C}(\gamma_j)}{u_{j,C}(\gamma_j)}
$$

follow. Estimate $m_{j,C}(s)$ and $u_{j,C}(s)$ for **each state** $s$: exact, partial, conflict, or missing, as defined by the comparison contract. Binary agreement parameters do not automatically specify partial-agreement weights. The original factorization permits groups of dependent subcomponents, not necessarily individual raw fields.[1]

## Theoretical explanation

**Bayes reasoning, assuming valid candidate-conditioned distributions and prior** $\pi_C=P(M\mid C=1)$:

$$
\operatorname{logit}P(M\mid\gamma,C=1)
=\operatorname{logit}\pi_C+W_C(\gamma).
$$

Thus a likelihood ratio is not a posterior probability. A log ratio of zero means evidence equally likely under both classes, not an even posterior split. The prior and distributions must describe the same population. Plug-in estimates produce model-based probabilities, not guaranteed empirical calibration. The landscape review explains this mixture/posterior interpretation and its assumptions.[5]

## Important variants

Estimate state probabilities from adjudicated samples, use frequency-specific agreement states, or model dependent groups jointly. Log-linear dependence variants and latent-mixture estimation are described in the landscape.[5] These variants have no separate pilot cards. Frequency-aware refinements should account for relevant non-match frequencies, not assert that rarity always strengthens evidence.

**Manual specification is a credible baseline, not a failed EM fit.** The original paper distinguishes weights based on prior population/error information from estimation using the files, and states assumptions for later weight reuse.[1] As Atlas operational synthesis, elicit a complete distribution across mutually exclusive states for each modeled group and class, record its population and rationale, and check normalization, positive support and sensitivity. Do not equate an expert's “field accuracy” with every match/nonmatch state probability. Deliberate smoothing prevents unsupported infinite ratios but is an assumption to audit, not new evidence. Missing and partial states need their own treatment; arbitrary weights are not made likelihood ratios by relabeling them as probabilities.

Winkler's 1990 comparison includes externally specified and EM-derived matching variants, partial-agreement comparators, frequency weights and dependency adjustments.[29] It establishes that these estimation alternatives were used in particular Census comparisons, not that EM must replace interpretable manual parameters. Keep comparison definitions, candidates and review evidence fixed when comparing them. [Source-conditioned pooling](source-aware-reliability.md) is a separate estimation choice applicable to either route.

## Assumptions and prerequisites

Labeled estimates need representative class-conditional samples and explicit sampling corrections. Unlabeled EM fits a restricted mixture
$P(\gamma\mid C=1)=\pi_Cm_C(\gamma)+(1-\pi_C)u_C(\gamma)$; EM-based extensions are reviewed in [5]. **Reasoning:** absent restrictions, this mixture need not identify its components. Identifiability depends on sufficiently informative, nondegenerate states and model structure; label switching requires semantic anchoring. Multiple starts, plausible constraints, and reviewed examples should check local solutions. Convergence does not validate the independence assumption, identify truth, or certify calibration.

**Identifiability counterexample (reasoning):** a single observed binary agreement frequency can be represented by different combinations of match prevalence and class-specific agreement probabilities. Maximizing the same mixture likelihood cannot tell those explanations apart. Additional independent comparison groups, justified restrictions or trusted anchors may add information, but more fields copied from one value need not do so. Multiple EM starts probe optimization stability; they do not test this identification problem. Independent adjudication and out-of-sample error analysis remain necessary to validate the model's interpretation.

## Applicability conditions

Consider this method when comparison states are interpretable and their distributions can be estimated credibly. Limited labels may make a generative model attractive, but weak evidence, extreme sparsity, or unrestricted dependence can make estimation unreliable. Document smoothing or prior choices for rare states rather than converting unobserved events into certainty.

## Advantages

State weights have a direct evidence interpretation. The distinction between match and non-match distributions exposes why agreement frequency matters. The stipulated-distribution theory supplies an ordering and decision framework, rather than only an unexplained weighted sum.[1]

## Trade-offs and failure modes

Name-derived comparisons or correlated address fields can double-count evidence under fieldwise factorization. Blocking can fix a feature to agreement or induce dependencies between otherwise separable features; transferred all-pairs weights may misstate candidate evidence. Sparse cells can yield unstable or infinite estimated ratios. Pairs sharing records also create cross-pair dependence, relevant to uncertainty and global resolution, distinct from within-vector dependence.[5]

## Relationships with other methods

Addresses the [scoring decision](../../decisions/scoring-strategy.md), can consume [multi-pass candidates](../candidate-generation/multi-pass-blocking.md), and substitutes for [logistic regression](logistic-regression.md) on the same evidence contract. Combining it with [thresholds and abstention](../decision-resolution/thresholds-abstention.md) does not make independent pair decisions a valid assignment or clustering. See [selection and calibration](../../deep-dives/selection-and-calibration.md) for nonduplicative conditioning analysis.

## How to evaluate

Use [pairwise quality and calibration](../../evaluation/pairwise-calibration.md): inspect observed versus modeled state frequencies, dependency residuals, rare-state sensitivity, and reliability by source and retrieval route. Compare against expert additive and logistic baselines with fixed candidates and labels. Reserve representative adjudication for checking unlabeled fits; report uncertainty rather than trusting mixture confidence alone.

## Research opportunities

Test grouping correlated evidence versus fieldwise factorization, or source-specific estimates versus pooled estimates. Hold comparison definitions and decision losses fixed. Check whether improvements survive smaller segments and changed candidate routes; no gain is presumed.

## References and evidence limitations

The original theorem assumes stipulated distributions and error constraints, not universal calibration or optimal entity assembly.[1] The landscape summarizes later estimation variants; this Atlas has not fitted or validated them.[5]

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
[29] https://www.stat.cmu.edu/NCRN/PUBLIC/RLClassFiles/HW/Winkler1990.pdf — String Comparator Metrics and Enhanced Decision Rules in the Fellegi-Sunter Model of Record Linkage
