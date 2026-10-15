# v1.2.1 Wave 5 — scientific review and final handoff

## Status and limits

**Feasible Wave 5 documentation, packaging and offline validation are complete.** One demonstrated scientific error was corrected in the existing canonical owner; no new card, taxonomy or ER implementation was introduced. Real AU-v2/workflow execution remains blocked, and substantial real-agent efficiency or recommendation-quality improvement is **not established**.

This is integrating-author closure of bounded reviews, including separately delegated review roles. Reviewer model identities and post-remediation independence are not attested; this is not independent scientific certification. No benchmark cases, keys or model results were consumed to author this correction. Existing review reports and pre-correction evidence remain historical, not silently updated to describe the corrected state.

## Scientific finding and correction

`solutions/decision-resolution/constrained-clustering.md:46` previously offered disjoint validity periods plus single occupancy as an impossibility example. One enduring person occupying address A and then address B satisfies those premises without being two people. That implication is insufficient and risks false fragmentation.

The correction requires **known overlapping validity**, genuinely mutually exclusive comparable states, a trusted single-occupancy invariant and the chosen identity scope. It explicitly rejects disjointness alone, unknown validity and legitimate concurrent states as sufficient hard-veto evidence. This aligns with the existing temporal-identity owner rather than inventing a new identity policy.

Two related clarifications in the same card:

- Line 28 distinguishes soft signed-evidence objectives from mandatory hard admissibility; a correlation-clustering objective need not satisfy every signed label.
- Line 36 requires must-link closure independently of candidate availability/utility and validation of initial groups before optional merges. Inconsistent mandatory groups require diagnosis, not silently discarding must-links.

Stable ID, path, metadata, relations, source IDs and all other canonical card bytes are preserved. Catalog/domain/task generation was rerun and remains byte-identical because no discovery metadata changed. These are bounded semantic corrections, not measured ER gains.

### Review evidence

| Family | Bounded review | Executed evidence / disposition |
|---|---|---|
| Incomplete truth, sampling, PU, selection, calibration, source conditioning | [Review](review-incomplete-calibration.md) | 14 mathematical check groups, including 224 finite-bound cases / 3,150 assignments; no demonstrated canonical error |
| Graph constraints, overmerge, temporal/incremental identity | [Review](review-graph-lifecycle.md) | 16 finite check records; one demonstrated temporal implication error corrected; two clarifications integrated |
| Experiment design, artifacts and stage interactions | [Existing review](review-experiments.md) | Six finite counterexamples rerun; inherited reference algebra rerun |
| Advisory metadata/length hints | [Disposition](review-advisories.md) | Four keyword hints manually inspected; 30 length advisories retained without mechanical truncation |

[Parent scientific rerun](scientific-rerun.json) confirms both delegated scripts actually executed and reproduced their saved JSON exactly. Graph checks ran from a scratch copy to avoid overwriting their original output. [Experiment output](final-experiment-boundaries.json) and [reference algebra](final-reference-algebra.json) retain the other actual calculations. These scripts use constructed mathematics, not project data, model training or measured ER outcomes. Passing them does not certify every theorem, every citation or real deployment correctness.

Sources were section-scoped, reusing existing ledger identities without resetting or editing the ledger. Primary retrieval methods and limits are stated in each review. The incomplete-reference reviewer lacked `web.run` and instead inspected browser/full-PDF content; this is explicitly not claimed as successful execution of that exact transport. The parent NIST recheck also needed direct HTTPS after the configured extract backend rejected URL extraction: [receipt](advisory-source-recheck.json). No search snippet was substituted for the named primary passages. Survey, PU and calibration proofs were not exhaustively audited.

## Corrected consumer release — old evaluation input preserved

Use **`dist/atlas-consumer-wave5/START_HERE.md`**, or unpack **`dist/atlas-consumer-wave5.tar.gz`**.

[Actual build](corrected-consumer-build.json): 57 cards, 130 files, **1,020,240 directory bytes** including manifest. Canonical cards retain the exact current source bytes. Source-bound validation checks policy inventory, IDs, relations, domain/task navigation, relative links/anchors, citations, transformations and forbidden evaluator/development content.

- Consumer manifest SHA-256: `be999130f3444e9a539d458287e34f7087440bd55c9cb9dc0cd3ad31b96ac592`
- Archive SHA-256: `c0db36fe4473cabc89c184e28cff552979cbf4ad2c2e1f553cfa1c6394fd7f0c`
- [Fresh equivalent build](corrected-reproducibility.json) produced the identical archive hash from a different output location. Temporary comparison output was removed.

`dist/atlas-consumer/` and its archive are **unchanged**. They are pinned Wave 3 evaluation inputs, not the corrected live release. They remain internally valid, but source-bound verification against today's corrected card should no longer pass. This is expected historical divergence, not permission to rebuild them, alter prepared cohorts, re-freeze or reinterpret future scores as applying to the corrected release. The final verifier records both old-package internal integrity and new-package source-bound integrity. Earlier pre-correction `final-*` records correctly describe the state before this finding; use the post-correction records for current status.

## Actual post-correction validation

[Commands, log paths and hashes](post-correction-test-summary.json):

| Suite | Result |
|---|---|
| Documentation/navigation/package/retrieval tooling | 59 pass |
| AU-v1 infrastructure | 39 pass |
| AU-v2 package | 17 pass |
| Integration/scoring | 65 pass |
| Workflow infrastructure | 12 pass |
| Wave 4 synthetic runtime boundary | 11 pass, **1 expected failure** |

Total: **203 passing tests and one expected failure**, not 204 passes. The expected failure is the unchanged legacy reader returning a complete buffered line before checking an expired deadline. It remains an unresolved runtime requirement; test exit zero is not pilot eligibility.

[Final lint](release-lint.json): **0 errors, 34 advisory warnings**. Manifest/card counts, exact generated navigation freshness, citation/Source blocks and six immutable historical inputs pass. Length/keyword warnings are not scientific verdicts; no validator, assertion or protected timeout was weakened. The four inspected keyword hints concern substantive content that is already present.

[Final verification](release-verification.json) records the externally anchored AU-v2 freeze, all three selected integration snapshots, frozen workflow/preparation, preserved old consumer internally and corrected consumer against live source. [Protected integrity](protected-integrity.json) reconciles pre-wave hashes/inventories and permitted source changes. No benchmark/frozen/runtime dependency, historical result, original pilot mapping or historical input changed.

The earlier `post-correction-verification.json` retains an initial lint failure while this report's linked output files were not yet created, plus citation `--strict` failures caused solely by unrelated unused entries in the shared 45-source ledger. Once the linked artifacts existed, lint passed. [Per-document shared-ledger verification](shared-ledger-citation-verification.json) passed without changing citations, the ledger or validator rules; unused sources are appropriate in a shared corpus ledger. These failed preliminary checks are preserved rather than relabeled as passes.

### AU-v1 intermittent timeout

The original 0.5-second process test passed in both suite runs. The existing diagnostic was rerun without changing it: [ten actual trials](final-subprocess-timing.json), five at 0.5 seconds and five at the 2-second diagnostic comparator, all completed. Maximum elapsed time was 0.031190 seconds including setup overhead. This does **not** establish the cause of the earlier timeout or exclude scheduler-dependent flakiness. No deadline/assertion was changed; 2 seconds remains a diagnostic comparator only. Existing unclosed-pipe ResourceWarnings remain visible in the AU-v1 logs. The distinct buffered-deadline defect is not offered as the cause of that historical timeout.

## Retrieval cost: modest offline saving, not the requested empirical win

[Corrected eight-task replay](corrected-retrieval-cost.json) uses exact `cl100k_base` retrieved-text tokens and the same declared L2 seed sets as the archived baseline. It does not measure autonomous choices, provider input, conversation replay, latency, money or quality.

| Task | Before tokens | Corrected after tokens | Reduction |
|---|---:|---:|---:|
| Scoring | 12,057 | 11,576 | 3.99% |
| Graph overmerge | 10,593 | 10,229 | 3.44% |
| Blocking | 11,013 | 10,569 | 4.03% |
| No reliable labels | 10,535 | 10,090 | 4.22% |
| Rule refactor | 12,022 | 11,539 | 4.02% |
| Experiments | 10,760 | 10,288 | 4.39% |
| New source | 9,681 | 9,192 | 5.05% |
| Incremental identity | 10,780 | 10,319 | 4.28% |

The graph path is slightly longer after the scientific fix; necessary qualifications were not removed to manufacture a larger saving. These reductions remain **modest** versus already-selective v1.2 consumption. Available corpus/package size is not loaded context. Discovery can exceed the illustrative 500–1,000-token soft target, and the split entry adds a read. A substantial real-agent benefit with preserved quality remains an unmet empirical criterion, not a claimed result.

## Delivery map and remaining gates

| Deliverable | Current artifact / boundary |
|---|---|
| Updated repository and compact entry | Root source, `START_HERE.md`, minimal `AGENTS.md`, separate `MAINTAINERS.md` |
| Selective navigation | Generated `indexes/tasks/`, domain indexes, catalog and stopping rules |
| Reproducible consumer builder / verified distribution | `tools/atlas_consumer.py`, explicit policy, corrected Wave 5 package and equivalent archive check |
| Retrieval audit | [Corrected replay](corrected-retrieval-cost.json); [original method/report](../wave-1-2-report.md) retained |
| Workflow evaluation | `validation/agent-workflow/`; frozen four-arm protocol and offline infrastructure; 32 planned cells unexecuted |
| AU-v2 readiness | [Wave 4 boundary](../wave-4/README.md); 24 planned cells unexecuted |
| Targeted scientific review/correction | The three family reviews and current canonical SOL-08-004 |
| Tests, manifests and handoff | Post-correction logs, lint, package manifest, protected integrity and this report |

Execution remains blocked on a compatible trusted process/transport seam, safely versioned frozen dependencies, actual backend model/version/effective settings, fresh broker-only contexts, full lifecycle/budget evidence and independently established evaluator identity/conflict status. The frozen workflow D arm still contains the pre-correction card; the frozen C-versus-D comparison also confounds guides/context/packaging, not a pure routing ablation. Do not modify either protocol or current prepared snapshots to incorporate this correction. Any evaluation of the corrected release needs a separately authorized, prospectively frozen version/design.

### Exact safe continuation commands

From the repository root, with the already exercised QA interpreter:

```sh
PY=/home/ghgin/.hermes/cache/scratch/atlas-v11-qa/bin/python
$PY -B tools/atlas_docs.py lint
$PY -B tools/atlas_consumer.py verify --output dist/atlas-consumer-wave5
$PY -B validation/agent-workflow/workflow.py verify --prepared validation/agent-workflow/prepared/initial
$PY -B validation/agent-utility-v2/verify.py --expected-manifest-sha256 22d2527c35b39e1f22a0ac5815c833924815b63cbd1704a958989f124c798f49
```

The existing Wave 5 build command is idempotent while its source is unchanged; later source edits need a fresh package path. Read [Wave 4 gates](../wave-4/README.md#pilot-gates-and-decision) before any runtime work. No eligible real model-run command is available. No credentials, production state, Git history, commit or remote branch was changed.
