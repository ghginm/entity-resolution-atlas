# Wave 2 evidence: engineering mechanisms, not ER performance claims

## Retrieval and scope

Six additions were registered in the shared ledger before authoring: [23]–[28]. Raw responses and extraction text remain in a temporary agent cache, not this repository. Durable URL/version/response-hash and selected-scope records are in [retrieval provenance](retrieval-provenance.json); the allowed citation status is in [retrieval status](retrieval-status.json). Existing ledger entries and source limitations are preserved.

Configured search used a fallback provider because its nominal native transport could not execute client-side search. The configured extraction backend was search-only and rejected content extraction. Direct HTTPS retrieval succeeded for the six admitted sources. DMN PDF extraction used `pypdf` in the existing isolated QA environment after the host `pdftotext` executable proved absent. These are retrieval/tool limitations, not missing scientific results. No Hermes configuration was changed.

An exploratory Parnas paper copy reset the connection; a second academic mirror returned HTTP 402. It was not registered as an admitted citation, its full text was not verified, and no card attributes a detailed modularity claim to that paper. Modularity comparisons are explicitly engineering reasoning rather than a fabricated literature-backed ranking. Further specialist references may deepen later revisions without blocking the bounded design comparison.

## Admitted support and exclusions

| Ledger ID | Retrieved version and reviewed portion | What is supported | What is not supported |
|---|---|---|---|
| [23] | OMG *Decision Model and Notation*, version 1.5, document formal/24-01-01; PDF title page release January 2024; sections 8.2.11–8.2.12, printed pp. 71–73 (PDF pp. 79–81), plus surrounding table definitions | Distinct single-/multiple-hit semantics; compound Collect without operators; ranked output-clause precedence for compound Priority; annotation/unranked-output distinctions; optional default output | No claim that version 1.5 is latest, that an ER implementation conforms to DMN, that all tools implement every hit policy, or that a table raises identity accuracy. Atlas conflict-escalation, missing-value, tie-result and trace requirements are explicit design choices rather than automatic normative DMN behavior. |
| [24] | DVC official *Running Pipelines*, live HTML as fetched; DAG, Caching Stages and missing-data sections | Dependencies/outputs determine stage order; unchanged declared commands/dependencies/parameters can avoid recomputation; previous outputs may be recovered from a run cache | A tool cannot infer every hidden semantic dependency, guarantee deterministic output, or certify ER-quality-preserving cache reuse. No DVC installation or recommendation is implied. |
| [25] | W3C *PROV Model Primer*, Working Group Note, 30 April 2013; introductory and intuitive-overview sections 1–2 | Distinguishing data entities, activities, derivation, responsible agents and plans in provenance descriptions | No ER identity ontology, mandatory RDF implementation, privacy guarantee, complete lineage automatically captured, or AI-agent framework. ER boundary/tracing recommendations are synthesis. |
| [26] | MLflow documentation pinned to 3.3.1, *MLflow Model Registry*, Concepts and registry overview | Registered models/versions, mutable aliases, tags, lineage and metadata are distinct concepts | A mutable alias or `approved` tag is not an independent validation result, a frozen dependency, a transactional ER release bundle, or a universal reproducibility guarantee. Marketing claims about full reproducibility are not adopted as guarantees. |
| [27] | Martin Fowler, *RulesEngine*, author-maintained essay; production-rule model, chaining and design cautions | Distinguishing imperative conditional code from production rules; chaining can create implicit inter-rule control flow | The author's explicitly nonrepresentative experiences are not failure-rate estimates or a general proof against rule engines. A pure decision table is not automatically a reactive production-rule engine. |
| [28] | Martin Fowler, *Event Sourcing*, author-maintained design essay; application state, replay, external updates/queries and wrong-sequence discussion | Reconstructing state from events, combining current-state materialization with event history, replay and the problem of external side effects | Event sourcing does not establish ER identity truth, complete change capture, automatic reversibility, an obligation to store immutable PII, or safe repeat delivery to external consumers. Stable-ID/merge/split policies remain project-dependent synthesis. |

## Evidence boundary and ownership

Cards compare mechanisms and conditional costs, not measured framework superiority. Domain 02 owns composition and logical artifact dependencies; domain 08 owns policy composition/actions and membership semantics; domain 09 retains identity/master maintenance; domain 13 retains physical capacity and distributed execution; domain 14 retains governance/monitoring. The [module contracts](../taxonomy/module-contracts.md), [run manifest](../guides/run-manifest-template.md) and [decision provenance](../guides/decision-provenance.md) support those owners instead of creating a parallel object system.

Behavioral equivalence can support a refactor claim, dependency replay can expose stale reuse, and controlled investigation tasks can evaluate debugging effort. None establishes real-world ER quality. Intended changes to candidates, actions or memberships require the applicable existing quality evaluations and independent reference evidence; absent labels constrain the claim. No engineering benchmark, production replay, ER experiment, or new agent-utility cohort has been executed in Wave 2.

## Sources

[23] https://www.omg.org/spec/DMN/1.5/PDF — Decision Model and Notation, version 1.5
[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
[25] https://www.w3.org/TR/prov-primer — PROV Model Primer
[26] https://mlflow.org/docs/3.3.1/ml/model-registry — MLflow Model Registry (3.3.1)
[27] https://martinfowler.com/bliki/RulesEngine.html — RulesEngine
[28] https://martinfowler.com/eaaDev/EventSourcing.html — Event Sourcing
