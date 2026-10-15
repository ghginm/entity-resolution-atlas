# ML or statistical experimentation

- **Minimum retrieval:** [experiment decision](../../decisions/experiment-design.md)
  plus the selected [scoring family](../../decisions/scoring-strategy.md).
  For reproducibility specifically, start instead at [artifact runs](../../solutions/architecture/versioned-artifact-runs.md)
  and the [realized manifest](../../guides/run-manifest-template.md); fitting/model alternatives
  are unnecessary unless the actual question changes them.
- **Essential facts:** independent label/split process, source/time population,
  feature/training dependencies, candidate conditioning and loss/operating point.
- **Choices/checks:** regularized/interpretable baseline versus justified source-aware
  or richer model. Isolate candidates, fitting, calibration and policy; use entity/
  temporal splits matched to the actual generalization target. Rule-derived tests
  cannot establish independent weak-supervision improvement.
- **Output:** predeclared experiment and realized manifest with negative/inconclusive
  rules. **Stop:** leakage/circular labels, unidentified estimand or absent permissions.

## Selective next reads

Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.

- [DEC-12-001 — Choose an experiment design that separates mechanisms from system effects](../../decisions/experiment-design.md) · [L1 section](../domains/12.md#dec-12-001--choose-an-experiment-design-that-separates-mechanisms-from-system-effects)
- [SOL-02-002 — Versioned artifacts and realized experiment runs](../../solutions/architecture/versioned-artifact-runs.md) · [L1 section](../domains/02.md#sol-02-002--versioned-artifacts-and-realized-experiment-runs)
- [SOL-12-001 — Controlled comparison with frozen baselines and independent evaluation](../../solutions/experimentation/controlled-comparison.md) · [L1 section](../domains/12.md#sol-12-001--controlled-comparison-with-frozen-baselines-and-independent-evaluation)
- [EVAL-11-007 — Complete-output execution cost and replay evaluation](../../evaluation/execution-cost-replay.md) · [L1 section](../domains/11.md#eval-11-007--complete-output-execution-cost-and-replay-evaluation)

Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.

Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.
