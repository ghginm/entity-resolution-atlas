# Verified bibliography

The initial pilot used eight verified references; v1.1 added four for assignment, transitive clustering, fusion and multifile partitions. Wave 1 adds eight primary/official references for sampling, weak/active supervision, incomplete truth and behavioral/experimental design. Numbers are stable ledger IDs, not importance rankings. Failed exploratory IDs 6 and 8 remain excluded; reference 9 remains publisher-abstract-only. This repository retains bibliographic/provenance records, not copyrighted papers. See [historical research notes](research-notes.md), [Wave 1 evidence scopes](wave-1-evidence-notes.md), [retrieval status](retrieval-status.json), [retrieval provenance](retrieval-provenance.json), and [evidence policy](evidence-policy.md).

| Reference | Bibliographic identification | Support used / limits |
|---|---|---|
| [1] | Ivan P. Fellegi and Alan B. Sunter. *A Theory for Record Linkage*. Journal of the American Statistical Association 64(328), 1183–1210, December 1969. IPUMS-hosted reprint. | Likelihood-ratio theory, conditional-independence simplification, error-controlled three-way dispositions and blocking. Not universal probability calibration or entity clustering optimality. |
| [2] | George Papadakis, Dimitrios Skoutas, Emmanouil Thanos and Themis Palpanas. *A Survey of Blocking and Filtering Techniques for Entity Resolution*. arXiv:1905.06167; retrieved manuscript dated August 2020. | Retrieval taxonomy, blocking/filtering distinctions and metric concepts. The manuscript contains a placeholder DOI, deliberately not copied. |
| [3] | Chuan Guo, Geoff Pleiss, Yu Sun and Kilian Q. Weinberger. *On Calibration of Modern Neural Networks*. Proceedings of ICML, PMLR 70, 2017. | Calibration and post-processing concepts; empirical image/document classification context, not an ER superiority result. |
| [4] | Olivier Binette, Youngsoo Baek, Siddharth Engineer, Christina Jones, Abel Dasylva and Jerome P. Reiter. *How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation*. arXiv:2404.05622v1, April 2024. | Entity-centric labeling, sampling-aware metric estimation and diagnostics. Inventor disambiguation and simulations; not a universal solution to incomplete truth. |
| [5] | Olivier Binette and Rebecca C. Steorts. *(Almost) All of Entity Resolution*. arXiv:2008.04443v3, retrieved January 2022 version. | Broad statistical/ER landscape. Used for orientation, not evidence that an Atlas hypothesis has been proven. |
| [7] | Trevor Hastie, Robert Tibshirani and Jerome Friedman. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, second edition, February 2009; author-hosted corrected twelfth printing, January 2017. | Chapter 4.4 logistic modeling/estimation and additive-model foundations. General statistics, not empirical ER ranking. Author site supplies a Google Drive download redirect. |
| [9] | Indrajit Bhattacharya and Lise Getoor. *Collective Entity Resolution in Relational Data*. ACM Transactions on Knowledge Discovery from Data 1(1), 2007. | Publisher abstract: motivation for joint resolution using relational co-occurrence. Full author-hosted text access failed; detailed experiments are not claimed reviewed. |
| [10] | Indrajit Bhattacharya and Lise Getoor. *Online Collective Entity Resolution*. AAAI, 2007. | Primary full paper on adaptive query-time collective resolution in publication databases. It does not establish that generic incremental updates preserve batch quality. |
| [11] | Mauricio Sadinle. *Bayesian Estimation of Bipartite Matchings for Record Linkage*. arXiv:1601.06630v1, January 2016. | Duplicate-free-file assumption, maximum one-to-one matching, assignment objective assumptions and unresolved estimates. The inspected preprint is identified explicitly; no universal gain or independent-pair probability interpretation is transferred. |
| [12] | Oktie Hassanzadeh, Fei Chiang, Hyun Chul Lee and Renée J. Miller. *Framework for Evaluating Clustering Algorithms in Duplicate Detection*. VLDB 2009 paper. | Section 2.1 defines connected components/transitive closure and contrasts other grouping mechanisms. Its synthetic string-corruption comparisons do not establish the best high-harm resolver for an unfamiliar project. |
| [13] | Jens Bleiholder and Felix Naumann. *Data Fusion*. ACM Computing Surveys 41(1), Article 1, **December 2008**, 41 pages; DOI 10.1145/1456650.1456651. | Published article retrieved from an academic teaching host. Sections 2–2.5 separate object identification from attribute fusion and classify conflict strategies. Persistent-ID lifecycle policies in Atlas are design synthesis, not attributed guarantees. |
| [14] | Serge Aleshin-Guendel and Mauricio Sadinle. *Multifile Partitioning for Record Linkage and Duplicate Detection*. arXiv:2110.03839v1, October 2021. | Partition representation, file-specific duplication/overlap assumptions and partial estimates. Source-cardinality constraints can be encoded in this model; it does not validate Atlas's illustrative greedy feasible-merge baseline or organization continuity rules. |

## Wave 1 additions
Acquisition, estimation, weak-label, experiment and behavioral-test references added in Wave 1:

| Reference | Bibliographic identification | Support used / limits |
|---|---|---|
| [15] | Statistics Canada. *Survey Methods and Practices*, Catalogue 12-587-X, 2010 electronic edition; originally published October 2003. | Selected chapters 6–7 on probability designs, weights, nonresponse and variance. Not measured ER acquisition benefits. |
| [16] | Alexander J. Ratner, Christopher M. De Sa, Sen Wu, Daniel Selsam and Christopher Ré. *Data Programming: Creating Large Training Sets, Quickly*. NeurIPS 2016. | Sections 3–5, restrictive label-model and learning assumptions; supplementary proofs not reviewed. Not arbitrary LF identifiability or ER superiority. |
| [17] | Charles Elkan and Keith Noto. *Learning Classifiers from Only Positive and Unlabeled Data*. KDD 2008, author-hosted paper. | SCAR conditional probability identity and distinction between single-sample/case-control data. Unknown propensity is not automatically identified. |
| [18] | Alina Beygelzimer, Sanjoy Dasgupta and John Langford. *Importance Weighted Active Learning*. arXiv:0812.4952v4, May 20, 2009. | Randomized querying/weighting under stated assumptions; not generic ER acquisition guarantees. |
| [19] | T. Y. Chen, S. C. Cheung and S. M. Yiu. *Metamorphic Testing: A New Approach for Generating Next Test Cases*. Technical Report HKUST-CS98-01, 1998. | Domain-conditional follow-up testing without complete oracle. ER properties are Atlas synthesis. |
| [20] | NIST/SEMATECH e-Handbook of Statistical Methods. *Two-level full factorial designs*, official page as retrieved. | Factor combinations and interaction analysis; not deployment causality or ER gains. |
| [21] | Alexander Ratner and colleagues. *Snorkel: Rapid Training Data Creation with Weak Supervision*. PVLDB 11(3), 2017. | Aggregation, training and controlled development/blind tests; no transfer of application gains to ER. |
| [22] | Hypothesis maintainers. *Introduction to Hypothesis*, official documentation identifying version 6.169.1 at retrieval. | Property-based inputs/assertions and valid input domains; not a library or language prescription. |

## Wave 2 additions

Six bounded engineering references support distinctions, not a recommended tool stack or measured ER gains. See [Wave 2 evidence notes](wave-2-evidence-notes.md).

| Reference | Bibliographic identification | Support used / limits |
|---|---|---|
| [23] | Object Management Group. *Decision Model and Notation*, version 1.5, formal/24-01-01; PDF title page January 2024. | Hit policies/default outputs, sections 8.2.11–8.2.12. Version-pinned illustration, not a latest-version or implementation-conformance claim. |
| [24] | DVC maintainers. *Running Pipelines*, official live documentation as retrieved. | DAG order and reuse based on declared dependencies/commands/parameters. No automatic complete dependency discovery or ER accuracy guarantee. |
| [25] | W3C. *PROV Model Primer*, Working Group Note, 30 April 2013. | Data entities, activities, responsibility and derivation; not same-as ER ontology or AI-agent orchestration. |
| [26] | MLflow maintainers. *MLflow Model Registry*, documentation pinned to 3.3.1. | Versions, mutable aliases, tags and lineage; a tag is not a validation result or a complete release bundle. |
| [27] | Martin Fowler. *RulesEngine*, author-maintained design essay as retrieved. | Production rules and chaining cautions; explicitly nonrepresentative experiences are not framework failure-rate evidence. |
| [28] | Martin Fowler. *Event Sourcing*, author-maintained design essay as retrieved. | Reconstructable state, materialized current state, replay and external-effects caveats; no ER identity or automatic reversibility guarantee. |

## Wave 3 additions

Twelve bounded references support representations, comparison mechanisms and selected retrieval/constraint alternatives. See [Wave 3 evidence scopes](wave-3-evidence-notes.md); the earlier author-provided ESL text was also revisited at sections 9.1, 9.2 and 10.10 for general additive/tree/boosting mechanisms.

| Reference | Bibliographic identification | Support used / limits |
|---|---|---|
| [29] | William E. Winkler. *String Comparator Metrics and Enhanced Decision Rules in the Fellegi-Sunter Model of Record Linkage*, 1990 primary paper, academic-hosted copy. | Partial comparison, EM/parameter variants, frequency weights and dependencies; Census-specific comparisons, not a universal weight recipe. |
| [30] | William E. Yancey. *An Adaptive String Comparator for Record Linkage*, Census Research Report 2004-02. | Variable edit costs learned from Census names; no multilingual or deployment guarantee. |
| [31] | William E. Yancey. *Evaluating String Comparator Performance for Record Linkage*, Census Research Report 2005-05. | Jaro-style adjustment and hybrid comparison plus Bigmatch contrast; data/configuration-limited findings. |
| [32] | Unicode Consortium. *UAX 15: Unicode Normalization Forms*, received revision 58 identifying Unicode 18.0.0, 2026-08-12. | Canonical/compatibility normalization and semantic-loss warning; character equivalence is not identity. |
| [33] | Unicode Consortium. *UAX 24: Unicode Script Property*, received revision 41 identifying Unicode 18.0.0, 2026-08-28. | Script and Script_Extensions/combining/mixed-script semantics; not language identification or transliteration. Ledger title is preserved as originally registered. |
| [34] | US National Archives. *Soundex System*, official guide as retrieved. | Historical surname coding rules; no universal phonetic or ER accuracy evidence. |
| [35] | Andrew McCallum, Kamal Nigam and Lyle H. Ungar. *Efficient Clustering of High-Dimensional Data Sets with Application to Reference Matching*, KDD 2000. | Cheap overlapping canopy construction and expensive-stage restriction; distance-preservation assumptions remain necessary. |
| [36] | Ralph Peeters, Aaron Steiner and Christian Bizer. *Entity Matching using Large Language Models*, arXiv:2310.11244v4 (18 October 2024); received text identifies EDBT 2025 publication. | Product/bibliographic benchmark setup and prompt/model sensitivity; cost/runtime are historical snapshots, not current estimates. |
| [37] | Kiri Wagstaff and Claire Cardie. *Clustering with Instance-level Constraints*, ICML 2000, author-hosted full paper. | Hard must/cannot constraints and COP-COBWEB; not the distinct COP-k-means algorithm or ER outcome evidence. |
| [38] | Author-hosted *Mining of Massive Datasets*, chapter 3, *Finding Similar Items*, received 59-page chapter. | MinHash/banding and set-cardinality/prefix exposition; no edition claim or identity-recall guarantee. |
| [39] | Mauricio A. Hernández and Salvatore J. Stolfo. *Real-world Data is Dirty: Data Cleansing and The Merge/Purge Problem*. Data Mining and Knowledge Discovery 2, 9–37 (1998), primary article via external mirror. | Key/sort/window and key-error reasoning; mirror and transport provenance disclosed. |
| [40] | Andrei Z. Broder. *On the resemblance and containment of documents*, 1997 primary paper, academic-course-hosted copy. | Document-set resemblance/sampling and hash-collision caveats; not a match-probability or ER recall theorem. |

## Reuse discipline
A verified title or mathematical model is not a measured gain on an unfamiliar project. Keep each cited claim within source scope; architecture contracts, suggested experiments and hypothetical scenarios are Atlas synthesis. Literature classification can guide which alternatives exist; primary mechanism/guarantee checks are required before expanding detailed methods. No performance numbers have been copied into this pilot as universal forecasts.

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
[2] https://arxiv.org/abs/1905.06167 — A Survey of Blocking and Filtering Techniques for Entity Resolution
[3] https://proceedings.mlr.press/v70/guo17a.html — On Calibration of Modern Neural Networks
[4] https://arxiv.org/abs/2404.05622 — How to Evaluate Entity Resolution Systems: An Entity-Centric Framework with Application to Inventor Name Disambiguation
[5] https://arxiv.org/abs/2008.04443 — (Almost) All of Entity Resolution
[7] https://hastie.su.domains/ElemStatLearn/main.html — The Elements of Statistical Learning, second edition
[9] https://dl.acm.org/doi/10.1145/1217299.1217304 — Collective Entity Resolution in Relational Data
[10] https://cdn.aaai.org/AAAI/2007/AAAI07-255.pdf — Online Collective Entity Resolution
[11] https://arxiv.org/abs/1601.06630 — Bayesian Estimation of Bipartite Matchings for Record Linkage
[12] https://www.vldb.org/pvldb/vol2/vldb09-1025.pdf — Framework for Evaluating Clustering Algorithms in Duplicate Detection
[13] https://www.bioinf.jku.at/teaching/ss2011/se-inf/data_fusion_a1-bleiholder.pdf — Data fusion
[14] https://arxiv.org/abs/2110.03839 — Multifile Partitioning for Record Linkage and Duplicate Detection
[15] https://www150.statcan.gc.ca/n1/pub/12-587-x/12-587-x2003001-eng.pdf — Survey Methods and Practices
[16] https://proceedings.neurips.cc/paper_files/paper/2016/file/6709e8d64a5f47269ed5cea9f625f7ab-Paper.pdf — Data Programming: Creating Large Training Sets, Quickly
[17] https://cseweb.ucsd.edu/~elkan/posonly.pdf — Learning Classifiers from Only Positive and Unlabeled Data
[18] https://arxiv.org/abs/0812.4952 — Importance Weighted Active Learning
[19] https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf — Metamorphic Testing: A New Approach for Generating Next Test Cases
[20] https://www.itl.nist.gov/div898/handbook/pri/section3/pri3331.htm — NIST/SEMATECH e-Handbook: Two-level full factorial designs
[21] https://www.vldb.org/pvldb/vol11/p269-ratner.pdf — Snorkel: Rapid Training Data Creation with Weak Supervision
[22] https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html — Hypothesis: Introduction to property-based testing
[23] https://www.omg.org/spec/DMN/1.5/PDF — Decision Model and Notation, version 1.5
[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
[25] https://www.w3.org/TR/prov-primer — PROV Model Primer
[26] https://mlflow.org/docs/3.3.1/ml/model-registry — MLflow Model Registry (3.3.1)
[27] https://martinfowler.com/bliki/RulesEngine.html — RulesEngine
[28] https://martinfowler.com/eaaDev/EventSourcing.html — Event Sourcing
[29] https://www.stat.cmu.edu/NCRN/PUBLIC/RLClassFiles/HW/Winkler1990.pdf — String Comparator Metrics and Enhanced Decision Rules in the Fellegi-Sunter Model of Record Linkage
[30] https://www.census.gov/content/dam/Census/library/working-papers/2004/adrm/rrs2004-02.pdf — An Adaptive String Comparator for Record Linkage
[31] https://www.census.gov/content/dam/Census/library/working-papers/2005/adrm/rrs2005-05.pdf — Evaluating String Comparator Performance for Record Linkage
[32] https://www.unicode.org/reports/tr15 — Unicode Normalization Forms (UAX 15)
[33] https://www.unicode.org/reports/tr24 — Unicode Script Extension Properties (UAX 24)
[34] https://www.archives.gov/research/census/soundex.html — NARA Soundex Coding Guide
[35] http://www.kamalnigam.com/papers/canopy-kdd00.pdf — Efficient Clustering of High-Dimensional Data Sets with Application to Reference Matching
[36] https://arxiv.org/abs/2310.11244 — Entity Matching using Large Language Models
[37] https://wkiri.com/research/papers/wagstaff-constraints-00.pdf — Clustering with Instance-level Constraints
[38] http://infolab.stanford.edu/~ullman/mmds/ch3.pdf — Mining of Massive Datasets: Finding Similar Items (author-hosted chapter 3)
[39] https://creatingfutureus.org/wp-content/uploads/2021/10/Hernandez-and-Stolfo-1998.pdf — Real-world Data is Dirty: Data Cleansing and The Merge/Purge Problem
[40] https://www.cs.princeton.edu/courses/archive/spring13/cos598C/broder97resemblance.pdf — On the resemblance and containment of documents
