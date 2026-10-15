---
id: SOL-08-006
type: solution
title: Declarative decision tables with explicit hit policies
domain: "08"
summary: >-
  Represent ER policy as typed input conditions and output dispositions with a
  declared hit policy, rather than assume every matching row should fire or
  that row order always determines priority. Distinguish disjoint rules,
  equal-output overlaps, output priority, ordered first match, and multiresult
  collection. Compare against a small conditional ladder under unchanged
  evidence, thresholds, and trust. Requires explicit unavailable-state,
  override, default, compatibility, and trace contracts; table readability and
  behavioral conformance do not establish better final ER accuracy.
tags: [entity-agnostic, interpretable, constraints, source-aware, missingness, provenance, human-review, governance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  addresses: [DEC-08-002]
  alternative_to: [SOL-08-005]
  evaluated_by: [EVAL-11-006, EVAL-11-003]
---

# Declarative decision tables with explicit hit policies

## Short summary

**Atlas synthesis:** specify input columns, typed conditions, output dispositions, and the policy for multiple matching rows. A table is a policy representation, not a promise of business-user autonomy or a reason to install a rule engine. A small explicit conditional/CASE ladder is the comparison baseline.

## Problem addressed

A long ladder can conceal gaps and overlaps. A table exposes combinations but is misleading unless readers agree whether row order, output priority, or all hits determine the result. Transferring conditions without that contract changes behavior rather than merely refactoring it.

## Core mechanism

Declare the evidence/context schema first. Columns may express qualified identifier status, trust scope, source pair, required-score availability, score region, and cluster admissibility. Keep complex comparisons as named pure predicates with versioned definitions. Output columns carry the action and its compatible decision payload; rule IDs and explanatory annotations support audit. Specify unavailable and invalid inputs explicitly instead of using a blank cell ambiguously as wildcard, unknown, or default.

The versioned DMN 1.5 standard provides an illustrative vocabulary for hit policies; these are not claims about a latest version or a selected product.[23]

| Hit policy | Supported semantic distinction | ER design question |
|---|---|---|
| Unique | Overlap is forbidden.[23] | Can conditions be partitioned into disjoint regions? |
| Any | Overlap is allowed only with equal outputs, ignoring annotations.[23] | Do apparently redundant rows really return the same disposition payload? |
| First | Select the first matching row by rule order.[23] | Is sequential precedence intentional and reviewable? |
| Priority | Select by ordered output values, independently of row order.[23] | Is there an authorized ordering of actions? |
| Collect | Return all hits; aggregation requires a supported, appropriately typed single-output table.[23] | Does the consumer expect multiple results rather than one action? |

For example, First can preserve an existing ladder's precedence. Unique requires disjoint conditions, possibly separating score acceptance from guard failures. Priority requires explicit output ordering: putting `review` above `accept` is a policy decision, not a property of confidence. Collect can gather diagnostic findings, but must not send contradictory terminal actions to a consumer expecting one disposition. Summing collected values does not make them a probability.

**Compound outputs:** DMN 1.5 permits Collect **without an operator** when several actual outputs are returned; count, sum, min and max operators are undefined for that compound table. Annotation-only additions do not create another output clause. Authorized postprocessing of the returned list is separate.[23] For compound Priority, compare ranked output clauses in precedence order: left to right in horizontal tables, top to bottom in vertical tables, using each clause's declared output-value order. Unranked outputs remain in the payload but do not rank it; annotations do neither.[23] For ER use, declare the tie/result contract; if tied ranks leave unequal unranked payloads, do not assume deterministic row-order selection.

Define no-hit behavior independently of overlap behavior. DMN 1.5 permits default outputs.[23] For this ER synthesis, make unresolved/review, reject, or another authorized fallback explicit and typed. A default output is not an input null and not automatically a true nonmatch. Validate that unsupported inputs and runtime errors cannot silently use a permissive default.

Before effects, resolve mandatory admissibility checks independently of whether an acceptance row hits. An unknown or failed mandatory guard defers/escalates with its reason unless a separately authorized risk contract specifies another treatment; marking its prohibition row inapplicable does not establish admissibility. Optional soft/diagnostic unknowns follow their own contract. Define conjunction and error propagation so short-circuiting cannot conceal a required unresolved check.

## Theoretical explanation

A table separates the set of satisfied conditions from selection semantics. Under Unique, proving disjointness addresses overlap but not completeness. Under First, overlap is resolved by sequence, not removed. Under Any, checking action labels alone is insufficient if other decision outputs differ. Under Priority, changing output ordering can change decisions while moving rows does not. These implications follow from the specified policies, not ER measurements.[23]

Tabulation can make finite categorical combinations easier to inspect, while complex temporal and namespace predicates remain external definitions. Neither a visual grid nor static coverage proves that the observations are trustworthy or that the resulting actions recover real identity.

## Important variants

- **Disjoint table:** explicit condition partitions with Unique and separate no-hit checks.
- **Ordered table:** First reproduces a ladder, including its shadowing risks.
- **Output-priority table:** Priority selects an authorized disposition ranking; it is not numeric row priority.
- **Diagnostic multi-hit table:** Collect gathers findings for a separate policy, without an operator for compound outputs; preserve dependence and provenance rather than treating findings as independent evidence.
- **Learned score plus table guards:** the table maps score regions and admissibility to actions without changing the scorer's statistical interpretation.

Use typed parameters rather than copying thresholds through many cells. Resolve source-specific settings before matching, or make mutually exclusive override scope explicit in rows. A table with explicit hit policy is distinct from a stateful production-rule engine; Fowler's design essay cautions about action-driven chaining, not about all tabular policies.[27]

## Assumptions and prerequisites

Require [evidence-state meanings](../comparison-features/evidence-states.md), authorized [actions and operating points](thresholds-abstention.md), constraint trust, and the [output contract](../../decisions/resolution-strategy.md). Document missing versus explicit null, invalid, incomparable, and valid disagreement. Typed cell expressions and the runtime must agree on unknown/error handling, numeric precision, cutoff inclusivity, and interval endpoints.

Define source override specificity and effective dates; reject equal-specificity collisions. Directional source pairs need directional lookup. Carry table, predicate, parameter, evidence, model/calibration, and resolver compatibility versions. DMN specifies hit-policy meaning but does not supply this project's trust, override hierarchy, or ER evaluation.

## Applicability conditions

Use tables when policy owners need to review interacting categorical conditions or deliberate overlap semantics, and their tooling can validate and preserve that contract. Keep a short ladder when it is easier to understand and maintain. Choose a globally constrained resolver when the action requires assignment or cluster feasibility; adding columns does not replace that responsibility.

## Advantages

Rows and typed columns can expose gaps and contradictory actions, support traceable policy reviews, and permit representation changes without altering evidence estimation. These are engineering hypotheses to verify. A table can be interpreted, generated, or reviewed alongside ordinary code; a rule-engine dependency is optional.

## Trade-offs and failure modes

Row explosion can hide logic more effectively than a small ladder. First permits structural shadowing: a later condition may be satisfiable but never selected because earlier rows always cover it. Zero observed triggers is only a sample fact. Unique and Any violations are contract errors, not invitations to silently choose a convenient row. A broad wildcard or wrong null coercion can swallow exceptional states. Priority can mask a substantive conflict behind an inadequately justified action ranking.

Trace every matching row when required, the selected result, hit policy, default use, and unavailable/error outcomes; distinguish diagnostic reevaluation from the actual decision. DMN does not standardize runtime access to matched-rule annotations, so auditable trace capability needs an explicit implementation contract rather than assumed support.[23]

Apply trusted guards before effects. For a proposed cluster union, inspect all required member constraints, not only the trigger pair. Infeasible hard obligations need escalation without unauthorized relaxation. A postmerge diagnostic table can flag possible contamination but does not prevent it or prove a false merge.

## Relationships with other methods

This solution addresses [DEC-08-002](../../decisions/rule-composition.md). The sole `alternative_to` edge points to [SOL-08-005](ordered-rule-policies.md): both compose conditions, but non-First tables expose different overlap choices. [SOL-08-001](thresholds-abstention.md) owns thresholds. In [replaceable-stage pipelines](../architecture/replaceable-stage-pipelines.md), exchange only semantically compatible dispositions, not a table-specific result list. Follow the [refactoring guide](../../guides/rule-policy-refactoring.md) for migration controls.

## How to evaluate

Use [EVAL-11-006](../../evaluation/synthetic-metamorphic.md) to compare a frozen ladder and equivalent table on the same witnesses. Include disjointness/completeness, same-versus-different output overlaps, deliberate First row swaps, Priority output-order changes, missing/invalid states, cutoff equality, defaults, source override collisions, incompatible versions, and conditional replay idempotency. Do not count a representation rewrite and threshold revision as one isolated mechanism.

Adopt when contract equivalence or declared policy differences are reviewed and engineering benefit exceeds table/tooling burden without critical violations. Reject silent policy substitution, guard bypass, or unreviewable expansion. Treat inadequate witness coverage or unsettled semantics as inconclusive. For intentional action changes, use independent [EVAL-11-003](../../evaluation/entity-resolution-quality.md) references and [controlled comparison](../experimentation/controlled-comparison.md) with project-defined quality/cost gains and harm limits; a clean table or lower conflict count is not accuracy evidence.

Measure engineering benefit separately with the [matched change/diagnosis task protocol](../architecture/replaceable-stage-pipelines.md#how-to-evaluate), a declared cost estimand and practical margin; equal behavioral violation rates cannot establish lower maintenance cost.

## Research opportunities

Compare authoring/review errors, trace completeness, and maintenance effort for ladder versus table while holding policy fixed. Test a different hit policy separately only when its changed conflict behavior is authorized.

## References and evidence limitations

Source [23], sections 8.2.11–8.2.12, supports the cited hit-policy/default distinctions; [27] is a design caution. ER integration and evaluation are synthesis. No table runtime, fixture suite, or ER accuracy experiment was executed here.

## Sources

[23] https://www.omg.org/spec/DMN/1.5/PDF — Decision Model and Notation, version 1.5
[27] https://martinfowler.com/bliki/RulesEngine.html — RulesEngine
