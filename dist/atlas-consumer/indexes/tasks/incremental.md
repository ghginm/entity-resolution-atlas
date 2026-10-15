# Incremental changes, deletions and recovery

- **Minimum retrieval:** [AR-06](../../architectures/incremental-continuous.md) and
  relevant [operational witnesses](../../guides/incremental-operations.md).
- **Essential facts:** accepted history/initial ID state, revision precedence, valid
  time, tombstones, global dependencies, index visibility and consumer authority.
- **Choices/checks:** versioned current-state + reconciliation baseline versus
  justified selective closure. Include previously unstored new neighbors and
  competitors; reject stale proposals. Identity continuity is not field or license
  continuity. Local replay does not undo external actions.
- **Output:** history-qualified repair, membership/master/ID checks and consumer
  correction plan. **Stop:** unbounded unknown closure, missing replay inputs,
  unauthorized restoration or unresolved external effects.

## Selective next reads

Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.

- [AR-06 — Incremental/Continuous Entity Resolution](../../architectures/incremental-continuous.md) · [L1 section](../domains/02.md#ar-06--incrementalcontinuous-entity-resolution)
- [DEC-09-001 — Choose master representation and identity lifecycle](../../decisions/master-representation.md) · [L1 section](../domains/09.md#dec-09-001--choose-master-representation-and-identity-lifecycle)
- [SOL-01-001 — Enduring identity with time-scoped evidence](../../solutions/identity-semantics/temporal-identity.md) · [L1 section](../domains/01.md#sol-01-001--enduring-identity-with-time-scoped-evidence)
- [EVAL-11-007 — Complete-output execution cost and replay evaluation](../../evaluation/execution-cost-replay.md) · [L1 section](../domains/11.md#eval-11-007--complete-output-execution-cost-and-replay-evaluation)

Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.

Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.
