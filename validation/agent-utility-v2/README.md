# AU-v2 held-out agent-utility data package

Preparation status: **frozen data only; model runs and scoring NOT EXECUTED**.

This directory is separately versioned from AU-v1. It supplies eight fictional single-project inputs, one common solver prompt, budgets/settings, an execution/scoring protocol, evaluator-only semantic keys and ordinal rubric, JSON schemas, and a stdlib structural/freeze verifier. No new Atlas knowledge, existing AU-v1 file, real project data, ER output, trained model, corpus snapshot, score or result is included or modified.

## Boundaries
- Solver dispatch only: exactly one `inputs/AUv2-*.json`, `prompt.txt`, safe runtime settings/read contract and one neutral authorized corpus inventory.
- Evaluator only: `evaluator-only/` in full. Never solver or integrating corpus-author context. Keys are non-exhaustive, allow multiple defensible conclusions, and require credit for unanticipated sound alternatives.
- Operator only: protocol, settings, package metadata, schemas, verifier and freeze manifest. No package artifact belongs in a future knowledge corpus. Exclude evaluation artifacts everywhere, not just the key directory.
- Eight independent ordinal dimensions, 0–3, no aggregate. Conditional critical caps apply only to endorsed harmful claims, never rejection of an unsafe baseline.

No execution interface has been integrated. All model/provider identities and generation settings are null/unregistered. Independent tested/evaluator identities, actual settings evidence, immutable equivalent baseline/expanded/empty corpora, leakage review, brokered reads and fresh contexts remain prerequisites. The existing AU-v1 runtime must not be presumed compatible; protocol.md defines the honest future integration contract. Do not implement another runtime as part of this data package.

## Local structural checks only
From the repository root:

```sh
python3 -B validation/agent-utility-v2/verify.py --expected-manifest-sha256 EXTERNALLY_RECORDED_SHA256
```

The supplied final-delivery hash is the external anchor, not a model result. The verifier checks strict JSON, every instance/schema association, package cardinalities/references, declared input/key path separation, and the exact freeze inventory. The separate integrity suite exercises schema constraints and tamper/security rejection. Neither can prove semantic absence of answer hints or model isolation. No model request, ER algorithm, private-data processing, scientific validation or runtime sandbox test is performed. No fake run/score examples are written.

The manifest is created once by a stdlib authoring operation using exclusive binary creation (`open(..., 'xb')`), with `benchmark_id='AU-v2'` and canonical relative-path-to-lowercase-SHA256 mapping. The manifest itself is excluded and its external byte hash is mandatory for verification. `verify.py` is read-only and cannot freeze or re-freeze a cohort. Preserve this package and record any future preregistration/results outside its frozen tree. Changes require a new cohort; never tune this one to observed responses. No improvement claim is possible from preparation alone.

Integrity-only tests (run serially; temporary synthetic mutations are confined to this directory and cleaned):

```sh
python3 -B -m unittest discover -s validation/agent-utility-v2/tests -p test_integrity.py -v
```

TDD observed the missing tamper verifier fail, then pass; a schema-invalid but correctly rehashed input was initially accepted (failing test), then rejected after schema validation was added. These are package checks, never model/scoring results. The final test count and freeze-verification status are reported by actual command output, not simulated fixtures. Do not run verification of the original tree concurrently with tests creating temporary directories inside it.

## Inventory guide
`package.json` lists prepared artifacts and explicit absent runtime/identity state. `settings.json` freezes planned arms/order and budgets, not an installed provider configuration. `schemas/registration.schema.json` and `schemas/score.schema.json` are contracts for future integration only; no instances exist. `evaluator-only/coverage.json` is an authoring map and not a solver hint. The freeze includes all files in this directory except its own manifest; verification must reject added, removed, modified or symlinked entries.

Known exposure: public AU-v1 README/AGENTS protocol information was read; no old inputs, keys, score files or results were opened, and no new Atlas cards were inspected. Thus this is held out from solution testing and corpus-tailored wording, not proof of total independence from public historical headlines. Corpus authors must not inspect the new scenario/key contents or revise cards based on future answers.
