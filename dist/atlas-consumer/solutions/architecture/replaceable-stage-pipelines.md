---
id: "SOL-02-001"
type: "solution"
title: "Replaceable-stage pipelines with explicit semantic contracts"
domain: "02"
summary: >-
  Separate pipeline responsibilities through explicit artifacts and semantic
  compatibility checks, starting from ordinary functions rather than a mandatory
  plugin framework. Introduce hooks, strategies, validated configuration, policies,
  or dependency scheduling only at justified change points. Preserve source,
  population, time, score, and state meaning across substitutions; expose global
  dependencies and migration obligations. Controlled refactor and extension
  experiments assess behavior and engineering costs. Equivalent outputs do not
  establish identity truth, and modularity is not an observed accuracy gain.
tags: [entity-agnostic, interpretable, provenance, experimentation, evaluation, batch, incremental]
maturity: "context-dependent"
evidence: "theoretically-motivated"
relations:
  addresses: [DEC-02-001]
  evaluated_by: [EVAL-11-006]
  used_by: [AR-01]
---

# Replaceable-stage pipelines with explicit semantic contracts

## Short summary

Make stage inputs, outputs, and assumptions visible, then expose only justified variation points. This solution addresses [DEC-02-001](../../decisions/pipeline-modularity.md) and is used by the [AR-01 baseline](../../architectures/linear-modular.md). It proposes change containment and diagnosis benefits under explicit dependencies; these are Atlas design hypotheses, not measured improvements or guarantees of ER accuracy.

## Problem addressed

A monolithic caller can mix retrieval, scoring, policy, and mutation so that a small change has unknown reach. Conversely, a framework can distribute the same hidden coupling across plugins and configuration. The goal is controlled replacement, not maximizing classes, stages, or abstraction layers.

## Core mechanism

1. **Name responsibilities and artifacts.** Start with explicit calls for preparation, candidates, comparison, scoring, policy/resolution, and output. Follow [module contracts](../../taxonomy/module-contracts.md), allowing physical co-location without erasing responsibilities. Require membership resolution only when the output demands it.
2. **Declare semantic compatibility.** Record each stage's eligible population, namespace/time scope, missingness, score scale, versions, state reads/writes, constraints, and failure dispositions. Validate structural shape and semantic requirements before composition; reject or explicitly migrate incompatible contracts.
3. **Expose dependencies.** Pass artifacts and context explicitly. Inventory external dictionaries, corpus statistics, indexes, calibration, policies, and mutable membership state. A stage's small direct input does not prove its dependency scope is local.
4. **Assemble transparently.** Begin with a visible caller and versioned parameters. If configuration is needed, allowlist components, validate parameters and cross-stage constraints, reject unknown selections, and retain the resolved plan including defaults/overrides. Configuration is not unrestricted executable code.
5. **Separate replacement from migration.** State whether observable behavior must remain unchanged or is intentionally revised. For incompatible changes, version the contract, identify affected consumers/artifacts, provide an explicit conversion or coordinated replacement, and retain a rollback route.

Illustratively, two scorers can both return `pair_key, score` while one emits an additive rank and the other a population-conditioned probability. Field equality is not compatibility with a probability threshold policy. A replacement must preserve the promised meaning or revise calibration/policy and evaluate the resulting system; merely renaming `score` hides the migration.

## Theoretical explanation

When a replacement preserves all relied-on semantics and dependencies, other modules need not change solely to accommodate its internals. That conditional argument does not establish how often preservation is possible or whether total maintenance cost falls. Explicit boundaries can also reveal that a proposed local change is actually global. Attribution requires controlled comparisons; interface cleanliness alone proves neither behavior nor identity truth.

## Important variants

Use ordinary functions as the reference implementation. Add bounded hooks for a fixed skeleton or an injected strategy at an independently changing role; configuration can select supported combinations. The [decision comparison](../../decisions/pipeline-modularity.md#available-solution-families) owns the complete alternative menu and DAG example. [Rule composition](../../decisions/rule-composition.md) owns declarative-policy semantics; [versioned artifact runs](versioned-artifact-runs.md) owns materialization, reuse and promotion. None requires adopting all the mechanisms or a framework.

## Assumptions and prerequisites

Require settled identity/output semantics, an inventory of dependencies and side effects, a reproducible reference execution, and access-controlled test inputs. Define compatibility ownership and rejection behavior. No-label refactor checks are possible; identity-quality claims require suitable independent evidence. State, time, and source assumptions cannot be reconstructed safely from column names.

## Applicability conditions

Use when source handling, scorers, policies, or execution requirements have credible independent change pressure. Preserve the [four dimensions](../../taxonomy/architecture-dimensions.md): batch, incremental, and hybrid maintenance can share boundaries without prescribing a scorer, resolver, or topology. Incremental updates require justified dependency closure and corrections/deletions; hybrid maintenance combines updates with periodic reconciliation. A full rebuild is a useful reference only when it uses equivalent observation/validity time, context, policy, and state semantics. Explicit iteration/context versions are needed for feedback, not a disguised cyclic DAG.

## Advantages

The intended benefits are inspectable assembly, earlier incompatibility rejection, isolated experiments, and traceable migration. Plain functions can supply these benefits without a framework. They remain engineering objectives to test against costs, not assertions that every stage can be replaced independently.

## Trade-offs and failure modes

Global data dependencies are the critical counterexample. A corpus-frequency change may alter evidence for unchanged observations; a retrieval change can invalidate calibration; a membership change can propagate to downstream views. A scheduler missing those dependencies can reuse stale artifacts while every schema check passes. Compare cold recomputation with reuse after deliberate dependency changes.

Hooks, plugin registries, configuration overrides, adapters, and scheduler state increase debugging surfaces and supported combinations. Excessive boundaries add serialization/storage costs; permissive adapters can silently weaken meaning. Keep explanations and failure traces linked to the resolved component/contract versions. Stage replacement is inappropriate when its required semantics cannot be met; choose an explicit migration rather than accepting an apparently compatible shape.

## Relationships with other methods

[Controlled comparison](../experimentation/controlled-comparison.md) separates engineering refactors from semantic experiments. A [run manifest](../../guides/run-manifest-template.md) records resolved execution context; [decision provenance](../../guides/decision-provenance.md) explains outputs. Neither documentation nor component versioning establishes correct identities. Incremental composition complements [AR-06](../../architectures/incremental-continuous.md), rather than replacing its state/reconciliation responsibilities.

Retrieve contracts for boundary substitution, the manifest only for realized-run packaging, provenance only for explanation, and AR-06 only for evolving state. A single scorer injection need not load every lifecycle guide.

## How to evaluate

For pure refactoring, run baseline/challenger on identical fixtures and initial state. Predeclare observable equivalence, allowable numerical tolerances, ordering exceptions, provenance, failure behavior, and state transitions. Retain mismatches and crashes. Use [EVAL-11-006](../../evaluation/synthetic-metamorphic.md) for conditional properties; do not demand symmetry or order invariance from a contract that legitimately lacks them.

Inject incompatible score semantics, changed global context, missing dependencies, and configuration conflicts; require rejection, invalidation, or declared migration. For engineering value, assign matched extension, diagnosis, and migration tasks under equal budgets. Measure task/review time, unrelated edits, escaped defects, and execution/storage overhead. Use the [task-order/familiarity controls](../../decisions/pipeline-modularity.md#related-evaluations) to reduce solution carryover, and disclose remaining learning effects. Predeclare worthwhile margins and guardrails. Adopt if supported, reject harmful complexity, and call weak evidence inconclusive. For intended semantic changes, add the appropriate independent [pair](../../evaluation/pairwise-calibration.md) and [entity-quality](../../evaluation/entity-resolution-quality.md) evaluations; equivalence to a mistaken baseline is not truth.

## Research opportunities

Test whether benefits persist across additional change axes and maintainers, and whether coupling reappears through shared statistics or state. A favorable scorer substitution task does not establish lower deletion/migration cost. Use negative results to remove unnecessary extension machinery, not merely add more hooks.

## References and evidence limitations

The linked decision's DVC example illustrates declared-dependency stage ordering and reuse.[24] It does not establish ER contract correctness, framework superiority or engineering savings. This solution's mechanisms and trade-offs are Atlas design reasoning. No engineering trial, dataset processing, training or ER performance experiment is reported.

## Sources

[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
