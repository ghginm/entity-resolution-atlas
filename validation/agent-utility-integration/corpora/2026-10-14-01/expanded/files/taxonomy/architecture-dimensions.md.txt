# Independent architecture dimensions

An architecture is a compatible choice across axes, not the name of a scorer. The axes are conceptually independent but contracts and data constraints can make a combination infeasible.

| Axis | Choices | Choice does not imply |
|---|---|---|
| Pipeline topology | Linear, cascade, parallel/multi-branch, iterative | Any specific model or resolver |
| Matching paradigm | Deterministic, likelihood-ratio/probabilistic, supervised, neural, hybrid | Mandatory clustering or labels available everywhere |
| Resolution strategy | Independent pairwise links, assignment, constrained partitioning, collective inference | Every source supports one-to-one matching |
| Execution lifecycle | Batch, incremental, streaming; federated where applicable | Streaming equals stateless matching; federated equals privacy-safe |

Federation describes ownership/access distribution and may coexist with batch or streaming. It is included in lifecycle navigation as requested, but is not a time-update mode. Adaptive compute and human involvement are additional composition policies, not new universal algorithms.

## Reference patterns, not six exclusive systems
- [AR-01 — Linear / Modular Baseline](../architectures/linear-modular.md): fixes sequential contracts while leaving model/resolver choices open.
- [AR-02 — Recall-Oriented Multi-Pass](../architectures/recall-multi-pass.md): changes candidate acquisition; the downstream scorer can remain linear or be cascaded.
- [AR-03 — Precision-First Adaptive Cascade](../architectures/precision-cascade.md): routes easy and ambiguous work differently; it can use multiple retrieval passes.
- [AR-04 — Parallel Multi-Model / Ensemble](../architectures/parallel-ensemble.md): adds scorer branches/fusion; candidate coverage and score conditioning must agree.
- [AR-05 — Collective / Consistency-Aware Resolution](../architectures/collective-consistency.md): adds joint decisions or constraints, not necessarily relational inference or clustering.
- [AR-06 — Incremental / Continuous ER](../architectures/incremental-continuous.md): adds change/state/reconciliation contracts; the affected subproblem can use any of the other patterns.

## Compatibility checks
1. Does the candidate artifact preserve pair/source/pass provenance and represent the resolver's eligible pair universe?
2. Is a score a rank, likelihood ratio, or calibrated probability for a declared population? Never sum incomparable raw model outputs.
3. Are cardinality or cannot-link constraints actually justified by identity semantics and reliable observations?
4. Does a skipped pair remain unknown rather than becoming a fabricated non-match?
5. Do changes/deletions invalidate candidate indexes, features, downstream memberships and master views?
6. Can review/corrections be applied without silently overriding the model/version audit trail?

## Example compositions
- Exact blocking → evidence states → additive expert score → pairwise thresholds/abstention, batch: AR-01 with a simple baseline and no clustering assumption.
- Complementary multi-pass candidates → Fellegi–Sunter → review/thresholds → constrained membership if required: AR-02 plus AR-05, batch or incremental.
- Multi-pass candidates → early trusted-identifier route → regularized logistic on remaining cases → calibrated policy → versioned entities: AR-02 plus AR-03 plus AR-06.
- Shared candidates → additive and logistic scorers → held-out calibrated fusion or disagreement review → justified assignment: AR-04 plus AR-05, with AR-01 as comparator.

These are theoretical configurations, not measured winners. See [contracts](module-contracts.md), [scenario stress tests](../guides/scenario-stress-tests.md), and [project intake](../guides/project-intake.md).
