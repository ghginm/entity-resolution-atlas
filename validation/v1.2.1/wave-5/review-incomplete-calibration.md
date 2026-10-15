# Wave 5 targeted scientific review: incomplete truth and calibration

Date: 2026-10-15. Scope: incomplete-reference estimands, pair/entity sampling, positive–unlabeled (PU) identification, candidate/label selection, calibration and source-conditioned scoring. This is a bounded documentation review, not certification, an ER experiment or evidence of measured utility.

## Outcome and authority

**No demonstrated canonical scientific error was found in the reviewed passages.** The adverse examples below support retaining the stated qualifications; they do not validate every method or citation in the Atlas. One counterexample demonstrates why a propensity estimator discussed in an external paper must not be imported as a consequence of SCAR alone. The canonical deep dive already excludes that inference, so no canonical correction is requested.

Read `START_HERE.md`, `MAINTAINERS.md`, `SCOPE.md`, `SCHEMA.md` and `references/evidence-policy.md` before authoring. Read the nine requested canonical documents (including all four `solutions/ground-truth/*.md` cards) plus the relevant B-cubed passages in `evaluation/entity-resolution-quality.md`. Read existing source-ledger entries to preserve IDs. Did not read benchmark scenarios, keys, results or protected historical input contents. Did not edit canonical content, the shared ledger, other reviews or protected trees.

## Findings: demonstrated counterexamples versus limitations

### F1 — PU correction does not identify propensity or prevalence

Locations: `evaluation/incomplete-reference-quality.md:54–56`; `deep-dives/incomplete-reference-estimation.md:55–65`.

**Finding: scientifically important limitation, already stated correctly; not a canonical error.** Source 17 §2, Lemma 1 supports the conditional identity under correct positive labels and constant positive-labeling propensity. Its subsequent discussion proposes estimators of that propensity; those proposals must be evaluated separately from the identity.[17]

Construct two equally likely feature states with the same observable labeling probabilities `g=(0.1,0.2)`. Model A uses `c=0.25`, true posteriors `(0.4,0.8)` and prevalence `0.6`; model B uses `c=0.5`, posteriors `(0.2,0.4)` and prevalence `0.3`. Both obey SCAR and produce exactly the same observable `(X,L)` distribution. Thus SCAR does not identify `c` or prevalence from those observations.

**Demonstrated external-estimator overgeneralization, not an Atlas defect:** even if `g(x)=P(L=1|X=x)` is known exactly, averaging `g` over labeled positives gives `E[g(X)|L=1]=E[g(X)^2]/E[g(X)]=1/6` here. That is neither model's `c`. Equivalently it equals `c E[f(X)^2]/E[f(X)]`, where `f=P(Y=1|X)`. Observing a positive label does not imply `P(Y=1|X)=1`. The warning at deep-dive line 63 is therefore necessary. Do not weaken it or silently import a source's estimator as an identification theorem.

### F2 — Weighting, response and estimand are distinct contracts

Locations: `deep-dives/incomplete-reference-estimation.md:13–28,69–84`; `evaluation/incomplete-reference-quality.md:50–56,74–76`; `solutions/ground-truth/probability-sampled-review.md:36–47,55,75–77`; `solutions/ground-truth/independent-reference.md:37–46,70–80`.

**Finding: no demonstrated error.** The survey manual distinguishes design weights, nonresponse adjustment assumptions and design-specific sampling variance; it does not establish that unresolvable ER labels are ignorable.[15] The cards correctly keep unresolved review, zero support and unknown label error outside automatic inverse-probability correction.

Tool example: sample one of two accepted units with probabilities `(0.1,0.9)` and fixed outcomes `(1,0)`. True precision is `1/2`. HT precision is `5` or `0`, with expectation `1/2`; the normalized weighted ratio is `1` or `0`, with expectation `1/10`. In a separate example with both units true and only the first asserted, true recall is `1/2`, while the ratio-of-HT-totals estimate again has expectation `1/10`. Boundedness and finite-sample unbiasedness are not interchangeable.

For six pair units on four records, let the three pairs incident on record 0 have fixed outcome one. Exhausting all 15 simple random samples of two pairs gives expected HT total `3` and variance `18/5`. The joint-inclusion covariance formula independently gives `18/5`. Shared endpoints do not themselves invalidate this finite-population design calculation; future-entity inference is a different claim.

**Residual limitation:** no operational response model or deployment sampling design is supplied by the Atlas. These must remain project prerequisites, not inferred from the presence of weights.

### F3 — Incomplete-reference bounds are outer bounds, not a hidden complete partition

Locations: `evaluation/incomplete-reference-quality.md:27,37–46,66–68`; `deep-dives/incomplete-reference-estimation.md:36–53`.

**Finding: formulas survived the bounded exhaustive check.** With positive count `p=1..4`, `a=0..p`, unknown asserted/outside counts `0..3` each, and one asserted known negative, all **224 parameter cases / 3,150 binary assignments** reproduce the stated precision and recall extrema. This verifies this finite family, not a general proof or interval coverage claim.

The identity-constraint caveat matters. On four records, known matches `(0,1)` and `(1,2)` force asserted pair `(0,2)` true. Free-pair bounds allow precision `[0,1]` and recall `[0,1/3]`; enumerating the two compatible partitions gives precision exactly `1` and recall `[1/6,1/3]`. The card correctly calls the unconstrained expressions outer bounds and does not claim that they encode all equivalence constraints.

For the zero-discovery branch at `N=100,n=10,alpha=0.05`, the specified integer inversion gives upper error total **24**, because `P(0|24)=0.0551420950` and `P(0|25)=0.0478865562`. This is a fixed-design zero-observation calculation, not evidence of zero errors or a general sequential interval. The cautions at deep-dive lines 94–98 remain necessary.

### F4 — Candidate selection is not always a prior-only correction

Locations: `deep-dives/selection-and-calibration.md:13–59`; `evaluation/pairwise-calibration.md:27–37,49–57`.

**Finding: no demonstrated error in the conditioning identities.** Direct evaluation of a feature-dependent two-state example gives candidate match/nonmatch inclusion probabilities `5/8` and `7/16`, and posteriors `(3/5,1/7)` by both joint-probability and candidate-likelihood calculations. This is algebra under declared synthetic probabilities, not a fitted scorer.

Adversarial controls:

- Prior match probability `0.01`, exact blocking agreement rates `0.8` in matches and `0.1` in nonmatches: candidate-conditioned agreement LR is `1`; compatible posterior is `8/107 ≈ 0.0747664`. Multiplying the unconditional LR `8` into candidate prior odds again gives the wrong `64/163 ≈ 0.392638`.
- Two independent Bernoulli-half comparison states within a class, selected by OR: candidate joint probability of `(0,0)` is `0`, but the product of candidate marginal disagreement probabilities is `1/9`. The field-factorization warning is real. The primary linkage source separates the joint-ratio rule from conditional-independent component simplification in §3.2.[1]
- If selection is deterministic from retained full `X`, its posterior on included support is unchanged. Coarsening two equally likely feature states with match rates `0.8` and `0.2` into constant `gamma`, then selecting only the first, instead changes `P(M|gamma)` from `0.5` to `P(M|gamma,C)=0.8`. The full-information exception at lines 36–38 is essential.
- Class-only positive/negative label sampling probabilities `(1,1/9)` move target probability `0.1` to sample probability `0.5`; multiplying sampled odds by `1/9` recovers the target. Feature-specific selection ratios `9` versus `3` cannot be undone by one common intercept shift.

### F5 — Global calibration is not source-specific field authority

Locations: `deep-dives/selection-and-calibration.md:63–75`; `evaluation/pairwise-calibration.md:41–55`; `solutions/matching-scoring/source-aware-reliability.md:32–48,58–78`.

**Finding: correctly bounded theory/proposal, not a demonstrated reliability improvement.** Guo et al. §2 defines prediction-confidence calibration and binned diagnostics; its empirical setting is not ER. The Atlas expressly labels its binary adaptation rather than attributing ER validation to that paper.[3]

Synthetic equal-mass source contexts with true rates `0.9` and `0.1`, all assigned probability `0.5`, have pooled ECE `0`, Brier score `1/4`, no ranking discrimination and source calibration errors `0.4` each. Identical contextual evidence LR `4` with priors `0.1` and `0.5` gives posteriors `4/13` and `4/5`: different posterior predictions alone do not demonstrate different field reliability.

**Residual limitation, explicitly disclosed:** the hierarchical/shrinkage structure is an Atlas proposal; the source-conditioned card says no primary hierarchical-ER paper was checked. This review does not upgrade that evidence. A project comparison still needs pooled, context-prior-only and field-context controls, independent supported slices and a separately tested unseen-context fallback.

### F6 — Entity sampling cannot silently change the B-cubed target

Locations: `solutions/ground-truth/independent-reference.md:44–46`; `deep-dives/incomplete-reference-estimation.md:30–34`; `evaluation/entity-resolution-quality.md:33–50`.

**Finding: the source/Atlas distinction is correct.** The retrieved v1 text of source 4 §3.2 permits prediction-assisted acquisition; §3.4.1 equation (15)/Lemma 4 uses entity-balanced B-cubed; §3.4.2 assumes with-replacement cluster sampling for its ratio estimator. The Atlas explicitly separates its stronger acquisition safeguards and record-average target from these source choices.[4]

A complete truth with entity sizes `1` and `3`, predicted as one cluster of four, has record-average B-cubed precision `5/8`, entity-balanced precision `1/2` and recall `1`. Clipping to the singleton changes its apparent precision from `1/4` to `1`. These are different quantities, not competing estimates of one target.

For an entity of size three in ten records and two uniform seed draws, per-draw probability is `3/10`, unique inclusion with replacement is `51/100`, and without replacement is `8/15`. Reusing a draw probability after deduplication would change the estimator. No such error was found in these cards.

### F7 — Targeted review and weak supervision retain independent evaluation boundaries

Locations: `solutions/ground-truth/targeted-active-review.md:36–47,77–87`; `solutions/ground-truth/weak-supervision.md:35–49,60–62,76–102`.

**Finding: no demonstrated source-scope error in the checked passages.** IWAL v4 Algorithm 1/Theorem 1 and §4 distinguish history-conditioned query weighting from its separate loss-weighting analysis; Theorem 1 states the finite-hypothesis/positive-floor condition. This is not a unique-unit inclusion formula for arbitrary repeated adaptive pools.[18] Data Programming main-text equations (1), (4)–(9) and Theorems 1–2 place substantive model/coverage/accuracy/learnability constraints on their claims.[16] Snorkel §2 explicitly separates development labels and a blind held-out test.[21] The Atlas does not turn arbitrary rule consensus, LF confidence or active-query yield into population truth. Appendix proofs and full active-learning label-complexity arguments were not independently audited here.

## Reproduction and source retrieval scope

Created `check-incomplete-calibration.py` and `check-incomplete-calibration-output.json` beside this report. Run from the repository root:

```sh
python validation/v1.2.1/wave-5/check-incomplete-calibration.py
```

Actual execution: exit 0; **14 check groups; all assertions passed**. Checks use exact rational arithmetic, enumerated pair assignments/partitions/samples and fixed synthetic probabilities. They read no ER data, train no model and read no benchmark input. Some illustrative controls are direct calculations rather than independent theorem proofs.

Primary-source retrieval on 2026-10-15, using existing ledger identities only:

| ID | Retrieval and passages actually checked | Boundary |
|---|---|---|
| 1 | Ledger PDF fetched; §3.2, PDF pp. 7–8, conditional independence and additive decomposition | Not a complete proof audit |
| 3 | Publisher abstract plus linked full PDF, §2 / PDF p. 2 calibration and ECE | No ER transfer inference |
| 4 | Versioned arXiv HTML `2404.05622v1`, §§3.2, 3.4.1–3.4.2 | Display identifies v1 dated 8 April 2024 but also renders a manuscript date 24 August 2026; version route and checked passages recorded, not silently interpreted as a new version |
| 15 | Ledger PDF fetched in memory; §6.2.6 / PDF p. 116, §7.1.3 / pp. 134–135, §7.3 / p. 148 and §7.3.1.1 / p. 150 | Selected survey sections, not all 408 pages |
| 17 | Author PDF fetched, §2 / PDF pp. 1–2 and adjacent weighting discussion p. 3 | Conditional identity checked; estimator scope challenged above |
| 18 | arXiv PDF `0812.4952v4`, Algorithm 1 and §§3–4 / PDF pp. 4–6 | Not all proofs/experiments |
| 16 | Conference PDF, main-text model/assumptions and Theorems 1–2 / PDF pp. 4–7 | Supplementary proof audit excluded |
| 21 | Journal PDF, §2 / PDF p. 3, development/test split | Does not validate arbitrary LF identifiability |

**Retrieval issue:** the requested `web.run` interface was not exposed in this subagent's callable toolset. The available web-search wrapper reported that its configured OpenAI-native backend could not run client-side and used fallback retrieval; the web-extract tool returned a search-only-backend error. Consequently this review does **not** claim to have completed the requested `web.run` transport. It instead checked primary content through browser DOM retrieval and direct in-memory PDF fetch/extraction. Initial local PDF extraction attempts also found missing `requests`/`pdftotext`; an in-memory pypdf loader resolved extraction without installing packages or writing primary papers to the repository. Search snippets were discovery only, not substitutes for the full passages listed above. No new sources or ledger modifications were needed. Source 7 and the landscape survey were not independently rechecked in this bounded pass.

## Disposition

Known: the cited passages were inspected and the attached synthetic checks executed. Assumed: each calculation's explicitly specified population, correct labels and sampling mechanism. Proposed: retain the existing qualifications and require project-specific response/support/calibration evidence. Testable: the attached mathematical examples and future authorized project comparisons. Proven here: only the bounded arithmetic/enumeration outputs, not ER accuracy, operational safety, exhaustive scientific correctness or measured Atlas usefulness.

No canonical edit is proposed on the basis of this review. If the exact requested transport is an acceptance criterion, the parent must supplement the source retrieval using `web.run`; that part remains unmet here.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[3] https://proceedings.mlr.press/v70/guo17a.html — On Calibration of Modern Neural Networks
[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
[16] https://proceedings.neurips.cc/paper_files/paper/2016/file/6709e8d64a5f47269ed5cea9f625f7ab-Paper.pdf — Data Programming: Creating Large Training Sets, Quickly
[17] https://cseweb.ucsd.edu/~elkan/posonly.pdf — Learning Classifiers from Only Positive and Unlabeled Data
[18] https://arxiv.org/abs/0812.4952 — Importance Weighted Active Learning
[21] https://www.vldb.org/pvldb/vol11/p269-ratner.pdf — Snorkel: Rapid Training Data Creation with Weak Supervision
