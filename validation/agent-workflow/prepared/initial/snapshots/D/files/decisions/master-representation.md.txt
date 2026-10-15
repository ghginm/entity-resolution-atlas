---
id: DEC-09-001
type: decision
title: Choose master representation and identity lifecycle
domain: "09"
summary: >-
  Decide how resolved members become a persistent entity that consumers use:
  virtual membership views, consolidated golden records, or hybrid derived
  views with retained lineage. Separately fix persistent identifier allocation,
  merge redirection, split ambiguity and versioning, independent of which
  attribute values the chosen representation displays. Each option changes what
  a correction can undo, what a downstream key means after merge or split, and
  what evidence a consumer can still see. Requirements and lifecycle rules are
  Atlas synthesis; no universally correct representation is claimed.
tags: [entity-agnostic, governance, provenance, incremental, interpretable, batch]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [AR-06]
  evaluated_by: [EVAL-11-003]
---

# Choose master representation and identity lifecycle

## Decision question

Given membership decisions, what artifact represents “the entity,” and how does its identifier behave across correction, merge and split? The representation choice and the identifier lifecycle are separable: golden, virtual and hybrid views can each be paired with different ID policies, and choosing a survivor value answers neither question.

## Problem context

Consumers need a stable handle and an entity view: CRM and billing need a current record, analytics need joinable IDs, compliance often needs per-source evidence and correction history. A record remains a source observation; the master artifact is a derived representation of the real-world entity the project's [identity semantics](identity-semantics.md) define. Data-fusion work defines its goal as combining duplicate object representations into one consistent representation, and treating escalation or preservation of conflict as an explicit strategy rather than an omission.[13]

## Relevant assumptions

Membership may be revised later: bridges can dissolve, clusters split, merges prove wrong. Corrections must be traceable: who authorized what change, against which observation versions and policy versions, and what downstream consumers saw at the time. Identifier meaning depends on this trace. The lifecycle rules below are **Atlas synthesis**; the cited fusion literature does not prescribe them.

## Available solution families

- **Virtual/linked entity:** the entity is an ID plus its member-observation set; consumers query through it. Evidence and source conflicts stay visible; no value needs to be “materialized” wrongly. Costs: read-time aggregation, more complex consumer contracts, harder “current value” questions.
- **Golden record:** a consolidated surviving representation written to storage. Consumers get one simple row. Costs: a clean appearance can hide contradictory evidence; if only the survivor is retained, correction and rederivation lose their basis.
- **Hybrid:** a derived golden convenience view plus retained memberships and lineage, rebuilt as inputs change. Requires explicit view-versus-evidence synchronization so a stale view cannot outrank its own history.

**Identifier lifecycle, independent of attribute representation:** allocate an entity ID when identity is first asserted or only when published, and never recycle a retired ID. On merge, retain one ID, redirect the other explicitly, and keep both member histories. On split, no algorithm determines which child “deserves” the original ID: options include one child retains it while others receive new IDs, or all children receive new IDs under a versioned parent. Each choice has different downstream key consequences; record the decision rather than inheriting an arbitrary database outcome.

## Criteria for choosing

Ask whether consumers can perform read-time aggregation; whether they can resolve redirects; whether privacy, licensing or federation prohibits materializing cross-source values into one record; whether as-of historical views are required; and how often corrections or splits occur relative to reference stability. High reversibility requirements favor retained memberships and derived views. Irreversible downstream key exposure favors cautious publication and explicit redirection.

## Trade-off comparison

Golden records optimize read simplicity while concentrating the harm of a wrong merge or bad survivor choice in one materialized row. Virtual entities preserve evidence but push semantics into every consumer query. Hybrids recover both but add a synchronization obligation and storage. Stable-ID redirection preserves references but can silently reinterpret them; renumbering makes change visible but breaks consumers without a resolver. None is universally superior; the correct comparison is against the application's unit of harm.

## Good baseline candidates

**Atlas synthesis:** begin with virtual membership plus a documented derived view, an append-only ID ledger, and explicit merge/split redirection. Only materialize golden fields where a demonstrated consumer need exists, with [provenance-preserving survivorship](../solutions/master-records/provenance-survivorship.md) supplying the value policy.

## Prerequisites

Membership decisions come from [resolution strategy](resolution-strategy.md) choices; entity meaning comes from identity semantics. The representation is downstream: it cannot repair ambiguous membership, and survivorship must never be used as evidence of entity truth. [Incremental maintenance](../architectures/incremental-continuous.md) depends on stable observation keys and reversible membership; without them, corrections become unverifiable appends. A correction trace is a prerequisite for auditable lifecycle claims, not merely an optional feature.

## Open questions

Which consumers require as-of entity versions, and for how long must redirects be retained? Who authorizes a split? Can a federated source expose membership without exposing raw values? Is entity versioning required when attributes change or only when membership changes? These need project answers, not Atlas defaults.

## Related evaluations

[EVAL-11-003 final-entity quality](../evaluation/entity-resolution-quality.md) must be measured on the promised representation and diagnostics must include ID stability, correction latency and split/merge lineage. Do not infer representation correctness from pairwise scores.

## Links to Solution Cards

[Provenance-survivorship](../solutions/master-records/provenance-survivorship.md) specifies field selection inside any representation. Temporal identity supplies intervals an as-of view may consume.

## Sources

[13] https://www.bioinf.jku.at/teaching/ss2011/se-inf/data_fusion_a1-bleiholder.pdf — Data fusion
