---
id: DEC-10-001
type: decision
title: Ground-truth acquisition for learning and independent evaluation
domain: "10"
summary: >-
  Choose which records, pairs or entities to investigate, separating informative
  training acquisition from evidence supporting population quality claims.
  Compare probability and stratified review, entity-centric reference construction,
  targeted active review, and weak or silver labeling with human adjudication.
  The choice depends on the annotation unit, accessible frame, identity semantics,
  reference completeness and review costs. A hybrid reserves an independent
  evaluation pool while targeting the learning budget; neither random splitting
  nor probability weighting repairs unknown response mechanisms or absent support.
tags: [entity-agnostic, no-labels, few-labels, human-review, provenance, uncertainty, evaluation, experimentation, governance]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  evaluated_by: [EVAL-11-002, EVAL-11-003, EVAL-11-005]
  complements: [DEC-12-001]
---

# Ground-truth acquisition for learning and independent evaluation

## Decision question

Which units should receive which kind of annotation, under what selection design, to support learning, diagnosis and an independently defensible quality claim within the available budget?

## Problem context

Label volume is not the objective. Informative difficult examples can help discriminate models without estimating deployment prevalence. Conversely, a defensible probability sample may spend much of its budget confirming easy negatives. Distinguish the desired artifact: pair dispositions, accepted-link audit, fully resolved entities, or imperfect training signals. A predicted cluster is a review aid, not a true-entity sampling frame. The acquisition design supplies evidence; domain 11 owns its estimators and domain 12 owns controlled comparisons.

## Relevant assumptions

Declare the eligible population and snapshot before sampling: candidate pairs, the entire eligible pairspace, records, or independently enumerated entities. Specify same-identity rules, time scope, source namespaces, permitted evidence and the review unit. Sampling a record and then resolving its entity does not sample entities uniformly. Entity-centric labeling can connect sampled complete memberships to population performance estimation, but requires its actual sampling design.[4]

Keep three questions separate: can a unit be selected, can its identity be resolved, and can its label be used without leakage? Probability sampling requires known positive inclusion probabilities on the population claimed; nonresponse introduces an additional problem.[15] A random train/test split of selectively acquired labels preserves that selection, rather than creating population support. Independent adjudication does not by itself establish representativeness.

## Available solution families

- **Probability and stratified pair review:** select randomly within a declared frame, optionally enriching source pairs, score ranges or outside-candidate regions. Preserve a residual stratum. Supports design-based audit questions without requiring complete entity search; rare positives and expensive adjudication can limit precision.
- **Entity-centric review:** sample records or independently framed entities, then search for complete memberships. Prefer when undermerges, contaminating members or entity-balanced quality matter. Its expense and completeness risk differ from pair review; keep search mechanics in [SOL-10-001](../solutions/ground-truth/independent-reference.md).
- **Targeted active review:** prioritize uncertainty, model disagreement, diversity or downstream cluster risk for learning and diagnosis. These are distinct objectives: informative boundary pairs need not expose confidently wrong bridges. Acquisition yield cannot substitute for independent test quality.
- **Weak or silver supervision:** rules, external mappings and model-generated labels supply training signals with imperfect coverage and possible correlated errors. [SOL-10-004](../solutions/ground-truth/weak-supervision.md) owns their construction and assumptions. Human review can audit and correct them, but auditing only rule agreement is circular.
- **Hybrid:** reserve independent evaluation and quality-control capacity; spend a separate learning pool on active queries, weak-label disputes and scarce-source evidence. Pool proportions are project choices, not universal recommendations.

## Criteria for choosing

Start with the estimand and required label completeness. Precision among accepted pairs needs a different frame from recall over missed identities; entity quality needs membership evidence that isolated pair judgments may not provide. Check frame coverage and permissions before optimization. If evidence cannot resolve a source slice, more selection effort alone is insufficient: seek authorized evidence, retain unknowns, or restrict the claim explicitly.

Next compare expected information per unit cost, including query construction, specialist time, second review, adjudication and entity search. Distinguish a fixed count of labels from a fixed labor/cost budget. An entity annotation and an easy pair judgment are not interchangeable budget units. Protect coverage of costly, scarce or high-harm slices instead of letting a cheap-label objective exclude them.

## Trade-off comparison

Uniform random pair review is transparent but can be inefficient for rare missed matches. Stratification can improve precision or ensure subgroup allocation when auxiliary variables are useful, but does not universally reduce variance for every outcome.[15] Entity search obtains richer membership evidence but risks falsely declaring a partial entity complete. Active selection may reveal useful failures while missing shared model blind spots; silver labels can expand training coverage while reproducing their labeler's assumptions. None is universally superior.

Treat sampling, annotation error and missing evidence separately. Do not apply inverse-probability corrections where probabilities are unknown or zero, and do not equate a known sampling probability with a known chance of successful annotation. Repeated agreement is weaker evidence when reviewers share tools or anchors.

## Good baseline candidates

Use a frozen probability review pool with written identity rules, explicit unknown labels and a second-review subsample. Add a separately partitioned uniform-random learning arm as the credible comparator for active acquisition. For entity-output claims, compare with independently seeded entity review rather than pretending pair labels establish complete truth. Preserve the same evidence access and downstream learner when comparing acquisition strategies.

## Prerequisites

Require an auditable frame or reproducible pair sampler, selection logs, label provenance, review permissions, budget accounting and leakage-safe pool assignment. Choose strata from information available before final annotation. Keep calibration and final evaluation outside training feedback; audit shared-entity and graph-context leakage, not just repeated pair IDs.

## Open questions

Which source slices lack evidence rather than labels? What cost of false completeness is tolerable? Are disagreements resolvable or semantic? Which acquisition objective changes the downstream decision? Predeclare these questions before judging a high positive-discovery rate as success.

## Related evaluations

Use [pair evaluation](../evaluation/pairwise-calibration.md), [entity evaluation](../evaluation/entity-resolution-quality.md) and [incomplete-reference quality](../evaluation/incomplete-reference-quality.md) for their distinct outputs and uncertainty requirements. Pair the decision with [experiment design](experiment-design.md) and a [controlled comparison](../solutions/experimentation/controlled-comparison.md). Adopt a richer design only if it meets predeclared decision-precision or held-out quality goals within cost and harm limits; reject it for leakage, unsupported strata or material reference error. Wide uncertainty is inconclusive, not evidence of equivalence.

## Links to Solution Cards

- [SOL-10-001: independent entity-centric reference](../solutions/ground-truth/independent-reference.md).
- [SOL-10-002: probability-sampled review and hybrid pools](../solutions/ground-truth/probability-sampled-review.md).
- [SOL-10-003: targeted active review](../solutions/ground-truth/targeted-active-review.md).
- [SOL-10-004: weak supervision](../solutions/ground-truth/weak-supervision.md).

Statistics Canada's manual, selected sections of chapters 6–7, supports survey-design distinctions; Binette and colleagues, sections 3.2–3.4, support entity-centric acquisition and estimation.[15][4] The hybrid allocation and safeguards here are Atlas protocol recommendations, not measured ER improvements.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
