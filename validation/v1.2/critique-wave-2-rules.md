# Wave 2 rule composition: adversarial scientific/conceptual critique

## Review boundary and disposition

**Reviewer:** delegated adversarial critique role, distinct from the drafting assignment. Independent human review or independent model identity is not attested. **Snapshot:** the actual files read in this task; fingerprints below identify that snapshot rather than a commit. **Contract:** `SCHEMA.md` and `guides/content-review-rubric.md`.

**Disposition: needs revision / Partial for the bounded composition-and-test-route question.** Six findings: **0 blocking, 3 major, 3 minor**. The basic ownership split, First/row-order versus Priority/output-order distinction, and separation of behavioral agreement from identity truth are supported. The major gaps are compound-output restrictions and ordering, plus explicit handling of an unresolved mandatory guard. These are documentation/contract gaps, not observed runtime defects. Parent review must disposition them before a final coverage judgment.

Reviewed family: `DEC-08-002`, `SOL-08-005`, `SOL-08-006`, `guides/rule-policy-refactoring.md`, and `EVAL-11-006`. Necessary owners inspected: `DEC-08-001`, `SOL-08-001`, `SOL-06-001`, `SOL-08-004`, `SOL-02-001`, `SOL-12-001`, `EVAL-11-003`, and `guides/er-behavioral-testing.md`. No benchmark cases, keys, results, ER implementation, datasets, training, or commits were accessed or produced. Only this report was written.

| Snapshot path | SHA-256 |
|---|---|
| `decisions/rule-composition.md` | `97b94f8e9c44697a46bea88ecf52eea66b0b3d2fe83e07c329d6b77846cccadd` |
| `solutions/decision-resolution/ordered-rule-policies.md` | `e4073d3e2d6da987eb41243fd2104555095dd32c63312fa3658a1b9291361d9e` |
| `solutions/decision-resolution/declarative-decision-tables.md` | `ddaa813900395c70a2dcfec0ac9167471d28efc52fc6b9d7796c544f100405d5` |
| `guides/rule-policy-refactoring.md` | `1e35806725581704e1e554be6a096e5c1d9a88e6df3f2d800fb76f676791010d` |
| `evaluation/synthetic-metamorphic.md` | `b54555d0f240df744767dc00d3650f46e079ea31ae1a1a333c73c5ce4d5847f9` |

## Primary-source verification

Read the **entire selected textual sections** of the supplied DMN 1.5 primary extraction, `/home/ghgin/.hermes/cache/scratch/atlas-wave-2-sources/primary-2.txt`, lines 3000–3091: section 8.2.11, subsection 8.2.11.1, both notes, and section 8.2.12; printed pages 71–73. This includes annotations, all seven hit policies, compound-output restrictions, and compound-output ordering—not merely the single-output summary. Figures were not independently visually inspected. The deliberately selected version is 1.5, not a latest-version recommendation.[23]

The text supports: Unique disjointness; Any equality for every output while ignoring annotations; First by rule sequence; Priority by declared output-value ordering independently of row sequence; Collect without an operator as arbitrary-order multiresult; no Collect aggregation for compound outputs; and left-to-right/top-to-bottom precedence among ranked compound-output clauses. Outputs without a declared ordering remain in the payload but do not rank it. Annotations do not form expression results, and runtime annotation access is not standardized. Section 8.2.12 permits default output values; it is not itself an ER unknown/error policy.[23]

Read Fowler's actual essay body in `primary-6.txt`, especially lines 299–327 and 330–365. Its chaining caution and explicit non-statistical anecdote qualification support the limited attribution in the cards, not an empirical failure-rate or accuracy claim.[27] The configured extraction tool could not extract either URL because its backend was search-only. A direct, read-only HTTP fallback returned both sources successfully and confirmed the essay's chaining/disclaimer passages; the supplied primary extraction remained the basis for the full selected-section review. No citation ledger was changed.

## Findings requiring disposition

### R1 — Major: compound outputs cannot use Collect aggregation

- **Location:** `solutions/decision-resolution/declarative-decision-tables.md`, **Core mechanism**, lines 36 and 46–48; **Important variants**, line 63; `guides/rule-policy-refactoring.md`, **5. Choose the minimal representation and audit coverage**, line 44.
- **Passage/problem:** The card first proposes action plus compatible decision payload, then describes Collect as all hits or a supported aggregate. “Supported” does not tell the reader that adding another actual output clause makes every Collect operator unavailable under the selected standard. The guide likewise mentions full outputs and aggregation without the restriction.
- **Concrete counterexample:** A diagnostic table has two actual outputs, `finding_code` and `severity`. Its author selects Collect with count, assuming count is harmless because the consumer only needs a total. A DMN 1.5 compound-output table cannot use that operator—even though counting hits sounds meaningful. Annotation columns are a different case and do not impose this restriction.[23]
- **Proposed fix:** State explicitly that compound outputs allow Collect **without** an operator only; aggregation operators are restricted to an appropriately typed single-output table. Preserve a separate diagnostic list and perform any authorized postprocessing outside the table. Add a written compatibility witness rejecting compound Collect aggregation and a control showing annotation-only additions do not create another output clause. Neither witness should be described as executed.
- **Rubric judgment:** **Needs revision:** mechanism, source-scope completeness, composability. This is an omitted restriction, not evidence that an invalid runtime configuration has actually been deployed.

### R2 — Major: compound Priority needs output-clause precedence, not only action ranking

- **Location:** `solutions/decision-resolution/declarative-decision-tables.md`, **Core mechanism**, lines 36, 45, 48; **Theoretical explanation**, line 54; **Important variants**, line 62; `guides/rule-policy-refactoring.md`, **First versus Priority witness**, line 83.
- **Passage/problem:** The First/Priority distinction is correct, but the examples rank only actions while the proposed schema permits multiple returned outputs. Compound Priority is not fully specified by saying the authorized action ordering exists.
- **Concrete counterexample:** Two rows match. Returned outputs are `action` followed by `risk_class`; action values rank `review` before `accept`, and risk values rank `high` before `low`. One row returns `(review, low)`, the other `(accept, high)`. With action first, the first payload wins; moving the ranked risk column before action reverses that choice, without moving any rule. If risk has no output-value ordering, it participates in the payload but not the priority comparison.[23]
- **Proposed fix:** State the selected standard's ordered comparison over ranked output clauses, including column/orientation precedence and exclusion of unranked clauses/annotations. Declare which outputs are ranked and the admissible tie/result-equality contract rather than inventing row weights. Add written controls for row permutation, output-clause permutation, and an unranked reason field.
- **Rubric judgment:** **Needs revision:** mechanism, assumptions, source scope, falsifiability. The existing single-output witness remains supported; it does not cover the advertised compound schema.

### R3 — Major: distinguish unknown optional evidence from unresolved mandatory admissibility

- **Location:** `solutions/decision-resolution/ordered-rule-policies.md`, **Core mechanism**, lines 38–40; `solutions/decision-resolution/declarative-decision-tables.md`, **Core mechanism**, line 50 and **Assumptions and prerequisites**, line 70; `guides/rule-policy-refactoring.md`, **Common illustrative contract / W2**, lines 68–74.
- **Passage/problem:** Unknown may make a rule inapplicable, and invalid required evidence defers, but the family does not explicitly bind an unresolved **mandatory guard** to the pre-effect decision. Preventing permissive no-hit defaults is insufficient when a separate acceptance row actually hits. This is an incompletely constrained project contract, not a demand that every optional unknown cause abstention.
- **Concrete counterexample:** The required cluster-union prohibition check returns unknown because its authoritative constraint snapshot is unavailable. The prohibition row is marked inapplicable on unknown; the valid-score acceptance row matches. Neither missing-score deferral nor no-hit default validation detects the bypass. Unknown prohibition is not proof of either prohibition or admissibility.
- **Proposed fix:** Require an explicit outcome for mandatory guard `unknown` and `evaluation-error`: preserve the reason and defer/escalate before effects unless a separately authorized risk contract specifies another treatment. Keep optional soft/diagnostic unknown handling separate. Add written high-score witnesses for unknown and error on a mandatory guard, plus a control where an optional diagnostic is unknown. State predicate conjunction/error propagation where a compound condition could hide the required outcome.
- **Rubric judgment:** **Needs revision:** assumptions, failure modes, composability. Existing missing/null/invalid distinctions and hard/soft trust safeguards are supported; this asks for their last effect-boundary connection, not a universal fail-closed rule for all observations.

### R4 — Minor: engineering adoption lacks a direct measurement bridge in this family

- **Location:** `decisions/rule-composition.md`, **Related evaluations**, lines 86–88; `ordered-rule-policies.md`, **How to evaluate**, lines 84–86; `declarative-decision-tables.md`, **How to evaluate**, lines 96–98; `evaluation/synthetic-metamorphic.md`, **What is measured / Definitions and formulas / Engineering substitution and replay contracts**, lines 27, 37–47, 77–79.
- **Passage/problem:** Behavioral rates and paired agreement fit the conformance claim. They do not measure the separate adoption requirement that an engineering benefit exceeds maintenance/tooling cost. That requirement is correct but underspecified locally.
- **Concrete counterexample:** Ladder and table agree on every eligible fixture, with no errors. Table authoring, diagnosis, and review take longer; both still have identical behavioral violation fractions. A passing EVAL-11-006 report alone cannot establish the stated engineering benefit.
- **Proposed fix:** Link directly to `solutions/architecture/replaceable-stage-pipelines.md`, **How to evaluate**, especially line 85: matched extension/diagnosis tasks, equal budgets, task/review time, escaped defects, overhead, and disclosed learning effects. Name the engineering estimand and predeclared practical margin in the project comparison; do not create a duplicate evaluation card or invent measured savings. Its existing protocol makes this a minor linkage gap rather than a missing evaluation family.
- **Rubric judgment:** **Needs revision:** evaluation-estimand linkage and falsifiability for the engineering-benefit claim. **Supported:** EVAL-11-006 for bounded conformance, EVAL-11-003 for independently referenced identity quality, and inconclusive handling of incomplete coverage.

### R5 — Minor: W6 should specify sequential replay from the resulting state

- **Location:** `guides/rule-policy-refactoring.md`, **6. Build a compact differential regression set**, line 52; **W6: replay/version**, line 77.
- **Passage/problem:** W6's “Same event ID/version and initial compatible state, then replay” leaves the state progression less explicit than the duplicate-effect assertion needs.
- **Concrete counterexample:** A harness restores the initial empty review queue before each run, observes one task each time, and reports replay success. Actual duplicate delivery after the first committed effect creates another task. Reset-state deterministic evaluation did not test promised delivery idempotency.
- **Proposed fix:** Write W6 as an initial state followed by first delivery, committed resulting state, and replay from that resulting state; inspect durable effects and review-task counts. Keep separate reset-state baseline/challenger branches. Add a changed-version/new-observation control whose legitimate new effects are not labeled replay violations.
- **Rubric judgment:** **Needs revision:** witness precision. **Supported:** idempotency is explicitly conditional throughout the family and is not confused with universal order invariance.

### R6 — Minor: diagnostic-only trust deserves an explicit boundary control

- **Location:** `decisions/rule-composition.md`, **Relevant assumptions**, line 41; `guides/rule-policy-refactoring.md`, **4. Extract pure predicates and explicit effect boundaries**, line 40; **W3**, line 74.
- **Passage/problem:** Diagnostic suspicion is correctly denied veto authority in prose; W3 tests soft disagreement versus trusted prohibition but not the diagnostic-only third role.
- **Concrete counterexample:** A postmerge anomaly detector is imported as a generic `guard=false` predicate. It vetoes a high-score proposal despite lacking the authority and observation guarantees of a mandatory restriction. The current soft/hard fixture can miss this boundary error if diagnostic inputs are never constructed.
- **Proposed fix:** Add a written W3 variant with a diagnostic-only suspicion, preserving its trace while leaving the frozen terminal decision unchanged; add an explicitly authorized trust-change variant as a policy revision, not a representation refactor. Keep prevention and postmerge detection separate.
- **Rubric judgment:** **Needs revision:** test-route completeness only. The conceptual trust distinction itself is **supported**.

## Supported judgments and ownership challenge

| Rubric criterion | Judgment | Passage and adversarial check |
|---|---|---|
| Mechanism | **Needs revision** | R1–R2 complete the selected standard's compound cases; basic First/Priority and Unique/Any distinctions are correct. |
| Assumptions | **Needs revision** | R3 specifies required-guard unresolved/error behavior; source roles, time, score meaning, and evidence states are otherwise explicit. |
| Failure modes | **Supported** | Ordered **Trade-offs and failure modes**, lines 72–76, distinguishes structural unreachability, no wins, suppression, early catch-all, and union infeasibility. A satisfiable source exception absent from observations is not proven dead. |
| Alternatives | **Supported** | DEC **Trade-off comparison** and SOL-08-006 **Relationships** distinguish intentional sequence from non-First overlap contracts, retaining the small ladder. |
| Falsifiability | **Needs revision** | Frozen paired witnesses separate representation from thresholds and hit-policy changes; R1–R3 and R5–R6 fill specific controls, R4 connects engineering outcomes. |
| Source scope | **Needs revision** | DMN attribution is bounded and Fowler is not presented as measurement; R1–R2 require the omitted compound qualifications. |
| Evidence discipline | **Supported** | Guide **Report and evaluation boundary** and both solutions' limitations explicitly deny executed tests and ER gains. Passing a mistaken baseline is not truth. |
| Composability | **Needs revision** | Existing proposal/effect and whole-union boundaries are correct; R3 prevents required unknown guard outcomes disappearing between them. |
| Economy | **Supported** | Threshold justification and membership optimization stay with their owners; add only the narrow R1–R6 fixes, using canonical links. |
| Responsibility boundaries | **Supported** | DEC lines 29, 35, 78 and threshold-owner line 65 separate composition, score semantics, authorized actions, membership feasibility, and diagnostics. |
| Evaluation estimand | **Supported, with R4 linkage revision** | EVAL-11-006 lines 45–47 excludes invalid execution/oracles only transparently, reports their coverage, makes empty denominators undefined, and restricts inference to fixed generator support. Lines 57, 83 reject adaptive-search probability claims and independent counting of related variants. |

**No shallow duplicate finding.** `SOL-08-001` justifies operating points, costs, and review; `DEC-08-001` selects authorized output structures; the new decision composes supplied conditions and precedence. `SOL-08-005` and the First-table variant can deliberately implement the same function, but non-First tables supply materially different overlap contracts. For an input hitting conflicting outputs, Unique reports a contract violation, Any requires equality of the entire returned output rather than just the action, and Priority selects by authorized output ordering. That is a meaningful choice, not a new threshold parameter. Do not market a First-table rewrite alone as another scientific ER method.

**Full payload versus annotations is already handled correctly for Any.** SOL-08-006 **Theoretical explanation** and guide **Unique/Any/default controls** reject equal action labels with unequal returned payloads, while allowing annotation-only differences. Keep action, reasons that are actual outputs, unresolved state, and applicable constraints distinct from annotations; the audit contract cannot assume annotations will be exposed at runtime.[23]

**Source override ambiguity is explicitly handled.** DEC **Criteria for choosing**, ordered **Assumptions and prerequisites**, and W4 define specificity as a proposed scoped contract, reject equal-specificity collisions, preserve directional roles, and disallow parameter overrides silently weakening hard restrictions. An `(A,B)` override cannot be obtained by casually reversing `(B,A)`.

**Cluster-union constraints are not reduced to edge checks.** Both solutions and W5 require full-union feasibility and escalation of contradictory trusted obligations. A plausible trigger edge can join groups with a cannot-link between other members; pair score is no authority to relax that prohibition. Postmerge diagnostics neither prevented that effect nor establish identity error without supported references.

## Residual scope and nonexecution statement

This review establishes passage-level support and conceptual counterexamples only. **No empirical test, behavioral fixture suite, ER accuracy experiment, maintainability trial, or model evaluation was executed.** The illustrative counterexamples are not observed failures or measured results. Documentation verification of this report is not scientific validation of a runtime.

Residual project requirements: the actual predicate/runtime semantics, mandatory-guard ownership and unavailable-state contract, compound output schema/order, compatible hit-policy subset, source/time parameter authority, idempotent effect storage, accepted observable equality, independent identity reference support, and practical engineering/quality margins. A specific runtime could have additional restrictions; nothing here certifies one. No global correctness guarantee follows from a finite witness suite, zero violations, constraint satisfaction, or agreement with a baseline. Parent review and disposition—not this report alone—determine whether the bounded coverage can advance.

## Sources

[23] https://www.omg.org/spec/DMN/1.5/PDF — Decision Model and Notation, version 1.5
[27] https://martinfowler.com/bliki/RulesEngine.html — RulesEngine
