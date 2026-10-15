---
id: SOL-10-003
type: solution
title: Targeted active review for learning and high-risk diagnosis
domain: "10"
summary: >-
  Allocate a learning or diagnostic review budget to uncertainty, disagreement,
  diversity, scarce-source evidence and consequential cluster decisions rather
  than treating every unlabeled pair alike. Acquire auditable labels, retain
  abstentions and revise the learner or error hypotheses through logged feedback.
  Compare against uniform acquisition on a separate independent test population
  under both label-count and actual-cost budgets. The approach needs adequate
  evidence access and a protected evaluation pool; heuristic query scores and
  selective label yield do not establish population accuracy or active-learning
  guarantees.
tags: [entity-agnostic, few-labels, human-review, uncertainty, source-aware, clustering, asymmetric-costs, experimentation, evaluation]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-10-001]
  evaluated_by: [EVAL-11-002, EVAL-11-003, EVAL-11-005]
---

# Targeted active review for learning and high-risk diagnosis

## Short summary

Select reviews for a stated learning or diagnostic objective, not as a representative accuracy sample. Source [18] supplies a specific importance-weighted active-learning construction with conditional query probabilities and theoretical assumptions; it does not prove that arbitrary uncertainty or graph-risk heuristics improve ER.[18] The operational variants below are proposals requiring controlled comparison.

## Problem addressed

Uniform review can spend scarce expert attention on repetitive easy cases. A boundary-focused learner may instead waste that budget on intrinsically unknowable pairs, ignore confidently wrong subpopulations or miss a decisive bridge whose removal changes many memberships. Acquisition must distinguish lack of labels from lack of evidence, and scorer uncertainty from downstream harm.

## Core mechanism

1. **Define objective and eligible pool.** Name the learner or failure hypothesis to change, unit of annotation, accessible sources, review budget and permitted feedback. Freeze an independent evaluation pool with its own [probability-review design](probability-sampled-review.md); reserve calibration labels separately. Candidate-only active selection cannot discover identities outside its eligible pool.
2. **Establish a credible baseline.** Begin with the same seed training labels, downstream model and evidence access as uniform random acquisition. Record source coverage and label scarcity before ranking queries; a source with few labels may also lack resolvable evidence.
3. **Rank under explicit heuristics.** Choose one signal or a declared combination from the variants below. Log model versions, query scores, eligible units, batch membership and randomized query probabilities when present. Do not call a ranking score a selection probability. Batch diversity can reduce duplicate investigations of one entity, but must not silently suppress rare slices.
4. **Obtain evidence-bearing feedback.** Reviewers return match, nonmatch or unknown, evidence provenance and reasons for abstention. Re-review disagreements with a specialist or independent search. Hide predictions where feasible; similarity to the model's answer is not an adjudication rule. Keep annotation uncertainty distinct from model uncertainty.
5. **Update only authorized learning artifacts.** Retrain or revise features/policy from the learning pool, then recompute query priorities at scheduled rounds. Record what changed; keep active diagnosis without model changes as a separate arm. Human corrections must not automatically trigger irreversible production membership changes.
6. **Stop by a predeclared rule.** Enforce budget, safety and unresolved-evidence limits. Use a separate validation pool for interim stopping if needed; a final test used repeatedly to choose acquisition strategies is no longer untouched. Preserve acquisition and adjudication history for later error analysis.

## Theoretical explanation

Informative labels could distinguish plausible models, while risk-targeted labels could prevent costly identity decisions. These are different mechanisms and neither implies population-representative labels. Deterministic top-ranked acquisition gives other units zero selection support; retrospective weighting cannot recover their outcomes.

IWAL observes unlabeled points from an underlying distribution and queries labels using history-dependent probabilities, then weights queried losses by reciprocal query probabilities.[18] Its safety result assumes bounded loss, a finite hypothesis class and a positive probability floor; its loss-weighting construction has a separate hypothesis-set analysis.[18] A logged conditional query probability in that setting is not automatically a unique pair's inclusion probability after repeated adaptive pool selection. Applying these ideas to ER requires a matching stream/pool design, evidence/label assumptions and variance analysis, not simply attaching inverse uncertainty weights. Unknown selection probabilities, zero support and unknown nonresponse cannot be corrected this way.

## Important variants

- **Uncertainty:** prioritize near-policy-boundary scores or predictive entropy if probabilities are meaningful. An arbitrary additive score's distance from zero is not calibrated uncertainty. Boundary examples can help threshold decisions but omit confident errors.
- **Disagreement:** review competing scorers, retrieval passes or rule/model conflicts. Diverse mechanisms can expose blind spots; models sharing normalization or training labels can agree while wrong. Committee variation is not independent truth.
- **Diversity and scarce-source coverage:** allocate reviews across sources, scripts, missingness patterns and representations before repeatedly choosing similar cases. This tests coverage rather than uncertainty alone. Novel-looking cases may be uninformative outliers; inaccessible sources need evidence acquisition, not forced binary labels.
- **Cluster risk:** prioritize a proposed bridge, competing assignment or large membership change with high potential harm. A bridge joining components of sizes $a$ and $b$ creates $ab$ cross-component co-membership assertions under closure; this derived count is exposure, not expected false merges. The bridge's truth and downstream costs still need evidence. Resolving one edge need not resolve the whole entity.
- **Cost-aware hybrid:** allocate exploration and risk/uncertainty quotas, with cost predictions used transparently. Keep coverage safeguards so expensive-source reviews do not disappear. [Entity-centric search](independent-reference.md) owns expanded membership investigation once required.

## Assumptions and prerequisites

Require authorized reviewer evidence, stable identity rules, a revisable learning pipeline and leakage-safe evaluation separation. Some labels must be learnable by the model's features for generalization to improve; repeated review cannot fix systematically missing features. Account for entity/graph-context leakage and weak-label provenance. Abstention is an allowed output, not a training negative.

## Applicability conditions

Use for learning efficiency or identifying high-impact failure modes when independent measurement is already feasible. Prefer simple uniform acquisition when uncertainty estimates are unreliable, the pool is small, ranking overhead dominates, or costly cases cannot be resolved with available evidence.

## Advantages

Targeting can direct experts toward actionable disagreements and consequences rather than raw pair volume. Logged feedback distinguishes annotation gaps from systematic model errors and makes subsequent acquisition decisions auditable.

## Trade-offs and failure modes

Self-reinforcing feedback can concentrate labels around existing model assumptions. Uncertainty can select irreducible ambiguity; diversity can select isolated noise; cluster risk can overfocus on large entities. Label-count efficiency may disappear after search time, specialist escalation, re-review and retraining overhead. Count unresolved queries and their costs, not only successful annotations. Evaluate whether selective reviewers have higher error rates or shared anchors. These are causal failure hypotheses, not established comparative findings.

## Relationships with other methods

This method addresses [ground-truth acquisition](../../decisions/ground-truth-acquisition.md). Independent review is a complementary evaluation role, not an alternative source of training feedback. [Weak supervision](weak-supervision.md) can supply provisional training labels or query disagreements, but testing on those same generated labels measures imitation. [Threshold abstention](../decision-resolution/thresholds-abstention.md) consumes supported uncertainty and costs; the acquisition ranking itself does not define deployment acceptance.

## How to evaluate

Use [controlled comparison](../experimentation/controlled-comparison.md): uniform versus uncertainty, disagreement, coverage/diversity and cluster-risk arms, with common seed labels, learner, eligibility and independent test reference. Keep test labels inaccessible to query ranking. Compare learning curves at fixed numbers of attempted/resolved labels and separately at fixed total cost, including computation and adjudication. Use [pair evaluation](../../evaluation/pairwise-calibration.md), [final-entity evaluation](../../evaluation/entity-resolution-quality.md) and [incomplete-reference analysis](../../evaluation/incomplete-reference-quality.md). Report source-slice quality, catastrophic-error exposure, abstentions and uncertainty; repeated acquisition seeds do not create new independent test truth. Adopt only for a predeclared practical held-out benefit within cost and harm guardrails; reject deterioration or circular evaluation. Sparse evidence or wide intervals are inconclusive. Discovery yield alone cannot establish population performance.

## Research opportunities

Ablate ranking, diversity and cost components independently. Test whether apparent gains come from broader evidence access rather than smarter selection, and whether avoiding unresolved cases sacrifices scarce-source coverage.

## References and evidence limitations

Source [18], arXiv v4, sections 2–4 and 7, supports its randomized weighting mechanism, bounded-loss guarantees and non-ER classification experiments.[18] It does not establish arbitrary active-query consistency, ER cluster-risk gains or immunity to reviewer error. No ER implementation, training run or measured gain is provided here.

## Sources

[18] https://arxiv.org/abs/0812.4952 — Importance Weighted Active Learning
