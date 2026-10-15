---
id: "SOL-02-002"
type: "solution"
title: "Versioned artifacts and realized experiment runs"
domain: "02"
summary: >-
  Record immutable source and intermediate artifacts, their producers, semantic
  dependencies, and realized run configurations so ER experiments can be replayed
  and valid controls reused. Separate artifact versioning, optional caching, and
  affected-state maintenance; use full recomputation as the simplest baseline.
  Population-specific calibration, guarded publication, and downstream correction
  remain explicit responsibilities. Requires lawful snapshot access and declared
  contracts; hashes, seeds, and compatible metadata do not establish semantic
  validity or identity accuracy.
tags: [experimentation, provenance, evaluation, governance, entity-agnostic, batch, incremental, calibration]
maturity: "context-dependent"
evidence: "theoretically-motivated"
relations:
  addresses: [DEC-02-001]
  complements: [SOL-12-001]
  used_by: [AR-06]
  evaluated_by: [EVAL-11-006, EVAL-11-003]
---

# Versioned artifacts and realized experiment runs

## Short summary

Make the executed configuration inspectable, not merely the intended recipe. Version inputs, intermediate outputs, fitting artifacts, and decision state; connect them through stage-specific dependencies. This supports [pipeline modularity](../../decisions/pipeline-modularity.md) without prescribing a tool, cloud, language, model, or resolver. It is conceptual Atlas synthesis, not an executed pipeline.

## Problem addressed

An experiment cannot distinguish a scorer improvement from fresher features if both read mutable inputs. Reusing an output because its filename or schema is unchanged can silently mix normalization, frequency, calibration, or membership versions. Conversely, recomputing everything for every contrast can make valid comparisons unnecessarily expensive. The question is which artifacts remain valid for which use, not simply whether a cache reports a hit.

## Core mechanism

1. **Freeze accessible inputs.** Identify source-scoped observation snapshots, reference/split versions, namespaces, and temporal availability. Preserve authorized raw evidence or protected references. Retain versions under a declared access/retention policy; immutability does not override deletion obligations. A mutable location is not a snapshot.
2. **Version stage products.** Store normalized observations, indexes/candidates, evidence, fitted statistics/models, scores, calibration, dispositions, memberships, and master views separately where their contracts differ. Record producer/configuration, input versions, schema and semantic contracts, population, feature definitions, and fitting context. W3C PROV distinguishes entities, generating/using activities, responsibility, and derivation/revision.[25] Here its entities describe data artifacts, not an ER identity ontology.
3. **Capture realization.** Link the frozen plan to the [run manifest](../../guides/run-manifest-template.md): actual resolved versions, executed parameters, outputs, reuse decisions, deviations, failures, and evaluation status. Keep planned and realized fields distinct; an absent result remains absent. Resolve mutable aliases once for the run and pin their immutable targets.
4. **Check reuse stage by stage.** Require matching declared dependencies, admissible semantics/population, integrity, and access. A changed dependency triggers recomputation or a documented unaffected-scope justification, never silent reuse. DVC's running-pipelines documentation illustrates skipping stages with unchanged declared commands, dependencies, and parameters and recovering cached outputs.[24] This is a bounded implementation example, not discovery of missing semantic dependencies.
5. **Evaluate then publish separately.** A complete run is not an approved deployment. Preserve the exact artifact bundle examined by the evaluator and any authorized promotion decision.

## Theoretical explanation

Under a complete dependency contract and the promised execution-equivalence conditions, unchanged inputs permit reuse of the same stage result. Versioning exposes violations of those assumptions; it does not prove dependency completeness. Distinguish byte-identical replay from equivalent decisions or equivalent aggregate measurements. Seeds alone do not control input order, parallel reduction, solver tie-breaking, hardware/runtime behavior, clocks, external services, or adaptive state. Pin or capture what is controllable and disclose residual nondeterminism; test only the equivalence actually promised.

## Important variants

- **Full recomputation:** rerun the complete configuration on fixed authorized snapshots, without cache reuse. This is the simplest credible baseline and a reuse comparator, not ground truth.
- **Versioned artifacts without caching:** retain lineage and reproducible controls while still recomputing stages. Useful when storage or dependency complexity makes automatic reuse unattractive.
- **Stage caching:** restore an entire valid stage product. It adds key construction, semantic checks, integrity verification, and storage costs; a hit is not new experimental evidence.
- **Affected incremental maintenance:** recompute a justified dependency closure inside evolving state. [AR-06](../../architectures/incremental-continuous.md) owns events, closure, and reconciliation. This solution supports that lifecycle but does not require it; versioning and caching are not synonymous with incremental ER.

## Assumptions and prerequisites

Require lawful snapshot access, stable observation/pair identifiers, resolved component versions, explicit [module contracts](../../taxonomy/module-contracts.md), and accountable artifact producers. Capture initial state and contextual iterations for stateful/collective stages. Unknown external dependencies limit replay and block unjustified reuse. Representative independent labels are needed for quality claims, not merely to record execution. Keep fitting, calibration, development, and final-reference access separated.

## Applicability conditions

Useful for repeated controlled comparisons, costly intermediate production, or auditable correction. Apply across the independent [architecture dimensions](../../taxonomy/architecture-dimensions.md); no scoring paradigm or clustering choice follows from artifact versioning.

For reuse, distinguish schema/version compatibility from semantic validity: readable fields can encode different units, missingness meanings, source authority, or conditioning populations. Record at least these invalidation paths:

| Changed dependency | Recompute or revalidate |
|---|---|
| Normalization used by keys/features | Dependent blocks/indexes, candidates and comparison features, then downstream products |
| Retrieval/routing/eligibility | Actual candidates and dependent evidence/scores; candidate-conditioned calibration and threshold applicability |
| Global frequency model or fitting corpus | Every dependent feature/score, potentially for unchanged records; downstream policy outputs |
| Score/model semantics | Scores and calibration applicability, edge admission, assignments/memberships |
| Accepted edges, constraints, or membership | Resolution competitors/closure as applicable; survivorship and published master views |

A retrieval change does **not** automatically invalidate every threshold. Reassess its declared population, score semantics, loss assumptions, and workload constraints; retain it only with an unaffected-domain justification or relevant validation. A threshold frozen as a diagnostic control is not thereby validated for changed deployment candidates.

## Advantages

Artifact lineage makes mixed-version errors diagnosable and negative runs retainable. Valid reuse can reduce repeated computation while preserving explicit controls. Separate publication bundles make the evaluated configuration identifiable and rollback targets inspectable. These are mechanism-based benefits, not measured ER gains.

## Trade-offs and failure modes

Incomplete cache keys can hide a changed global frequency denominator or remote enrichment response. Record both dependency fingerprints and validity reasoning. Cached stochastic output reproduces one realization, not its distribution; repeated seeds must not be replaced by the same cached sample. Hashes identify content under declared hashing/serialization rules, not anonymization, authenticity, or lawful access. Protected artifacts and manifests can still disclose sensitive identities, paths, or aggregates.

Separate **serving reuse** of a frozen fitted model from **retraining** after changed training data/features and from **recalibration** for changed score populations. None automatically entails the others. Reusing weights can be a declared experimental control yet require new population validation; retraining changes the comparator and must follow the experiment plan. Evaluation-only reference changes rerun affected evaluation, not automatically training or predictions.

For authorized promotion, require contract/integrity checks, independent quality and behavioral guardrails, compatible consumers, and a recorded owner decision. Publish a consistent bundle of applicable model, normalization/features, retrieval, calibration, policy and entity state atomically at the declared authoritative boundary; specify version visibility/pending status outside it and isolate partial/failed runs. MLflow documents aliases as mutable references to model versions.[26] An alias or approval tag is not a validation guarantee or an atomic whole-pipeline transaction. Preserve the prior bundle, membership/merge-split history and rollback procedure only where still authorized. Erasure or changed access can make restoration unavailable; do not restore withdrawn evidence. Restoring a pointer does not undo consumer actions: record downstream acknowledgments and compensating corrections, with unresolved consequences explicit.

## Relationships with other methods

[Controlled comparison](../experimentation/controlled-comparison.md) owns contrasts, fair tuning, splits, and inference; this solution supplies realized artifacts and reuse evidence. [Provenance-aware survivorship](../master-records/provenance-survivorship.md) consumes changed membership and source lineage, rather than treating a cache-valid master value as identity evidence.

## How to evaluate

Reuse a versioned evaluation harness across configurations: pin its metric/oracle definitions, fixtures/generator, state, references, exclusions, and access boundary. Under [behavioral evaluation](../../evaluation/synthetic-metamorphic.md), compare cache-free recomputation with allowed reuse and deliberately change each dependency, including global statistics, ordering, and failed-publication boundaries. Test stale-product rejection, consistent publication, and authorized rollback/compensation; report unexecuted cases and counterexamples.

For a changed retriever, use fixed-candidate diagnostics only to isolate downstream mechanisms; also evaluate the **actual changed candidate population** and end-to-end output, including independently supported omissions. Use [final-output quality](../../evaluation/entity-resolution-quality.md) plus linked candidate/pair evaluations for adoption evidence. Compare total build, fitting, validation, storage, and correction costs. Adopt reuse only if declared equivalence and project guardrails hold with worthwhile cost benefit; reject demonstrated stale-state or harmful outputs; call unsupported populations or unresolved nondeterminism inconclusive.

## Research opportunities

Test whether explicit global-statistic dependencies expose divergences missed by record-local invalidation. Compare valid stage caching with full recomputation under equal contracts and budgets before investigating affected-state optimization.

## References and evidence limitations

Sources [24]–[26] support bounded caching, provenance, and registry concepts, not this ER dependency table, privacy guarantees, semantic correctness, or a preferred stack. No ER experiment, measured speedup, successful promotion, or rollback is reported.

## Sources

[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
[25] https://www.w3.org/TR/prov-primer — PROV Model Primer
[26] https://mlflow.org/docs/3.3.1/ml/model-registry — MLflow Model Registry (3.3.1)
