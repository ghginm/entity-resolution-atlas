---
id: SOL-08-001
type: solution
title: Thresholds, abstention, and review policies
domain: "08"
summary: >-
  Convert pairwise scores into link, non-link, or deferred decisions using
  explicit losses, validated operating points, and review constraints. A
  probability-based cost threshold is justified only for calibrated estimates
  in the stated decision population with specified pairwise losses. Review is
  an action with cost, delay, and residual error, not a free confidence band.
  Semantic vetoes require genuine incompatibility. Assignment and clustering
  may need global resolution rather than independent thresholding.
tags: [entity-agnostic, pairwise, asymmetric-costs, high-precision, human-review, uncertainty, assignment, clustering]
maturity: established
evidence: supported-by-external-literature
relations:
  complements: [SOL-07-001, SOL-07-002, SOL-07-003]
  evaluated_by: [EVAL-11-002, EVAL-11-003]
  used_by: [AR-03]
---

# Thresholds, abstention, and review policies

## Short summary

Keep evidence estimation separate from the actions taken on its output. Link, non-link, and deferred review are distinct dispositions in classical linkage theory; the justified policy depends on distributions, error constraints, or losses rather than on an arbitrary confidence label.[1]

## Problem addressed

A useful ordering does not specify acceptable false-link risk, review workload, or permitted entity structure. A policy must translate scores into actions while respecting identity semantics, operational objectives, and downstream consequences. It should also distinguish a deferred unresolved pair from a confirmed non-match.

## Core mechanism

For a raw score, specify lower and upper operating thresholds: reject below the lower boundary, accept above the upper boundary, and defer between them. Fix boundary and tie handling explicitly. Select thresholds on representative validation labels under stated precision, recall, loss, or capacity requirements; do not use a probability formula on arbitrary score points.

For a **calibrated candidate-population probability** $p$, suppose correct actions have zero loss, false links cost $C_{FP}>0$, and missed links cost $C_{FN}>0$. **Expected-loss reasoning with these fixed pairwise losses:**

$$
R_{link}=(1-p)C_{FP},\qquad R_{nonlink}=pC_{FN}.
$$

Minimizing the two risks selects link when

$$
p>\frac{C_{FP}}{C_{FP}+C_{FN}},
$$

with an explicit tie convention. This is not a universal threshold: probability calibration, candidate population, action semantics, and the loss definition are conditions of the derivation. Context-dependent costs require conditioning on that context, not merely different thresholds without justification.

## Theoretical explanation

Introduce review risk rather than assuming review is perfect. **Illustrative risk model:**

$$
R_{review}=c_R+p\,e_{FN}C_{FN}+(1-p)e_{FP}C_{FP},
$$

where $c_R$ includes effort and delay, and $e_{FN},e_{FP}$ are review's conditional error rates. Select the minimum-risk feasible action. A middle abstention interval follows only if the risk functions cross appropriately; it is not guaranteed by three available actions. Capacity constraints can require prioritizing expected loss reduction per unit review effort. Uncertainty near a threshold is only one possible contributor to review value.

The landscape describes posterior-based expected-cost linkage decisions; the formulas here are explicit derivations under the stated assumptions.[5] Aggregate reliability is insufficient when costs or error rates differ across segments; validate probabilities at the information level used to act.

## Important variants

Single-threshold binary decisions, two-threshold deferred decisions, context-dependent thresholds, time-limited abstention, and workload-constrained review are policy variants. Formal assignment and constrained clustering are unexpanded pilot methods, not implied extensions of every threshold policy. A cost-sensitive threshold need not change the underlying scorer.

## Assumptions and prerequisites

Define the candidate population, loss units, permitted actions, and whether rejecting a candidate means no link now or a durable cannot-link. Estimate review accuracy and service capacity rather than treating annotation as infallible. Reserve independent test labels; thresholds chosen on the test set cannot support an honest prospective estimate. Document model and calibration versions, cutoff inclusivity, review expiry, and escalation ownership.

## Applicability conditions

Independent thresholds fit tasks with separable pairwise actions. If one-to-one linkage is required, several individually plausible pairs may compete for the same record. If the output is entity membership, pairwise decisions must be reconciled with the specified equivalence semantics and constraints.[5] These tasks require evaluating a resolution method, not merely tuning a cutoff.

## Advantages

Separating policy permits one scorer to support different loss profiles and review budgets. Explicit deferral preserves uncertainty and makes workload measurable. Stated risk assumptions allow policy changes to be audited instead of conflating them with improved scoring.

## Trade-offs and failure modes

Thresholds transfer poorly after candidate, source, or calibration shifts. A narrow review band can satisfy capacity while hiding dangerous accepted errors. Review delay can itself create loss. A hard veto is justified only by genuine semantic incompatibility backed by valid scope and observation guarantees; a noisy identifier conflict normally remains evidence, not a logical impossibility. Weak agreements must not arbitrarily override a legitimate constraint.

Connected components of accepted edges can amplify one false link into an overmerge; a rejected edge need not become a cannot-link.[5] Marginal pair probabilities are not automatically compatible partition probabilities.

## Relationships with other methods

Complements [additive scores](../matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../matching-scoring/fellegi-sunter.md), and [logistic regression](../matching-scoring/logistic-regression.md); their probability interpretations differ. A [precision cascade](../../architectures/precision-cascade.md) can route unresolved pairs to additional evidence or review rather than forcing immediate decisions.

## How to evaluate

Use [pairwise quality and calibration](../../evaluation/pairwise-calibration.md) for threshold sensitivity, accepted/rejected errors, and selective risk versus coverage. Measure review demand, delay, residual error, and cost. Use [entity-resolution quality](../../evaluation/entity-resolution-quality.md) for assignment violations, overmerges, and undermerges; pairwise gains alone do not establish safer entities.

## Research opportunities

Compare uncertainty-based review with expected-risk-reduction routing at a fixed budget. Treat review effectiveness and entity-level loss estimates as hypotheses requiring operational evidence, not automatic gains from abstention.

## References and evidence limitations

Classical disposition theory and later expected-cost formulations support the mechanism.[1][5] No project costs, reviewer accuracy, calibration result, or empirically optimal cutoff is supplied here.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
