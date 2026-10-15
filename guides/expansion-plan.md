# Expansion plan: after user review of the pilot

**Historical v1/v1.1 proposal; review gate superseded.** The user's comprehensive v1.2+ authorization now permits substantial connected expansion. The active [implementation tracker](v1.2-expansion-tracker.md) owns status and sequencing; this earlier plan is retained as provenance, not a competing task list. The current session completes Wave 0–1 and hands off Wave 2. Nothing authorizes implementing ER, mass-generating taxonomy items or modifying frozen benchmark artifacts. Historical ordering below reflects the earlier scenarios, not universal project priorities.

**v1.1 status (2026-10-13).** Group 1 is now mostly implemented: [DEC-01-001](../decisions/identity-semantics.md), [SOL-01-001](../solutions/identity-semantics/temporal-identity.md), [DEC-08-001](../decisions/resolution-strategy.md), [SOL-08-002](../solutions/decision-resolution/one-to-one-assignment.md), [SOL-08-003](../solutions/decision-resolution/connected-components.md), [SOL-08-004](../solutions/decision-resolution/constrained-clustering.md), [DEC-09-001](../decisions/master-representation.md) and [SOL-09-001](../solutions/master-records/provenance-survivorship.md); group 3 gained [SOL-10-001](../solutions/ground-truth/independent-reference.md) and [EVAL-11-004](../evaluation/retrieval-blind-spots.md). Still outstanding from group 1: a dedicated hard trusted-identifier rule card. Group 3 label-acquisition variants (active learning, weak supervision), groups 2, 4–6 remain deferred exactly as written. Do not re-add the completed items to a future batch; re-derive priorities from benchmark findings and the [coverage matrix](decision-coverage-matrix.md).

Effort is relative: **S** = bounded synthesis of well-understood material and a few primary checks; **M** = multiple mechanisms/references and careful comparison; **L** = specialist literature, complex assumptions or threat models. These are not measured durations. Reorder after a real project intake; strict privacy or identity semantics can take precedence over all model work.

| Sequence / group | Proposed coverage | Effort | Why this order; quality gate |
|---|---|---|---|
| 1 — Core established solutions | Identity/cardinality Decision Card; hard trusted-identifier rules; one-to-one bipartite assignment with unmatched option; connected components versus constrained membership; master virtual/golden/reversible representations — **v1.1: implemented except the hard trusted-identifier rule card** | M | Scenarios A/C expose assumptions currently explained only in maps/architectures. Add complete mechanisms before recommending specialized resolution; review counterexamples and identity-cost units |
| 2 — Supporting techniques | Unicode/language-aware multi-representation normalization; string/token/phonetic comparison family; sorted neighborhood and q-gram/inverted retrieval; source/field profiling and multi-valued/time evidence | M | Scenario B needs verified language/error-model choices beyond conservative examples. Require scripts/locales, information-loss failure cases and independent retrieval diagnostics |
| 3 — Evaluation and experimentation | Label-sampling/annotation Decision and Solution Cards; incomplete-ground-truth estimators; outside-candidate audit; oracle component diagnostics; factorial/ablation design; shift/transfer and tail-risk metrics | M–L | These constrain every later claim. Require explicit estimands, inclusion probabilities, dependence-aware intervals and examples that separate inconclusive from falsified evidence |
| 4 — Architecture extensions | Human review/correction composition; source-aware/GAM/hybrid configurations; streaming out-of-order updates/deletion/replay; skew-aware distributed execution; versioned ID maintenance | M–L | Scenario C reveals dependency/state/capacity gaps. Require compatible conceptual contracts, failure containment and comparisons with simple batch/linear baselines |
| 5 — Experimental research opportunities | Adaptive budgets/learned retrieval; symbolic+ANN complementarity; source-pair shrinkage/mixture routing; distillation/selective neural matching; joint normalization/matching; LLM-assisted comparison | M–L | Investigate only when an observed error opportunity and data/budget justify it. Cite primary work, avoid novelty claims and require controlled hypotheses with security/reproducibility constraints |
| 6 — Advanced theoretical deep dives | FS dependence and unsupervised identifiability; collective/global optimization; incomplete truth and survey-design variance; advanced retrieval guarantees; privacy-preserving linkage threat models | L | More depth should answer a demonstrated decision gap, not duplicate L2. Privacy may move to sequence 1 when access constraints apply; security guarantees require specialist primary sources |

## Missing coverage, grouped by domain
- **01/03/04:** ontology/temporal semantics, schema evolution/matching, linguistic normalization and enrichment have maps but no standalone pilot solutions.
- **05/06:** sorted neighborhood, canopy/q-gram/LSH/ANN/learned retrieval and detailed similarity/temporal/graph comparisons are unexpanded. Exact/multi-pass and evidence-state cards do not cover their full parameter spaces.
- **07:** GAM/constrained models, boosting, neural/hybrid/weak supervision, distillation and transfer lack L2 comparisons. The interpretable additive/FS/logistic pilot is intentionally the anchor.
- **08/09:** assignment/clustering/collective and master survivorship/stable identity are architectural/domain guidance, not a fully researched solution set.
- **10/11/12:** label-construction, advanced incomplete-truth estimation and dedicated oracle/factorial cards remain; the pilot evaluation cards define important limitations rather than solve all of them.
- **13/14:** physical scalability, streaming state, operational monitoring, subgroup reliability and protected linkage need deeper evidence and explicit threat/cost models.

## v1.2 priorities from the executed AU-v1 benchmark
The [measured comparison](../validation/agent-utility/results/COMPARISON-2026-10-13.md) is exploratory, not universal evidence. Prioritize these observed reasoning gaps before broad method expansion; this list requires user review and does not authorize new cards or benchmark tuning.
1. Pinned evaluator identity, enforceable sampling and blind second-evaluator/human adjudication; repeat across models with interleaved no-Atlas and complete same-cohort pairs.
2. Identity-continuity and assignment-utility counterexamples: AU-03 v1.1 falsely inferred discontinuity from a license change and confused surrogate optimality with truth despite relevant retrieval.
3. Operational independent-reference design: AU-02 v1/no-Atlas endorsed selected-only recall certification; v1.1 avoided that failure but still omitted denominators, inclusion weighting and uncertainty.
4. Master-field authority, copied-source dependence, unknown dates, correction replay and membership/survivorship ablations; AU-06 improved but left these unresolved.
5. Multilingual and retrieval-family depth only after the correctness gaps, rather than expanding advanced models because they are available.

## Acceptance criteria for each expansion batch
Add a small connected set around an actual decision. Verify primary sources; compare plausible alternatives and baseline; explain mechanism/prerequisites/cost/failures; avoid duplicating canonical theory. Add falsifiable hypotheses only when they provide information not already captured. Update catalog/relations and scenario routes, run documentation checks and a conceptual audit, then pause for review. Do not require every method to receive a deep dive.

## Feedback that changes the next iteration
1. Prefer deeper multilingual preparation/retrieval first, or fuller assignment/master-entity semantics?
2. Should the next batch emphasize interpretable GAM/constraints or labeling/evaluation under incomplete truth?
3. Are privacy/federated constraints a near-term consumer need requiring an earlier specialist review?
4. Is this selective-retrieval granularity sufficient for future agents, or do certain domains need richer Decision Cards?

Preserved lower-profile ideas remain in the [opportunities index](../research/opportunities-index.md). The [scenario tests](scenario-stress-tests.md) provide context for this ordering; none reports measured ER performance.
