# Incomplete-reference estimation: denominators, bounds and uncertainty

**L3 scope.** Read [EVAL-11-005](../evaluation/incomplete-reference-quality.md) first. This document adds derivations for unresolved estimation choices, not a second evaluation taxonomy. Formulas are Atlas reasoning under the stated finite-population assumptions. Source 15 supplies survey-design principles; source 17 supplies the conditional positive-unlabeled identity, not a universal metric correction.

## 1. Separate target, sampling and review populations

Fix semantic pairspace $U$, candidates $C\subseteq U$, true statuses $y_i\in\{0,1\}$ and $A=(\text{all asserted pairs})\cap U$. A production eligibility filter is a stage inside semantic $U$, not authority to redefine identity after misses are discovered. In a pair-output policy $A\subseteq C$; a partition can assert pairs outside $C$ through closure. Restrict pair numerators and denominators consistently to $U$; report forbidden assertions outside it separately. Complete-partition B-cubed over records is a different estimand. Freeze whether the question concerns scored edges or induced memberships.

The sampling frame $F$ must cover the population of the claim. If $F=C$, even a census can only estimate candidate-conditioned quality. A holdout can be independently drawn yet systematically omit a source; independence from training is not representativeness. A probability sample can span $U$ but still yield selectively missing adjudications. Keep draw, inclusion, response and label correctness separate.

## 2. Weighted totals, not a weighted fraction of whatever was reviewed

For probability sample $S$ without replacement, define first-order inclusion probability $\pi_i=P(i\in S)>0$. With correct, resolved sampled outcomes and frozen predictions, the Horvitz–Thompson total for any fixed pair quantity $z_i$ is

$$
\widehat{Z}=\sum_{i\in S}\frac{z_i}{\pi_i},\qquad
E_S[\widehat{Z}]=\sum_{i\in U}z_i.
$$

The expectation follows from $E_S[1(i\in S)]=\pi_i$. It is over repeated samples, not random identity labels. Use $z_i=y_i$, $y_i1(i\in A)$ or $y_i1(i\notin C)$ for true-pair, true-accepted and missed-candidate totals. Design weights and domain estimators follow the same population distinctions as survey estimation.[15]

When $|A|$ is exactly known, $\widehat{TP}/|A|$ has an exact nonrandom denominator and is design-unbiased under these assumptions. A noisy total divided by a known count can exceed one for some unequal-probability designs; a normalized ratio estimator can remain bounded while giving up exact unbiasedness. State the estimator, not just “weighted precision.” With an accepted-only stratified sample, estimate true accepted totals within its strata and divide by known $|A|$.

Recall generally uses $\widehat{TP}/\widehat{T}$, a ratio of random totals. It is not generally unbiased; approximation and large-sample validity need conditions, including an estimable positive denominator and no dominant weights. Jointly estimate numerator/denominator covariance. Replacing unknown $\widehat{T}$ with the number of known positives silently changes the estimand.

For separate candidate and outside-candidate strata, estimate $T_C$ and $T_O$ with their own inclusion probabilities. Candidate recall is estimated by $\widehat{T_C}/(\widehat{T_C}+\widehat{T_O})$. [The blind-spot audit](../evaluation/retrieval-blind-spots.md) defines the operational attribution. A convenience positive list and a probability pair sample cannot be concatenated as if they shared one design.

Under sampling **with replacement**, per-draw probabilities and repeated draws require a draw-based estimator, or the actual unique-unit inclusion probabilities after deduplication. A final query probability from an adaptive sampler is neither automatically the overall inclusion probability nor an evaluation weight. Entity sampling likewise needs the induced design for the entity-level contributions or pair totals being estimated.

### Translation for sampled-entity B-cubed

The [entity-quality card](../evaluation/entity-resolution-quality.md) defines record-average B-cubed over a completely partitioned record universe $V$. For completely known true entity $e$, let $m_e=|G_e|$ and $b_e$ be the mean record-level purity or completeness within that entity, computed using full predicted-cluster intersections. The record-average target is $\sum_e m_e b_e/|V|$; entity-balanced B-cubed instead averages $b_e$ across true entities. Under without-replacement entity sampling with known entity inclusion $\pi_e$, the HT total $\sum_{e\in S}m_e b_e/\pi_e$ divided by known $|V|$ targets the record-average metric. Using an estimated size denominator creates a generally biased ratio estimator. Entity-balanced reporting uses $b_e$ contributions and its own entity-count denominator. These are Atlas translations under complete sampled memberships, not literal formulas copied from a source.

Source 4, v1 section 3.4.1 equation (15)/Lemma 4, uses equal weight per ground-truth entity, not the card's record average; its section 3.4.2 develops with-replacement ratio estimators.[4] Do not transplant that estimator into a without-replacement or record-average analysis. Partial true memberships can invalidate $m_e$ and $b_e$ even when entity inclusion is known. Pair-restricted $U$ metrics cannot be substituted into complete-record B-cubed without redefining the target.

## 3. Worst-case finite-reference bounds

Suppose all pairs in finite $U$ are assigned to correct known positives $P$, correct known negatives $N$, or unresolved $W$; this is not a sample generalized to unsampled populations. Write

- $a=|A\cap P|$, $p=|P|>0$;
- $u_a=|A\cap W|$, $u_o=|W\setminus A|$;
- $d=|A|>0$.

If $x$ unknown asserted pairs and $z$ unknown nonasserted pairs are true, then precision is $(a+x)/d$ and recall is $(a+x)/(p+x+z)$, with $0\le x\le u_a$ and $0\le z\le u_o$. Therefore

$$
\frac{a}{d}\le P_A\le\frac{a+u_a}{d},\qquad
\frac{a}{p+u_o}\le R_A\le\frac{a+u_a}{p+u_a}.
$$

The recall extrema follow from monotonicity in $x$ and $z$, using $a\le p$. They are **outer identification bounds**, not confidence intervals or simultaneously attainable precision/recall corners. Constraints from a real equivalence relation can rule out some pairwise assignments and tighten bounds. If $p=0$, truth could contain no positives at all; recall may be undefined, not automatically zero or one.

These bounds show why dropping unresolved pairs can reverse a comparison. To compare systems, evaluate admissible shared assignments to unknown truth, not separate optimistic imputations for each system. Sampling error requires an additional layer of inference; do not substitute fractional weighted pseudo-counts into these finite bounds and call them exact population bounds. Known false positive labels or missing true entities also invalidate the assumptions.

## 4. Positive-unlabeled assumptions and nonidentifiability

Let $L=1$ mark a correctly labeled positive. Under no false positive labels and **constant positive-labeling propensity** $P(L=1\mid Y=1,X)=c>0$,

$$
P(L=1\mid X)=cP(Y=1\mid X).
$$

This is the selected-completely-at-random identity in Elkan and Noto's section 2.[17] It concerns probabilities in a defined sampling population. Given only the left-hand side, different admissible $c$ and true posterior functions can give the same observations. Estimating $c$ needs additional information/assumptions; SCAR alone is not a guarantee that an arbitrary fitted labeling model identifies prevalence. Do not adopt every estimator proposed in a source without checking its additional requirements.

If identifier-linked positives preferentially represent easy same-script matches, propensity varies with $X$ and may be zero for alias-only sources. A global correction cannot recover that absent support. Case-control positive lists and separately sampled background records also have different observable proportions from a single sampled population; source 17 explicitly distinguishes those settings.[17] Source-specific sensitivity is preferable to asserting an identified population estimate. It remains assumption-dependent, not an independent adjudication.

## 5. Which uncertainty are you quantifying?

### Finite-population sampling

Fixed outcomes can share records without invalidating an actual pair probability design. For second-order inclusion probabilities $\pi_{ij}=P(i,j\in S)$, with $\pi_{ii}=\pi_i$, elementary indicator covariance gives

$$
\operatorname{Var}_S(\widehat Z)=
\sum_{i,j\in U}\frac{\pi_{ij}-\pi_i\pi_j}{\pi_i\pi_j}z_i z_j.
$$

First-order probabilities identify the total estimator, not necessarily an estimable variance: joint inclusion, replication structure or a justified approximation is also needed. Stratified simple random sampling without replacement uses its within-stratum finite-population correction. Cluster/multistage designs require their actual sampled units and stages; survey variance and replication must reflect that design.[15]

### Superpopulation and paired comparisons

A claim about future entities/sources introduces generalization uncertainty beyond that finite design. Pair observations sharing endpoints are not independent draws from a future-world distribution. Use entity/record-cluster or multiway dependence methods justified by the endpoint structure; cross-entity negative pairs cannot be assigned arbitrarily to only one entity. If a defensible method is unavailable, disclose the limitation rather than produce a narrow iid pair bootstrap interval. For paired pipelines, recompute both metrics and their difference in every valid replicate.

Algorithm seeds quantify training/retrieval randomness conditional on the same data, not new independent entities. Reviewer disagreement and omissions add label uncertainty not repaired by sampling weights. Re-adjudication subsamples and sensitivity to unresolved labels should accompany the sampling interval.

### Rare events and zero discoveries

If a stratum contains $N_h$ units and an actual simple random sample without replacement of size $n_h$ finds zero errors, the probability of that event when there are $K$ errors is

$$
P(0\mid K)=\frac{\binom{N_h-K}{n_h}}{\binom{N_h}{n_h}}.
$$

For observed zero, one conservative integer convention at level $1-\alpha$ retains $K$ with $P(0\mid K)\ge\alpha$ and sets the upper endpoint to the largest retained integer. State the equality convention; discreteness can make coverage conservative. This is the zero-observation branch of an inverted one-sided test, not a general interval recipe. Sampling size/stopping must match the design: repeated looks followed by favorable stopping require a valid sequential method, not reuse of a fixed-size bound.

The endpoint bounds the **stratum error total $K$**, not automatically the pipeline missed-pair ratio. Summing stratum limits or combining a missed-total limit with an estimated true-pair denominator needs jointly valid uncertainty, such as simultaneous error allocation across prespecified component limits. Marginal bounds do not automatically give their nominal joint coverage.

Do not replace zero discoveries with zero estimated variance. Under independent equal-probability Bernoulli trials with error probability $q$, the corresponding zero-event likelihood is $(1-q)^n$; its inversion is **not** automatically valid for weighted or clustered samples. Zero misses in an enormous low-prevalence residual region can still permit a large missed total.

Tail harm can be estimated only for the sampled unit: auditing seed records weights exposure by records, auditing entities targets entities, and auditing predicted clusters targets those clusters. A predeclared catastrophic-error indicator/cost with a valid design can estimate its population rate; risk-targeted inspections alone demonstrate existence/severity, not prevalence.

## 6. Decision under incomplete evidence

Predeclare the practical effect, cost and high-harm limits; use the [experiment template](../guides/experiment-plan-template.md). A result is inconclusive if plausible sampling intervals or admissible unresolved outcomes cover both worthwhile improvement and harm. Collect information where it most reduces that decision uncertainty while preserving independent evaluation. Fewer contradictions or prettier clusters are not evidence that population recall improved. No numerical example here represents measured ER performance.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
[17] https://cseweb.ucsd.edu/~elkan/posonly.pdf — Learning Classifiers from Only Positive and Unlabeled Data
