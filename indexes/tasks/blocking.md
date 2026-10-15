# Blocking comparison and performance investigation

- **Minimum retrieval:** [candidate choice](../../decisions/candidate-strategy.md);
  [execution choice](../../decisions/execution-strategy.md) only for physical cost.
- **Essential facts:** eligible pair universe, actual passes/caps/indexes, block/degree
  tails, feature cost, memory and independent positives outside old candidates.
- **Choices/checks:** exact/multi-pass baseline versus selected approximation; or
  equivalent local/batched/partitioned work. Keep candidate change separate from
  placement, profile build/update/retention and whole-output completion.
- **Output:** recall–cost frontier or equivalent-output execution comparison using
  [EVAL-11-007](../../evaluation/execution-cost-replay.md) plus candidate/entity evaluation.
  **Stop:** lost pairs disguised as faster execution or unsupported outside-C recall.

## Selective next reads

Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.

- [DEC-05-001 — Choose a candidate generation strategy](../../decisions/candidate-strategy.md) · [L1 section](../domains/05.md#dec-05-001--choose-a-candidate-generation-strategy)
- [SOL-05-001 — Exact-key blocking](../../solutions/candidate-generation/exact-blocking.md) · [L1 section](../domains/05.md#sol-05-001--exact-key-blocking)
- [SOL-05-003 — Approximate retrieval under explicit candidate budgets](../../solutions/candidate-generation/approximate-blocking.md) · [L1 section](../domains/05.md#sol-05-003--approximate-retrieval-under-explicit-candidate-budgets)
- [EVAL-11-001 — Candidate recall and retrieval efficiency](../../evaluation/candidate-recall.md) · [L1 section](../domains/11.md#eval-11-001--candidate-recall-and-retrieval-efficiency)
- [EVAL-11-007 — Complete-output execution cost and replay evaluation](../../evaluation/execution-cost-replay.md) · [L1 section](../domains/11.md#eval-11-007--complete-output-execution-cost-and-replay-evaluation)

Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.

Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.
