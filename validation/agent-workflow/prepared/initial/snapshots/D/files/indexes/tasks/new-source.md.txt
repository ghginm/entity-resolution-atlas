# New source onboarding and operational monitoring

- **Minimum retrieval:** [identifier semantics](../../solutions/comparison-features/identifier-namespaces.md)
  and [monitoring response](../../decisions/monitoring-response.md); source-pooling details
  only if the model transfers across sources.
- **Essential facts:** new source authority, namespace/reuse, units, time, copied
  fields, language/missingness, admissible combinations and actual consumers.
- **Choices/checks:** source-isolated/simple fallback baseline versus supported
  sharing, with shadow contrasts on old and new slices. Preserve old behavior where
  promised; drift/score profiles are not calibration or accuracy evidence.
- **Output:** onboarding contract, compatibility/invalidation map, independent audit
  and authorized escalation. **Stop:** unknown namespace/permission or unsupported
  new-source confidence; prefer bounded abstention and evidence acquisition.

## Selective next reads

Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.

- [DEC-14-001 — Operational monitoring, independent audits and response](../../decisions/monitoring-response.md) · [L1 section](../domains/14.md#dec-14-001--operational-monitoring-independent-audits-and-response)
- [SOL-06-003 — Namespace-qualified identifier evidence](../../solutions/comparison-features/identifier-namespaces.md) · [L1 section](../domains/06.md#sol-06-003--namespace-qualified-identifier-evidence)
- [SOL-07-004 — Pooling and source-conditioned evidence reliability](../../solutions/matching-scoring/source-aware-reliability.md) · [L1 section](../domains/07.md#sol-07-004--pooling-and-source-conditioned-evidence-reliability)
- [EVAL-11-002 — Pairwise discrimination and probability calibration](../../evaluation/pairwise-calibration.md) · [L1 section](../domains/11.md#eval-11-002--pairwise-discrimination-and-probability-calibration)

Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.

Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.
