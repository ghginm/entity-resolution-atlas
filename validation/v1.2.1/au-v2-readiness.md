# AU-v2 runtime readiness — v1.2.1 recheck

**Continuation:** [Wave 4 runtime boundary report](wave-4/README.md) records fresh
process probes, the unresolved buffered-deadline failure, frozen dependency
constraints and current pilot gates. The earlier checkpoint below is retained;
neither checkpoint establishes an eligible model executor or independent evaluator.

## Actual state

No AU-v2 solver/evaluator run, provider probe, registration or score was created.
Frozen AU-v2 and AU-v1 bytes remain unchanged. The new workflow evaluation is a
separate frozen offline package, not an AU-v2 modification or an eligible runtime.

The host has `hermes` at `/home/ghgin/.local/bin/hermes` and `codex` at
`/snap/bin/codex`. Executable presence is **not** evidence of compatible protocol,
actual backend model/version, generation settings, fresh broker-only context,
credits, trusted identity or independent evaluation. No credentials were read.

## Existing executor and smallest valid integration boundary

The existing AU-v1 `harness.run_scenario` is executable and its synthetic fixtures
pass, but it binds the old case/prompt/root/schema and corpus contract. Its CLI
accepts old arms and adapter argv/settings, not an injected AU-v2 scenario/provenance
or a complete protocol/broker/lifecycle binding. The old process path discards
stderr and uses its own identity/protocol expectations. Merely pointing it at a
new snapshot cannot satisfy the frozen AU-v2 contract.

The AU-v2 bridge supplies tested broker/state/schema/snapshot/registration seams;
its Session does not spawn processes or enforce OS lifecycle deadlines. New AW
Broker independently reuses the old read method, not a copied executor. Neither
constitutes a working AU-v2 or AW process runtime.

The smallest sound next engineering change remains an explicitly reviewed shared
executor binding: preserve AU-v1 behavior and original source bytes, inject the
case/prompt/protocol/broker/artifact handling at a documented seam, retain raw
sent/received/stderr evidence, and test startup/partial-line/initial/final/wall and
descendant behavior using real synthetic processes. Do not clone the scheduler or
relax frozen inputs. Existing protected runtime modification has not been explicitly
authorized; the current task forbids changing protected artifacts just to erase a
failure. That boundary was respected.

Even a compatible executor cannot authorize a real pilot without trustworthy
actual solver/evaluator version, effective settings, zero-tool/fresh-context and
conflict/independence evidence. A current author/subagent cannot self-score the new
knowledge or workflow material as an independent evaluator. Requested CLI strings,
PID and init echoes are insufficient. No model-access failure is inferred from
historical billing incidents; access was not retested.

## Re-executed evidence

- [AU-v2 integrity](au-v2-integrity.json): external frozen manifest anchor preserved.
- [AU-v2 package suite](au-v2-tests-corrected.txt): 17 tests pass. Initial discovery
  at the package root collected no tests and exited 5; corrected to its `tests/`
  directory. No package test was edited.
- [Existing integration/scoring suite](integration-tests.txt): 65 tests pass.
- [AU-v1 infrastructure suite](au-v1-tests.txt): 39 tests pass, including the
  original 0.5-second fixture assertion. Existing unclosed-pipe ResourceWarnings
  are retained rather than suppressed.
- AW offline verification and 12 tests pass separately; its 32 planned cells are
  unexecuted, not AU-v2 results. The old 24-cell AU-v2 plan is unchanged.

Tests establish their particular synthetic infrastructure contracts, not trusted
model identity, independent semantic scoring or measured utility improvements.

## AU-v1 0.5-second subprocess diagnostic

[Reproducible diagnostic](diagnose_subprocess.py),
[actual trials](subprocess-timing.json): five successful synthetic fixture runs at
0.5 seconds and five at a 2.0-second **diagnostic comparator**, zero failures;
maximum observed whole-call elapsed time 0.028399 seconds. Whole-call timing also
includes freeze/corpus/setup overhead, not only child startup.

The earlier timeout was **not reproduced** in this bounded run. This does not
identify scheduler latency as its cause or rule out environmental flakiness.
Protected assertions/deadlines/source were not changed. If it recurs, retain the
original failing run under comparable load and instrument time-to-spawn,
time-to-ready, protocol exchange and exit separately in an authorized diagnostic.
A minimal proposed test-only fix would separate logical protocol assertions from
an environment-tolerant success deadline while retaining dedicated explicit timeout
fixtures. That is a proposal, not an applied change or weakened test.

```sh
/home/ghgin/.hermes/cache/scratch/atlas-v11-qa/bin/python -B validation/v1.2.1/diagnose_subprocess.py --output NEW_TIMING_REPORT.json
```

## Resume without inventing a run command

Read the unchanged `validation/v1.2/au-v2-remaining-work.md` and the current
`validation/agent-workflow/README.md`. Obtain explicit protected-executor refactor
scope only if that path is selected, then separately verify the trusted transport
and independent evaluator. Until then, run only verify/tests/plan/report; neither
new package exposes a working/eligible model `run` command. No fabricated result,
new model platform or unauthorized production change substitutes for this blocker.
