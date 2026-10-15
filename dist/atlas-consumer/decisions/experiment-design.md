---
id: "DEC-12-001"
type: "decision"
title: "Choose an experiment design that separates mechanisms from system effects"
domain: "12"
summary: >-
  Choose between fixed-candidate comparisons, stage replacements, ablations,
  factorial designs, and end-to-end evaluations according to the question an
  entity-resolution experiment must answer. The card distinguishes conditional
  component value from deployable system value, requires explicit identity,
  reference, split, and cost assumptions, and explains when controls conceal
  rather than remove interactions. A simple frozen baseline remains credible;
  uncertainty and behavioral guardrails determine whether to adopt, reject, or
  gather more evidence, without asserting unmeasured gains.
tags: [experimentation, evaluation, uncertainty, entity-agnostic, provenance]
maturity: "context-dependent"
evidence: "theoretically-motivated"
relations:
  complements: [SOL-12-001]
  evaluated_by: [EVAL-11-001, EVAL-11-002, EVAL-11-003, EVAL-11-006]
---

# Choose an experiment design that separates mechanisms from system effects

## Decision question

Which comparison can distinguish the proposed mechanism from plausible competing explanations, while also revealing consequences at the promised output? Choose a design, not a preferred algorithm. Domain 12 owns this choice and its execution protocol; domain 11 owns metric definitions and inference from the reference.

## Problem context

A new normalization may change both retrieval keys and comparison evidence. A scorer evaluated only on its own candidates mixes ranking value with admission effects. A safer pair policy may reduce links yet fragment entities. Consequently, an experiment needs a target artifact—candidate pairs, scores, dispositions, assignments, memberships, or consumer attributes—and a declared population and error cost. There is no universally sufficient aggregate score.

## Relevant assumptions

Settle same-as versus related-to, time scope, namespaces, eligible source pairs, cardinality, and unresolved outputs before comparing. Assume only authorized observations and label access; the Atlas supplies no project data. A controlled comparison estimates value under its controls, not automatically under deployment shift. Evaluation labels must be independent of fitting, rule imitation, and adaptive test-case discovery. Independence from development does not itself make a holdout representative.

## Available solution families

| Design | Question answered | What it does not establish |
|---|---|---|
| Fixed candidate pool | Which scorer or evidence representation works better on the same admitted pairs? | Retrieval completeness or benefit outside that pool |
| Stage replacement | What changes when one module is replaced, with its input contract and other modules fixed? | Transfer after upstream distributions or downstream policy change |
| Ablation | What is the incremental contribution of a pass, feature group, constraint, or context signal in this configuration? | Universal standalone value or unique causal explanation |
| Small factorial | Does one change's effect depend on another specified change? | Interaction on every score scale or untested combinations |
| End-to-end comparison | Which feasible full configuration better meets the intended output and budget? | Attribution to a single changed component |

These are design choices within the [controlled-comparison protocol](../solutions/experimentation/controlled-comparison.md), not extra ER algorithms. Use isolated and end-to-end checks together where both attribution and adoption matter.

## Criteria for choosing

Start with the strongest competing explanation. If gains might come from extra candidates, use a common fixed pool for the scorer comparison and separately assess retrieval. If copied evidence may be counted twice, ablate dependency groups, not arbitrary individual columns. If a constraint changes whole-cluster feasibility, freeze scored evidence but evaluate final memberships. If normalization changes keys and similarity jointly, consider a crossed design with each change independently switchable.

NIST describes two-level full factorial designs with all factor combinations and analysis columns for main effects and interactions.[20] For an illustrative retrieval factor $A$ and scoring factor $B$, define $M_{ab}$ as the same oriented performance metric, on the same target reference, at settings $a,b\in\{0,1\}$. The derived interaction contrast is

$$
I=(M_{11}-M_{10})-(M_{01}-M_{00}).
$$

It asks whether the scoring change's difference varies with retrieval setting. This is a score-scale- and design-specific contrast, not a claim of causality in deployment. Nonlinear metrics, unequal tuning allowances, changed populations, or infeasible cells alter its meaning. Declare each cell's fitting/calibration protocol; do not silently reuse a probability map invalidated by retrieval.

## Trade-off comparison

Fixed inputs make differences easier to attribute but can hide the failure they were chosen to exclude. A union pool can support a conditional scorer comparison, yet is not any production retriever's output; preserve admission provenance. Ablating a required module without a valid replacement creates an invalid pipeline, not evidence of its value. End-to-end comparisons capture dependencies but require more cost and cannot explain every gain. Factorial designs expose specified interactions at added run cost; incompatible cells require a revised question, not fabricated outputs.

An oracle replacement using independently known truth can diagnose a bottleneck on that reference support. It is neither deployable nor a universal upper bound: altered evidence can change assignment competition or closure in unfavorable ways.

## Good baseline candidates

Use the current reproducible configuration and one credible simple alternative compatible with the identity contract: for example, exact blocking plus an interpretable scorer and explicit threshold policy. For mechanism isolation, change one admissible stage first. For an ablation, compare the full configuration with the same configuration minus one optional information group under a declared retuning rule. Match tuning opportunity and report resource differences rather than disguising additional search as method value.

## Prerequisites

Record the baseline, challenger, expected output, controls, independent development/final partitions, reference support and unknown-label policy. Predeclare practical margins, statistical uncertainty procedure, harm/cost guardrails, and stopping rules using actual project consequences. Use the [experiment-plan template](../guides/experiment-plan-template.md); no numerical project threshold is supplied here.

## Open questions

Can the label design resolve a practically important effect? Which interactions deserve a factorial rather than a single-stage comparison? Is future-source transfer the target, or recurring observations of existing identities? A null result may reflect redundant evidence, missing candidates, poor estimation, or insufficient precision; these require different follow-ups.

## Related evaluations

Use [candidate recall](../evaluation/candidate-recall.md) for admission, [pairwise quality/calibration](../evaluation/pairwise-calibration.md) for scores and dispositions, and [entity quality](../evaluation/entity-resolution-quality.md) for final assignments/memberships. [Behavioral tests](../evaluation/synthetic-metamorphic.md) check contract violations in a declared generated domain; passing them cannot establish real-world accuracy. Their denominators and interpretation are separate from population-quality metrics.

## Links to Solution Cards

[SOL-12-001](../solutions/experimentation/controlled-comparison.md) complements this decision by operationalizing freezes, dependency validity, paired analysis, and reporting. [Probability-sampled review](../solutions/ground-truth/probability-sampled-review.md) can supply evaluation evidence; [targeted review](../solutions/ground-truth/targeted-active-review.md) serves adaptive discovery and must not silently replace it. NIST supports the factorial structure, not ER-specific gains; the remaining design choices are Atlas synthesis. No Atlas ER experiment has been run.

## Sources

[20] https://www.itl.nist.gov/div898/handbook/pri/section3/pri3331.htm — NIST/SEMATECH e-Handbook: Two-level full factorial designs
