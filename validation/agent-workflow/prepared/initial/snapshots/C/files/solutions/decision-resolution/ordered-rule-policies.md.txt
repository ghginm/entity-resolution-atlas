---
id: SOL-08-005
type: solution
title: Ordered first-match policies with pure predicates
domain: "08"
summary: >-
  Compose ER dispositions through a deliberately ordered sequence of pure
  predicates and terminal rules. Keep hard admissibility separate from soft
  evidence, resolve source parameters before matching, and preserve unknown
  states, defaults, priority, and trace semantics. A small explicit conditional
  ladder is the credible baseline; an ordered registry adds named checks and
  versioned configuration, not automatic accuracy. Requires trusted constraint
  scope and compatible evidence, score, policy, and resolver contracts, with
  regression witnesses for overlap, boundaries, and cluster-wide guards.
tags: [entity-agnostic, interpretable, constraints, source-aware, provenance, missingness, human-review, governance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  addresses: [DEC-08-002]
  complements: [SOL-08-001]
  evaluated_by: [EVAL-11-006, EVAL-11-003]
---

# Ordered first-match policies with pure predicates

## Short summary

**Atlas synthesis:** evaluate a visible sequence of side-effect-free conditions against an immutable evidence/context snapshot and select the first satisfied terminal rule. Make applicability, priority, defaults, and unavailable-state handling inspectable. Rules produce proposals and explanations; state changes happen afterward under the selected resolver and authorization contract.

## Problem addressed

Repeated inline exceptions can make it unclear whether an identifier shortcut outranks a trusted incompatibility, whether a source-specific setting supersedes a global threshold, or why a case was deferred. Extracting rules can help inspection, but simply moving branches into configuration can preserve every existing defect while obscuring the sequence. A small conditional or CASE ladder remains a legitimate implementation, not technical debt by definition.

## Core mechanism

1. **Validate compatibility and scope.** Check evidence schema, source roles, time snapshot, predicate definitions, model/score meaning, calibration applicability where used, and policy/parameter versions. Reject an unsupported combination explicitly; do not interpret absent new fields as false.
2. **Resolve parameters.** Select an unambiguous override using declared specificity and validity scope. Keep this separate from condition matching. Record which source-pair setting or global fallback supplied each value.
3. **Evaluate pure predicates.** Named checks consume observations/context without mutating membership or consulting undeclared live state. Define true, false, unknown, and evaluation-error behavior. A rule must explicitly say whether unknown causes deferral, makes it inapplicable, or signals invalid input.
4. **Apply ordered terminal rules.** Use a unique sequence, or a complete documented tie-break for equal priorities. Earlier applicable rules win. Handle invalid mandatory evidence and trusted-constraint conflicts before permissive score acceptance when required by the contract. Keep soft disagreement available to scoring rather than converting it into an automatic veto.
5. **Emit the default and trace.** No hit is a named disposition, often unresolved/review, not an implicit acceptance. The trace records input references, versions, predicate outcomes, winning rule, parameter origin, and guards. Short-circuited checks are marked not evaluated, never false.

Before any effect, an unknown or failed **mandatory admissibility guard** must preserve its reason and defer/escalate unless a separately authorized risk contract specifies another treatment. Do not mark its prohibition rule inapplicable and then infer admissibility from a high-score hit. Optional soft/diagnostic unknowns need not veto. Define compound-predicate conjunction/error propagation and required evaluations explicitly; a short-circuited condition is not proof that an unresolved required guard passed.

For illustration, an audited hard incompatibility can block a high-score proposal; otherwise valid score at the supplied acceptance boundary can propose a link; an unavailable required score can defer. This specifies precedence, not a calibrated threshold or an identity truth claim.

## Theoretical explanation

With fixed inputs and pure predicates, a complete sequence determines one winning rule or default; overlapping rules make reordering consequential. These are construction properties, not ER results. Purity prevents a rule changing another's input. Fowler cautions about reasoning and debugging with action-driven chaining, not measured engine reliability.[27] This solution instead fixes sequence and inputs.

## Important variants

- **Inline ladder with parameters:** shortest useful baseline; a CASE expression needs explicit null/unknown handling and ordered WHEN branches.
- **Pure predicate registry:** reusable definitions with stable IDs and tests. The registry is not itself an execution order.
- **Ordered policy list:** rules reference predicates and immutable parameters, returning typed dispositions and reason IDs. Sequential numbering and numeric priority are interchangeable only under a documented mapping.
- **Learned score plus guards:** keep the scorer's meaning unchanged and add trusted admissibility checks and review routing. An uncalibrated score remains uncalibrated.
- **Proposal plus global guard:** pair policy proposes an action; assignment or membership feasibility is checked at the proper decision unit before effects.

## Assumptions and prerequisites

Require settled [membership/output semantics](../../decisions/resolution-strategy.md), [evidence states](../comparison-features/evidence-states.md), and justified [threshold/review parameters](thresholds-abstention.md). These are conceptual inputs, not requirements to adopt a particular technology. Supply namespace-qualified trust and validity scope for hard constraints. Missing, explicit null, invalid, and incomparable observations require separate handling where their meanings differ.

For source overrides, state the hierarchy, such as exact directional source pair before source family before global. Validate equal-specificity ambiguity and unknown sources. Do not mix override selection with terminal rule order or allow a permissive source exception to bypass a mandatory guard accidentally.

## Applicability conditions

Use this method where policy precedence is genuinely intended, the rule set stays reviewable, and deterministic explanations are useful. Prefer the simpler ladder when few branches change rarely. Prefer [decision tables](declarative-decision-tables.md) when condition coverage and overlap validation matter more than an intentional sequence. Neither representation resolves global membership automatically.

## Advantages

Stable rule and predicate IDs localize changes and explanations. Named parameters allow operating-point revisions without rewriting control flow. Explicit defaults expose unresolved cases. Pure conditions support differential and boundary testing independently of side effects. These are proposed engineering benefits; their value should be checked against maintenance burden.

## Trade-offs and failure modes

A broad early rule can shadow a narrower one. **Structural unreachable** means no eligible input can reach the later terminal rule given earlier conditions; retain a proof or bounded-domain analysis and its assumptions. **Observational zero trigger** means it did not win on a particular sample. The latter cannot prove dead code, and a matching-but-suppressed count is different again.

An early unconditional catch-all hides everything after it. Threshold inclusivity mistakes misroute equality cases; equal-priority rules without a tie-break undermine determinism. Coercing missing score to zero can manufacture rejection. A trace evaluating every rule in a diagnostic pass must not claim all conditions were evaluated during the short-circuited decision.

Trusted guards belong before the merge they prohibit. Check the full proposed union: two individually plausible edges can imply a cluster containing incompatible records. Conflicting must-link/cannot-link obligations require escalation or a declared infeasible output, not arbitrary priority-based relaxation. Postmerge diagnostics can identify suspicious clusters but do not establish preventive protection or identity accuracy.

## Relationships with other methods

This solution addresses [DEC-08-002](../../decisions/rule-composition.md) by making sequence explicit and complements [SOL-08-001](thresholds-abstention.md) by implementing its supplied actions and boundaries without deriving them. Tables are substitutable composition representations; constraints and learned scores are compatible inputs. The [refactoring guide](../../guides/rule-policy-refactoring.md) covers migrations and versioned witnesses.

## How to evaluate

Under [EVAL-11-006](../../evaluation/synthetic-metamorphic.md), compare the existing explicit ladder and extracted policy on identical fixtures, source roles, parameters, scores, and state. Cover overlaps, both threshold equalities, absent/null/invalid evidence, override ambiguity, trusted conflicts, no-hit defaults, cluster infeasibility, and incompatible versions. Test deterministic output on fixed input; require event replay idempotency only where promised, including no duplicate review request or merge effect.

Adopt an equivalence refactor only after reviewed differences are resolved and the declared engineering benefit exceeds maintenance cost. Reject critical guard bypasses or unexplained output changes. Treat incomplete coverage or unsettled policy as inconclusive. If dispositions intentionally change, use independent [EVAL-11-003](../../evaluation/entity-resolution-quality.md) evidence and [controlled comparison](../experimentation/controlled-comparison.md) for practical quality/cost and harm criteria. Regression agreement alone cannot establish better ER.

For the engineering claim, use the [matched change/diagnosis task protocol](../architecture/replaceable-stage-pipelines.md#how-to-evaluate) with its cost estimand and predeclared practical margin; conformance alone does not measure maintenance benefit.

## Research opportunities

Test whether named predicates and traces reduce review/change errors compared with the small ladder without adding runtime or governance burden. Separate representation effects from revised priorities or thresholds. An unused rule may motivate better witness coverage rather than deletion.

## References and evidence limitations

The mechanism and ER safeguards are Atlas synthesis. Source [27] supports only the attributed caution about implicit chaining. No production policy, behavioral suite, measured maintainability benefit, or ER accuracy experiment is reported.

## Sources

[27] https://martinfowler.com/bliki/RulesEngine.html — RulesEngine
