# Wave 1–2 tooling review and disposition

A separate read-only critic exercised scratch copies of the new builder, route
renderer and read-accounting CLI. Reviewer model identity is unattested; this is a
bounded implementation critique, not independent utility scoring or full scientific
certification. No frozen keys/scenarios/results were opened.

## Demonstrated findings and author fixes

| Severity | Reproducer | Resolution | Regression evidence |
|---|---|---|---|
| High | Archive output inside package or source could overwrite START_HERE/canonical bytes after verification, yet return success | Destination checked before build/write; package-contained paths, source paths outside dist and symlink aliases rejected. Package reverified after archive creation | Observed failing then passing archive-collision test using scratch source/package; canonical source files not touched |
| Medium | Reference-style Markdown definitions escaped allowlist rewriting and relative-link checking | Explicit fail-closed unsupported-reference-definition gate in shared validator, route generation and consumer source ingestion; use inline Markdown links | Observed failing then passing missing/escaping/unbundled target tests; code-fenced examples remain allowed |
| Medium | Fenced `##` examples truncated declared sections and token counts | Shared fence-aware line mask/range used by read audit and route extraction; backtick/tilde fences and delimiter length honored, original byte ranges/CRLF preserved | Observed failing then passing fake-matching-heading/inner-boundary cases for three fence forms |
| Low | Route slug algorithm disagreed with canonical L1 parser for linked titles | Route anchors use shared heading-ID implementation | Observed failing then passing linked-title regression |

Returned review probes lived in scratch. Author verified each principal defect
with repository regressions and fixed the relevant sibling path, not just the
reported call. All 59 documentation/tooling tests pass after fixes; 49 are inherited
Atlas documentation tests. These tests demonstrate tooling behavior, not ER outcomes.

## Post-fix checks

- Source-bound consumer verification passes: 130 files, 57 cards; manifest and archive
  hashes remain unchanged because the fixes affect tooling rather than consumer text.
- Exact-token read replay rerun to [post-review accounting](retrieval-cost-post-review.json)
  reproduces all eight earlier cost totals. The fenced-example bug did not affect
  those existing source sections. Savings remain modest, not a measured model gain.
- [Post-review lint](post-review-lint.json): zero errors and 34 existing advisory
  warnings. No warning or validation gate was suppressed.
- [Protected-byte check](wave-2-protected-integrity.json): 796 historical/protected
  files and 57 canonical cards unchanged from pre-v1.2.1 baseline.

No independent post-remediation approval is claimed. Markdown validation supports
explicit inline navigation and rejects reference-style definitions; it is not a
complete CommonMark/HTML renderer or a malicious-file security sandbox. Integrity
hashes are not digital signatures. The new workflow experiment remains separate.
