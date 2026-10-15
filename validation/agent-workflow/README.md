# Agent workflow evaluation — AW-offline-1

**Offline infrastructure only. Zero genuine solver runs, zero independent scores, no model-gain claim.** This package owns only `validation/agent-workflow/`. It neither changes nor replaces AU-v1/AU-v2. Nothing here belongs in a consumer retrieval corpus.

## Frozen inputs and arms

Eight new fictional project briefs (232–241 context words each) cover no-labels evaluation, graph overmerge, ordered-rule refactoring, source-aware scoring, blocking cost, source onboarding, incremental IDs, and reproducible experiments. They include implementation context, identity grain, constraints, evidence limitations and bounded authorization. The evaluator checklists are non-exhaustive semantic prompts, not answer scripts or required method names. Quality dimensions are framing, method, assumptions, baseline, failures, evaluation, uncertainty and actionability.

Freeze manifest SHA-256 (recorded before implementation probes or any solver outputs):

```text
132fef9b963a68c87faae045f1e2ef96201827f1f70a445616464fdb728011e8
```

`freeze-manifest.json` binds all 14 files under `frozen/`: eight scenarios, prompt, protocol, evaluator rubric/checklists, export policy and external bindings. There is no re-freeze command. Copy the anchor outside this package before future work; hashes detect byte changes, not malicious replacement of the verifier plus every anchor. Frozen inputs have not been changed after freezing.

| Arm | Available documents, not retrieved | Knowledge / navigation policy |
|---|---:|---|
| A | 0 | noAtlas |
| B | 52 | v1.1 knowledge; existing immutable shared-eligibility baseline, 31 cards |
| C | 79 | v1.2 knowledge; existing immutable shared-eligibility expanded snapshot, 57 cards |
| D | 130 | v1.2.1 public consumer files plus generated compact L0; 57 cards, guides, entry and task routes included |

B/C use pinned existing source manifests and `bridge.verify_snapshot` without changing legacy eligibility. D copies the exact pinned consumer allowlist and bytes into neutral `.txt` paths, with compact L0 using existing card-metadata primitives. Canonical cards are not rewritten. Source manifests and all copied content are checked. Links do not grant access: use exact inventory paths, including `.txt` suffixes. D includes `START_HERE.md.txt`, the new task routes and intake/integration guides. Its source consumer manifest is pinned to `fc6078f5243355ab19947d1c649ee80aa04ba8c3266dee16200f5d7a7f440bd3`. Parent tooling updates are intentionally not dependencies; consumer source bytes, not mutable builder code, are bound.

**No E ablation:** C versus D confounds navigation, guides, normative/reference context and packaging. Equal canonical card counts do not identify a pure navigation effect. Do not attribute future differences solely to routing.

## Implemented interfaces and separation

- `workflow.py prepare|verify|plan|report` — deterministic, exclusive preparation and honest unexecuted reports. Explicit missing preparation paths fail. Existing outputs are never overwritten.
- `Broker(prepared, arm, tokenizer_asset=None)` — tested explicit subclass binding to unchanged legacy `ReadBroker.read`; it does not use legacy `Session`, `contract`, execute/run code, frozen scenarios, keys or results. No globals are redirected and no executor is copied.
- `Broker.read(request)` — legacy-compatible result object with `content` and `error`; exact request shape is `{type, request_id, path, offset, length}`, with type `read_file`. Offsets/lengths are zero-based Unicode code points, not UTF-8 bytes. All invocations are retained, including denials, malformed requests, fatal budgets and post-failure attempts. Fatal errors poison the broker. Returned excerpts retain their text/hash, returned bytes/characters, optional tokens and evaluator-relevance placeholders. Repeated content counts again.
- `Broker.accounting()` — attempts, successful reads, unique documents, returned characters/UTF-8 bytes and optional real text tokens. Provider input/output tokens, wall time, money and semantic relevance remain null without evidence/judgments. No bytes-to-billing conversion exists.
- `offline_probe(prepared, tokenizer_asset=None)` — deliberately prescribed repeated reads and traversal denials. Not a model run, not a task comparison, not quality evidence. `evidence/offline-probe.json` retains actual read accounting, including ordinary tokenizer counts from the local pinned asset.
- `gate_real_run()` always raises: no registration string can enable dispatch in this package.

Every operational entry point checks the freeze and external bindings. Preparation verification compares its entire inventory and bytes against the frozen source closure, not just an untrusted mutable receipt. Every broker read rechecks the whole prepared package. This small-corpus approach is intentionally simple, not optimized for large runtimes. Symlinks, inventory additions, changed payloads, changed manifests and changes hidden behind rehashed preparation receipts fail closed.

`prepared/initial/solver/` contains only the prompt, fictional inputs and path/layer/byte inventories. It contains no keys, rubric, protocol, reports or runtime implementation. Payload bytes are broker-only under `snapshots/`. `frozen/evaluator/` and `evidence/` are evaluator/operator-only; a future executor must isolate the solver from the whole host filesystem. This offline layout is **not itself OS/process isolation**.

## Comparable budget and quality/cost rules

All 32 planned cells use one repetition, the same scenario/prompt, counterbalanced four-arm order, 24 attempted reads, 16 successful reads, 48,000 returned Unicode characters, 8,000 characters/chunk, 12,000 final characters and a future 240-second solver wall ceiling. Future evaluators have a 600-second ceiling. Only read budgets are exercised here; no process exists to enforce final/wall/generation limits. Fresh contexts, model/provider/version and equivalent effective generation settings require trusted executor/operator evidence before any real run.

Quality is an eight-dimensional ordinal vector, never a weighted winner. The frozen rubric requires concrete quotes or scoped omissions, reasons, applicability and evaluator relevance judgments. Defensible alternative answers receive credit. A quality pass requires all dimensions at least 2 and no critical failure; fewer tokens cannot rescue missing limitations, invented outcomes or unsafe assumed prerequisites. Reports expose a per-task quality/cost frontier, presently empty because there are no eligible independent judgments. Frontier eligibility is quality-gated and dimensionwise; no significance claim is possible from this planned single repetition.

Retrieved text tokens are opt-in `tiktoken==0.12.0`, `cl100k_base`, sum of `encode_ordinary` counts **per returned excerpt**; they are not provider usage or whole-conversation tokens. The local asset must hash to `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7`. Construction reads the supplied local BPE file directly, never a remote registry or downloader. Without that asset/library, omit the option and tokens are null, not estimated. The exercised asset is in expiring scratch storage, not bundled. Inventory, scenario and prompt byte sizes can be audited separately; tool wrappers, automatically loaded instructions and repeated provider context remain unobserved. The prescribed probe measures plumbing only, with no token-savings claim.

## Exact tested commands

Run from `/home/ghgin/projects/entity-resolution-atlas` using the existing QA interpreter. No install or network is needed for the default path.

```bash
PY=/home/ghgin/.hermes/cache/scratch/atlas-v11-qa/bin/python
$PY -B -m unittest discover -s validation/agent-workflow -p 'test_workflow.py' -v
$PY -B validation/agent-workflow/workflow.py prepare --output validation/agent-workflow/evidence/preparation.json
$PY -B validation/agent-workflow/workflow.py verify --prepared validation/agent-workflow/prepared/initial --output validation/agent-workflow/evidence/verify.json
$PY -B validation/agent-workflow/workflow.py plan --prepared validation/agent-workflow/prepared/initial --output validation/agent-workflow/evidence/plan.json
$PY -B validation/agent-workflow/workflow.py report --prepared validation/agent-workflow/prepared/initial --output validation/agent-workflow/evidence/report.json
```

The initial preparation and listed evidence files already exist. **Do not rerun the creation commands into those destinations.** Read-only resume commands:

```bash
$PY -B validation/agent-workflow/workflow.py verify --prepared validation/agent-workflow/prepared/initial
$PY -B validation/agent-workflow/workflow.py plan --prepared validation/agent-workflow/prepared/initial
$PY -B validation/agent-workflow/workflow.py report --prepared validation/agent-workflow/prepared/initial
```

For another deterministic preparation choose a new path with `prepare --prepared validation/agent-workflow/prepared/<new-name>`. `evidence/probe-command.txt` contains the exact executed opt-in tokenizer probe command and real stdout. It also uses exclusive output creation; choose a new evidence filename to repeat it. Do not classify these prescribed probes as solver outputs.

Observed TDD main slice: the initial test failed with `AssertionError: False is not true : missing offline workflow implementation` (one test); after the minimal implementation it passed (one test). Subsequent slices exposed missing prepare/Broker/report/tokenizer/probe APIs before implementation; the caller-request-alias regression was observed failing (`777 != 4`) and fixed by retaining a deep copy. Final suite: **12 tests passed**. `evidence/tests.txt` retains actual test stdout. Tests include no-key inventories, Unicode byte/character accounting, repeated reads, null billing, all frozen-input tampering, rehashed prepared tampering, symlinks, extra paths, attempt/read/character/chunk budgets, malformed requests, post-failure accounting, optional pinned offline tokens and blocked real runs. Optional-tokenizer testing skips its positive asset check if the preinstalled asset is absent; it passed here.

## Blockers and resume boundary

1. Existing bridge `Session`/`contract` is AU-v2-specific (three historical arms, old settings, no guides). It is not an AW-compatible executor. Broker reuse is proven; runtime compatibility is **not**.
2. No trusted fresh-process/broker-only/zero-tool executor, registration evidence, raw transport journals or effective-generation evidence is integrated. This package creates no subprocess/provider runtime.
3. Genuine independent evaluator identity/version/settings and non-authorship/conflict attestation are unavailable. The current author/subagent identity is unattested and cannot independently evaluate its own new material. Strings, hashes and ready messages do not prove independence.

Resume with read-only verify/plan/report, then have an operator inspect the existing executor's supported binding seam and independently establish identity/settings/isolation evidence. If it cannot support AW without changing frozen contracts, remain blocked or authorize a separately versioned executor integration **outside this frozen cohort**, not a monkeypatch. Before real outputs, bind any new registration/settings/executor evidence in a new write-once supplemental manifest tied to this anchor; do not edit this protocol or add outcomes to it. A future independent scorer/admission adapter must verify raw replay and judgments before any nonempty frontier is reported. Retain every attempt; recovery is a new full cohort, never selective cell replacement. No run command is offered because none is attested to work.

`evidence/report-final.json` and `evidence/tests-final.txt` are the final read-only readiness/test records. Earlier `report.json` is retained; the final report clarifies that tokenizer availability is opt-in rather than asserting that an external scratch asset is absent. Neither contains model outcomes. The preparation manifest SHA-256 is `bb8cd3f9d29283eed65b0a5c32d23c635cfdd766a85217711bf827b073994f83`; final report SHA-256 is `f1067b32b7e25bba4b27124eb04b9956a74549dd8134a2018b8b674f4b4c5dfb`. `evidence/status.json` provides the same readiness boundary and resume paths in machine-readable form.

`evidence/` artifacts are offline verification/probes, not benchmark results. No commits, pushes, model calls, old benchmark input reads or protected-tree edits were performed.
