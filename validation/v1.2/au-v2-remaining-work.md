# AU-v2 remaining work and scope — after mechanical scoring implementation

This operator note is evaluation infrastructure, not Atlas knowledge or a solver hint.
The user requested remaining steps/overall volume and continued implementation.
Knowledge expansion is already implemented; new cards are not required to finish
this benchmark. No utility improvement or complete runtime is claimed.

## Implemented at this checkpoint

- Frozen AU-v2 data: eight scenarios/keys and eight ordinal dimensions; integrity
  anchored externally. Canonical content was hashed before case design and is not
  tuned to keys/responses.
- Shared-policy baseline v1.1 / expanded v1.2 / no-Atlas exports: 31 / 57 / zero
  cards. Selected `-02` snapshots and the 24-cell Latin preparation plan are retained.
- Legacy broker reuse, strict protocol state and mechanical registration bindings.
- `scoring.py`: completed-run provenance and journal replay, exact sent/read/final
  bytes and stderr hash checks, neutral evaluator packets with private receipts,
  strict score/identity/quote/finding validation, per-dimension caps, null retrieval
  applicability, alternative credit and exclusive packet/draft/final artifacts.
  CLI and end-to-end tests use explicitly synthetic contexts in scratch only.

Actual final checks belong to [scoring validation](au-v2-scoring-validation.json).
The subsequent [bounded scoring review](au-v2-scoring-review.md) and
[post-review validation](au-v2-scoring-post-review-validation.json) supersede the
current implementation hashes. Registration evidence/executable checking remains
an explicit external operator prerequisite, not an enforced scoring gate.
These tests prove bounded infrastructure behavior, not model identity, signature
honesty, semantic correctness of an evaluator's endorsement judgment or OS isolation.
Real provider calls, solver runs and independent scores remain zero.

## Remaining steps

| Step | Concrete work / acceptance boundary | Dependency / scope |
|---|---|---|
| Process executor and transport | Bind the existing executor to AU-v2 protocol/corpus contracts; enforce initial/line/wall/final budgets, actual ready evidence, raw sent/received/stderr retention, exit/timeout and descendant handling; synthetic-process regression tests before models | Do not clone a second runtime. Limited refactor of protected legacy runtime source requires explicit scope authorization, archived original bytes and preserved AU-v1 behavior |
| Actual identity/settings eligibility | Select tested/evaluator models and versions, obtain trusted response/transport identity evidence, zero-tools/fresh-context and generation-equivalence evidence, resolve author/evaluator conflicts and independent declaration, pin implementation/registration hashes | Requested CLI strings and structural attestations are insufficient; provider access/credits/prices are not newly verified. Missing trustworthy identity evidence may block execution regardless of code readiness |
| Evaluator invocation and full cohort | Connect an independently eligible evaluator to the implemented packet/scoring tools; preregister and run all 24 solver cells and score each genuinely completed response, retaining failures and unscored cells | Frozen prompt/settings/cases/keys unchanged. Transport recovery is a fresh full cohort, not selective favorable retries; no author self-scoring |
| Comparative report | Revalidate run/packet/draft/score provenance and caps; report case × dimension outcomes, regressions, cost/read/latency/completion and limitations under the frozen first-completed rule | No weighted total, invented winner or significance claim. One repetition is exploratory. This corpus export excludes the task/integration guides |
| Final closure | Full regression/lint/citations/hash checks, honest execution status and resumable commands, final tracker/report | Preserve frozen inputs, old results, original runtime archive and all attempted artifacts; commits/push remain unauthorized |

## Overall volume and budgets

The remaining engineering centerpiece is a shared process-executor/transport block,
plus evaluator invocation/eligibility and reporting. The mechanical scoring block
is now implemented, not independently executed. Expect another substantial
implementation/verification iteration and a separate model/evaluation/reporting
cycle, not a few documentation edits. Exact elapsed time depends on the required
executor seam, available trusted identity evidence and provider failures; no invented
completion percentage or precise implementation deadline is supplied.

The frozen design has 8 scenarios × 3 arms × 1 repetition = 24 solver cells.
If all complete, it needs 24 independent assessments: 48 result-bearing artifacts,
not 48 API calls (broker turns may make several requests). At the full sequential
wall budgets, solver cells account for 96 minutes and evaluator assessments for
240 minutes, 5.6 hours combined before overhead/recovery. These are budget sums,
not a runtime prediction or spending quote. Provider prices and access remain unknown.

## Authorization checkpoint and exact next action

A targeted UI question requested permission to refactor only the necessary
unfrozen AU-v1 runtime source while preserving frozen cases/keys/manifest and old
results plus original source bytes. It timed out without a submitted answer.
**No authorization was inferred and no legacy runtime source was edited.**

Resume the remaining executor seam only after that scope is explicit. Archive and
hash the original harness, then introduce a shared dependency-bound executor with
AU-v1 compatibility tests and AU-v2 synthetic-process tests; never bypass the new
protocol by using init/requested identity strings. Keep semantic evaluator material
out of the author/solver conversation. If provider/identity evidence cannot be
established, finish and report executable infrastructure as unexecuted rather than
fabricating an empirical result.
