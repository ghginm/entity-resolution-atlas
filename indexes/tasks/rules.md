# Rule-heavy refactoring and conflicts

- **Minimum retrieval:** [composition decision](../../decisions/rule-composition.md)
  and [refactor witnesses](../../guides/rule-policy-refactoring.md); ordered/table details only
  for the selected alternative.
- **Essential facts:** precedence, overrides, default/unknown/error behavior,
  mandatory guards, effects, source exceptions and rule versions.
- **Choices/checks:** explicit ladder baseline versus parameterized predicates,
  ordered policy or table. Inspect shadowing, conflicting hits and required unknown
  guards. Behavioral agreement is rule imitation, not correct identity.
- **Output:** semantic mapping, traces, conditional regression suite and staged
  migration. **Stop:** unresolved mandatory conflict, changed effects or missing oracle.

## Selective next reads

Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.

- [DEC-08-002 — Choosing explicit rule composition and conflict semantics](../../decisions/rule-composition.md) · [L1 section](../domains/08.md#dec-08-002--choosing-explicit-rule-composition-and-conflict-semantics)
- [SOL-08-005 — Ordered first-match policies with pure predicates](../../solutions/decision-resolution/ordered-rule-policies.md) · [L1 section](../domains/08.md#sol-08-005--ordered-first-match-policies-with-pure-predicates)
- [SOL-08-006 — Declarative decision tables with explicit hit policies](../../solutions/decision-resolution/declarative-decision-tables.md) · [L1 section](../domains/08.md#sol-08-006--declarative-decision-tables-with-explicit-hit-policies)
- [EVAL-11-006 — Synthetic fixtures, metamorphic relations, and behavioral contract violations](../../evaluation/synthetic-metamorphic.md) · [L1 section](../domains/11.md#eval-11-006--synthetic-fixtures-metamorphic-relations-and-behavioral-contract-violations)

Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.

Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.
