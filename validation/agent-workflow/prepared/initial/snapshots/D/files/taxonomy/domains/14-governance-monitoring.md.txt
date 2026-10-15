# 14 — Explainability, Governance & Monitoring

**Design question:** How can users understand, audit, correct and monitor identity decisions safely?

## Decisions and coverage
- Match explanations and evidence-level contributions need input/normalization/candidate/model/policy versions; feature attribution is not causal proof.
- Decision audit trails, human review/adjudication, correction/rollback and operational approval controls preserve accountable changes.
- Quality/drift monitoring, source coverage and model lifecycle distinguish covariate/prevalence/calibration changes; label-based monitoring samples must include routes not selected for review.
- Data access/privacy, privacy-preserving record linkage and reliability across population/language/source segments constrain every earlier component. Specify threat model before choosing encodings or federated execution.

## Solution families and useful baselines
- Versioned evidence/decision traces and reversible membership change records; sampled quality monitoring with explicit escalation.
- Review queues, shadow comparisons, release/rollback gates and threat-model-specific protected linkage designs.

## Ownership and limitations
Privacy is not assured by ordinary hashing. Detailed PPRL/security guarantees remain a research gap in this pilot; do not deploy a protective design from a taxonomy mention.

The [monitoring decision](../../decisions/monitoring-response.md) and [stage-monitoring solution](../../solutions/governance/stage-monitoring.md) connect source/route/version diagnostics with separately independent outcome audits and authorized response. The [governance guide](../../guides/er-governance.md) compares local/minimized/external routes, data/derived-artifact exposure and correction/retention authority. The [decision-provenance guide](../../guides/decision-provenance.md) connects the explanation chain; [run manifests](../../guides/run-manifest-template.md) record versions. Explanation, drift and quiet alerts are not accuracy or privacy assurance. Deep cryptographic/federated guarantees remain deferred in the tracker (source repository only).

This is a domain map, not complete L2 method coverage. Mature names are not automatic recommendations.

## Cross-domain dependencies
- [03 — Data Understanding & Integration](03-data-integration.md).
- [08 — Decision Policies & Entity Resolution](08-decision-resolution.md).
- [09 — Master Entity Construction & Maintenance](09-master-maintenance.md).
- [10 — Ground Truth & Labeling](10-ground-truth.md).
- [13 — Scalability & Execution](13-scalability-execution.md).

## Selective retrieval
Start from the [catalog](../../CATALOG.md) and [project intake](../../guides/project-intake.md). Compare applicable pilot cards before assuming a family is suitable.
