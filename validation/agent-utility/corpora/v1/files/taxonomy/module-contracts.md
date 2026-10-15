# Conceptual module contracts

These contracts describe knowledge-level artifacts, not APIs, code classes, a mandatory technology stack, or an executable pipeline. Carry raw observation provenance and component versions forward. A deployment may combine modules physically without erasing their responsibilities.

| Module | Input | Output | Invariant / question to settle |
|---|---|---|---|
| Intake/integration | Source observations, schemas, identifier namespaces and observation/validity times | Comparable typed observations plus raw references, validity/quality flags and mapping versions | Same named field need not mean same attribute; no silent conflict overwrites |
| Normalization/enrichment | Typed observations and locale/source context | Raw plus normalized/parsed/variant representations, transformation provenance and uncertainty | Lossy transformation must not replace the only evidence copy |
| Candidate generation | Representations, eligible pair definition, retrieval/index versions and budgets | Unique record pairs, source pairs, pass/routing provenance, retrieval reasons, omissions/caps | Canonical pair identity; absent candidate is unknown, not a known non-match |
| Comparison | Candidate pair and observation histories | Evidence vector, missing/invalid/conflict masks, source/time context, dependency groups, feature version | Separate absence from reliable contradiction; reveal shared provenance |
| Scoring | Versioned evidence and applicable trained/estimated/manual model | Score, score semantics, contributions, model version and conditioning population | A raw additive sum or LR is not automatically a calibrated posterior |
| Calibration | Scores plus independent representative calibration reference | Population-specific probability mapping and validity conditions | Changed retrieval/routing/source mix can invalidate it |
| Decision policy | Scores/probabilities, loss/cardinality assumptions and review budget | Link/non-link/abstain disposition, rationale and policy version | Pairwise policy does not by itself enforce globally consistent membership |
| Joint resolution (optional) | Scored pairs, known constraints and unresolved alternatives | Assignments/partition or uncertainty-preserving memberships, decision trace, conflicts | Unscored edge is not a cannot-link; unmatched options must exist when allowed |
| Entity construction | Membership decisions and original observations | Golden/virtual/hybrid representation, field lineage, stable/versioned entity identity | Membership truth and chosen consumer value are different questions |
| Review/correction | Evidence traces and uncertain or audited decisions | Adjudicated label, correction authorization, membership/attribute change history | Model predictions cannot automatically become independent gold labels |
| Incremental maintenance | New/changed/deleted observations, state/version dependencies | Recomputed affected artifacts, ID redirections, reversible merge/split events | Dependency closure can extend beyond the changed record; distinguish event time and processing time |

## Composition and failure containment
- A cascade records terminal and escalated decisions plus routing versions; evaluate early exits separately, not just the remaining hard cases.
- A parallel composition keeps missing branch outputs distinct from negative branch evidence; fusion must use comparable scales or a justified learned map.
- An iterative composition records the context snapshot and iteration producing a feature; known labels and predicted memberships must not be confused.
- A budgeted retriever declares whether truncation/splitting sacrifices coverage. Index build and update costs belong in total compute accounting.
- Reversible entity changes require restoring membership/lineage and notifying downstream consumers; simply deleting a link does not necessarily reverse its transitive effects.

See [dimensions](architecture-dimensions.md), [taxonomy ownership](overview.md), and the [catalog](../CATALOG.md) for actual alternatives. Contracts are Atlas design synthesis; they are not externally benchmarked requirements.
