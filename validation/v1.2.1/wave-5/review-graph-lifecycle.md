# Wave 5 targeted scientific review: graph constraints and identity lifecycle

## Outcome and scope

**One demonstrated insufficient-condition claim needs correction; no other scientific error demonstrated in this bounded review.** Two lower-priority clarifications are distinguished below from that finding. No canonical correction was made.

Read `MAINTAINERS.md` and `references/evidence-policy.md` first, then `START_HERE.md`. Reviewed canonical connected-components, constrained-clustering, temporal-identity, incremental-continuous architecture, incremental-operations, identity-semantics and master-representation/resolution decisions; graph/incremental task routes; and `evaluation/{entity-resolution-quality,synthetic-metamorphic,execution-cost-replay}.md`. Paths below are repository-relative; line numbers refer to the reviewed text.

No benchmark scenarios, keys or results were opened. A broad filename-only discovery search initially returned frozen-corpus/snapshot filenames; none of their contents were inspected or used. Existing experiment review and snapshots were not edited. Only this report and its uniquely named mathematical check files were written. No commits, pushes or production actions.

## Demonstrated finding

### GL-1 — Disjoint validity plus single occupancy does not imply different enduring entities (medium; semantic hard-veto risk)

**Location:** `solutions/decision-resolution/constrained-clustering.md:46`, in the examples of trustworthy impossibility: “disjoint validity periods under a single-occupancy contract.”

**Countermodel:** one enduring person occupies address A during `[0,1)` and address B during `[1,2)`. There is at most one occupied address at every instant. The validity intervals are disjoint, the single-occupancy contract is satisfied, and both observations still refer to the same person. Thus those premises alone do not imply a cannot-link. The executed `disjoint_validity_single_occupancy_countermodel` check verifies these conditions. This is a logical insufficiency in the stated example, not evidence of a deployed implementation bug.

**Consequence:** promoting that example to a hard veto fragments legitimate histories. The wording conflicts with the more careful local explanation in `solutions/identity-semantics/temporal-identity.md:45,71`, which permits movement and warns against treating simultaneous differences as impossible without a trusted contract.

**Small correction recommended, not applied:** replace the example with “overlapping known validity intervals asserting mutually exclusive states under an audited single-occupancy invariant.” Require comparable state types, actual overlap and a genuinely invariant exclusivity rule. If disjointness was intended to distinguish registration episodes rather than enduring objects, state that separate identity target explicitly. Merely swapping the interval word without these assumptions would also overclaim.

## Clarifications, not additional demonstrated errors

- **Soft signed labels versus hard admissibility:** `solutions/decision-resolution/constrained-clustering.md:28` uses correlation clustering to motivate “label-based admissibility.” The checked source describes maximizing agreements/minimizing disagreements, not mandatory satisfaction of all labels.[12] An inconsistent signed triangle `+ab,+bc,-ac` has minimum disagreement one across all five partitions. The card correctly separates soft objectives from hard feasibility at lines 40 and 52; therefore this is a terminology/source-scope clarification, not a claim that the card's objective is wrong. Prefer “partition-level signed-evidence objectives” at line 28, using source 37 for hard restrictions.
- **Must-link initialization:** `solutions/decision-resolution/constrained-clustering.md:36–38` permits starting from singletons before sorted candidate merging. The explicit output contract at line 28 still requires every must-link. Clarify that singleton initialization is allowed only if mandatory must-link closure is enforced independently of candidate availability/utility before optional merges. Otherwise a missing candidate between two must-linked records could leave them separate. This is an underspecified construction path, not a demonstrated contradiction when the card is read as a whole.

## Executed finite challenges

Command: `python validation/v1.2.1/wave-5/check-graph-lifecycle-review.py`.

**Actual execution:** exit 0; 16 check records, zero assertion failures. Output: `check-graph-lifecycle-review.output.json`. These are independently constructed finite mathematical witnesses, not tests of an Atlas matching implementation or sampled ER outcomes.

| Challenge and observed result | Reviewed claim / interpretation |
|---|---|
| All 64 simple graphs on four vertices; reversed edge order gives identical partitions; all 192 individual edge removals only refine connectivity | `connected-components.md:36,72,78`; finite confirmation, not a complexity benchmark |
| Bridge between sizes 3/3 produces 9 false pairs; sizes 20/30 produces 600, including the bridge pair | `connected-components.md:46`; `constrained-clustering.md:42` counting claims survive |
| Removing one triangle edge leaves connectivity; removing one chain edge splits it | `connected-components.md:56,78`; repairing one witness path is insufficient when alternatives remain |
| True three-record chain has two bridges; wrong six-record clique has none and nine false pairs | `connected-components.md:50`; `entity-resolution-quality.md:62`; bridge count is not accuracy |
| Must ab, must bc, cannot ac has zero feasible partitions; cannot ac and cannot bc permits ab | `constrained-clustering.md:52,64`; must-link closure and cannot-link nontransitivity survive |
| Cannot ac blocks union `{a,b}` with `{c}` despite allowable endpoint bc | `constrained-clustering.md:36`; whole-union checking is necessary |
| Capacity-two example: sorted ab=10 blocks ac=9 and bd=9; feasible optimum 18 versus greedy 10 | `constrained-clustering.md:68`; feasibility is not optimality or identity truth |
| Two coherent partition distributions have AB=BC=0.9 but all-three identity probabilities 0.8 and 0.9 | `connected-components.md:44`; edge averages/minima/product 0.81 cannot generally supply cluster confidence |
| Deleting stored top-1 b reveals previously unstored c; stored-edge filtering returns nothing | `architectures/incremental-continuous.md:64`; `incremental-operations.md:45`; old graph closure misses replacement retrieval |
| Tombstone revision 2 then live revision 1: last arrival is live but source precedence retains deletion | `architectures/incremental-continuous.md:72`; stale delivery is not reinstatement |
| Old-valid address arriving last differs from valid-current address | `temporal-identity.md:39–47`; valid time and ingestion projections differ |
| Version check succeeds at version 1; concurrent version 2 makes the subsequent write stale | `incremental-operations.md:22–25`; check and publication need one conditional/serialized boundary |
| Old two-member ID splits into two children; membership recovery supplies no unique redirect target | `architectures/incremental-continuous.md:78`; `master-representation.md:43`; lineage and identity continuity require separate policy |

## Primary-source verification

Checked primary full-text passages through `web.run`; existing source IDs below are reused without changing the ledger. “Full-text” denotes access to the document and inspection of the named sections, not a claim to have audited every page.

- **[12], sections 2.1.1 and 2.3:** connected components and chaining warning; signed-label agreement/disagreement objective. These support the bounded mechanisms, not a general hard-constraint guarantee.[12]
- **[37], sections 2.1–2.3/Table 1:** must/cannot constraints, COP-COBWEB and whole-cluster checks; the consistency assumption is explicit. The card correctly avoids confusing this with COP-k-means.[37]
- **[14], accessed PDF dated October 11, 2021:** the multifile-representation and partial-estimate passages support file-specific duplication structure and unresolved/partial partition estimates. They do not validate the Atlas sorted-merge heuristic.[14]
- **[10], introduction/query formulation:** adaptive query-time collective resolution over publication references, not a general continuously maintained identity-store guarantee. AR-06:27 preserves that limitation.[10]
- **[28], “External Updates,” “External Queries,” and “Code Changes”:** replay can repeat external writes, and historical query results/code semantics matter. AR-06:42–46,84 accurately limits this to architectural support, not measured ER performance.[28]

Publisher-hosted/author-hosted PDFs and the arXiv PDF resolved the checked claims. No retrieval blocker, new source ID or ledger edit was needed.

## Evaluation-route assessment and limits

The routes reach appropriate mechanisms and estimands: entity harm and independent labels (`EVAL-11-003`), conditional behavioral witnesses with execution/oracle coverage (`EVAL-11-006`), and history-qualified completion/cost comparisons (`EVAL-11-007`). Their reviewed warnings distinguish topology from truth, fixed snapshots from path-dependent replay, stable IDs from partition labels, and local publication from consumer adoption. No numerical cost, accuracy or utility superiority is established here.

Not reviewed: population estimation derivations, all external sources in the evaluation cards, real data, distributed fault injection, performance, source-ledger-wide consistency, global structural validation, frozen-input hashes, or benchmark utility. The finite closure routine is a tiny relation-composition oracle, not an implementation/performance test of the traversal bound. The concurrency and time witnesses are simplified countermodels, not operational tests. Absence of further findings is not proof of corpus correctness. This report does not reopen or supersede the existing experiment review.

## Sources

[10] https://cdn.aaai.org/AAAI/2007/AAAI07-255.pdf — Online Collective Entity Resolution
[12] https://www.vldb.org/pvldb/vol2/vldb09-1025.pdf — Framework for Evaluating Clustering Algorithms in Duplicate Detection
[14] https://arxiv.org/abs/2110.03839 — Multifile Partitioning for Record Linkage and Duplicate Detection
[28] https://martinfowler.com/eaaDev/EventSourcing.html — Event Sourcing
[37] https://wkiri.com/research/papers/wagstaff-constraints-00.pdf — Clustering with Instance-level Constraints
