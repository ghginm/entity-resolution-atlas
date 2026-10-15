---
id: SOL-05-002
type: solution
title: Multi-pass blocking and candidate union
domain: "05"
summary: >-
  Combine candidate sets from distinct blocking or retrieval passes so that
  different attributes and representations can expose different matching pairs.
  Requires stable pair identity, pass provenance, explicit eligibility rules,
  and evaluation beyond the original candidate set. An uncapped union preserves
  prior pair coverage, but overlapping passes add work without necessarily
  adding matches. Global caps, routing, or filtering can break that guarantee
  and change the downstream evidence distribution.
tags: [candidate-generation, blocking, multi-pass, high-recall, noisy, source-aware, provenance, evaluation]
maturity: established
evidence: supported-by-external-literature
relations:
  addresses: [DEC-05-001]
  used_by: [AR-02]
  evaluated_by: [EVAL-11-001]
---

# Multi-pass blocking and candidate union

## Summary and problem addressed

Multi-pass generation exposes pairs through several admission routes rather than relying on one fragile key. The blocking survey describes repeated block building with different schemes to accommodate noisy data.[2] The design problem is choosing complementary routes while controlling duplicated work, candidate volume, and subsequent selection effects.

## Core mechanism

**Atlas synthesis:** define each pass's key or retrieval predicate, applicable sources, required attributes, and representation lineage. Run the eligible passes; form their candidate-set union; identify each pair consistently; and preserve every admitting pass. Deduplication changes repeated pair emissions into one comparison request, not multiple independent votes for identity.

An illustrative organization pair might enter through name-plus-locality in one pass and an identifier in another. A changed name can defeat the first route while leaving the second intact. Two passes based on differently transformed versions of the same corrupted name may fail together. These are mechanism examples, not observed results.

The conceptual output includes pair identity, source pair, admission reasons, and budget or pruning status. A skipped pass must remain distinguishable from a completed pass finding no candidates. Any downstream filtering is a separate operation with separately attributable losses.

## Theoretical explanation

**Mathematical reasoning:** for a fixed admissible universe and fixed true-match set, an exhaustive union contains every constituent candidate set. Adding a pass cannot lower candidate-pair recall if all previously admitted pairs survive. This requires neither independent passes nor uncorrelated errors. Complementarity determines whether recall increases strictly, not whether set inclusion holds.

A pass contributes only its candidates outside the existing union; its coverage gain comprises the true matches in that difference. Both quantities depend on which passes were already included. Marginal gain is therefore order-dependent as an attribution measure, even though the full uncapped union is order-independent. Do not add individual recall values or assume independent miss probabilities without justification.

Under top-ranked candidate limits, block removal, stochastic sampling, or time-bounded early stopping, additional emissions can displace older candidates. Such a budgeted composition is not an exhaustive union and inherits no automatic monotonicity guarantee. Raw pair emissions and generation cost may grow even when unique candidates scarcely change.

## Variants and prerequisites

**Atlas synthesis:** variants include multiple [exact keys](exact-blocking.md), source-specific routes, alternate representations, and a broad fallback for unavailable attributes. The [approximate retrieval menu](approximate-blocking.md) supplies selected constituent mechanisms and explicitly bounded adaptive/vector roles; specialist learned blocking remains deferred. Sequential routing that skips later passes after apparent success is a distinct selection policy, not equivalent to running all passes.

Prerequisites are explicit pair scope, key eligibility, consistent identity for candidate deduplication, and provenance sufficient to reconstruct overlap. Applicability is strongest where distinct fields plausibly survive distinct corruption patterns. Sparse records may defeat every route; multilingual representations may share systematic losses rather than supply independent coverage.

## Advantages, trade-offs, and failure modes

Multiple routes make exclusions less dependent on one attribute and expose the cause of admission. Costs include repeated retrieval, deduplication, memory, and comparison of weakly selective additions. Common values can dominate one pass. Several correlated representations of one observation can create an illusion of corroboration if pass count is treated as match evidence.

**Atlas synthesis:** pass membership also identifies a selected population. Newly recovered pairs may have weaker names, more missing attributes, or different source reliability. Old match prevalence and evidence weights need not transfer. Any use of pass membership in scoring requires training and validation under the deployment selection policy, not an automatic confidence bonus.

## Relationships and evaluation

The approach [addresses candidate strategy](../../decisions/candidate-strategy.md) and is a component [used by the recall-oriented architecture](../../architectures/recall-multi-pass.md). That architecture can choose different scorers; candidate union does not determine scoring or final entity membership.

Use [candidate recall evaluation](../../evaluation/candidate-recall.md). **Atlas synthesis:** compare a single-pass baseline, the exhaustive union, and the operationally budgeted union. Report overlap, unique candidate volume, marginal true-match coverage, block skew, latency, and source/sparsity segments. Leave-one-pass-out ablation reveals dependence on each route; independent truth must cover pairs missing from all routes. Test equal-budget alternatives alongside uncapped coverage to avoid attributing extra compute to superior retrieval design.

## Research opportunities and evidence limits

Investigate passes chosen from actual missed-match categories and routing that preserves coverage for vulnerable segments. Falsify complementarity claims when added routes expose no useful new matches at acceptable cost. The survey supports repeated blocking, not universal superiority.[2] Union properties are conditional mathematical reasoning; examples, contracts, and experiments are Atlas synthesis, with no benchmark results.

## Sources

[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
