---
id: "DEC-02-001"
type: "decision"
title: "Choose pipeline boundaries and extension mechanisms from expected change"
domain: "02"
summary: >-
  Choose how to separate pipeline responsibilities and expose controlled variation
  without assuming a framework is necessary. Compare explicit linear functions,
  fixed-skeleton hooks, strategy substitution, validated configuration, declarative
  policies, and dependency scheduling against expected changes and semantic
  contracts. Distinguish refactoring from intended behavior changes and execution
  lifecycle from topology. The proposed engineering experiments test change
  containment, compatibility, diagnosis, and migration costs; behavioral equivalence
  is not evidence of identity accuracy or a measured modularity improvement.
tags: [entity-agnostic, interpretable, provenance, experimentation, evaluation, batch, incremental]
maturity: "context-dependent"
evidence: "theoretically-motivated"
relations:
  complements: [DEC-12-001]
  evaluated_by: [EVAL-11-006]
---

# Choose pipeline boundaries and extension mechanisms from expected change

## Decision question

Which responsibilities should have explicit boundaries, and which change axes justify an extension mechanism rather than ordinary function replacement? Choose the least machinery that supports plausible changes and observable failures. This is Atlas design reasoning, not a measured claim that more modules improve maintainability or ER quality.

## Problem context

The target is a comprehensible, replaceable pipeline with declared artifacts, not a particular scorer or entity algorithm. [AR-01](../architectures/linear-modular.md) supplies a sequential reference; the [four architecture dimensions](../taxonomy/architecture-dimensions.md) keep topology, matching paradigm, resolution strategy, and lifecycle separate. Modularity does not require new topology names, a workflow service, or a new architecture ID. A linear composition can contain replaceable stages, and an incremental lifecycle can maintain that same composition.

Engineering errors include silently changing score meaning, accepting stale evidence, or hiding state behind a stable interface. Their consequences can be wrong pair dispositions, assignments, memberships, or consumer values. A cleaner code boundary alone establishes none of those outputs as true.

## Relevant assumptions

List expected changes: source mappings, normalization, candidate passes, evidence, scorer, thresholds, resolution constraints, execution placement, and update handling. Distinguish frequently varied parameters from independently evolving algorithms and rare migrations. Do not invent a project change history.

For a **pure refactor**, predeclare preserved observable behavior, including abstentions, failures, provenance obligations, and state transitions. Ignore irrelevant ordering only when order is not contractual; define numerical tolerances before inspection. An **intended semantic change**, such as replacing an additive score with a calibrated probability, needs migrated consumers and separate quality evaluation. Behavioral equivalence may preserve an existing identity error.

## Available solution families

These alternatives are operational design choices, not empirical rankings; several can coexist.

| Family | Mechanism and change axis | Principal limitation |
|---|---|---|
| Explicit linear functions | A visible caller passes artifacts through named functions; replace code at one boundary | Repeated callers may duplicate assembly and checks |
| Template-method fixed skeleton | A shared execution skeleton calls selected overridable hooks | Changing order or required steps strains the skeleton; inherited defaults can conceal behavior |
| Strategy/plugin substitution | Inject a selected implementation behind a declared stage role | Shared method signatures do not ensure semantic interchangeability; discovery/version management adds work |
| Validated configuration | Select approved implementations and parameters, validate combinations, expose the resolved plan | Syntax validation cannot prove semantic compatibility; defaults and overrides need tracing |
| Declarative policies | Express conditions, precedence, exceptions, and outcomes as inspectable policy artifacts | Conflict, missing-value, and evaluation-order semantics still require ownership |
| Dependency DAG/workflow scheduling | Declare prerequisite artifacts and schedule ready work, optionally materializing/reusing results | Undeclared dependencies invalidate reuse; a scheduler does not validate identity semantics |

As a concrete scheduler example, DVC documents dependency/output ordering, unchanged-stage skipping, and run-cache output recovery; its described DAG execution is sequential, not a promise of parallel speedup.[24]

## Criteria for choosing

Require a reason for each abstraction. A scorer experiment may need one injected strategy; changing thresholds may need only validated parameters. Independently reviewed rules may justify [rule composition](rule-composition.md), not arbitrary plugin loading. Branches, expensive reusable artifacts, or retries may justify a scheduler. A fixed workflow with occasional edits may need none of these.

Ask who changes what, how invalid combinations are rejected, what a reviewer sees, and how failures are reproduced. Contract compatibility includes eligible populations, identifier namespaces, missingness, score interpretation, time scope, and side effects, not just matching field names. Use the shared [module contracts](../taxonomy/module-contracts.md); a probability-consuming policy must not accept an identically shaped raw-score column without an explicit admissible conversion.

## Trade-off comparison

Boundaries can contain change only when dependencies are real and visible. A name-frequency feature may depend on the entire permitted corpus: adding one observation can change evidence for unchanged pairs. A retrieval change can invalidate calibration; a new accepted edge can affect memberships far beyond its endpoints. Passing a small table between modules does not eliminate these global data dependencies. Record snapshots, population scopes, indexes, policies, and state in dependency reasoning.

Extension convenience competes with debugging indirection, compatibility tests, configuration combinations, deployment packaging, and migration support. A plugin framework for one stable implementation can cost more than editing explicit functions. A fixed skeleton can become a fragile collection of exceptional hooks. A DAG can conceal missing edges behind apparently successful cache hits. Diagnose with resolved execution traces, cold-versus-reused comparisons, and deliberately incompatible inputs rather than module counts.

Batch, incremental, and hybrid execution compose with the chosen boundaries. Incremental operation requires dependency closure, deletion/correction handling, and state reconciliation. Hybrid periodic rebuilds can check drift, but do not make untracked changes correct between rebuilds. Feedback/iteration needs explicit context versions or unrolled iterations; calling a computation a DAG does not remove a cyclic semantic dependency.

## Good baseline candidates

Use one explicit sequential caller, named functions, explicit artifacts, immutable run inputs where feasible, and direct versioned parameters. Preserve logical boundaries even if stages share a process or storage. Add a strategy only at an exercised substitution point; add configuration validation for actual supported combinations. Compare broader frameworks against this baseline, not against deliberately tangled code.

## Prerequisites

Require an inventory of inputs, outputs, global reads, mutations, consumers, and compatibility obligations; authorized test access; and a reproducible baseline. Independent identity labels are unnecessary for a narrow equivalence test but necessary for claims of identity improvement. Versions and manifests support reproducibility, not truth. Artifact retention and promotion are owned by [versioned artifact runs](../solutions/architecture/versioned-artifact-runs.md), not by this boundary decision.

## Open questions

Which changes truly recur? Can a supposed local replacement avoid global state? Who owns incompatible-contract migration and rollback? Are team skills and diagnosis time sufficient to justify runtime indirection? Unsupported guesses about future extension demand are reasons to start small.

## Related evaluations

[DEC-12-001](experiment-design.md) complements this decision by controlling the comparison; [SOL-12-001](../solutions/experimentation/controlled-comparison.md) supplies the protocol. Freeze behavior and give baseline/challenger the same predeclared change tasks, starting snapshots, tools, and budgets. Record edit/review time, unrelated modules touched, escaped contract defects, diagnosis time, migration effort, and runtime/storage overhead. Repeated tasks and matched or rotated maintainers help expose skill/learning effects; report remaining confounding.

Counterbalance configuration/task order where feasible, use matched nonidentical task instances to limit solution carryover, and record prior familiarity. Separate initial setup/migration cost from later task cost. Where a small team or rare tasks prevent these controls, restrict the inference rather than attribute every time difference to modularity.

Use [EVAL-11-006](../evaluation/synthetic-metamorphic.md) for eligible behavioral properties and counterexamples, not an unearned maintainability or identity-accuracy score. Set practical cost margins and behavior guardrails before results. Adopt only with useful change-cost evidence and satisfied guardrails; reject costly indirection or semantic regressions; call sparse tasks or wide uncertainty inconclusive. An improved benchmark task time alone does not establish future maintenance gains.

## Links to Solution Cards

[Replaceable-stage pipelines](../solutions/architecture/replaceable-stage-pipelines.md) operationalize these boundaries and compatibility checks. The comparisons above are Atlas synthesis; the DVC source supports only the stated scheduling/cache example. No engineering trial or ER performance experiment is reported here.

## Sources

[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
