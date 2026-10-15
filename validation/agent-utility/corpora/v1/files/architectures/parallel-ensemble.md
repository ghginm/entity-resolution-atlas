---
id: AR-04
type: architecture
title: Parallel Multi-Model/Ensemble
domain: "02"
summary: >-
  Several scorers examine shared or explicitly unioned candidates, then a fusion
  policy combines outputs or sends disagreements to review. The pattern seeks
  complementary evidence and error behavior rather than assuming more models are
  better. It requires compatible candidate keys, declared score meanings, and
  leakage-safe training when fusion is learned. Costs include multiple inference
  paths, calibration, and monitoring; correlated errors, incomparable scores, and
  silently missing branch outputs can undermine both accuracy and interpretability.
tags: [entity-agnostic, pairwise, calibration, uncertainty, compute-intensive, human-review, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [AR-05, AR-06]
  evaluated_by: [EVAL-11-002, EVAL-11-003]
---

# AR-04 — Parallel Multi-Model/Ensemble

## Philosophy and four dimensions

Ask whether distinct models add useful information beyond a strong single scorer. The ER landscape includes probabilistic and supervised methods, making model choice broader than one mandatory paradigm.[5] The proposed fusion contracts and experiments below are Atlas synthesis, not a claim of ensemble superiority.

- **Topology:** parallel scoring branches with fusion; branches may share candidates or use an explicitly unioned pool.
- **Scoring paradigm:** expert rules, additive evidence, probabilistic models, supervised or neural scorers, and mixed ensembles.
- **Resolution:** fused pair dispositions or downstream assignment/constrained/collective membership.
- **Lifecycle:** batch, incremental, or streaming execution. Federated privacy/access constraints independently limit branch evidence and permissible exchanged outputs.

## Pipeline and modules

`Representations → shared candidates or eligible union → [scorer A | scorer B | scorer C] → aligned outputs → fusion/disagreement policy → resolver`.

Required modules include common observation/pair identities, candidate scope, branch evidence and scoring, output alignment, fusion or disagreement handling, and resolution. Optional modules include branch-specific features, probability calibration, learned stacking, review, and explanation aggregation. Multiple retrieval branches alone constitute a retrieval pattern, not this multi-scorer pattern.

For a unioned pool, specify whether every branch scores every pair. A branch that cannot score a pair must report unavailable output; absence is not a negative vote. Shared candidates simplify attribution but prevent any branch from repairing missing candidates.

## Conceptual input/output contracts

Extend the [module contracts](../taxonomy/module-contracts.md) with branch coverage.

- **Branch input:** candidate keys, observation versions, permitted evidence, and model configuration. **Output:** branch ID/version, score, score meaning, explanation where available, and success/unavailable/failure status for each pair.
- **Alignment input:** branch outputs and candidate manifest. **Output:** pair-keyed score vector, branch availability mask, and compatible snapshot metadata. Never join outputs solely by ambiguous record names.
- **Fusion input:** aligned outputs plus fusion/calibration version. **Output:** declared fused scale, uncertainty or disagreement signal, and provenance of contributing branches. A weighted sum of heterogeneous scales is not automatically meaningful.
- **Resolver input:** fusion results, policy, constraints, and competing candidates. **Output:** dispositions or memberships, abstentions, reasons, and review work items where promised.

Illustratively, a strong identifier-rule output and an ambiguous name-model score should expose their different evidential meanings. An explicit identifier precedence policy is a hybrid rule, not a calibrated probability average.

## Assumptions and compatible alternatives

Useful conditions include different evidence modalities, source-specific specialists, uncertain cases benefiting from disagreement review, and sufficient operational budget. Different model classes need not make different errors. Diversity must be checked on shared held-out cases, not inferred from model names.

[Additive soft matching](../solutions/matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), and [logistic regression](../solutions/matching-scoring/logistic-regression.md) provide interchangeable branches. Alternatives include explicit voting over comparable dispositions, validated probability fusion, priority rules, stacking, or review-only disagreement detection. [Thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md) remain a separate policy layer.

Fixed expert fusion can operate without training labels but needs representative auditing. Learned fusion needs enough labeled entities and source combinations. Generate stacking inputs out-of-fold: each training pair's base prediction must come from models not trained on its entity or linked observations. Use entity-disjoint folds, nested tuning where needed, and a separate final test set; ordinary random pair splits can leak identities across folds.

## Mechanism, trade-offs, and failures

The proposed mechanism is exploiting complementary residual errors or exposing disagreement that deserves review. Strong positive error correlation limits redundancy's benefit; disagreement itself does not identify the correct model. Averaging arbitrary additive scores, likelihood ratios, and logits risks domination by scale rather than evidence.

Parallel execution adds total compute and memory even when latency falls. Tail latency follows slow branches unless explicit timeout policies apply. Calibration, training, monitoring, and explanation reconciliation expand operational burden. Correlated features can double-count evidence. Missing branch outputs, candidate-distribution shift, source leakage, and stale calibration can create apparent gains that disappear outside training conditions.

## Interactions, evaluation, and research

[AR-05](collective-consistency.md) can resolve fused scores, but fusion must preserve its objective's score semantics. [AR-06](incremental-continuous.md) must invalidate both branch and fusion artifacts after relevant changes.

Evaluate [pair quality/calibration](../evaluation/pairwise-calibration.md) and [entity quality](../evaluation/entity-resolution-quality.md), including shared-case error correlation, disagreement yield, branch ablations, source segments, inference cost, and review load. Compare to the strongest separately tuned single scorer under the same candidates and budget. Variations include specialist gating and ensembles only inside expensive cascade stages. Research can test whether diversity-aware selection improves the quality–cost frontier; reject the proposal if marginal benefit vanishes on entity-disjoint tests. No measured ensemble benefit is claimed.

## Sources

[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
