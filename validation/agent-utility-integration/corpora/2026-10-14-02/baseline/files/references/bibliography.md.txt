# Verified bibliography

The initial pilot used eight verified references; v1.1 adds four scoped references for assignment, transitive clustering, fusion and multifile partitions. Their numbers are stable ledger IDs, not an importance ranking. Failed exploratory IDs 6 and 8 remain excluded. Primary PDFs were retrieved for the additions; reference 9 remains publisher-abstract-only. The repository contains bibliographic/provenance records, not copies of copyrighted papers. See [research notes](research-notes.md), [retrieval status](retrieval-status.json), [retrieval provenance](retrieval-provenance.json), and [evidence policy](evidence-policy.md).

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
