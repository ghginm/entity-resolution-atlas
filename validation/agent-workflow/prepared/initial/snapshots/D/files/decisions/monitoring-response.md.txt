---
id: DEC-14-001
type: decision
title: Operational monitoring, independent audits and response
domain: "14"
summary: >-
  Choose how ER operational signals, independent outcome audits and response
  authority work together as sources and versions change. Compare periodic
  audits, stage-profile alerts and combined monitoring rather than treating
  drift as measured accuracy loss. Requires eligible-population denominators,
  pinned reference regimes and assigned incident owners. Targeted review can
  discover failures but cannot alone estimate population quality; recalibration,
  retraining, retrieval repair and suspension answer different diagnoses.
tags: [entity-agnostic, monitoring, source-aware, missingness, calibration, uncertainty, human-review, governance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [DEC-10-001, DEC-12-001]
  evaluated_by: [EVAL-11-005, EVAL-11-003, EVAL-11-006]
---

# Operational monitoring, independent audits and response

## Decision question

Which changes should trigger investigation, independent review, remediation or
suspension, and who may authorize each action? Distinguish instrumentation from
quality estimation and response policy from model selection.

## Problem context

A source changes its schema, missingness or population; candidate yield declines;
a new rule changes score admission; components grow after an onboarding. Any of
these can indicate harm, intended behavior, changing workload or an instrumentation
error. An unchanged aggregate score histogram can also hide severe degradation in
a small source slice. Neither alarms nor quiet dashboards establish identity truth.

General ML systems research discusses changing upstream producers, fixed
thresholds and monitoring beyond static tests.[43] NIST AI RMF 1.0's MEASURE
function separates documented evaluation conditions, production behavior
monitoring and tracking risks that are difficult to measure.[44] Neither source
supplies an ER-specific accuracy estimator or automatic response rule.

## Relevant assumptions

Name the eligible source/time population, actual candidates and decision outputs,
measurement window, version regime and owner. Define whether missingness means
absent, invalid or failed ingestion. Review delay changes when an outcome becomes
observable. Ground-truth corrections need as-of interpretation. Monitoring can be
label-free; calibration/accuracy claims cannot be manufactured from score changes.

## Available solution families

- **Periodic independent audit baseline:** review a declared probability or
  entity-centric sample on a fixed schedule; record unresolved outcomes. This
  supports stated quality estimands but can detect fast incidents late.
- **Stage-profile monitoring:** inspect inputs, candidates, scores, policy hits,
  graph/membership and master views with versioned denominators. It localizes
  possible faults rapidly but remains diagnostic without outcome evidence.
- **Combined design:** retain independent audits and add targeted incident/risk
  investigation; preserve the independent sample even when alerts change research
  allocation. [SOL-14-001](../solutions/governance/stage-monitoring.md) describes
  this separation and the action loop.

## Criteria for choosing

Consider irreversible downstream harm, update cadence, review latency, source
scarcity, staffing and the cost of false alarms versus missed incidents. A high-risk
identity action may require a hold until authorized adjudication; an aggregate
operational alert might only warrant investigation. Project-defined action limits
must have a safe fallback, not simply drop suspect inputs and report better quality.

## Trade-off comparison

| Design | Information gained | Limitation |
|---|---|---|
| Independent scheduled audit | Defined outcome estimands with suitable labels/design | Cost; delay; rare failures need deliberate design |
| Unlabeled profiles | Stage-specific change and workload evidence | Stable profiles can conceal errors; shift may be benign |
| Targeted review | Examples and causal clues for failure research | Selection bias; cannot substitute for independent audit |
| Combined monitoring | Faster hypotheses plus separately estimated outcomes | More lineage, response and sample-management effort |

Compare source-conditioned profiles before interpreting aggregate drift. A pooled
candidate-rate change can reflect source composition rather than worse retrieval
within each source. Conversely, stable aggregate rates can conceal offsetting
slice changes. Record raw denominators and conditional rates, not only normalized
plots. No universal drift score or alarm threshold follows from this Atlas.

## Good baseline candidates

Start with version/ingestion completeness checks, a few stage counters and a
scheduled independent sample matched to the consequential output. Keep existing
thresholds as a bounded shadow comparator where admissible. Add more alerts only
when each has a plausible incident, owner, observable denominator and tested response.

## Prerequisites

Need lawful instrumentation and review access, known version boundaries, stable
slice definitions, declared intervals and an accountable incident owner. Quality
estimation additionally needs the acquisition and identifiability conditions in
[EVAL-11-005](../evaluation/incomplete-reference-quality.md). Source onboarding
requires namespace, semantic, authority and compatibility checks before comparing
old and new populations; unobserved slices remain unsupported.

## Open questions

Does an alert originate in ingestion, retrieval eligibility, scoring, calibration,
policy or global resolution? Can delayed reviewer feedback support the intended
current-population claim? Would changing a threshold hide the incident while
leaving its mechanism intact? Are missing alerts evidence of healthy outcomes or
of missing telemetry?

## Related evaluations

Use [independent incomplete-reference evaluation](../evaluation/incomplete-reference-quality.md)
and [final-entity quality](../evaluation/entity-resolution-quality.md) for outcomes;
[behavioral tests](../evaluation/synthetic-metamorphic.md) for detection/response
witnesses. Evaluate monitoring itself with injected incidents, benign changes,
alert delay, unobserved failures and review burden. These measure the selected
incident suite, not population ER accuracy. Adopt a monitoring design when its
operational detection/response benefit and outcome safeguards justify its cost.
Reject unsafe escalation or audit displacement; inconclusive labels limit quality
claims, not the need to investigate a demonstrated contract breach.

## Links to Solution Cards

[Stage monitoring with independent audits](../solutions/governance/stage-monitoring.md),
[probability-sampled review](../solutions/ground-truth/probability-sampled-review.md)
and [targeted active review](../solutions/ground-truth/targeted-active-review.md)
have complementary roles, not interchangeable denominators.

## Sources

[43] https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf — Hidden Technical Debt in Machine Learning Systems
[44] https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf — NIST AI Risk Management Framework (AI RMF 1.0, January 2023)
