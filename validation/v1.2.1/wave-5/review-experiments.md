# Bounded review: experiment design, stage interactions and reproducibility

## Scope and status

Integrating-author review of the pre-Wave-5 source snapshot, not an attested
independent certification, benchmark score or executed ER experiment. Freshly read:

- `decisions/experiment-design.md`
- `solutions/experimentation/controlled-comparison.md`
- `solutions/architecture/versioned-artifact-runs.md`
- `guides/run-manifest-template.md`
- `guides/experiment-plan-template.md`
- `evaluation/execution-cost-replay.md`

No frozen cases, answer keys or model results were used. No demonstrated scientific
error requiring a canonical-content change was found in this bounded slice.
This does not validate every claim elsewhere in the Atlas or substitute for real
project evaluation.

## Adversarial claim checks

[Executable counterexamples](check_experiment_boundaries.py) and
[actual output](experiment-boundaries.json) exercise six finite mathematical
witnesses. All quantities are illustrative constructed values, not observed data.

| Claim / source passage | Challenge | Disposition |
|---|---|---|
| `decisions/experiment-design.md:53–59`: interaction is scale-specific | Four probability cells have zero additive difference-of-differences; their logit contrast is about −0.133531 | Supported: the text explicitly limits the scale and does not equate this contrast to a coded regression coefficient or deployment causality |
| `controlled-comparison.md:38–49`, decision table at lines 39–45 | A has better candidate-conditioned recall (1 versus 4/5), but worse eligible-truth recall (1/5 versus 18/25) | Supported: conditional component value is separated from whole-system evaluation; the toy numbers illustrate denominator reversal, not a measured comparison |
| `execution-cost-replay.md:129–138`: edge marginals do not determine joint output | Two laws over three-vertex graphs share edge marginals 1/2; connected probabilities are 1/2 and 3/4 | Supported: the document already demands named joint objects/projections, not just marginal equivalence |
| `execution-cost-replay.md:45–60`: counts are not set-level completion | Two completed units and two required units can differ by an omitted required unit plus an unrelated extra | Supported: the frame, subset constraint, unresolved work and reconciliation are explicit |
| `versioned-artifact-runs.md:45,80`: cached stochastic output is one realization | Four independent fair-bit draws have mean variance 1/16; four copies of one cached draw retain variance 1/4 | Supported: the text rejects treating cache consumption as independent repetition and separates byte replay from distributions |
| `controlled-comparison.md:67,75–77`: nonsignificance is not equivalence | An interval from −0.3 to 0.3 includes zero but exceeds a declared ±0.05 equivalence region | Supported: practical margins, prespecified inference and inconclusive outcomes are already required; this witness asserts no coverage guarantee |

The inherited `validation/v1.2/check_reference_algebra.py` also ran unchanged:
[output](reference-algebra.json) reports exact finite recall-bound, HT variance and
hypergeometric-zero-event checks. This is documentation algebra, not new ground
truth or evidence of asymptotic coverage.

## Primary-source rechecks

Existing ledger identities were reused, not reset. [Retrieval receipts](experiment-source-rechecks.json)
record source URLs, UTC observation times, HTTP status, redirected URLs and body
hashes. Full HTML was retrieved; review was limited to the following sections, not
all documentation or the behavior of a locally installed tool.

- **NIST, ledger 20:** the two-level design matrix and interaction columns support
  full factorial combinations and main/interaction terms. The Atlas labels its
  ER contrast as a derived, scale-specific expression rather than a copied
  deployment-effect theorem. The first exact-term lookup did not match; direct
  inspection of the titled matrix/interaction sections supplied the check.[20]
- **DVC, ledger 24:** “Running Pipelines”, especially caching/skipping, supports
  reuse tied to unchanged declared commands, dependencies and parameters. It does
  not discover omitted semantic dependencies; the Atlas already says so.[24]
- **W3C PROV primer, ledger 25:** sections on entities/activities, usage/generation,
  responsibility and derivation/revision support artifact provenance. They do not
  define ER entity identity or prove correctness of the declared dependency graph.[25]
- **MLflow version 3.3.1, ledger 26:** the Model Alias concept describes mutable
  references to registered versions. The exact versioned primary URL succeeded
  through direct HTTPS after web-tool retrieval failed. The Atlas correctly does
  not infer atomic whole-pipeline publication or approval from an alias.[26]

No new source was needed. No broad current-version recommendation, privacy/legal
certification, runtime behavior claim or ER performance gain follows from these
source checks.

## Cross-stage and operational boundaries

The inspected text already separates fitting from serving and recalibration,
reference-only changes from prediction changes, frozen diagnostic controls from
valid deployment applicability, and evaluation from publication. It also requires
independent state/history comparators, permitted context at the decision time,
failed/unresolved work accounting, holdout protection and retention-qualified
rollback. These are conditional design requirements, not guarantees that any
implementation satisfies them. Real joint uncertainty, leakage audits, causal
identification, privacy authorization and distributed publication remain project
responsibilities. No corpus shortening or stylistic rewrite was justified.

## Sources

[20] https://www.itl.nist.gov/div898/handbook/pri/section3/pri3331.htm — NIST/SEMATECH e-Handbook: Two-level full factorial designs
[24] https://dvc.org/doc/user-guide/pipelines/running-pipelines — DVC: Running Pipelines
[25] https://www.w3.org/TR/prov-primer — PROV Model Primer
[26] https://mlflow.org/docs/3.3.1/ml/model-registry — MLflow Model Registry (3.3.1)
