# v1.2.1 Wave 4 — AU-v2 runtime readiness and blocked pilot

**Bounded offline work completed; real execution remains BLOCKED.** This is
operator-only evaluation infrastructure, not consumer knowledge. No AU-v2 solver
attempt, provider-model probe, registration, evaluator invocation or score was
created. A synthetic pipe exchange is not a benchmark pilot or utility evidence.
Wave 5 scientific review is not included in this checkpoint.

## What changed

- Added [synthetic process boundary tests](test_runtime_boundary.py) outside all
  existing benchmark trees. They reuse the byte-pinned AU-v1 `LineReader` and
  existing AU-v2 `Broker`/`Session`; they do not implement a new executor, provider
  client, arbitrary-command dispatcher or cohort scheduler.
- Exercised real stdin/stdout pipes, repeated Unicode reads, a denied traversal,
  actual child receipt of broker bytes, non-UTF-8 stderr retention, ready ordering
  and identity mismatch, malformed/partial output, chunk/line/final bounds,
  output after final and unsuccessful process exit.
- Reproduced a deadline-boundary defect in the proposed legacy reuse primitive.
  Kept its strict assertion and protected source unchanged; the test is explicitly
  an expected failure, not a fulfilled runtime requirement.
- Retained fresh runtime discovery, regression logs, snapshot/freeze verification
  and before/after protected-file hashes. Historical benchmark plans and result
  artifacts were not rewritten; the earlier readiness note only gains a pointer here.

## Executor discovery and exact remaining seam

[Discovery evidence](runtime-discovery.json) records installed executable paths,
versions and actual `--help` output. Scope: `hermes`, `codex`, `claude`, `opencode`
on the current PATH, and the repository's existing Python subprocess call sites;
not an exhaustive search of every host program or remote runtime. Hermes and
Codex were present. Their CLI availability does not establish AU-v2 compatibility.
No credentials or profile configuration were inspected or changed. Provider
availability, credits and prices were not tested; historical billing failures
are not a current diagnosis.

Relevant unchanged source boundaries:

- `validation/agent-utility/harness.py:368–478`: `run_scenario` still binds AU-v1
  roots, frozen inputs, start/result schema, settings and broker directly. It is
  not an injectable AU-v2 executor. `stderr=DEVNULL` at line 402 discards evidence.
- `harness.py:329–357`: `LineReader.line` returns a complete buffered line before
  checking the deadline. The new strict probe fails with `BenchmarkError not
  raised` for a buffer containing a complete line and an already expired deadline.
  [Initial failing output](boundary-initial.txt) is preserved. This is a directly
  constructed reader-state counterexample, **not** an observed over-budget model
  run, and does not invalidate historical model results.
- `harness.py:461–465`: cleanup kills the adapter group only while the leader is
  alive. The existing adapter at
  `validation/agent-utility/adapters/hermes_cli_jsonl_adapter.py:168–174` starts a
  separate transport session. Source inspection therefore does not justify a
  full-descendant containment claim. No escaped-descendant experiment was run.
- That adapter's lines 249–262 declare ready from requested identity before
  transport evidence; lines 298–303 accept missing returned identity; lines
  347–362 correct/drop invalid or exhausted reads before broker accounting. These
  are incompatible with unchanged reuse under the frozen AU-v2 contract.
- `validation/agent-utility-integration/bridge.py:268–331` is a protocol state
  machine, not a spawn/write/timeout/containment implementation. Passing it bytes
  in tests does not implement the missing lifecycle.

**Additional frozen dependency constraint:** Wave 3's
`validation/agent-workflow/frozen/bindings.json` pins the exact legacy harness,
AU-v2 verifier and bridge bytes. `workflow.py:47–64` checks those dependencies on
operational entry. Editing the legacy harness in place would break that frozen
binding even if AU-v1 tests still passed. The selected AU-v2 preparation plan also
pins the bridge. Permission to refactor alone is not permission to re-freeze,
redirect imports, monkeypatch globals or overwrite historical source bindings.

The smallest *candidate* engineering boundary remains a reviewed shared process
execution seam, with scenario/protocol/broker/provenance supplied explicitly and
one owning deadline across startup, writes, reads, final and successful exit.
It must retain exact sent/received/stderr bytes, fail closed on every excess, and
contain the actual transport descendants. Before implementing it, explicitly
resolve source-version preservation and the frozen dependency closure above.
Use a separately authorized versioned integration/dependency design; preserve
old source paths/bytes and existing prepared cohorts. Do not copy the old scheduler
into a second runtime merely to evade this decision. No such compatible seam is
claimed to exist at this checkpoint.

## Actual evidence and limits

[Machine-readable test summary](test-summary.json) binds commands to complete logs.

| Executed suite | Outcome |
|---|---|
| New runtime-boundary suite | 12 tests: 11 pass, 1 expected failure (buffered deadline) |
| Unchanged AU-v1 infrastructure | 39 pass |
| Unchanged AU-v2 package | 17 pass |
| Unchanged integration/scoring | 65 pass |
| Wave 3 workflow | 12 pass |
| Documentation/navigation/package tooling | 59 pass |

The original AU-v1 0.5-second process fixture passed in this suite run. No protected
deadline/assertion was extended. Existing AU-v1 unclosed-pipe ResourceWarnings
remain visible in its log. This bounded repeat does not establish the cause of
an earlier intermittent timeout. The prior timing diagnostic remains available
in [the earlier readiness note](../au-v2-readiness.md#au-v1-05-second-subprocess-diagnostic).

[Synthetic pipe evidence](synthetic-pipe.json) contains the actual sent/received
frames and raw stderr hash/hex from a fixed Python fixture. The child reports the
exact stdin bytes it received; the test reconciles those with parent writes and
broker-generated replies. Three attempts produce two successful three-character
reads and one content-free denial. Repeated text counts twice. The start is
intentionally `synthetic_start`, not a frozen scenario. The artifact is marked
ineligible for scoring and is not a frozen-schema run or execution journal.

The fixture has a minimized environment and temporary HOME/cwd. Its five-second
reader deadline is a **test timeout**, not the frozen solver budget. Blocking test
writes are bounded fixture writes, not a production nonblocking writer. Fixture
cleanup handles its own process group; remote context isolation, malicious
adapters, escaped descendants, initial-context dispatch, end-to-end wall budget,
large stderr backpressure and authenticated actual model identity remain unproved.

[Verification](verification.json) confirms the externally anchored AU-v2 freeze,
the three selected inventories (52 / 79 / 0 files), Wave 3's frozen preparation,
and the unchanged source-bound consumer package (57 cards). The existing 24-cell
AU-v2 plan remains byte-identical and unexecuted. The separate workflow package's
32 planned cells remain unexecuted. [Protected integrity](protected-integrity.json)
compares the exact file inventory and hashes captured in [the before record](before.json):
AU-v1, AU-v2, integration, workflow, distribution and historical inputs preserved.
[Lint](lint.txt) covers links, generated navigation, manifest, citations and input
integrity; it is not a scientific review.

## Pilot gates and decision

| Gate | Current evidence / status |
|---|---|
| Frozen inputs, snapshots and existing plan | Reverified; preserved |
| Shared compatible executor | Missing; strict buffered-deadline probe remains red |
| Safe versioned dependency integration | Not authorized/designed; existing pins must remain valid |
| Actual solver and evaluator model/version | No registered trusted runtime evidence |
| Generation equivalence | No new effective-setting evidence or operator attestation |
| Fresh broker-only, zero-direct-tool contexts | Fixed synthetic fixture only; model runtime not attested |
| Evaluator independence and author conflicts | No eligible independent evaluator established |
| Raw end-to-end transport and descendant lifecycle | Partial synthetic evidence only |
| Pilot eligibility | **BLOCKED — do not dispatch** |

Do not turn the current chat's model/provider label, a CLI request, PID, init echo,
role string or hash of a declaration into backend-version or independence proof.
The author cannot supply independent semantic scores for its own work. A successful
mechanical registration check would still not authenticate declarations.

## Resume

Read-only commands from the repository root:

```sh
PY=/home/ghgin/.hermes/cache/scratch/atlas-v11-qa/bin/python
$PY -B -m unittest discover -s validation/v1.2.1/wave-4 -p test_runtime_boundary.py -v
$PY -B -m unittest discover -s validation/agent-utility-integration/tests -v
$PY -B validation/agent-utility-v2/verify.py --expected-manifest-sha256 22d2527c35b39e1f22a0ac5815c833924815b63cbd1704a958989f124c798f49
$PY -B validation/agent-workflow/workflow.py verify --prepared validation/agent-workflow/prepared/initial
$PY -B tools/atlas_consumer.py verify --output dist/atlas-consumer
```

The first command should report one expected failure until a separately authorized
compatible implementation exists. A test exit code of zero does **not** authorize
a model run. To retain another synthetic transcript, set
`ATLAS_WAVE4_EVIDENCE_DIR` to a new existing scratch directory; evidence files use
exclusive creation. Do not reuse this report directory or overwrite prior logs.

Next authorized independent work is Wave 5 scientific review/final validation,
without consuming frozen cases/keys/results or changing existing consumer snapshots.
To unblock runtime work, first approve a concrete versioned reuse design preserving
all frozen dependencies, then establish trusted model/settings/context/independence
evidence and registration. A future pilot must be separately identified from the
complete comparison cohort; preserve all attempts and the frozen full-cohort
recovery rule. There is no eligible model `run` command to provide yet.

No canonical card, generated route, frozen benchmark, legacy runtime, production
system, credential, commit or remote branch was changed in this wave.
