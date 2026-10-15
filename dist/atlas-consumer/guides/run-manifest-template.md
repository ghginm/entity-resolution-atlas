# Conceptual run-manifest template

This supporting guide accompanies [SOL-02-002](../solutions/architecture/versioned-artifact-runs.md) and the [experiment plan](experiment-plan-template.md). It is not a sixth primary card template, an executable configuration, a tool recommendation, or authorization to access data or publish decisions. Copy relevant fields into an authorized project record. Populate only known facts; leave explicit unresolved requirements instead of inventing versions, thresholds, results, or permissions.

A **planned manifest** specifies intended controls and outputs. A **realized manifest** records the exact inputs, configuration, reuse, execution, and evaluation that actually occurred, including deviations. Keep both and link revisions; do not rewrite the plan after seeing outcomes. Treat each finalized record as immutable within authorized retention, with corrections in a linked successor; authorized erasure can require withdrawal/redaction rather than preserving restricted contents. No run is reported by this template.

## 1. Identity, status, and unresolved fields

| Reusable field | What to record |
|---|---|
| Run / comparison / attempt identifiers | Distinguish configuration, stochastic repetition, retry, and parent experiment; retries do not erase failures |
| Plan and manifest revisions | Frozen plan reference, manifest format version, predecessor/correction links, and planned versus realized role |
| Responsible owner / authorization | Who may execute, evaluate, promote, or correct; allowed scope and forbidden actions |
| Status and phase | `planned`, `notexecuted`, `failed`, or `evaluated`; use `executed-unevaluated` for completed execution awaiting evaluation. Record execution and evaluation status separately where needed |
| Actual activity times | Start/end and availability cutoffs with timezone, or explicitly unknown; never populate actual times from the schedule |
| Failure / deviation record | Failed stage, partial outputs, unavailable inputs, changed controls, exclusions, and whether claims remain admissible |
| Unknown-field register | Field, `unknown` / `not applicable` / `withheld` / `unavailable`, reason, owner, retrieval route, and blocking consequence |

`evaluated` means an assessment exists, not that it passed or was promoted. `notexecuted` is an explicit non-result. Record incomplete execution and missing evaluation separately; absent output is not an empty successful artifact. A required unknown dependency prevents a justified reuse claim; missing label support limits the estimand rather than becoming a negative label.

## 2. Source snapshots and artifact inventory

For every input/intermediate/output, record:

- **Immutable artifact identity:** protected locator, snapshot/version, producer run/stage, content digest and algorithm where appropriate, serialization/order convention, integrity-check status, and retention/deletion policy. Do not use a mutable filename or alias as the only identity.
- **Source and time semantics:** namespace, schema/mapping revision, observation/validity/event/ingestion times as applicable, snapshot boundary, historical state, and permitted as-of availability.
- **Access:** authorized role, access-policy reference, retrieval prerequisite, and whether another evaluator can lawfully obtain the same snapshot. Store no passwords, tokens, secret keys, signed access URLs, or raw personal values in a shared manifest.
- **Dataset and feature lineage:** selection/filter/deduplication rules, partition membership artifact, feature definitions and missingness semantics, fitted transformation/statistic versions, fitting population and permitted context. Preserve raw-to-derived relationships without exposing restricted contents.
- **Population and coverage:** eligible records/pairs, source roles, actual candidates, caps/omissions, excluded/unknown units, and justified counts only when measured.

Hashes can check content identity under declared conventions; they do not anonymize records, establish authenticity, or restore deleted data. Restrict sensitive digests/locators and lineage like other protected metadata. Separate artifact identity from permission to retain it. W3C PROV supplies usage, generation, derivation, and responsibility concepts for provenance.[25] This template uses them for artifacts and activities, not to define who is the same ER entity.

## 3. Component contracts and execution realization

Record topology, scoring paradigm, resolution strategy, and lifecycle independently using the [architecture dimensions](../taxonomy/architecture-dimensions.md). For each actual component, specify immutable implementation/configuration identity, input/output schema versions, semantic contract, score units/meaning, constraints, and compatibility conditions. A readable schema or compatible version label does not prove unchanged source meaning or calibration validity.

Capture resolved parameters, not only defaults or configuration expressions. Record every mutable alias used, its immutable target at resolution time, and the resolution event; pin that target for the attempt. MLflow's registry documentation illustrates mutable aliases to model versions.[26] Neither such an alias nor a status tag certifies validation or whole-bundle publication.

Record acquisition, split, fitting, generator, and inference random states separately where applicable; algorithm/runtime/library/hardware environment; determinism controls; canonical input order, scheduling and tie-breaking rules; initial state/iteration; and captured external response versions. Declare byte equality, decision equivalence, or bounded stochastic variation as the promised replay criterion. Seeds alone cannot freeze external services, clocks, adaptive state, or all parallel/hardware behavior. Unknown nondeterminism is a limitation, not a fabricated guarantee.

## 4. Stage-level producer and dependency table

Instantiate a row for every realized stage/branch/iteration, including non-model stages. These are conceptual responsibilities; a project may combine stages physically.

| Stage / producer identity | Inputs and dependencies to pin | Output artifact and validity scope |
|---|---|---|
| Integration / normalization | Source snapshots, mappings, namespaces, locale/enrichment responses, transformations | Typed/normalized observations with raw lineage |
| Retrieval / indexing | Normalized fields, eligibility, pass/routing rules, index build, budgets/order | Actual unique candidates, retrieval provenance, caps/omissions |
| Feature/statistic production | Candidate pairs, observations/context, feature definitions, global frequency corpus/model and as-of boundary | Evidence/masks with population and fitting scope |
| Model fitting, if used | Training partitions/labels, feature artifacts, estimation settings, random state | Frozen fitted model; no final-holdout fitting |
| Serving / scoring | Evidence, frozen model/manual score configuration, source/routing context | Scores with semantics and conditioning population |
| Calibration / policy | Calibration, if used: scores, independent permitted calibration reference and mapping configuration. Policy: its actual qualified evidence/scores/predicates, losses, thresholds/review constraints | Calibration mapping if applicable; dispositions and declared applicability. A non-probability rule need not add calibration or labels |
| Resolution / survivorship | Dispositions, competitors, constraints, initial memberships, original observations, source authority | Assignments/memberships, master attributes, lineage |
| Evaluation | Predictions, actual candidate artifact, independent references, evaluation frame, harness/oracle revision | Measurements, denominators, uncertainty, failures/unknowns |
| Publication / correction, if authorized | Approved coherent bundle, previous state, consumer contracts | Published revision, acknowledgment and compensation record |

Add columns for **planned dependencies versus actual resolved inputs; executed versus reused; cache/source run identity; integrity check; reuse justification; stale reasons; execution status; and actual outputs**. A reused output retains its original producer; the new attempt records its consumption, not fictitious regeneration.

DVC documents stage skipping/recovery based on unchanged declared commands, dependencies, and parameters.[24] That illustrates bounded cache operation, not automatic discovery of ER's semantic dependencies. Specify global statistics, external responses, and population contracts explicitly or refuse unsupported reuse.

## 5. Reuse and invalidation example

**Illustrative only, not a run result:** change a normalization rule used by both a blocking key and a comparison feature. Invalidate those normalized products, blocks/indexes, actual candidates and features, then dependent scores, decisions, memberships, and survivorship. Preserve unaffected raw snapshots; document any unaffected branch rather than blanket-invalidating unrelated products.

Use the [canonical invalidation table](../solutions/architecture/versioned-artifact-runs.md#applicability-conditions) for other changes rather than duplicate its dependency analysis here. Fill actual producer/reuse rows with the applicable global-statistic, candidate-population and consumer dependencies. In the normalization example, an unaffected branch needs its explicit justification; unchanged filenames and readable schemas are insufficient.

Distinguish reuse of frozen serving weights, retraining, and recalibration. Choose each from its actual dependencies and the [controlled contrast](../solutions/experimentation/controlled-comparison.md), not automatically whenever any dataset revision changes. Full cache-free recomputation is the simplest baseline. Versioned artifacts are useful without caching; [affected incremental repair](../architectures/incremental-continuous.md) adds closure/state obligations and is not required here.

## 6. Prediction and evaluation frames

Record prediction artifact identity, eligible universe, actual candidates/routing, score semantics, disposition/resolution outputs, unresolved cases, and initial/final state. Separately record the evaluation frame: independent reference/split identity, inclusion design/weights, unit/denominator, missing-label treatment, slices, estimand, metric/oracle/harness versions, fixture/generator support, random states, and analysis conventions. Reference access must not leak truth into prediction inputs.

Reuse the same admissible harness across contrasts; rerun affected evaluation when predictions, reference, metric, or frame changes. An old report is not evaluation of a new bundle. Fixed-candidate diagnostics isolate downstream mechanisms but cannot establish changed-retriever value: evaluate actual changed candidates and end-to-end output, including independently supported misses. Follow [behavioral evaluation](../evaluation/synthetic-metamorphic.md) and the plan's independent real-quality route. Record all attempts, undefined denominators, failures, unknowns, costs, and adopt/reject/inconclusive reasoning; no measurements are supplied here.

## 7. Guarded publication and handoff

If publication is authorized, record the evaluated bundle, contract/quality/behavior gates, consumer compatibility, decision owner, and explicit approval or rejection. Publish a consistent revision atomically at the promised boundary; retain a prior complete bundle and failure isolation. Record rollback target, membership/merge-split lineage, correction authorization, consumer acknowledgments, and compensating actions. A pointer rollback cannot undo decisions already taken downstream; unresolved compensation remains visible. Otherwise mark publication not applicable or notexecuted, never imply deployment from `evaluated` status.

Retain prior bundles and finalized records only within current authorization/retention scope. Authorized erasure can withdraw/redact artifacts and make rollback/replay unavailable; record the limitation without restoring erased contents. An earlier approval or unchanged digest does not authorize restoration after access is withdrawn. A source tombstone and an erasure request are distinct inputs under the project contract.

Before handoff, check that realized inputs resolve, reused artifacts have justified dependencies, claims match evaluation support, secrets are absent, and remaining unknowns have consequences. Reproducibility, semantic conformance, statistical quality, and promotion are distinct claims. Sources support bounded provenance/cache/alias concepts only; the ER-specific template and invalidation example are Atlas design synthesis.

## Sources

[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
[25] https://www.w3.org/TR/prov-primer — PROV Model Primer
[26] https://mlflow.org/docs/3.3.1/ml/model-registry — MLflow Model Registry (3.3.1)
