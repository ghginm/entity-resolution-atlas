# Taxonomy and decision space

**Problem → Decision → Alternatives → Trade-offs → Evaluation → Research.**
These fourteen domains are knowledge responsibilities, not fourteen mandatory pipeline stages. Domains 01–09 describe core ER decisions; 10–12 own research/evaluation; 13–14 own system-level constraints. Scoring and clustering are not interchangeable terms. Related-to edges do not establish same-as membership.

| Domain | Responsibility | Main question |
|---|---|---|
| [01](domains/01-problem-identity.md) | Problem Formulation & Identity Semantics | What does one entity mean, and what output constitutes a correct resolution? |
| [02](domains/02-architecture-orchestration.md) | Pipeline Architecture & Orchestration | How should components interact, route work and revise decisions? |
| [03](domains/03-data-integration.md) | Data Understanding & Integration | Which observations are semantically comparable and sufficiently reliable to use? |
| [04](domains/04-normalization-enrichment.md) | Normalization & Enrichment | Which transformations make values comparable without erasing identity evidence? |
| [05](domains/05-candidate-retrieval.md) | Candidate Generation & Retrieval | Which pairs merit scoring under a candidate budget, and which true matches could be missed? |
| [06](domains/06-comparison-evidence.md) | Comparison Features & Evidence Engineering | What similarities, contradictions and contextual observations should a scorer see? |
| [07](domains/07-matching-scoring.md) | Matching & Scoring | How should evidence be aggregated into a score whose interpretation is clear? |
| [08](domains/08-decision-resolution.md) | Decision Policies & Entity Resolution | When should a score trigger a link, abstention, assignment or entity-membership change? |
| [09](domains/09-master-maintenance.md) | Master Entity Construction & Maintenance | How should resolved entities be represented, updated and corrected without hiding evidence? |
| [10](domains/10-ground-truth.md) | Ground Truth & Labeling | What labeled evidence supports training, evaluation and diagnosis for the actual target population? |
| [11](domains/11-evaluation-diagnostics.md) | Evaluation & Diagnostics | Which measurements reveal local quality, final identity quality and the cost of errors? |
| [12](domains/12-experimentation.md) | Experimentation & Research Methods | Which controlled test would distinguish mechanisms and reduce decision uncertainty? |
| [13](domains/13-scalability-execution.md) | Scalability & Execution | How can a logically valid ER design fit resource and update constraints without concealing quality loss? |
| [14](domains/14-governance-monitoring.md) | Explainability, Governance & Monitoring | How can users understand, audit, correct and monitor identity decisions safely? |

## Boundaries that prevent duplicate knowledge
- Source profiling: **03**; quality-aware evidence: **06**; learned weighting: **07**.
- Single-record transformations: **04**; pair comparisons: **06**.
- Retrieval logic: **05**; physical execution/index maintenance: **13**.
- Score interpretation/calibration: **07**; score-dependent actions and membership: **08**; consumer entity construction: **09**.
- Label construction: **10**; measurements: **11**; experiment procedures: **12**.
- Lifecycle/topology: **02** with resource details in **13** and identity-state consequences in **09**.

## Cross-cutting dependencies
Normalization changes retrieval keys and evidence. Retrieval changes the score/calibration population. Scoring quality does not guarantee entity-quality improvement. Membership decisions affect master attributes and future graph features, which can feed errors back into matching. Privacy constraints can remove otherwise available evidence. Labeling, monitoring and experiments must evaluate these interactions rather than attributing all errors to a matcher.

See [independent architecture dimensions](architecture-dimensions.md), [conceptual contracts](module-contracts.md), [catalog](../CATALOG.md), and [reconciliation](../guides/design-reconciliation.md). Pilot method coverage is deliberately narrower than this taxonomy; the [expansion plan](../guides/expansion-plan.md) records the gap.
