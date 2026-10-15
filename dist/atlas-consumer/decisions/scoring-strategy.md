---
id: DEC-07-001
type: decision
title: How should candidate pairs be scored?
domain: "07"
summary: >-
  Compare expert-weighted additive evidence, Fellegi–Sunter likelihood ratios,
  and supervised logistic regression without treating them as a mandatory
  progression. Choose using identity semantics, candidate selection, evidence
  dependencies, label representativeness, interpretability, and downstream
  losses. Distinguish ranking scores from probabilities and scoring from
  decision policy. Reliable identifiers may justify simpler rules; limited
  labels do not remove statistical assumptions. Controlled comparisons must
  hold candidate generation and evaluation populations explicit.
tags: [entity-agnostic, interpretable, pairwise, calibration, few-labels, asymmetric-costs, evaluation]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  complements: [DEC-05-001, SOL-07-004, SOL-07-005]
  evaluated_by: [EVAL-11-002, EVAL-11-003]
---

# How should candidate pairs be scored?

## Decision question

Which evidence-combination mechanism is defensible for the intended candidate population, and what meaning should its output carry: ordering, likelihood ratio, or estimated match probability? Choose a scorer independently of whether downstream resolution uses pairwise decisions, assignment, or clustering. Statistical linkage and entity-level reconstruction are related but distinct problems.[5]

## Problem context

Candidate pairs already reflect retrieval choices; their comparison vectors contain agreements, partial similarities, missingness, and contradictions. Scoring must combine these without silently treating duplicated representations as independent evidence. A shared surname can be weak evidence among surname-blocked candidates even when unusual among arbitrary record pairs. The [comparison decision](comparison-evidence.md) defines the evidence contract; the [candidate decision](candidate-strategy.md) defines which pairs the scorer will encounter.

## Relevant assumptions and prerequisites

Before selecting a family, document:

- Identity semantics, identifier namespaces, time validity, and permitted source cardinalities.
- Candidate-rule versions and inclusion provenance; changes alter the statistical target.
- Feature state definitions, missingness indicators, source reliability, and suspected dependencies.
- Available adjudicated labels, sampling design, unresolved cases, and entity-disjoint or temporal evaluation splits.
- Whether operations require only a rank order or defensible probabilities for explicit losses.

A numerical score is not evidence that these prerequisites hold. An unvalidated transformation into the interval zero to one does not establish calibration.

## Available solution families

- [Additive soft matching](../solutions/matching-scoring/additive-soft-matching.md): manually assign positive and negative contributions to explicit comparison features. Transparent, label-light, and useful as a controlled baseline; probability meaning requires additional justification.
- [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md): estimate comparison distributions under matches and non-matches, then form likelihood ratios. The joint formulation does not require independent fields; the familiar sum of field weights requires conditional factorization.[1]
- [Logistic regression](../solutions/matching-scoring/logistic-regression.md): learn conditional log-odds from labeled comparison vectors. It does not require independent predictors, but its chosen feature basis constrains the conditional relationship.[7]
- [Pooling and source-conditioned reliability](../solutions/matching-scoring/source-aware-reliability.md): compare shared, separate and shrunk context parameters while separating prevalence from field reliability. This is an estimation choice composable with the scorer family, not a competing architecture.
- [Nonlinear, embedding and language-model comparators](../solutions/matching-scoring/learned-neural-comparators.md): compare additive nonlinear functions, boosted trees, ranking and neural roles against the simple baselines. Richer capacity, label demands and cost require independent evidence, not a mandatory complexity ladder.
- [Namespace-qualified exact rules](../solutions/comparison-features/identifier-namespaces.md), [weak supervision](../solutions/ground-truth/weak-supervision.md) and [rule composition](rule-composition.md) retain separate semantic, training-label and policy responsibilities. Other ensemble/specialist variants remain unexpanded rather than implied validated methods.

## Criteria for choosing

Prefer a reliable-identifier rule only when uniqueness, scope, and observation quality justify its semantics. Consider expert additive scoring when labels are scarce and explanations need explicit evidence accounting. Consider Fellegi–Sunter when comparison-state distributions can be estimated credibly, including candidate conditioning. Consider logistic regression when labels cover operational matches and difficult non-matches, and a manageable feature basis is plausible. Label abundance alone does not establish representativeness.

## Trade-off comparison

| Family | Weight interpretation | Principal burden | Important risk |
|---|---|---|---|
| Expert additive | Designed evidence points | Elicitation and sensitivity analysis | Subjective scale; compensating conflicts |
| Fellegi–Sunter | Joint or factorized log likelihood ratio | Estimating match/non-match distributions | Dependence and selection misspecification |
| Logistic | Conditional log-odds coefficients | Representative labels and model assessment | Sampling bias; unstable correlated coefficients |

These burdens follow the respective mechanisms.[1][7] Interpretability means knowing how contributions were obtained, not asserting that a coefficient is causal. Candidate selection can invalidate a transferred probability interpretation even if ranking remains useful; see the [selection and calibration deep dive](../deep-dives/selection-and-calibration.md).

## Good baseline candidates

Keep an expert additive specification and, where justified, a small reliable-identifier rule as interpretable reference points. Compare statistically learned weights on the same evidence states and candidates. Fellegi–Sunter and logistic regression offer different estimation routes, not successive maturity grades. Regularization, interactions, and additive nonlinear functions are optional responses to diagnosed limitations, not obligatory upgrades.[7]

## Related evaluations

Use [pairwise quality and calibration](../evaluation/pairwise-calibration.md) to compare ranking, probability reliability, and threshold sensitivity. Freeze features and candidate rules initially; reserve separate fitting, calibration, and final testing populations. Report source-pair and missingness slices, costs, and uncertainty. Then use [entity-resolution quality](../evaluation/entity-resolution-quality.md) under an unchanged resolution policy: better pairwise ordering need not establish better final entities.[5] Audit [candidate recall](../evaluation/candidate-recall.md) separately because scorers cannot rank omitted pairs.

## Open questions and next experiments

Does disagreement come from weight estimation, missing evidence, or dependence? Compare manual versus learned contributions first, then ablate redundant representations or add one justified interaction. Hold policy fixed before testing [thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md). Treat source-aware gains as the untested [contextual reliability hypothesis](../research/hypotheses/contextual-reliability.md), with explicit failure criteria. No method is declared universally optimal; no Atlas performance experiment has been run.

## References and evidence limitations

Fellegi–Sunter supplies stipulated-distribution decision theory, not automatic operational calibration.[1] ESL supplies general logistic foundations, not an ER superiority result.[7] The ER landscape supports scope distinctions, not a benchmark recommendation.[5]

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
[7] https://hastie.su.domains/ElemStatLearn/main.html — The Elements of Statistical Learning, second edition
