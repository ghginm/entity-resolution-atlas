# Scenario-based stress tests

**Conceptual tests only.** The assumptions below are deliberately hypothetical. No datasets were processed, models trained or ER performance measured. These tests ask whether the Atlas offers selective retrieval, meaningful comparisons, two defensible compositions, relevant evaluation and falsifiable research. Their evidence is the documented decision route, not a numerical benchmark.

## Scenario A — Clean structured data

### Assumed project characteristics and missing facts
Reliable structured identifiers, broadly consistent schemas and modest matching complexity. Assume pairwise cross-source links are the first output; do not assume one row per entity/source. Missing facts: identifier namespace/issuance/reuse, exceptions to reliability, eligibility for one-to-one assignment, label representativeness and the cost of an incorrect link.

### Selective retrieval and decisions
Read domains [01](../taxonomy/domains/01-problem-identity.md) and [03](../taxonomy/domains/03-data-integration.md), then [DEC-05-001](../decisions/candidate-strategy.md), [DEC-06-001](../decisions/comparison-evidence.md) and [DEC-07-001](../decisions/scoring-strategy.md). This locates candidate-key choice, trusted versus missing/conflicting identifier evidence and score complexity without scanning every domain.

| Alternative | Why defensible | Condition / failure to test |
|---|---|---|
| [Exact blocking](../solutions/candidate-generation/exact-blocking.md) and trusted-identifier rule | Simple matches when equality really identifies the target entity | Shared namespace and validity; reused/local IDs can create false links; missing keys lose coverage |
| [Multi-pass](../solutions/candidate-generation/multi-pass-blocking.md) and [additive scoring](../solutions/matching-scoring/additive-soft-matching.md) for residual cases | A complementary key can recover missing identifiers while preserving contribution explanations | Added candidates may be mostly ambiguous collisions; raw weights are not probabilities |
| [Fellegi–Sunter](../solutions/matching-scoring/fellegi-sunter.md) or [logistic](../solutions/matching-scoring/logistic-regression.md) | Data-informed evidence weighting when residual error modes justify it | Estimated distributions or adequate representative labels; no presumed advantage over the simple rule |

### Two candidate architectures
1. **A1 — AR-01 linear baseline:** integrated identifiers with namespace/validity → exact candidates → explicit evidence states → validated identifier rule → pairwise links plus [abstention](../solutions/decision-resolution/thresholds-abstention.md) on conflict. Batch; no clustering required. [AR-01](../architectures/linear-modular.md) supplies contracts. Hard rules are a documented family, not a full pilot Solution Card.
2. **A2 — AR-02 plus AR-03 residual cascade:** exact-key pass plus justified secondary pass → candidate union → early trusted-identifier route → interpretable additive scorer for unresolved pairs → conservative threshold/review policy. Batch; the pairwise output remains unchanged. [AR-02](../architectures/recall-multi-pass.md) and [AR-03](../architectures/precision-cascade.md) expose added coverage, early-exit risk and cost.

A2 is justified only if the independent reference reveals missed-identifier matches. One-to-one assignment is an optional replacement after cardinality is established, not an automatic cleanup step.

### Evaluation and high-information research
Use [candidate recall](../evaluation/candidate-recall.md) with positives found independently of the keys, and [pairwise/calibration diagnostics](../evaluation/pairwise-calibration.md) with identifier-missing/reused slices and operating-cost guardrails. Calibration is irrelevant to a purely Boolean trusted rule, but becomes necessary before probability-based cost thresholds. If memberships are later required, add [entity evaluation](../evaluation/entity-resolution-quality.md).

[HYP-07-001](../research/hypotheses/contextual-reliability.md) is informative if residual false positives involve shared contacts or field/source reliability differences. [HYP-06-001](../research/hypotheses/frequency-aware-evidence.md) is useful only if names are doing meaningful residual matching. Hold candidates and downstream policy fixed, compare the added evidence and guard identifier-conflict errors. With no such residual opportunity, defer these experiments rather than declaring universal high priority.

### Gap revealed
No complete pilot card yet for identifier semantics, hard rules or assignment. Domain maps/AR-05 expose the choices but deeper primary-supported methods are needed before an implementation recommendation. This gap changes expansion sequence, not the clean-data baseline.

## Scenario B — Noisy multilingual data

### Assumed project characteristics and missing facts
Sparse attributes, inconsistent names across scripts, transliteration problems and limited labels. Assume raw script and observation provenance can be retained. Missing facts: languages/scripts, acceptable transliteration variants, source coverage, parse reliability, identity versus household relationships, independent positive reference and review capacity.

### Selective retrieval and comparisons
Read [04](../taxonomy/domains/04-normalization-enrichment.md) plus the same three Decision Cards; retrieve evidence states, both blocking cards and the additive/FS cards. Compare exact canonical keys, multiple conservative representations and approximate retrieval families from DEC-05-001. Approximate/ANN methods remain taxonomy-level alternatives, not fully specified pilot solutions.

- Exact keys are cheap and auditable, but cross-script mismatches can prevent any comparison.
- Multiple raw/normalized/transliterated passes could recover distinct variation modes; destructive single-string canonicalization and correlated duplicate evidence are risks.
- Explicit missing/invalid/conflict states preserve uncertainty; maximizing similarity over many aliases can increase accidental agreements and needs count/quality context.
- FS supplies estimated evidence under stated distribution/dependence assumptions; limited labels do not make unsupervised estimation assumption-free. Additive manual weights are a legitimate baseline. Logistic requires a representative labeled subset, not merely plentiful synthetic negatives.

### Two candidate architectures
1. **B1 — AR-01 conservative interpretable baseline:** the [linear pattern](../architectures/linear-modular.md) composes provenance-preserving raw plus restrained normalized/variant forms → simple exact/composite candidates → [evidence states](../solutions/comparison-features/evidence-states.md) → expert additive score → thresholds/abstention and review. Batch; pair links or explicitly provisional memberships, no unqualified transitive merge.
2. **B2 — AR-02 richer retrieval with FS:** the [multi-pass pattern](../architectures/recall-multi-pass.md) composes distinct raw/parsed/validated transliteration passes → unique union with pass provenance → grouped comparison states → FS with declared estimation population → abstention/representative review. Batch, optionally an [AR-03](../architectures/precision-cascade.md) expensive route only for unresolved cases after early exits are independently audited.

B2 addresses retrieval failure; it does not claim FS fixes language normalization. Compare the scorers on shared candidates separately from the end-to-end multi-representation change. Adding ANN is an optional challenger only after the representation and retrieval budget can be objectively evaluated.

### Evaluation and research
Measure independent candidate coverage on cross-script and sparse-field positives, marginal pass cost, pairwise operating points and final memberships when applicable. Retrieve [candidate recall](../evaluation/candidate-recall.md), [pairwise quality/calibration](../evaluation/pairwise-calibration.md) and [entity quality](../evaluation/entity-resolution-quality.md); segment by source/language/script/missingness and account for dependent records and label uncertainty. Do not call unannotated cross-script candidates negatives.

Frequency evidence [HYP-06-001](../research/hypotheses/frequency-aware-evidence.md) could distinguish common-name collisions, but frequencies must correspond to relevant language/source populations and avoid rare-variant overconfidence. Contextual reliability [HYP-07-001](../research/hypotheses/contextual-reliability.md) could separate a personal identifier/contact from shared or poorly parsed evidence. Their experiments use fixed candidates and entity-disjoint held-out evaluation with predeclared practical benefit and segment guardrails; changing transliteration concurrently would confound attribution.

### Gap revealed
Language-specific normalization, phonetic methods, approximate indexing and probabilistic variants need deeper evidence. Limited-label/annotation design is currently methodology guidance rather than a full label-acquisition card. The Atlas can compare hypotheses and coherent patterns, but cannot honestly name one best multilingual algorithm.

## Scenario C — Large heterogeneous multi-source data

### Assumed project characteristics and missing facts
Many source combinations, costly false merges, compute constraints and ongoing updates. Assume the desired output includes maintained entity membership; sources may contain repeated observations. Missing facts: block-degree/skew tails, true cardinality constraints, source-pair labels, change/deletion timing, downstream ID stability, privacy/access and tolerated reconciliation lag.

### Decisions and alternatives
Retrieve candidate/evidence/scoring decisions; then [AR-02](../architectures/recall-multi-pass.md), [AR-03](../architectures/precision-cascade.md), [AR-05](../architectures/collective-consistency.md) and [AR-06](../architectures/incremental-continuous.md). Read domains [08](../taxonomy/domains/08-decision-resolution.md), [09](../taxonomy/domains/09-master-maintenance.md) and [13](../taxonomy/domains/13-scalability-execution.md) for missing membership/state/physical-execution detail.

| Choice | Plausible reason | Main risk |
|---|---|---|
| Broad complementary candidates versus exact narrow keys | Recover difficult source-pair matches | Shared frequent keys and caps cause explosion or hidden recall loss |
| Uniform FS/additive versus cheap-first logistic cascade | Comparable baseline versus concentrating compute where needed | Early terminal errors, shifted remaining population and insufficient labels per source pair |
| Independent pair decisions versus constrained membership | Keep simple comparator versus prevent invalid/catastrophic entity merges | Wrong constraints exclude true identities; one-to-one is not justified merely by having two sources |
| Batch recomputation versus incremental affected updates | Clear replay comparator versus lower change-processing work | Incorrect dependency closure, stale indexes, historical mistakes, ID instability |

### Two candidate architectures
1. **C1 — Batch AR-02 plus AR-05:** complementary blocking with recorded omissions/budgets → evidence states → FS or additive baseline → conservative abstention → only semantically justified constrained membership → virtual/hybrid entities with lineage. Uniform scoring makes component comparison easier; no cardinality constraints are invented.
2. **C2 — AR-06 with AR-02/AR-03/AR-05:** changes/deletions → affected dependency search and multi-pass candidates → audited early trusted-evidence route → regularized logistic for the remaining population if labels support it → calibrated contextual policy → constrained membership changes with reversible merge/split and versioned IDs → periodic batch reconciliation. Higher operational complexity is accepted only if quality/review/compute comparisons justify it.

AR-04 is a further alternative for disagreement-driven review, not automatically an accuracy improvement. Connected components are a useful simplicity comparator only with explicit bridge-error diagnostics; they are not the assumed production resolver.

### Evaluation and high-information research
Use [candidate recall](../evaluation/candidate-recall.md) for independent coverage/marginal cost by source pair and block tail; [pairwise quality/calibration](../evaluation/pairwise-calibration.md) for representative pair and early-exit analysis at comparable policy costs; and [entity quality](../evaluation/entity-resolution-quality.md) for overmerge/undermerge, large-merge harms, constraint violations and review load. Include index-build/update costs, latency distributions and arrival/deletion replay. Full batch output is a **comparator**, not ground truth; both must be evaluated against an independent reference.

Contextual reliability [HYP-07-001](../research/hypotheses/contextual-reliability.md) targets demonstrated source/field collisions, with pooled/shrinkage comparison when per-source labels are sparse. Frequency evidence [HYP-06-001](../research/hypotheses/frequency-aware-evidence.md) targets shared-value collisions without treating a whole source as one homogeneous population. Hold candidate and resolver controls fixed first; then test end-to-end behavior and a quality–cost frontier. Negative or inconclusive results can reveal that budgeted retrieval or incorrect constraints, rather than scorer weights, are the binding limitation.

### Gap revealed
Detailed distributed/skew execution, stable-ID/split semantics, streaming out-of-order updates, constrained-resolution algorithms and privacy threat models need deeper cards. Architecture contracts support coherent designs but are not production correctness proofs.

## Stress-test conclusion and next gate
All three routes offer a simple baseline, materially different alternatives, at least two composable configurations, layered evaluation and conditional research opportunities. The alternatives change with the assumed problem rather than recommending the same complex matcher everywhere. The test also identifies explicit limits: language-specific preparation/retrieval, identity/cardinality, labeling under incomplete truth, membership/master maintenance and system/privacy execution are not fully researched pilot solutions.

Use the [expansion plan](expansion-plan.md) to review those gaps. These conceptual walkthroughs show decision-support coverage; they neither predict numerical performance nor replace an experiment on a real project's data.
