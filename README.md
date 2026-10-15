# Entity Resolution Solution Atlas

A project-agnostic, Markdown-first knowledge base for deciding how to design, evaluate and improve Entity Resolution systems. It expands alternatives rather than prescribing one architecture.

**This is not an ER implementation.** There are no matching algorithms, trained models, processed datasets or production application here. Documentation validation tools check the knowledge repository only.

The repository-local normative contract is [SCOPE.md](SCOPE.md), [AGENTS.md](AGENTS.md), [SCHEMA.md](SCHEMA.md) and the [evidence policy](references/evidence-policy.md); no external master instruction is required.

## Start with a question
Start at [START_HERE.md](START_HERE.md): choose one task route, retrieve only what the question needs, and produce a bounded project-specific decision note. [AGENTS.md](AGENTS.md) is the short agent entry point; authoring instructions are in `MAINTAINERS.md`.

## v1.2.1 consumer release and validation

Use `dist/atlas-consumer-wave5/START_HERE.md` for the corrected consumer release;
build/verification commands are in [tools](tools/README.md#consumer-package).
Distribute only `dist/atlas-consumer-wave5/` (or its matching archive), not this
development repository. Its README contains the copy-paste external-agent prompt
and filesystem-access instructions; no harness-specific discovery or tools are required.
`dist/atlas-consumer/` remains the unchanged Wave 3 evaluation input, not the latest
source-bound release. The [Wave 5 final handoff](validation/v1.2.1/wave-5/README.md)
records the temporal cannot-link correction, bounded scientific reviews, actual
validation and remaining runtime/utility blockers. Documentation and synthetic
checks do not establish real-world ER accuracy or measured agent improvement.

## Navigation
| Location | Purpose |
|---|---|
| [Scope](SCOPE.md) | Repository-local purpose, object types, evidence, retrieval and validation contract |
| [Taxonomy](taxonomy/overview.md) | Fourteen coherent knowledge domains and boundaries |
| [L0 catalog](CATALOG.md) / [L1 domain indexes](indexes/domains/) | Generated compact discovery and per-domain comparison navigation |
| `decisions/` | Identity, modularity, candidates, evidence, scoring, resolution/rules, masters, acquisition, experiments, execution and monitoring |
| `solutions/` | Retrieval/evidence/scoring, resolution/rules, lifecycle/masters, reference acquisition, experiments, artifact pipelines, bounded execution and stage monitoring |
| `architectures/` | Six reusable, composable reference patterns |
| `research/hypotheses/` | Untested frequency and contextual-reliability experiments |
| `evaluation/` | Candidate, pairwise/calibration, entity, blind-spot, incomplete-reference, synthetic/metamorphic and complete-output execution/replay evaluation |
| [Guides](guides/project-intake.md) | Intake/integration/task patterns, experiment/run templates, rule/operational/governance witnesses, coverage and review |
| [Selection deep dive](deep-dives/selection-and-calibration.md) / [incomplete-reference estimation](deep-dives/incomplete-reference-estimation.md) | Optional L3 probability, bounds, denominator and variance details |
| `templates/` | The five primary card formats |
| [References](references/bibliography.md) | Verified sources, evidence scope and immutable-input hashes |
| [Agent-utility benchmark](validation/agent-utility/) | Frozen scenarios, rubric, brokered harness and adapter; results are evaluation artifacts, not retrieval knowledge |
| `dev_docs/` | Six historical design discussions, unchanged |
| `tools/` | Optional documentation lint/catalog tooling, not ER code |

## Pilot scope and retrieval layers
The validated v1 pilot contained **21 knowledge objects** (6 architecture cards plus 3 decisions, 7 solutions, 2 hypotheses, 3 evaluations). The v1.1 iteration adds **10 connected cards** across identity semantics (2), resolution policy (4), master construction (2) and ground truth/evaluation (2), for **31 objects**: 6 decisions, 13 solutions, 6 architectures, 2 hypotheses and 4 evaluations. All IDs from v1 are unchanged; generated L0 and 14 L1 indexes replaced the monolithic catalog.

**Current snapshot: v1.2, 57 objects** — 13 decisions, 29 solutions, 6 architectures, 2 hypotheses and 7 evaluations. Wave 1 covers acquisition/incomplete truth/experiments; Wave 2 modularity/rules/artifacts; Wave 3 representations/retrieval/source-aware and richer scoring/graph alternatives; Wave 4 execution, cost/replay, monitoring and bounded operational/governance guidance. Wave 5 adds task-oriented entry, project integration and documentation safeguards without multiplying cards or creating another taxonomy. The [tracker](guides/v1.2-expansion-tracker.md), [final review](guides/v1.2-final-review.md) and [coverage matrix](guides/decision-coverage-matrix.md) distinguish implemented documentation, actual checks and specialist/empirical gaps. Five primary types, fourteen domains and six architecture IDs are unchanged.

For absent/poor labels, start with [acquisition choice](decisions/ground-truth-acquisition.md) and [what incomplete truth can establish](evaluation/incomplete-reference-quality.md). For a controlled change, use [experiment design](decisions/experiment-design.md) and the [plan template](guides/experiment-plan-template.md). [Behavioral tests](guides/er-behavioral-testing.md) help with contract regressions, not real-world accuracy claims. Retrieve only applicable alternatives and optional L3 details.

For a rule-heavy refactor, start with [composition choice](decisions/rule-composition.md), then the relevant ordered/table alternative and [refactor witnesses](guides/rule-policy-refactoring.md). For engineering boundaries, start with [modularity choice](decisions/pipeline-modularity.md); only follow [artifact reuse](solutions/architecture/versioned-artifact-runs.md), the [run manifest](guides/run-manifest-template.md), [stage contracts](taxonomy/module-contracts.md) or [decision provenance](guides/decision-provenance.md) when the actual change needs them. A framework, workflow service and every role as a separate stage are not prerequisites.

For lossy name cleaning, start with [representation choice](decisions/name-representation.md), then the selected [comparator](solutions/comparison-features/string-comparators.md) or [identifier semantics](solutions/comparison-features/identifier-namespaces.md). For blocking, use [candidate choice](decisions/candidate-strategy.md) and the selected [approximate mechanism](solutions/candidate-generation/approximate-blocking.md). For source heterogeneity, compare [pooling](solutions/matching-scoring/source-aware-reliability.md) against a global scorer before considering a [richer model](solutions/matching-scoring/learned-neural-comparators.md). For unexpected giant entities, follow [closure fragility and repair](solutions/decision-resolution/connected-components.md#graph-fragility-selective-verification-and-repair), not a blanket “remove bridges” policy.

For physical capacity, compare [execution placement](decisions/execution-strategy.md) and [complete-output cost](evaluation/execution-cost-replay.md): successful tiles are not proof of required comparison-unit coverage. For source change or alerts, start with [monitoring response](decisions/monitoring-response.md); independent evaluation audits and operational review are different roles. [Operational lifecycle witnesses](guides/incremental-operations.md) and [governance](guides/er-governance.md) bound publication, consumer consistency, external access and restoration authority.

All fourteen domains have maps; important decisions have bounded detailed routes, not complete implementation recipes. Specialist algorithms, full distributed protocols and advanced private/federated guarantees remain explicit gaps. [Reconciliation](guides/design-reconciliation.md) explains draft changes; [opportunities](research/opportunities-index.md) preserves research areas; [coverage](guides/decision-coverage-matrix.md) records per-decision judgments rather than domain-wide certification.

The [three scenario stress tests](guides/scenario-stress-tests.md) are conceptual walkthroughs, **not empirical benchmarks**. The frozen [AU-v1 benchmark](validation/agent-utility/) has 33 validated scored responses about historical v1/v1.1/no-Atlas corpora, with [mixed findings](validation/agent-utility/results/COMPARISON-2026-10-13.md) and disclosed model/transport limits. They are **not results for v1.2**. No new solver/scorer cohort, ER or engineering experiment has run in these expansion waves. Wave 3 review was author-only; Wave 4 received a separate critique with four major/two minor findings and integrating-author correction, but unattested model identity and no independent post-remediation sign-off. The separate [AU-v2 data package](validation/agent-utility-v2/README.md) is frozen and integrity-verified, with eight scenarios and 17 passing package tests. [Offline integration](validation/agent-utility-integration/README.md) implements snapshot/broker/protocol/registration-artifact checks and [mechanical packet/score tools](validation/agent-utility-integration/SCORING.md); process executor/transport, genuine independent evaluator invocation and attested identities remain pending, with zero actual runs/scores. Frozen inputs or passing infrastructure tests are not measured utility. See [final review](guides/v1.2-final-review.md), [scoring checks](validation/v1.2/au-v2-scoring-validation.json) and [remaining work](validation/v1.2/au-v2-remaining-work.md).

## Evidence and contribution rules

The [v1.2+ original-task handover](guides/v1.2-final-delivery.md) brings together
the ten requested deliverables, content-section coverage, review/test evidence,
consumer workflow and technically justified residuals. Actual v1.2 decision-quality
improvement remains unestablished; additional runtime work is not substituted for
the implemented knowledge expansion.

- Follow [SCHEMA.md](SCHEMA.md) and the [evidence policy](references/evidence-policy.md); the [content rubric](guides/content-review-rubric.md) separates substantive review from structural lint.
- Preserve source bytes, stable IDs and one canonical location per object.
- Cite checked literature, specify its context, and label hypotheses/unknowns explicitly.
- Distinguish score semantics, decision actions and entity representations; keep hard prerequisites, compatibility roles, interaction risks and conditional exclusions explicit.
- Maintain the manifests, generated L0/L1 navigation, typed relations and [change log](guides/change-log.md).
- Run documented [repository checks](tools/README.md) and perform conceptual review before declaring coverage complete.

This Atlas is a knowledge resource, not an instruction to change a production system. No reference pattern is universally optimal.
