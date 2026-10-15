---
id: SOL-10-004
type: solution
title: Weak supervision with auditable labeling functions
domain: "10"
summary: >-
  Generate provisional pair-training labels from explicit rules, external resources
  and other noisy sources that can vote match, nonmatch or abstain. Diagnose
  coverage, conflicts and copied evidence before choosing simple voting or a
  dependency-aware label model. Independent adjudication remains necessary to
  distinguish rule imitation from identity discrimination and operational benefit.
  This approach requires defensible label semantics, source lineage and informative
  overlap; scarce sources, class imbalance and self-reinforcing errors can make
  confident silver labels misleading.
tags: [entity-agnostic, few-labels, noisy, conflicting, pairwise, source-aware, provenance, uncertainty, human-review, experimentation]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-10-001]
  evaluated_by: [EVAL-11-002, EVAL-11-003, EVAL-11-005]
---

# Weak supervision with auditable labeling functions

## Short summary

Produce silver training supervision, not reference truth. The source-supported pipeline separates labeling functions (LFs), probabilistic label aggregation and discriminative training.[16][21] The ER safeguards and proposed comparisons below are Atlas reasoning, not measured ER gains.

## Problem addressed

Expert rules can label many pairs cheaply but disagree, cover different populations and reuse the same evidence. The decision is whether their combined supervision offers more value than deploying explicit rules or buying a small adjudicated training set—not whether weak labels can replace independent evaluation.

## Core mechanism

For eligible pair $x_i$, define $\lambda_j(x_i)\in\{+1,-1,0\}$ as match, nonmatch or abstain; collect the matrix $\Lambda_{ij}$. A label model estimates $q_i=P_\theta(Y_i=+1\mid\Lambda_i)$ from observed votes under specified source-accuracy and dependency assumptions.[16][21]

Pass soft labels to a noise-aware expected training loss; the canonical [logistic scorer](../matching-scoring/logistic-regression.md) explains the objective without another scorer derivation.[16][21] These are model-conditioned probabilities, not automatically calibrated truth.

Specify each LF's evidence, namespace/time validity, vote meaning and provenance. A rule that declines a merge for risk control does not assert nonidentity: do not automatically convert policy rejection, failed retrieval or missing evidence into LF negatives. All-abstain pairs remain unknown; even a prior-derived $q_i$ is not evidence of their identity.

## Theoretical explanation

The independent model in Data Programming assumes conditional LF independence, balanced classes, per-LF conditional-on-voting accuracy 0.8–0.9 and coverage 0.3–0.5.[16]

Its main-text **Theorem 1** additionally assumes correct specification, $Y\perp f(X)\mid\Lambda$ and bounded optimization/generalization error. The displayed 2,000-LF condition simplifies that theorem; it is not an operational minimum or a recommendation to add votes. The paper points to arbitrary-count appendix results, whose proofs were not reviewed here.[16]

The dependent extension's **Theorem 2** restricts feasible parameters, requires learnability from labeled samples and bounds conditional label variance across feasible models.[16] These are substantive assumptions, not guarantees for arbitrary ER rule collections.

**Reasoning:** identical LFs add no independent information. In an unrestricted latent-label model, swapping class meanings can preserve the observable vote distribution; defensible orientation therefore needs semantic anchors, independent labels or justified accuracy constraints. Counting more copied votes cannot establish identifiability or truth.

## Important variants

- **High-confidence silver:** retain only selected LF agreements or a validated confidence range. This trades coverage for provisional precision, not certainty.
- **Majority vote:** cheap and inspectable; abstain on ties. Duplicates receive undue influence unless grouped.
- **Dependency-aware label model:** estimate reliability while representing shared evidence.[21] Added flexibility costs fitting and validation effort; it cannot manufacture missing independent information.
- **Model pseudo-labels/self-training:** reuse a predictor's own outputs. Keep these separate from externally sourced LF votes: feeding them back as independent evidence can reinforce the predictor's mistakes.

## Assumptions and prerequisites

Require authorized sources, identity semantics, useful coverage and informative overlap. With one effective source, or disjoint sources that never overlap, unlabeled votes alone cannot establish relative correctness without extra constraints or evidence. Audit conditional accuracies using independent adjudication by source pair, missingness, language and conflict stratum; global LF reliability may conceal reversals.

Declare the match prior for the eligible candidate population and test sensitivity to plausible alternatives. Rare matches make aggregate accuracy misleading; balancing silver classes changes the training distribution without recovering deployment calibration. A small independent development set can challenge orientation, priors and LF reliability, but final audit labels must remain held out independently.

Preserve immutable input/resource snapshots, LF code/version lineage, aggregation settings and label confidence/abstention reasons. Record which audit evidence was independent of these resources. Detailed deployment monitoring and retraining orchestration are later MLOps work, not this card's scope.

## Applicability conditions

Consider this when reusable expert knowledge is available and representative training annotation is expensive. Prefer explicit rules when they already meet requirements cheaply. Reject a truth-quality claim when only silver labels are available; shared-source evidence or unsupported identity semantics cannot be repaired by a larger label model.

## Advantages

LFs expose label rationale, localize disagreements and permit inexpensive relabeling after a documented rule correction. Soft aggregation can retain uncertainty instead of forcing every conflict into a binary label. These are workflow capabilities, not promised accuracy improvements.

## Trade-offs and failure modes

**Illustrative counterexample:** three name LFs use exact normalization, accent removal and token sorting. All vote match for two organizations named “Atlas Trading.” An independent registry LF votes nonmatch because valid, different identifiers in a namespace with one identifier per organization at that time contradict identity under the declared semantics. Majority vote selects the name match; an independence-assuming model can overcount the shared name evidence. Collapsing the name family or modeling its dependence is a useful control, but adjudication must verify the registry assumptions. Different identifiers across unrelated namespaces alone would not justify the negative vote.

**Circularity:** training and evaluating against the same rule-generated labels measures imitation. Disjoint rows do not remove the shared label authority or systematic rule errors. A model may perfectly imitate the name family while failing registry contradictions. Likewise, confident pseudo-labels recycled into new LFs can turn repeated mistakes into apparent consensus. Audit confidence tails, uncovered pairs and conflicts independently rather than treating agreement as correctness.

## Relationships with other methods

Addresses [ground-truth acquisition](../../decisions/ground-truth-acquisition.md) for training supervision only. [Probability-sampled review](probability-sampled-review.md) supplies design-aware independent evidence; [targeted active review](targeted-active-review.md) can investigate LF conflicts but its selection does not establish population accuracy. [Independent entity references](independent-reference.md) support membership evaluation. Threshold policy consumes scores separately; LF abstention is not automatically production abstention.

## How to evaluate

Use [controlled comparisons](../experimentation/controlled-comparison.md). Freeze candidates, features, admissible sources and downstream policy. For new identities use entity-disjoint splits; for existing-identity continuation use forward-time, as-of historical state without future-label feedback. Add source holdouts for source transfer under the [split contract](../experimentation/controlled-comparison.md#applicability-conditions). Compare explicit rules only, majority-vote, dependency-aware and small gold-supervised arms at matched expert/review cost, including LF construction/tuning. Disclose compute/maintenance separately; keep the scorer fixed across silver variants and calibrate/select thresholds outside the final test.

Keep three distinct outcomes:

1. **LF diagnostics:** coverage is the fraction receiving any vote; overlap receives multiple votes. Measure per-LF coverage and agreement/disagreement conditional on co-voting, with denominators and undefined empty overlaps. Break out conflicting and all-abstain strata; these diagnostics do not measure truth.
2. **Independent discrimination:** apply [pair quality/calibration](../../evaluation/pairwise-calibration.md), with sampling weights where justified, uncertainty preserving shared-entity dependence, and covered/uncovered source slices. Rule-label agreement is imitation only.
3. **Actual outcome gain:** use [entity quality](../../evaluation/entity-resolution-quality.md) on supported memberships and report false merges, missed identities, review load and operational cost. Use [incomplete-reference assessment](../../evaluation/incomplete-reference-quality.md) rather than closing unknown labels as negatives; candidate-only tests cannot establish full-population recall.

Predeclare practical gains and harm limits from project costs. **Adopt** only if independent tests show useful benefit within guardrails and budget; **reject** if harm or cost dominates, or improvements are imitation alone. **Inconclusive** evidence from sparse positives, unresolved labels or wide intervals calls for independent review, not more circular labels.

## Research opportunities

Test family-collapse/dependency ablations against the copied-name counterexample. Test additional independently justified evidence on the same audit sample. A gain only against silver labels supports rule reproduction; improvement against adjudication supports discrimination; final identity/cost improvement supports operational value.

## References and evidence limitations

Reviewed Data Programming §§3–5: LF modeling, conditional theorems and relation-extraction experiments against if-then-return supervision using blind hand-labeled evaluation.[16] Reviewed Snorkel §2, §§3.1–3.2 and §4.1: aggregation/training, modeling tradeoffs and application comparisons; its setup uses small labeled development and blind held-out test sets.[21] Neither establishes ER superiority, calibration of arbitrary LF posteriors or validity of copied/poorly identified sources. Supplementary proofs were not reviewed. No ER implementation, dataset processing or experiment was performed.

## Sources

[16] https://proceedings.neurips.cc/paper_files/paper/2016/file/6709e8d64a5f47269ed5cea9f625f7ab-Paper.pdf — Data Programming: Creating Large Training Sets, Quickly
[21] https://www.vldb.org/pvldb/vol11/p269-ratner.pdf — Snorkel: Rapid Training Data Creation with Weak Supervision
