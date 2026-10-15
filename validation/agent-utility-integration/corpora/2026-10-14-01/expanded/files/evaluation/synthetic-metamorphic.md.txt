---
id: "EVAL-11-006"
type: "evaluation"
title: "Synthetic fixtures, metamorphic relations, and behavioral contract violations"
domain: "11"
summary: >-
  Evaluate entity-resolution behavior on controlled fixtures and declared
  transformations rather than infer accuracy from unlabeled production output.
  The protocol distinguishes known synthetic identity, metamorphic relations,
  and property-based contract checks; it measures violation rates only within
  the generated test domain. Policy, cardinality, state, namespaces, and temporal
  preconditions determine which properties are legitimate. Paired comparisons,
  counterexample review, and regression suites support diagnosis, while an
  independent real-reference evaluation remains necessary for world accuracy.
tags: [evaluation, experimentation, constraints, uncertainty, entity-agnostic, provenance, no-labels]
maturity: "context-dependent"
evidence: "theoretically-motivated"
relations:
  tests: [SOL-08-001, SOL-08-002, SOL-08-003, SOL-08-004, SOL-02-001, SOL-02-002, SOL-08-005, SOL-08-006, AR-06]
  complements: [EVAL-11-003]
---

# Synthetic fixtures, metamorphic relations, and behavioral contract violations

## What is measured

Measure conformance to a specified behavior contract on an explicitly generated domain. A controlled fixture has author-specified latent identities or decisions; a metamorphic test checks a justified relation between outputs before and after transformation; a property test checks an invariant over admissible generated inputs. These roles can overlap but are not interchangeable measures of real ER accuracy.

Chen, Cheung, and Yiu derive follow-up cases from apparently successful input/output cases using problem-domain knowledge, including situations without a complete output oracle.[19] Their examples justify conditional relations, not universal invariance. Property-based testing generates inputs for declared assertions; the official Hypothesis introduction also treats it as an addition to example tests, not their automatic replacement.[22] The ER examples and metrics here are Atlas synthesis.

## Why it matters

A regression can violate source namespaces, lose records, or convert unknown evidence to a nonmatch before population-quality metrics expose the problem. A reproducible counterexample identifies a narrower failure than a changed aggregate score. Conversely, a defective property can label correct behavior a bug; checking the contract is part of evaluation, not an excuse to force outputs toward preferred identities.

## Definitions and formulas

Let $Q$ specify a generator, its admissible parameters, and transformation distribution. For property $p$, let $H_p(x)$ mean its prerequisites hold and $R_p$ be its expected relation on the output of configuration $f$. A case $x$ includes its full base fixture, transformed inputs, and any controlled initial state. Define $v_p(x)=1$ when $R_p$ is violated and zero otherwise, only when $H_p(x)$ holds and the case executes with a valid oracle.

For a fixed suite $S$, the descriptive violation fraction is

$$
\widehat V_p=\frac{\sum_{x\in S_p}v_p(x)}{|S_p|},
$$

where $S_p$ contains the eligible, executed, oracle-resolved cases for $p$. An empty denominator is undefined, not a pass. Report generated, ineligible, oracle-unknown, execution-error, and evaluated counts separately; a timeout or crash is a separate failure guardrail, not an invisible omission. An abstention is an output assessed against the contract, not automatically oracle-unknown. Unknown real labels are never substituted as synthetic nonmatches.

With genuinely independent draws from fixed $Q$ and valid prerequisites/oracles, the estimand is $V_p(Q)=P_Q(v_p=1\mid H_p,\text{valid execution/oracle})$, accompanied by execution/oracle-coverage rates. It is not the probability of an ER error in the world. For adversarially selected or adaptive cases, report a suite-specific fraction and counterexamples, not a probability-sample estimate. Keep property-level and fixture-level summaries distinct; counting many transformations of one seed does not create independent fixtures.

## Data requirements

Specify latent identity/time/source scope, raw observations, namespace-qualified identifiers, eligibility/cardinality, declared normalization, trusted constraints, expected outputs or relations, and allowed exceptions. Preserve a seed-to-variant mapping and component versions. Keep fixture truth outside model inputs, unless an oracle substitution is the explicitly named diagnostic. Separate identity-preserving formatting from identity-changing namespace, legal-entity, or temporal changes.

For duplicate-free bipartite linkage, generate at most one observation per entity per source within the tested scope. Duplicating a row on one side breaks that prerequisite; use it as an explicit out-of-contract test or change the representation, not as an expected extra one-to-one match. See the [behavioral-testing guide](../guides/er-behavioral-testing.md) for complete patterns and counterexamples.

## Sampling assumptions

Publish the generator's support, boundary-case strata, transformation frequencies, selection rules, and initial-state distribution. Realistic-looking strings do not establish representativeness. A property-search engine may choose cases adaptively to expose failures; its discovered counterexamples belong to discovery/regression evidence. To estimate a rate under $Q$, use a separate frozen sampling protocol, rather than infer one from search traces.

## Interpretation

Pass means the specific evaluated relation held for these admissible cases. It does not mean true identities were recovered outside their synthetic support. Controlled synthetic identity accuracy can be reported as such, but synthetic success cannot establish world accuracy. A failed relation may indicate an implementation defect, invalid fixture, mistaken contract, or legitimate stateful exception; retain those distinctions in triage.

## Potential biases

Fixtures copied from production mistakes can overrepresent known failures and miss new mechanisms. A generator can omit difficult scripts, same-name collisions, source reuse, or time transitions. Filtering out inconvenient generated cases changes $Q$. Shrinking a counterexample can destroy the property prerequisites: retain namespace, constraint, and state context needed to make the failure meaningful. Development repeatedly tuned to a suite can memorize its quirks.

## Known limitations

Symmetry, idempotency, and order invariance are conditional. A directional source-authority scorer need not be symmetric; a stateful adaptive resolver need not be order invariant. Test the promised artifact and exception, not bitwise equality of irrelevant trace ordering or transient entity names. Connected components of a fixed accepted graph must implement connectivity, including accepted bridges; the policy admitting a weak edge is a different test boundary. Universal weak-bridge rejection is not a valid closure property.

## Recommended comparisons

Run baseline and challenger on the same fixtures, transformations, state, and budgets. Compare threshold boundaries and abstention semantics for [SOL-08-001](../solutions/decision-resolution/thresholds-abstention.md), endpoint cardinality/unmatched options for [SOL-08-002](../solutions/decision-resolution/one-to-one-assignment.md), fixed-graph closure for [SOL-08-003](../solutions/decision-resolution/connected-components.md), and audited admissibility/conflict escalation for [SOL-08-004](../solutions/decision-resolution/constrained-clustering.md). These typed targets each supply a different contract, not interchangeable accuracy promises.

## Engineering substitution and replay contracts

The same behavioral estimand applies to [replaceable stages](../solutions/architecture/replaceable-stage-pipelines.md), [versioned artifact runs](../solutions/architecture/versioned-artifact-runs.md), [ordered policies](../solutions/decision-resolution/ordered-rule-policies.md), [decision tables](../solutions/decision-resolution/declarative-decision-tables.md) and [AR-06](../architectures/incremental-continuous.md): only explicitly eligible fixtures and promised observables define agreement. For a pure refactor, freeze snapshots, candidate/evidence artifacts, resolved policies and initial state. Compare decisions and promised membership/ID/lineage outputs, not merely row counts or identical schema shapes. Trace order may be irrelevant; stable external IDs may not be. Different allocations cannot be silently relabeled away when continuity is part of the contract.

For cache reuse, compare cache-free computation under identical declared inputs/context. For affected-state repair, choose a history/initial-state-equivalent reference, or a snapshot rebuild only where the contract promises snapshot-determined outputs; freeze accepted corrections, history boundary and ID state as applicable. Do not seed the reference with the derived artifact whose invalidation is under test. [AR-06](../architectures/incremental-continuous.md#affected-closure-versus-full-replay) distinguishes snapshot recomputation from historical replay.

Include a changed global statistic, deleted bridge, duplicate/late event, source override, publication retry and missing dependency where applicable. Add a small eligible universe with an independent exhaustive retrieval oracle: deleting a top-ranked candidate must reconsider a previously unstored eligible neighbor, or explicitly expose unsupported scope. For approximate retrieval, predeclare a bounded coverage property or incomplete result rather than demand exact ranking. This tests reconsideration, not whether that neighbor is a true match. Failures/crashes and unassessed paths remain separate guardrails. Identical outputs can preserve an existing bug; divergence can reflect an intended change or an invalid oracle. Use the [manifest](../guides/run-manifest-template.md) and [refactor witnesses](../guides/rule-policy-refactoring.md) to record those distinctions. This is a proposed project protocol: no such ER suite or replay has been executed here.

## Statistical uncertainty

A fixed regression suite has exact descriptive counts, not a population confidence interval by default. Independent confirmation draws from a fixed $Q$ can support a declared binomial interval for a binary fixture-level event. For related variants, use paired fixture-family resampling or an analysis respecting their dependence; preserve generator strata. Report stochastic-run variation separately. Zero observed violations is finite evidence, not a guarantee. Never expand sample size by counting identical reruns as new truth.

## Related solutions and references

Use [controlled comparison](../solutions/experimentation/controlled-comparison.md) and the [plan template](../guides/experiment-plan-template.md) to predeclare guardrails and confirmatory evidence. Complement with [real entity-quality evaluation](entity-resolution-quality.md) and [incomplete-reference limits](incomplete-reference-quality.md). Sources [19] and [22] support general testing concepts, not an ER library choice, correctness theorem, or empirical improvement. No behavioral suite or ER experiment has been executed by the Atlas.

## Sources

[19] https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf — Metamorphic Testing: A New Approach for Generating Next Test Cases
[22] https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html — Hypothesis: Introduction to property-based testing
