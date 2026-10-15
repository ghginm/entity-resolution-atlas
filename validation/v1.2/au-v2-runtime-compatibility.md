# AU-v2 runtime compatibility review — execution remains blocked

## Scope and evidence

This is an operator/maintenance report, never solver corpus knowledge. A separate
read-only tooling critique was followed by integrating-author inspection of the
listed code/contracts and synthetic schema probes. The critique's model identity
is unattested; this is not independent model certification. Neither reviewer opened
scenario inputs, evaluator-only instances, keys, responses or scoring results.
No provider request, runtime integration or benchmark response was produced.

The frozen AU-v2 data package remains verified against anchor
`22d2527c35b39e1f22a0ac5815c833924815b63cbd1704a958989f124c798f49`.
Data preparation is complete; execution eligibility is not. Old AU-v1 source,
freeze/corpora/results and all other protected files remain unchanged. The
[readiness validation](au-v2-runtime-readiness-validation.json) records actual
utility probes, fresh lint/freeze checks and byte comparisons after this report.

## Verified compatibility gaps

Paths/line references are repository-relative code evidence, not literature claims.
These gaps describe reuse under the new frozen contract, not defects that invalidate
historical AU-v1 results or requirements to rewrite its preserved implementation.

| Boundary | Current implementation | AU-v2 requirement / consequence |
|---|---|---|
| Cohort binding | `validation/agent-utility/harness.py:7–12,368–387,478` binds root, anchor, IDs, input paths and result schema to AU-v1 | AU-v2 cannot use `run_scenario` unchanged or by merely redirecting one CLI path; global monkeypatches do not establish independent provenance |
| Broker | `harness.py:274–326` invokes the old corpus validator, expects old budget names, and returns `content/error/remaining` | New frozen contract requires `text/returned_characters/content_sha256`, separate `read_denied`, different field names and complete attempt accounting |
| Transport accounting | `adapters/hermes_cli_jsonl_adapter.py:347–362` corrects invalid/oversized reads before the broker and redirects depleted budgets toward a final | Such attempts are absent from broker counters; the new attempt accounting/fail-closed rule is not preserved by unchanged reuse |
| JSON/schema subset | `harness.py:23–24,43–79` uses ordinary JSON parsing and an intentionally limited old subset | It does not reject duplicate keys, implement `number`, or enforce `maxItems`/`uniqueItems`; use explicitly anchored AU-v2 strict parsing/schema primitives for its records |
| Ready identity | `adapters/hermes_cli_jsonl_adapter.py:249–262` constructs identity from requested provider/model/PID before transport response | Requested strings and process IDs do not attest the actual model/version or author/evaluator independence |
| Returned identity | `adapters/hermes_cli_jsonl_adapter.py:149–150,298–303` reads `system/init.model`, rejects a present mismatch but permits absent evidence | Init echo/missing evidence is insufficient for AU-v2's actual-identity/version gate; reject fallback or missing trusted evidence |
| Evaluator identity | `adapters/evaluator_runner.py:94–97,136–139` derives a label from CLI arguments and permits provider-default selection | Cannot register attested distinct actual evaluator identity/version from this label |
| Generation settings | Adapter ready metadata lists temperature/seed/output-limit enforcement as unavailable and supplies no `top_p` evidence | Frozen registration requires evidence/limits for each setting and comparable cross-arm defaults; null preparation values are not registration |
| Evidence retention and containment | `harness.py:401–403` discards stderr; adapter transport at `:168–174` starts a separate session | Exact trusted protocol/transport evidence must be retained; killing one process group alone does not prove descendant cleanup |
| Schedule and artifacts | AU-v1 CLI at `harness.py:681–710` accepts old labels/paired paths and artifact kinds | Map the frozen three-arm order, registration/run/packet/score contracts explicitly; renaming IDs or dimensions is not valid integration |

The exact required behavior is in the frozen
[AU-v2 protocol](../agent-utility-v2/protocol.md),
[settings](../agent-utility-v2/settings.json) and
[registration schema](../agent-utility-v2/schemas/registration.schema.json).
No frozen file is edited to make an old adapter appear compatible.

## Bounded reuse, not a second runtime

- `harness.py:329–360` provides bounded JSONL reading, deadlines and partial-line
  handling; `:19,82,86` provide hashing, serialization and exclusive artifact writes.
  Distinguish original file-byte hashes from reserialized-object hashes.
- Existing broker accounting and subprocess lifecycle are design/code reuse targets,
  not ready AU-v2 entry points. A future compatibility layer must demonstrate a
  dependency-binding seam and all changed semantics rather than clone a scheduler
  and call it reuse. No such seam or bridge is implemented in this continuation.
- Scoring/blinding mechanisms may guide explicit adaptation, but frozen AU-v2
  packet/score/provenance/applicability contracts need their own conformance checks.
  No real response exists to score.

## Execution blockers and responsible next decision

1. A tested compatibility seam/bridge is absent. Keep new integration files outside
   both protected trees; if safe reuse requires modifying protected AU-v1 source,
   obtain explicit scope authorization rather than alter it or build a second runtime.
2. Equivalent immutable baseline/expanded/empty inventories and leakage review are
   absent. Preregister the comparator and identical export policy before responses.
3. Actual tested/evaluator identities and versions, applicable author/evaluator
   conflict evidence, signed evaluator declaration, fresh-context/tool-registry and
   generation-equivalence evidence are absent. Configuration aliases, requested
   models and an author self-report cannot resolve those facts.
4. Do not call models until all execution gates have evidence. The old HTTP 402
   history is not a newly tested provider blocker; no paid-model probe was made here.

Next implement synthetic, no-provider conformance checks at an independently reviewed
existing-runtime binding seam, then register eligible transport identities/settings
and corpus snapshots before a full counterbalanced cohort. Tests must cover ready
ordering/mismatch, attempts and budget exhaustion, strict JSON/paths/hashes,
post-final output, exit/timeout/descendant cleanup, retained raw evidence,
three-arm scheduling and exact score provenance/caps. Synthetic transport fixtures
remain infrastructure evidence, never model outcomes. If identity/settings evidence
cannot be obtained, retain the blocked status instead of weakening the frozen protocol.

**Result:** documentation and AU-v2 data integrity are checked; runtime unimplemented,
registration absent, actual AU-v2 runs = 0, scores = 0, utility improvement unestablished.
