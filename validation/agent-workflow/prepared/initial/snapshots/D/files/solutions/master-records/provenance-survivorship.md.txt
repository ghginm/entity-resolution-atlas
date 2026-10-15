---
id: SOL-09-001
type: solution
title: Provenance-preserving attribute survivorship
domain: "09"
summary: >-
  Derive consumer-facing master values from field-specific raw observations
  while preserving source, transformation, time and selection lineage for every
  chosen value. Handle uncertainty and contradiction explicitly, support
  recency, source precedence and independent corroboration without letting
  copied observations count repeatedly, and keep selection distinct from
  inference. Coherent attribute bundles and separate review of attribute truth
  versus entity membership reduce Frankenstein records. Replay and merge or
  split recomputation must reproduce the same trace.
tags: [provenance, source-aware, conflicting, missingness, governance, interpretable]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-09-001]
  complements: [SOL-06-001]
  used_by: [AR-06]
  evaluated_by: [EVAL-11-003]
---

# Provenance-preserving attribute survivorship

## Short summary

Survivorship chooses the fields presented for a membership-decided entity while leaving evidence intact. The fusion literature classifies conflict handling and supports preservation, source precedence, recency and similar strategies; the lineage contract and recommendations here are **Atlas synthesis**.[13] It is not an identity scorer.

## Problem addressed

Multiple observations of one entity may disagree or be incomplete. A single golden value can obscure an absence from a contradiction, and a plausible mix from multiple sources may never have been true together. Consumers need a current answer, auditors the basis, and corrections a replayable state. Choosing fields cannot prove that records belong to the same entity.

## Core mechanism

For each entity, role and field, retain an observation set: raw value, source/record version, namespace, transformation lineage, observation and valid-time context, and quality state. [Evidence states](../comparison-features/evidence-states.md) distinguish agreement, partial agreement, unavailable, invalid and qualified contradiction; apply those meanings before survivorship rather than collapsing them to one similarity.

A documented field policy then selects a presentation or returns multiple values:

- **Recency:** prefer the assertion with the latest applicable valid time, not merely latest ingestion.
- **Source precedence:** prefer a named authoritative source, with scope and policy version recorded.
- **Corroboration:** count observations only after removing copies and shared derivation lineage; no universal voting threshold is tested here.
- **Preserve:** keep conflicting or multi-valued results visible, or send them to review, instead of forcing one value.

Record what was selected and why, including alternatives. A calculation, average or external enrichment is an explicit inference tied to inputs and versions, never stored as an observation. Do not create values outside admissible evidence to conceal a gap.

## Theoretical explanation

Field truth and entity truth are different estimands: correct membership plus a wrong survivor still produces a wrong consumer value, while correct current fields do not justify a false merge. Preserving observations makes selection a function replayable from membership, evidence and policy. Copy independence matters because duplicated sources alter apparent frequency; a mode can measure propagation rather than corroboration. These are mechanism arguments, not measured gains.

## Important variants

Single golden, multi-valued entity view, and virtual per-query derivation suit different consumer capabilities. Field-specific policies may mix recency for mutable contact data with precedence for legal identifiers. As-of derivation from [temporal identity](../identity-semantics/temporal-identity.md) preserves intervals rather than overwriting history. A conservative baseline passes conflicts through for review; a resolving alternative supplies a selection rationale. These variants concern field presentation; identity scoring remains upstream.

## Assumptions and prerequisites

Stable memberships, field semantics, source namespaces, quality states and time interpretation are prerequisites. Policy owners must authorize precedence and acceptable uncertainty, and raw retention must remain accessible. If no observation supports a value, the result is unknown or review, not an invented default.

## Applicability conditions

Use when multiple sources populate overlapping attributes and correction, audit or consumer interpretation requires lineage. Prefer raw-preserving virtual fields where privacy or licensing prohibits consolidation. Under clean single-source data, direct projection is adequate; costs here are storage, policy governance and review capacity.

## Advantages

It exposes whether disagreement reflects uncertainty or contradiction, lets consumers choose a documented current view, and permits recomputation after a merge/split correction. A bad precedence or stale recency stays visible in the trace rather than as unexplained data.

## Trade-offs and failure modes

A “Frankenstein record” can combine individually plausible fields into an entity bundle that never co-occurred: a later name with an old address and two incompatible jurisdiction statuses. Evaluate coherent bundles, not only independent cells, and do not invent cross-field rules without domain support. Wrong precedence can persist an error; recency can reward an incorrect but fresher source; corroboration can double-count copies. Materializing one survivor erases alternatives if lineage is discarded; survivorship must never justify entity membership. Stale hybrid views can diverge from evidence.

## Relationships with other methods

This addresses the [master representation](../../decisions/master-representation.md) question. It complements [evidence states](../comparison-features/evidence-states.md) and temporal observation histories. [AR-06](../../architectures/incremental-continuous.md) can consume it when membership or observations change. Decision policy determines pair membership; this solution determines attribute presentation under that decision. Do not multiply pair probabilities into record confidence and select fields with it.

## How to evaluate

Use an attribute-level reference independent of membership labels. Within adjudicated-correct entities, measure field validity, missingness resolution and contradiction handling. Report entity truth and field truth separately. Replay the same observations and policy to test determinism; after merge/split fixtures, confirm retained lineage, recomputed views and no orphaned values. Inspect bundle coherence, review queue volume, lineage completeness and time-interpretation errors. A view-level improvement is not evidence that identity resolution improved.

## Research opportunities

Test whether cross-field bundle scoring reduces incoherent masters compared with independent field policies, holding membership and evidence fixed. Compare explicit corroboration after copy de-duplication against naive source precedence on source-shifted data. No thresholds are preassigned by the Atlas.

## References and evidence limitations

The verified fusion source supports separate duplicate/object identification and data fusion, uncertainty versus contradiction, and conflict-handling strategies including preserving, preferred source and recent value; it does not validate this implementation contract or performance superiority.[13] Corroboration-threshold, replay and failure-frequency claims are Atlas reasoning. No Atlas experiment has been run.

## Sources

[13] https://www.bioinf.jku.at/teaching/ss2011/se-inf/data_fusion_a1-bleiholder.pdf — Data fusion
