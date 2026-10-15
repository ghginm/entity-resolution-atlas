# Content quality review: separate from structural lint

## Review procedure

Review one decision and its connected alternatives/evaluations as a unit. Record reviewer, snapshot, card IDs, source versions, finding and remedial action. Use **supported / needs revision / not applicable**, with a concrete passage or counterexample; never infer correctness from length, keywords, metadata maturity or lint success. A second reviewer should challenge mechanisms and sampling assumptions before upgrading evidence claims. This rubric reviews knowledge; the separate [agent benchmark](../validation/agent-utility/) reviews actual recommendation behavior.

| Criterion | Required review question | Rejection example |
|---|---|---|
| Mechanism | What operation uses what information, and why could it change the stated objective under these assumptions? | “Graph methods improve consistency” without explaining membership admissibility or information flow |
| Assumptions | Are identity type/time/cardinality, data availability, trust, candidate conditioning and score meaning explicit? | One-to-one imposed solely because there are two files |
| Failure modes | Is there a plausible causal counterexample and an observable diagnostic? | Only “can be inaccurate” rather than a bridge contaminating whole entities |
| Alternatives | Is there a credible simple baseline and a genuinely different approach to the same decision, with costs? | Comparing different parameter settings as if they were independent solution families |
| Falsifiability | Can proposed data/control/split/metrics distinguish the mechanism from a plausible competing explanation? | Simultaneously changing retrieval and scorer, then attributing improvement to weighting |
| Source scope | Does the verified source support this exact theoretical/empirical claim in its stated context? | Citing classification calibration as proof of ER transfer |
| Evidence discipline | Are mathematical consequences conditional, empirical results contextual, and untested proposals labeled? | Treating a raw additive score as probability or reporting invented gains |
| Composability | Can the reader separate hard prerequisites, compatible roles, interaction risks and conditional exclusions? | Declaring every probabilistic scorer incompatible with connected components |
| Economy | Does each paragraph add distinct decision information, using canonical links rather than repeated foundations? | Repeating a scorer derivation across three downstream cards |
| Discovery discipline | Do tags/summary identify supported applicability without spraying unrelated conditions? Is a reused concept assigned to its existing owner? | Every card tagged for every label/scale regime, or identical summaries hiding distinct choices |
| Operational evidence | Do completion, missing work, audit roles and consumer versions match the engineering claim? | Successful tiles treated as full evidence coverage; received deltas treated as coherently applied views |
| Responsibility boundaries | Does the object answer its type/domain question without silently acquiring another module's job? | Survivorship selecting a plausible value to justify entity membership |
| Evaluation estimand | Do labels, denominator, inclusion probabilities, unresolved cases and dependence match the output? | Candidate-selected labels used to claim full-population recall |

## Blocking findings

Any unsupported guarantee, unavailable required evidence concealed as known, wrong identity/cardinality semantics, unknown labels treated as negatives, or irreversible high-harm merge recommended without risk handling blocks a “Covered” judgment. Correct citations and section headings cannot compensate. A statistical interval is meaningful only under the label/sampling design; an empty denominator must be undefined. Constraint satisfaction is not identity accuracy.

Hypothesis review must identify at least one competing explanation, a control separating it, a predeclared practical effect threshold, guardrails and what negative/inconclusive evidence changes. A “falsification” heading alone is insufficient. Numerical project thresholds must come from real project consequences, not be invented by the Atlas.

## Coverage standard

**Covered** means sufficient decision-level mechanism, assumptions, at least one meaningful alternative, failure diagnostics, evaluation and usable cross-links exist for the explicitly bounded question. It does not mean every algorithm/variant in a domain is supported or an independent agent has succeeded. **Partial** means relevant content exists but lacks a major element. **Missing** means no usable substantive object. **Deferred** means an identified question is intentionally outside this iteration. The [matrix](decision-coverage-matrix.md) records baseline and final judgments separately.

## Verification boundary

Automated QA checks frontmatter, sections, type/ID consistency, navigation and immutable bytes. Human/agent review checks the meaning. Independent benchmark assessment checks retrieval and reasoning under fixed budgets. None measures production ER quality without an appropriate project experiment.

For final integration, revisit changed families and cross-module seams rather than rereading every unchanged card. Challenge expected-work denominators, whole-union constraints, candidate/calibration validity, missing labels, membership versus master continuity, authorization and unsafe restoration. Record which earlier reviews are inherited and which passages were freshly inspected. Contradictory or unsupported guidance remains a review finding even when all links resolve; a sampled conceptual pass is not full scientific certification.
