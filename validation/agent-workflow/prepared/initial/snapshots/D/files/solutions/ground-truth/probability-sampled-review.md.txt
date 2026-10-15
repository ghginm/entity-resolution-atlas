---
id: SOL-10-002
type: solution
title: Probability-sampled review with separate evaluation and learning pools
domain: "10"
summary: >-
  Acquire auditable pair labels through a probability sample of a declared frame,
  with optional stratification for rare matches, source coverage and costly errors.
  Reserve independent evaluation labels and spend a separate targeted learning
  budget without confusing the two distributions. Log sampling units, strata,
  draw and inclusion probabilities, response dispositions and annotation costs.
  The design supports evaluation only where sampling support and label evidence
  exist; unresolved reviews, frame omissions and extreme weights limit claims.
  Entity search and estimator derivations remain with their canonical owners.
tags: [entity-agnostic, few-labels, pairwise, human-review, source-aware, provenance, uncertainty, evaluation, experimentation]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-10-001]
  evaluated_by: [EVAL-11-002, EVAL-11-004, EVAL-11-005]
  complements: [SOL-10-001, SOL-10-003]
---

# Probability-sampled review with separate evaluation and learning pools

## Short summary

Create a probability-based audit pool and a separately governed learning pool. The former supports quality claims; the latter can prioritize informative cases. Random selection within score-defined strata is legitimate probability sampling when its inclusion probabilities and support are known; deterministic selection of only ambiguous pairs is not the same design.[15]

## Problem addressed

Candidate-only or convenience labels cannot reveal errors absent from their frame. Uniform pair review supplies a transparent baseline but can consume the budget on nonmatches. The proposed hybrid retains an independent probability sample while enriching review effort where positives, scarce sources or costly mistakes are plausible. It does not promise a universal budget saving.

## Core mechanism

1. **Define frame and annotation unit.** Freeze universe, eligibility, candidate set and policy versions. A pair frame may be specified by a reproducible sampler rather than materializing every pair. Declare unordered deduplication versus cross-file pairs. Distinguish sampling a pair, sampling a record then pairs, and sampling a cluster then its members; these induce different inclusion probabilities. A pair label does not certify a complete entity.
2. **Separate uses before feedback.** Reserve evaluation entities or leakage-safe groups independently of active learning; protect calibration labels too. Include randomized pool assignment in evaluation inclusion probabilities, or explicitly limit the estimand to the resulting population. Entity-disjoint partitioning can require entity discovery: different pair IDs do not guarantee isolation. Retain cross-boundary unknowns. Evaluation labels and evaluation-derived rankings stay inaccessible to learning decisions.
3. **Stratify from available information.** Use mutually exclusive source-pair, missingness, score or candidate-status categories with known sizes. For full-pairspace recall include outside-candidate strata and a broad residual region, not only enriched near-misses. Assign ambiguous or unscored units explicitly. In fixed-size simple random sampling without replacement within stratum $h$, $\pi_i=n_h/N_h$, where $N_h$ and $n_h$ are its frame and sample sizes. Avoid tiny allocations that cannot support the planned uncertainty analysis.[15]
4. **Log the actual design.** Store frame version, stratum, sampling stages, selected unit, randomization record, repeats and first-order inclusion probability; preserve joint inclusion information or replication instructions needed by the evaluator. Under independent with-replacement draws having constant per-draw probability $q_i$, unique-unit inclusion after $k$ draws is $1-(1-q_i)^k$. This derived identity does not apply unchanged to adaptive draws. Do not deduplicate and keep $q_i$ as though it were inclusion probability.
5. **Annotate with response accounting.** Use written match/nonmatch/unknown rules and evidence provenance; blind scores where feasible. Retain inability to access evidence, ambiguity and review abandonment as separate dispositions. Randomly re-review a prespecified subsample, add targeted disagreement investigation, and retain both routes' probabilities and costs. Count first reviews, repeated reviews, adjudication and search time separately.
6. **Spend the learning allocation separately.** Route uncertainty, disagreements or scarce-source cases through [targeted acquisition](targeted-active-review.md). Return training labels and error hypotheses, not unweighted population accuracy. Never append these labels to the audit pool and reuse its original weights.

## Theoretical explanation

Known positive inclusion probabilities allow inverse-probability estimation under a specified probability design.[15] For fixed, fully observed finite-population outcomes, the Horvitz–Thompson total is design-unbiased: each unit's weighted contribution has its original value in expectation. Ratios of estimated totals are generally biased in finite samples; neither equal counts of positives and negatives nor normalized weights make them exactly unbiased. The [blind-spot audit](../../evaluation/retrieval-blind-spots.md) and [incomplete-reference evaluation](../../evaluation/incomplete-reference-quality.md) own the estimators, identifiability and intervals.

Strata can enrich rare outcomes without abandoning inference, but support must remain positive throughout the population claimed. One realized sample with no positives is possible under a sound design; it is not proof of no missed links or of a defective sampler. Review error and frame omissions are nonsampling errors, not solved by narrower sampling intervals.

## Important variants

Proportional allocation is a simple baseline; disproportionate allocation can reserve scarce-source coverage or enrich suspected misses. Pilot information can inform a later frozen allocation, with pilot/final uses and probabilities documented. Multistage record or cluster review may amortize search effort but changes design and variance. Use [entity-centric construction](independent-reference.md) when complete memberships are required, rather than duplicating its search procedure here.

## Assumptions and prerequisites

Require authorized evidence, a reproducible covered frame and interpretable labels. Known selection probability is not known response probability. Survey nonresponse adjustment assumes respondents adequately represent nonrespondents within the adjustment groups.[15] In ER, unresolvable pairs may systematically differ from resolved ones. Do not silently drop them or invent response weights; investigate, report sensitivity/bounds, or narrow the estimand explicitly. Zero-support and unknown-probability regions cannot be repaired by selection weighting.

## Applicability conditions

Prefer when accepted-pair precision, candidate loss or calibration must describe a declared population and the independent annotation is feasible. Under extreme positive rarity, pair review alone may not deliver useful recall precision within budget; compare entity review and report an inconclusive audit rather than redesigning the denominator after seeing labels.

## Advantages

The artifact connects labels to an auditable population and preserves evaluation across alternative scorers or retrieval rules within its declared universe. A separate learning pool permits targeted investigation without pretending those findings are representative.

## Trade-offs and failure modes

Frame maintenance, specialist review and double annotation consume budget. Extreme weights, empty sparse strata and unknown-heavy slices can make estimates unstable. Replacing inaccessible sampled units with easy volunteers changes the design. Selecting high-risk entities but analyzing their constituent pairs as independent random pair draws changes it too. Reviewer agreement can reflect shared anchoring rather than correct identity evidence.

## Relationships with other methods

This solution addresses [acquisition design](../../decisions/ground-truth-acquisition.md). It complements entity search by supplying probability pair audits where complete memberships are unnecessary, and active review by protecting its independent test route. Their artifacts need distinct provenance and population contracts. Conditional exclusion: an unresolved pair cannot become a negative merely because another module needs binary labels.

## How to evaluate

Separate two comparisons. **Audit allocation:** vary uniform, stratified or hybrid review designs at matched cost; assess design-specific precision, coverage, unresolved outcomes and reference error. The audit sample is the treatment, not an unchanged control. **Learning acquisition:** vary training selection while preserving a common protected evaluation reserve; compare held-out quality and both fixed-label-count and total-cost frontiers. A joint change needs an explicit crossed/system design, not attribution to ranking alone. Use [controlled comparison](../experimentation/controlled-comparison.md).

Predeclare precision goals and reference-error guardrails. Adopt useful precision/quality within budget; reject unsupported population claims or excessive review error. Wide intervals remain inconclusive. Variance must follow actual pair, entity or multistage sampling; shared entities do not invalidate genuine finite-population random-pair variance. Transfer models and correlated reviewer errors introduce different dependence questions. A naive pair bootstrap is not universal.

## Research opportunities

Test whether source-aware allocation improves decision precision at matched cost, separating enrichment from better reviewer evidence. Do not optimize the final audit on its observed outcomes without an explicit adaptive design.

## References and evidence limitations

Statistics Canada's manual, sections 6.2, 6.2.6, 7.1, 7.1.3 and 7.3, grounds probability sampling, stratification, weighting, nonresponse assumptions and design-specific variance.[15] The ER pool separation and operational artifact are Atlas recommendations; no local label collection or measured gain is reported.

## Sources

[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
