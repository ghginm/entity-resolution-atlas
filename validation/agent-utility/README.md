# Independent agent-utility benchmark — AU-v1

**Status: frozen; paired runs, no-Atlas runs and blinded scoring EXECUTED (2026-10-13).** Two paired cohorts retain 32 attempts (25 completed, seven failed); the no-Atlas arm completed eight more. All **33 completed responses have validated scores**. The first-completed, earlier-cohort-first comparison covers all eight scenarios; extra attempts remain visible. Results are mixed, including a v1.1 assignment/identity regression: see the [per-dimension comparison and critical failures](results/COMPARISON-2026-10-13.md). Scoring recovered via fresh `openai-codex` provider-default processes; the exact evaluator model/version was not pinned or wire-attested. Initial provider failures remain in the [execution history](results/EXECUTION-STATUS-2026-10-13.json). No simulated scores or universal improvement claim. Protocol fixtures validate the harness, not Atlas usefulness.

## Package boundaries
- `inputs/AU-01.json` … `AU-08.json`: eight fictional, novel project scenarios: harmful bridge, selected truth, one-to-one monthly linking, sparse multiscript labels, temporal/reused identity, conflicting master fields, capped high-scale queue, unjustified graph upgrade.
- `evaluator-only/keys/`: semantic findings and conditional critical failures. **Not agent context.**
- `evaluator-only/rubric.json`: eight ordinal dimensions, anchors 0–3, per-dimension caps; no weighted aggregate.
- `prompt.txt`, `settings.json`, `protocol.md`: frozen common instructions, character/read/wall budgets, independent-agent/evaluator protocol.
- `schemas/`: scenario, execution-result and independently scored-result schemas. Stdlib validator supports exactly the schema keywords used here, not general JSON Schema. Score validation against a run also checks quotes, IDs, caps, independence declarations and provenance.
- `baseline/atlas-v1-baseline-hashes.json`: original full 77-file baseline manifest, copied byte-for-byte. Git `main` had no HEAD; this byte snapshot/manifest is the baseline, not a fabricated commit.
- `corpora/v1/`: preserved **42 allowlisted files**, including generated L0, 17 L1 pages, 21 original L2 cards and 3 L3 references/deep dive. The content is a copy of v1, not newly authored Atlas knowledge. Its manifest hash is pinned in the harness. The full baseline snapshot is not required for tests or v1 runs, only if rebuilding/verifying the entire original snapshot.
- `harness.py`, `tests/`: stdlib broker, fresh subprocess runner, counterbalanced comparison, schemas/provenance/caps and actual subprocess test fixtures. Tests use the shipped corpus; no network, credentials or installed model needed.

Freeze occurred at **2026-10-13T02:14:09.192271+00:00**. Frozen content is never edited/refrozen for this cohort. The harness and operational README are not answer keys; their hashes are recorded separately per execution. Any harness fix after genuine runs requires rerunning both arms and retaining prior attempts; changing inputs/prompt/protocol/rubric/settings requires a new named cohort. To verify the freeze, use the externally recorded anchor below, not a newly generated manifest.

## Tested local commands (no model adapter)
Run from `/home/ghgin/projects/entity-resolution-atlas`:

```bash
python3 validation/agent-utility/harness.py verify-freeze
python3 validation/agent-utility/harness.py verify-corpus --corpus validation/agent-utility/corpora/v1
python3 -m unittest discover -s validation/agent-utility/tests -v
```

A repeatable dry-run path uses a **new** output directory; never overwrite an attempted cohort:

```bash
python3 validation/agent-utility/harness.py dry-run   --corpus validation/agent-utility/corpora/v1   --out validation/agent-utility/results/operator-dry-run-01
python3 validation/agent-utility/harness.py run   --corpus validation/agent-utility/corpora/v1   --out validation/agent-utility/results/operator-unexecuted-01
```

The second command deliberately has no adapter: all eight records are `unexecuted`, not successful runs. `prepare` is exercised by harness tests and the shipped v1 corpus was built with:

```bash
python3 validation/agent-utility/harness.py prepare   --source /home/ghgin/.hermes/cache/scratch/atlas-v1-baseline   --label v1 --out validation/agent-utility/corpora/v1
```

This exact destination already exists; do not rerun into it. Rebuilding to a fresh destination verifies every original source file and the complete preserved baseline mapping before packaging.

## Real equivalent v1/v1.1 execution
The actual cohorts were executed with the trusted zero-tool transport `adapters/hermes_cli_jsonl_adapter.py` (evidence and initial blocker history: [results/EXECUTION-STATUS-2026-10-13.json](results/EXECUTION-STATUS-2026-10-13.json)); all completed responses are scored. Do **not** use `tests/fixture_adapter.py` as a tested agent — its replies are protocol fixtures, never model results. The adapter handles no credential capture, no environment credential forwarding, no API-key CLI flag and no fake API client; the tested model receives no direct filesystem/network/shell tools beyond the broker.

Prepare v1.1 **after** coverage/content changes finish, not during edits:

```bash
python3 validation/agent-utility/harness.py prepare   --source /home/ghgin/projects/entity-resolution-atlas   --label v1.1 --out validation/agent-utility/corpora/v1.1
```

Select the actual model identity by replacing `ACTUAL_MODEL_ID` below. All other model/budget/layer settings are frozen and the runner rejects tuning. The pin command writes a new execution settings file; record its printed hash externally before model results.

```bash
python3 validation/agent-utility/harness.py pin-settings   --model ACTUAL_MODEL_ID   --out validation/agent-utility/execution-settings.json
sha256sum validation/agent-utility/execution-settings.json
```

Replace `/ABSOLUTE/PATH/real_jsonl_adapter.py` with the operator's real adapter and `BENCHMARK_AUTHOR_ID` with the author identity. These are **required substitutions**, not an installed adapter/model. No secret may appear in argv. The model's attested identity must differ from the benchmark author. Each scenario is a new process, temporary cwd/HOME and fresh remote conversation; default cohort has one run per arm per scenario, alternating arm order.

```bash
python3 validation/agent-utility/harness.py run-paired   --v1 validation/agent-utility/corpora/v1   --v11 validation/agent-utility/corpora/v1.1   --settings validation/agent-utility/execution-settings.json   --adapter '["/usr/bin/python3","/ABSOLUTE/PATH/real_jsonl_adapter.py"]'   --author-identity BENCHMARK_AUTHOR_ID   --out validation/agent-utility/results/model-cohort-01
```

`registration.json` is written before spawning any process: model/settings/prompt/freeze/harness/corpus hashes, author, adapter command, fixed scenario order/repetitions/exclusions. Results are written one by one, not lost when a later run fails. Counterbalanced order is AU-01 v1→v1.1, AU-02 v1.1→v1, and alternating onward. `failed` records retain the failure and any partial read logs/response; they are unscored. The CLI returns the recorded statuses; check them, not just the CLI exit code. Setup/corpus/eligibility errors abort before a model run and return exit 2 rather than inventing results. All actual attempts must be retained.

Optional no-Atlas baseline:

```bash
python3 validation/agent-utility/harness.py prepare   --label no-atlas --out validation/agent-utility/corpora/no-atlas
python3 validation/agent-utility/harness.py run   --corpus validation/agent-utility/corpora/no-atlas   --settings validation/agent-utility/execution-settings.json   --adapter '["/usr/bin/python3","/ABSOLUTE/PATH/real_jsonl_adapter.py"]'   --author-identity BENCHMARK_AUTHOR_ID   --out validation/agent-utility/results/no-atlas-cohort-01
```

## JSONL adapter contract and containment limits
The frozen protocol is authoritative. Adapter stdin starts with one JSON object: scenario, frozen prompt/settings/hash, path/layer/byte inventory and read tool contract. It has **no key/rubric, source-repo path, run results or arm label**. L0 is a generated compact metadata index; raw CATALOG/README/AGENTS are not loaded, avoiding stress-test/coverage pointers. All guides, validation/tests/tools/dev_docs, research answers/reviews/opportunities, coverage/change logs and implementation plans are outside the corpus allowlist; only substantive `research/hypotheses/` cards are retained from research. Deep dives plus bibliography/evidence policy are L3. Paths mentioned as links are not automatically readable.

Adapter stdout, line 1:

```json
{"type":"ready","identity":"ACTUAL_FRESH_AGENT_ID","fresh_context":true,"broker_only":true,"settings_sha256":"COPY_FROM_START_MESSAGE"}
```

Read request and final output shapes:

```json
{"type":"read_file","request_id":"r1","path":"index/L0.json","offset":0,"length":8000}
{"type":"final","text":"The actual independently generated recommendation"}
```

The adapter waits for `read_result` before using retrieved content, and must exit zero after `final`; further stdout fails. Log chatter belongs on stderr (discarded by the harness), never protocol stdout. Requests are exact inventory paths, Unicode-character offsets/chunks; traversal, keys, symlinks and alternative spellings are denied. Limits: 24 attempts / 16 successful reads / 64000 retrieved chars / 8000 per chunk / 24000 initial chars / 24000 final chars / 65536 bytes per stdout line / 240 seconds wall. Repeated reads count again; denied attempts count. Budget violations fail closed. Read content, offsets/layers, hashes and counters are retained for evaluator inspection. Character budgets are not tokenizer-specific token budgets; optional model-provider usage should be recorded externally, without replacing broker measurements.

**Not an OS security sandbox.** The broker enforces model context only if the trusted adapter exposes no other tools/memory. Child code itself can access the host. Attestations and fresh PIDs cannot prove fresh API sessions or absence of unauthorized tools. Untrusted adapters require an operator-supplied OS/container sandbox before eligibility; the harness does not install or pretend to supply one. HOME/cwd/env are isolated/minimized and wall timeout kills the process group. No environment service credentials are copied into the subprocess.

## Independent scoring commands
The evaluator must be a distinct human or fresh model process, not the author, tested agent or coverage-card writer, and must actually inspect claims and read excerpts. Independent/blinded role and conflicts are declared; a program cannot establish sincerity or semantic correctness of that declaration. Blinding excludes labels/timestamps/adapter identifiers, but quoted corpus wording may incidentally reveal coverage/version. Do not add author conclusions to the packet.

For one **completed real run** (unexecuted/prepared/failed runs are refused):

```bash
python3 validation/agent-utility/harness.py packet   --run validation/agent-utility/results/model-cohort-01/AU-01-v1.json   --out validation/agent-utility/evaluator-only/packets/neutral-001.json   --template validation/agent-utility/evaluator-only/evaluations/neutral-001.json
```

Give only the neutral packet to the evaluator. The template is deliberately **not a valid completed evaluation**: unset raw scores, empty rationales and false independence/blinding flags must be filled honestly. Preserve provenance hashes. Fill each dimension's raw ordinal, rationale, exact response excerpts and/or omitted finding IDs; specify triggered failure IDs with exact quotes and explanations. `effective_score` is required by the schema but may initially equal raw; the harness computes caps deterministically. For no-Atlas, retrieval raw/effective are null and rationale contains `not_applicable`. The frozen keys are a semantic checklist, not a mandatory wording or algorithm. Honest corpus gaps earn credit where reasoning warrants it. Trigger a failure only when endorsed, not when a response describes a dangerous baseline for rejection.

After the independent evaluator completes the JSON:

```bash
python3 validation/agent-utility/harness.py score   --run validation/agent-utility/results/model-cohort-01/AU-01-v1.json   --evaluation validation/agent-utility/evaluator-only/evaluations/neutral-001.json   --out validation/agent-utility/results/scored-cohort-01/AU-01-v1.json
python3 validation/agent-utility/harness.py validate   --kind score --file validation/agent-utility/results/scored-cohort-01/AU-01-v1.json
```

Repeat packet/evaluator/score for all completed real run records; retain disagreements separately, never overwrite. The executed package already contains 25 scored paired responses and eight scored no-Atlas responses — see [EXECUTION-STATUS](results/EXECUTION-STATUS-2026-10-13.json). Existing result destinations cannot be reused. Then:

```bash
python3 validation/agent-utility/harness.py report   --runs validation/agent-utility/results/model-cohort-01   --scores validation/agent-utility/results/scored-cohort-01   --out validation/agent-utility/results/scored-report-01.json
```

Report every scenario, per-dimension raw/effective scores, critical failures, read costs, failed/unexecuted/unscored attempts and provenance. No sums/means/weighted winner or improvement claim can be inferred from fixture tests. Mechanical score validation proves structural/provenance/quote/cap consistency, **not semantic evaluator correctness**. Report uncertainty; a single exploratory seed is not significance evidence.

To reproduce the first-completed comparison from the existing results, with full score/quote/provenance/cap validation and no model calls:

```bash
python3 validation/agent-utility/summarize_results.py --out validation/agent-utility/results/comparison-repeat.json
```

Use a fresh output path. The [comparison JSON](results/comparison-2026-10-13.json) retains all attempts, selected rows, dimension distributions and source-report hashes; no overall aggregate is calculated.

## Frozen paths and SHA-256 anchors
`freeze-manifest.json`: **`bd2e57dc2d96f40fb65a6fd4ac2d9a5e6000411b91a5dc1ca47071a8bed3104c`**.

Original baseline **sorted mapping** SHA-256: `22e9bbeea8ac2b56e94e8e5b22df534e81fb103da3fcf3ab0769042b50a4403b` (computed from `json.dumps(mapping, sort_keys=True)`, not the original file bytes). Original manifest-file bytes and every benchmark file are listed below. Shipped v1 corpus manifest SHA-256: `e1ade517e405ac79fa93bc700dfe098848a1517dcbecf81080e307d2b30b8772`.

| Frozen path relative to this directory | SHA-256 |
|---|---|
| `baseline/atlas-v1-baseline-hashes.json` | `d0de61cdea6e2667ad6192d5c3afd7743bdef981a84979086c071773e33ab67c` |
| `evaluator-only/keys/AU-01.json` | `a9dc01bd3044670d685ed911842c9f84dcc922ca4b26334d2ac976925a687ee8` |
| `evaluator-only/keys/AU-02.json` | `50a7fc6c655cd247423cdfacf0b1e65ba29a2c41c1ccab0ddaefa5a0f08fc739` |
| `evaluator-only/keys/AU-03.json` | `1a3be15681225e139f63f60e4f9826b944f2327c37c5062e1c2f7e2608b9de32` |
| `evaluator-only/keys/AU-04.json` | `564c656996c3f41683f1141a79b1611f2cff0b58ab10972e0bf9228806cca53e` |
| `evaluator-only/keys/AU-05.json` | `6e0045fef4a3f0dbded64265d2256e03ab3377d6dea5f7b48b415decd3e5f24b` |
| `evaluator-only/keys/AU-06.json` | `26f44ec9e51f5de960f5a751a437c1534b2fef2a58c4c9973fcfdeefd86c5245` |
| `evaluator-only/keys/AU-07.json` | `84e75987cd1465ea96ee419305eaeb8a909c1b75f02835c7f0100d2e99594e18` |
| `evaluator-only/keys/AU-08.json` | `6d74d08ce5cf71aa3aee2525e665879e22602c7ccad9ad9b16b267f6ac4f17a5` |
| `evaluator-only/rubric.json` | `59055379b39284fbcc301a83aa2166a24ae6315880a08b7643db9af78227fb1a` |
| `inputs/AU-01.json` | `57b8ebfbbaeafdaa2b359014b22f4b219a1af3ec6e757a558e0283c9daba48ef` |
| `inputs/AU-02.json` | `21b1d61b1332bd01a8688573b0c866e00d3c0c71485922109bb1fd2658a1f6ea` |
| `inputs/AU-03.json` | `fe8ecd951a44399a61934e1445837929b6c58a685408f8cdc7fbe8ba24c98d1c` |
| `inputs/AU-04.json` | `146d3d26b4d09370609e95c6b4c19f6a5bdd5ec0cb5adeee9a01a7fb6ac79de8` |
| `inputs/AU-05.json` | `eb8675f40d0342b07ddad0c52587670e23dcbd6744e19637f0feccba197e6727` |
| `inputs/AU-06.json` | `d9bc0039aa97473b6c2c57d1d5e8ac075930960a53a0d25c1106bed35c659b82` |
| `inputs/AU-07.json` | `6477f23f3b3e34d3fe06a722f7ed3f3f9400847e777a4b690556ef26efa09118` |
| `inputs/AU-08.json` | `8e2df91a6a295fe455fcf3d30c4e6d7edeca0b087f6c97a54d55032718e7cb98` |
| `prompt.txt` | `a9d81edd52d51ee8bfd2f228daade2cc99f8bf288b3d80bd97096a1076e0ae15` |
| `protocol.md` | `809f8e2bacd3d2bb5bfc1478827e4f4dd578f4030f7afe383deb53a91986fd5e` |
| `schemas/result.schema.json` | `3505db81cd6d472587f6f4f4e95faf9285878e9f1d3d7d0238fc91fc8f0b0d26` |
| `schemas/scenario.schema.json` | `1642132e519235769e5ed7bbfb75218cdb8d69b93aad2503f62994749b1457e8` |
| `schemas/score.schema.json` | `6ecf6ee9806a1b62277e86642a0eff204ae3040a36d144e321ee9a7bb6ddab4c` |
| `settings.json` | `c3e0e073aa1960624c790dcfb88f920322b2ee406f83a6bdbbbcba09a965b535` |
