# AU-v2 mechanical scoring — bounded critique and dispositions

## Authority and evidence limits

A separate read-only critique returned two P2 findings in delegation
`deleg_1d10cd27`. Its model identity is unattested; this is not certified independent
review. The reviewer used isolated synthetic seams and did not invoke providers,
change files or inspect original case/key/prompt/result contents. Integrating-author
follow-up used the existing synthetic fixtures and actual byte-pinned parser/broker.
No independent post-remediation sign-off, semantic certification or benchmark
outcome is claimed. Original review-time [validation](au-v2-scoring-validation.json)
is retained; [post-review validation](au-v2-scoring-post-review-validation.json)
records the corrected implementation and rerun checks.

## P2: registration evidence guarantee exceeded the scoring boundary

**Finding:** schema, supplied registration byte hash, selected snapshot and declared
journal hashes do not establish evidence-file/executable bindings. Scoring did not
invoke `bridge.validate_registration`. Changing a tested-model version/runtime
hash while retaining old evidence could survive structure/replay checks. The
statement that new evidence was enforced was too strong.

**Disposition:** clarified in [SCORING](../agent-utility-integration/SCORING.md#completed-run-admission-and-replay).
The operator must separately run the existing registration checker against all
three immutable snapshots, actual runtime/adapter files and model/generation
evidence, retain its result and link it to exact registration bytes. The checker
returns a canonical-registration hash, not automatically the original file-byte
hash; both must be retained. Scoring itself does not load those files or enforce
that external prerequisite. Signature truth and eligibility remain independent
checks. Future executor admission must enforce the prerequisite rather than infer
it from a schema-valid declaration. No second evidence system or frozen schema
change was introduced merely to claim this gap closed.

**Additional concrete invariant fixed:** the critique identified
`enforcement=unsupported, effective=0.5, limitation=""` admission. A focused test
`test_packet_rejects_unsupported_setting_with_effective_value` failed with
`IntegrationError not raised`, then passed after requiring a null effective value
and nonempty limitation for every unsupported generation setting in scoring.
This is a local consistency check, not an evidence-file check or proof of settings
being enforced. The external evidence/executable prerequisite remains unresolved
in the automatic runtime path and blocks real dispatch.

## P2: recursive nonfinite validation bypassed replayed adapter messages

**Finding:** the new finite-number parser checked run/registration/journal JSON,
but journal `raw_hex` hid decoded adapter JSON until Session passed it to the
unchanged original strict loader. A malformed read containing an extra
`overflow:1e999` could be denied by the broker yet counted in a completed replay.
The reviewer source-confirmed the bypass but requested real dependency confirmation.

**Disposition:** confirmed and fixed. The new regression
`test_packet_rejects_nonfinite_replayed_read_even_when_broker_denies_it` uses the
actual pinned strict loader, broker and existing synthetic context. It embeds
exponent-overflow JSON in the read event, reconstructs actual broker denial bytes,
reconciles run/journal hashes and clears the successful read log. After correcting
an initial test-setup omission of Broker's required manifest hash argument, the
focused test failed with `IntegrationError not raised`. Adding recursive finite
validation of every `received` frame before Session handling made it pass.
Ready/read/final ordering and Session's line/byte checks still apply. No bridge,
frozen verifier or historical file was edited; the protection applies to scoring
replay, not all other users of the old strict loader.

## Verification and residual acceptance

Both focused tests passed; the full integration suite then passed 65 tests.
Fresh Atlas/legacy/package/lint/citation/freeze/hash outputs are recorded in the
post-review validation rather than retroactively substituted into older reports.
The code repairs and narrowed documentation address the returned findings only
within the stated boundary. Actual registration eligibility, shared process
executor/transport, independent evaluator invocation and measured utility remain
unfinished. Actual AU-v2 runs/scores are zero. No commit, push or production action.
