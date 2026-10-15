---
id: DEC-08-002
type: decision
title: Choosing explicit rule composition and conflict semantics
domain: "08"
summary: >-
  Choose how validated evidence, thresholds, semantic guards, source overrides,
  and review conditions compose into an auditable policy. Compare a small
  conditional or CASE ladder, parameterized predicates, ordered first-match
  rules, and declarative tables with explicit hit policies. Requires settled
  action semantics, evidence states, trust scope, and version compatibility.
  Covers overlap, shadowing, defaults, boundary cases, and cluster-wide guard
  placement without choosing membership structures, deriving thresholds, or
  claiming that rule engines improve entity-resolution accuracy.
tags: [entity-agnostic, interpretable, constraints, source-aware, missingness, provenance, human-review, governance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [DEC-08-001, DEC-07-001]
  evaluated_by: [EVAL-11-006, EVAL-11-003]
---

# Choosing explicit rule composition and conflict semantics

## Decision question

How should conditions combine when several rules apply, no rule applies, or required evidence is unavailable? Choose explicit composition semantics and their representation, not merely a framework. A conditional ladder and a table can express the same policy; a table with a different hit policy can express a different one.

This decision complements [DEC-08-001](resolution-strategy.md), which chooses independent decisions, assignment, or membership, and [DEC-07-001](scoring-strategy.md), which chooses evidence combination and score meaning. Neither responsibility moves here. [Thresholds and review](../solutions/decision-resolution/thresholds-abstention.md) supplies justified operating points; this card decides precedence and interaction once those points exist.

## Problem context

**Atlas synthesis:** ER policies often combine reliable-identifier shortcuts, learned scores, semantic restrictions, source exceptions, and review routing. Their individual plausibility does not establish safe joint behavior. An early score acceptance can bypass a valid veto; a broad source rule can hide a narrower exception; a null comparison can fall through to acceptance. These are policy-composition defects, separate from mistaken evidence or inadequate retrieval.

The output should preserve an action, reasons, unresolved state, applicable constraints, and versioned trace. Pair acceptance proposes a link; it does not authorize violating the selected membership contract. Review is an operational action with ownership and capacity, not a magic repair for every conflict.

## Relevant assumptions

Use [explicit evidence states](../solutions/comparison-features/evidence-states.md). Missing means unavailable observation; explicit null needs a declared meaning, potentially unknown or not applicable; invalid means a failed validity requirement. None automatically means disagreement. Define predicate behavior for each state, including incomparable namespaces and time scopes. Do not let a host language's truthiness or SQL unknown outcome define business policy accidentally.

Separate trustworthy hard constraints from soft adverse evidence. A qualified prohibition must carry an audited source, namespace, validity interval, and reliability rationale. Noisy identifier disagreement remains evidence unless those guarantees hold. A learned score cannot compensate for a genuine hard restriction; conversely, a diagnostic suspicion must not acquire veto authority merely because it is called a guard.

Unknown optional evidence differs from unresolved mandatory admissibility. An unknown or failed required guard defers/escalates before effects unless a separately authorized risk contract defines another treatment. A nonmatching prohibition row is not proof that the guard passed; compound conditions must preserve required unknown/error outcomes instead of coercing them to false.

## Available solution families

1. **Explicit conditional/CASE ladder:** keep a short, visible precedence sequence and an explicit default. Separate parameters from control flow when only thresholds or source settings vary.
2. **Pure predicate registry:** give reusable checks stable names, input contracts, and true/false/unknown/error outcomes. A registry alone does not define how those outcomes compose.
3. **[Ordered first-match rules](../solutions/decision-resolution/ordered-rule-policies.md):** externalize a deliberate sequence of conditions and terminal dispositions, with stable IDs and priority validation.
4. **[Declarative decision tables](../solutions/decision-resolution/declarative-decision-tables.md):** expose condition combinations and specify which overlapping hits determine the result. DMN 1.5 distinguishes First by row order from Priority by ordered output values.[23]
5. **Alternatives:** learned scores plus a small explicit guard layer, or a constraint-aware resolver for globally coupled decisions. Stateful production-rule chaining is a distinct computational choice, not a prerequisite for tables.

Fowler cautions that actions changing other conditions can make chaining difficult to understand; this is an author's design essay, not statistical evidence of rule-engine failure.[27]

## Criteria for choosing

Prefer the representation reviewers can inspect and change safely within the actual policy size and change pattern. Consider number of interacting conditions, domain-specific review needs, source variation, versioned trace requirements, and whether overlaps are deliberate. A complex condition can remain clearer as a named pure predicate than as many table columns.

Specify per-source override specificity before evaluation: for example, an exact ordered source pair and valid interval before a source-family setting before a global parameter. That is a proposed contract, not a universal precedence hierarchy. Reject ambiguous equal-specificity overrides; directional roles must not be silently swapped. Parameter overrides cannot disable mandatory semantic constraints without separately authorized policy change.

## Trade-off comparison

| Representation | What is explicit | Principal burden | Revealing failure |
|---|---|---|---|
| Small ladder + parameters | Control flow and early exits | Reviewing growing branches | Acceptance placed before a veto |
| Ordered rules + registry | Sequence and named checks | Priority, coverage, and overlap audit | Broad earlier condition shadows a later rule |
| Table + declared hit policy | Condition combinations and overlap semantics | Typed cells, completeness, runtime compatibility | First imported as output Priority |
| Score + guards / global resolver | Evidence versus admissibility | Score validity and decision-unit integration | Pair guards miss an infeasible cluster union |

This comparison is synthesis, not a ranking. A rule is structurally unreachable if its condition is unsatisfiable or earlier terminal conditions cover it throughout the eligible domain. A satisfiable rule with no observed triggers is merely unused on that observation set; source changes may activate it. Preserve proof assumptions or witnesses separately from trigger counts.

## Good baseline candidates

Start with a visible ladder: validate required input; handle trusted conflicts; enforce hard admissibility; apply the supplied acceptance/rejection boundaries; otherwise defer. Keep thresholds and source parameters named. If evaluating a table, translate the same policy first, with First semantics or disjoint rows as appropriate; only afterward test a separately declared change to conflict handling. Do not credit representation change for simultaneous threshold tuning.

## Prerequisites

Require action and evidence schemas, score/calibration applicability, trust ownership, source/time scope, default and tie conventions, review routes, and compatible versions. Emit policy/parameter/predicate versions, evaluated outcomes, selected rule, guard result, and input artifact references. Distinguish skipped conditions from false ones. Repeated evaluation on identical immutable inputs should be deterministic; duplicate delivery should not duplicate effects when event idempotency is promised.

Apply trusted premerge guards to the proposed cluster union where membership constraints demand it. If must-links and cannot-links make that union infeasible, preserve the conflict and escalate rather than silently relaxing a constraint. Postmerge diagnostics detect suspicious results but cannot retroactively prevent them; correction needs an authorized reversible path.

## Open questions

Who owns trust revisions, conflict escalation, and refreshed cluster guards? Can runtime upgrades preserve unavailable-state and hit-policy semantics? Use the [refactoring guide](../guides/rule-policy-refactoring.md) to resolve these questions with versioned witnesses.

## Related evaluations

Use [EVAL-11-006](../evaluation/synthetic-metamorphic.md) for boundaries, overlap witnesses, defaults, compatibility rejection, and conditional replay properties. Freeze inputs, scores, parameters, state, and budgets under [controlled comparison](../solutions/experimentation/controlled-comparison.md). Representation equivalence and maintainability are engineering claims. Use [EVAL-11-003](../evaluation/entity-resolution-quality.md) with independent supported references before claiming improved final ER output.

Adopt a refactor when declared semantic equivalence and engineering benefits are supported without critical violations. Reject known guard bypasses, incompatible-state coercion, or unmanageable ambiguity. Call incomplete contract coverage inconclusive. For changed policy, separately require project-defined practical quality/cost benefit and harm guardrails; behavioral passes or fewer conflicts alone do not establish it.

Assess engineering benefit through [matched extension/diagnosis tasks](../solutions/architecture/replaceable-stage-pipelines.md#how-to-evaluate), recording the project cost estimand and practical margin separately from behavioral conformance. Do not infer lower maintenance cost from equal decisions.

## Links to Solution Cards

The ordered-rules and decision-table cards supply alternative composition mechanisms. The existing threshold card remains the owner of operating-point justification. Source [23] is a deliberately versioned illustrative standard, not a latest-version claim; [27] supports the limited chaining caution. All ER-specific guidance here is synthesis; no ER experiment was run.

## Sources

[23] https://www.omg.org/spec/DMN/1.5/PDF — Decision Model and Notation, version 1.5
[27] https://martinfowler.com/bliki/RulesEngine.html — RulesEngine
