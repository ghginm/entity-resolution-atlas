# AU-v2 offline integration layer

**Implemented:** snapshot export/verification, neutral metadata-only L0, frozen
three-arm preparation plan, broker compatibility binding, offline JSONL state,
mechanical registration/evidence checks and [mechanical blinded packet/score tooling](SCORING.md).
**Not implemented:** model process executor/transport adaptation, actual independent
evaluator invocation and genuine model-identity/settings eligibility.
There is deliberately no `run` command and no provider client or credential access.
No AU-v2 model run or score exists.

This directory is evaluation infrastructure, never Atlas retrieval knowledge.
AU-v1 source/results and the AU-v2 frozen data tree are byte-preserved. The frozen
package metadata describes its preparation checkpoint; current integration status
belongs here and in the tracker, not in edits to `package.json` or a new freeze.

## Reuse boundary

`bridge.py` imports the byte-pinned AU-v1 harness for `ReadBroker.read`, path/layer
eligibility, discovery metadata, canonical serialization and exclusive writes. It
uses the byte-pinned AU-v2 verifier for strict JSON/schema/path validation. No global
monkeypatching, cloned subprocess runner or second agent runtime is introduced.
`Broker` explicitly binds snapshot semantics and budget names while retaining the
old read/accounting mechanism; responses are transformed to AU-v2 fields. The
original legacy `run_scenario` is **not** a usable AU-v2 executor yet.

`Session` checks ready identity/settings equality, exact JSONL framing, read/final
order, byte/final limits, terminal exit and raw-message journal hashes/timestamps.
It does not spawn or kill processes, enforce wall deadlines, attest remote context
or prove tools/model identity. Its generated broker-response bytes are recorded as
`broker_generated`, not falsely labeled transport-sent bytes.

## Shared corpus eligibility and provenance

Atlas arms use the same source eligibility, layer policy and metadata generation.
Only cards, selected taxonomy pages, deep dives, bibliography/evidence policy are
eligible. Guides, raw README/CATALOG/AGENTS, maintenance/review documents, validation,
tools/tests/dev_docs and benchmark artifacts are excluded. Legitimate L2 cards whose
names contain `review` are retained; such a name alone is not an evaluation artifact.
This comparison therefore does **not** measure the new task/integration guides.

Markdown payloads are byte-preserved under neutral `.md.txt` inventory names in both
arms. This keeps copied historical links outside the live Markdown documentation
graph without weakening its linter. Generated L0 maps to the actual exported paths;
links inside payload text do not authorize access. The broker uses only exact
inventory names, not automatic link-following or live repository access. Content
may reveal corpus age/coverage; this is not perfect blinding.

Selected snapshots: `corpora/2026-10-14-02/{baseline,expanded,empty}`.
Baseline is the verified historical v1.1 corpus (31 cards, 52 files); expanded
contains all 57 current cards (79 files); no-Atlas is empty. The comparison question
is the entire v1.1 → v1.2 expansion, not Wave 4 alone. The preparation plan pins
inventory/manifest/prompt/settings/bridge hashes and 24 **unexecuted** cells in the
frozen Latin rotation. Source provenance and actual checks are in
[the integration validation](../v1.2/au-v2-integration-validation.json).

The initial `2026-10-14-01` export attempt is retained but superseded/unselected:
a too-broad name filter omitted two review-named L2 cards from expanded export.
A failing regression was observed, the policy was versioned and a complete new
three-arm export was made. This was an export defect, not a failed model cohort;
no answers/scores were produced or used to tune knowledge.

## Exercised commands

From the repository root:

```sh
python3 -B -m unittest discover -s validation/agent-utility-integration/tests -v
python3 -B validation/agent-utility-integration/bridge.py verify --snapshot validation/agent-utility-integration/corpora/2026-10-14-02/expanded --expected-sha256 3c69f5e66bfb4a3b517df20611505563dd343fe3164139dd1770596890d889c7
```

`prepare --source SOURCE --arm baseline-atlas|expanded-atlas --out NEW_DIRECTORY`
exports eligible knowledge. `prepare --arm no-atlas --out NEW_DIRECTORY` requires
no source. `plan --baseline SNAPSHOT --expanded SNAPSHOT --empty SNAPSHOT --out NEW_FILE`
creates an offline preparation plan. Existing destinations are never overwritten.
The selected [plan](preparation-plan-2026-10-14-02.json) already exists; do not reuse
that output path. Prepared cells are not frozen-schema run records or actual attempts.

`check-registration --registration FILE --evidence DIRECTORY --runtime FILE --adapter FILE`
also requires the three snapshot arguments above. No real registration file is
provided. It validates the frozen registration schema, source bindings, supplied
runtime/adapter file hashes, distinct model/version declarations and evidence
artifacts. It never returns execution eligibility merely because those checks pass.

Model evidence is strict JSON at `<evidence_sha256>.json`, byte-hashed to its registered
anchor, with `kind=model-attestation`, role/identity/provider/model/version and
fresh-process/conversation/independence values matching registration. It also requires
`broker_only=true`, integer `callable_tools=0` and a nonempty signed conflict declaration.
Generation evidence is strict JSON at each registered canonical `generation.*.evidence`
path, with `kind=generation-attestation`, setting, requested/effective/enforcement
and `cross_arm_equivalence=true`. Missing null-valued keys are not accepted as
present nulls; unsupported effective values must be null and limitations disclosed.

**Trust limitation:** these checks verify artifacts/claims and supplied single-file
hashes, not signature authenticity, actual backend identity, full transitive runtime
identity or honesty of declarations. Independent operator verification and real
transport evidence remain necessary. Synthetic registration fixtures live only in
scratch tests and are not an operator registration or model results.

## Exact next implementation boundary

Connect these tested protocol/broker bindings to an explicitly reviewed seam in the
existing executor, preserving AU-v1 behavior/artifacts. A specific refactor-authorization
question timed out without a submitted answer; do not infer permission to alter
protected legacy source or clone a second executor. Then test wall/line/initial budgets, retained stderr
and raw transmitted bytes, spawn/exit/timeout and full descendant containment using
synthetic processes before model eligibility. Connect the implemented packet/score
tools to genuinely independent evaluator invocation; do not open keys in corpus-author/solver context.
Register attested actual identities/settings/conflicts and externally pinned
provenance before a complete real cohort. No provider probe was made in this wave.

The remaining steps and budget sums are [recorded separately](../v1.2/au-v2-remaining-work.md).
[Scoring-wave checks](../v1.2/au-v2-scoring-validation.json) are synthetic infrastructure
evidence, not genuine independent scores; original evaluator draft bytes are preserved
and per-dimension caps/quotes/provenance are checked without inventing raw judgments.
