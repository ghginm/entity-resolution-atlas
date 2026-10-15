# Refactoring rule policies without silently changing their meaning

This supporting guide connects [DEC-08-002](../decisions/rule-composition.md), [ordered policies](../solutions/decision-resolution/ordered-rule-policies.md), and [decision tables](../solutions/decision-resolution/declarative-decision-tables.md). It is Atlas synthesis: an operational sequence for a separately authorized project, not executable ER code or an instruction to modify production. The witnesses below are illustrative and **not executed**. They contain no measured accuracy results.

## Separate the change contracts

Name the intended change before editing:

- **Parameter change:** same conditions/composition, different approved thresholds or source settings.
- **Representation refactor:** same observable policy, moved from a conditional/CASE ladder to named predicates, ordered rules, or a table.
- **Policy change:** different priority, null handling, hit policy, constraint trust, override scope, or default. Do not disguise this as cleanup.
- **Resolver change:** different assignment/membership semantics; return to [DEC-08-001](../decisions/resolution-strategy.md).

The credible baseline is the smallest explicit ladder implementing the authorized policy. A table is an alternative only with an explicit hit policy. DMN 1.5 distinguishes First's rule order from Priority's ordered output values.[23] A pure predicate registry supplies named checks, not composition semantics. Fowler's essay cautions about action-driven chaining; it is a design perspective, not a measured rate of engine failures.[27]

## Operational sequence

### 1. Inventory the actual behavior and its authority

Read the current conditions, early returns, CASE branches, source exceptions, parameter defaults, and side effects. Record which behavior is intended, accidental, undocumented, or contested. Identify owners for identity semantics, trust declarations, thresholds, and review capacity. Do not turn current output into truth simply because it is reproducible.

Keep membership output and score estimation outside this refactor. Link the authorized [threshold/review contract](../solutions/decision-resolution/thresholds-abstention.md) rather than derive a new operating point here. Record the distinction between soft evidence, mandatory hard restrictions, and diagnostics.

### 2. Freeze the comparison boundary

Record input artifacts, evidence/predicate schemas, source roles, validity time, model/calibration applicability, thresholds, resolver, review routes, initial state, and budgets. Keep these fixed for equivalence refactors. [Versioned artifact runs](../solutions/architecture/versioned-artifact-runs.md) and the [run manifest](run-manifest-template.md) preserve the realized bundle; [controlled comparison](../solutions/experimentation/controlled-comparison.md) separates development from confirmation. Do not tune on final outcomes.

Specify observable equality: action, unresolved state, constraint result, selected parameter values, and authorized effects. Changed explanatory IDs may be mapped explicitly; timestamps and incidental trace ordering need not be identical. Persistent identity IDs require their own continuity contract.

### 3. Make hidden input and parameter semantics explicit

Use [evidence states](../solutions/comparison-features/evidence-states.md). Missing is an absent observation; explicit null needs a declared meaning; invalid is a failed validity check. Both-missing equality is not identifier agreement. Define incomparable and predicate-error handling, not only true/false behavior.

Declare numeric precision, inclusive/exclusive thresholds, ties, no-hit defaults, and unknown-source behavior. Resolve override specificity before rule matching, for example exact directional source pair and interval, then family, then global. Reject equal-specificity ambiguity. An override of score threshold cannot silently override a mandatory identity constraint.

### 4. Extract pure predicates and explicit effect boundaries

Give predicates stable names and versioned input contracts. They read a frozen snapshot and return documented outcomes without merging records, emitting review tasks, or fetching undeclared live context. Parameters remain named values, not duplicated literals.

Evaluate trusted premerge guards at the required decision unit. A cluster-union guard checks all relevant members and constraints, not just the proposed edge. Conflicting hard must-link/cannot-link obligations produce an infeasible/escalated result. Keep suspicious-but-untrusted findings diagnostic; postmerge detection does not prevent a prohibited merge. Any correction needs separately authorized reversible effects.

### 5. Choose the minimal representation and audit coverage

Keep a short ladder if it remains clearer. For ordered rules, publish sequence, terminal behavior, and equal-priority tie handling. For a table, declare hit policy and full output schema, including which reason fields are outputs versus annotations. Unique forbids overlap; Any permits it only with equal outputs; Collect is multiresult/aggregation, not a probability model.[23]

For compound outputs, Collect supports no aggregation operator; annotation-only columns do not create compound output. Priority compares ranked output clauses left-to-right in horizontal tables or top-to-bottom in vertical tables; unranked returned fields do not rank results.[23] Record output-clause precedence and the tie/result contract, not merely an action ranking. The [table card](../solutions/decision-resolution/declarative-decision-tables.md) owns these details.

Audit satisfiability, overlaps, gaps, and defaults. For a later ordered rule, distinguish **unreachable under declared input assumptions** from **no observed wins**. Retain a proof or counterexample search domain for the first; record observation scope and suppression counts for the second. Neither a zero trigger count nor an incomplete search proves dead code.

### 6. Build a compact differential regression set

Use reviewed witnesses for threshold boundaries, unknown states, conflicts, overrides, and cluster infeasibility. Preserve their preconditions when minimizing counterexamples. Compare baseline and challenger on the same input/state without executing effects twice. Record errors and unsupported oracles separately; passing an empty or ineligible test set is not coverage.

Test compatibility rejection when evidence, predicate, score, calibration, policy, or resolver versions disagree. Confirm deterministic decisions on identical immutable inputs. Test duplicate-delivery idempotency only when promised: deliver the event, commit its resulting state, then replay the same versioned event from that resulting state and inspect durable effects. Resetting to the initial state for both executions tests determinism, not duplicate-delivery idempotency. A genuinely new observation may legitimately change output. Reordering input records is not reordering First-policy rules.

### 7. Review differences and decide

Classify every difference as implementation regression, intentional policy revision, incorrect witness, or unresolved contract. Do not update expected outputs merely to match the challenger. Keep the original reviewed failure and add its boundary control.

**Adopt an equivalence refactor** when declared equivalence, critical guardrails, compatibility, and trace requirements are supported and the engineering benefit justifies maintenance/tooling cost. **Reject** proven guard bypass, silent semantic coercion, unauthorized effects, or an unreviewable rule expansion. **Inconclusive** means missing contract decisions or inadequate coverage, not presumed equivalence. Retain the baseline until those gaps close.

For intentional policy changes, predeclare practical quality/cost improvements and severe-error limits using [EVAL-11-003](../evaluation/entity-resolution-quality.md), supported independent references, and the controlled-comparison protocol. Passing witnesses or reducing conflict counts does not establish those improvements. Plan rollout, rollback, and correction only under project authorization; the Atlas supplies no production action permission.

## Small conditional witness fixtures — not executed

The following are written specifications, not a test runner. They do not define actual project costs, probabilities, thresholds, or identities.

### Common illustrative contract

Assume an authorized pair policy with supplied lower boundary `L` and upper boundary `U`, with `L < U`. Required input incompatibility/invalidity defers; conflicting trusted obligations escalate; a valid hard prohibition blocks the proposal; otherwise valid score `s >= U` proposes acceptance, `s < L` rejects now, and the remaining region defers. Rejection now is not a durable cannot-link. Proposal acceptance is still subject to the selected resolver's premerge feasibility check.

In this illustrative contract, an unknown/error mandatory guard defers/escalates before effects; optional diagnostic unknowns do not establish a veto. Define compound-predicate unknown/error propagation so an acceptance hit cannot bypass required unresolved admissibility. A different authorized risk treatment is a separately declared policy, not an equivalence refactor.

| Witness | Fixed construction / preconditions | Expected behavior under this contract |
|---|---|---|
| W1: cutoffs | Compatible inputs, no hard conflict; evaluate `s = L` and `s = U` | First defers; second proposes acceptance. Values just either side follow declared numeric precision, not an arbitrary machine epsilon |
| W2: unavailable state | Required score is missing, explicit null-as-unknown, or invalid; both identifiers absent | Defer with distinct reasons; no invented score zero or both-missing agreement |
| W3: soft / diagnostic / hard | Valid `s >= U`; vary soft identifier disagreement, diagnostic-only suspicion, then a valid scoped prohibition | Soft/diagnostic findings retain their trace without changing the frozen terminal policy; trusted prohibition blocks. This is conformance, not identity truth; granting a diagnostic veto is a separately authorized policy change |
| W4: override scope | Global `U`; exact `(A,B)` override `U_AB`; roles are directional, input otherwise fixed | Select `U_AB` for `(A,B)`; `(B,A)` uses only its authorized setting. Two simultaneous equal-specificity values cause explicit configuration conflict |
| W5: infeasible union | Proposal joins clusters containing records with a trusted cannot-link; a trusted must-link demands the same union | Escalate infeasibility; do not let pair score or first rule silently relax either obligation |
| W6: replay/version | Initial state → first event delivery → committed resulting state → same-event replay from that resulting state; separate reset-state baseline/challenger branches | No second durable merge/review effect when idempotency is promised. A new observation/version is a separate legitimate-change control; incompatible predicate schema stops explicitly |
| W7: unresolved guard | Valid `s >= U`; mandatory cluster guard returns unknown, then evaluation-error; control has only an optional diagnostic unknown and all required guards resolved | Mandatory variants defer/escalate with reasons before effects, even when the score row hits; optional-only control follows the unchanged terminal policy |

### Overlap and representation controls

**Shadow witness:** place an earlier terminal rule `s >= L -> defer` before `s >= U -> accept`. Under valid numeric scores and `L < U`, every input satisfying the latter also satisfies the former: the accept rule is structurally shadowed. In contrast, a source-specific rule with a satisfiable uncovered condition but no winners on the inspected observations is only observationally unused. Retain the eligible domain in both reports.

**First versus Priority witness:** construct one input hitting a hard-prohibition row returning `reject-now` and a permissive score row returning `accept-proposal`. Under First, row order selects the result; swapping those rows changes the result. Under Priority with authorized output order `reject-now` before `accept-proposal`, row swaps preserve that result.[23] The unsafe First swap is a deliberate counterexample, not recommended precedence. A trusted-guard layer outside the table may independently block effects; state which boundary is being checked.

**Unique/Any/default controls:** the same conflicting overlap violates Unique and Any. For Any, matching action labels with different output payloads are still unequal; differing annotation-only text does not affect equality.[23] A no-hit input follows the declared default. A malformed input is a separate compatibility/validity case and must not become a no-hit permissive fallback.

**Compound controls:** reject Collect-count on two actual outputs such as finding and severity; an annotation-only addition is a control that does not create another output.[23] For Priority, compare `(review, low)` versus `(accept, high)` with `review` ranked before `accept` and `high` before `low`: action-first selects the former, risk-first the latter, without moving rules. Row permutations must not change that ranking; an unranked reason field remains returned but does not affect it.[23] Record the admissible result for tied ranks with unequal payloads instead of inventing row priority. These are written controls, not runtime results.

## Report and evaluation boundary

Retain policy versions, change class, controls, witness preconditions, coverage gaps, reviewed differences, traces, compatibility checks, effect/idempotency contract, decision, and rollback limits. Apply [EVAL-11-006](../evaluation/synthetic-metamorphic.md) and the [behavioral-testing guide](er-behavioral-testing.md) for counts, dependent fixture families, unknown oracles, and uncertainty; their general evaluation mathematics is not repeated here.

Engineering evidence concerns semantics, maintainability, traceability, and authorized effects. ER evidence concerns identity output on a supported reference population. Equivalence to a mistaken baseline can pass the first boundary while failing the second. No witnesses or accuracy experiments were executed in this knowledge-only guide; [23] supports only its versioned hit-policy distinctions and [27] the attributed design caution.

## Sources

[23] https://www.omg.org/spec/DMN/1.5/PDF — Decision Model and Notation, version 1.5
[27] https://martinfowler.com/bliki/RulesEngine.html — RulesEngine
