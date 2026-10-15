# Pilot quality review

## Review scope
This review separates documentation integrity, scientific/experimental content and conceptual usefulness. Passing tooling does not prove ER performance. No matching implementation, data processing, training or empirical ER benchmark was produced.

## Conceptual and research checks
- Distinguish likelihood-ratio foundations from the conditional-independence additive simplification; avoid automatically calibrated expert scores or probabilities without compatible priors/populations.
- Distinguish candidate conditioning, label sampling, within-pair feature dependence, cross-pair record dependence and global constraints.
- Review missing/invalid/contradiction evidence, identity namespace/time semantics, double counting and shared-attribute collisions.
- Keep score estimation, risk/abstention actions, membership consistency and consumer master representation separate.
- Check candidate union monotonicity conditions, clipping/skew costs, early-exit errors, correlated ensemble signals, unmatched assignment options, feedback and incremental dependency closure.
- Verify hypotheses are untested, controlled and falsifiable, with application-specific effect thresholds/guardrails selected before testing; low power remains inconclusive.
- Match metrics to candidate, pairwise, entity and end-to-end outputs; incomplete truth does not authorize unknown-negative labels, naive partial-cluster metrics or population-wide oracle ceilings.

## Tooling scope
The [documentation checker](../tools/README.md) checks YAML, ID/type/domain/tag validity, typed relationships, paths/anchors, approved citations, immutable source hashes, pilot counts and catalog freshness. Its unit tests exercise both success and deliberate-invalid cases. External-source claim support additionally requires source-aware review, not just valid citation numbers.

## Scenario assessment
The [three conceptual stress tests](scenario-stress-tests.md) compare baseline and alternative compositions under clean structured, noisy multilingual and large heterogeneous assumptions. They explicitly expose gaps and do not supply hypothetical performance numbers. Every scenario offers layered evaluation and conditional research opportunities rather than one universal architecture.

## Remaining limitations
Pilot depth concentrates on candidate generation, comparison states and interpretable soft scoring. Language-specific normalization, approximate/learned retrieval, label acquisition, global-resolution algorithms, master maintenance, distributed/streaming execution and privacy remain taxonomy/architecture guidance or planned work. Architecture contracts are not implementation or security guarantees. Numeric experiment criteria require a real application; no local ER results validate them. One collective reference has publisher-abstract support only, and failed exploratory URLs are excluded.

## Executed verification results
- **Nineteen documentation-tool unit tests passed**, including intentional invalid metadata, links, input modification, citation failures and reciprocal relations.
- Full repository lint returned **zero errors and zero warnings**. Verified counts: fourteen domains, six architectures, three decisions, seven solutions, two hypotheses, three evaluations and five templates.
- All twenty-one object IDs and typed targets resolve. The catalog matches current frontmatter, and relative Markdown paths/heading anchors resolve.
- Citation rendering and ledger verification passed for **twenty-three documents**: all cards, the deep dive and bibliography. Shared-ledger unused-source notices are expected per document, not missing-source failures; failed exploratory references are forbidden by the repository checker.
- All six historical input hashes and their original inventory match. No source bytes were altered.
- Every scenario has two explicit alternative configurations, at least two linked architecture patterns, all three evaluation routes and both hypothesis routes. These are documented conceptual checks, not measured performance.
- Discovery summaries span 64–76 words. Card bodies meet the standard depth range. Inline/display math delimiters are paired in the five equation-bearing documents.

Machine-readable scope and results: [validation-results.json](validation-results.json). Commands and checker limits: [tools](../tools/README.md).

## Integration problems identified and corrected
1. Removed four redundant reciprocal metadata pairs across hypotheses/evaluations, retaining inferred reverse navigation; added a regression test.
2. Fixed the checker to distinguish numeric domain-navigation labels from bibliography citations; added two regression tests rather than hiding valid domain links.
3. Added direct architecture/evaluation/hypothesis retrieval links to scenarios B/C so each scenario is usable independently.
4. Clarified statistical probability resolution versus entity-membership resolution, and strictly monotone recalibration versus maps that introduce score ties.
5. Standardized math to GitHub-flavored `$`/`$$` delimiters and refreshed source blocks from verified ledger metadata.
6. Excluded unverified/failed exploratory URLs and removed unverified bibliographic metadata; preserved the explicit publisher-abstract-only limitation.

## Initial acceptance gate
The foundation and bounded pilot meet the requested structural and conceptual gate: coherent fourteen-domain ownership; independent architecture axes; six composable archetypes; five templates; fifteen additional meaningful pilot cards; mechanisms/prerequisites/failures; falsifiable hypotheses; supported or qualified claims; valid cross-references; selective catalog and agent workflow; three conceptual scenario tests; a grouped expansion plan; and unchanged historical inputs.

This gate is not a claim of exhaustive ER coverage, empirical method validation or universal architecture superiority. Further expansion requires user review of [priorities and feedback questions](expansion-plan.md).

## v1.1 iteration review

### Scope and baseline preservation
Baseline re-verified before edits: 21 objects, 19 tooling tests, zero-error lint; the whole v1 tree was snapshotted byte-for-byte because the repository has no Git commit. A recursive diff after the iteration confirms all 21 original cards (including Fellegi–Sunter, thresholds/abstention and selection/calibration materials) are byte-identical, all IDs/paths intact, `dev_docs/` unchanged, and only navigation/schema/tools/references plus ten new cards and guides differ.

### Substantive content review of the ten new cards
Reviewed against the [content rubric](content-review-rubric.md) by the integrating agent (not by the card-authoring processes). Findings accepted as supported: mechanisms stated with assumptions (equivalence algebra and the nontransitive shared-telephone counterexample in DEC-01-001; valid/observation/ingestion time separation in SOL-01-001; the partial-matching formulation, seven-enumerated feasible matchings and greedy-9-vs-joint-16 counterexample independently re-derived in SOL-08-002; the O(|V|+|E|) traversal scope and 20×30→600 false-co-membership arithmetic re-derived in SOL-08-003; cluster-level admissibility, infeasibility diagnosis and greedy-order sensitivity in SOL-08-004; representation-versus-ID-lifecycle orthogonality and split ambiguity in DEC-09-001; copy-de-inflation before corroboration and bundle coherence in SOL-09-001; PPS entity inclusion math and length-bias warning in SOL-10-001; ratio-estimator and nonidentifiability discipline in EVAL-11-004). Source scopes match the retrieved PDFs for ledger IDs 11–14; every derived example is labeled illustrative, and Atlas synthesis is separated from cited claims in each card. No card asserts a measured ER improvement. Needs-revision items: none blocking; identifier-namespace and relational-inference depth remain explicitly Partial in the [coverage matrix](decision-coverage-matrix.md).

### Composability and relation semantics
Interaction knowledge is prose (prerequisite/compatibility/interaction risk/conditional exclusion), matching the revised schema: e.g., closure is conditionally excluded for nontransitive related-to targets or mandatory one-to-one contracts, while probabilistic scoring itself is *not* declared incompatible with clustering; one principled `requires` edge (SOL-08-004→DEC-01-001) exists and cycles remain an error. Tags never imply compatibility, and the L1 generator explicitly refuses to invent alternatives.

### Retrieval scalability
The old catalog repeated 50–100-word summaries for every object; the generated L0 now carries one ≤180-character applicability statement per card with a canonical path — 17.6 KB even after a 48% object increase (the v1 hand-written catalog was 22.2 KB for 21 objects) — while fourteen generated L1 files hold the full summaries, both-direction `alternative_to` views, typed relations and in-card section anchors, opened only for relevant domains. Tag routes derive from metadata instead of the previous hardcoded table.

### Structural verification after v1.1
45 documentation-tool unit tests and 26 harness + 13 adapter protocol tests pass; lint reports zero errors and one informational keyword hint (AR-05 “failure/limitations” wording; the card’s failure prose exists — the hint is heuristic, per the separation rule). The relation graph is a single connected component with no orphans. Pilot manifest fingerprint unchanged and still a subset of the current 31-card inventory manifest. Citation/ledger verification passes for all documents; only ledger-cleared sources 1–5, 7, 9–14 are cited.

After scoring and report updates, both suites were rerun (45 + 39 tests passed), L0/L1 rebuilt, all three corpus manifests and all 24 frozen paths verified, and historical/card hashes compared again. Machine-readable final checks: [v1.1 validation results](validation-results-v1.1.json); [validation-results.json](validation-results.json) remains the historical v1 report. Benchmark tests emitted nonblocking unclosed-file ResourceWarnings. The summary command independently revalidates all 33 scores, including exact quotes, hashes and caps.

### Benchmark execution (separate from content review)
The frozen AU-v1 package ran 32 genuine paired fresh-model attempts (google/gemini-2.5-flash, zero tool schemas and brokered selective retrieval): 25 completed, seven failed and retained. All eight no-Atlas runs also completed. **All 33 completed responses have validated blinded scores**, produced by fresh `openai-codex` provider-default evaluator processes after the initial Sonnet HTTP 402/rate-limit blockers. The exact evaluator model/version was not pinned or wire-attested; independent/blinded roles are declarations, not machine-proven identity. First-completed selection (cohort 01 preferred) yields 16 paired responses; remaining samples are retained, and AU-05 crosses cohorts. Per-run attestations disclose that temperature/seed/output-cap were declared but not wire-attestable. Full findings and dimension vectors: [measured comparison](../validation/agent-utility/results/COMPARISON-2026-10-13.md); provenance and failure history: [execution status](../validation/agent-utility/results/EXECUTION-STATUS-2026-10-13.json).

Measured judgments are mixed. v1.1 improved understanding on four scenarios and regressed on one; retrieval relevance tied on all eight. AU-02 selected-only recall certification triggered critical failures in v1 cohort 01 and no-Atlas, but not v1.1; the v1.1 experiment still omitted weighting/denominator/uncertainty details. AU-06 improved separation of identity and master construction. AU-03 regressed despite relevant retrieval: v1.1 asserted entity discontinuity from a license change and confused assignment optimality with identity truth. No v1.1 response triggered a rubric critical failure across either cohort, but important dimension-level omissions remain. These are exploratory ordinal evaluator judgments, not statistical significance, universal corpus superiority or empirical ER performance. The frozen keys and corpus snapshots were not tuned after scoring.

### v1.1 remaining limitations
Coverage additions concentrate on identity, resolution, master and reference/evaluation decisions; retrieval families, advanced scorers, physical execution and privacy stay deferred. The benchmark has one tested model, uncontrolled effective sampling, seven transport failures, one unpinned evaluator per response, no human adjudication and a later, noninterleaved no-Atlas arm. It measures exploratory agent-response judgments, not ER quality or universal method superiority. Coverage statuses remain review judgments. The Atlas still contains no ER implementation and no empirical ER result.
