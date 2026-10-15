# v1.2.1 Wave 1–2: retrieval and consumer delivery

## Status and claim boundary

Implemented compact entry, generated task views, stopping rules and a deterministic
consumer package. **Not established:** substantial reduction in actual model input
usage, lower billing, faster supported answers or preserved recommendation quality.
Those require the separate workflow evaluation. The existing v1.2 already supported
selective reading; it is not defensible to compare only against loading all cards.

## Exact-token offline read replay

Command and complete per-read logs/hashes: `tools/atlas_retrieval_cost.py`,
[retrieval-cost.json](retrieval-cost.json). Tokenization is tiktoken 0.12.0,
`cl100k_base`, on exact returned UTF-8 text. These are **content tokens, not provider
usage**. Model prompts, tool wrappers, accumulated conversation replay, reasoning,
output, cache discounts, elapsed time and billing are not measured.

Both paths read the **same L2 seed cards** and selected L1 sections. Before uses
archived AGENTS plus the relevant old task-pattern section; after conservatively
counts auto-loaded small AGENTS, START_HERE and one generated route. A skilled
consumer can skip L1 when its Decision already resolves the comparison; this replay
does not presume it must read every navigation layer. It is a declared reproducible
path, not a trace of autonomous choices or a sufficiency proof.

| Task | L2 cards | Before content tokens | After content tokens | Reduction |
|---|---:|---:|---:|---:|
| Scorer selection | 5 | 12,057 | 11,576 | 3.99% |
| Graph overmerge | 4 | 10,593 | 10,141 | 4.27% |
| Blocking | 5 | 11,013 | 10,569 | 4.03% |
| Without reliable labels | 4 | 10,535 | 10,090 | 4.22% |
| Rule refactor | 4 | 12,022 | 11,539 | 4.02% |
| Reproducible experiment | 4 | 10,760 | 10,288 | 4.39% |
| New source | 4 | 9,681 | 9,192 | 5.05% |
| Incremental identity | 4 | 10,780 | 10,319 | 4.28% |

The selective whole-path saving is **modest**, not a demonstrated major efficiency
improvement. Each after path has one additional read request/document for the split
entry: graph is 11 reads/9 distinct documents versus 10/8. Reading requests are not
measured sequential hops or latency. Grouping related reads into a tool call can
change latency without changing returned text. No route loads all 57 cards or all
14 indexes.

### Entry and duplication audit

- Old AGENTS: 8,175 bytes / 947 words / 1,514 content tokens. New AGENTS: 865 bytes /
  107 words / 172 tokens. The reduction alone is not the whole workflow saving.
- START_HERE: 408 words / 697 tokens. Graph route: 519 tokens. Entry + graph route is
  **1,216 tokens**, before optional auto-loaded AGENTS; the illustrative 500–1,000
  discovery target is not met for this route. It is a soft budget, not a reason to
  remove essential limitations. Eight routes remain individual small files.
- All L1 files together: 171,637 → 132,799 bytes, by removing long-title repetition
  in relation/tag fanout while retaining canonical summaries and all links. Agents
  are not instructed to load that combined amount.
- The old task-pattern guide is 8,907 bytes and catalog 29,349 bytes; neither was
  required wholesale by the old guidance. The new direct route avoids needing to
  locate its heading manually. README/intake/integration are optional purpose-specific
  material, not automatic cold-start loads.
- Canonical corpus remains 57 cards / 517,428 bytes, unchanged in Wave 1–2. No
  scientific cards were shortened to manufacture token savings.

The graph route points directly to DEC-08-001, SOL-08-003, SOL-08-004 and
EVAL-11-003. It separates edge filtering (admission change) from constrained
membership and preserves true-chain/false-dense-merge counterexamples. Project facts
may require additional calibration, incomplete-reference or lifecycle material;
2–4 cards is not a ceiling.

## Consumer package

Built `dist/atlas-consumer/` and `dist/atlas-consumer.tar.gz`: 130 files, 57 exact-byte
canonical cards, 1,019,689 total directory bytes including manifest. Source-bound
verification, links/anchors, canonical IDs/counts/relations, navigation freshness,
source-reference rendering, exclusion policy and equivalent-build archive hashes
pass. Full output: [consumer-build.json](consumer-build.json).

The inclusion allowlist is `tools/consumer-policy.json`; it derives canonical IDs
and domain maps from approved manifests and names each support file. Unknown files
cannot enter merely because they are Markdown or share a directory. Maintainer-only
files, tests, validation, keys, traces, results and dev_docs are absent. Public mixed
support pages retain scope/evidence information but explicit unbundled maintainer
links become marked plain text; all changes are manifest-recorded. Canonical card
bytes are never transformed.

No hosted search, RAG, embeddings, local database or runtime lookup helper was added:
individual Markdown routes already supply deterministic paths. Builder tokenization
is optional audit tooling, not a consumer dependency.

## Validation and remaining acceptance boundary

Observed route-generation and title-duplication RED → GREEN tests, a missing-builder
RED → GREEN end-to-end package test, exact CRLF section preservation, two equivalent
builds/archives, updated-title regeneration, and extra/missing/modified/symlink
rejections. After Wave 2, 55 documentation/tooling tests pass; existing checks were
not weakened. The old subprocess test and expanded scientific review remain for
later waves.

Automated checks establish path discovery, bounded declared retrieval, referential
integrity, isolation, reproducibility and scientific-boundary wording. They do not
prove an unfamiliar model follows the route or preserves recommendation quality.
Actual per-task relevant/irrelevant reads, provider input usage, supported-answer
latency and quality must be measured in the new workflow protocol, with failed and
unscored attempts retained. No new solver result or independent score is asserted
by this report. No commit/push or production change was performed.
