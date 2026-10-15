---
id: SOL-07-005
type: solution
title: Select nonlinear, embedding and language-model comparators
domain: "07"
summary: >-
  Compare additive nonlinear models, boosted trees, ranking objectives,
  embeddings and language-model pair comparators against interpretable logistic,
  likelihood-ratio and rule baselines. Requires an explicit output role, admissible
  data access and evaluation evidence suited to the claimed population. Richer
  models can represent interactions or textual variation unavailable to a small
  feature basis, but can also learn shortcuts, confuse relatedness with identity,
  increase cost and fail under shift. Complexity is an experimental choice,
  not a maturity ladder.
tags: [rich-labels, few-labels, compute-intensive, pairwise, calibration, uncertainty, privacy, experimentation]
maturity: context-dependent
evidence: supported-by-external-literature
relations:
  addresses: [DEC-07-001]
  alternative_to: [SOL-07-002, SOL-07-003]
  complements: [SOL-10-004, DEC-12-001]
  evaluated_by: [EVAL-11-002, EVAL-11-005, EVAL-11-003]
---

# Select nonlinear, embedding and language-model comparators

## Short summary and problem addressed

Use a richer comparator only when a diagnosed limitation warrants it. The same apparent scoring error may originate in normalization, absent candidates, ambiguous identity semantics or biased labels. A neural classifier cannot recover an omitted pair it never sees, and a more flexible model cannot establish accuracy from its own weak labels. [Logistic regression](logistic-regression.md), [FS](fellegi-sunter.md), exact rules and expert additive scoring remain credible baselines.

## Core mechanisms, theoretical explanation and variants

### Additive nonlinear and constrained models

An additive logistic model replaces a linear feature effect with a fitted function while retaining an additive logit. This can represent saturation or a nonuniform response to edit similarity without learning every interaction. ESL section 9.1 explains the additive formulation and smoothing/centering constraints.[7] Optional interactions are explicit departures from a main-effects model.

**Atlas synthesis:** a justified monotone constraint can prevent similarity increases from lowering a feature's contribution at fixed other inputs. It is not universally correct: high overlap on common organization boilerplate can behave differently from rare-name overlap, and invalid values require separate evidence states. Constraints encode assumptions, not independently established identity facts. This wave did not verify a specialist constrained-ER implementation or its guarantees.

### Boosted trees and interactions

Trees partition feature space using conditional splits; a boosted ensemble adds trees fitted toward reduction of a specified loss. Tree depth, iteration count and regularization govern flexibility and cost. ESL sections 9.2 and 10.10 describe trees and gradient boosting.[7] A model can capture, for example, name similarity behaving differently with a missing identifier, without manually specifying every interaction.

A large ensemble is less transparent than a small additive model; feature-attribution output does not prove causal reliability. Rare-source partitions, annotation artifacts and overfitting remain risks. A probability-producing loss does not certify calibration on shifted candidates. Guo et al. supply non-ER evidence about calibration of neural classifiers, not a universal post-processing guarantee for trees or ER.[3]

### Learning to rank

**Atlas synthesis, bounded coverage:** a query- or record-conditioned ranking objective can train ordering among candidate partners. Its natural evaluation unit is a candidate list, not an unconstrained collection of calibrated pair probabilities. Negative sampling and list construction define what the ranker learns; top-ranked does not mean a true partner exists. Specify a no-match/review policy and cardinality assumptions. This wave provides a role comparison, not a verified specialist ranking algorithm or universal ranking-to-probability conversion.

### Embeddings and language models

An encoder maps record text to vectors; vector similarity may generate candidates or become a comparison feature. Retrieval recall at a budget and pair discrimination are different targets. Similar vectors can mean topical, commercial or organizational relatedness rather than strict identity. Record serialization, model/version, truncation and normalization are part of the evidence contract.

A pairwise language model consumes two descriptions jointly and predicts a label or score; a generative LLM uses a prompt and parsed response. These need not share the retrieval encoder's representation or cost. Peeters, Steiner and Bizer compare hosted/local generative LLMs with PLM baselines on product and bibliographic benchmarks, including prompting, examples and fine-tuning. Their prompt-sensitivity and transfer findings depend on model/dataset configuration; there is no universally best prompt in their experiments.[36] This is external benchmark evidence, not proof for persons, regulated identifiers or the consumer's source mixture.

## Assumptions, prerequisites and applicability

Declare whether the output is a rank, similarity, model probability, abstention or rule recommendation. Labels must match the identity target and independently support the operating slices. Small labels can support narrow experiments or error exploration; they do not automatically validate a high-capacity model. [Weak supervision](../ground-truth/weak-supervision.md) may supply training signals, but evaluating on the generating rules measures imitation rather than independent improvement.

Language models additionally need authorized data access, a pinned model/prompt/serialization, explicit handling of timeouts, refusals and unparsable responses, and a repeatability policy. Never turn a failed required check into a negative identity label. External API use, sensitive identifiers, retention and embeddings require project authorization. Local inference changes access risks and cost; it is not by itself a privacy guarantee.

## Advantages, trade-offs and failure modes

Richer models can express nonlinearities, interactions and textual correspondences missing from a small explicit feature basis. Whether that helps is empirical. Added burdens include tuning data, accelerator or API cost, latency, index maintenance for embeddings, version drift and debugging. Source-specific shortcuts and copied training/test entities can create misleading results. A semantic comparator may merge a parent with a subsidiary because their descriptions are related.

An LLM's explanation is an account of its answer, not independent verification that the identity is correct. Response order, prompt wording and serialization can change behavior. Treat record text as untrusted data rather than executable instructions, test output parsing, and separate generated identity claims from trusted constraints. Cache keys must include model/prompt and all evidence versions. The source's historical API-price/runtime figures are not current estimates; section 5 explicitly treats them as snapshots.[36]

## Relationships and how to evaluate

Use [controlled comparisons](../experimentation/controlled-comparison.md) with fixed candidates, immutable inputs and independent fitting/calibration/test partitions. Match label budget, allowable context, tuning effort and policy-selection protocol; report remaining differences rather than pretend unlike models have equal capacity. Compare regularized logistic first, a chosen nonlinear family second, and selective expensive verification only where justified.

[Pairwise evaluation](../../evaluation/pairwise-calibration.md) checks ranking, proper scoring rules, threshold costs and calibration separately. For a selective verifier report gate coverage, whole-pipeline errors and total cost, not just accuracy on cases it accepted. For retrieval report omitted true matches independently; for changed edge decisions measure [entity outcomes](../../evaluation/entity-resolution-quality.md). Slice unseen identities, sources, languages, rare qualifiers and difficult nonmatches. Prompt selection is development, never tuning on the final test set.

[Incomplete reference](../../evaluation/incomplete-reference-quality.md) limits what can be inferred: agreement with another model, weak-label rules or synthetic behavior is not population accuracy. Predeclare practical gain, high-cost merge/review limits, latency and spend budgets. Reject added complexity after a sufficiently informative negative comparison; call sparse-transfer evidence inconclusive. Repeat stochastic/model-version-sensitive runs and preserve negative results rather than report only the best prompt.

## Research opportunities and evidence limitations

Does a nonlinear interaction solve a reproducible error slice beyond improved labels or representation? Does selective neural verification justify its cost after controlling for the gate? General statistical mechanisms are supported by the author's textbook; their ER adaptation and ranking/embedding/constraint menu are synthesis.[7] The LLM paper supports its specific benchmark configurations, not a universal complexity advantage.[36] No local model training, inference experiment or measured ER gain is claimed.

## Sources

[3] https://proceedings.mlr.press/v70/guo17a.html — On Calibration of Modern Neural Networks
[7] https://hastie.su.domains/ElemStatLearn/main.html — The Elements of Statistical Learning, second edition
[36] https://arxiv.org/abs/2310.11244 — Entity Matching using Large Language Models
