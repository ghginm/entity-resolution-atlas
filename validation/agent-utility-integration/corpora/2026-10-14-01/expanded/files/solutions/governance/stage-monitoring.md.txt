---
id: SOL-14-001
type: solution
title: Versioned stage monitoring with independent outcome audits
domain: "14"
summary: >-
  Attach stage- and source-conditioned telemetry to versioned ER runs and route
  anomalies through diagnosis, authorized containment and controlled validation.
  Keep representative outcome acquisition separate from targeted incident review.
  Requires stable denominators, missing-telemetry states and response ownership;
  score shift or graph growth cannot certify accuracy loss, and fewer alerts
  cannot certify improvement. Combine source onboarding, compatibility checks
  and delayed-review accounting with independent quality evidence.
tags: [entity-agnostic, monitoring, source-aware, calibration, missingness, governance, human-review, provenance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  addresses: [DEC-14-001]
  complements: [SOL-10-002, SOL-10-003, SOL-02-002]
  evaluated_by: [EVAL-11-005, EVAL-11-003, EVAL-11-006]
---

# Versioned stage monitoring with independent outcome audits

## Short summary

Bind operational signals to versions, populations and actions. Independent audit
estimates and targeted investigations remain separately reported. This is a
conceptual ER control loop; no service, dashboard or production alert is deployed.

## Problem addressed

A dashboard without denominators cannot distinguish dropped ingestion from better
matching. An alert-driven review queue can preferentially find errors and then
misrepresent them as a population rate. Automated threshold tuning can restore
a target merge count without repairing a broken normalizer.

## Core mechanism

For each run/window, record source/schema and pipeline versions, eligibility and
completion states; emit counters/profiles at relevant stage boundaries. Compare
like versions and population slices, annotate deliberate changes, and retain
missing telemetry as unknown. Route anomalies to an owner with a diagnosis,
authorized action and validation obligation. Maintain an independent sampling
stream beside alert-targeted research.

| Boundary | Example signal and denominator | Diagnostic question |
|---|---|---|
| Ingestion/evidence | Present/invalid field among expected observed records; lag among accepted changes | Schema, authority, source coverage or missing telemetry? |
| Retrieval | Unique candidate degree among eligible observations; truncated records among queried records | Key collapse, hot blocks, index/version failure or population change? |
| Scoring/calibration | Score profile among completed candidates by route/source/model | Feature shift, context prevalence or changed candidate selection? |
| Policy/review | Each rule hit/abstention among eligible decisions; pending/unresolved among submitted reviews | Shadowed override, new missing values, reviewer delay or workload? |
| Resolution/master | Component tails, merges/splits among affected entities; stale fields among published views | Bridge contamination, intended correction, closure or consumer inconsistency? |

Accepted-change lag and queried-record truncation are conditional diagnostics.
Pair them with an independently defined expected source/input/change frame and
eligible query frame: report unaccepted, unqueried, failed and unknown work.
Use an authorized source snapshot, sequence contract or independent intake manifest
where available; a worker's successful-output list cannot define expected coverage.
If the expected frame is unavailable, completeness is unidentifiable, not healthy.

Profiles with no eligible denominator are undefined, not zero. Graph growth and
contradictions identify investigation targets; dense wrong clusters and consistent
wrong constraints can evade them. Review outcomes describe submitted cases unless
a valid independent design supports broader estimates.

## Theoretical explanation

Conditioning on source, route and version reduces composition confounding; it
does not establish causality. For example, increased sparse-source share can alter
a pooled missingness rate even when each source's rate is unchanged. A controlled
replay or ablation separates processing changes from population changes more
reliably than comparing two unmatched dashboard windows. Static tests and live
monitoring have different information roles in changing ML systems.[43]

## Important variants

Simple counters plus scheduled audits are a credible baseline. Profile alerts
add operational localization; shadow/canary comparisons can test bounded behavior
without unapproved identity publication. Learned drift detectors add fitting and
threshold validation; they are not required here. Calibrated pair estimates,
entity harm and operational health require different evidence.

## Assumptions and prerequisites

Need stage contracts, explicit version boundaries, stable source keys, lawful
telemetry and response ownership. Audit labels need independent sampling support
and appropriate as-of semantics; reviewer nonresponse remains unknown. Keep
[targeted review](../ground-truth/targeted-active-review.md) separate from the
[independent audit](../ground-truth/probability-sampled-review.md). Retain cohort
entry, due/outcome time and unresolved counts so delayed feedback is not silently
excluded. Derived metrics and logs can themselves expose sensitive entities.

## Applicability conditions

Useful for changing sources, hybrid policies and incremental maintenance. During
onboarding, test namespaces, units, validity and copied evidence; run shadow
candidate/pair/entity contrasts on old and new source slices. A source-conditioned
model can have an unsupported new-source slice even when global profiles look
familiar. Preserve an explicit unknown-source fallback and review capacity.

## Advantages

Versioned signals can localize a likely failing boundary, while separate audits
support bounded outcome claims. Traceable action records distinguish containment
from validated repair. No reduction in harm or alert volume is established here.

## Trade-offs and failure modes

Many correlated alerts create workload and false discovery concerns. Freeze
reference regimes and practical thresholds with owners; test benign shifts and
seasonality as well as incidents. Automatically normalizing every new window can
hide drift. Incident reviews can leak into training or final tests. Errors in
instrumentation can imitate model change. A silent missing metric is not healthy.

Do not automatically retrain or recalibrate. Repair ingestion/index/schema faults
first; recalibration needs representative score/outcome evidence, while retraining
changes discrimination and requires its own evaluation. Threshold changes alter
edge admission and can amplify graph effects. Suspension, rollback or queued
publication must respect current access, consumer safety and authorization.

## Relationships with other methods

[Artifact runs](../architecture/versioned-artifact-runs.md) provide realized
versions; [source-aware scoring](../matching-scoring/source-aware-reliability.md)
provides context hypotheses; [AR-06](../../architectures/incremental-continuous.md)
provides repair/consumer boundaries. The [governance guide](../../guides/er-governance.md)
bounds collection, disclosure and restoration authority.

## How to evaluate

Specify incident classes and injection eligibility under
[EVAL-11-006](../../evaluation/synthetic-metamorphic.md). Measure detection delay
from an independently recorded eligible breach/injection time and a declared
observation deadline, not from when the monitored system finally notices it.
Report never-detected incidents and observation loss separately, retaining them
in eligible denominators; latency among detected incidents is a conditional
statistic, not the whole incident-suite result. Include false alarms on declared
benign cases, containment delay and review burden, including broken telemetry.
This establishes suite behavior only. For actual quality use
[EVAL-11-005](../../evaluation/incomplete-reference-quality.md) and
[EVAL-11-003](../../evaluation/entity-resolution-quality.md), preserving source/time
populations, unknown labels and dependence-aware uncertainty.

Compare scheduled-operational-audit baseline, telemetry-only and combined designs
with a common independent **evaluation audit** and matched held-out incident
exposure. Freeze evaluation selection/adjudication independently of alerts and
remediation; withhold its findings from operational arms until their assessed
response is complete. Operational audits and targeted investigations are arm
interventions: telemetry-only does not receive a scheduled operational audit.
Predeclare either matched total operational resources or incremental benefit/cost;
report staffing and review consumption separately. Keep tuning incidents distinct
from held-out assessment incidents. Adopt when practical response benefits
and outcome guardrails justify costs; reject unsafe automated changes or loss of
audit independence. Unresolved outcomes or unrepresentative incident exposure
make population benefit inconclusive. Retain negative and mixed findings.

## Research opportunities

Does stage conditioning improve useful diagnosis rather than just reduce alerts?
Compare diagnosis/action accuracy and time against equivalent raw counters; hold
incident mix and review resources fixed to distinguish better localization from
more staff or easier cases.

## References and evidence limitations

[43] motivates system monitoring, not the ER signal table or an estimator.
[NIST AI RMF 1.0](../../decisions/monitoring-response.md) provides risk-governance
context. All operational designs here require project trials and authorization.

## Sources

[43] https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf — Hidden Technical Debt in Machine Learning Systems
