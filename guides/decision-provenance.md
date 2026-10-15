# Decision provenance: an explanation is not a correctness certificate

## Scope and minimum retrieval

Use this guide when an agent must explain an accepted link, a deferral, an entity change, or a regression. Start from the affected [module contract](../taxonomy/module-contracts.md), then retrieve the applicable [policy](../decisions/rule-composition.md), [resolution](../decisions/resolution-strategy.md), or [master](../decisions/master-representation.md) owner. Do not load every stage to investigate a local formatting defect.

The W3C PROV primer distinguishes the things produced, the activities using/producing them, and responsible agents.[25] Here, a provenance *entity* can be an input snapshot or decision artifact; it is not a claim of real-world same-as identity. A PROV *agent* need not be an AI agent. This guide uses that distinction as vocabulary, not a requirement to implement RDF, a provenance service, or agent orchestration. The ER trace design below is Atlas synthesis.

## Minimal evidence chain

A small pipeline can retain a versioned input snapshot, resolved configuration, stage outputs, and decision references. More instrumentation is justified when it answers an actual audit/replay question. Link records by stable artifact and observation references rather than copying all raw PII into each trace.

| Boundary | Minimum explanation retained | What it cannot establish |
|---|---|---|
| Ingestion and representation | Source-scoped record/version, valid/observation/ingestion time where applicable; representation/normalizer version; invalid or unavailable fields | That an observation is authoritative or a lossy representation preserves identity evidence |
| Candidate retrieval | Pass/index/version, eligibility and budget/truncation status, deduplicated union membership; stored or reproducible generation path | That a never-returned pair is a nonmatch; completeness without independent reference evidence |
| Comparison | Representations and comparison versions, agreement/disagreement/missing/invalid states, scope of a trusted contradiction | That similarity is identity or a measured conflict is a hard prohibition |
| Scoring and evidence aggregation | Feature schema, producing model and training reference, raw score semantics, calibration population/version if applicable; dependence/copy handling and aggregation rule | That an additive total is a probability or a pair probability is cluster confidence |
| Decision policy | Resolved policy/source override, applicable guards, evaluated predicates and results, selected rule/action, default/review/expiry path, boundaries and tie policy | That a fired rule is scientifically correct or an unevaluated rule was false |
| Resolution or assignment | Input edges/proposals, competitors/constraints, accepted and excluded actions with reasons, objective/tie semantics, affected membership version | That surrogate optimality, feasibility, or graph consistency certifies identity |
| Entity construction | Membership reference, identifier allocation/redirect/split decision, separate attribute candidates/authority/temporal selection, unresolved conflicts | That ID retention or plausible master attributes prove membership or identity continuity |
| Human intervention and publication | Protected review reference, authorization, precondition state, change/reason, committed output version, correction lineage and downstream acknowledgement | That human review is infallible, publication is globally atomic, or rollback undoes external consequences |

For a short-circuit policy, label each predicate **true / false / unknown / not evaluated / failed** as appropriate to its declared semantics. Do not invent a complete rule-match explanation from only the winning branch. A diagnostic all-rules evaluation must use a frozen, side-effect-free context; otherwise it can change the decision it is meant to explain. Recording overlap is different from allowing several conflicting actions.

A useful illustrative counterexample is a high-scoring pair stopped by a source-scoped incompatibility guard. The trace should identify the guard's evidence and scope, not just say “low confidence.” If the guard's authority is later revoked, that dependency should locate decisions to reopen. The trace does not decide whether the original guard was justified; adjudication and the identity contract do.

## Replay and counterfactual boundaries

An explanatory chain identifies **why this implementation acted on these inputs**. Replay additionally requires retained accessible inputs, dependency-complete artifacts, compatible code/environment, declared nondeterminism and controlled external effects; a log of rule names alone is insufficient. Use the [run-manifest template](run-manifest-template.md) and [versioned artifact solution](../solutions/architecture/versioned-artifact-runs.md). A hash detects a content change only when the underlying content remains available; it is neither a reconstruction method nor anonymization.

Separate three questions:

1. **Historical reconstruction:** can the recorded versions reproduce the promised output, including stable-ID behavior where part of the contract?
2. **Counterfactual recomputation:** what would a different policy or corrected observation produce on the declared frozen state? This is a new run, not a rewrite of history.
3. **Identity correctness:** are resulting links/memberships true under the project semantics? Use independent [entity evaluation](../evaluation/entity-resolution-quality.md), or report [incomplete-reference limits](../evaluation/incomplete-reference-quality.md).

A trace can correctly explain an incorrect merge. Conversely, absent trace evidence means an explanation is unavailable, not that the decision was necessarily wrong. Preserve both conclusions instead of substituting a plausible narrative.

## Access, retention and evaluation

Record who may resolve protected references, retention limits and what reconstruction becomes unavailable after deletion. Minimize raw identifiers, names and reviewer notes in widely shared logs. Retained intermediate artifacts, embeddings, hashes and trace exports still need a project threat/access assessment. Generic provenance is not a privacy or legal-compliance guarantee.

For a declared set of decisions, report counts requiring traces, complete chains, missing/inaccessible evidence, incompatible versions, failed replays and unresolved cases. Define completeness by required boundaries for that decision type; an optional absent stage is not a failure. Do not quietly remove untraceable decisions from the denominator. Compare simple snapshot-plus-reference logging against richer tracing on the same fixed decisions and investigation tasks, including storage/access cost and diagnostic effort. These are engineering diagnostics, not population accuracy estimates.

Use [behavioral evaluation](../evaluation/synthetic-metamorphic.md) for declared trace/replay contracts and [controlled comparisons](../solutions/experimentation/controlled-comparison.md) for attribution. Adopt richer tracing only if it resolves necessary investigations within project cost/privacy limits; reject it if it leaks restricted evidence or cannot reconstruct claimed dependencies. If original inputs are unavailable, record that blocker rather than claiming a successful replay. No trace harness or ER experiment has been executed by this guide.

## Sources

[25] https://www.w3.org/TR/prov-primer — PROV Model Primer
