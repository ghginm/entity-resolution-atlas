---
id: SOL-07-004
type: solution
title: Pooling and source-conditioned evidence reliability
domain: "07"
summary: >-
  Compare pooled, source-specific and partially pooled evidence models when
  fields have different error processes across source pairs or periods. Separate
  contextual match prevalence from class-conditional evidence reliability.
  Requires observed provenance, compatible comparison semantics and independent
  evaluation support for the claimed contexts. Pooling can stabilize sparse
  estimates while concealing heterogeneity; separate models can expose it while
  overfitting tiny groups. Hierarchical shrinkage is a proposed compromise, not
  a verified ER improvement or a substitute for unseen-source validation.
tags: [source-aware, few-labels, sparse, interpretable, calibration, uncertainty, pairwise]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  addresses: [DEC-07-001]
  complements: [SOL-07-002, SOL-07-003, SOL-06-003, HYP-07-001]
  evaluated_by: [EVAL-11-002, EVAL-11-005]
---

# Pooling and source-conditioned evidence reliability

## Short summary and problem addressed

The question is not whether some source is universally trustworthy. It is whether **a field's observed evidence has different match/nonmatch distributions in a declared context**, and whether labels support estimating that difference. A pooled scorer can average over distinct collection processes; fully separate scorers can estimate noise in small groups. This card owns the pooling choice, while [Fellegi–Sunter](fellegi-sunter.md) owns likelihood-ratio construction and [logistic regression](logistic-regression.md) owns discriminative fitting.

## Core mechanism and theoretical explanation

**Conditional-probability reasoning:** let $Z$ denote an observed source-pair/time context, $C$ candidate inclusion, $M$ a true match and $U$ a nonmatch. On common positive support, contextual evidence is

$$
W_{C,z}(\gamma)=\log\frac{P(\gamma\mid M,C=1,Z=z)}{P(\gamma\mid U,C=1,Z=z)}.
$$

Posterior log-odds additionally require the prior $P(M\mid C=1,Z=z)$. A context-specific intercept may therefore model prevalence without changing field reliability. If a contextual scorer improves only because match prevalence differs, that does not establish different error processes for the field. The original linkage theory discusses weight calculation from population/error information and the assumptions needed to reuse weights across populations and record-generating processes.[1]

**Atlas synthesis:** compare three parameter-sharing strategies:

| Strategy | Operation | Potential advantage | Main risk |
|---|---|---|---|
| Complete pooling | One evidence table or conditional model across contexts | More observations inform each effect | Stable-looking average hides opposing segment behavior |
| No pooling | Separate parameters for each supported context | Context-specific behavior can be represented | Sparse cells, unstable ratios, no justified unseen-context model |
| Partial pooling | Estimate contextual deviations with shared shrinkage | Sparse contexts can borrow information under a shared structure | Wrong similarity assumptions shrink important exceptions toward an unsafe average |

For illustration, a discriminative formulation can use a global feature coefficient plus a context deviation. Penalizing deviations toward zero controls how strongly the context departs from the shared model. A hierarchical probabilistic formulation instead specifies a distribution over deviations. These are **proposed model structures**, not equivalent inference procedures or verified specialist methods in this wave. No primary hierarchical-ER paper was checked; detailed prior choice and uncertainty computation require further specialist evidence.

## Worked example and important variants

**Synthetic scenario:** a source copies old addresses while another verifies current addresses. Address disagreement may be compatible with continuing person identity in the former context, while a contemporary incompatible identifier has different semantics. A pooled address coefficient can hide this variation. However, the apparent difference may instead result from candidate rules, alias coverage, identity mix or review selection. “Source quality” measured from the model's own accepted matches is circular evidence, not an independent reliability estimate.

Variants include source-pair tables, field-specific deviations, temporal strata, missingness interactions and context-prior-only adjustment. Preserve [identifier namespace/validity](../comparison-features/identifier-namespaces.md) as observed semantics rather than hide them inside source weights. Known incompatibility may belong to policy, not a learned reliability contribution. Multiple source labels derived from one copied observation do not supply independent corroboration.

## Assumptions, prerequisites and applicability

Hard prerequisites are context available at decision time, comparable feature meanings and an explicit target candidate population. Source-profiling metadata is useful but not identity truth. Independent adjudication across relevant classes and contexts is needed to validate claimed quality; a no-label fit can still be explored, but not certified by its own latent confidence.

Pooling is credible when sharing assumptions are plausible or evidence is too sparse to support differences. No pooling is plausible when processes differ materially and each segment has adequate support. Partial pooling is worth testing when there is both heterogeneity and a defensible sharing structure. None automatically transfers to a new source. An unseen-context fallback must expose uncertainty and obey required policy guards; “use the pooled model” is a proposal requiring evaluation, not a guarantee.

## Advantages, trade-offs and failure modes

Explicit context exposes what is shared, what is estimated separately and why. It supports source-level debugging and distinguishes prior adjustment from reliability adjustment. Costs include extra parameters, metadata dependencies, larger evaluation slices and versioned fallback behavior. Source-pair combinations can proliferate faster than independent labels; repeated pairs from a few entities do not solve that support problem.

A context can proxy sensitive populations, collection policy or annotation differences. Source drift can change class priors and feature distributions simultaneously. Global recalibration can conceal source-specific errors. Shrinkage can improve stability while biasing a rare but high-harm segment; fully separate tables can look certain after empty-cell smoothing. Neither extra parameters nor a strong regularizer repairs selection bias or zero evaluation support.

## Relationships and how to evaluate

Use the [contextual-reliability hypothesis](../../research/hypotheses/contextual-reliability.md) for a falsifiable adoption question and [selection/calibration deep dive](../../deep-dives/selection-and-calibration.md) for population conditioning. Keep normalization, candidates, feature semantics, label budget, tuning effort and policy selection protocol fixed for the initial [controlled comparison](../experimentation/controlled-comparison.md). Compare pooled baseline, context-prior-only model and field-context model before attributing gains to reliability. Then compare no-pooling with a prespecified shrinkage configuration; inspect parameter stability and context support.

[Pairwise evaluation](../../evaluation/pairwise-calibration.md) must report discrimination, proper scoring rules, calibration, harmful decisions, review load and runtime by source pair, time and missingness. For unseen-identity transfer use entity separation; for existing-identity continuation use forward-time, as-of history without future labels. Hold out whole source contexts when transfer to new sources is claimed, acknowledging whether the fallback is being tested rather than an estimated per-source effect.

Use sampling-design-appropriate uncertainty and the [incomplete-reference route](../../evaluation/incomplete-reference-quality.md): a tiny contextual holdout or unknown labels cannot certify segment safety. Predeclare worthwhile benefit, high-cost merge limits and budget. Retain pooling if added context fails practical criteria, reject unsafe segment behavior despite an average gain, and call wide or under-supported comparisons inconclusive. Replicate positive evidence in another period before broader promotion.

## Research opportunities and evidence limitations

When does statistical efficiency from sharing outweigh hidden heterogeneity? Which sharing structure survives source onboarding rather than memorizing provenance? These are project experiments, not conclusions from this card. Likelihood conditioning follows probability definitions; pooling design and hierarchy suggestions are Atlas synthesis. No local fitting, ER experiment or measured transfer improvement accompanies them.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
