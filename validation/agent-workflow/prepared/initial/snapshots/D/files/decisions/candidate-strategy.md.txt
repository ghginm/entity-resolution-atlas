---
id: DEC-05-001
type: decision
title: Choose a candidate generation strategy
domain: "05"
summary: >-
  Choose how to expose plausible record pairs to downstream comparison without
  exhausting the admissible pair space. Compare exact keys, complementary passes,
  and approximate retrieval families using coverage, skew, cost, and
  source compatibility. Requires explicit identity semantics, permitted source
  pairs, and a way to investigate missed matches. Candidate admission is not a
  match decision; budgets and filtering can undo the coverage benefits of broader
  retrieval.
tags: [candidate-generation, blocking, high-recall, low-cost, source-aware, evaluation, entity-agnostic]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  complements: [DEC-06-001]
  evaluated_by: [EVAL-11-001]
---

# Choose a candidate generation strategy

## Decision question and context

Which record pairs should receive expensive comparison, under the project's coverage and resource constraints? Blocking restricts comparisons to records sharing blocks; similarity filtering instead excludes pairs using conditions tied to a specified similarity function and threshold. Their assumptions differ even when both reduce work.[2] Neither candidate membership nor exclusion should silently become a definitive identity judgment.

Define the admissible pair universe first: within-source deduplication, selected cross-source linkage, or both. Excluding prohibited source combinations is different from dropping plausible identities for efficiency. Candidate recall concerns true matching pairs admitted from this universe, not final cluster recovery.

## Assumptions and prerequisites

**Atlas synthesis:** establish identity granularity, identifier namespaces and validity periods, source-pair permissions, normalization contracts, and the acceptable consequences of missed matches. Profile field availability, key stability, common values, and block-size tails by source. Retain raw observations and retrieval provenance so exclusion causes remain inspectable. Labels collected only from current candidates cannot establish coverage outside that candidate set; use independently assembled identities or a defensible outside-set audit.

Do not assume missing fields are equal keys. Do not assume two copied sources provide independent corroboration. For identifier-based admission, lexical equality needs a compatible issuing namespace and temporal meaning, not merely matching characters.

## Available alternatives and solution links

- [Exact blocking](../solutions/candidate-generation/exact-blocking.md): economical, inspectable equality-based admission; sensitive to missing or corrupted keys. Composite keys demand agreement on every required component.
- [Multi-pass blocking](../solutions/candidate-generation/multi-pass-blocking.md): union complementary admission routes, preserving pass provenance and deduplicating pairs. Its value depends on newly exposed matches, not the number of generators.
- [Approximate retrieval under budgets](../solutions/candidate-generation/approximate-blocking.md): compare sorted-neighborhood, shingle-index, canopy and MinHash/LSH mechanisms, with bounded vector/hybrid roles. Preserve candidate caps and representation assumptions; similarity guarantees are not identity-recall guarantees. Specialist learned blockers and ANN internals remain explicitly deferred, not implied implemented.
- **Taxonomy-only, unexpanded:** similarity filtering may complement retrieval when its exclusion bound is valid for the intended comparison predicate; a heuristic rejection rule is not automatically such a guarantee.[2]

## Selection criteria and trade-offs

**Atlas synthesis:** compare mechanisms against observed corruption, rather than ranking families universally. Stable, populated keys favor exact admission. Multiple complementary attributes favor passes with different failure patterns. Text variation motivates testing approximate retrieval; representation and language coverage then become additional prerequisites. Learned retrieval needs representative evidence about both admitted and missed matches, with protection against source-specific shortcuts.

Measure unique pairs, retrieval work, downstream comparison cost, latency, memory, and coverage by source, script, sparsity, and key frequency. A broad pass may recover rare missed identities while flooding common-name blocks. A selective composite key controls cost but excludes matches whenever any required component changes. Duplicate candidates consume generation and deduplication work even if scored once.

**Mathematical reasoning:** adding a pass cannot reduce pair coverage if the admissible universe and truth set remain fixed and every old candidate survives. With ranking caps, block removal, sampling, or early stopping, this monotonicity no longer follows. Correlated passes may add substantial work without new matches. Distinguish losses at admission, budget enforcement, filtering, and scoring.

## Baseline and related evaluations

**Atlas synthesis:** begin with a small, documented exact-key strategy, plus a complementary pass only where profiling suggests a different recoverable failure. This is a diagnostic baseline, not a universally safe deployment choice. Compare alternatives with unchanged input representations and truth scope, then repeat under equal operational budgets.

Use [candidate recall evaluation](../evaluation/candidate-recall.md) to report pair completeness, reduction against the defined universe, unique candidate volume, segment gaps, and marginal coverage per pass. Inspect misses independently of scorer performance. The [comparison evidence decision](comparison-evidence.md) complements this choice because retrieval determines which agreements and contradictions the scorer can observe.

## Open questions and evidence limits

Which exclusions are unacceptable? Do large blocks contain recoverable matches or mostly ambiguity? Can sparse and multilingual records receive useful fallback routes? Does a new pass alter candidate composition enough to invalidate existing scoring estimates? The survey supports the method taxonomy and blocking/filtering distinction, not a recommended winner.[2] No Atlas benchmark has been run; baseline and experiment recommendations above are synthesis.

## Sources

[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
