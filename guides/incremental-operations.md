# Incremental ER: operational boundaries and repair witnesses

## Ownership and simple comparator

Use [AR-06](../architectures/incremental-continuous.md) for identity lifecycle,
[master representation](../decisions/master-representation.md) for ID policy,
and [artifact runs](../solutions/architecture/versioned-artifact-runs.md) for
invalidation. This guide deepens operational stress cases without a second
identity theory or production protocol. Baseline: versioned current state with a
journal and scheduled history-qualified reconciliation. Alternative: selective
closure with checkpoints and event-derived state. No universal delivery or
cross-system atomicity guarantee is supplied.

## Proposal and publication contract

A repair proposal names accepted input/history boundary, observation revisions,
model/policy bundle, membership/ID base version, affected closure and unresolved
scope. Publication must reject a stale base or recompute/revalidate against the
new accepted state. Merely updating a timestamp cannot resolve a competing
correction. Single-writer serialization is a credible simple baseline; optimistic
version checks or scoped locks are alternatives with contention/retry costs.
Base/dependency validation and publication must share the same serialization or
atomic conditional-commit boundary; a check followed by an interleavable write
is insufficient. Include every relevant version/competitor dependency in that
boundary. If it cannot be established, hold or revalidate without claiming safety.
Declare scope: two disjoint record updates can still conflict through shared
assignment competitors, common frequency statistics or a merge proposal.

Record the committed membership, redirects, derived master versions and outgoing
correction intents together at the authoritative boundary where the storage
contract permits it. Outside that boundary, expose pending delivery and consumer
acknowledgment rather than promise instantaneous consistency. A durable intent
can survive a worker crash but does not guarantee exactly-once remote action:
consumer-side idempotency or reconciliation needs a separate agreed contract.
Reject same-delivery-key/different-payload conflicts. Do not replay external writes
as part of reconstructing internal state.

## Time and closure witnesses

| Witness | Required distinction/check | Failure interpretation |
|---|---|---|
| Late historical revision | Source revision versus valid time versus ingestion; rebuild affected as-of views | Last-arrival-wins can corrupt current or historical fields |
| Tombstone then stale update | Compare accepted source revision; quarantine incomparable revisions | A stale observation must not silently resurrect withdrawal |
| Delete a bridge | Repair old memberships and fields, not only new candidate edges | Removing an edge leaves materialized transitive state stale |
| Delete a top-k neighbor | Query updated index and previously unstored candidates; repair competitors | Stored-edge closure misses newly eligible replacement |
| Global frequency/source prior update | Invalidate all declared dependent scores, including unchanged records | Record-local closure is insufficient |
| Concurrent merge and split review | Validate both proposals against committed base and authority | Disjoint-looking actions can produce incompatible membership/IDs |
| Base changes after validation, before commit | Conditional commit/serialization must reject the now-stale proposal | A prior version check alone leaves a race |
| Crash after local commit, before acknowledgment | Inspect committed state and pending intent; reconcile without blind replay | Local rollback cannot undo an already delivered external effect |
| Out-of-order distinct-key deltas | Apply declared version/sequence precedence; reject/quarantine stale/conflicting deltas and detect gaps | Deduplication alone permits old corrections to overwrite new state |
| Partial merge/split publication bundle | Keep pending until membership, redirects and derived views are coherently applied | Receipt acknowledgment is not consistent downstream adoption |
| Backlog and rebuild overlap | Name index visibility, snapshot boundary and updates incorporated | Mixed epochs omit or duplicate effects |
| Retention/erasure before replay | Remove withdrawn inputs/derived copies under current authority | A historical snapshot may be unauthorized to restore |

Uncertain time, unknown revisions, infeasible constraints and incomplete closure
remain explicit states. Corrected replay reconstructs revised conclusions;
historical replay reconstructs what was known/published then, if retained evidence
and permission allow. Neither is ground truth. Record withdrawal, source purge
and real-world entity cessation are not equivalent.

## Reconciliation and downstream effects

Choose full replay when closure cannot be justified or a global change invalidates
most products. Reference histories, initial ID state, versions and tie/order
semantics must match the claim. Do not initialize the comparator from the derived
state under test. Compare membership equivalence, field provenance and exact ID
continuity separately. A split may require one-to-many historical resolution,
not a single redirect; master values must be rebuilt over the new memberships.

Consumers need entity version, delta sequence, redirect/split semantics and permitted
as-of references. Distinguish received, durably accepted and coherently applied
acknowledgments; the last names the consistently applied entity/view version.
Require declared version precedence, rejection/quarantine of stale or conflicting
deltas and detection of sequence gaps, including different delivery keys. Partial
bundles stay pending rather than acknowledge consistent adoption. Track lag and unresolved external
compensations. A consumer still reading an old authorized version is distinct
from one silently mixing memberships and master fields. Current access and
retention policy govern compensating corrections and rollback.

## Evaluation and stopping

Write conditional witnesses under [behavioral evaluation](../evaluation/synthetic-metamorphic.md);
compare full versus selective repair and cold/update/recovery cost with
[EVAL-11-007](../evaluation/execution-cost-replay.md). Evaluate actual identity and
attribute harms on independently adjudicated temporal snapshots, not replay
agreement alone. Predeclare freshness, backlog, correction-cost and safety
margins from consumer requirements. Contract violations reject the boundary;
unknown dependencies, unavailable history or uncertain consumer effects block
an equivalence/safety claim and favor a bounded hold or wider authorized repair.
These are written test designs, not executed ER fixtures or a deployment approval.
