---
id: AR-05
type: architecture
title: Collective/Consistency-Aware Resolution
domain: "02"
summary: >-
  Resolution decisions are coupled when identity semantics impose cardinality,
  membership constraints, or useful relational dependencies. The pattern covers
  one-to-one assignment with unmatched outcomes, constrained clustering, and
  genuinely collective relational inference without treating them as equivalent.
  It requires justified constraints and score semantics compatible with the
  resolution objective. Joint decisions may prevent locally plausible conflicts,
  but incorrect constraints or propagated evidence errors can harm whole groups;
  a graph representation and iterative inference are not mandatory.
tags: [entity-agnostic, assignment, clustering, collective, constraints, provenance, uncertainty, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [AR-06]
  evaluated_by: [EVAL-11-002, EVAL-11-003]
---

# AR-05 — Collective/Consistency-Aware Resolution

## Philosophy and four dimensions

Independent plausible pairs may be incompatible with the requested identity output. Couple decisions only when the task warrants it. Primary work demonstrates adaptive query-time relational collective resolution in publication databases; it does not validate every constrained resolver or establish universal gains.[10] This broader archetype is Atlas synthesis.

- **Topology:** scored candidates followed by joint resolution; optionally iterative evidence/resolution feedback. A one-shot assignment is also compatible.
- **Scoring paradigm:** deterministic, additive, probabilistic, supervised, neural, or hybrid pair/relational evidence.
- **Resolution:** assignment, constrained membership, or relational collective inference, explicitly distinguished below.
- **Lifecycle:** batch or maintained incrementally. Federated privacy/access restrictions separately constrain relational visibility and feasible joint computation.

## Pipeline and modules

`Eligible candidates → comparison/scoring → constraints and optional relationships → joint resolver → dispositions/membership → optional evidence refresh`.

Required modules are identity/cardinality specification, candidates and evidence, declared score/objective semantics, a resolver, and decision provenance. Relational data and iterative inference are optional unless the selected configuration depends on them. Constraint validation and infeasibility handling are required whenever constraints are imposed. Optional modules include review, uncertainty analysis, entity construction, and rollback support.

## Resolution alternatives and rationale

1. **One-to-one assignment:** eligible cross-source links compete because each observation may be assigned at most once. Include explicit unmatched options and their costs; forcing a complete matching can create false links. This is not unrestricted duplicate clustering.
2. **Constrained clustering:** decide memberships with must-link/cannot-link or cardinality conditions. Constraints need scope and temporal meaning. Simple transitive closure can overmerge through one erroneous bridge; rejecting bridges or optimizing memberships are different policies.
3. **Relational collective inference:** linked references or entities influence one another's identity hypotheses. Relationship types must remain distinct from same-as identity. Co-occurrence-based joint resolution is a concrete primary-literature example.[10] Merely sharing an address or collaborator is not an identity rule.

A graph can represent evidence or dependencies, but it is not required for assignment or constrained membership. Hard constraints encode admissibility; soft penalties encode preferences. Neither should be silently treated as observed truth.

## Conceptual input/output contracts

Use the [module contracts](../taxonomy/module-contracts.md).

- **Evidence input:** versioned candidate pairs and [comparison states](../solutions/comparison-features/evidence-states.md). **Output:** scores with declared scale, model version, provenance, and optional typed relationship observations.
- **Constraint input:** source/cardinality rules, temporal scope, and adjudicated conditions. **Output:** versioned admissibility rules or penalties with justification and conflict diagnostics.
- **Resolver input:** candidate scores, constraints, unmatched/singleton options, and optional relationship evidence. **Output:** selected assignments or memberships, unresolved cases, constraint violations/infeasibility, and decision explanations.
- **Iteration input:** provisional memberships and original evidence. **Output:** revised evidence/objective values and a versioned resolution proposal; retain stopping criteria and feedback lineage.

Illustratively, two plausible matches competing for one target require a choice or unmatched outcome, not two independent acceptances. Output confidence must distinguish pair certainty from the stability of that joint choice.

## Assumptions and scorer compatibility

Use when one-to-one cardinality is genuinely warranted, duplicate groups need membership consistency, or relationships supply relevant identity information. Reject inappropriate one-to-one assumptions when a source legitimately repeats the same entity. Relational coverage and meanings may differ across sources.

[Additive scoring](../solutions/matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), or [logistic regression](../solutions/matching-scoring/logistic-regression.md) can supply evidence, but objective-compatible utilities must be specified; optimizing arbitrary score sums is not automatically optimal expected loss. Deterministic constraints need no training labels, yet adjudication is needed to assess their correctness. Learned relational components require leakage-safe labels; entity and connected-context separation may be necessary beyond random pair splits.

## Mechanism, costs, and failures

The proposed advantage is excluding incompatible local decisions or borrowing informative context. Benefits require correct constraints and useful context. False constraints force systematic errors; relational feedback can amplify a mistaken seed. Candidate omissions still restrict feasible true resolutions.

Assignment, constrained clustering, and relational iteration have different costs; no single complexity claim covers them. Large ambiguous groups increase memory and optimization burden. Approximation, stopping rules, partition boundaries, and update order can affect outcomes. Repeatedly counting context derived from the same provisional memberships can create unsupported certainty.

## Interactions, evaluation, and research

[AR-06](incremental-continuous.md) must revisit dependent competitors and relationships, not only changed records. Multi-pass retrieval and ensembles can feed this resolver if score meanings and candidate scope remain explicit.

Evaluate [pair calibration](../evaluation/pairwise-calibration.md) separately from [entity quality](../evaluation/entity-resolution-quality.md), assignment accuracy, unmatched quality, constraint errors, and runtime. Compare independent pair decisions with joint resolution on identical scored candidates. Variations include soft constraints and reviewed conflict sets. Research should ablate constraints and relationships separately, inject erroneous conditions, and test sensitivity to missing context. No universal advantage is claimed.

## Sources

[10] https://cdn.aaai.org/AAAI/2007/AAAI07-255.pdf — Online Collective Entity Resolution
