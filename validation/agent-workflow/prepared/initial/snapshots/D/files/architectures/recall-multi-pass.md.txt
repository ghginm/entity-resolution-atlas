---
id: AR-02
type: architecture
title: Recall-Oriented Multi-Pass
domain: "02"
summary: >-
  Multiple retrieval passes propose overlapping candidate pairs, which are unioned,
  deduplicated, and scored under a declared downstream policy. The pattern targets
  missed matches caused by heterogeneous names, identifiers, scripts, or sparse
  attributes without dictating a scorer. It requires complementary retrieval
  evidence and explicit eligibility rules. Candidate coverage can increase before
  pruning, but workload, selection bias, and false-positive exposure can also grow;
  pass value must be assessed marginally rather than by pass count.
tags: [entity-agnostic, high-recall, noisy, sparse, multilingual, multiscript, candidate-generation, multi-pass, provenance]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [AR-03, AR-05]
  evaluated_by: [EVAL-11-001, EVAL-11-002]
---

# AR-02 — Recall-Oriented Multi-Pass

## Philosophy and four dimensions

Use different retrieval views to reduce dependence on one fragile key. Blocking, filtering, and hybrid candidate-efficiency families are distinguished in the blocking survey; their taxonomy does not establish this particular composition as universally superior.[2] This card's composition and experiments are Atlas synthesis.

- **Topology:** parallel or sequential candidate passes, then union/deduplication and a downstream pipeline; sequential execution need not imply adaptive routing.
- **Scoring paradigm:** any deterministic, additive, probabilistic, supervised, neural, or hybrid scorer compatible with the union's evidence.
- **Resolution:** pairwise policy, assignment, constrained clusters, or collective resolution, independently selected.
- **Lifecycle:** batch or incremental candidate maintenance. Federated access/privacy restrictions separately constrain which representations and pairs can cross boundaries.

## Pipeline and modules

`Versioned representations → [pass A | pass B | pass C] → eligible union → optional budget/filter → evidence → scoring → resolution`.

Required modules are representation preparation, at least two retrieval passes, common eligibility checks, canonical pair deduplication, pass provenance, comparison, scoring, and resolution. Optional modules include approximate indexes, learned retrieval, pass-specific normalization, adaptive budgets, review, and entity construction. Embedding retrieval is an alternative, not a required modernizing step. The [multi-pass blocking solution](../solutions/candidate-generation/multi-pass-blocking.md) supplies a component-level view.

## Conceptual input/output contracts

Follow the [module contracts](../taxonomy/module-contracts.md).

- **Pass input:** source-scoped observation IDs and versions, permitted pair scope, representation version, and pass settings. **Output:** proposed pair keys with pass identity, retrieval rank or similarity when meaningful, and truncation/coverage metadata. Retrieval rank is not identity confidence.
- **Union input:** pass proposals. **Output:** unique eligible pair keys with the complete set of producing passes and referenced observation versions. Deduplication removes repeated computation, not corroborating provenance.
- **Budget/filter input:** union plus explicit resource policy. **Output:** retained pairs and an auditable account of excluded pairs and selection rules; expose pre-budget and post-budget recall separately.
- **Comparison/scoring input:** retained pairs and observation evidence. **Output:** [evidence states](../solutions/comparison-features/evidence-states.md), score scale/model version, and explanations.
- **Resolver input:** scores plus decision/cardinality policy. **Output:** dispositions or membership, abstentions, and reasons; no-candidate records remain unresolved rather than silently unmatched by proof.

Illustratively, one pass might retrieve an address variant while another retrieves a transliterated organization name. Their union exposes both opportunities; it does not establish either pair as correct.

## Assumptions and compatible alternatives

Prefer this pattern when diagnosed retrieval omissions concentrate in noisy names, sparse attributes, mixed scripts, or different source schemas. Complementarity means different missed-match cases, not statistical independence between passes. Namespace semantics must prevent matching unrelated identifiers solely because text agrees. Broad passes may be inappropriate where privacy rules prohibit required representations.

[Additive scoring](../solutions/matching-scoring/additive-soft-matching.md) supports explicit expert evidence; [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md) or [logistic regression](../solutions/matching-scoring/logistic-regression.md) are alternative scoring modules. Labels are unnecessary for constructing deterministic passes, but representative labeled matches are needed to estimate their coverage. Learned retrieval and downstream supervision require separate training/evaluation partitions; labels confined to an old pass cannot reveal all new-pass errors.

## Mechanism, trade-offs, and failures

As mathematical reasoning, if every unchanged candidate set remains in an unpruned union under the same eligibility scope, the union contains each constituent set; known-match candidate recall cannot decrease. This says nothing about final resolution quality. Global top-k limits, filtering, or changed normalization invalidate that monotonicity comparison.

Additional passes cost indexing, storage, candidate comparison, and skew management. Redundant passes may contribute few unique true matches while generating many negatives. A permissive common-name pass can dominate workload. Pass-specific representations can hide contradictions; features that count pass agreement may double-count shared keys.

Changing the candidate distribution changes the hard-negative mix and potentially score calibration. Thresholds learned under narrow blocking therefore require reassessment. Higher candidate recall may still yield lower final precision or different assignments because downstream competitors change.

## Interactions, evaluation, and research

[AR-03](precision-cascade.md) can route expensive comparison after union, but early exits must not suppress late-pass competitors. [AR-05](collective-consistency.md) can consume the resulting scores; broader candidates alter its optimization problem.

Use [candidate recall evaluation](../evaluation/candidate-recall.md) for each pass, marginal union gain, overlaps, and recall after budgets. Use [pairwise calibration](../evaluation/pairwise-calibration.md) by source pair, script, missingness, and producing-pass combination. Measure final entity errors and cost, not only retrieval gains.

Variations include exact-plus-approximate passes, source-specific passes, and incremental index refresh. Research should compare complementary versus redundant passes with fixed downstream models, then retuned models as a separate comparison. Falsify the proposed benefit if additional passes consume the agreed budget without useful held-out recall or end-to-end loss reduction. No Atlas measurements are reported.

## Sources

[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
