# Reusable ER experiment-plan template

This is a supporting guide, not a primary card template or executable experiment. Copy the specification into an authorized project report and replace the prompts with known facts or explicit unresolved requirements. Do not fill gaps with invented data, thresholds, results, or permissions. Keep the five card templates unchanged.

Use [DEC-12-001](../decisions/experiment-design.md) to choose the design, [SOL-12-001](../solutions/experimentation/controlled-comparison.md) for the controlled protocol, and [compare-and-experiment](compare-and-experiment.md) for context. A complete plan does not authorize implementation or constitute an executed result.

## 1. Question, scope, and expected output artifact

- **Experiment identifier / owner / snapshot / authorization:** Name the responsible decision maker and allowed data, review, compute, and state changes; state forbidden actions.
- **Known / assumed / proposed / unresolved:** Distinguish project facts from assumptions; identify blocking missing information and how it will be obtained.
- **Decision and hypothesis:** Name linked cards, the directional claim, proposed mechanism, and at least one competing explanation.
- **Identity contract:** Same-as unit versus related-to, entity type, namespace, validity/observation time, eligible pairspace, source cardinality, and permissible unmatched/abstained/partial outputs.
- **Expected artifact:** Specify candidate pairs, evidence, scores with declared semantics, dispositions, assignment, partition, master attributes, or behavioral report. State what makes the artifact complete and what it does not prove.
- **Intended transfer:** New identities, existing-identity continuation, later observations, new sources/languages, or only the frozen reference population.

## 2. Baseline, challenger, and design

| Item | Required specification |
|---|---|
| Credible baseline | Current reproducible configuration and/or a simple admissible alternative; why it is credible |
| Challenger | Changed operation and information exploited; required prerequisites, costs, and expected failure slices |
| Design | Fixed pool, stage replacement, frozen/remodeled ablation, crossed factors, end-to-end, or a justified combination |
| Comparator fairness | Equal or explicitly different fitting/tuning opportunity, review budget, candidate budget, and compute accounting |
| Diagnostic versus adoption | Which contrast isolates a mechanism; which complete feasible configuration could be adopted |

For a factorial design, list every planned cell, factor levels, admissibility, response scale, and cell-specific calibration/refitting protocol. Name the interaction contrast and its target population. Do not interpret a score-scale-specific contrast as causality in deployment. For an oracle replacement, identify supported truth and why the result is only diagnostic.

## 3. Controls and semantic dependencies

- **Frozen common inputs:** Authorized source/reference snapshots; record eligibility; source roles; normalization/evidence policy; fixed candidates where isolating scoring; constraints; resolver; initial state; downstream consumers.
- **Allowed differences:** List exactly which artifacts/parameters change and why. A full-system comparison can differ broadly, but does not isolate one cause.
- **Dependency validity:** For each reused artifact, state compatible inputs and semantics. Consider normalization → keys/features, retrieval/routing → calibration, and accepted edges → membership → masters. Recompute invalid dependencies; do not call stale output a control.
- **Minimal run record:** Input/reference/component/configuration versions, split membership, candidate provenance, seed/run identity, and outcome status. Detailed tracking/cache/promotion machinery is outside this template's scope.
- **Resource accounting:** Fitting/tuning, index build/update, repeated comparisons, memory, latency distribution, review effort/delay, and relevant maintenance cost. Name units and measurement window.

## 4. Reference, inclusion design, and unknown labels

- **Annotation unit:** Pair, record/entity neighborhood, assignment, or another justified output unit; independent adjudication and disagreement handling.
- **Reference support:** What is complete, what is partially searched, and what cannot be observed? How are missed candidates or unreviewed entities sought independently of the challenger?
- **Inclusion/nonresponse:** Sampling frame, selection probabilities, strata, reviewed/unreviewed counts, search expansion, exclusions, response uncertainty, and any weights. State whether population inference is justified.
- **Unknown-label rule:** Unknown stays unknown. Name separately abstained decisions, ambiguous truth, missing reference, nonresponse, and independently established nonmatches. State identifiable estimands, denominator limitations, and any justified bounds/assumptions.
- **Independence from development:** Model predictions, weak-label rules, targeted review, and synthetic identities must not silently become independent gold.

Use [ground-truth acquisition](../decisions/ground-truth-acquisition.md) for design, [probability review](../solutions/ground-truth/probability-sampled-review.md) for representative sampling, and [incomplete-reference quality](../evaluation/incomplete-reference-quality.md) for inferential limits. Independent holdouts do not repair selective coverage or unknown nonresponse.

## 5. Split, tuning, and leakage audit

| Partition | Purpose / admissible use | Separation and access |
|---|---|---|
| Training | Fit permitted parameters and learned transformations | Entity/source/time rules and label/context access |
| Development | Discover properties, inspect errors, select thresholds/calibration, allocate tuning | Fixed budget and permitted repeated comparisons |
| Frozen final holdout | Evaluate predeclared contrasts once, or under a valid predeclared sequential design | Independent labels, no property discovery or adaptive tuning |
| Transfer replication | Confirm the intended later-time/source/population scope | Fresh supported evidence and explicit shift |

Audit shared identities/aliases, copied observations, graph neighborhoods, aggregate features, label rules, calibration, and future information. For incomplete identity truth, record uncertain overlap rather than claim guaranteed entity disjointness. If existing entities legitimately recur, name the historical state available at decision time. State what invalidates the holdout and what fresh evidence is then required.

## 6. Estimand, measurements, and uncertainty

- **Primary estimand:** Population, sampling/decision unit, weighting/averaging convention, target output, comparator difference and orientation. Distinguish candidate-conditioned from eligible-population recall and observed-reference from population quality.
- **Metric owner:** [Candidate coverage](../evaluation/candidate-recall.md), [pairwise discrimination/calibration](../evaluation/pairwise-calibration.md), [final entities/assignments](../evaluation/entity-resolution-quality.md), or [behavior violations](../evaluation/synthetic-metamorphic.md). Do not duplicate their foundational definitions here.
- **Denominators:** Eligible, sampled, reviewed, resolved, candidate, accepted, abstained, error, and unknown counts as applicable; an empty denominator is undefined.
- **Slices and guardrail metrics:** Source pairs, language/script, rare/high-harm entities, collisions, time gaps, cardinality, review workload, and cost; justify chosen slices instead of inventing project priorities.
- **Paired uncertainty:** First distinguish finite-population design, transfer/model, reviewer-error and algorithm uncertainty. Name interval/test conventions, precision/power assumptions, actual strata/weights/stages and valid variance/replicate units. Genuine random-pair design variance with fixed outcomes does not automatically require endpoint clustering; transfer inference may need entity/graph or multiway endpoint dependence. Do not replace real survey stages with arbitrary clusters.
- **Repeated runs and splits:** Separate acquisition/training/generator seeds, prespecified development-split repetitions where useful, frozen final contrasts and fresh transfer replications. Record split IDs, aggregation and matched randomization before outcomes. Overlapping entities/labels across repeated splits are dependent; changing final splits until a gain appears is test selection, not replication. Disclose all runs; more seeds do not create more independent truth.
- **Selection/multiplicity:** Planned contrasts, primary versus exploratory outcomes, stopping rules, and protection against favorable post-test selection.

For behavior tests, specify contract, generator support/distribution, prerequisites, fixture family, transformations, oracle, exceptions, and failure triage using the [testing guide](er-behavioral-testing.md). Selected regression counts are descriptive; generated-domain rates are not real-world error rates.

## 7. Practical decision and safety rules — complete before final evaluation

Specify numerical margins only from project consequences and available design precision; no Atlas defaults apply.

| Outcome | Predeclared evidence criterion | Next authorized decision |
|---|---|---|
| Adopt / bounded positive | Required practical benefit supported at the stated uncertainty level, harm/cost/behavior guardrails satisfied, and integrated output validated | Replicate intended transfer; propose only authorized reversible adoption |
| Reject / negative | Evidence rules out minimum useful value under the design, or establishes unacceptable harm/cost/contract violation | Retain baseline; diagnose mechanism, redundancy, estimation, or retrieval loss |
| Inconclusive | Interval spans materially useful benefit and unacceptable harm; unsupported labels; inadequate precision; or unresolved execution/oracle problem | Keep uncertainty explicit; collect relevant evidence or revise the next design without tuning on the final holdout |

Name minimum worthwhile effect, statistical versus practical significance, critical violation rules, cost/false-merge limits, review capacity, stop conditions, correction/reversibility requirements, and who may authorize continuation. Nonsignificance is not proof of equivalence; statistical significance alone is not an adoption rule.

## 8. Result artifact and bounded handoff

The completed report must include frozen-plan identity and deviations, actual configuration/input/reference versions, execution status, all planned runs and failed attempts, denominators/unknowns, paired estimates/intervals, guardrail/slice results, cost, and behavioral counterexamples. State **not run** where evidence is unavailable; never synthesize plausible outcomes.

Conclude with adopt/reject/inconclusive under the predeclared rule, limits of the inference, retained negative findings, and the next bounded question. Distinguish reproducibility, contract conformance, sampled quality, transfer, and deployment accuracy. Synthetic success alone cannot establish the last. This guide supplies a reusable specification, not evidence that any experiment has passed.
