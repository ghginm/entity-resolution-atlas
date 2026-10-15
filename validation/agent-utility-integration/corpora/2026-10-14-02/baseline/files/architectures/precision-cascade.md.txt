---
id: AR-03
type: architecture
title: Precision-First Adaptive Cascade
domain: "02"
summary: >-
  A cascade routes uncertain cases to progressively more costly evidence, scorers,
  or human review while allowing justified early decisions. It targets asymmetric
  false-merge costs and uneven case difficulty, not a universal ordering of models.
  Reliable early evidence, explicit routing units, and reversible dispositions are
  prerequisites. Compute savings depend on how often cases can safely exit;
  downstream distribution shift and irreversible early mistakes can erase the
  benefit, so route-specific quality and end-to-end costs must be tested together.
tags: [entity-agnostic, high-precision, asymmetric-costs, uncertainty, human-review, provenance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [AR-04, AR-06]
  evaluated_by: [EVAL-11-002, EVAL-11-003]
---

# AR-03 — Precision-First Adaptive Cascade

## Philosophy and four dimensions

Spend additional effort where current evidence cannot justify a safe disposition. Precision-first describes a project objective, not a guarantee or permission to discard recall. The broader ER landscape includes different scoring and resolution families; a cascade can compose these rather than equating complexity with correctness.[5] Routing design here is theoretically motivated Atlas synthesis.

- **Topology:** staged routing with early accept/reject/abstain opportunities, escalation, and optional reopening.
- **Scoring paradigm:** rules, additive evidence, probabilistic or supervised models, neural matching, and hybrids at different stages.
- **Resolution:** pairwise dispositions or staged proposals feeding assignment/constrained membership; local acceptance is not necessarily final global resolution.
- **Lifecycle:** batch, incremental, or streaming orchestration. Federated privacy/access constraints independently limit evidence available at each stage.

## Pipeline and modules

`Eligible cases → cheap evidence/policy → unresolved route → richer evidence/scorer → unresolved route → review or abstention → resolver`.

Required modules are candidate availability, a declared routing unit, staged evidence/scoring, exit and escalation policies, route provenance, and a final resolver. Optional modules include enrichment, parallel specialist scorers, human adjudication, and audit sampling. Reopening and correction are required whenever early outputs can later alter entity state; review capacity is required only if the policy promises review rather than indefinite abstention.

Record routing and pair routing differ. A cheap decision on one pair does not establish that a record has no competing candidates. Record-level early exit requires coverage and cardinality justification, particularly with late retrieval passes. Pair-level rejection only removes that comparison, unless an explicit downstream policy says otherwise.

## Conceptual input/output contracts

Apply the [module contracts](../taxonomy/module-contracts.md), adding routing lineage.

- **Router input:** observation or pair IDs and versions, available evidence, eligibility scope, stage history, and budget. **Output:** next-stage work items or provisional dispositions with the exact routing reason.
- **Stage input:** routed cases and permitted representations. **Output:** evidence version, score scale/model version, uncertainty diagnostics where available, and accept/reject/escalate recommendation. A recommendation must not masquerade as committed membership.
- **Exit-policy input:** stage outputs plus policy version and any competing candidates. **Output:** match/non-match/abstain, scope of commitment, and reopening conditions; retain rejected-case provenance.
- **Final resolver input:** all applicable proposals and constraints. **Output:** consistent dispositions or memberships, unresolved cases, and reversible change records.

Illustratively, agreement on a namespaced identifier may justify provisional acceptance only if namespace uniqueness, identifier reuse, and contradictions have been checked. An unqualified exact identifier match is not a universally safe shortcut.

## Assumptions and alternatives

Applicable characteristics include expensive evidence acquisition, heterogeneous difficulty, strict false-merge costs, and credible cheap signals. [Additive soft matching](../solutions/matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), and [logistic regression](../solutions/matching-scoring/logistic-regression.md) can occupy different stages. [Thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md) define actions separately from score generation.

Expert routes can operate without training labels, but their reliability remains unestablished without audits. Learned routing needs representative route labels and end-to-end outcomes. Few labels should motivate conservative escalation, not unsupported confidence. Later-stage training must reflect the uncertain cases actually routed there, with entity-disjoint partitions and temporal testing where appropriate.

## Mechanism, costs, and failures

Conceptually, expected compute is the first-stage cost plus each later-stage cost weighted by the fraction reaching it. Savings require cheap stages and sufficient safe exits; routing, review, and reopening overhead may eliminate them. This is reasoning, not a measured latency claim.

Early accept errors can create false merges, while early reject errors can prevent recovery of true matches. Irreversible exits make later evidence useless for those cases. Downstream cases are selected by earlier policies, so their difficulty and class mix differ from the original population; changing a gate can invalidate downstream calibration and thresholds. Budget-driven escalation truncation must remain visible as abstention, not fabricated non-match evidence.

## Interactions, evaluation, and research

[AR-04](parallel-ensemble.md) can provide a specialist ensemble at an expensive stage. [AR-06](incremental-continuous.md) provides event-triggered reopening when identifiers or contradictions change. With consistency-aware resolution, early exits should remain proposals until competitors and constraints are considered.

Evaluate [pair quality/calibration](../evaluation/pairwise-calibration.md) conditional on route and [entity quality](../evaluation/entity-resolution-quality.md) after all exits. Audit early accepted and rejected cases, not only escalations. Compare against a single full scorer at matched error-cost or precision targets; record recall, coverage, tail latency, review load, and correction cost.

Variations include evidence-only cascades, pair-level gates, and record-level retrieval escalation. Research can test reversible versus terminal exits using identical evidence and adjudicated cases. A saving is not useful if the agreed end-to-end loss or segment safety limit worsens. No configuration is universally preferred and no experimental results are asserted.

## Sources

[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
