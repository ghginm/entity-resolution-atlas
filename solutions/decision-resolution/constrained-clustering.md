---
id: SOL-08-004
type: solution
title: Constrained entity partitioning with admissible membership
domain: "08"
summary: >-
  Resolve records into entity clusters only when proposed merges satisfy audited
  must-link, cannot-link, source, entity-type, and time constraints. A
  conservative sorted feasible-merge baseline and a soft partition-level
  objective expose different trade-offs: vetoing false bridges versus tolerating
  violated evidence. The card defines admissibility, infeasibility diagnosis,
  greedy order limits, and controlled comparisons, and warns that untrustworthy
  constraints systematically undermerge legitimate repeated source observations.
tags: [entity-agnostic, clustering, constraints, source-aware, high-precision, asymmetric-costs, interpretable, batch]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-08-001]
  requires: [DEC-01-001]
  complements: [SOL-08-001]
  evaluated_by: [EVAL-11-003, EVAL-11-004]
---

# Constrained entity partitioning with admissible membership

## Short summary

The hard-admissibility variant returns a partition of eligible records in which every cluster is jointly admissible: no cannot-linked pair shares a cluster, every must-linked pair does, and source, entity-type, and time restrictions hold. Correlation clustering formalizes partition-level signed-evidence objectives over +/− similarity labels; those soft labels need not all be satisfied and are not hard admissibility rules.[12]

## Problem addressed

Unconstrained closure merges through any accepted path; assignment forbids endpoint reuse but cannot represent multi-record entities or within-source duplicates. When the application knows specific unions are impossible — or specific records must stay together — membership policy, not just edge acceptance, should be the lever. Everything beyond the cited mechanisms below (baselines, conflict diagnostics, experiments) is **Atlas synthesis**, not reported source findings.

## Core mechanism

Start from singleton clusters, enforce the transitive closure of all mandatory must-links independently of candidate availability or utility, and validate those initial groups against every hard constraint before optional merges. Inconsistent initial groups require infeasibility diagnosis, not silently dropping must-links. Represent admissibility as constraints over **whole clusters**, not only the pair being merged: with respect to cannot-links, merging groups $X$ and $Y$ is feasible exactly when no cannot-linked pair has one member in $X$ and one in $Y$. All other declared source/type/time constraints must also hold on the proposed union.

A conservative baseline processes candidate merges in descending utility and executes only feasible ones, leaving blocked records in separate clusters or unresolved. It is deterministic given a stated tie rule; cost depends on maintaining whole-union checks, and each refusal is auditable to a named constraint. Its opposite failure is also auditable: it may reject a legitimate merge because one distant cluster member conflicts.

A soft formulation instead optimizes a partition objective, rewarding positive evidence within clusters and negative evidence across clusters, or equivalently penalizing positive edges cut and negative edges kept inside.[12] Fallible constraints can receive soft penalties; independently mandatory constraints still restrict the feasible set rather than become freely violable costs. This card specifies admissibility rules and objectives, not engine architecture, solver choice, or infrastructure.

**Derived harmful-bridge example:** entities $E_1=\{a_1,a_2,a_3\}$ and $E_2=\{b_4,b_5,b_6\}$ with one false accepted link $a_2$–$b_5$. Closure yields a six-record cluster containing $3\times3=9$ false cross-entity co-memberships. If a validated cannot-link exists between $a_1$ and $b_4$, both feasible merging and a hard-constrained objective refuse the $E_1$–$E_2$ union regardless of the bridge's utility, because the merge would co-locate $a_1,b_4$.

## Theoretical explanation

Source-structured partitioning matters: multifile modeling treats within-file duplication and cross-file overlap as file-specific patterns rather than imposing one cardinality everywhere, and its estimators can leave uncertain portions of the partition unresolved.[14] A constraint is trustworthy when its provenance genuinely implies impossibility — a validated unique-identifier contract with known scope, an entity-type rule from [identity semantics](../../decisions/identity-semantics.md), or overlapping known validity intervals asserting mutually exclusive states under an audited single-occupancy invariant for comparable state types and the chosen identity target. Disjoint periods alone do not imply incompatibility: an enduring person may move between addresses. Unknown validity or legitimate concurrent states cannot justify that hard veto. A noisy identifier mismatch normally remains fallible evidence, not a logical prohibition.

## Important variants

Hard cannot/must constraints, soft penalties, per-file no-duplication restrictions, and abstention that outputs partial partitions with flagged unresolved records are distinct choices.[14] Prefer hard constraints only with verified impossibility; encode doubtful vetoes as losses.

**Hard-constraint semantics:** must-links close transitively; a cannot-link between two must-link groups prohibits their union. Cannot-link itself is not transitive: two records each incompatible with a third need not be incompatible with each other. Wagstaff and Cardie formalize instance-level must/cannot restrictions and integrate them into COBWEB (COP-COBWEB), with context-specific clustering experiments.[37] This is not the later COP-k-means algorithm or ER validation. Conflicting hard constraints make the proposed problem infeasible; a solver cannot repair incorrect provenance by asserting consistency.

## Assumptions and prerequisites

Requires settled same-as semantics and time scope, constraint ownership and provenance, and utility units comparable across merges (see the companion [assignment card](one-to-one-assignment.md)). Missing candidate pairs remain unknown; never auto-generate cannot-links from absent comparisons, unlike the explicit below-threshold − labels a scored graph can supply.[12]

## Applicability conditions

Suited to high-false-merge-cost entity assembly where specific incompatibilities are known and repeated legitimate within-source observations make one-to-one matching infeasible.[14] Conditionally exclude it when constraints are unvalidated: a cannot-link derived from "same source" or a weak ID conflict forbids exactly the repeated observations a duplicate-prone registry contains, producing systematic undermerge — fragmentation that looks precise while violating identity semantics.

## Advantages

Direct veto power over whole-cluster unions; interpretable refusals; infeasibility is diagnosable — when must-link closure contains a cannot-linked pair (e.g., must $a$–$b$, must $b$–$c$, cannot $a$–$c$), no partition satisfies the set, so quarantine and audit provenance rather than silently dropping either side.

## Trade-offs and failure modes

Greedy order matters: an early feasible merge changes which later merges are feasible, so tie rules and score scale determine the output, and the result can be far from the best admissible partition. A soft objective reintroduces the weighting problem it was meant to avoid. Over-constraining undermerges; under-constraining permits bridges. Satisfying constraints is not identity accuracy: a feasible partition can still be the wrong one.

**Local versus global choice (Atlas synthesis):** local feasible merges are easy to trace but commit before seeing later competition. A partition-level objective compares competing groupings, at the cost of defining a loss, choosing a solver/approximation and reporting stopping or optimality limits. Global objective value is still a surrogate for identity truth. Do not make a universal complexity or exact-optimality guarantee for all constrained formulations. If constraints or relation types are uncertain, retain unresolved membership or a typed related-to edge rather than force it into same-as. Parent/subsidiary, co-occurrence and shared-address relations can support investigation without authorizing transitive identity closure.

## Relationships with other methods

[Thresholds and abstention](thresholds-abstention.md) can supply accepted links and vetoes, but only genuine incompatibility deserves cannot-link status. [Connected components](connected-components.md) is the alternative to compare against; its chain risk motivates cluster-level admissibility. [Partial assignment](one-to-one-assignment.md) competes only under audited duplicate-free scopes. [Temporal identity](../../solutions/identity-semantics/temporal-identity.md) governs time-constraint meaning; [provenance and survivorship](../master-records/provenance-survivorship.md) consumes the resulting membership.

## How to evaluate

Freeze candidates, scores, and constraints; run controlled comparisons of closure, feasible merging, and soft objectives on the same graph. Ablate constraints one at a time to observe whether a trusted prohibition prevents harmful unions or a spurious one fragments true entities; neither change is guaranteed to alter the selected partition when other evidence already determines it. Inject noise into constraint provenance to measure sensitivity. Report largest erroneous merge, foreign-entity contamination, fragmentation, refusal counts with constraint attribution, and declared cost via [entity-quality diagnostics](../../evaluation/entity-resolution-quality.md); [retrieval blind spots](../../evaluation/retrieval-blind-spots.md) bound what any comparison can see.

## Research opportunities

Test whether abstention-bounded partial partitions cut review workload at a fixed harm limit, and whether sorted feasible merging with provenance-gated constraint promotion approximates the soft objective on realistic graphs. Predeclare practical-effect thresholds before inspecting results.

## References and evidence limitations

[12] supports label-based correlation clustering as an established resolution family and its scalability framing; [14] supports source-specific duplication/cardinality structure and partial partition estimates, not a generic greedy algorithm. No source here measures the derived bridge example or the sorted-merge baseline; no Atlas experiment is reported.

## Sources

[12] https://www.vldb.org/pvldb/vol2/vldb09-1025.pdf — Framework for Evaluating Clustering Algorithms in Duplicate Detection
[14] https://arxiv.org/abs/2110.03839 — Multifile Partitioning for Record Linkage and Duplicate Detection
[37] https://wkiri.com/research/papers/wagstaff-constraints-00.pdf — Clustering with Instance-level Constraints
