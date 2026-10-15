# Large components and graph-level identity errors

- **Minimum retrieval:** [resolution choice](../../decisions/resolution-strategy.md)
  and [closure/fragility](../../solutions/decision-resolution/connected-components.md).
- **Essential facts:** strict identity versus typed relations, edge provenance,
  admission semantics, constraints, competitor scope and downstream consequences.
- **Choices/checks:** connected-components baseline versus edge filtering/selective
  verification (change admitted edges) or constrained clustering (change membership
  using audited whole-union restrictions). Hold records/candidates/scores fixed and
  vary admission separately from membership. A true chain may have bridges; smaller components
  and fewer contradictions are not truth. Repair materialized memberships and fields.
- **Output:** contamination hypothesis, independent adjudication and reversible repair
  plan. **Stop:** topology-only certainty, unjustified must-links or irreversible harm.

## Selective next reads

Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.

- [DEC-08-001 — Choosing the resolution output and membership policy](../../decisions/resolution-strategy.md) · [L1 section](../domains/08.md#dec-08-001--choosing-the-resolution-output-and-membership-policy)
- [SOL-08-003 — Connected components of accepted identity links](../../solutions/decision-resolution/connected-components.md) · [L1 section](../domains/08.md#sol-08-003--connected-components-of-accepted-identity-links)
- [SOL-08-004 — Constrained entity partitioning with admissible membership](../../solutions/decision-resolution/constrained-clustering.md) · [L1 section](../domains/08.md#sol-08-004--constrained-entity-partitioning-with-admissible-membership)
- [EVAL-11-003 — Final entity-resolution quality and error diagnostics](../../evaluation/entity-resolution-quality.md) · [L1 section](../domains/11.md#eval-11-003--final-entity-resolution-quality-and-error-diagnostics)

Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.

Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.
