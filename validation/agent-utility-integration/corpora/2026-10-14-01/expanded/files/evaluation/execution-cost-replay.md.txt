---
id: EVAL-11-007
type: evaluation
title: Complete-output execution cost and replay evaluation
domain: "11"
summary: >-
  Compare execution, reuse or incremental repair only after specifying output
  equivalence, completion and state/history boundaries. Measure cold build, warm
  reuse, update, recovery, peak resources and total retained cost on declared
  workloads. A faster incomplete run is not an equivalent optimization. Requires
  realized versions, task coverage and independent replay controls; quality
  changes need separate candidate and entity evidence, while synthetic stress
  results do not predict population accuracy or production capacity.
tags: [entity-agnostic, large-scale, evaluation, experimentation, batch, incremental, provenance, uncertainty]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  tests: [SOL-13-001, SOL-02-002, AR-06]
  complements: [EVAL-11-001, EVAL-11-003, EVAL-11-006]
---

# Complete-output execution cost and replay evaluation

## What is measured

Engineering cost and contract conformance for a specified completed logical ER
workload. This evaluation does not estimate identity accuracy. Distinguish an
execution-only contrast, artifact-reuse contrast, incremental-maintenance
contrast and quality–budget frontier before choosing denominators.

## Why it matters

Throughput can appear better when hot blocks time out, expensive features are
skipped or fewer candidate pairs are admitted. Conversely, warm serving cost
can hide index construction, lineage retention or correction expense. Require
completion and the promised output equivalence before crediting saved work.

## Definitions and formulas

Name the run population, eligible input records, emitted pairs, unique eligible
candidates, completed comparisons, published dispositions and failures. Define
end-to-end latency from declared input availability to a consistent committed
bundle, not merely worker CPU time. Downstream convergence has a separate clock.

Let $U$ be the required logical comparison-unit frame, keyed by pair identity,
directed roles, observation revisions, required feature route and configuration/
context versions. Candidate-pair count is not necessarily $|U|$. Define disjoint
sets $C_{\mathrm{new}}$ and $C_{\mathrm{cache}}$ of unique valid completed units,
attributed to new execution or permitted reuse under a predeclared rule. Their
union $C\subseteq U$ is logical completion; unresolved required work is $U\setminus C$.
An explicitly permitted skip disposition can satisfy its contract; absent
required evidence cannot. Conflicting duplicate products are unresolved until
reconciled, not two successful units. Require set-level reconciliation or a
justified independent coverage/enumeration argument, not tile status or totals.

For measured wall duration $T>0$, logical-completion throughput is $|C|/T$;
new-execution throughput is $|C_{\mathrm{new}}|/T$. Report valid reused units,
unresolved/failed/pending required units, unique newly executed units and physical
attempts/retries separately. Repeated or unused computations consume resources
without increasing valid logical completion. A successful task missing an internal
route remains incomplete. Report task latency distributions and maximum, peak
memory, spill/storage/network bytes, external calls and correction effort.

A lifecycle cost account over a stated horizon $H$ is

$$
C_H=C_{\mathrm{build}}+C_{\mathrm{runs}}+C_{\mathrm{updates}}+C_{\mathrm{retention}}+C_{\mathrm{recovery}}.
$$

These are disjoint billed/resource categories, not a universal currency formula.
State resource units or a project-specific price conversion; do not double-count
update work inside run totals. Amortizing build cost requires an explicit reuse
horizon and rebuild schedule, not an invented number of future requests.

## Data requirements

Freeze the observation/configuration bundle, workload schedule, hardware/runtime,
index dependencies, initial state and authorized history. Capture complete task
manifests and realized outputs. For cache-free controls, do not reuse the derived
product being tested. For maintenance, reconstruct from an independent accepted
history and initial ID state rather than injecting the repaired final state into
the reference. Include an independent small candidate oracle for previously
unstored/truncated neighborhoods where possible.

## Sampling assumptions

A whole-run measurement is conditional on that workload and infrastructure.
Select stress cases from block/degree tails, expensive-feature routes, delete and
correction closures, index rebuilds and backlog bursts. Synthetic cases deliberately
oversample failures; they do not represent population frequencies. Representative
workload sampling needs an explicit frame and weights. Repeated runs sharing
hardware, caches or external-service congestion are not independent records.

## Interpretation

First compare candidate sets, evidence/dispositions, assignments/memberships,
master views and IDs under each promised equivalence. Byte equality, semantic
membership equality and as-of ID continuity are different claims. Fix tie/order
semantics or expose their permitted variation. Full snapshot recomputation is
not the correct historical comparator for a path-dependent policy; use
[AR-06](../architectures/incremental-continuous.md)'s history-qualified contract.

## Potential biases

Warm cache after one arm, omitted build time, different feature routes, unreported
retries, survivor-only latency and stopping before slow tasks complete bias cost
comparisons. Counterbalance arm order and separate cold, warm, update and recovery
regimes. Record failed runs under predeclared retry rules, not silently select
the fastest completed attempt. Profiling overhead and resource contention also
need disclosure.

## Known limitations

Equivalent behavior is not correct identity. A complete pair manifest does not
prove reference quality or global resolver correctness. Cheap average execution
can coexist with unacceptable tails. Unavailable replay evidence, erasure or
uncontrolled external nondeterminism limits claims explicitly. Distributed
consistency and remote effects require project protocols, not this metric card.

## Recommended comparisons

Compare [bounded local execution](../solutions/scalability/skew-aware-execution.md)
with resident-data batching and optional distribution on fixed logical inputs.
Compare cold rebuild with valid reuse; compare affected closure with equivalent
full replay on matched histories. Change budgets in a separate experiment with
[EVAL-11-001](candidate-recall.md) and [EVAL-11-003](entity-resolution-quality.md).
Use [EVAL-11-006](synthetic-metamorphic.md) for fault/retry witnesses.

For execution-only stochastic controls, freeze the realized workload or use a
justified coupling that preserves it. Independently realized retrieval/model
contrasts instead estimate expected cost and specified output behavior. Name the
joint candidate/evidence/disposition and assignment/membership objects or declared
projections compared: equal marginal edge inclusion can conceal different
correlated graphs. Predeclare practical equivalence margins, replication/coupling,
uncertainty and guardrails. Evidence only supports the evaluated projections and
populations, not equality of an unspecified whole distribution. A confidence
region that cannot resolve the chosen equivalence margins is inconclusive;
non-detection of difference never establishes equivalence.

Adoption requires project-declared equivalence, completion and practical cost,
freshness and harm guardrails. Reject unexplained divergence or unsafe recovery.
If completion/reference semantics cannot be verified, record inconclusive rather
than a speedup. Retain negative and mixed regime results.

## Statistical uncertainty

Repeat complete runs under a prespecified design; distinguish within-workload
runtime variability from transfer to future workloads. Use paired run differences
when matching is valid, report all attempts and intervals appropriate to the
workload/run sampling unit. Shared pair/entity dependencies matter for quality
uncertainty; they do not become independent latency replicates. Sparse extreme
closures support observed stress bounds, not a reliable population tail estimate.

## Related solutions and references

[DEC-13-001](../decisions/execution-strategy.md),
[SOL-13-001](../solutions/scalability/skew-aware-execution.md),
[artifact runs](../solutions/architecture/versioned-artifact-runs.md) and
[controlled comparisons](../solutions/experimentation/controlled-comparison.md)
connect engineering evidence to the chosen method. This protocol is Atlas
synthesis; no execution cost or ER result has been measured.
