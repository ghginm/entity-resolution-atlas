# Wave 1 verified evidence and scope notes

## Retrieval and use boundary

Sources 15–22 were retrieved as primary PDFs or official documentation pages through direct HTTPS and reviewed in the selected scopes below. This repository retains bibliographic identity, scope and received-byte hashes in [retrieval provenance](retrieval-provenance.json), not full source texts.

The ledger's access dates use local 2026-10-13; provenance records the UTC retrieval date 2026-10-14. That difference is timezone bookkeeping, not a source-version discrepancy. Full-text availability means selected sections could be examined, not that every theorem, supplement or empirical result was independently reproduced.

## Sources checked

| Ledger ID | Retrieved primary work / version | Support used | Deliberate limit |
|---|---|---|---|
| 15 | Statistics Canada, *Survey Methods and Practices*, Catalogue 12-587-X; 2010 electronic edition, originally October 2003 | Selected chapters 6–7: probability/nonprobability designs, stratification, inclusion weights, nonresponse assumptions, totals/proportions, variance and replication.[15] | General survey principles, not empirical ER gains. Algebraic ER adaptations explicitly define fixed outcomes and sampling assumptions. |
| 16 | Ratner, De Sa, Wu, Selsam and Ré, *Data Programming: Creating Large Training Sets, Quickly*, NeurIPS 2016 | Sections 3–5, equations 1–9, Theorems 1–2 and application comparisons: LF aggregation, noise-aware fitting, restrictive independent/dependent-model conditions.[16] | Supplementary proofs not reviewed. Displayed theorem conditions are not universal practical prerequisites for all LF systems. No paper gain transferred to ER. |
| 17 | Elkan and Noto, *Learning Classifiers from Only Positive and Unlabeled Data*, KDD 2008, author-hosted PDF | Section 2 and beginning of section 3: correct positive labels, constant positive-label propensity, conditional probability factorization; single sampled population versus case-control data.[17] | The factorization alone does not identify unknown propensity or validate the paper's proposed estimator for arbitrary overlapping distributions. No automatic PU metric correction. |
| 18 | Beygelzimer, Dasgupta and Langford, *Importance Weighted Active Learning*, arXiv:0812.4952v4, May 20, 2009 | Full extracted paper with focus on sections 2–4 and 7: randomized query probabilities, importance weights, bounded-loss/finite-class safety assumptions and separate loss-weighting analysis.[18] | Not a guarantee for deterministic uncertainty, disagreement, diversity or cluster-risk ER heuristics; conditional query probability is not arbitrary unique-unit inclusion. |
| 19 | Chen, Cheung and Yiu, *Metamorphic Testing: A New Approach for Generating Next Test Cases*, HKUST-CS98-01, 1998 | Abstract, introduction, preliminaries, domain-conditional examples and conclusion: follow-up relations without a complete oracle.[19] | Supports testing concepts, not the proposed ER properties, representative synthetic populations or world accuracy. |
| 20 | Official NIST/SEMATECH e-Handbook page, *Two-level full factorial designs* | Factor combinations, design and analysis matrices, replication example and interaction columns.[20] | ER interaction contrasts remain Atlas reasoning on a specified response scale; no deployment causal guarantee or ER advantage. |
| 21 | Ratner and colleagues, *Snorkel: Rapid Training Data Creation with Weak Supervision*, PVLDB 11(3), 2017 | Section 2 including 2.1–2.3, sections 3.1–3.2, section 4.1 including 4.1.1–4.1.4: aggregation, fitting, modeling tradeoffs, development and blind held-out tests.[21] | Does not establish calibration, identifiability or superiority for arbitrary ER LFs, copied sources or unsupported populations. |
| 22 | Official Hypothesis introduction; retrieved page identifies documentation version 6.169.1 | Strategies/assertions, reference equivalence, domain-restriction counterexample and complementary role beside example tests.[22] | Used as author-maintained conceptual documentation, not a recommendation to install a library or prescribe a programming language. |

## Reused foundation and explicit Atlas reasoning

Source 4's arXiv v1 sections 3.2–3.4 were revisited for prediction-assisted entity search, record-induced entity sampling and ratio estimation.[4] Its original URL/ID and historical provenance are preserved. A reviewed source is not an independent execution of its methods.

Hybrid pool separation, annotation provenance, abstention handling, source-risk heuristics, experimental controls, ER-specific metamorphic examples and adoption rules are Atlas synthesis. Conditional sampling identities, finite-reference bounds, HT expectation/covariance and zero-event combinatorics are displayed as mathematical reasoning with explicit assumptions, not attributed empirical results. Limited numerical enumeration sanity checks were performed during authoring; they are not required evidence for the displayed arguments and do not prove estimator coverage, perform ER or measure agent usefulness.

No label collection, ER dataset processing, model training, ER experiment or agent-utility evaluation of these additions was performed. Results from other corpora cannot establish their utility.

## Sources

[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
[16] https://proceedings.neurips.cc/paper_files/paper/2016/file/6709e8d64a5f47269ed5cea9f625f7ab-Paper.pdf — Data Programming: Creating Large Training Sets, Quickly
[17] https://cseweb.ucsd.edu/~elkan/posonly.pdf — Learning Classifiers from Only Positive and Unlabeled Data
[18] https://arxiv.org/abs/0812.4952 — Importance Weighted Active Learning
[19] https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf — Metamorphic Testing: A New Approach for Generating Next Test Cases
[20] https://www.itl.nist.gov/div898/handbook/pri/section3/pri3331.htm — NIST/SEMATECH e-Handbook: Two-level full factorial designs
[21] https://www.vldb.org/pvldb/vol11/p269-ratner.pdf — Snorkel: Rapid Training Data Creation with Weak Supervision
[22] https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html — Hypothesis: Introduction to property-based testing
