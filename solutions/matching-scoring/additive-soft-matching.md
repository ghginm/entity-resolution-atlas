---
id: SOL-07-001
type: solution
title: Additive soft matching
domain: "07"
summary: >-
  Combine explicit comparison features through a baseline and signed evidence
  contributions rather than requiring every field to agree. Expert weights
  provide a transparent reference specification; likelihood-ratio estimation
  or supervised fitting can replace manual weights while retaining an additive
  structure. Feature semantics, candidate conditioning, and conflicting evidence
  require deliberate treatment. A raw additive score is neither necessarily a
  probability nor a calibrated confidence, and learned or nonlinear variants
  are alternatives rather than mandatory upgrades.
tags: [entity-agnostic, no-labels, few-labels, interpretable, pairwise, evidence-engineering, missingness, low-cost]
maturity: established
evidence: theoretically-motivated
relations:
  addresses: [DEC-07-001]
  alternative_to: [SOL-07-002, SOL-07-003]
  complements: [SOL-07-004, SOL-07-005]
  evaluated_by: [EVAL-11-002]
  used_by: [AR-01]
---

# Additive soft matching

## Short summary

Assign a signed contribution to each interpretable comparison feature and add the contributions. This card describes the scoring form and expert-weighted baseline; probabilistic and supervised instantiations have separate cards. The mechanism is Atlas synthesis, not a measured performance claim.

## Problem addressed

**Atlas design reasoning:** hard conjunctions can reject pairs with one corrupted field, while permissive disjunctions can accept weak coincidences. Soft scoring allows strong supporting evidence, partial agreement, and contradictory observations to affect a common ranking. This flexibility does not determine which compensation patterns are acceptable under the identity definition.

## Core mechanism

For comparison features $f_j(a,b)$, define

$$
S(a,b)=b_0+\sum_{j=1}^{k}w_jf_j(a,b).
$$

Features may be continuous similarities or indicators for mutually exclusive [evidence states](../comparison-features/evidence-states.md). Specify their ranges and reference states: otherwise weights cannot be compared meaningfully. An exact agreement indicator, a partial-agreement indicator, and a reliable-conflict indicator can receive distinct contributions. Missing observations need explicit semantics; zero contribution means deliberately neutral evidence, not confirmed disagreement or agreement.

The output contract should expose the total, individual contributions, feature versions, and source provenance. A threshold belongs to the [policy layer](../decision-resolution/thresholds-abstention.md), not to this equation. Retain enough provenance to reconstruct why a pair received its score.

## Theoretical explanation

**Reasoning:** a positive weight raises the score when its feature increases; a negative weight lowers it. Contributions remain auditable, but additivity only describes the chosen function. It neither proves that fields are independent nor establishes a probability scale. Dividing by a maximum score or applying a sigmoid to arbitrary points does not supply a statistical model or calibration evidence.

There are principled routes from manual to learned contributions. [Fellegi–Sunter](fellegi-sunter.md) obtains comparison-state log likelihood ratios; a sum follows from conditional independence of the modeled evidence groups.[1] [Logistic regression](logistic-regression.md) learns a joint conditional log-odds function without requiring predictor independence.[7] The same additive shape therefore supports different assumptions and interpretations. Choosing learned weights is a testable change in estimation, not proof that the feature definitions are adequate.

## Important variants

Expert points, source-specific tables, state-based likelihood-ratio weights, and supervised linear weights retain explicit contributions. Optional interactions introduce joint evidence features. Generalized additive models replace selected linear effects with fitted functions; regularization or justified monotonic constraints control selected aspects of fitting.[7] The [nonlinear/learned comparator menu](learned-neural-comparators.md) explains the bounded alternatives and their evidence limits. None is a mandatory next stage. A hard veto is a separate policy constraint, not merely a very negative score.

## Assumptions and prerequisites

Declare the candidate population, feature scales, reference coding, and compensability assumptions. Review duplicated signals such as raw name agreement, normalized name agreement, and name-derived initials. Separate evidence absence from collection failure where possible. Expert elicitation should record why a weight is credible and which plausible alternatives were considered. Learned versions additionally require an estimation population appropriate to their statistical target.

## Applicability conditions

Consider this family when interpretable comparison evidence exists and a transparent, inexpensive scoring baseline is valuable. It can support sparse-label settings without pretending that manual weights are empirically optimal. It is less attractive when useful evidence consists mainly of complex joint patterns that the chosen feature basis cannot represent.

## Advantages

Explicit contributions support explanation, controlled ablation, and correction of individual evidence rules. Separating features, weights, and decisions makes component replacement possible without redesigning an entire pipeline. These are structural properties, not demonstrated accuracy improvements.

## Trade-offs and failure modes

Several weak agreements may overwhelm one genuine contradiction. Correlated representations can count one observation repeatedly. Weight scaling changes how features compete; a seemingly modest preprocessing change can therefore change rankings. Noninformative fields can acquire expert weight without data support. Within a blocked candidate set, an always-agreeing blocking feature supplies no discrimination, yet a transferred weight may inflate a claimed confidence. None of these issues is repaired merely by renaming the total “probability.”

**Atlas synthesis:** compare dropping a redundant representation, grouping dependent signals and jointly fitting weights before interpreting a larger sum as stronger corroboration. [Name representation lineage](../normalization/name-representations.md) identifies shared origins; [frequency-aware evidence](../../research/hypotheses/frequency-aware-evidence.md) proposes contextual weighting, not a license to count every rare transform independently. A dependency-aware score may still misestimate source-specific reliability; [pooling choices](source-aware-reliability.md) require their own controls.

## Relationships with other methods

This solution addresses the [scoring decision](../../decisions/scoring-strategy.md) and complements explicit evidence-state engineering. Fellegi–Sunter and logistic regression are alternatives for estimating contributions on the same evidence contract. It can be used inside a [linear modular architecture](../../architectures/linear-modular.md); topology does not require manual weights.

## How to evaluate

Use [pairwise quality and calibration](../../evaluation/pairwise-calibration.md) on fixed candidates. Compare expert points with learned contributions using identical splits, features, and operating constraints. Inspect conflict cases, missingness slices, redundant-feature ablations, and sensitivity to plausible weight perturbations. Evaluate calibration only for a separately justified probability mapping; otherwise report ordering and decision quality without probabilistic language.

## Research opportunities

Test whether [contextual reliability](../../research/hypotheses/contextual-reliability.md) or [frequency-aware evidence](../../research/hypotheses/frequency-aware-evidence.md) improves held-out quality at comparable cost. Distinguish better evidence from better weight estimation. A negative result should trigger diagnostics, not automatic escalation to a larger model.

## References and evidence limitations

The likelihood-ratio and logistic interpretations have separate foundations.[1][7] This expert-weighted specification is theoretically motivated; no universal weight table, benchmark gain, or Atlas experiment is claimed.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[7] https://hastie.su.domains/ElemStatLearn/main.html — The Elements of Statistical Learning, second edition
