---
id: SOL-01-001
type: solution
title: Enduring identity with time-scoped evidence
domain: "01"
summary: >-
  Maintain enduring entity identity while representing changing attributes as
  versioned, time-scoped observations rather than overwriting history. Separate
  validity, source observation and ingestion times, and use an explicit domain
  continuity policy for migration, identifier reuse and organizational succession.
  Compare with snapshot or episode identity when longitudinal continuity is not
  required or cannot be established. The approach enables revisable histories
  and as-of views but needs trustworthy temporal semantics, correction lineage
  and evaluation that distinguishes identity truth from attribute-state truth.
tags: [entity-agnostic, incremental, provenance, identifiers, uncertainty, source-aware]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  addresses: [DEC-01-001]
  complements: [SOL-09-001]
  used_by: [AR-06]
  evaluated_by: [EVAL-11-003]
---

# Enduring identity with time-scoped evidence

## Short summary

Resolve a continuing target object while keeping its observations, attributes and identity decisions versioned. The mechanism and tests are **Atlas synthesis**. A changed state need not imply a changed entity; conversely, lexical continuity does not establish enduring identity. No domain-independent rule decides succession or identifier reuse.

## Problem addressed

Overwriting old names or addresses loses evidence needed to reconcile historical records. Treating every state change as a new entity fragments longitudinal analysis. Treating every recurring key as permanent identity can instead merge distinct entities after reassignment. These are different failures and need different labels.

## Core mechanism

Define the target and continuity policy using [identity semantics](../../decisions/identity-semantics.md). Retain each raw observation with source-scoped record/version, field meaning, transformation lineage and:

- **Valid time:** when the assertion applies in the modeled world, possibly an uncertain interval.
- **Observation time:** when the source observed or asserted it; distinguish measurement from source revision when available.
- **Ingestion time:** when the resolving system received it. A late import does not make an old address current.

Track decision/publication time separately when reconstructing what the system previously believed. Missing time remains unknown; an ingestion timestamp is not a substitute for validity. Corrections may revise past validity while preserving the superseded assertion and its correction relationship.

Associate observations with an enduring entity provisionally or confidently according to policy. Compare attributes under their applicable intervals; nonoverlapping residences may represent movement, while overlapping incompatible states warrant review only under an explicitly trusted constraint. Historical values can help retrieval; preserve which version generated each candidate.

**Illustration:** an address valid in an earlier period is ingested after a later-period address. Keep both, use valid time for a current-state view, and use ingestion/decision history for the previously-known view. If validity is unknown, publish that uncertainty rather than silently replacing the current address.

## Theoretical explanation

Separating identity from state prevents the logical implication “different attribute implies different entity” unless that attribute is an invariant under the chosen semantics. Versioned observations retain distinctions that an overwrite destroys. This is an information-preservation argument, not a guarantee that extra history improves matching: old observations can create misleading coincidences and additional candidate load.

## Important variants

Use event histories, interval-valued assertions or periodic snapshots with explicit observation gaps. A two-axis validity/system-history view supports both “what applied then?” and “what did we believe then?” Partial temporal evidence can support bounded or unknown intervals rather than fabricated exact dates. Namespace-scoped episodes are appropriate for reusable accounts or assets when continuity cannot be established.

## Assumptions and prerequisites

Require interpretable field/time semantics, identifiable observation revisions, a domain continuity policy and reversible membership. Migration may preserve an account only when an authorized mapping establishes it; shared attributes are insufficient. Reuse, re-registration and organizational succession need separate adjudication. If facts are missing, keep alternatives or a typed successor relation, not a hardcoded same-as or different verdict.

## Applicability conditions

Favor this approach for longitudinal joins, auditability, corrections and changing attributes when continuity is meaningful. Use the **snapshot/state identity baseline** for current-state reconciliation or independently defined episodes. Exclude lifetime merging when the requested unit is a legal registration episode; exclude snapshot-only output when consumers require enduring histories unless explicit state-to-entity links restore them.

## Advantages

History can support temporally appropriate comparisons, as-of consumer views and correction explanations rather than renumbering an entity after a name change. Unknown time remains inspectable rather than disguised as a conflict.

## Trade-offs and failure modes

History adds storage, policy and retrieval costs. Guessing intervals from ingestion creates false temporal contradictions. Matching on any historical alias can overmerge after contact reuse. Declaring all simultaneous differences impossible rejects legitimate multiple addresses or roles. Untracked retrospective edits make replay diverge from prior published beliefs.

## Relationships with other methods

[Explicit evidence states](../comparison-features/evidence-states.md) carry comparability and temporal uncertainty to scoring. [Survivorship](../master-records/provenance-survivorship.md) consumes memberships and observation intervals to select views; it must not use a convenient display value to justify identity. [Incremental maintenance](../../architectures/incremental-continuous.md) invalidates indexes, scores, memberships and views after revisions. The input contract includes policy and observation versions; output includes enduring IDs, versioned memberships, intervals, unresolved alternatives and correction lineage. Consumer values are derived artifacts, not the only retained evidence.

## How to evaluate

Compare enduring versus snapshot identity on independently adjudicated longitudinal targets with separate state labels. Fix observations, retrieval budget and scorer when testing temporal comparison; separately measure whole-pipeline historical retrieval effects. Hold out later periods and whole entities. Inspect false continuity, fragmentation, temporal contradictions, unresolved cases and as-of accuracy. Replay late arrivals, duplicates, deletions, migration, reuse and retrospective corrections; check deterministic publication, ID lineage and divergence from full recomputation. Neither replay agreement nor full recomputation is truth.

## Research opportunities

Test whether interval-qualified contradictions outperform time-agnostic vetoes without increasing harmful continuity errors. Predeclare acceptable harm and review workload from project needs; report inconclusive evidence rather than infer continuity from convenience.

## References and evidence limitations

Data-fusion literature distinguishes object identification from combining attributes.[13] It does not establish this temporal contract or continuity laws. All temporal variants and proposed evaluations here remain synthesis; no Atlas experiment has been run.

## Sources

[13] https://www.bioinf.jku.at/teaching/ss2011/se-inf/data_fusion_a1-bleiholder.pdf — Data fusion
