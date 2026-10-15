# Project intake: facts before methods

Copy these questions into a project-specific note outside the universal Atlas. Mark every answer **observed**, **provided**, **assumed**, or **unknown**; unknown facts must not be filled from a card's example.

| Area | Questions to resolve | Retrieval route |
|---|---|---|
| Identity semantics | Deduplication, linkage or multiple sources? Person, legal organization, address, account or another object? Same-as versus related-to? Can identities/identifiers change or be reused? | [01](../taxonomy/domains/01-problem-identity.md) |
| Output/constraints | Pair links, one-to-one assignment, memberships, virtual/golden entities? Multiple observations per entity/source? Unmatched and uncertain cases allowed? | [08](../taxonomy/domains/08-decision-resolution.md), [09](../taxonomy/domains/09-master-maintenance.md) |
| Sources | Schemas, namespaces, units, locale, timestamp semantics, provenance, source/field quality and observed conflicts? | [03](../taxonomy/domains/03-data-integration.md) |
| Preparation/evidence | Languages/scripts, sparse fields, aliases, normalization loss, shared contact fields, validity flags and relationship context? | [04](../taxonomy/domains/04-normalization-enrichment.md), [comparison decision](../decisions/comparison-evidence.md) |
| Candidate coverage | Current passes, caps, largest blocks, independent known positives outside existing candidates? | [candidate decision](../decisions/candidate-strategy.md) |
| Labels | Training versus evaluation versus diagnostic labels? Sampling/inclusion process, annotation uncertainty, entity/source/time-disjoint split, independent gold? | [10](../taxonomy/domains/10-ground-truth.md) |
| Scoring | Existing rules/features/models, score interpretation, conditioning population, calibration support and source-transfer performance? | [scoring decision](../decisions/scoring-strategy.md) |
| Costs and review | False-link/false-merge versus missed-match harm, downstream cost unit, required operating point, review capacity and correction authority? | [policy](../solutions/decision-resolution/thresholds-abstention.md) |
| Compute/lifecycle | Pair budget, skew, memory/latency/index cost, batch/update cadence, changed/deleted observations and periodic replay? | [13](../taxonomy/domains/13-scalability-execution.md), [AR-06](../architectures/incremental-continuous.md) |
| Access/governance | Permitted evidence, retention, audit/rollback, privacy threat model, reliability across source/population/language segments? | [14](../taxonomy/domains/14-governance-monitoring.md) |

## From intake to an evidence-backed plan
1. Identify the failure level with available evidence; do not blame scoring for missed retrieval or membership propagation.
2. Retrieve only the relevant [catalog](../CATALOG.md) entries; document coverage gaps.
3. Compare a simple baseline and at least one plausible alternative using the [comparison guide](compare-and-experiment.md).
4. Specify a controlled experiment with labels appropriate to its estimand. Scorer comparison can fix candidates; final behavior must still be checked after changed retrieval/policy/resolution.
5. Choose practical success/falsification criteria before the test; missing labels or low power imply an evidence-collection step, not an invented preference.

No task here authorizes a production change. See [AGENTS](../AGENTS.md); the [architecture compositions](../taxonomy/architecture-dimensions.md#example-compositions) are conceptual examples, not measured results or project facts.

Produce a project-local [integration decision note](project-atlas-integration.md), distinguishing Known / Assumed / Proposed / Testable / Proven. Use only the relevant [task pattern](agent-task-patterns.md); do not expand intake into mandatory whole-corpus retrieval.
