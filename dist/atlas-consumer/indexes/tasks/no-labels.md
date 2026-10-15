# Matching improvement without reliable labels

- **Minimum retrieval:** [acquisition decision](../../decisions/ground-truth-acquisition.md)
  and [incomplete-reference evaluation](../../evaluation/incomplete-reference-quality.md).
- **Essential facts:** annotation unit, eligible universe, candidate selection,
  available positive/negative/partial truth, response/inclusion process, harm and
  review budget. Do not infer recall from candidate-only references.
- **Choices/checks:** independent probability/entity audit baseline versus targeted
  active/weak acquisition; preserve independent test evidence and unknown labels.
- **Output:** acquisition + identifiable-estimand experiment, with denominators,
  uncertainty and costs. **Stop:** unknown inclusion, zero support or unavailable
  semantic truth blocks the claimed population estimate, not all diagnostics.

## Selective next reads

Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.

- [DEC-10-001 — Ground-truth acquisition for learning and independent evaluation](../../decisions/ground-truth-acquisition.md) · [L1 section](../domains/10.md#dec-10-001--ground-truth-acquisition-for-learning-and-independent-evaluation)
- [SOL-10-002 — Probability-sampled review with separate evaluation and learning pools](../../solutions/ground-truth/probability-sampled-review.md) · [L1 section](../domains/10.md#sol-10-002--probability-sampled-review-with-separate-evaluation-and-learning-pools)
- [SOL-10-003 — Targeted active review for learning and high-risk diagnosis](../../solutions/ground-truth/targeted-active-review.md) · [L1 section](../domains/10.md#sol-10-003--targeted-active-review-for-learning-and-high-risk-diagnosis)
- [EVAL-11-005 — Quality estimation with incomplete reference evidence](../../evaluation/incomplete-reference-quality.md) · [L1 section](../domains/11.md#eval-11-005--quality-estimation-with-incomplete-reference-evidence)

Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.

Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.
