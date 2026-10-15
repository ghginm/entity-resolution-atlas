# Conceptual module contracts

These contracts describe knowledge-level artifacts, not APIs, code classes, a mandatory technology stack, or an executable pipeline. The roles below are **not a compulsory thirteen-stage sequence**: roles may be fused, branches may omit inapplicable roles, and graph resolution and assignment are distinct resolution choices rather than consecutive obligations. Preserve responsibilities at every boundary a chosen composition actually exposes.

## Shared artifact envelope and prerequisites

Every exchanged artifact identifies its kind and semantic scope, its observation/pair/entity keys and versions, the producing component/configuration, and the exact upstream artifacts or reproducible snapshot on which it depends. Record relevant source namespace, eligible population, temporal scope, processing/decision time, and access restrictions. Distinguish observed values, derived representations, predicted decisions and adjudicated corrections. A run identifier alone does not establish which evidence produced a field or membership.

Outputs declare whether they are complete, partial, stale, rejected or failed, with reasons and unresolved inputs. Missing observation, invalid value, unavailable branch, skipped comparison, uncertain decision and execution error are different states; none silently becomes zero evidence, a non-match or an empty successful result. Retention/access policy may limit replay: record that limit without promising raw retention that is unauthorized.

**Hard prerequisites** are the semantics and artifacts the selected role needs: source namespaces for identifier comparison, score meaning for thresholding, justified cardinality for assignment, and membership plus a field policy for a master view. If absent, reject or defer the dependent operation. **Optional context** includes enrichment, relational neighborhoods, calibration when probabilities are not consumed, golden views, and review routing; absence must follow the role's declared fallback. Labels are needed for particular estimation/evaluation claims, not for every role's execution. A trained scorer's required features are not optional simply because another scorer could omit them.

See [architecture dimensions](architecture-dimensions.md): topology, scoring, resolution and lifecycle remain independently selected, subject to these compatibility checks. The [versioned-artifact run solution](../solutions/architecture/versioned-artifact-runs.md), [run-manifest template](../guides/run-manifest-template.md), and [decision-provenance guide](../guides/decision-provenance.md) develop packaging and traces; the role-specific meanings below remain the contract, not a checklist of manifest fields.

## Role-specific contracts

### Source ingestion and integration
- **Input → output:** source observations or source revisions/tombstones, schema mappings, namespaces and observation/validity times → accepted typed observations with raw references, source-scoped record/version keys and quality flags, or quarantined changes.
- **Invariant and lineage:** equally named fields need not denote the same attribute. Preserve conflicting assertions rather than overwrite them; bind each typed value to its raw source and mapping version. Distinguish a source revision from a second independent observation.
- **Failure and substitution:** malformed payloads, unknown schemas, duplicate deliveries and conflicting revisions have explicit dispositions. A replacement connector must preserve key, revision and deletion semantics and demonstrate coverage; silently dropping a field or changing a namespace invalidates downstream artifacts.

### Normalization and enrichment
- **Input → output:** typed observations and required locale/source context → raw plus normalized, parsed or variant representations, transformation lineage and uncertainty. External enrichment is a separately attributed inference, not an original observation.
- **Invariant and lineage:** lossy normalization cannot replace the only evidence copy. Version transformation rules, dictionaries and external reference responses; each variant links to its source field and temporal scope.
- **Failure and substitution:** unknown locale or failed parsing remains explicit, with raw fallback only if the comparator supports it. A replacement must preserve field meaning or declare a new representation contract; changed tokens may require new indexes, comparisons and calibration, not just a new normalizer label.

### Candidate retrieval
- **Input → output:** definition of the eligible pair universe, representations, source/time restrictions, retrieval passes/index snapshot and budgets → unique version-qualified pairs with source/pass/routing provenance, retrieval reasons, known exclusions/caps and coverage limitations. The universe need not be fully materialized; unobserved missed matches are not known omissions to enumerate.
- **Invariant and lineage:** canonical pair identity de-duplicates repeated retrieval without erasing pass provenance or directional source roles. An absent candidate is unknown, not a known non-match. Record index freshness and coverage restrictions, including truncation, block splitting and routing early exits.
- **Failure and substitution:** stale/failed indexes or exhausted budgets yield partial coverage, not certified absence. A substitute must cover the resolver's required eligible universe or expose the loss; changed candidate selection requires downstream population/calibration review even if the pair schema is unchanged.

### Pair comparison
- **Input → output:** a candidate and its versioned observations/representations → evidence vector with comparability, missing/invalid/conflict masks, source/time context and dependency groups.
- **Invariant and lineage:** distinguish absence from a reliable contradiction under declared trust and overlapping temporal scope. Shared source derivation cannot masquerade as independent corroboration. Version feature definitions and link each feature to the compared fields and transformations.
- **Failure and substitution:** unsupported scripts, unknown validity or unavailable fields remain qualified evidence states. A new comparator must preserve direction, scale and state meanings or trigger scorer re-estimation/revalidation; identical feature names do not establish compatibility.

### Scoring and optional calibration
- **Input → output:** compatible versioned evidence and an applicable manual/estimated/trained model → rank, additive sum, likelihood ratio or probability with declared semantics, contributions where available, model version and conditioning population.
- **Invariant and lineage:** a raw sum or likelihood ratio is not automatically a posterior. Optional calibration consumes scores and an independent representative reference, producing a versioned population-specific mapping and validity conditions. Track training/estimation and calibration dependencies separately from the scored observations.
- **Failure and substitution:** missing required features, unsupported populations and numerical failures are unresolved/failed scores, not non-matches. Replace a scorer only with an explicit scale/conditioning contract and revalidated consumers; changed retrieval, routing or source mix can invalidate calibration. No scoring family requires a particular partitioner or lifecycle.

### Evidence aggregation and fusion
- **Input → output:** comparison evidence or scorer-branch outputs for compatible pair/context snapshots → combined evidence/score, disagreement indicators and contributing or unavailable branches. Declare whether fusion precedes or follows scoring; it need not exist as a separate role.
- **Invariant and lineage:** preserve dependency/copy groups and branch conditioning; do not count repeated retrieval or shared features as independent support. Combining raw scores requires comparable semantics or a justified versioned learned mapping. Record branch, routing and fusion versions and input coverage.
- **Failure and substitution:** a missing branch is not negative evidence. Specify defer, partial fusion or a validated fallback, including applicable populations. Replacing a branch or fusion method requires consumer-scale checks and evaluation of full and missing-branch paths, not only complete cases.

### Decision policy
- **Input → output:** qualified evidence/scores, trusted rule predicates, project error costs and review capacity → link/non-link/abstain or admissibility dispositions with rationale, triggered rules, precedence and policy version.
- **Invariant and lineage:** pair acceptance is not globally consistent entity membership. Record which evidence and policy resolved rule conflicts; a trusted veto and a threshold use different assumptions. Do not turn unavailable scores or unmatched rule conditions into a negative by default.
- **Failure and substitution:** conflicting predicates or unknown prerequisites follow explicit abstention/escalation semantics. A replacement policy must preserve its claimed output meaning and reopen dependent memberships when decisions change; policy changes do not intrinsically require rescoring unchanged evidence.

An unknown/error mandatory admissibility guard must not disappear as an inapplicable rule while another rule authorizes effects. Defer/escalate unless a separately authorized risk contract specifies another treatment; optional diagnostic unknowns remain distinct. Preserve required outcomes across compound-predicate short-circuiting.

### Graph or joint membership resolution
- **Input → output:** accepted/scored edges, eligible observations, justified constraints and unresolved alternatives → partition, constrained memberships or uncertainty-preserving alternatives, plus a trace of supporting edges, conflicts and unassigned cases.
- **Invariant and lineage:** graph closure implements the declared membership rule; an unscored edge is not a cannot-link. Accepted bridges can connect entire components. Version resolver/objective/constraints and retain the graph and context snapshot, including isolated observations.
- **Failure and substitution:** inconsistent constraints or bounded search return conflicts/partial solutions, not silently dropped records. Substitution must preserve the target membership semantics or explicitly change them; pair-quality equivalence does not establish partition equivalence. Removing an edge may require whole-component repair.

### Assignment
- **Input → output:** a task-defined bipartite or other assignment problem, compatible utilities, capacities/cardinalities and unmatched costs/options → selected assignments, unmatched or unresolved observations, objective and constraint trace.
- **Invariant and lineage:** two sources do not establish one-to-one cardinality. Preserve competing alternatives and the declared unmatched option when permitted. Record the candidate/utility snapshot and solver, tie, capacity and unmatched-policy versions.
- **Failure and substitution:** missing utility is not a forbidden edge unless the task says so; infeasibility or resource exhaustion is explicit. A substitute must preserve eligibility, objective and capacities or declare a different problem. Changed evidence for one endpoint can invalidate assignments of unchanged competitors.

### Entity construction and attribute presentation
- **Input → output:** versioned membership and original observations, representation/continuity and field policies → virtual, golden or hybrid entity views with stable/versioned IDs, field lineage, alternatives and applicable intervals.
- **Invariant and lineage:** [master representation](../decisions/master-representation.md) owns representation and identifier lifecycle; [survivorship](../solutions/master-records/provenance-survivorship.md) owns value selection. Membership truth, identity continuity and attribute continuity are separate: a new address need not create a new entity, and a convenient survivor cannot prove membership. Trace selected and inferred fields to membership and policy versions.
- **Failure and substitution:** missing or incompatible values remain unknown/conflicting or reviewed; no invented default conceals a gap. Substitute representation/field policy only with explicit consumer semantics and rebuilt affected views. Feed derived entity context upstream only as versioned predicted context, not independent evidence.

### Persistence and publication
- **Input → output:** validated observations, decisions, memberships/views and proposed deltas → durable versioned artifacts, committed publication boundary, stable-ID/redirect history and recoverable lineage.
- **Invariant and lineage:** declare the authoritative state versus derived caches/views; publish mutually dependent membership, ID and view changes consistently. Retired IDs are not recycled. Raw observation keys and allocated entity IDs are different identities. Retention, access and deletion authorization constrain what can be stored.
- **Failure and substitution:** interrupted/conflicting writes remain uncommitted or visibly pending; do not expose half-applied merges or dangling references. A substitute store/publication mechanism must preserve historical resolution, version visibility and authorized retention, not merely current rows; downstream acknowledgments are distinct from local commit.

### Review and correction
- **Input → output:** uncertain or audited decisions with evidence/version traces and authorized reviewers → adjudicated labels or unresolved findings, scoped correction proposals and membership/attribute change history.
- **Invariant and lineage:** predictions do not become independent gold labels. Distinguish correction of a source assertion, pair judgment, membership and presented field; retain what was reviewed, reviewer authority, rationale and supersession links.
- **Failure and substitution:** reviewer disagreement, unavailable evidence or stale case versions remain explicit; reevaluate applicability before applying a correction to changed state. A substitute workflow must preserve authority, scope and trace, and cannot replace independent evaluation with its own model-generated confirmations.

### Monitoring
- **Input → output:** versioned retrieval/decision/publication/review outcomes, workload/exposure denominators and independently labeled samples where available → coverage/freshness/drift/quality diagnostics, alerts and proposed reopening actions.
- **Invariant and lineage:** latency, score drift, review yield and identity accuracy are different quantities. Bind metrics to eligible/evaluated populations, windows and configuration versions; partial feeds and unknown labels cannot count as successful negatives.
- **Failure and substitution:** absent telemetry/reference yields unavailable estimates, not zero incidents or proof of accuracy. A replacement monitor preserves metric meaning and comparable denominators or marks a break. Alerts do not themselves authorize retraining, merging, correcting or publishing entities.

## Mutation dependencies and incremental maintenance

The forward dependency chain is `source revision → typed observation → representations → retrieval indexes/candidates → comparisons → scores/fusion → policy → resolution/assignment → entity fields/IDs → published views and monitors`. This is an explanatory chain, not a fixed order: branches, calibration and iterative context add dependencies. Record reverse dependencies so a change can invalidate all consumers, including cases previously terminated by a cascade.

- **Observation/normalization changes:** remove obsolete index entries and reretrieve against both old and new relevant keys. Repair pairs lost as well as gained, competing assignments, bridging memberships and selected fields. Source deletion retracts evidence; it is not proof of entity death.
- **Global dependencies:** changed value frequencies, source priors, embeddings/reference dictionaries or index construction can affect unchanged records. Top-k insertion or deletion can displace/reveal a neighbor; updating only saved pairs misses this effect. Truncated blocks and approximate indexes require coverage diagnostics or wider replay, not a claim that the stored pair graph contains every dependency.
- **Configuration boundaries:** a scorer change invalidates scores and consumers, while policy-only changes may reuse valid scores. Resolver changes revise memberships under unchanged pair evidence; survivorship-only changes revise fields, not identity. If selected fields or predicted memberships feed upstream, explicitly track that feedback and iteration snapshot rather than assuming the chain is acyclic.
- **Repair output:** refreshed artifacts, unresolved scope, stable-ID redirects and reversible merge/split lineage under a consistent snapshot. Dependency closure may extend beyond a changed record; separate valid/observation time from ingestion/decision time using [temporal identity](../solutions/identity-semantics/temporal-identity.md). [AR-06](../architectures/incremental-continuous.md) owns lifecycle composition, including selective repair versus full replay.

## Composition and failure containment
- A cascade records terminal and escalated decisions plus routing versions; evaluate early exits separately, not just the remaining hard cases.
- A parallel composition keeps missing branch outputs distinct from negative branch evidence; fusion must use comparable scales or a justified learned map.
- An iterative composition records the context snapshot and iteration producing a feature; known labels and predicted memberships must not be confused.
- A budgeted retriever declares whether truncation/splitting sacrifices coverage. Index build and update costs belong in total compute accounting.
- Reversible entity changes require restoring membership/lineage and notifying downstream consumers; simply deleting a link does not necessarily reverse its transitive effects.

Safe substitution preserves artifact semantics, prerequisites and consumer obligations, not identical implementation or necessarily identical predictions. A fused implementation still explains both responsibilities; an absent role still explains how its consumer's needs are satisfied or why they are inapplicable.

## Evaluation and scope

Use [EVAL-11-006 behavioral contracts](../evaluation/synthetic-metamorphic.md) for declared namespace, unknown-state, lineage, unmatched-option, revision and replay properties, with explicit eligibility/oracle/error counts. Order invariance and deterministic IDs are tested only when promised; fixture success is not world accuracy. Use [candidate recall](../evaluation/candidate-recall.md) for coverage and [final-entity quality](../evaluation/entity-resolution-quality.md) for membership and downstream harm, separating field truth from entity truth. Compare a simple fixed-snapshot composition with the proposed substitution under matched inputs/budgets; violations reject its contract, adequate reference evidence can support adoption, and uncovered dependencies leave the result inconclusive.

See [taxonomy ownership](overview.md) and the [catalog](../CATALOG.md) for actual alternatives. These contracts are Atlas design synthesis, not externally benchmarked requirements or a detailed operational protocol. Wave 4 retains deeper temporal cases and operational/performance treatment; these boundaries do not claim exhaustive delivery, concurrency or recovery procedures.
