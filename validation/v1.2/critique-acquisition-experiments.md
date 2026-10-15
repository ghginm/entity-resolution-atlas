# Adversarial content review: acquisition, weak supervision, experiments, and behavioral tests

## Review identity and boundary

- **Reviewer:** Hermes fresh acquisition/experiments critic, separate from the incomplete-reference critic and document authors.
- **Review date:** 2026-10-13, EDT; initial local snapshot record `2026-10-13T23:23:31-04:00`, final changed-document reread record `2026-10-13T23:32:31-04:00`.
- **Protocol:** `guides/content-review-rubric.md`, with `SCHEMA.md` and `references/evidence-policy.md` as normative context.
- **Snapshot:** the file SHA-256 values below. `HEAD` is unavailable: this repository has an unborn `main` branch, so no commit hash is asserted.
- **Reviewed family:** DEC-10-001; SOL-10-001 through SOL-10-004; DEC-12-001; SOL-12-001; EVAL-11-006; the two supporting guides listed below.
- **Selective consistency read:** `evaluation/incomplete-reference-quality.md` only. Its final review, its L3 derivation, source 17, and source/card totals belong to the parent/other critic; no judgment of their completeness is made here.
- **Forbidden material/actions:** no benchmark keys, scenarios, or results were read; no ER implementation, data processing, training, behavioral-suite execution, commits, or canonical-document edits were performed.

This is a distinct scientific/content critique, **not an independently executed or scored agent-utility benchmark**. Neither favorable rubric judgments nor the proposed counterexamples establish measured agent utility or production ER quality.

## Overall judgment

**No blocking scientific/content finding identified in this snapshot.** The family is **Covered for its explicitly bounded decision-support questions**, not for every acquisition algorithm, every testing invariant, or any accuracy guarantee. Five nonblocking clarifications are actionable below. The strongest remaining issue is inconsistent wording about variance and split scope across otherwise careful cards; it does not conceal absent labels or endorse an unsupported quality claim.

The review actively tried to break the separation between research acquisition and representative evaluation, selection and response, silver labels and truth, component and system effects, and behavioral conformance and world accuracy. Those major boundaries survive the counterexamples below. Length alone is not a rejection criterion; the longer cards add operational contracts and causal failure cases rather than merely expanding headings.

## Rubric judgments

| Criterion | Judgment | Passage-based reason / limitation |
|---|---|---|
| Mechanism | supported | `targeted-active-review.md:36–41` specifies ranking, evidence-bearing feedback, authorized updating and stopping. `weak-supervision.md:35–39` separates votes, aggregation and training. `controlled-comparison.md:35–39` identifies freezes, dependency checks and paired execution. |
| Assumptions | needs revision, nonblocking | Identity/time/namespace/evidence assumptions are explicit. Unconditional entity-holdout wording in SOL-10-001 and SOL-10-004 is broader than SOL-12-001's intended-transfer distinction; see AE-N1. |
| Failure modes | supported | SOL-10-001 names abandoned large entities and common search omissions; SOL-10-003 separates unlearnable ambiguity from confidence errors; SOL-10-004 gives a copied-name versus registry counterexample. Diagnostics include additions, reversals, unresolved cases and source slices. |
| Alternatives | supported | Uniform and stratified review, complete entity search, targeted learning, explicit rules, majority votes, label models and small gold-supervised learning have different mechanisms and budget demands. No universal preference is asserted. |
| Falsifiability | supported | DEC-12-001:41–45 separates conditional component contrasts from integrated comparisons; SOL-12-001:49 distinguishes removal from refitting. AE-N3 and AE-N5 would make acquisition-comparator and repetition specifications easier to use. |
| Source scope | supported | Checked primary-source passages support the limited survey, IWAL, Data Programming, Snorkel, factorial and testing claims. Theory is not transferred to arbitrary ER heuristics. Theorem pointers/simplification could be clearer; AE-N4. |
| Evidence discipline | supported | Explicitly no locally measured gains; unknowns remain unknown; intervals require a design; stochastic reruns and synthetic passes are not new independent truth. |
| Composability | supported | Probability audits complement active/weak training. Accepted-graph closure is separated from admission policy. Changed candidates can invalidate calibration even when downstream code is unchanged. |
| Economy | supported | Acquisition chooses the evidence route, solutions construct artifacts, experimentation controls contrasts, and EVAL-11-006 defines behavioral denominators. Repeated warnings mostly appear at actual handoff risks. No need to reproduce scorer derivations or the incomplete-reference L3 material here. |
| Responsibility boundaries | supported | SOL-10-004 does not certify reference truth; SOL-10-003 does not authorize production corrections; the guide does not make weak-bridge rejection a connectivity algorithm. |
| Evaluation estimand | needs revision, nonblocking | Sampling support, inclusion versus draw probability, unknown labels and response mechanisms are carefully distinguished. Generic dependence language in SOL-12-001/template needs the finite-population versus transfer qualification already present in SOL-10-002; AE-N2. |

The two “needs revision” judgments identify local wording improvements, not the rubric's blocking conditions. No unknown-as-negative rule, hidden unavailable required evidence, wrong cardinality prescription, irreversible high-harm merge recommendation, or arbitrary guarantee was found.

## Source-scope verification

Local source material was inspected selectively in `/home/ghgin/.hermes/cache/scratch/atlas-v12-sources/`. Text line numbers below refer to those extraction files, not repository cards. Source 4's arXiv v1 entity-sampling sections were additionally checked selectively through the primary text; a fresh full-paper or supplementary-proof audit is not claimed.

| Ledger source / version checked | Checked locus and scope finding |
|---|---|
| 15 — Statistics Canada, *Survey Methods and Practices*, cached official PDF | §6.2.6 (`15.txt:5809–5870`) conditions efficiency on useful strata, rather than universal variance reduction. §7.1.3 (`6747–6785`) requires assumptions linking respondents to nonrespondents. The cards correctly do not equate seed/selection probabilities with successful annotation probabilities. Survey principles do not validate the proposed ER acquisition workflow.[15] |
| 18 — *Importance Weighted Active Learning*, arXiv v4, 20 May 2009 | §§2–4, `18.txt:117–248`: Theorem 1 is the bounded-loss, finite-class safety result with a positive query-probability floor. Theorem 2 concerns the particular loss-weighting hypothesis-set construction and does **not** require that floor. SOL-10-003:47 preserves this distinction. Conditional stream query probability is not a repeated adaptive pool unit's inclusion probability. Neither theorem guarantees arbitrary uncertainty/bridge-risk heuristics, unbiased annotation under nonresponse, or ER gains.[18] |
| 16 — *Data Programming*, NeurIPS 2016 main paper | §3, `16.txt:186–284`: balanced independent LF model, specified accuracy/coverage ranges, conditions (4)–(6), and **Theorem 1** with the simplified `m ≥ 2000` statement; the immediately following paragraph says the appendix treats arbitrary `m`. §4, `349–390`: **Theorem 2** invokes conditions (5)–(9), including feasible models, labeled-sample learnability and conditional variance. SOL-10-004 states substantive conditions rather than a general unlabeled-vote identification guarantee. Supplementary proofs were not checked.[16] |
| 21 — *Snorkel*, PVLDB 11(3), cached publisher PDF | §2 (`21.txt:324–350`) explicitly includes a small labeled development set and blind held-out test, and describes vote aggregation followed by discriminative training. §4.1 (`1006–1018`) controls end-model choice and tunes on development labels. These support the card's pipeline/independent-evaluation boundary, not ER superiority or calibration of arbitrary LF posteriors.[21] |
| 4 — *How to Evaluate Entity Resolution Systems*, arXiv v1 | §§3.2–3.4 permit prediction-assisted annotation and connect probability-sampled complete entity memberships to design-specific estimation. SOL-10-001:28,44–46,88 accurately distinguishes the paper from the Atlas's stricter independent-search proposal and warns against using incomplete supported size as complete size.[4] |
| 20 — NIST/SEMATECH two-level full factorial page, cached official HTML | The analysis-matrix example (`20.html:316–365`) contains factor and interaction columns and replication. It supports crossed design structure, not a uniquely causal ER interpretation of a nonlinear metric or infeasible cells. DEC-12-001 labels its contrast as derived and scale/design-specific.[20] |
| 19 — HKUST-CS98-01, 1998 technical report | Introduction/preliminaries (`19.txt:78–106,124–138`) motivate follow-up cases using domain knowledge and limits on production-side mutation. EVAL-11-006 and the guide claim general testing concepts only; their ER fixtures and rate definitions are Atlas synthesis.[19] |
| 22 — official Hypothesis “latest” introduction, cached HTML | `22.html:253–411` provides strategies/assertions and explicitly describes property testing as an addition, not always a replacement, for unit testing. It does not establish an iid confirmation-sample design or a real-world ER error rate. The cards correctly supply those additional conditions themselves.[22] |

**Identifiability stress test:** the card's class-orientation warning is explicitly Atlas reasoning, not attributed as a proved Data Programming theorem. In an unrestricted latent binary model, relabeling the hidden classes can leave the visible votes unchanged. Semantic anchors or additional restrictions/evidence are needed; mere LF count, overlap, or a dependency graph is not a sufficient certificate. The card does not claim otherwise. Do not later rewrite “Theorem 2 bounds” into “any dependency-aware label model identifies truth.”

## Actionable nonblocking concerns

### AE-N1 — Qualify entity-disjoint splits by the promised transfer task

- **Status:** nonblocking, medium; assumptions/composability wording needs revision.
- **Passages:** `solutions/ground-truth/independent-reference.md:60`: “Hold out whole entities across training, calibration and evaluation.” `solutions/ground-truth/weak-supervision.md:86`: “Freeze candidates, features, admissible sources, downstream policy and entity-disjoint splits”. Compare `solutions/experimentation/controlled-comparison.md:57`: “Use entity-disjoint partitions when testing transfer to new identities” and its separate existing-entity-continuation contract.
- **Counterexample:** deployment receives a later observation of an already resolved identity and legitimately sees historical membership. A universal entity-disjoint experiment removes exactly that historical state and measures a different task. Conversely, allowing recurring aliases in a new-identity experiment leaks identity evidence.
- **Remedy:** make whole-entity separation conditional on new-identity transfer; for continuation require forward-time, as-of features/history and prohibited label access. Point both acquisition solutions to the canonical split discussion. Keep audits of uncertain identity overlap and forbid final-label feedback in either task.
- **Why not blocking:** the experiment decision, protocol and template already distinguish intended transfer and historical state; no empirical estimate or unconditional deployment recommendation depends on the broader sentences.

### AE-N2 — Preserve the distinction between design variance and superpopulation dependence

- **Status:** nonblocking, medium; evaluation-estimand wording needs revision.
- **Passage:** `solutions/experimentation/controlled-comparison.md:75`: “preserving inclusion weights, strata, and entity/graph dependence; cross-entity pairs need both endpoints' dependence addressed.” `guides/experiment-plan-template.md:63` lists “entity/graph dependence, and cross-entity endpoint dependence”. In contrast, `solutions/ground-truth/probability-sampled-review.md:75` explicitly says shared-entity labels do not automatically invalidate finite-population random-pair variance.
- **Counterexample:** a genuine simple random pair audit has fixed adjudicated finite-population outcomes. Pair inclusion dependence, not an automatically imposed entity-cluster model, governs its design variance. For transfer to new identities or correlated reviewer error, endpoint/shared-entity dependence can become essential. Treating these as one universal bootstrap requirement risks answering the wrong uncertainty question.
- **Remedy:** add the SOL-10-002 qualification to the protocol/template: first name finite-population design uncertainty versus transfer/model, reviewer-error and algorithm uncertainty; then choose compatible units/replicates. Do not prescribe endpoint clustering universally or replace actual survey stages with arbitrary clusters.
- **Why not blocking:** “paired design-aware uncertainty” is already required and the connected sampling card supplies the correct qualification. No invalid interval is reported here.

### AE-N3 — Separate audit-allocation experiments from learning-acquisition experiments

- **Status:** nonblocking, minor; comparator specification could be clearer.
- **Passage:** `solutions/ground-truth/probability-sampled-review.md:75`: “Compare uniform, stratified and hybrid allocations under equal total cost, with evaluation reserve fixed across learning arms.”
- **Counterexample:** if the experiment varies the **audit** allocation, the audit pool/design is the treatment, so it cannot simultaneously remain the same artifact in every allocation arm. If it varies **learning** acquisition, changing the test reference alongside the query strategy confounds apparent downstream benefit with different observation support.
- **Remedy:** state two distinct comparisons: (a) audit-design precision/coverage/reference-error at matched review costs and valid design-specific analysis; (b) learning-strategy quality/cost on a common protected evaluation reserve. For joint optimization, use an explicit crossed/system design and do not attribute its result to acquisition ranking alone. Keep attempted, resolved and unknown reviews in cost accounting.
- **Why not blocking:** “across learning arms” already points toward the correct reading. This is an ambiguity at the handoff, not a claim that an unchanged test can measure changed audit allocation.

### AE-N4 — Name the Data Programming theorems and distinguish an illustrative floor from a practical requirement

- **Status:** nonblocking, minor; source-navigation precision.
- **Passage:** `solutions/ground-truth/weak-supervision.md:45`: “Its displayed theorem needs at least 2,000 LFs”; line 47 then describes “The dependent extension”.
- **Counterexample:** an operational reader could reject a defensible small-LF pilot merely because it has fewer than the displayed floor, or assume adding duplicated LFs satisfies meaningful theory conditions.
- **Remedy:** identify **main-text Theorem 1** and **Theorem 2** explicitly; say the floor belongs to the simplified display, not a recommended/minimum operational LF count. Mention that the main paper points to arbitrary-count appendix results, while retaining the honest “supplementary proofs not reviewed” limitation. Do not claim those unreviewed proofs establish a small ER rule set's validity.[16]
- **Why not blocking:** “displayed theorem” is accurate; correct specification and other substantive assumptions are stated, and the copied-evidence/identifiability counterexample already defeats a count-only guarantee.

### AE-N5 — Make split variation explicit rather than hide it inside repetitions

- **Status:** nonblocking, minor; experiment reproducibility/interpretation improvement.
- **Passage:** `guides/experiment-plan-template.md:64`: “Predeclared seeds/repetitions, matched randomization where justified, aggregation, all-run disclosure, and stochastic variation separate from label-sampling uncertainty.” SOL-12-001:49 and75 correctly say stochastic runs are not additional independent labels.
- **Counterexample:** repeated acquisition or training seeds on one favorable entity/source split can look stable while another permissible split changes the ranking. Repeatedly changing the final holdout until a gain appears would instead be adaptive test selection, not valid replication.
- **Remedy:** distinguish acquisition/training/generator seeds, prespecified development-split repetitions where useful, frozen final contrasts, and genuinely fresh transfer replications. Record split IDs and aggregation before outcomes; account for overlapping entities/labels across repeated splits. Do not require random split repetition for every design, and do not call it new independent truth.
- **Why not blocking:** split assignments, multiplicity, all-run reporting and holdout invalidation are already present. The gap is an explicit checklist distinction, not best-seed approval.

## Adversarial challenges that did not expose a blocker

1. **Research-optimized labels presented as representative truth.** DEC-10-001:37 says “A random train/test split of selectively acquired labels preserves that selection”. SOL-10-003:79 says “Discovery yield alone cannot establish population performance.” A deterministic boundary sampler missing confident errors cannot pass as a full-population audit. **Judgment: supported; retain these boundaries.**
2. **Known sampling support used to excuse unresolved labels.** SOL-10-002:55: “Known selection probability is not known response probability.” Suppose difficult cross-script matches are abandoned while easy nonmatches resolve; inverse seed weights alone cannot remove that response bias. Match/nonmatch/unknown and separate abandonment dispositions are explicit. **Judgment: supported.**
3. **A tiny complete reference treated as the entire truth.** SOL-10-001:46: “supported size is not silently the complete size”; line80 requires sampling-aware precision and carries reference uncertainty. One fully resolved conveniently chosen entity can demonstrate an error, not its prevalence; a probability sample of complete entities may support estimation but remain too imprecise for adoption. The selectively read EVAL-11-005 distinguishes complete sampled entities from a clipped labeled partition. **Judgment: supported; no whole-truth shortcut found.**
4. **Label counts substituted for fair cost.** DEC-10-001:51 says “An entity annotation and an easy pair judgment are not interchangeable budget units.” SOL-10-003:71,79 count unresolved queries, search, specialist review and retraining. SOL-10-004:86 includes LF construction/tuning rather than treating programmatic supervision as free. A targeted arm with fewer successful labels but extensive failed investigations may lose at matched cost. **Judgment: supported.**
5. **Copied weak labels masquerading as independent evidence.** SOL-10-004:78: “Disjoint rows do not remove the shared label authority or systematic rule errors.” A held-out sample generated by the same mistaken name rules rewards imitation. The registry counterexample supplies an independent semantic contradiction, with its namespace/time prerequisites checked. **Judgment: supported.**
6. **An arbitrary active-learning guarantee imported from IWAL.** SOL-10-003:28 and47 distinguish source-specific randomized construction from heuristic proposals. A deterministic entropy ranking with zero support on confident mistakes and unknown evidence response does not inherit the theorem. **Judgment: supported within the source scope documented above.**
7. **Fixed-pool gain renamed end-to-end benefit.** DEC-12-001:41 excludes retrieval completeness from a fixed-candidate result; line63 warns a union pool is not a production retriever. A scorer that improves ranking only inside the union of retrievers cannot prove one retriever admits the needed matches. Feasible integrated output remains required. **Judgment: supported.**
8. **Factorial interaction overinterpreted or infeasible cells invented.** DEC-12-001:59 calls the contrast “score-scale- and design-specific”; line63 requires a revised question for incompatible cells. A changed candidate distribution can require fresh calibration even if scoring code is unchanged; an incompatible retrieval/scorer cell cannot be fabricated. **Judgment: supported.**
9. **A passing synthetic/metamorphic suite treated as world accuracy.** EVAL-11-006:47 restricts its probability target to fixed `Q`, valid prerequisites and execution/oracle coverage; lines57,77 distinguish adaptive discovery from independent confirmation. A constant matcher can pass preserving transformations yet fail collision controls; the guide:27,44 specifically adds identity-changing tests. Selected regression fractions and related transformations are not independent real-population draws. **Judgment: supported.**
10. **Weak-bridge rejection made a closure invariant.** `guides/er-behavioral-testing.md:50`: “Connected components should join the groups: this is conformance to closure and, in the constructed world, an identity error.” A fixed accepted bridge must join connected groups; below-threshold admission and hard constraint conflicts are different boundaries. The guide also preserves alternate-path and one-to-one duplicate-free prerequisites. **Judgment: supported.**

These are analytical counterexamples, not execution results. Passing this adversarial reading does not mean any proposed acquisition arm, LF model, resolver, behavioral suite or agent recommendation has been run successfully.

## Prioritized disposition

1. Clarify AE-N1 and AE-N2 before consumers turn the generic protocol into a project-specific split/uncertainty plan.
2. AE-N3 through AE-N5 are useful authoring refinements; no need for new parallel theory cards or a larger bibliographic expansion.
3. Retain the adoption/rejection/inconclusive routes and prohibition on invented margins/results. Fresh evidence is needed after holdout-driven repair; repeated seeds are not a substitute.
4. No canonical edits or coverage-index changes were made by this reviewer. Source/card totals and the independent-reference estimator deep dive remain the parent's verification responsibilities.

## Snapshot fingerprints

SHA-256 identifies the reviewed bytes, not scientific validity. Paths below are relative to the repository root.

| Reviewed document | SHA-256 |
|---|---|
| `decisions/ground-truth-acquisition.md` | `217a9b330fc339933907a336101978d828fba81702fd9b7b9169257b21ab2f57` |
| `solutions/ground-truth/independent-reference.md` | `1b004b8384f63942ea76a5223980b8b815a8144abd44e8c762c6e53ff11a255d` |
| `solutions/ground-truth/probability-sampled-review.md` | `69fc25ad986f1a120159fe63f9210a9010765d9513559515f55ea0c9ec3ff1b9` |
| `solutions/ground-truth/targeted-active-review.md` | `5c3668755b34eaddc2f2dd14c7a7dfed962e84389cf9dd4922cd4e363a12b824` |
| `solutions/ground-truth/weak-supervision.md` | `b280883cf770ac59c231e5aa707e60abd0f41da9e82bf74694891bb02ab9ad9a` |
| `decisions/experiment-design.md` | `e2ba7cb2c85991232972c871db7c867d22fd5913893e8df4219d5893f22cf8b4` |
| `solutions/experimentation/controlled-comparison.md` | `bf7e711a2cb4569a86037de87f8328714f1b85b73f94feb28214cd4261af30c5` |
| `evaluation/synthetic-metamorphic.md` | `fecbbcb40ccb32dd965f48748e5e755dee0d247c32dd812d577087fe4966aba1` |
| `guides/er-behavioral-testing.md` | `2d3c1fdbfe34b4e3acbe5e2f0b41afb0abdccd9bb43b71851e202c775f2cc5d9` |
| `guides/experiment-plan-template.md` | `243b5093ace11f782ed6312011ea05c8c5293615391edc17d2ac5f7246df1348` |

Cached external files are outside the repository; their fingerprints preserve which source copies were consulted. Source 4 was a selective primary-text web check, not one of these cached files.

| Cached source file | SHA-256 |
|---|---|
| `15.pdf` | `ee016aa1303e94c412a67e824f392a43b9ef04b13c51fc1649d5293cb766b31b` |
| `16.pdf` | `54f91b929f910218c05ffb47f10cd9e061afe04a019bc5f882c363d24b7705b5` |
| `18.pdf` | `b6381912c3b3922dbf36e1f0c6d521981c440bcbdda1ed9b10ca2202ac50c030` |
| `19.pdf` | `a2095b46cebac69051c7d5e6eb16bea4c0ddce5f1981182852c929a4167e131b` |
| `20.html` | `e549492766b04444ca97c61f0edbfe11d6e7b2f10aa24afe2e2e572c791879c7` |
| `21.pdf` | `efd3784f0ea27a2c3d10270d269b661e2c08ae34fe9d7c3985d97db5426bd558` |
| `22.html` | `721c97c5ccf6428530bde575a9e7a02247b46122d3d2cce2908022305e7be030` |

## Verification limits and encountered issues

- The review checked source scope and literal repository passages; it did not reproduce theoretical proofs, source experiments, ER algorithms or benchmark scoring.
- A commit identifier could not be recorded because `HEAD` does not exist; content hashes substitute for snapshot identity.
- An optional BeautifulSoup extraction attempt found the package unavailable. Inspection of the official cached Hypothesis HTML recovered the relevant passage; no installation or environment modification was needed.
- The configured page-extraction backend could not extract source 4; direct retrieval from the primary arXiv v1 HTML recovered the relevant labeling and estimation sections.
- Two reviewed documents acquired `no-labels` metadata tags concurrently. Both were reread; their substantive passages and line references were unchanged. The table records the updated hashes, not the superseded initial bytes.
- The shared-ledger citation verifier passed in its default mode. Strict mode flags ledger sources intentionally unused by this scoped report; no source IDs were removed and the report's Sources block was rendered mechanically.
- No blocker prevents delivery of this report. Follow-up clarifications above remain recommendations for the authors, not edits made here.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
[16] https://proceedings.neurips.cc/paper_files/paper/2016/file/6709e8d64a5f47269ed5cea9f625f7ab-Paper.pdf — Data Programming: Creating Large Training Sets, Quickly
[18] https://arxiv.org/abs/0812.4952 — Importance Weighted Active Learning
[19] https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf — Metamorphic Testing: A New Approach for Generating Next Test Cases
[20] https://www.itl.nist.gov/div898/handbook/pri/section3/pri3331.htm — NIST/SEMATECH e-Handbook: Two-level full factorial designs
[21] https://www.vldb.org/pvldb/vol11/p269-ratner.pdf — Snorkel: Rapid Training Data Creation with Weak Supervision
[22] https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html — Hypothesis: Introduction to property-based testing
