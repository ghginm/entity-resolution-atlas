# Atlas v1.2.1 final consumer cleanup

## Result

The canonical documents and generators were repaired, not just the distribution.
Current entry: `dist/atlas-consumer-wave5/START_HERE.md`. Distribute only that consumer
directory or its matching archive. The consumer README contains the small copy-paste
instruction for Codex, Claude Code, Hermes and similar agents, including filesystem
access, explicit START_HERE entry, selective retrieval, stop rules and read-only scope.
Tools and harness-specific automatic discovery are not required.

All 26 originally marked document lines (29 occurrences) of “source repository only”
were eliminated from current consumer output by fixing canonical support sources.
Core scope/schema authoring operations and valuable review history belong in
MAINTAINERS.md; CATALOG generation no longer emits an unavailable rebuild command.
Excluded local links now fail the build even if a policy lists them as unbundled.
Regression tests cover source-byte preservation, forbidden raw infrastructure paths,
excluded-link rejection and the unchanged historical consumer-1 verification path.

There are still 57 canonical IDs/paths, five types, fourteen domains, six architectures
and L0–L3 navigation. Fifty-six cards are byte-identical to the pre-cleanup release.
The sole card correction is `evaluation/candidate-recall.md:54` (EVAL-11-001): a
smoke test exposed the obsolete claim that approximate retrieval was taxonomy-only.
It now links the existing method and states its bounded coverage; no formula,
frontmatter, ID, relation, scientific evidence or method scope was expanded.
All existing external URLs, Sources blocks and provenance URL/SHA256 pins are unchanged.

## Build and inventory

Two independent fresh builds have identical file manifests and archives. The release
is verified against canonical source and the explicit allowlist, with no support-page
rewriting and no broken supported internal Markdown paths/anchors. This verifies
supported Markdown grammar, not every possible HTML/CommonMark construct or live
availability of external research sites.

- Included: **130 files**, including **57 cards**, **23 navigation indexes**, **18 taxonomy
  files**, **12 guides**, **11 references/provenance files**, **2 deep dives**, and **7 root
  files** (including the generated README and manifest).
- Excluded: validation/benchmarks/keys/results/traces, tests/fixtures, maintainer reviews,
  handoffs/trackers, tools, templates, historical inputs, archives and local metadata.
- Exact included paths and exclusions: `consumer-cleanup-inventory.json`; output hashes:
  `dist/atlas-consumer-wave5/consumer-manifest.json`.
- Consumer agents receive usable knowledge, navigation and scientific provenance,
  **not Atlas development operations**.

Archive SHA256: `2030c296c1be3a246495c39729ab11b0aa7c9d433aaab5085d39c5d303f550f3`.
Manifest SHA256: `5462892dd6a250afda86df17b25f80159b782826c0a326a601a78472939b2485`.

The original `dist/atlas-consumer/` and archive were not changed. The pre-cleanup
Wave 5 archive is retained at `consumer-cleanup-wave5-before.tar.gz` beside this report
for reproduction of older release reports. It is historical evidence, not the current
consumer. The legacy verifier recognizes only the exact old generated catalog footer
for recorded consumer-1 snapshots; current consumer-2 freshness is not relaxed.

## Consumer-only cold starts

Separate fresh subagents used hypothetical project facts and selected consumer files,
not development or evaluator material. Tool-log read sequences were reconciled against
their recorded paths/ranges; selected IDs resolve to the final manifest. The no-labels
and graph returned texts are byte-identical to final-release text. The first blocking
attempt identified the stale sentence; a fresh blocking attempt then used the final
package. All attempts and complete recommendations are retained in
`consumer-cleanup-smoke.json`.

| Task | File reads | Returned UTF8 bytes | Whitespace words |
|---|---:|---:|---:|
| no-labels | 8 | 60,714 | 7,186 |
| graph | 8 | 58,320 | 6,948 |
| blocking | 10 | 63,439 | 7,594 |

- No labels: DEC-10-001 → probability-sampled review versus targeted diagnosis →
  EVAL-11-005; propose independent audit, not fabricated population accuracy.
- Graph overmerge: DEC-08-001 → closure baseline versus conditional constrained
  membership → EVAL-11-003; separate admission changes from fixed-edge membership.
- Blocking: DEC-05-001 / DEC-13-001 → exact/multi-pass baseline versus complete
  batching/tiling → EVAL-11-007 and EVAL-11-001; do not call candidate caps equivalent execution.

Each result identifies unknown project facts and a stop reason. No agent scanned
all cards or the entire corpus. These are observed navigation smoke tests, not
empirical improvement, independent scientific review or attested sandbox/model
isolation. Shared instructions exist; counts include returned file content, entry
and route, not inherited system context, tool wrappers, provider input or billed tokens.

## Tests and portability

| Suite | Successful | Expected failure | Unexpected failure |
|---|---:|---:|---:|
| tools | 62 | 0 | 0 |
| AU-v1 | 39 | 0 | 0 |
| AU-v2 package | 17 | 0 | 0 |
| offline integration | 65 | 0 | 0 |
| workflow | 12 | 0 | 0 |
| runtime boundary | 11 | 1 | 0 |
| **Unique test cases** | **206** | **1** | **0** |

The 62 tool tests also pass with TMPDIR unset; TMP and TEMP point at approved scratch
storage so the test respects this environment's storage policy. Before the fix, the
59-test suite with TMPDIR unset produced five KeyError errors. Tests now use standard
tempfile directory selection instead of indexing TMPDIR or hardcoding a user path.
No deadlines or protected assertions were changed. A first workflow run with the
default interpreter failed because tiktoken was absent; the existing QA environment
with the pinned tiktoken 0.12.0 passes all twelve tests. AU-v1 still emits ResourceWarning
messages for unclosed handles; its frozen implementation was not rewritten.

Lint: **0 errors, 34 unchanged advisory warnings**. No scientific content was deleted
to suppress them. AU-v1 freeze/corpus, externally anchored AU-v2 freeze and prepared
workflow verify successfully. All historical/frozen baseline bytes remain unchanged;
the only change among the 1,379 mechanically snapshotted paths is the explicitly
allowed live EVAL-11-001 prose correction, not a frozen benchmark edit.

## Privacy and publication boundary

The case-insensitive scan covers source, both dist packages, current/historical
archives and nested archive members. `consumer-cleanup-privacy.json` records pattern
rules, per-scope counts, location-only findings and coverage exceptions. A final scan
is run after creating this report. No organization, credential-shaped, user-path or
archive-ownership matches were found in dist. Compressed binary organization-pattern
hits elsewhere were false positives, not textual company references.

Source publication is a separate risk: historical/frozen evidence contains user-local
paths/environment fields and archive ownership metadata, and operational test logs
also retain their actual command/runtime provenance. Do not publish the full development
repository as a clean consumer. Preserve protected hashes; a separately authorized
sanitized publication/export is required if source publication is desired. No frozen
file was silently rewritten. Pattern scanning is not proof against unknown proprietary
names, every secret format, encryption/steganography or text requiring OCR; no claim
of credential authenticity or exhaustive secret absence is made.

## Git hygiene

.gitignore now covers Python environments, Python/test/lint/type caches, coverage,
local secrets, editor/OS metadata and bounded local scratch/log outputs. Only the
regenerable current Wave 5 directory/archive are ignored; dist/ and validation/ are
not blanket-ignored. Canonical sources, frozen inputs, older distribution dependencies
and the preserved pre-cleanup Wave 5 archive remain visible. There are zero tracked
files in this repository, so no git rm --cached was needed or performed. No commit,
push, remote change or broad destructive cleanup occurred.

## Reproduction commands

Use a Python 3.10+ QA interpreter with the repository's pinned requirements; `$PY`
below denotes that interpreter. Existing test logs record exact commands and outputs.
Fresh output names are required when source changes; do not overwrite frozen snapshots.

```sh
$PY tools/atlas_docs.py catalog
$PY -B -m unittest discover -s tools -p 'test_*.py'
env -u TMPDIR TMP="$TMPDIR" TEMP="$TMPDIR" "$PY" -B -m unittest discover -s tools -p 'test_*.py'
$PY tools/atlas_consumer.py build --output "$TMPDIR/atlas-fresh-a" --archive "$TMPDIR/atlas-fresh-a.tar.gz"
$PY tools/atlas_consumer.py build --output "$TMPDIR/atlas-fresh-b" --archive "$TMPDIR/atlas-fresh-b.tar.gz"
cmp "$TMPDIR/atlas-fresh-a.tar.gz" "$TMPDIR/atlas-fresh-b.tar.gz"
$PY tools/atlas_consumer.py verify --output dist/atlas-consumer-wave5
$PY tools/atlas_docs.py lint
$PY -B -m unittest discover -s validation/agent-utility/tests
$PY -B -m unittest discover -s validation/agent-utility-v2/tests
$PY -B -m unittest discover -s validation/agent-utility-integration/tests
$PY -B -m unittest discover -s validation/agent-workflow -p 'test_workflow.py'
$PY -B -m unittest discover -s validation/v1.2.1/wave-4 -p 'test_runtime_boundary.py'
$PY validation/agent-utility/harness.py verify-freeze
$PY validation/agent-utility-v2/verify.py --expected-manifest-sha256 22d2527c35b39e1f22a0ac5815c833924815b63cbd1704a958989f124c798f49
$PY validation/agent-workflow/workflow.py verify --prepared validation/agent-workflow/prepared/initial
```

## Remaining actionable issues

1. Full source-repository publication needs an explicitly authorized sanitized export;
   frozen local metadata must not be rewritten in place.
2. The existing buffered-output-after-deadline runtime defect remains an expected
   failure. AU-v2/workflow runs remain blocked on the previously documented trusted
   transport, model/settings/context and independent-evaluator eligibility gates.
   No new benchmark infrastructure, synthetic scores or model evaluations were added.

## Modified source paths

- `.gitignore`
- `AGENTS.md`
- `CATALOG.md`
- `MAINTAINERS.md`
- `README.md`
- `SCHEMA.md`
- `SCOPE.md`
- `evaluation/candidate-recall.md`
- `guides/compare-and-experiment.md`
- `guides/project-atlas-integration.md`
- `guides/project-intake.md`
- `references/evidence-policy.md`
- `references/retrieval-provenance.json`
- `references/retrieval-status.json`
- `references/wave-1-evidence-notes.md`
- `references/wave-2-evidence-notes.md`
- `references/wave-3-evidence-notes.md`
- `references/wave-4-evidence-notes.md`
- `taxonomy/architecture-dimensions.md`
- `taxonomy/domains/01-problem-identity.md`
- `taxonomy/domains/02-architecture-orchestration.md`
- `taxonomy/domains/03-data-integration.md`
- `taxonomy/domains/04-normalization-enrichment.md`
- `taxonomy/domains/05-candidate-retrieval.md`
- `taxonomy/domains/06-comparison-evidence.md`
- `taxonomy/domains/07-matching-scoring.md`
- `taxonomy/domains/09-master-maintenance.md`
- `taxonomy/domains/10-ground-truth.md`
- `taxonomy/domains/11-evaluation-diagnostics.md`
- `taxonomy/domains/12-experimentation.md`
- `taxonomy/domains/14-governance-monitoring.md`
- `taxonomy/overview.md`
- `tools/README.md`
- `tools/atlas_consumer.py`
- `tools/atlas_docs.py`
- `tools/consumer-policy.json`
- `tools/test_atlas_consumer.py`
- `tools/test_atlas_docs.py`
- `tools/test_atlas_routes.py`

Evidence beside this report: `consumer-cleanup-build.json`, `consumer-cleanup-inventory.json`,
`consumer-cleanup-tests.json`, `consumer-cleanup-integrity.json`, `consumer-cleanup-provenance.json`,
`consumer-cleanup-privacy.json`, `consumer-cleanup-smoke.json`, and the historical pre-cleanup archive.
