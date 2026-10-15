---
id: HYP-07-001
type: hypothesis
title: Context-dependent attribute reliability without circular supervision
domain: "07"
summary: >-
  Test whether constrained source- and time-aware evidence weighting reduces
  held-out decision cost relative to a pooled scorer with the same candidates
  and comparisons. The proposal is untested: contextual likelihoods motivate
  it, but sparse source pairs, label bias, circular reliability estimates, and
  population shifts can defeat it. Independent adjudication, hierarchical
  shrinkage, entity-disjoint and temporal holdouts, and predeclared precision
  and compute guardrails are prerequisites. Context is a conditional evidence
  model, not a universal ranking of trustworthy sources.
tags: [experimentation, source-aware, evidence-engineering, pairwise, interpretable, asymmetric-costs, uncertainty, entity-agnostic]
maturity: experimental
evidence: theoretically-motivated
relations:
  tests: [SOL-07-002, SOL-07-003]
  evaluated_by: [EVAL-11-002, EVAL-11-003]
  complements: [SOL-06-001]
---

# Context-dependent attribute reliability without circular supervision

## Question and explicitly untested hypothesis

Can field-specific weighting conditional on source provenance and temporal quality reduce decision cost without sacrificing required precision? **This hypothesis is untested in the Atlas.** For a defined target population, it predicts that a constrained contextual scorer will outperform a pooled scorer by a predeclared practically meaningful cost reduction, with identical candidates, comparisons, and downstream policy. Contextual weighting is not universally necessary; homogeneous data or few independent labels may favor the simpler baseline.

## Mechanism, ownership, and assumptions

Likelihood-ratio reasoning compares evidence distributions under match and nonmatch hypotheses.[1] For comparison vector γ and observed context z, contextual evidence is log[P(γ | match,z)/P(γ | nonmatch,z)]. Posterior interpretation also requires the contextual match prior; a source-specific intercept may reflect prevalence rather than field reliability. The experimental design must distinguish these effects.

A possible [logistic scoring](../../solutions/matching-scoring/logistic-regression.md) intervention uses score = β_0 + sum β_k x_k + sum θ_kz x_k z, with constrained or shrunk interaction terms. As proposed reasoning, an address disagreement could receive different weight for stale versus contemporaneous observations, while identifier agreement may depend on namespace integrity. Provenance and observation age must be available at decision time, not inferred from final successful linkage.

Source profiling belongs to data understanding; encoding validity and provenance belongs to evidence engineering; learning these conditional contributions belongs to scoring. This card owns the final hypothesis rather than duplicating all three domains. It does not assign a single trust score to each source. Copied attributes and shared collection processes can create dependent errors, so more context does not automatically justify additive independence.

## Independent supervision and sparse contexts

Use independently adjudicated match/nonmatch labels or external audited evidence to estimate conditional reliability. Never estimate a source's correctness from this scorer's own predicted matches and then treat that estimate as independent confirmation. Weak or pseudo-label supervision would be a separate experiment with explicitly weaker evidence, not a substitute for held-out truth.

Many source-pair/field combinations will have few labeled entities. Use a prespecified hierarchical shrinkage structure toward pooled field effects, minimum-support rules, and an unseen-context fallback. Compare this constrained intervention with unrestricted interactions only as an additional development ablation. Do not present shrinkage as proven ER improvement; it is a proposed variance-control mechanism, unexpanded as a supporting method in this pilot. Explain pooled fallback decisions and their uncertainty rather than hiding unsupported weights.

## Baseline and controlled experiment

Choose pooled [FS evidence](../../solutions/matching-scoring/fellegi-sunter.md) or a pooled logistic scorer as the baseline, keeping the scorer family fixed. Compare pooled weights, context-prior-only adjustment, and contextual field interactions to separate prevalence from reliability effects. Fix normalization, candidate sets, comparison functions, training label budget, tuning effort, frequency features, calibration procedure, thresholds' selection protocol, and entity-resolution policy. Preserve [missing/invalid evidence states](../../solutions/comparison-features/evidence-states.md); missingness and agreement are different events.

Required data include provenance, collection/observation timestamps, independently adjudicated labels, and sufficiently complete reference entities to measure final false merges. Separate entity-disjoint training, calibration, and evaluation cohorts; also reserve a later temporal holdout. Add held-out source pairs if transfer to new combinations is claimed. Prevent shared entities and copied histories crossing splits, and freeze external quality estimates to information available before the test horizon.

## Metrics, confounders, and falsification

Primary metric: reduction in held-out weighted expected decision cost, with prespecified false-merge, missed-match, and review costs. Before evaluation, register numerical minimum worthwhile reduction δ_cost, precision floor P_min, maximum recall loss, catastrophic-overmerge limit, and compute/review budgets. Choose them from application consequences, not observed test gains. Select thresholds on calibration labels only. [Pairwise evaluation](../../evaluation/pairwise-calibration.md) supplies weighting, AP convention, probability diagnostics, and threshold sensitivity; [entity-quality evaluation](../../evaluation/entity-resolution-quality.md) checks downstream harm.

Use paired, sampling-design-aware entity/cluster uncertainty and power for δ_cost. Support practical benefit only when the lower confidence bound exceeds δ_cost and all guardrails hold. An adequately powered upper confidence bound below δ_cost falsifies the practical-benefit claim for the stated population; breaching a safety guardrail rejects adoption even with lower average cost. Intervals spanning the worthwhile reduction are inconclusive. Confounders include source identity proxying demographics, uneven adjudication quality, source-pair prevalence, temporal drift, copied observations, and additional parameter capacity. Inspect sparse and unseen contexts separately; aggregate benefit must not conceal precision failures.

After a positive result, replicate in another period and audit explanations, fairness-relevant segments, and fallback behavior. After a negative result, examine label support, shrinkage, prior-only effects, and whether context adds information beyond existing features. Retain the simpler baseline when warranted. Combining this proposal with [frequency-aware evidence](frequency-aware-evidence.md) needs a separate interaction experiment; neither hypothesis implies universal research priority.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
