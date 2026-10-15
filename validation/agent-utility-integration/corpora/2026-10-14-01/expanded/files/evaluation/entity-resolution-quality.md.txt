---
id: EVAL-11-003
type: evaluation
title: Final entity-resolution quality and error diagnostics
domain: "11"
summary: >-
  Assess the final identity output rather than assuming pairwise scores determine
  entity quality. Complete reference partitions support cluster-induced pair
  precision/recall and record-averaged B-cubed metrics; sampled fully resolved
  entities require design-aware estimation instead of naive benchmark slicing.
  Overmerge, undermerge, assignment, and catastrophic-error diagnostics connect
  measurements to application costs. Reference completeness, dependent records,
  output semantics, and oracle label support are essential prerequisites.
  The protocol offers complementary views, not one universally optimal metric.
tags: [evaluation, clustering, assignment, constraints, collective, uncertainty, asymmetric-costs, entity-agnostic]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  tests: [AR-01, AR-03, AR-05, AR-06]

---

# Final entity-resolution quality and error diagnostics

## Output contract and purpose

Evaluate the output promised by identity semantics: accepted links, constrained assignments, or entity memberships. Clustering is not mandatory for every linkage task; the ER landscape includes distinct pairwise and clustering approaches.[5] A transitive closure can create identity assertions for unscored pairs, while assignment constraints can reject high-scoring edges. Consequently, final quality is not determined by [pairwise calibration](pairwise-calibration.md).

For partition-producing systems, define a fixed record universe V, reference partition G, and predicted partition P, including singleton records. State temporal identity rules, eligibility boundaries, and treatment of unresolved records. Do not remove difficult records to improve metrics. For assignment-only systems, measure link precision/recall, cardinality violations, unmatched-record rates, and decision cost directly; do not invent clusters merely to use a convenient metric.

## Definitions on complete reference truth

The following formulas assume G completely partitions the evaluated V. Let S(G) and S(P) contain every unordered distinct-record pair co-clustered in their respective partitions, not merely accepted graph edges.

- Cluster-induced pair precision = |S(P) ∩ S(G)| / |S(P)|.
- Cluster-induced pair recall = |S(P) ∩ S(G)| / |S(G)|.
- B-cubed precision = (1/|V|) sum over r in V of |P(r) ∩ G(r)| / |P(r)|.
- B-cubed recall = (1/|V|) sum over r in V of |P(r) ∩ G(r)| / |G(r)|.

Here P(r) and G(r) are the clusters containing record r. Pair metrics emphasize large entities through their many induced pairs; B-cubed averages per-record purity and completeness, not equal weight per entity. If reporting F1, specify the harmonic mean of aggregate precision/recall rather than an average of record-level F1. Empty pair denominators are undefined; B-cubed handles singleton partitions without manufacturing positive pairs. These are definitions, not empirical findings.

Restricting both partitions to a labeled subset can hide contaminants and missing members outside it. The resulting numbers describe that induced subset only, not global precision or recall. Unknown cross-boundary pairs must not be labeled nonmatches. Fully resolving an entity includes finding all its records within the declared universe; labeling an arbitrary convenient cluster is insufficient.

## Sampling and reference requirements

The entity-centric framework of Binette, Baek, Engineer, Jones, Dasylva, and Reiter connects fully resolved sampled entities, error diagnostics, and population performance estimation.[4] The verified version is arXiv v1, with inventor-disambiguation and simulation validation; it does not license naive metrics on incomplete labels.[4]

For new-identity transfer separate whole evaluation entities from training; for continuation use later observations with only admissible historical state, never future-label feedback. Follow the [split contract](../solutions/experimentation/controlled-comparison.md#applicability-conditions). Preserve source coverage, entity inclusion probabilities, adjudication ambiguity and searches for omissions. Under entity sampling, use estimators derived for that design and observed predicted-cluster intersections, rather than applying complete-partition formulas to a partial benchmark. For a completely known sampled true entity G_e, inspecting its full predicted clusters reveals how many records outside G_e contaminate them; the foreign records' own complete entities need not all be known for that bounded impurity question. If G_e itself is partial, outside records may be undiscovered true members: retain unknowns. [Incomplete-reference evaluation](incomplete-reference-quality.md) distinguishes these cases and their unidentifiable extensions.

Source 4's v1 section 3.4.1 equation (15)/Lemma 4 uses **entity-balanced** B-cubed, unlike the record-average definition above; section 3.4.2 uses with-replacement ratio estimation.[4] Do not transplant those estimators unchanged. The [sampling translation](../deep-dives/incomplete-reference-estimation.md#translation-for-sampled-entity-b-cubed) separates record-size-weighted contributions, entity averages and draw versus inclusion designs.

## Diagnostics and comparisons

Compare identical records and semantic constraints across the [linear baseline](../architectures/linear-modular.md), [precision cascade](../architectures/precision-cascade.md), and [collective resolution](../architectures/collective-consistency.md). Freeze candidates and scores to isolate resolution effects; separately compare whole systems on a quality–cost frontier. Record threshold selection outside the evaluation holdout.

Diagnose overmerging through supported foreign-record contamination and false co-clustered pairs; undermerging through fragmentation and missed within-entity pairs. Counting distinct true identities swallowed additionally requires adjudicating foreign membership or reporting bounds: two foreign records may belong to one or two identities. Track largest supported errors, contradictions and downstream exposure. A bridge can contaminate large groups despite acceptable average F1. Report exact recovered-entity rate and entity-balanced views with their own truth requirements and denominators.

For [incremental resolution](../architectures/incremental-continuous.md), add correction latency, identity churn, and persistence of mistaken merges. These monitoring signals need adjudicated outcomes before being interpreted as accuracy. A predeclared catastrophic-error rate needs a denominator (entities, records, predicted clusters or downstream decisions) and its corresponding probability sample. [Cluster-risk review](../solutions/ground-truth/targeted-active-review.md) can find severe counterexamples but cannot estimate that rate by inspection yield alone. Fewer contradictions, bridges or large components are not proof of better identity quality.

## Graph diagnostics without labels

**Atlas synthesis:** monitor component-size tails, bridge/articulation exposure, source/type mixtures, contradictions, edge-admission margins and sensitivity to plausible score perturbations on a versioned graph. Report their denominators and observation scope. These identify fragile or suspicious decisions for investigation, not true/false identity rates. A legitimate sparse entity may be bridge-heavy, while a dense wrong union can evade bridge tests. Fewer components above a size limit may simply reflect undermerging.

Compare diagnostics on the same eligible records and graph semantics; changing retrieval changes topology before resolution is even applied. Audit selected cases independently and record review coverage, cost and unresolved evidence. Risk-targeted adjudication tests the reason for the alarm; population accuracy additionally needs the [independent acquisition design](../decisions/ground-truth-acquisition.md) and [incomplete-reference estimand](incomplete-reference-quality.md). A graph contradiction cannot create the missing labels required for precision/recall.

## Oracle diagnosis, uncertainty, and limitations

Component oracles are controlled diagnostic replacements, not performance forecasts. A scorer oracle substitutes known dispositions only where independent labels support them; candidate augmentation requires independently known missed true pairs; a resolution oracle needs complete reference membership on its stated universe. Unsupported pairs remain unknown. Run each replacement with other modules fixed and report its scope. Assignment competition, transitivity, and policy interactions can make downstream changes nonmonotonic, even when a local component becomes more accurate.

Use paired design-aware uncertainty, resampling actual entity/cluster primary units and preserving their weights and strata, or the appropriate finite-population pair design if pairs were genuinely probability-sampled. An iid pair bootstrap does not capture shared-entity generalization uncertainty; few sampled entities cannot support narrow claims about future entities. Treat overlapping predicted-cluster contributions according to the estimator/design, not as independent errors. Cost-sensitive comparisons need application-specific penalties and predeclared catastrophic-error limits. This protocol specifies evaluation only; no ER experiment or universally preferred architecture is established.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
