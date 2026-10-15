# AU-v2 mechanical blinded packet and score tooling

`scoring.py` is trusted evaluator-operator infrastructure, not an agent runtime,
model evaluator, solver tool or Atlas knowledge. It does not assign raw scores,
call providers, prove independence or authenticate signatures. Real execution and
independent evaluator eligibility remain prerequisites. Synthetic unit/CLI fixtures
live only in configured scratch and are never benchmark results.

## Completed-run admission and replay

Before loading a case's evaluator-only key, the builder requires a schema-valid
completed run with nonempty response, exact UTF-8 response hash, no failure, actual
identity-attested flag, registration file-byte hash and matching frozen
case/prompt/settings/manifest hashes. Registered tested/evaluator declarations must
be distinct. The selected corpus is externally anchored and its inventory binding
must match registration. Unexecuted/failed records cannot acquire private key material.

**Registration boundary:** this path checks registration structure/declarations,
the supplied registration byte hash, frozen provenance, the selected snapshot and
journal evidence-hash declarations. It rejects an `unsupported` generation setting
unless its effective value is null and its limitation is nonempty. It does **not**
load model/generation evidence files, hash runtime/adapter executables or invoke
`bridge.validate_registration`. Before any real use, the operator must separately
run the bridge's registration checker against all three pinned snapshots, actual
runtime/adapter files and the evidence directory, retain its result, and bind it
to these exact registration bytes. That result's hash is over canonical registration;
retain the source file-byte hash too. Changes to dependencies/model versions require
new evidence and a repeated operator check. This is an external prerequisite, not
an automatically enforced score-admission gate. Evidence/signature authenticity and
execution eligibility still require independent verification. A rehashed declaration
alone is insufficient even if this validator accepts its structure.

The journal is a separately retained operator artifact, not a new frozen run schema.
Its exact top-level keys are:

- `format`: `au-v2-execution-journal-v1`;
- `run_sha256`, `runtime_identity_evidence_sha256` and successful integer `exit_code`;
- timezone-aware `exit_observed_at`;
- `stderr_hex` and its UTF-8-independent byte `stderr_sha256`;
- `events`, each with exactly `direction`, `raw_hex`, byte `sha256`, and timezone-aware
  `observed_at`.

The first event is actual `sent_start`. That JSONL object has exactly `type=start`,
one frozen `scenario`, frozen `prompt`, `settings_sha256`, neutral `inventory` and
`read_file` equal to `scoring.READ_CONTRACT`. Type-sensitive comparison rejects
boolean/integer aliases and additional arm/provider/history/author context. Initial
Unicode-character budget and monotone observed times through terminal exit are
checked against frozen solver wall limits. These are recorded-time consistency
checks, not proof of a functioning OS timeout or trusted clock.

Subsequent adapter stdout events are `received`. Each read is replayed through the
existing broker binding against the immutable snapshot. Its next event must be
actual `sent_broker` bytes matching the computed reply. A `broker_generated` record
alone is not transmission evidence. Successful read excerpts are reconstructed
from source bytes, not trusted supplied text. Denied attempts remain in the private
raw journal and count toward attempts; the frozen run's `read_log` contains the
schema-representable successful excerpt records. Counters/logs must reconcile.
Ready/final ordering, no output after final and successful terminal exit are checked.

The scoring parser rejects exponent-overflow nonfinite numbers in its JSON inputs,
including every replayed `received` message before handing it to the unchanged
Session. This does not upgrade the parser of the protected bridge outside scoring.
The source package hash anchor and frozen operator-side payload reads are checked;
runtime/model evidence checking remains the external prerequisite above.

## Blinding and artifact boundaries

The evaluator receives only `packet.json`: scenario/task, exact response, authorized
read excerpts, read attempt/success/character counts, retrieval applicability,
matching key/rubric/frozen evaluator instructions and opaque required provenance
hashes. Generated arm labels, provider/model/adapter identities, timestamps, source
repository paths and author conclusions are absent. Retrieved content or response
self-disclosures can still reveal coverage/identity; perfect blinding is not claimed.

`private-receipt.json` binds run/registration/journal/packet and key/rubric/prompt
hashes plus operator-only arm and identity information. **Never send this receipt,
its whole directory, registration or journal to the evaluator or solver.** The
packet's own hash is supplied by the trusted router as neutral provenance metadata
outside its byte content; the receipt itself is not that metadata packet.

New bundle directories are exclusively created (mode 0700); files are mode 0600.
Symlink ancestors and output into either protected benchmark tree are rejected.
Partial I/O failures remain partial attempts; do not overwrite/reuse their directory.
Packet/draft/score examples are not delivered as fake results.

## Mechanical score validation

Only the frozen score schema is accepted. Provenance, registered evaluator identity,
independence/blinding declarations and timezone-aware evaluation-after-run timestamp
must match. Every quoted string is an exact response substring. Omitted findings
must be unique, exist in this case key and apply to that dimension. Applicable raw
scores are ordinal integers; empty no-Atlas retrieval is null with `not_applicable`,
never zero. Evidence/rationale cannot silently disappear.

Critical-failure IDs must be known, unique and case-scoped, with exact quote and a
nonempty endorsement explanation. The independent evaluator is responsible for
semantics: discussing/rejecting an unsafe baseline must not trigger a failure. A
program cannot prove endorsement from a quoted phrase. Effective scores are computed
only for explicitly affected dimensions as the minimum of raw and applicable caps;
there is no aggregate. Alternative credit is preserved, including defensible
choices outside the non-exhaustive key.

The original evaluator draft bytes remain in `evaluator-draft.json`. Normalized
`score.json` computes effective caps and appends the mechanical-validation limitation;
raw/rationale/quotes/IDs/alternative credit are not rewritten. `validation.json`
binds every input/output and the scoring implementation hash. Rejected drafts are
not replaced with invented scores. Semantic correctness, genuine independent
execution, clock/signature trust and containment remain outside this proof.

## Commands and actual evidence

```sh
python3 -B validation/agent-utility-integration/scoring.py --help
python3 -B -m unittest discover -s validation/agent-utility-integration/tests -p test_scoring.py -v
```

Operator interfaces (placeholders, not existing real run files):

```sh
python3 -B validation/agent-utility-integration/scoring.py packet --role evaluator-operator --run RUN_JSON --registration REGISTRATION_JSON --journal JOURNAL_JSON --snapshot SELECTED_SNAPSHOT --out NEW_PRIVATE_DIRECTORY
python3 -B validation/agent-utility-integration/scoring.py score --role evaluator-operator --run RUN_JSON --registration REGISTRATION_JSON --journal JOURNAL_JSON --snapshot SELECTED_SNAPSHOT --packet PACKET_JSON --receipt PRIVATE_RECEIPT_JSON --evaluation INDEPENDENT_DRAFT_JSON --out NEW_SCORE_DIRECTORY
```

The role argument is a declaration/accidental-use guard, not OS authorization or an
independence proof. There is no CLI fixture-context override. Tests inject explicit
synthetic contexts into the callable parser/writers; the actual CLI always uses the
anchored package. The author inspected schemas and synthetic fixtures only; the
package verifier internally checks original JSON structure/hashes without exposing
original case/key text to the author conversation.

[Actual scoring-wave validation](../v1.2/au-v2-scoring-validation.json) records executed
checks. [Review dispositions](../v1.2/au-v2-scoring-review.md) and
[post-review checks](../v1.2/au-v2-scoring-post-review-validation.json) record the
replay-parser repair and registration-boundary clarification, not independent
post-remediation certification. [Remaining work](../v1.2/au-v2-remaining-work.md) states scope/volume and the
unanswered executor-refactor authorization checkpoint. No real model response,
independent assessment or utility improvement is asserted.
