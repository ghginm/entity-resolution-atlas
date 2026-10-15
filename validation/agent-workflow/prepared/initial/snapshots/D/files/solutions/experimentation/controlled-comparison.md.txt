---
id: "SOL-12-001"
type: "solution"
title: "Controlled comparison with frozen baselines and independent evaluation"
domain: "12"
summary: >-
  Operationalize an entity-resolution comparison by freezing a credible baseline,
  naming the changed mechanism, controlling shared inputs, and reserving an
  independent final evaluation. The protocol covers semantic dependencies,
  admissible stage substitution, entity/time/source leakage, paired uncertainty,
  stochastic repetitions, and practical adoption rules. It separates diagnostic
  ablations from end-to-end claims and records negative or inconclusive results.
  It requires valid reference support and project-defined guardrails; reproducible
  execution alone does not establish population accuracy or useful improvement.
tags: [experimentation, evaluation, uncertainty, provenance, entity-agnostic]
maturity: "context-dependent"
evidence: "theoretically-motivated"
relations:
  addresses: [DEC-12-001]
  evaluated_by: [EVAL-11-001, EVAL-11-002, EVAL-11-003, EVAL-11-006]
---

# Controlled comparison with frozen baselines and independent evaluation

## Short summary

Treat a comparison as a declared contrast between complete, versioned configurations on a specified evidence population. Freeze the baseline before final outcomes, isolate the proposed mechanism where feasible, then check the integrated output. The protocol is an Atlas design synthesis, not an executed experiment or a mandatory software stack.

## Problem addressed

A result is uninterpretable when the challenger also receives cleaner labels, a larger search budget, a different candidate population, or favorable post-test threshold selection. Even unchanged downstream code may cease to be valid when its input semantics change. Controls must therefore cover both artifacts and the assumptions governing their reuse.

## Core mechanism

1. **Declare the contrast.** Name the [design choice](../../decisions/experiment-design.md), baseline, challenger, hypothesis, target output, estimand, cost units, and competing explanation. Specify which modules change and which remain controls. Separate diagnostic and prospective claims.
2. **Freeze inputs and opportunities.** Fix eligible records, source/reference snapshots, namespaces/time semantics, shared candidate or evidence artifacts as appropriate, and tuning allowances. Record versions, partition assignments, seeds, policy, and reference support in a compact run manifest. A manifest documents a comparison; detailed tracking/cache/promotion infrastructure belongs to later MLOps work.
3. **Separate development from final evidence.** Fit models on training partitions; discover properties, inspect errors, choose thresholds, and tune calibration only on declared development partitions. Reserve an independently adjudicated final holdout. Fix evaluation entities and their context before running; no final-holdout property discovery or adaptive tuning.
4. **Check semantic dependencies.** Changing normalization can change keys and features; changing retrieval/routing can invalidate candidate-conditioned calibration; changing edge policy can change graph memberships and master attributes. Reuse a cached artifact only when its input versions and semantic assumptions still match the contrast. A frozen upstream artifact is a deliberate control, not an excuse to use stale downstream evidence. Follow [module contracts](../../taxonomy/module-contracts.md); do not prescribe an implementation cache here.
5. **Execute paired comparisons and report all dispositions.** Evaluate configurations on shared supported units, retain abstentions/errors, and account for fitting, indexing, inference, review, and update costs. Record unexpected failure without replacing it with invented results. Include integrated evaluation before claiming deployable value.

## Theoretical explanation

Holding input and evaluation units fixed removes those differences as explanations within the comparison; it does not remove biased labels or deployment shift. A paired contrast preserves shared-unit variation instead of pretending that two scores are independent. Stage replacement measures value conditional on the controlled inputs; end-to-end evaluation measures value of the feasible whole configuration. Neither implies the other.

For crossed changes, full factorial structure permits main-effect and interaction comparisons.[20] Interpret the [defined contrast](../../decisions/experiment-design.md#criteria-for-choosing) only on its named response scale and design, not as deployment causality.

## Important variants

Use fixed-pool scorer replacement, pass/evidence-group ablation, small factorial cells, and full-system challengers for their respective questions. For each ablation, declare **frozen-parameter removal** versus **refitting without the input**: they measure reliance and achievable value under retuning, respectively. Oracle stage replacements are reference-supported diagnostics, not production alternatives. Repeated stochastic runs are repetitions within a configuration, not additional independent labels.

## Assumptions and prerequisites

Require settled identity/cardinality semantics, lawful access, a reproducible baseline, enough label support for the estimand, and output-compatible evaluation. Unknown labels stay unknown; use [incomplete-reference evaluation](../../evaluation/incomplete-reference-quality.md) to constrain what can be estimated. [Ground-truth acquisition](../../decisions/ground-truth-acquisition.md) chooses review units/design; this solution does not manufacture labels.

## Applicability conditions

Use entity-disjoint partitions when testing transfer to new identities; split all known aliases/observations together. Audit possible identity overlap when labels are incomplete rather than asserting perfect disjointness. Use forward-time splits with features available as of the decision time for prospective ingestion. For existing-entity continuation, allow only the historical state explicitly promised by deployment. Hold out sources when source transfer is the question; entity separation may also be needed across those sources.

Copied records, graph neighbors, aggregates, weak-label rules, and calibration populations can leak across splits. Fit data-dependent transformations on permitted partitions; restrict context by its availability contract. A [targeted active-review sample](../ground-truth/targeted-active-review.md) or [weak supervision](../ground-truth/weak-supervision.md) can support training/discovery but is not independent final truth. Splits do not repair nonrepresentative review selection.

## Advantages

The frozen contrast makes changes and failures traceable, supports reuse of valid controls, and prevents successful isolated results from bypassing integrated guardrails. Negative results retain value because the tested question and precision are explicit.

## Trade-offs and failure modes

Overcontrol can conceal retrieval loss; undercontrol prevents attribution. Retuning only the challenger confounds method with opportunity. Best-seed reporting hides instability. Inspecting holdout failures and rerunning after fixes converts that holdout into development evidence; any new confirmatory claim needs fresh evidence or an explicitly valid sequential design. Repeated comparisons require a predeclared selection/multiplicity plan, not optional stopping when a favorable interval appears.

## Relationships with other methods

The [behavioral-testing guide](../../guides/er-behavioral-testing.md) supplies conditional property/counterexample checks alongside quality metrics. [Probability-sampled review](../ground-truth/probability-sampled-review.md) supplies independent evidence under its inclusion/nonresponse assumptions. Neither reproducibility nor synthetic consistency substitutes for that evidence.

## How to evaluate

Use [candidate](../../evaluation/candidate-recall.md), [pairwise](../../evaluation/pairwise-calibration.md), [final-output](../../evaluation/entity-resolution-quality.md) and [behavioral](../../evaluation/synthetic-metamorphic.md) owners as appropriate. First name the uncertainty: finite-population sampling, future-population/model, reviewer error or algorithm randomness. Pair finite-population contrasts using the actual inclusion/stratum/stage design; shared records do not invalidate genuine random-pair variance. For transfer inference, justify entity/graph or multiway dependence treatment, including both endpoints of cross-entity pairs. Report acquisition/training/generator seeds separately. Prespecified development-split repetitions can assess split sensitivity but overlapping labels/entities are not independent truth; keep frozen final contrasts distinct from fresh transfer replication and disclose all runs.

Predeclare a minimum worthwhile improvement, statistical interval/test convention, precision target, and harm/cost guardrails from project consequences. Statistical detectability is not practical benefit. Adopt only when the declared practical and guardrail requirements are supported; reject when evidence rules out sufficient value or establishes unacceptable harm; call wide or label-unsupported contrasts inconclusive. Lack of statistical significance is not equivalence. Use the [reusable plan](../../guides/experiment-plan-template.md) to record the resulting next decision.

## Research opportunities

After positive evidence, replicate on the intended new source/time population. After negative evidence, distinguish redundancy from bad estimation, retrieval loss, or a false mechanism. After inconclusive evidence, improve relevant label coverage or precision rather than optimize against the final holdout.

## References and evidence limitations

NIST supports factorial combinations and interaction analysis, not this ER-specific protocol or a winning configuration.[20] Remaining procedures are Atlas synthesis constrained by existing evaluation/module contracts. No comparison, performance gain, or behavioral test result is reported here.

## Sources

[20] https://www.itl.nist.gov/div898/handbook/pri/section3/pri3331.htm — NIST/SEMATECH e-Handbook: Two-level full factorial designs
