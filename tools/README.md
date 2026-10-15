# Documentation validation tools

These optional tools lint Markdown metadata/navigation and regenerate L0/L1 retrieval indexes. They do **not** implement Entity Resolution, execute an ER experiment, process entity data or validate algorithm performance.

## Requirements and commands
Python 3.10+ and the pinned YAML parser in `requirements.txt`. Use an isolated environment; no global package install is necessary.

```sh
python3 -m venv .venv-qa
.venv-qa/bin/python -m pip install -r tools/requirements.txt
.venv-qa/bin/python -m unittest discover -s tools -p 'test_*.py'
.venv-qa/bin/python tools/atlas_docs.py catalog
.venv-qa/bin/python tools/atlas_docs.py lint
```

The `catalog` action generates `CATALOG.md`, `indexes/domains/01.md` through `14.md`, and the bounded `indexes/tasks/` views when `guides/task-routes.json` is present. It does not edit cards, templates, manifests or immutable inputs. For the exercised build, the QA environment lives in the agent scratch cache rather than inside the repository. QA fixtures use the configured scratch directory, never real ER datasets.

## Generated retrieval layers
- **L0 catalog:** one row per ID with title, type, primary domain, concise applicability and canonical path. Applicability is the summary's first sentence, capped at 180 characters at a word boundary. Optional frontmatter `applicability` overrides this derivation and must be a nonempty, single-line string of at most 180 characters. The summary remains the canonical L1 description; neither field is evidence of applicability.
- **Tag routes:** generated from current card tags, never a hardcoded method/problem table. L0 routes to domain-specific tag anchors; L1 lists the matching card links. L0 tag navigation scales with domains, not repeated lists of every matching ID.
- **Question-led entry:** when the supporting `guides/agent-task-patterns.md` exists, L0 links to its relevant task sections; fixtures without it receive no broken prospective link. Canonical card/domain/tag navigation remains generated, not a second routing ontology.
- **Bounded task views:** `atlas_routes.py` renders the selected section of the existing task-pattern guide plus seed IDs from `guides/task-routes.json`. Canonical titles, paths and L1 anchors are derived, not manually copied. The seed set is not an exhaustive prerequisite closure or an accuracy judgment. The Markdown-only consumer begins at [START_HERE](../START_HERE.md); no lookup runtime, embeddings or hosted service is required.
- **L1 domain indexes:** retain each card's discovery summary (target 50–100 words), tags, canonical link and typed relation links. Declared alternatives are inferred in both directions from the one stored `alternative_to` edge. Differences and composition conditions link to relevant existing card sections; no generator invents a comparison, compatibility rule or missing alternative.
- Domains without cards explicitly report taxonomy-only coverage. Ordering is stable by domain, card ID, tag and relation; generation has no timestamps or external requests.

`index_texts(root)` returns the expected output mapping without writes; `generate_indexes(root)` writes it. `catalog_text(root)` remains available for existing callers and returns the L0 text. Lint checks every generated output for exact freshness and flags unexpected domain-index files. If a registry domain is deliberately removed, remove its obsolete generated index explicitly; the generator does not silently delete files.

## Inventory contract
Default lint reads the current approved inventory from `references/atlas-manifest.json`:

```json
{
  "version": "1.1",
  "counts": {"decision": 6, "solution": 13, "architecture": 6, "hypothesis": 2, "evaluation": 4},
  "cards": {"<stable ID>": "<canonical repository-relative path>"}
}
```

The example counts describe the approved 31-card expansion; the real `cards` mapping must enumerate every card, not contain placeholders. All five counts are mandatory, nonnegative integers and checked against the actual corpus. IDs and paths must agree exactly. The six architecture IDs remain AR-01 through AR-06.

`references/pilot-manifest.json` remains the historical baseline, not the current total. Default lint verifies its original mapping fingerprint; every original ID/path must still be a subset of the expanded corpus. Never rewrite that manifest to fit the new counts. Lint only reads both manifests.

## What is checked
- Required YAML fields and field shapes, duplicate keys and IDs, quoted domains, ID/type/domain consistency, approved tags, maturity/evidence classes. Malformed YAML or metadata yields a path-bearing diagnostic instead of a traceback; generation validates metadata before writing.
- Duplicate applicability tags are errors. Identical whitespace/case-normalized discovery summaries produce one grouped advisory warning with affected IDs, not a semantic duplication verdict. Distinct mechanisms can share a short description; maintainers decide whether to deepen an owner, improve routing or justify overlap. Tests exercise both rejection and warning-only behavior.
- Nonempty required sections derived from all five templates, with structural aliases accepting the original combined headings. If templates are absent in a minimal fixture, the built-in canonical section list applies. A section can satisfy several template concepts when it is an accepted combined heading; this does not prove semantic completeness.
- Typed relationship targets and direction for addresses/used_by/evaluated_by/tests; self-links, duplicate targets, redundant reciprocal metadata and underconnected cards. A documented minimum-edge exception uses a nonempty `Relation exception: <reason>` line in the card body, not a new structured relation model.
- Every non-Evaluation Card must explicitly declare a nonempty `evaluated_by` route; arbitrary connectivity or a `requires` edge to an evaluation does not substitute for it. Existing direction/target checks also apply. This gate checks navigation, not whether the linked evaluation measures the right estimand; that remains a content-rubric question. The Wave 1 regression test was observed failing before the gate was added, then passing with the complete suite.
- Orphans with no resolved typed connections are errors; disconnected components are warnings with component IDs. Directed `requires` cycles are errors. Other relation cycles are not treated as incompatibility, and tags never imply compatibility.
- Ordinary relative Markdown paths and heading anchors; prose IDs; repository-contained navigation.
- Frozen, allowlisted retrieval snapshots under `validation/agent-utility/corpora/` are not part of the live documentation graph: their historical links can refer to deliberately unbundled files. Only those snapshot copies are excluded; live harness protocol/documentation links are still checked, and the harness owns its snapshot integrity checks.
- Citation IDs against the ledger and verified retrieval status; citation/Source-block agreement.
- Original `dev_docs/` byte hashes and exact input inventory **when that optional,
  unpublished directory is present**. A fresh clone omits it: lint emits an explicit
  warning and reports `immutable_inputs: 0`. If present, even a partial/empty
  directory must match the entire original baseline; changed, missing or extra
  inputs fail. The tracked hash manifest itself remains required in all cases.
- Expanded shape: fourteen domains, exactly the six original architectures, five templates, current manifest counts/paths and historical pilot subset preservation.
- Exact freshness of L0 and every L1 index, including tag and relation-derived navigation.
- Body/discovery-summary lengths and type-specific content keyword hints are **warnings only**, not semantic completeness or scientific validity proofs. Body targets are 400–900 words excluding Sources; discovery summaries target 50–100. Keywords are checked outside headings/code fences.

`lint --no-pilot` is for minimal legacy fixtures or deliberately inventory-independent checks. It skips only the expanded manifest/exact repository-shape gate, **not** metadata/schema, required sections, graph, citation, applicable historical-input or generated-index freshness checks. If a historical manifest is present, its original cards/paths still must exist. Fixtures without a domain registry infer their represented domains and need no added template/manifest/registry fixture files; they must still generate and maintain fresh L0/L1 output. Approved expansions should update `atlas-manifest.json`, not use this flag to hide missing cards.

## What is not proved
A passing lint cannot establish scientific truth, adequate citations for every claim, meaningful mechanisms, valid sampling assumptions, experiment power, composability or useful recommendations. It does not fetch external URLs and cannot prove them permanently available. A human/agent must review conceptual requirements, source scope and the [scenario routes](../guides/scenario-stress-tests.md). [Quality review](../guides/quality-review.md) records that separate assessment.

Citation rendering uses the source-ledger helper available to the initial agent; the resulting Markdown Sources blocks and JSON ledger are portable. A future editor can preserve the same ledger numbering and generate equivalent blocks without requiring Hermes.

## Optional historical evaluation tests

The README's build, verification, lint and `tools/test_*.py` checks need only
`requirements.txt`. They do not need an agent runtime, provider credentials or
tokenizer assets. Historical evaluation infrastructure is separate from consumer
acceptance; its tests are not measurements of ER accuracy or agent utility.

For the broader offline suites, use a POSIX environment (verified with Python 3.12),
set a writable `TMPDIR` for the process-boundary fixtures, and install the existing
optional tokenizer requirements:

```sh
.venv-qa/bin/python -m pip install -r tools/retrieval-requirements.txt
mkdir -p .scratch
export TMPDIR="$PWD/.scratch"
.venv-qa/bin/python -B -m unittest discover -s validation/agent-utility/tests -v
.venv-qa/bin/python -B -m unittest discover -s validation/agent-utility-v2/tests -v
.venv-qa/bin/python -B -m unittest discover -s validation/agent-utility-integration/tests -v
.venv-qa/bin/python -B -m unittest discover -s validation/agent-workflow -p 'test_workflow.py' -v
.venv-qa/bin/python -B -m unittest discover -s validation/v1.2.1/wave-4 -p 'test_runtime_boundary.py' -v
```

The historical workflow tokenizer test uses a pre-existing, hash-pinned local
asset at its original author-cache location. Its positive check skips when that
asset is absent; when present, it requires `tiktoken==0.12.0` from the optional
requirements above (otherwise it fails with `PackageNotFoundError`). The asset is
not shipped or downloaded by the test. This is a disclosed historical test
prerequisite, not a consumer-build dependency; do not change frozen inputs or
expected outcomes to bypass it.

## Consumer package

```sh
.venv-qa/bin/python tools/atlas_docs.py catalog
.venv-qa/bin/python tools/atlas_consumer.py build --output dist/atlas-consumer-wave5 --archive dist/atlas-consumer-wave5.tar.gz
.venv-qa/bin/python tools/atlas_consumer.py verify --output dist/atlas-consumer-wave5
```

`tools/consumer-policy.json` is the explicit inclusion policy: canonical manifest IDs,
registered domain maps, generated navigation and named consumer support files. It
does not recursively copy arbitrary directories. Frozen benchmarks, evaluator data,
validation reports, tests, maintainer-only files and historical inputs are excluded.
The older `dist/atlas-consumer/` is pinned by the frozen workflow evaluation and
must not be rebuilt in place. It remains internally verifiable but no longer
matches the corrected live source; use the Wave 5 path for source-bound verification.
All canonical cards and included support documents retain their source bytes.
Missing consumer-local links fail the build; fix the canonical document rather
than substituting a label for inaccessible maintainer evidence. The only synthetic
document is the short consumer README, authored in `atlas_consumer.py`. The package
manifest records source/output hashes; it is generated, not a second source of truth.

Verification reconciles all IDs/counts, relations, fourteen domain maps, generated
index freshness, relative links/anchors, source citations and inventory/hashes.
Source-bound verification additionally reconciles the entire allowlist and source
bytes. Manifest hashes are integrity bindings, not signed authenticity guarantees.
Archives have sorted paths, fixed metadata and timestamp-free gzip headers. Equivalent
builds have identical hashes. Archive destinations inside the package, source paths
outside `dist/`, and symlink aliases are rejected before writes; verification is
repeated after archiving. Reference-style Markdown definitions are rejected
fail-closed: use explicit inline links. This is not a complete CommonMark/HTML
renderer. Repeating an unchanged build is idempotent; a stale or
changed destination fails closed. Use a fresh output path when source changes; do not
overwrite an old snapshot in an evaluation arm. Temporary fixtures use `TMPDIR`.

The final consumer cleanup keeps the pre-cleanup Wave 5 archive at
`validation/v1.2.1/consumer-cleanup-wave5-before.tar.gz` so earlier release reports
remain reproducible; it is historical evidence, not the current consumer. The
current Wave 5 directory/archive are reproducible generated outputs ignored by
Git. Do not ignore `dist/` or `validation/` wholesale: the older consumer and frozen
snapshot/benchmark dependencies remain visible and unchanged. The verifier retains
the exact consumer-1 catalog footer only when checking legacy consumer-1 packages;
current consumer-2 output must match current generated navigation.

For an external agent, provide only the package path and explicitly request reading
`START_HERE.md` if its harness does not automatically discover `AGENTS.md`. No tool
installation is necessary to consume Markdown. Available files are not loaded context.

## Retrieval cost audit

```sh
.venv-qa/bin/python -m pip install -r tools/retrieval-requirements.txt
.venv-qa/bin/python tools/atlas_retrieval_cost.py --baseline validation/v1.2.1/pre-v1.2.1.tar.gz --output validation/v1.2.1/retrieval-cost.json
```

This replays eight declared selective read paths against archived pre-edit bytes and
the current source. The L2 seed sets are identical; L1 reads are named sections,
not whole-domain straw-man baselines. Each returned chunk has path/line range,
hash, bytes and `cl100k_base` token count. Without optional tiktoken, only explicit
byte/word proxies are reported. These are retrieved-text tokens, **not model input
usage**, latency, billed tokens or autonomous retrieval choices. Prompts, tool
wrappers, accumulated conversation replay and reasoning are not included. A separate
workflow benchmark is needed to establish a quality/cost benefit. See the
[Wave 1–2 report](../validation/v1.2.1/wave-1-2-report.md).
