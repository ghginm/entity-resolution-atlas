# Decision coverage matrix — v1.2 integration, with earlier history

## How to read this matrix

Rows are ER design questions, not domains. A status is a **content-review judgment under the definition in the [quality rubric](content-review-rubric.md)**, made after structural validation, not a lint or benchmark result.

- **Covered:** decision-level mechanism with explicit assumptions, at least one meaningful alternative, failure diagnostics, an evaluation route and usable cross-links for the bounded question.
- **Partial:** relevant objects exist but a major element (alternative depth, mechanism or evaluation) remains at map/architecture level.
- **Missing:** no usable knowledge object for the question.
- **Deferred:** valuable but explicitly outside the bounded implementation or blocked by named specialist/project/independent-evidence prerequisites; historical v1.1 and current v1.2 reasons remain in their owning rows, [tracker](v1.2-expansion-tracker.md) and [opportunities index](../research/opportunities-index.md).

“Covered” never means complete domain coverage, empirical validation, or demonstrated usefulness; only the [agent-utility benchmark](../validation/agent-utility/) measures actual decision behavior, and its status is reported separately in the [quality review](quality-review.md).

## Wave 5 agent integration and evidence boundary

Current manifest `1.2` retains 57 cards. [Final review](v1.2-final-review.md) records inherited earlier-wave review, fresh changed-family/seam review and author closure of Wave 4's four major/two minor critique findings; no independent post-remediation certification is claimed.

| Question | Earlier scope | Integration judgment | Owner / evidence limit |
|---|---|---|---|
| How does a natural-language project question reach a small relevant slice? | Generated domain/tag routes | **Covered operationally** | [Task patterns](agent-task-patterns.md) and conditional L0 entry; structural/conceptual routing, not observed solver quality |
| How are project facts connected to choices and a reversible experiment? | Intake/comparison guides | **Covered** | [Integration note](project-atlas-integration.md); external facts and permission cannot be supplied by the Atlas |
| What should agents return and when must they stop? | AGENTS discipline | **Covered** | Known/Assumed/Proposed/Testable/Proven, baseline/alternative/contracts/evidence and stop rules |
| How is shallow duplication or weak navigation detected? | Existing graph/evaluation/source/freshness gates | **Covered structurally; semantic review required** | Duplicate tags reject, identical summaries warn; unsupported strength/excessive tags/contradictions remain content questions |
| Did v1.2 improve actual agent decisions? | Historical AU-v1 only | **Unestablished** | AU-v2 data frozen/integrity-verified; offline bindings, 31/57/empty exports and mechanical packet/score tools implemented; trusted process execution, eligible identities and independent evaluator invocation absent; zero runs/scores; infrastructure passes cannot answer this |

The [original-task delivery](v1.2-final-delivery.md) maps all 26 content subsections
and ten deliverables to these existing owners, with explicit specialist and empirical
limits. It does not add a taxonomy or upgrade a bounded coverage judgment into
measured utility. [Delivery review](../validation/v1.2/final-delivery-content-review.md)
and [checks](../validation/v1.2/final-delivery-validation.json) record the final handover.

## Wave 4 operational coverage — separate critique and author remediation

The Wave 4 checkpoint had 57 cards. [Review](v1.2-wave-4-content-review.md) records returned separate critique and six author corrections; [initial checks](../validation/v1.2/wave-4-validation.json) retain pre-critique outputs. Final checks are separate, not a reinterpretation of those original runs. No measured ER/agent improvement is asserted.

| Decision question | Earlier scope | Wave 4 judgment | Canonical route | Residual limit |
|---|---|---|---|---|
| Where should skewed comparison work run without losing pairs? | Taxonomy only | **Covered for bounded execution** | [DEC-13-001](../decisions/execution-strategy.md), [SOL-13-001](../solutions/scalability/skew-aware-execution.md) | Engine-specific implementation and global resolver capacity need project trials |
| What costs count for equivalent build/reuse/update/recovery? | Partial artifact/AR contracts | **Covered for protocol** | [EVAL-11-007](../evaluation/execution-cost-replay.md) | No actual workload/speedup; future workload transfer is uncertain |
| How do concurrent/late/deleted updates reach consistent consumers? | Bounded AR-06 | **Covered for operational witnesses** | [AR-06](../architectures/incremental-continuous.md), [repair guide](incremental-operations.md) | Complete delivery/consensus/compensation protocols remain specialist scope |
| What do drift and graph alarms justify? | Domain map only | **Covered for diagnostic/audit distinction** | [DEC-14-001](../decisions/monitoring-response.md), [SOL-14-001](../solutions/governance/stage-monitoring.md) | Alarm/quality thresholds and independent reference evidence are project-specific |
| Which evidence and external routes are permissible? | Privacy caveats | **Covered for intake/alternatives** | [Governance](er-governance.md), provenance/run guides | Authority and obligations are external facts; no legal/compliance certification |
| Which private/federated/unlearning guarantees hold? | Deferred | **Deferred with substantive reason** | Governance and domain 14 | Primary specialist threat-model/leakage evidence and consumer need required |

## Historical Wave 3 documentation checkpoint — author-only content review

Manifest `1.2-wave-3` enumerates **52 cards**: 11 Decision, 27 Solution, 6 Architecture, 2 Hypothesis and 6 Evaluation. [Content review](v1.2-wave-3-content-review.md) records two sequential author passes and concrete corrections, not independent approval: all four delegated authoring attempts failed with HTTP 402. Actual structural/citation/integrity checks are in [validation](../validation/v1.2/wave-3-validation.json). The bounded judgments below do not establish measured ER/agent improvement.

| Decision question | Earlier scope | Wave 3 judgment | Canonical route | Residual limitation |
|---|---|---|---|---|
| Which name transformations preserve useful distinctions? | Domain map only | **Covered for representation choice** | [DEC-04-001](../decisions/name-representation.md); [SOL-04-001](../solutions/normalization/name-representations.md) | Detailed specialist transliteration/language parsing needs primary verification and project language evidence |
| Which character/token/phonetic similarities fit the error process? | Map/feature-state scope | **Covered for selected mechanisms** | [SOL-06-002](../solutions/comparison-features/string-comparators.md); DEC-06-001 | Exact/edit/Jaro/token/frequency and documented Soundex; other phonetic systems not implied verified |
| When do identifiers justify equality, contradiction or abstention? | Partial namespace prose | **Covered for semantic contract** | [SOL-06-003](../solutions/comparison-features/identifier-namespaces.md); SOL-06-001 | Issuer rules, authoritative assignment, reuse and trust are external facts, not supplied standards |
| How do approximate candidates trade coverage for budget? | Families named | **Covered for selected mechanisms; Partial for specialists** | [SOL-05-003](../solutions/candidate-generation/approximate-blocking.md); DEC-05-001; EVAL-11-001/004/005 | Sorted/shingle/canopy/MinHash mechanisms; ANN/learned roles bounded, internals and edit-specific filters deferred |
| When are manual FS, EM and pooled/source-specific weights defensible? | Core theory and hypothesis | **Covered for bounded comparison** | SOL-07-002; [SOL-07-004](../solutions/matching-scoring/source-aware-reliability.md); HYP-07-001; L3 | Detailed hierarchical inference/calibration guarantees need specialist evidence; source slices may be unidentifiable |
| When does nonlinear/neural capacity justify its labels, access and cost? | Named/deferred | **Covered for selection; Partial for specialist algorithms** | [SOL-07-005](../solutions/matching-scoring/learned-neural-comparators.md); SOL-07-003; DEC-07-001 | General GAM/tree/boosting and specific LLM benchmark scopes; LTR/monotone/embedding implementations remain bounded synthesis |
| How can graph fragility inform review without becoming identity truth? | Bridge warning/constraints | **Covered for diagnosis and logical repair** | [SOL-08-003](../solutions/decision-resolution/connected-components.md); SOL-08-004; DEC-08-001; EVAL-11-003/006 | No duplicate graph card; specialized joint solvers and physical/concurrent repair remain outside this scope |
| Do the proposed refinements need new hypotheses? | Existing frequency/context hypotheses | **Covered by existing owners and controlled routes** | HYP-06-001/HYP-07-001; SOL-12-001 | Named potential methods do not justify new causal claims or empirically validated cards |

Independent scientific critique remains unperformed. Monitoring/governance, physical scale and deeper operational lifecycle stay Wave 4; integration/task patterns and separately frozen utility evaluation stay Wave 5. The [tracker](v1.2-expansion-tracker.md) and [handoff](v1.2-wave-3-handoff.md) retain exact next work and substantive specialist deferrals.

## Validated Wave 2 checkpoint — historical

At that checkpoint, manifest `1.2-wave-2` enumerated **45 cards**: 10 Decision, 21 Solution, 6 Architecture, 2 Hypothesis and 6 Evaluation. The [content review](v1.2-wave-2-content-review.md) records two distinct critiques and author closure of 13 findings. Post-remediation structural lint passed; final outputs and limits are in [validation](../validation/v1.2/wave-2-validation.json). **Covered** below is the integrating author's bounded content judgment, not independent post-remediation approval, runtime validation or measured ER/agent benefit. The [tracker](v1.2-expansion-tracker.md) retains unimplemented algorithmic/operational/agent work.

| Decision question | Wave 1 status | Wave 2 judgment | Canonical route | Bounded responsibility / residual limitation |
|---|---|---|---|---|
| Which boundaries and extension mechanism fit expected changes? | Partial AR/module maps | **Covered** | [DEC-02-001](../decisions/pipeline-modularity.md); [SOL-02-001](../solutions/architecture/replaceable-stage-pipelines.md); AR-01 | Explicit baseline versus hooks, strategies, configuration and DAGs; maintenance effects unmeasured |
| What must each exposed stage preserve when substituted? | Compact contracts | **Covered** | [Module contracts](../taxonomy/module-contracts.md); EVAL-11-006 | Thirteen conceptual roles may fuse or be absent; not a prescribed API/stack or independent guarantee |
| How do ordered policies and tables compose overrides, guards and unavailable states? | No composition family | **Covered** | [DEC-08-002](../decisions/rule-composition.md); [SOL-08-005](../solutions/decision-resolution/ordered-rule-policies.md); [SOL-08-006](../solutions/decision-resolution/declarative-decision-tables.md) | Composition differs from threshold justification and membership-output choice |
| How can a rule refactor be tested without claiming identity improvement? | Generic behavioral tests | **Covered** | [Refactor guide](rule-policy-refactoring.md); [EVAL-11-006](../evaluation/synthetic-metamorphic.md) | Written witnesses and conditional equivalence, not an executed project suite or population accuracy |
| Which artifacts can be reused, invalidated, evaluated and promoted together? | Experiment controls only | **Covered** | [SOL-02-002](../solutions/architecture/versioned-artifact-runs.md); [manifest](run-manifest-template.md) | Full-rebuild comparator; global dependencies, population validity, nondeterminism and downstream compensation; no physical scale guarantee |
| What must incremental state preserve across correction, deletion, replay and IDs? | AR-06 partial | **Covered for bounded contract** | [AR-06](../architectures/incremental-continuous.md); module contracts; existing temporal/master owners | Detailed concurrency, temporal stress cases and operational cost remain Wave 4 |
| What trace explains a decision without proving it correct? | Scattered trace obligations | **Covered for trace interface** | [Decision provenance](decision-provenance.md); manifest; module contracts | Explanation, replay, privacy and identity truth are separate; governance/monitoring depth remains Wave 4 |

## Validated Wave 1 checkpoint — historical

The [tracker](v1.2-expansion-tracker.md) owns remaining work. The [Wave 1 content review](v1.2-wave-1-content-review.md) records two critique passes, one corrected blocking finding and all nonblocking dispositions. Its historical inventory was **39 cards**: 8 Decision, 17 Solution, 6 Architecture, 2 Hypothesis and 6 Evaluation. Original IDs/paths, five types, fourteen domains and six architectures are preserved. These are content judgments after remediation, not measured ER or agent-utility results.

| Decision question | v1.1 checkpoint | Wave 1 judgment | Canonical route | Residual limitation |
|---|---|---|---|---|
| Which annotation units and independent/targeted acquisition design fit the claim? | Partial / active variants deferred | **Covered** | [DEC-10-001](../decisions/ground-truth-acquisition.md); [SOL-10-001](../solutions/ground-truth/independent-reference.md); [SOL-10-002](../solutions/ground-truth/probability-sampled-review.md) | Frame access, completeness and reviewer reliability remain project evidence |
| How can uncertainty/disagreement/diversity/cluster-risk review help research without biasing the final test? | Deferred | **Covered** | [SOL-10-003](../solutions/ground-truth/targeted-active-review.md); SOL-10-002 | Heuristic mechanisms, not universal efficiency or arbitrary IWAL guarantees |
| When are silver, LF or pseudo labels useful, and how do we detect circular evaluation? | Deferred | **Covered** | [SOL-10-004](../solutions/ground-truth/weak-supervision.md) | Project LF assumptions, calibration and independent outcome benefit unmeasured |
| What accuracy is identifiable from positive-only, partial-entity or unresolved truth? | Partial | **Covered for bounded routes** | [EVAL-11-005](../evaluation/incomplete-reference-quality.md); [estimation L3](../deep-dives/incomplete-reference-estimation.md) | PU propensities/response may remain unidentified; no turnkey estimator for every design |
| Which denominators and uncertainty support candidate, pair and final-entity claims? | Covered, operational gaps | **Covered, deepened** | [EVAL-11-001](../evaluation/candidate-recall.md); [EVAL-11-002](../evaluation/pairwise-calibration.md); [EVAL-11-003](../evaluation/entity-resolution-quality.md); [EVAL-11-004](../evaluation/retrieval-blind-spots.md) | Finite-design versus transfer uncertainty; source-4 B-cubed/design variants now explicit |
| Can an opaque retriever be evaluated for missed matches? | Misleading production-selection prerequisite | **Covered, corrected** | EVAL-11-004; EVAL-11-005 | Independent review inclusion/output membership is needed; stage attribution can remain unavailable |
| Which contrast isolates mechanism, interactions or deployable system value? | Partial | **Covered** | [DEC-12-001](../decisions/experiment-design.md); [SOL-12-001](../solutions/experimentation/controlled-comparison.md) | Advanced sequential inference and full power/sample-size derivations remain unexpanded |
| How should a reusable experiment specify controls, splits, unknowns and adoption rules? | Partial guide only | **Covered** | [Experiment-plan template](experiment-plan-template.md); [comparison guide](compare-and-experiment.md) | A plan is not authorization or an execution result |
| What can synthetic, perturbation, metamorphic and property tests establish without labels? | Missing dedicated route | **Covered** | [EVAL-11-006](../evaluation/synthetic-metamorphic.md); [testing guide](er-behavioral-testing.md) | Conditional behavior/generated-domain evidence, never world accuracy |
| Does each method declare an evaluation route? | Existing links, no mandatory gate | **Covered structurally** | [Schema](../SCHEMA.md); [tooling](../tools/README.md) | Resolved links do not prove matching estimands; substantive review remains required |
| Architecture/modularity, rules, MLOps, lifecycle, scale, governance and richer algorithms | Partial / Deferred | **Planned later waves** | [Wave 2–5 tracker](v1.2-expansion-tracker.md) | Not implemented or marked Covered by Wave 1 |

## Historical v1/v1.1 chain

The table and summary below retain the earlier checkpoint. Their `v1.1` statuses are history, not overrides of subsequent wave rows above.

### Chain: Problem formulation → Candidates → Evidence → Scoring → Decision → Resolution → Master → Evaluation

| Question | v1 baseline | v1.1 checkpoint | Knowledge objects | Residual limitation |
|---|---|---|---|---|
| Record vs real-world entity; type/granularity | Missing | **Covered** | [DEC-01-001](../decisions/identity-semantics.md) | Project adjudication still required; no worked domain ontology cards |
| Strict same-as vs related-to; transitivity scope | Partial (AR-05, maps) | **Covered** | DEC-01-001; [DEC-08-001](../decisions/resolution-strategy.md); [SOL-08-003](../solutions/decision-resolution/connected-components.md) | Typed relationship-ER solution families remain taxonomy-only |
| Temporal identity: valid/observation/ingestion time, migration, reuse, succession | Missing | **Covered** | [SOL-01-001](../solutions/identity-semantics/temporal-identity.md); DEC-01-001 | Continuity laws deliberately not hardcoded; no per-domain policy cases |
| Identifier namespace/validity/reuse semantics | Partial (SOL-05-001/DEC-06-001 prose) | Partial | DEC-01-001; DEC-06-001; SOL-05-001 | No dedicated identifier-namespace Solution Card — deferred |
| Source selection rules / admissible pairs | Partial (DEC-05-001) | Partial | DEC-05-001 | Governance-heavy selection policies remain at map level |
| Exact & composite blocking, multi-pass union, marginal yield | **Covered** (unchanged) | **Covered** | DEC-05-001; SOL-05-001; SOL-05-002; EVAL-11-001 | — |
| Approximate/q-gram/LSH/vector/learned retrieval; sorted neighborhood | Deferred (named in DEC-05-001) | Deferred | DEC-05-001 §alternatives; [expansion plan](expansion-plan.md) group 2 | Names only; no mechanism cards |
| Block-size skew, splitting, budgets as quality decisions | Partial (SOL-05-001; domain 13 map) | Partial | SOL-05-001; EVAL-11-004 adds attribution protocol | Physical partitioning/skew execution remains Deferred (domain 13) |
| Evidence states: agreement/missing/invalid/contradiction | **Covered** (unchanged) | **Covered** | DEC-06-001; SOL-06-001 | — |
| Frequency-aware and contextual evidence | **Covered as hypotheses** (unchanged) | **Covered as hypotheses** | HYP-06-001; HYP-07-001 | Explicitly untested |
| Temporal-comparison and multi-valued history evidence | Partial (DEC-06-001 prose) | Partial | DEC-06-001; SOL-01-001 supplies time contract | No dedicated temporal-comparison Solution Card |
| Embedding/graph-context evidence features | Deferred | Deferred | DEC-06-001; opportunities index | Related-to leakage documented, methods unexpanded |
| Additive / Fellegi–Sunter / logistic scoring; score semantics | **Covered** (unchanged) | **Covered** | DEC-07-001; SOL-07-001/002/003; deep dive | Deliberately interpretable-anchor pilot |
| GAM/constrained/boosted/neural/weak-supervision scorers | Deferred | Deferred | DEC-07-001 §unexpanded; expansion group 5 | LLM-assisted comparison also deferred with privacy caveats |
| Thresholds, abstention, review losses | **Covered** (unchanged) | **Covered** | SOL-08-001; EVAL-11-002 | — |
| Which resolution output: pair links / assignment / closure / constrained membership | Missing (maps + AR-05 only) | **Covered** | DEC-08-001 | — |
| One-to-one assignment with unmatched options; competition and ties | Missing | **Covered** | [SOL-08-002](../solutions/decision-resolution/one-to-one-assignment.md) | Utility elicitation remains project work; solver variants are referenced through ledger source 11's context only |
| Connected components and transitive overmerge/bridge risk | Missing (warning prose only) | **Covered** | [SOL-08-003](../solutions/decision-resolution/connected-components.md) | Empirical tail-risk magnitudes are derived illustrations, not measured |
| Constrained clustering: trust of constraints, infeasibility, greedy order | Missing | **Covered** | [SOL-08-004](../solutions/decision-resolution/constrained-clustering.md) | Soft global-optimization algorithms remain family-level; correlation-clustering approximations unexpanded |
| Collective/relational inference beyond constraints | Partial (AR-05; publisher-abstract source 9) | Partial | AR-05; ledger sources 9/10 | Dedicated Solution Card deferred (expansion group 6) |
| Master representation: virtual/golden/hybrid; ID allocation/redirect/split | Missing (map 09) | **Covered** | [DEC-09-001](../decisions/master-representation.md) | Lifecycle rules are synthesis; no worked schema examples |
| Attribute survivorship with provenance; conflicts; corroboration vs copies | Missing (map 09) | **Covered** | [SOL-09-001](../solutions/master-records/provenance-survivorship.md) | Bundle-coherence scoring proposed, untested |
| Identity resolution vs master construction separation | Partial (maps) | **Covered** | DEC-08-001; DEC-09-001; module contracts | — |
| Independent reference construction; entity-centric labeling; splits/leakage | Missing (map 10) | **Covered** | [SOL-10-001](../solutions/ground-truth/independent-reference.md) | Cost model bounded, not measured; active learning deferred |
| Label sampling bias and selection dependence | Partial (eval cards + deep dive) | **Covered** | SOL-10-001; EVAL-11-002/004; deep dive | — |
| Active learning / weak supervision label efficiency | Deferred | Deferred | Domain 10 map; expansion group 3 | — |
| Candidate recall & marginal pass yield | **Covered** (unchanged) | **Covered** | EVAL-11-001 | — |
| Missed-pair estimation outside candidates; nonidentifiability | Missing (requirement noted only) | **Covered** | [EVAL-11-004](../evaluation/retrieval-blind-spots.md) | Protocol only; requires project budget to execute |
| Pair discrimination vs calibration; conditioning population | **Covered** (unchanged) | **Covered** | EVAL-11-002; SOL-08-001 | — |
| Final entity quality: overmerge/undermerge/tail/B-cubed; design-aware estimates | **Covered** (unchanged) | **Covered** | EVAL-11-003 | — |
| Experimentation procedure; controlled ablations; power | Partial (compare guide + hypothesis cards) | Partial | compare-and-experiment; HYP cards; EVAL cards | Dedicated domain-12 Decision Card deferred (expansion group 3) |
| Incremental lifecycle: events, dependency closure, replay | Partial (AR-06 contracts) | Partial | AR-06; SOL-01-001 evaluation hooks | Bounded-vs-adaptive closure comparison deferred |
| Distributed execution, skew-aware partitioning, index cost | Deferred | Deferred | Domain 13 map | Physical-engineering depth intentionally out of scope |
| Explainability requirements of decisions | Partial (SOL-07-001; AR-03/04 traces) | Partial | AR contracts; governance map | No dedicated explanation card |
| Monitoring, drift, recalibration operations | Partial (maps; deep dive conditions) | Partial | Domain 14 map; deep dive | Deferred (expansion group 4) |
| Privacy-preserving / federated linkage guarantees | Deferred | Deferred | Domain 14 map with explicit gap warning | Requires specialist threat-model sources before any card |

## Historical v1.1 summary

v1.1 moved **12 questions from Missing to Covered** (identity granularity, same-as/related-to, temporal identity, resolution-output choice, assignment, closure risk, constrained membership, master representation, survivorship, independent reference construction, missed-pair estimation, plus the Covered identity/master boundary separation), deepened label-bias coverage, and left retrieval families, advanced scorers, physical scaling and privacy explicitly deferred rather than thinly generated. The end-to-end chain `Problem → Candidates → Evidence → Scoring → Decision → Resolution → Master → Evaluation` now has at least one Covered object at every transition; Partial rows name what is still absent. Generated navigation for this graph is the [L0 catalog](../CATALOG.md) and per-domain [L1 indexes](../indexes/domains/).

```text
Total objects at the v1.1 checkpoint: 31 knowledge cards (6 DEC, 13 SOL, 6 AR, 2 HYP, 4 EVAL).
Domain card presence: 01(2), 02(6 AR), 05(3), 06(2), 07(5), 08(5), 09(2), 10(1), 11(4), 12–14(0 standalone).
```

Matrix maintenance: update a row only with a [content-rubric](content-review-rubric.md) review entry; do not inflate status because a file merely exists.
