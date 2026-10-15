# Wave 1 adversarial scientific review: incomplete-reference estimation

## Verdict and scope

**Family judgment: needs revision. One blocking finding; four open nonblocking findings and one nonblocking finding closed during integration.** The conditional mathematics is substantially sound. The blocker is an incorrect nonidentifiability claim that confuses production retrieval with evaluation sampling, not a defect in Horvitz–Thompson estimation.

- **Reviewer:** delegated adversarial scientific-review agent, in a fresh critique role. This is not a claim of a different model, independently recruited reviewer, or empirical reviewer independence.
- **Snapshot:** October 13, 2026, EDT; live clock checked. The repository has no resolvable HEAD, so the six content hashes below identify the reviewed snapshot.
- **Reviewed:** EVAL-11-001 through EVAL-11-005 and `deep-dives/incomplete-reference-estimation.md`; rubric and evidence policy also read.
- **Boundary:** no canonical-card edits, commits, ER implementation, original-source changes, or AU-v1/benchmark access. Pending acquisition/weak-supervision/experiment cards were not read or assessed. Global lint was deliberately not run during concurrent authoring; the preexisting AR-05 warning is outside this review.
- **Evidence:** checked local source-15 and source-17 text; checked the version-specific source-4 PDF for the metric/sampling distinction below. External literature is not evidence of locally measured ER outcomes.

| Reviewed path | SHA-256 |
|---|---|
| `evaluation/incomplete-reference-quality.md` | `da93821191b58cfdb22d23b6617bfa3c7f7dacb58ad10c87c0cab6b88dedaab2` |
| `deep-dives/incomplete-reference-estimation.md` | `983dcf52133a517fbc2a48dc090883d7a954f413e0019bea8e0a6c36c78e4418` |
| `evaluation/candidate-recall.md` | `2987eb88e2ebaadb898fe0e8b52bae8f8b5f39ebdf93cc8fdf4c0261e2f3d9bb` |
| `evaluation/pairwise-calibration.md` | `ee3790c4cc0a9a020f6b3175982b1057869f14ff07a2a9073661886944c85fd6` |
| `evaluation/entity-resolution-quality.md` | `30dd5b71457332d222de22b17171415b6997db2198d291a9f92b968521c41330` |
| `evaluation/retrieval-blind-spots.md` | `f0d2e7fc261063f7be12fa8b21f7388595c4c436d2f3bc2941baf52bbf41f494` |

Line references and exact quotations refer to this snapshot, not subsequent edits.

## Blocking finding

### B1 — Unknown production retrieval is not unknown evaluation inclusion

**Judgment:** needs revision. **Rubric:** mechanism, assumptions, evaluation estimand. **Blocks:** a Covered judgment for EVAL-11-004 in this snapshot.

**Exact passage:** `evaluation/retrieval-blind-spots.md:52`:

> If the production selection mechanism is unknown, or any stratum has $\pi_i=0$, $\rho$ is not identified there: report the unidentifiable region instead of estimating it.

**Counterexample, calculated independently:** Let the frozen universe be all unordered pairs of four records. True entities are `{1,2}` and `{3,4}`. An opaque production retriever emits `C={(1,2),(1,3)}`. We do not know its retrieval mechanism, but observe its final output. A census of the pairspace with correct adjudication gives `T_C=1`, `T_outside=1`, hence `rho=1/2` exactly. Alternatively, independent SRS of three of the six pairs has evaluation inclusion probability `1/2` for every pair. Exhaustive enumeration of its 20 possible samples gives mean HT totals `1` in each region. No production selection probabilities appear in either estimator.

**Why this matters:** For finite, frozen `C`, candidate membership is a fixed domain indicator. The review design supplies the randomness and inverse weights. Unknown production rules can obstruct *stage attribution*, replay, or future-version prediction; they do not by themselves make the missed-pair total unidentifiable. If only production-selected labels are available and excluded pairs have no evaluation support, the failure is instead the reference acquisition frame/design.

**Recommended fix:** Replace “production selection mechanism” with “evaluation/review inclusion mechanism,” and explicitly distinguish unknown review inclusion, absent frame support, unresolved outcomes, and uncertain stage attribution. Retain the warning about zero evaluation inclusion and the bounds/sensitivity route for unsupported regions. Add a sentence that independently sampling the full semantic universe can evaluate a frozen black-box retriever.

**Acceptance check:** A reader should correctly evaluate the frozen opaque-retriever counterexample while refusing population recall from candidate-only labels.

## Nonblocking findings

### N1 — Make the output-within-universe invariant explicit

**Judgment:** needs revision; high-priority semantic hardening, not a refutation of the formulas under their intended assumptions. **Rubric:** assumptions, composability, evaluation estimand.

**Exact passages:** `evaluation/incomplete-reference-quality.md:27`:

> For pair-output systems $A$ contains accepted links; for partition systems use all induced co-memberships, not just scored edges.

`deep-dives/incomplete-reference-estimation.md:7`:

> Fix semantic pairspace $U$, candidates $C$, asserted links $A$ and true statuses $y_i\in\{0,1\}$.

Neither sentence explicitly states `A subseteq U`. This becomes consequential when consuming the cross-file pairspace allowed at `evaluation/candidate-recall.md:29`.

**Counterexample:** Records `a,b` are in one file and `c` in another; all three are one entity, with within-file duplication allowed. Cross-file `U={(a,c),(b,c)}` has two true pairs. The correct partition has three unrestricted induced pairs. Mixing an HT true-accepted total over `U` with the unrestricted denominator `|A|=3` reports precision `2/3`, despite perfect truth. Restricting both numerator and output denominator to `U` gives precision `1`. Alternatively, define an all-pairs partition estimand and evaluate all three pairs. Neither may silently substitute for the other.

**Recommended fix:** Define `A_U=A intersect U`, require all finite-reference bounds and HT pair ratios to use that same scope, or state `A subseteq U` as a hard prerequisite. When the application treats assertions outside `U` as invalid, report those constraint violations separately rather than assigning unspecified identity labels. Clarify that complete-partition B-cubed over `V` is a different estimand and is not obtained by substituting a restricted pairspace into its formulas.

### N2 — Source 4's B-cubed aggregation is not the card's aggregation

**Judgment:** needs revision; source-to-estimator translation gap, not an incorrect record-average definition. **Rubric:** source scope, evaluation estimand.

**Exact passages:** `evaluation/entity-resolution-quality.md:40`:

> B-cubed averages per-record purity and completeness, not equal weight per entity.

At line 48:

> Under entity sampling, use estimators derived for that design and observed predicted-cluster intersections, rather than applying complete-partition formulas to a partial benchmark.

**Checked source distinction:** Source 4, v1 PDF, printed page 15, section 3.4.1, equation (15), explicitly uses “equal weight on each ground truth cluster.” Its Lemma 4 therefore targets entity-balanced B-cubed. Section 3.4.2 assumes sampled clusters with replacement; its ratio-estimator formulas cannot simply be imported as without-replacement inclusion estimators.[4]

**Counterexample, calculated:** A true entity of four records is completely split into singleton predictions; one additional true singleton is correctly retained. The card's record-average recall is `(4*(1/4)+1)/5=0.4`; equal-entity averaging is `((1/4)+1)/2=0.625`. Both are legitimate, different metrics.

**Recommended fix:** Add the source-variant warning next to the entity-sampling guidance. For a fully resolved true entity `e`, let `b_e` be its mean record-level purity or completeness. Under a without-replacement entity design, record-average B-cubed can use the HT total of `|G_e| b_e` divided by known `|V|`; an estimated size denominator instead produces a ratio estimator. Entity-balanced reporting uses contributions `b_e` and an entity-count denominator. With replacement requires the draw-based route already identified in L3. Label this translation Atlas reasoning, not source-4's literal estimator.

### N3 — Known contaminant records do not reveal all swallowed identities

**Judgment:** needs revision; clarify the evidence prerequisite for this diagnostic. **Rubric:** failure modes, evaluation estimand.

**Exact passage:** `evaluation/entity-resolution-quality.md:54`:

> Track largest erroneous merges, number of true entities swallowed, worst contamination, cross-source contradictions, and irreversible downstream exposure.

Line 48 correctly says the foreign records' own complete entities need not be known for the bounded impurity question. The diagnostics list should not imply that this same evidence identifies the number of distinct foreign identities.

**Counterexample:** Fully resolved `G_e={a}` is predicted with `b,c` in one cluster. Both `b,c` are known foreign records. They might be one foreign entity `{b,c}` or two entities `{b}` and `{c}`. The predicted cluster then swallows two versus three true entities, despite identical evidence about `G_e` and the output. Known contamination remains exactly two foreign records in both worlds.

**Recommended fix:** Separate supported foreign-record counts/false links from distinct-identity counts, which need additional foreign membership adjudication or explicitly bounded truth. For a partially resolved `G_e`, report supported negatives and unresolved boundary membership separately; do not relabel all outside records foreign. Preserve the existing sound permission to estimate bounded impurity around a *fully resolved* entity without fully resolving every contaminant's entity.

### N4 — Specify the discrete inversion and scope of the zero-event limit

**Judgment:** needs revision for reproducibility; the stated zero-event probability is supported mathematical reasoning. **Rubric:** falsifiability, evaluation estimand.

**Exact passage:** `deep-dives/incomplete-reference-estimation.md:88`:

> Invert this finite design to obtain a one-sided upper limit at a predeclared confidence level.

**Concrete ambiguity:** Give an integer convention, for example retaining `K` when `P(0|K)>=alpha`, with upper endpoint the largest retained `K`. For `N=100`, fixed `n=10`, `alpha=0.05`, the calculation gives `K_upper=24`: the zero probability is approximately `0.0551421` at 24 and `0.0478866` at 25. This is an illustrative calculation, not an ER estimate.

**Recommended fix:** State the endpoint convention, fixed-size sampling/stopping requirement, and that the bound covers the stratum total `K`, not automatically the pipeline's missed-pair ratio. Summing multiple stratum bounds or combining an upper missed total with an estimated positive denominator requires a jointly justified confidence region or simultaneous error allocation. Reusing a fixed-size limit after repeatedly looking and stopping at a favorable result is not licensed merely by predeclaring the confidence level.

This is not a criticism of zero-discovery samples themselves: `evaluation/retrieval-blind-spots.md:68` now explicitly and correctly says that zero discoveries with positive inclusion are possible.

### N5 — Citation rendering incomplete at initial snapshot; now closed

**Judgment:** supported after readback of concurrent integration; initially needed revision. This was a nonblocking integration/provenance issue, not a scientific falsification. **Rubric:** evidence discipline.

**Exact locations at initial snapshot:** `evaluation/incomplete-reference-quality.md:54,56,60` cite `[15]`, `[17]`, and `[4]`, but initially ended at line 80 without a Sources block. L3 cites `[15]` and `[17]` and initially ended at line 94 without one. `evaluation/retrieval-blind-spots.md:38,72` cite `[15]`, while its initial Sources block at lines 78–81 contained only `[2]` and `[4]`.

**Policy evidence:** `references/evidence-policy.md:15` requires source-bearing statements to cite checked IDs and each document's Sources block to be mechanically rendered from the retained ledger.

**Recommended fix:** Render the cited entries from `references/source-ledger.json` after integration, preserving IDs. Do not reset the ledger or treat successful rendering as substantive validation. The source-15 survey principles and source-17 conditional identity are supported within their bounded scopes; missing rendering is not grounds to claim the papers were unverified.

**Readback outcome:** Concurrent authoring added the required blocks/entry in all three documents. Their cited-ID sets and Sources entries now agree. Reconstruction against the initial SHA-256 hashes confirmed these changes were source rendering only, with scientific bodies unchanged. The reviewer did not make those canonical edits. N5 is closed; it is not an outstanding fix request.

## Acknowledged sound mechanisms and rejected false alarms

1. **Outer finite-reference bounds — supported.** L3 lines 32–47 correctly partition finite `U` into correct `P,N,W` and derive precision `[a/d,(a+u_a)/d]` and recall `[a/(p+u_o),(a+u_a)/(p+u_a)]` for positive denominators and scoped `A`. Recall increases with unknown asserted positives and decreases with unknown nonasserted positives because `a<=p`. Calling these *outer* bounds, allowing equivalence constraints to tighten them, and refusing separate system-specific optimistic truth assignments are important safeguards. Unattainable equivalence-relation corners do not invalidate outer bounds.
2. **HT totals, known denominators, and ratio bias — supported.** L3 lines 13–28 distinguish true totals, unbiased precision with a known output denominator, generally biased recall ratios, and with-replacement/adaptive designs. Source 15 supports inverse-inclusion weighting and separates nonresponse adjustment from design weighting; its adjustment arguments require assumptions about respondents and nonrespondents.[15] A bounded ratio estimate is not thereby unbiased, and possible HT precision above one is not itself evidence of a wrong total estimator.
3. **Exact covariance versus future-world dependence — supported.** L3 lines 65–78 give the correct indicator-covariance variance of the fixed-outcome HT total and warn that first-order inclusion alone need not identify an estimable variance. The same design/generalization distinction appears in all four preexisting evaluation cards. Shared records do not invalidate genuine finite-population pair SRS; conversely, that fact does not license an iid pair bootstrap for new-entity inference. Overlapping predicted-cluster contributions are not automatically independent primary units.
4. **SCAR identity without automatic propensity identification — supported.** L3 lines 51–59 correctly retain the conditional identity supported by source 17, section 2, Lemma 1, while refusing to infer unknown `c` merely by fitting a labeling model.[17] An independently calculated illustration has identical observed labeling probability `0.1` under `(c,eta)=(0.2,0.5)` and `(0.5,0.2)`. Even the paper's proposed mean-score estimate on labeled positives does not establish general identification from overlapping feature classes: observing a positive draw is not the same as `P(Y=1|X)=1`. Do not remove the Atlas's caution to conform to a stronger source assertion.
5. **Unknown outcomes and reference boundaries — supported.** EVAL-11-005 lines 50–68, EVAL-11-004 line 44, and EVAL-11-002 lines 29 and 57 refuse silent unknown-to-negative conversion, model self-validation, and nonresponse deletion. Complete `G_e` supports foreign-record impurity around its full predicted clusters; partial `G_e` does not. Completeness is a substantive truth assumption, not something sampling weights can supply.
6. **Candidate versus partition output — supported.** EVAL-11-001 line 40 and EVAL-11-004 line 56 correctly limit the multiplicative recall identity to accepted links inside candidates. Partition-induced co-memberships can recover an unscored pair and can introduce harmful bridges. Candidate-graph connectivity is described as a diagnostic, not attainable production improvement.
7. **Rare zeros and inference boundaries — supported.** L3's hypergeometric zero-event expression is correct for fixed-size SRS without replacement and complete correct observations. Its separate Bernoulli expression is not advertised as a correction for clustered or weighted samples. A zero point estimate or estimated variance does not certify no missed total. N4 concerns operationalizing the stated limit, not replacing it.
8. **No manufactured performance evidence — supported.** These six documents explicitly separate observed, design-estimated, assumption-dependent, and diagnostic-only results. No Bayesian posterior interval is presented as design coverage, and no inverse class-frequency weight is substituted for evaluation inclusion. Bayesian/model-based alternatives would need their own priors, observation model, and sensitivity treatment; their absence is not a defect in this bounded family.

## Rubric judgments

| Criterion | Judgment | Evidence and action |
|---|---|---|
| Mechanism | needs revision | B1 confuses the random evaluation inclusion with fixed production membership; other estimation mechanisms are supported above. |
| Assumptions | needs revision | B1; make the `A`/`U` invariant explicit in N1. Label correctness, frozen output, positive inclusion, and response limitations are otherwise explicit. |
| Failure modes | needs revision | N3's identity-count diagnostic needs additional evidence. Omission, anchoring, copied reference errors, overmerge bridges, and rare positives otherwise have plausible causal failures. |
| Alternatives | supported | EVAL-11-005's evidence-route table and unchanged-rule/challenger comparison; EVAL-11-001 exact versus multi-pass; EVAL-11-002 additive/FS/logistic; EVAL-11-003 architecture comparisons. No universal complex-method preference. |
| Falsifiability | supported | Frozen records/output, paired arms, predeclared benefit/harm limits, and inconclusive outcomes are specified. N4 is a reproducibility improvement to a limit, not empirical validation. |
| Source scope | needs revision | N2 needs explicit source-4 metric/design translation; bounded use of sources 15 and 17 is supported. |
| Evidence discipline | supported | N5 rendering was completed concurrently and checked; no local gains or interval-coverage evidence is invented. |
| Composability | supported | Acquisition, pair scoring, retrieval, partition quality, and policy diagnostics are kept separate; N1 hardens pairspace composition. |
| Economy | supported | EVAL-11-005 routes to the canonical metric owners; L3 supplies additional derivations rather than a second taxonomy. |
| Responsibility boundaries | supported | Evaluation does not silently authorize production changes or require clustering for assignment-only outputs. |
| Evaluation estimand | needs revision | B1 and N1–N4; finite truth, unresolved outcomes, weighting, dependence, and separate denominator requirements are otherwise sound. |
| Hypothesis-specific competing-explanation gate | not applicable | These are Evaluation Cards and an estimation deep dive, not new Hypothesis Cards. |
| Measured ER outcomes / benchmark improvement | not applicable | No local ER experiment or agent benchmark was run or claimed. |

## Verification and remaining work

- Independently executed the black-box retrieval counterexample, all 20 samples of its small pair-SRS design, the pairspace and metric-weighting examples, the foreign-identity ambiguity, the two SCAR models, and the discrete hypergeometric endpoint calculation. These are arithmetic/logic checks, not statistical validation or ER measurements.
- Read `validation/v1.2/algebra-sanity-checks.json`: it reports 500 recall-bound configurations, 516 HT mean/variance configurations, and 328 hypergeometric configurations, with `passed=true`. Those parent checks were not independently rerun. Neither their counts nor this review establish interval coverage, label reliability, or decision-quality improvement.
- Seven exact finding quotations were programmatically checked against the canonical text. Concurrent changes to three document hashes were detected and shown to be source rendering only by reconstructing the initial bytes and comparing SHA-256 hashes. The quoted scientific passages and their line locations remain applicable; N5 is closed.
- The web extraction backend could not extract URLs, and the host Python initially lacked PyMuPDF. Direct official-PDF download plus document extraction and an isolated `uv run --with pymupdf` check resolved source-4 verification. No source content was fabricated or added to the repository.
- The reviewer created only this report in the repository. Canonical documents require author fixes and integration QA. B1 must be corrected before upgrading coverage; N1–N3 should be addressed before a reader follows the general-purpose estimation route. No benchmark keys, scores, scenarios, or reports were accessed.

## Checked-source locator notes

- **[4]** Version-specific arXiv v1 PDF, dated April 9, 2024 on its title page; section 3.4.1 equation (15)/Lemma 4 and section 3.4.2. This review used the version-specific PDF for version fidelity; no claim about a newer version or a current HTML date was verified. The evidence-policy/ledger identity remains source 4, not a newly invented source ID.
- **[15]** Statistics Canada, *Survey Methods and Practices*, electronic edition copyright 2010, originally published October 2003; section 7.1, especially 7.1.3, and sampling/estimation principles. Local checked text: `/home/ghgin/.hermes/cache/scratch/atlas-v12-sources/15.txt`.
- **[17]** Elkan and Noto, *Learning Classifiers from Only Positive and Unlabeled Data*, KDD 2008; section 2, equations (1)–(2)/Lemma 1 and proposed propensity estimator discussion. Local checked text: `/home/ghgin/.hermes/cache/scratch/atlas-v12-sources/17.txt`.

## Sources

[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
[17] https://cseweb.ucsd.edu/~elkan/posonly.pdf — Learning Classifiers from Only Positive and Unlabeled Data
