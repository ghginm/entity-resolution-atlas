# Start here: one project question

The Atlas is project-agnostic ER knowledge, not an implementation or production authorization. Project facts and user permissions govern action. [Scope](SCOPE.md), [agent instructions](AGENTS.md), [schema](SCHEMA.md) and [evidence policy](references/evidence-policy.md) remain normative; historical drafts add no requirements.

## Choose one task

- [Improve scoring](indexes/tasks/scoring.md)
- [Diagnose graph merges](indexes/tasks/graph.md)
- [Improve blocking](indexes/tasks/blocking.md)
- [Work without reliable labels](indexes/tasks/no-labels.md)
- [Refactor rules](indexes/tasks/rules.md)
- [Design a controlled experiment](indexes/tasks/experiments.md)
- [Onboard a source](indexes/tasks/new-source.md)
- [Handle incremental updates/deletion](indexes/tasks/incremental.md)

## Retrieve only what changes the decision

First inspect the project's requirements **and current implementation**. Use [intake](guides/project-intake.md) only for unresolved relevant facts: identity semantics, namespaces, labels, time, error costs, access, compute and downstream constraints. Distinguish candidate loss, insufficient evidence, scorer/policy errors, membership errors and master-field errors.

Use a **500–1000 token soft discovery budget** for navigation, not a cap on necessary evidence or full cards. A task route can lead directly to cards; do not read every layer mechanically:

- **L0:** search the relevant [catalog](CATALOG.md) slice for IDs/questions/tags.
- **L1:** use only applicable [domain indexes](indexes/domains/) to compare choices.
- **L2:** read selected Decision, Solution, Architecture, Hypothesis and Evaluation Cards. An initial **2–4 cards is illustrative**, not a minimum or ceiling; follow prerequisites, alternatives and evaluation links as needed.
- **L3:** open [deep dives](deep-dives/) or references only for an unresolved technical question.

Stop discovery when you can identify the relevant decision, credible baseline, applicable alternative, prerequisites and evaluation route. Stop expanding when another document would not change the recommendation, test or explicit uncertainty. If coverage is absent, report the gap rather than inventing a method.

## Deliver a bounded decision note

Use the [integration template](guides/project-atlas-integration.md), outside the Atlas. Include:

- **Known → Assumed → Proposed → Testable → Proven**, separating facts, unknowns and evidence states. “Proven” means only a bounded claim supported by completed evidence, never literature transfer or structural validity.
- Selected paths/IDs and relevance; baseline versus at least one alternative, mechanisms, prerequisites, costs and failure modes.
- Independent topology/scoring/resolution/lifecycle choices and affected contracts.
- Comparator, controls, labels/split, metrics, uncertainty, success/falsification criteria, guardrails and next decisions for positive, negative or inconclusive evidence.

Do not invent facts/results or prefer complexity by default. Scores are not automatically probabilities; pair confidence is not cluster confidence; missing edges are not negatives. Candidate changes may invalidate calibration. Evaluate relevant slices and entities. **Stop action** on missing hard semantics/authority, conflicting mandatory constraints, unavailable protected evidence, unverified closure or unresolved high-harm/irreversible effects. Report the blocker and smallest authorized reversible evidence-collection step instead.
