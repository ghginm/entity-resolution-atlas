# Agent task patterns: retrieve one job, not the whole Atlas

Use this guide as a small operational entry point, not another taxonomy, search
engine or mandatory reading list. Each pattern starts at a canonical decision or
existing owner. Retrieve the baseline, plausible alternative and matching evaluation
only after inspecting the consumer project's facts. The expected output follows
[project integration](project-atlas-integration.md); all production permissions
remain external. Minimum context means an entry point, not enough by itself to
certify a recommendation.

## Matching improvement without reliable labels

- **Minimum retrieval:** [acquisition decision](../decisions/ground-truth-acquisition.md)
  and [incomplete-reference evaluation](../evaluation/incomplete-reference-quality.md).
- **Essential facts:** annotation unit, eligible universe, candidate selection,
  available positive/negative/partial truth, response/inclusion process, harm and
  review budget. Do not infer recall from candidate-only references.
- **Choices/checks:** independent probability/entity audit baseline versus targeted
  active/weak acquisition; preserve independent test evidence and unknown labels.
- **Output:** acquisition + identifiable-estimand experiment, with denominators,
  uncertainty and costs. **Stop:** unknown inclusion, zero support or unavailable
  semantic truth blocks the claimed population estimate, not all diagnostics.

## New method or feature selection

- **Minimum retrieval:** decision for the affected stage: [evidence](../decisions/comparison-evidence.md),
  [representation](../decisions/name-representation.md) or [scoring](../decisions/scoring-strategy.md),
  then only selected alternatives and evaluations.
- **Essential facts:** current implementation, target error process, field validity,
  languages, independent labels, compute/access and calibration scope.
- **Choices/checks:** preserve a simple exact/interpretable baseline; contrast the
  new representation/feature/model with unchanged candidates and downstream policy,
  then check integrated effects separately. More capacity is not itself evidence.
- **Output:** mechanism-based controlled change note. **Stop:** unavailable authority,
  absent prerequisites or evaluation incapable of distinguishing mechanisms.

## Architecture review and modularity

- **Minimum retrieval:** [modularity](../decisions/pipeline-modularity.md) and the
  affected [module contracts](../taxonomy/module-contracts.md), not all architectures.
- **Essential facts:** actual extension tasks, state/global dependencies, existing
  interfaces, team/runtime constraints and migration costs.
- **Choices/checks:** explicit linear baseline versus hooks/strategy/configuration/
  DAG only where needed. Separate topology, scoring, resolution and lifecycle;
  inspect substitution, error propagation and realized artifact invalidation.
- **Output:** bounded architecture comparison and migration/equivalence plan.
  **Stop:** abstract reuse claims without concrete change tasks or unsafe boundaries.

## Rule-heavy refactoring and conflicts

- **Minimum retrieval:** [composition decision](../decisions/rule-composition.md)
  and [refactor witnesses](rule-policy-refactoring.md); ordered/table details only
  for the selected alternative.
- **Essential facts:** precedence, overrides, default/unknown/error behavior,
  mandatory guards, effects, source exceptions and rule versions.
- **Choices/checks:** explicit ladder baseline versus parameterized predicates,
  ordered policy or table. Inspect shadowing, conflicting hits and required unknown
  guards. Behavioral agreement is rule imitation, not correct identity.
- **Output:** semantic mapping, traces, conditional regression suite and staged
  migration. **Stop:** unresolved mandatory conflict, changed effects or missing oracle.

## Large components and graph-level identity errors

- **Minimum retrieval:** [resolution choice](../decisions/resolution-strategy.md)
  and [closure/fragility](../solutions/decision-resolution/connected-components.md).
- **Essential facts:** strict identity versus typed relations, edge provenance,
  admission semantics, constraints, competitor scope and downstream consequences.
- **Choices/checks:** connected-components baseline versus edge filtering/selective
  verification (change admitted edges) or constrained clustering (change membership
  using audited whole-union restrictions). Hold records/candidates/scores fixed and
  vary admission separately from membership. A true chain may have bridges; smaller components
  and fewer contradictions are not truth. Repair materialized memberships and fields.
- **Output:** contamination hypothesis, independent adjudication and reversible repair
  plan. **Stop:** topology-only certainty, unjustified must-links or irreversible harm.

## Blocking comparison and performance investigation

- **Minimum retrieval:** [candidate choice](../decisions/candidate-strategy.md);
  [execution choice](../decisions/execution-strategy.md) only for physical cost.
- **Essential facts:** eligible pair universe, actual passes/caps/indexes, block/degree
  tails, feature cost, memory and independent positives outside old candidates.
- **Choices/checks:** exact/multi-pass baseline versus selected approximation; or
  equivalent local/batched/partitioned work. Keep candidate change separate from
  placement, profile build/update/retention and whole-output completion.
- **Output:** recall–cost frontier or equivalent-output execution comparison using
  [EVAL-11-007](../evaluation/execution-cost-replay.md) plus candidate/entity evaluation.
  **Stop:** lost pairs disguised as faster execution or unsupported outside-C recall.

## ML or statistical experimentation

- **Minimum retrieval:** [experiment decision](../decisions/experiment-design.md)
  plus the selected [scoring family](../decisions/scoring-strategy.md).
  For reproducibility specifically, start instead at [artifact runs](../solutions/architecture/versioned-artifact-runs.md)
  and the [realized manifest](run-manifest-template.md); fitting/model alternatives
  are unnecessary unless the actual question changes them.
- **Essential facts:** independent label/split process, source/time population,
  feature/training dependencies, candidate conditioning and loss/operating point.
- **Choices/checks:** regularized/interpretable baseline versus justified source-aware
  or richer model. Isolate candidates, fitting, calibration and policy; use entity/
  temporal splits matched to the actual generalization target. Rule-derived tests
  cannot establish independent weak-supervision improvement.
- **Output:** predeclared experiment and realized manifest with negative/inconclusive
  rules. **Stop:** leakage/circular labels, unidentified estimand or absent permissions.

## New source onboarding and operational monitoring

- **Minimum retrieval:** [identifier semantics](../solutions/comparison-features/identifier-namespaces.md)
  and [monitoring response](../decisions/monitoring-response.md); source-pooling details
  only if the model transfers across sources.
- **Essential facts:** new source authority, namespace/reuse, units, time, copied
  fields, language/missingness, admissible combinations and actual consumers.
- **Choices/checks:** source-isolated/simple fallback baseline versus supported
  sharing, with shadow contrasts on old and new slices. Preserve old behavior where
  promised; drift/score profiles are not calibration or accuracy evidence.
- **Output:** onboarding contract, compatibility/invalidation map, independent audit
  and authorized escalation. **Stop:** unknown namespace/permission or unsupported
  new-source confidence; prefer bounded abstention and evidence acquisition.

## Incremental changes, deletions and recovery

- **Minimum retrieval:** [AR-06](../architectures/incremental-continuous.md) and
  relevant [operational witnesses](incremental-operations.md).
- **Essential facts:** accepted history/initial ID state, revision precedence, valid
  time, tombstones, global dependencies, index visibility and consumer authority.
- **Choices/checks:** versioned current-state + reconciliation baseline versus
  justified selective closure. Include previously unstored new neighbors and
  competitors; reject stale proposals. Identity continuity is not field or license
  continuity. Local replay does not undo external actions.
- **Output:** history-qualified repair, membership/master/ID checks and consumer
  correction plan. **Stop:** unbounded unknown closure, missing replay inputs,
  unauthorized restoration or unresolved external effects.

## Common recommendation boundary

Distinguish **Known → Assumed → Proposed → Testable → Proven**. Follow related
Hypothesis/Evaluation Cards only when needed, record missing specialist coverage,
and choose project practical margins before results. Baseline, alternative,
contracts, controls, outcome estimand and rollback limits must be explicit.
No pattern authorizes implementation outside the consumer's requested scope.
