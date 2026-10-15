---
id: EVAL-11-005
type: evaluation
title: Quality estimation with incomplete reference evidence
domain: "11"
summary: >-
  Decide which accuracy claims incomplete reference evidence can support before
  computing a metric. Separate finite known-positive recovery, probability-sampled
  estimates, complete sampled entities, positive-unlabeled assumptions and proxy
  diagnostics. Specify the pair or entity population, output denominator, unknown
  outcomes, inclusion design and adjudication uncertainty. Conservative bounds and
  sensitivity analyses can be more defensible than a point estimate. Independent
  reference acquisition remains necessary when selection, completeness or label
  reliability cannot identify the intended quality measure.
tags: [evaluation, no-labels, few-labels, uncertainty, human-review, pairwise, clustering, asymmetric-costs]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  tests: [SOL-10-001, SOL-10-002, SOL-10-004]
  complements: [EVAL-11-002, EVAL-11-003]
---

# Quality estimation with incomplete reference evidence

## What is measured

An **evidence-to-estimand contract**, not a replacement for the canonical [pair metrics](pairwise-calibration.md) or [entity metrics](entity-resolution-quality.md). For fixed semantic pairspace $U$, let $Y_i$ be true identity and define $A$ as the system's asserted pairs **intersected with $U$**. For partition output, intersect all induced co-memberships, not only scored edges. Every pair numerator and denominator uses this same scope: precision divides by $|A|$, recall by $\sum_{i\in U}Y_i$. Report forbidden out-of-$U$ assertions separately as contract violations. Complete-partition B-cubed over records is a different estimand.

## Why it matters

A known-positive list can assess recovery of its entries but cannot distinguish unlisted true matches from nonmatches. A candidate-selected list cannot reveal retrieval exclusions. Graph contradictions, size distributions and rule agreement locate risk without identifying population accuracy. No labels therefore means no directly observed accuracy, not permission to rename a diagnostic as precision.

## Definitions and formulas

Choose the narrowest justified route:

| Evidence | Identifiable result under stated assumptions | Unsupported extension |
|---|---|---|
| Convenient known positives | Recovery on that finite list | Population recall or precision |
| Probability-sampled, adjudicated accepted pairs | Precision of frozen $A$ | Recall over excluded/nonasserted pairs |
| Probability sample spanning $U$ | Weighted TP and true-pair totals; ratio recall when estimable | Tight intervals just because weights exist |
| Completely resolved probability-sampled entities | Design-specific membership metrics with necessary predicted intersections | Complete-partition metrics on a clipped labeled subset |
| Partial memberships or selective positive labels | Supported errors/links, bounds or explicit assumption-based sensitivity | Every unknown is negative |
| Synthetic fixtures or graph proxies | Behavior violations and diagnostic yield | Real-world accuracy |

For a fully enumerated finite $U$ with correct known positives $P$, known negatives $N$ and unknown pairs $W$, precision lies between $|A\cap P|/|A|$ and $(|A|-|A\cap N|)/|A|$. This is mathematical worst-case reasoning, not a sampling confidence interval. Unknown pairs inside and outside $A$ affect recall differently; [the L3 derivation](../deep-dives/incomplete-reference-estimation.md) gives recall bounds, sampling totals and sensitivity checks. Empty denominators are undefined.

## Data requirements

Freeze records, semantic eligibility, source/time scope, reference version and output. Preserve selection probabilities, review responses, supported negatives, unresolved outcomes and evidence lineage. [Probability-sampled review](../solutions/ground-truth/probability-sampled-review.md) supplies pair evidence; [entity-centric construction](../solutions/ground-truth/independent-reference.md) supplies searched memberships. State completeness per reviewed entity and keep predicted-cluster members outside labeled truth visible.

## Sampling assumptions

Inverse-probability totals require known positive inclusion probabilities and usable outcomes throughout the target frame; survey estimation separates design weights, nonresponse adjustments and variance.[15] Missing or unresolved review is a second selection process. Do not silently drop it, substitute a model prediction or assume its response propensity equals one. A ratio of estimated totals is generally biased in finite samples; it can be unstable or undefined when positives are scarce. Entity sampling needs induced inclusion probabilities, not arbitrary inverse cluster sizes.

Positive-unlabeled reasoning adds different assumptions. If labeled positives are correct and each positive has constant labeling propensity $c>0$ independent of its features, then $P(L=1\mid X)=cP(Y=1\mid X)$.[17] This does not determine $c$ from an arbitrary positive list. Unknown propensity, source-dependent selection, copied silver labels or absent feature support undermine the correction. Report conditional sensitivity to plausible propensities, not a gold-standard score; fitting a PU model does not validate its assumptions.

## Interpretation

Keep **observed**, **design-estimated**, **assumption-dependent** and **diagnostic-only** results separate. Fully resolved sampled entities can support the entity-centric estimation framework under its design; partial entities cannot simply be treated as complete.[4] Finding one harmful overmerge is established evidence of that error, not its prevalence. Discovering no sampled errors is not proof of zero risk.

## Potential biases

Production-assisted search can hide omissions or anchor reviewers. Rule-derived labels can reward rule imitation. Repeated records and copied evidence can correlate reference errors. Entity-disjoint holdouts reduce leakage but do not repair sampling bias. Source slices with no reviewed support remain unsupported regardless of aggregate sample size.

## Known limitations

Bounds can be uninformative and worst-case label assignments need not respect all identity constraints; valid constraints may tighten them. Weighting cannot fix zero inclusion or unknown label error. Label-error sensitivity, sampling uncertainty and future-source transfer are separate limitations. This protocol produces no ER measurements.

## Recommended comparisons

Compare unchanged rules and a challenger on the same independent reference, frozen outputs and budget. Record known-positive recovery, weighted outcome estimates where defensible, unresolved mass and independent discoveries outside both candidate pools. Adopt only if the predeclared practical benefit and harm limits survive sampling and reference sensitivity. Reject an attributable harmful change; remain inconclusive when admissible unknown outcomes reverse the conclusion. Use [controlled comparison](../solutions/experimentation/controlled-comparison.md) rather than tuning on this final reference.

## Statistical uncertainty

Name the inference: finite-population probability-sampling variance, future-population/model uncertainty, reviewer error, or algorithm randomness. Use actual strata, stages, inclusion probabilities and paired arms. Entity-primary-unit designs need unit-level variance/replicates; arbitrary independent pair bootstrap is not justified for shared-entity superpopulation inference. Conversely, a genuine simple random pair sample permits its design-based variance with fixed outcomes even when pairs share records. Rare-event zero discoveries need a design-specific upper bound, not a zero estimated variance. See the L3 guidance before choosing an interval.

## Related solutions and references

[Targeted active review](../solutions/ground-truth/targeted-active-review.md) and [weak supervision](../solutions/ground-truth/weak-supervision.md) may produce research/training evidence without representative test truth. [Behavioral testing](synthetic-metamorphic.md) remains useful when accuracy is unidentifiable, but answers a different question. Source 17 supports the conditional PU identity, not automatic identifiability or ER performance; source 15 supports survey principles, not the ER-specific acquisition recommendations.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
[17] https://cseweb.ucsd.edu/~elkan/posonly.pdf — Learning Classifiers from Only Positive and Unlabeled Data
