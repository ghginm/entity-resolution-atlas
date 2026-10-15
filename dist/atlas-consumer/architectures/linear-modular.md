---
id: AR-01
type: architecture
title: Linear/Modular Baseline
domain: "02"
summary: >-
  A sequential reference composition separates normalization, candidate generation,
  comparison evidence, scoring, decision policy, and entity construction through
  explicit artifacts. It supports controlled component replacement without choosing
  a mandatory matching algorithm or resolution strategy. Use it when traceable
  experiments and understandable interfaces matter. Identity semantics, candidate
  scope, and score interpretation must be specified first; simplicity does not
  remove candidate omissions, calibration problems, or downstream merge risks.
tags: [entity-agnostic, interpretable, batch, pairwise, provenance, evaluation]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  complements: [AR-02, AR-06]
  evaluated_by: [EVAL-11-001, EVAL-11-002, EVAL-11-003]
---

# AR-01 — Linear/Modular Baseline

## Philosophy and four dimensions

Make boundaries visible before increasing orchestration complexity. This is an Atlas synthesis, not an empirically ranked baseline. The ER literature contains probabilistic, supervised, clustering, and canonicalization approaches; those choices need not determine one pipeline topology.[5]

- **Topology:** sequential modules with materializable intermediate artifacts; internal parallel execution does not change the logical sequence.
- **Scoring paradigm:** deterministic, expert-additive, probabilistic, supervised, neural, or hybrid.
- **Resolution:** independent pair dispositions, assignment, or constrained entity membership, chosen from identity semantics.
- **Lifecycle:** batch reference execution; the same interfaces can support incremental updates. Federated execution adds privacy/access constraints separately, rather than prescribing a scorer.

## Pipeline and modules

`Observations → representations → candidates → evidence → scores → dispositions/membership → entity view`.

Required responsibilities are identity/source specification, representation preparation, candidate enumeration, comparison, scoring, resolution policy, and output provenance. Preparation may be an identity transformation when observations are already suitable. Entity construction can remain a virtual membership view: a golden record is not required. Optional modules include enrichment, probability calibration, review, survivorship, and monitoring. If the application needs membership rather than pair decisions, a membership resolver becomes required rather than optional.

## Conceptual input/output contracts

Use the shared [module contracts](../taxonomy/module-contracts.md); these are logical artifacts, not prescribed schemas or code.

- **Preparation:** source-scoped observation IDs, versions, raw values, namespaces, and timestamps enter; normalized representations retain raw-value lineage and transformation versions. Missing and invalid values remain distinguishable.
- **Retrieval:** representations plus eligible source/cardinality scope enter; distinct canonical pair keys, retrieval provenance, and coverage limits leave. A pair absent from this artifact is unexamined, not a declared non-match.
- **Comparison:** candidate keys and referenced observation versions enter; per-field evidence states, similarities, contradictions, and provenance leave. The [evidence-state solution](../solutions/comparison-features/evidence-states.md) prevents missingness from silently becoming disagreement.
- **Scoring:** versioned evidence enters; score, declared scale, model version, and available explanation leave. An additive weight is not automatically a probability.
- **Resolution/output:** scores and policy/constraint versions enter; match/non-match/abstain or memberships, decision reasons, and unresolved cases leave. Entity views preserve contributing observations; stable-ID maintenance is a separate responsibility.

For example, two source-scoped observations sharing a normalized organization name produce a candidate and name-agreement evidence, not an identity conclusion until namespace and policy assumptions are checked.

## Compatible alternatives and assumptions

[Exact blocking](../solutions/candidate-generation/exact-blocking.md) can feed [additive soft matching](../solutions/matching-scoring/additive-soft-matching.md), [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md), or [logistic regression](../solutions/matching-scoring/logistic-regression.md). Select [thresholds and abstention](../solutions/decision-resolution/thresholds-abstention.md) for pair outputs, assignment for a justified one-to-one task, or constrained clustering for duplicate groups. Do not substitute connected components without examining transitive false merges.

Applicable settings include structured identifiers, modest heterogeneity, interpretable linkage, and component experiments at any manageable scale. No-label operation requires defensible rules or estimated distributions; supervised scoring requires representative labels. Few labels may support auditing, but cannot establish every segment's calibration. Multilingual normalization or sparse evidence may demand richer representations without changing this topology. Identity semantics and cardinalities must be explicit.

## Mechanism, costs, and failure modes

The proposed advantage is experimental attribution: holding candidate and evidence artifacts fixed helps separate scorer changes from retrieval changes. Attribution remains conditional because normalization changes propagate through every later artifact. Materialization reduces repeated computation but costs storage and stale-artifact management; a strictly serial deployment may add latency.

Candidate omissions cannot be repaired by a better scorer. Destructive normalization can remove discriminative detail. Treating score scales as interchangeable misconfigures policies. Good pair metrics can coexist with poor assignment or overmerged entities. Interface stability is therefore semantic, not merely structural: every replacement must preserve or explicitly migrate scope, versions, missingness, and score meaning.

## Interactions, evaluation, and research

For implementation structure, compare [modularity choices](../decisions/pipeline-modularity.md) and [replaceable stages](../solutions/architecture/replaceable-stage-pipelines.md); AR-01 remains the logical linear baseline, not an inheritance hierarchy or workflow-engine requirement. [Versioned artifact runs](../solutions/architecture/versioned-artifact-runs.md) can preserve controlled comparisons without changing the scorer or membership policy. A behavior-preserving extraction and an intended matching change need different evidence.

[AR-02](recall-multi-pass.md) replaces the retrieval module with candidate union; [AR-06](incremental-continuous.md) changes maintenance around the same boundaries. These complement relations do not mandate either pattern.

Evaluate [candidate recall](../evaluation/candidate-recall.md), [pairwise calibration](../evaluation/pairwise-calibration.md), and [entity quality](../evaluation/entity-resolution-quality.md) separately, with entity-disjoint labels and segment diagnostics. Compare component replacements on identical snapshots and policies; report compute, review load, uncertainty, and end-to-end error costs.

Two illustrative end-to-end configurations preserve the same modular boundaries:

- Prepared observations → exact blocking → evidence states → additive scorer → threshold/abstain policy → virtual linked-record output: a no-training-label composition requiring expert assumptions and independent auditing.
- Prepared observations → multi-pass blocking → evidence states → logistic scorer → cost-sensitive pair proposals → one-to-one assignment with unmatched options → versioned entity view: a supervised composition requiring representative labels and justified cardinality.

These are alternatives, not measured winners. Variations include reviewed pair linkage and probabilistic scoring. Research can test whether richer evidence helps after candidate recall is controlled, using ablations and an unchanged resolver. No improvement or universal research priority is asserted.

## Sources

[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
