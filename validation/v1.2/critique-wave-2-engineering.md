# Wave 2 adversarial critique: modularity, artifacts, contracts and lifecycle

## Review identity, boundary and disposition

- **Reviewer:** delegated engineering-family critic, distinct from the author role. Runtime reports model `gpt-6.1-sol` and provider `openai-codex`; model identity and reviewer independence are not independently attested. This is a role-separated critique, not proof of independent-model review.
- **Snapshot:** live working-tree files read on October 14, 2026; SHA-256 capture at `2026-10-14T13:36:30.377713+00:00` appears below. Findings concern those bytes, not a prior baseline or an inferred committed version. The parent owns dispositions and canonical edits.
- **Primary scope:** DEC-02-001, SOL-02-001, SOL-02-002, module contracts, AR-06, the manifest and provenance guides, and EVAL-11-006's engineering section. Normative checks: SCHEMA, evidence policy and the content-review rubric. Targeted foundations: master representation, temporal identity, controlled comparison, candidate recall and pairwise calibration. No whole-repository review, benchmark case/key/result access, ER execution, training, service changes, commit or push.
- **Overall judgment:** **needs revision** for the engineering replay estimand and economy; otherwise the requested safety distinctions are substantially **supported**. One major and six minor findings below; no blocking unsupported guarantee identified in the inspected family. These are documentation findings, not observed software defects or measured outcomes. “Covered” should not imply that any engineering experiment has been executed.

## Findings and bounded remedies

### ENG-01 — Major: the engineering rebuild comparator loses the history/state qualification

**Passage:** `evaluation/synthetic-metamorphic.md:79`, “contrast a clean rebuild with declared reuse on the same corrected snapshot and version bundle.” Compare the stronger qualifications in `architectures/incremental-continuous.md:46,66` and `solutions/architecture/replaceable-stage-pipelines.md:65`.

**Counterexample:** a legitimate published-state policy retains an earlier accepted membership until authorized review reverses it. A corrected final observation snapshot no longer supplies that link. A fresh snapshot resolver splits the entity, while selective repair correctly preserves the pending membership under its stated policy. Identical current observations and component versions do not give identical accepted history, review decisions or ID-allocation state. Calling the difference a reuse violation would reject conforming behavior; seeding both paths from the same stale derived result could conversely mask the defect being tested.

**Judgment:** **needs revision** — assumptions and evaluation estimand. AR-06 already explains path dependence; the local evaluation instruction does not carry that prerequisite into its proposed comparison. This is not a demand for universal order invariance or replaying every historical event in every experiment.

**Proposed bounded fix:** replace the opening of line 79 with: “For cache reuse, compare cache-free computation under identical declared inputs/context. For affected-state repair, choose a history/initial-state-equivalent reference, or a snapshot rebuild only where the contract promises snapshot-determined outputs; freeze accepted corrections, history boundary and ID state as applicable. Do not seed the reference with the derived artifact whose invalidation is under test.” Link to AR-06's affected-closure section; retain the existing failure and oracle qualifications.

**Uncertainty:** a reader following all linked cards may resolve this correctly already. The major rating concerns the locally usable evaluation instruction, not a family-wide assertion that snapshot rebuilding is historical truth.

### ENG-02 — Minor: add a positive witness for candidates that never entered stored state

**Passages:** `taxonomy/module-contracts.md:87`; `architectures/incremental-continuous.md:64`; engineering fixtures at `evaluation/synthetic-metamorphic.md:79`.

**Counterexample:** query A keeps only its top candidate B; C is eligible but not emitted or stored as a pair. Deleting B must reveal C. A repair restricted to stored reverse pair dependencies never visits C. A supposed full comparator that also iterates the old pair table can agree with the broken repair. Logging incomplete scope is honest but does not itself detect this omission.

**Judgment:** the **mechanism and failure explanation are supported**: both contract and architecture explicitly reject treating saved candidates as complete dependencies, and AR-06 directs wider recomputation when scope is unjustified. The observable positive witness is a small **needs revision** opportunity in falsifiability, not missing conceptual coverage. Candidate recall's independently assembled denominator is already correctly owned by `evaluation/candidate-recall.md:33,44–46`.

**Proposed bounded fix:** add one engineering fixture clause: “Use a small eligible universe with an independent exhaustive retrieval oracle: delete a top-ranked candidate and require a previously unstored eligible neighbor to be reconsidered, or explicitly report the unsupported scope.” This tests retrieval reconsideration, not whether that neighbor is a true match. For approximate retrieval, predeclare a bounded property or incomplete result rather than require exact ranking. No production all-pairs requirement or new card is needed.

**Uncertainty:** existing broad “missing dependency” fixtures could include this witness; none is explicitly specified. No such fixture was run by this review.

### ENG-03 — Minor: make retained rollback bundles subordinate to current erasure authorization

**Passages:** `guides/run-manifest-template.md:5,77` (“immutable” finalized records; “retain a prior complete bundle”); `solutions/architecture/versioned-artifact-runs.md:84`. Existing safeguards are explicit at artifact solution lines 37,80, AR-06 line 46 and provenance guide line 42.

**Counterexample:** an authorized erasure removes a source observation and restricted trace content. A prior evaluated bundle or checkpoint still contains that evidence. Its old approval and unchanged digest cannot authorize restoring the erased content through rollback, replay or a cache restore. Merely appending a successor manifest does not remove restricted content from its predecessor.

**Judgment:** **supported** on erasure precedence and replay limitations; **needs revision** on the local retention/rollback wording. No legal-compliance guarantee is claimed, and this finding must not be inflated into one. The issue is reconciling the reusable handoff instruction with its own retention premise.

**Proposed bounded fix:** append to manifest section 7: “Retain prior bundles and finalized records only within current authorization/retention scope. Authorized erasure can withdraw or redact retained artifacts and make rollback/replay unavailable; record that limitation without restoring erased contents.” In the artifact solution, qualify “Preserve the prior bundle” with “where still authorized.” Refer to the existing access/retention sections; do not prescribe model unlearning, a legal rule or an exhaustive purge protocol.

**Uncertainty:** the correct project action depends on the actual erasure/access policy, which is not provided. A logical source tombstone is not automatically a request to erase every derivative.

### ENG-04 — Minor: the artifact card should name the atomic publication boundary locally

**Passage:** `solutions/architecture/versioned-artifact-runs.md:84`, “Atomically publish a consistent bundle of model, normalization/features, retrieval, calibration, policy, and entity state as applicable.” Stronger scoped language exists at `architectures/incremental-continuous.md:82`, `guides/run-manifest-template.md:77` and `guides/decision-provenance.md:22`.

**Counterexample:** a single authoritative bundle pointer changes atomically, but a remote consumer acknowledges a later delta and a separate index replica becomes available asynchronously. That can satisfy a declared version-visibility contract without a global transaction covering all services. Conversely, swapping only a model alias while local retrieval/calibration still exposes old versions is not coherent publication.

**Judgment:** **supported** at family level; **needs revision** for local composability wording. The adjacent alias warning and compensation text correctly prevent interpreting a registry pointer as whole-system validation.

**Proposed bounded fix:** replace “Atomically publish” with “Publish a consistent bundle atomically at the declared authoritative boundary, with explicit version visibility/pending status for consumers outside it.” Keep failure isolation, acknowledgments and compensation. No framework, distributed transaction or cloud capability should be added.

**Uncertainty:** the actual consistency boundary is project-specific; this report does not choose it.

### ENG-05 — Minor: combined manifest rows can accidentally make calibration mandatory

**Passage:** `guides/run-manifest-template.md:52`, row “Calibration / policy,” whose inputs include an independent calibration reference and mapping. Compare `taxonomy/module-contracts.md:11,37–40,47–50`.

**Counterexample:** an authorized deterministic identifier rule emits abstain/link dispositions without probability outputs or a calibration stage. Interpreting all cells in that row as prerequisites requires labels and a probability mapping the policy neither consumes nor needs. The guide's “copy relevant fields” premise prevents a strict contradiction, but the row is less precise than the canonical contracts.

**Judgment:** **needs revision** — responsibility boundaries and hard-versus-optional prerequisites. The family otherwise explicitly allows absent roles, physical fusion and non-probability scoring; it does not impose thirteen stages.

**Proposed bounded fix:** keep one row but qualify calibration inputs/output as “if calibration is used,” and policy inputs as qualified evidence/scores/predicates plus its actual losses/thresholds/review constraints. Do not introduce new role types, a required scoring stage or labels for simple event/refactor checks.

**Uncertainty:** readers who apply the guide's opening instruction selectively will already avoid the mistake. This is an economical clarity fix, not a structural blocker.

### ENG-06 — Minor: maintainer rotation alone does not remove task-order learning

**Passages:** `decisions/pipeline-modularity.md:84–86`; `solutions/architecture/replaceable-stage-pipelines.md:85,89`.

**Counterexample:** each maintainer first diagnoses a difficult source override in the explicit-functions baseline and then diagnoses the identical defect in the plugin challenger. Rotation across maintainers preserves the challenger-second advantage: the underlying cause and test are now known. Faster challenger diagnosis is compatible with no benefit from the extension mechanism. Comparing only scorer substitution also does not estimate deletion/migration maintenance value.

**Judgment:** broad engineering **falsifiability is supported**: credible baseline, fixed tasks/tools/budgets, practical margins, defect/cost guardrails and adopt/reject/inconclusive outcomes are present. **Needs revision** only for an explicit order/carryover control. The cards already disclose skill/learning effects; do not describe them as claiming unconfounded causal proof.

**Proposed bounded fix:** add one sentence to the decision's experiment paragraph: “Counterbalance configuration/task order where feasible, use matched nonidentical task instances to limit solution carryover, and record prior familiarity; distinguish initial setup/migration cost from later task cost.” Retain remaining-confounding disclosure and the narrow task-support limitation. Do not prescribe a statistical model or invent worthwhile margins.

**Uncertainty:** small teams or rare changes may not permit counterbalancing; that limits the inference rather than invalidating descriptive task evidence.

### ENG-07 — Minor: remove repeated exposition, not local safety caveats

**Passages:** the same extension-family menu appears in `decisions/pipeline-modularity.md:45–55` and `solutions/architecture/replaceable-stage-pipelines.md:48–55`; invalidation exposition repeats in artifact solution lines 62–72 and manifest lines 63–67; global-dependency foundations repeat across decision lines 64–68, replaceable solution lines 73–75, contracts lines 84–89 and AR-06 lines 62–66.

**Concrete reading counterexample:** an agent deciding whether a single scorer needs injection can follow decision → solution → contracts → manifest and reread the same global-frequency/retrieval-calibration warning and extension menu before finding a concrete substitution/rejection obligation. Conversely, deleting all those local warnings would make an independently retrieved card unsafe. The problem is duplicate exposition and weak reading triage, not the existence of guides or an informational word limit.

**Judgment:** **needs revision** — economy; **supported** — responsibility ownership. Measured whitespace body-word counts, including headings/references, are DEC 1,124; replaceable SOL 1,141; artifact SOL 1,319; AR-06 1,964. SCHEMA's usual 400–900-word L2 guidance is informational, so these counts alone are not rejection evidence. Contracts and guides need not fit the L2 card range.

**Proposed bounded fix:** keep the full alternative comparison in the decision; compress the solution's repeated six-item menu to a short selection paragraph linking that comparison. Keep the artifact solution's invalidation table canonical; turn the manifest's duplicate discussion into one filled conceptual example plus that link. Retain role-specific invariants in contracts and event/history/ID distinctions in AR-06. Add a one-line retrieval cue: contracts for boundary substitution, manifest only for realized run packaging, provenance only for explanation, AR-06 only for evolving state. No new card, taxonomy or encyclopedia is warranted.

**Uncertainty:** no timed agent retrieval study was run. This is a passage-based economy judgment, not a measured reading-time improvement.

## Adversarial checks that are already supported

| Challenge / rubric dimension | Actual support and counterexample boundary |
|---|---|
| Hidden global dependencies | DEC lines 64–68, replaceable SOL lines 38,73, artifact SOL lines 66–70 and contracts lines 84–88 explicitly expose corpus statistics, indexes, priors, feedback and closure. Adding one unchanged-field observation can alter other scores; no locality guarantee is asserted. ENG-02 concerns a witness, not absence of this warning. |
| Provenance versus proof | Provenance guide lines 13–22,30–38 distinguishes explanation, historical replay, counterfactual and identity correctness. A fully traced incorrect merge remains incorrect. Artifact provenance does not become same-as evidence or a privacy certificate. |
| Raw scores and population probabilities | DEC line 60; replaceable SOL line 42; contracts lines 38–40; pairwise evaluation lines 27–29 separate raw sums, likelihood ratios and candidate/full-population probabilities. A schema-compatible `score` substitution is expressly insufficient. Candidate-calibrated probabilities are not promised for never-retrieved pairs or clusters. |
| Serving reuse, retraining, recalibration | Artifact SOL lines 72,82 and manifest lines 65–67 separate frozen serving weights, fitting and calibration dependencies. A changed reference may require reevaluation only; a changed retriever requires applicability review, not an automatic universal retraining/threshold rule. |
| Metadata, snapshot and determinism limits | Artifact SOL lines 37,45,80; manifest lines 25,31,37,39; provenance line 30 reject mutable locators, seed-only guarantees and hash-as-reconstruction/anonymization. A captured random output is one realization, not evidence about its distribution. |
| Full rebuild versus history | AR-06 lines 44–46,66 clearly separates current-state journal, authoritative event history, historical replay, corrected replay and snapshot recomputation. All are comparators, not identity truth. ENG-01 requests that the evaluation preserve this distinction. |
| Stable ID mapping versus permitted allocation differences | AR-06 lines 78–82; master representation lines 43,51; EVAL lines 69,77; AR-06 line 106. Unpublished transient allocation can differ when permitted; a changed published ID or one-to-many split cannot be normalized away to improve agreement. Match partitions on fixed observation-version keys separately from the promised public-ID/redirect/as-of mapping. No universal bitwise-ID requirement is needed. |
| Tombstones and late events | AR-06 lines 52,70–72 rejects duplicate-key/different-payload idempotent success, last-arrival-wins and stale resurrection. A source deletion is not entity death; an incomparable revision remains explicit. These are proposed contracts, not executed stress tests. |
| Erasure and replay availability | Artifact SOL line 37, AR-06 line 46 and provenance guide lines 40–46 explicitly subordinate retention to authorization and disclose unavailable reconstruction. ENG-03 tightens the local rollback wording; it does not demand perpetual history. |
| External-effects replay and scoped publication | AR-06 lines 56,82–84; provenance lines 22,30; manifest line 77 distinguish a local commit, consumer adoption and compensation. Replaying a membership event must not automatically resend billing/notification writes. Captured historical responses are distinct from today's external query results. |
| No compulsory framework/cloud/new AR/taxonomy | DEC lines 27,31,58,72; replaceable SOL lines 36,39,55–57; artifact SOL lines 29,49–52; contracts lines 3,98; AR-06 lines 29–38. Explicit functions and cache-free recomputation remain credible baselines; event sourcing and DAG scheduling are optional design choices, not required ER algorithms. |

## Source/version review

Source-bearing statements were checked against the supplied full-text extracts in `/home/ghgin/.hermes/cache/scratch/atlas-wave-2-sources/`; the shared ledger was read-only. Direct HTTP retrieval additionally succeeded for all four primary URLs and checked the source-specific markers (DVC sequential execution, W3C's publication date, MLflow's mutable alias description and Fowler's essay date/external-query section). A separate extraction attempt reported a search-only backend; direct retrieval resolved that tool limitation. Source judgments below remain bounded to the cited versions, not a claim about the latest software releases.

- **DVC, ledger source 24:** unversioned Running Pipelines documentation; supplied `primary-3.txt:49–94` supports sequential dependency/output DAG execution, unchanged declared-stage skipping and run-cache recovery.[24] The exact installed DVC version is neither known nor needed for this bounded illustration. DEC, both solutions and manifest do not treat that example as discovery of undeclared ER dependencies or an engineering speedup theorem. **Source scope: supported.**
- **W3C, ledger source 25:** PROV Model Primer, Working Group Note dated April 30, 2013; supplied `primary-4.txt:347–476` covers entities, activities, responsibility, generation/usage and revision.[25] The artifact solution, manifest and provenance guide correctly restrict their application to artifact/activity vocabulary, not identity equivalence, trust or validation. **Source scope: supported.**
- **MLflow, ledger source 26:** documentation explicitly pinned to **3.3.1**; supplied `primary-5.txt:98–113` describes mutable version aliases and tags.[26] Artifact solution line 84 and manifest line 37 use this only as a bounded alias example and expressly deny validation/whole-bundle atomicity guarantees. No claim about the latest MLflow release is made. **Source scope: supported on supplied versioned full text; direct live retrieval also confirmed the mutable-alias marker.**
- **Fowler, ledger source 28:** Event Sourcing essay dated December 12, 2005, explicitly draft-form; supplied `primary-7.txt:236–269,528–613` supports state-changing event history and the external-update/query replay hazards.[28] AR-06 labels its ER lifecycle design as synthesis, not an ER proof or empirical performance result. **Source scope: supported.** Source 23/DMN was unnecessary for this family review; rule-interaction internals were not reviewed.

## Rubric summary and uncertainty

| Rubric criterion | Judgment |
|---|---|
| Mechanism | **Supported:** explicit boundary substitution, dependency-aware reuse and affected-state lifecycle mechanisms, without assumed accuracy gains. |
| Assumptions | **Needs revision:** carry the history/initial-state prerequisite into EVAL's comparator; other namespace/population/score/time assumptions are explicit. |
| Failure modes | **Supported:** concrete stale-state, bridge, competitor, calibration and replay failures; ENG-02 improves the unstored-candidate witness. |
| Alternatives | **Supported:** simple functions/current-state journal/full recomputation versus justified extension, caching and event-history choices. |
| Falsifiability | **Supported with minor strengthening:** controlled behavior/cost tasks, margins and guardrails; counterbalance carryover when feasible. |
| Source scope | **Supported within checked source versions:** no framework marketing imported as ER validation. |
| Evidence discipline | **Supported:** theoretical synthesis and nonexecution are explicit; replay/equivalence is not truth. |
| Composability | **Needs minor revision:** conditional calibration inputs and locally scoped publication wording; independent architecture dimensions remain preserved. |
| Economy | **Needs revision:** duplicate menus/invalidation exposition can be trimmed without new objects or removing necessary safety warnings. |
| Responsibility boundaries | **Supported with ENG-05 qualification:** contracts, artifact packaging, provenance and lifecycle have distinct owners. |
| Evaluation estimand | **Needs revision:** ENG-01; synthetic conformance and independently referenced identity quality otherwise remain separate. |

No result from structural lint, a benchmark or an ER harness is claimed. Report-only verification found that its Sources block matches the ledger mechanically, ordinary citation verification passes, and all recorded primary-file/ledger fingerprints remain unchanged. Strict citation verification warns/fails because the read-only shared ledger also contains unrelated sources not cited in this bounded report; no ledger entries were removed to suppress that warning. This review does not establish dependency completeness, temporal label representativeness, lawful replay access, a working atomic publisher or lower maintenance cost in any real project. Wave 4's deeper operational/concurrency scope remains deferred rather than silently imposed here. The parent can resolve these bounded edits without expanding the family or changing evidence maturity.

## Reviewed snapshot fingerprints

| Path | SHA-256 |
|---|---|
| `decisions/pipeline-modularity.md` | `5cba3ca23d9600f26f6d56d55ad020822d801d0194a488dbbc9ffa7aac550cae` |
| `solutions/architecture/replaceable-stage-pipelines.md` | `ab8903e14079156f1283dea60e6a6682edf6491223912c9f75d61e92adeeb9b0` |
| `solutions/architecture/versioned-artifact-runs.md` | `2f747460fb8d6cf4fd90eeafa869b8c96768d2259321059c3a91f0df5f594464` |
| `taxonomy/module-contracts.md` | `cc240bcfe8b5c9caa58c846039c37c78f1f8ecb243e5dbe8e26826d9e5abc694` |
| `architectures/incremental-continuous.md` | `eb6a4848fd8ae673d68c79ff77f96e32156e9d17a9179fa1e767df7c783f8b86` |
| `guides/run-manifest-template.md` | `7b2cad7c8b9c18e6db173993accddebac4d3fb0d1adc20810e4a8f35938ce50a` |
| `guides/decision-provenance.md` | `e15ae031b759e4460e308a5f5ea7b222ae1e761c6fc12e341e332c691fa12cf9` |
| `evaluation/synthetic-metamorphic.md` | `b54555d0f240df744767dc00d3650f46e079ea31ae1a1a333c73c5ce4d5847f9` |
| `references/source-ledger.json` (read-only) | `dba1af71ad83550385f61785af93f4a17acd8871b0e8b25aceb470f3e6f0813e` |

## Sources

[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
[25] https://www.w3.org/TR/prov-primer — PROV Model Primer
[26] https://mlflow.org/docs/3.3.1/ml/model-registry — MLflow Model Registry (3.3.1)
[28] https://martinfowler.com/eaaDev/EventSourcing.html — Event Sourcing
