# Project–Atlas integration: a bounded decision note

## Interface and evidence states

Copy this template into the consumer project's own documentation, not into the
Atlas. Populate it from observed implementation and user-provided requirements.
An Atlas example cannot fill a project fact. Use:

- **Known:** inspected code/data contract or provided fact, with provenance and scope.
- **Assumed:** explicit temporary premise, owner and consequence if false.
- **Proposed:** baseline/alternative configuration, not a selected winner.
- **Testable:** defined contrast with accessible evidence, metrics and guardrails.
- **Proven:** only the bounded claim actually supported by completed evidence;
  record population, configuration, uncertainty and what remains unproven.

“Implemented,” “structurally valid” and “proven identity accuracy” are not synonyms.
A method's literature support does not prove that it helps this project.

## Decision note template

### 1. Project question and current behavior

State the consequential output and failure hypothesis. Record current identity
type/time/granularity, eligibility/cardinality, stages and artifacts from actual
implementation. Cite project paths/versions outside this universal repository.
Separate candidate loss, evidence insufficiency, scorer/policy error, global
membership and master-field error. Record errors and costs without inventing rates.

### 2. Known, assumed and unknown

List source namespaces/authority, languages/quality, label acquisition and coverage,
current scores/calibration population, constraints, update/delete semantics,
compute/review budgets, access/retention and downstream consumers. Each uncertainty
has an owner, collection route and stop consequence. Use [intake](project-intake.md)
only for unresolved relevant fields, not as a demand to gather every possible fact.

### 3. Selective Atlas retrieval

Map `project question → relevant Decision ID → baseline/alternative Solution IDs
→ appropriate Evaluation IDs → optional L3`. Start at [L0](../CATALOG.md), use a
relevant [L1](../indexes/domains/) slice if needed, then selected cards. Record why
each is applicable, hard prerequisites, optional context and unsupported specialist
gaps. Use the [task pattern](agent-task-patterns.md) for the current job only.
Do not copy the full corpus or treat shared tags as compatible configurations.

### 4. Candidate configurations and contracts

For each baseline/alternative, describe topology, scoring, resolution and lifecycle
independently. Name affected [stage contracts](../taxonomy/module-contracts.md),
input/output semantics, actual exchanged artifacts, versions and invalidation.
Explain mechanism, prerequisite, cost, causal failure example and safe substitution
boundary. A library or workflow engine is optional unless a real requirement
makes it necessary. Include unchanged components as explicit controls.

### 5. Experiment and implementation boundary

Use the [experiment template](experiment-plan-template.md) and
[realized manifest](run-manifest-template.md). Specify comparator, intervention,
competing explanation, fixed-candidate versus actual-population scope, labels/split,
unit/denominator, uncertainty, practical margins, run order/seeds and unknowns.
Reference behavioral witnesses separately from outcome evidence. Name authorized
files/actions, shadow/provisional publication, consumer consistency, external-call
permissions, erasure and rollback/compensation limits. Do not run a production
change merely because the note can describe it.

### 6. Required tests and stop rules

List stage equivalence, namespace/missing/error cases, policy conflicts, old/new
neighborhoods, global constraints, replay and unauthorized-route tests as applicable.
Outcome tests must match the claimed estimand. No representative labels means
an acquisition/bounds/diagnostic plan, not fabricated precision or recall. Stop on
missing hard semantics/authority, unsafe irreversible effects, unavailable protected
evidence, conflicting mandatory constraints or unverified closure. Record the
smallest reversible action that can resolve the uncertainty.

### 7. Final decision and evidence

Record positive, negative or inconclusive results and authorized next action.
Separate changes applied, tests executed, measured effects, theoretical expectations,
unexecuted work and unresolved concerns. A negative result can favor the baseline;
inconclusive evidence can justify targeted acquisition, not a complex winner.
Published IDs, memberships and master values need distinct acceptance claims.

## Consumer output contract

The deliverable is a bounded project decision/experiment note, followed by actual
implementation only with user authorization. Include the selected Atlas paths/IDs,
not entire copied cards. The Atlas grants no access, production permission or
project identity semantics. [Governance](er-governance.md) constrains evidence use;
content review (source repository only) challenges the recommendation's meaning.
