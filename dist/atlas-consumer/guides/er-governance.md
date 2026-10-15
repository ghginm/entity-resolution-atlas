# ER governance: permissible evidence, disclosure and correction

## Scope and evidence

This is a project-agnostic engineering intake and comparison guide, not legal
advice, a compliance certification or an implementation of private linkage.
Projects supply applicable obligations, permitted processing purposes, responsible
owners and qualified legal/security review. NIST Privacy Framework 1.0 describes
risk-based data management, minimization, deletion, processing permissions and
minimized audit records (CT.DM-P), alongside controls limiting observability and
linkability (CT.DP-P).[45] It does not certify an ER design. The version is
explicitly pinned to January 2020, not claimed to be the latest framework.

## Facts required before processing

Record entity/identity semantics, sensitive fields and derived artifacts, allowed
purposes, who may inspect each source, source-combination permissions, authorized
retention/deletion and export recipients. Access to two tables separately does
not establish permission to link them or disclose a combined entity. A processing
proposal identifies approved data placement and where raw fields, candidate
pairs, vectors, logs, model artifacts and human-review screens can travel.
Unknown authority is a stop condition, not permission inferred from Atlas content.

## Compare credible configurations

| Configuration | Mechanism | Cost and residual risk |
|---|---|---|
| Restricted local baseline | Keep necessary evidence within approved boundary; role-scoped review and publication | Local administrators/logs still expose data; fewer features may hurt matching |
| Minimized derived representations | Retain only purpose-necessary features, access-controlled references and bounded traces | Lossy features can destroy discrimination; derivation is not anonymization |
| Authorized external comparator | Send approved minimum payload to a specifically approved service | Retention, logging, training use, region, subprocessors and erasure need actual terms/controls |
| Specialist protected/federated linkage | Protocol chosen for a stated adversary and permitted output | Guarantees and leakage need verified specialist analysis; not supplied here |

Compare the local baseline with a proposed external route on the same approved
input/output semantics and independent evidence. A provider marketing claim or a
configuration flag cannot replace actual permission and retention verification.
Avoid categorical claims that external models are either always forbidden or
always safe; the project threat model and agreements decide.

## ER-specific threat and dependency map

- **Enumeration/linkability:** deterministic transforms of guessable identifiers
  can be tested against guesses; ordinary hashing is not an anonymity guarantee.
  Even if raw values are withheld, joined identities or stable pair keys can
  reveal relationships. Encryption in transit does not remove recipient access.
- **Derived exposure:** vectors, indexed names, rare frequencies, rule traces and
  snapshots are potential disclosure surfaces. Treat them as sensitive until a
  justified assessment establishes otherwise; do not assume embeddings are raw
  text-free and therefore safe.
- **Review exposure:** a reviewer needs the minimum relevant context and explicit
  authority to correct observations, membership or fields. Separate these actions;
  a convenient interface must not grant unapproved merge power.
- **Copy/retention propagation:** input withdrawal can affect candidate artifacts,
  evidence, training data, retained runs, backups and consumer views. Trace dependencies,
  track permitted erasure/retention decisions and residual limits. Do not claim
  deleting a source row erases all derived influence or a fitted model's influence.
- **Restoration risk:** rollback must not resurrect withdrawn evidence. Preserve
  only currently authorized history; immutability is subordinate to access and
  retention constraints, with replay limits explicitly recorded.

These are threat prompts and conditional engineering reasoning, not claims of
attack resistance. Bloom filters, keyed encodings, secure computation and
federated training have different leakage and adversary assumptions; no deep
cryptographic guarantee is synthesized from their names.

## Authorization and release artifact

Use the [project intake](project-intake.md) and
[run manifest](run-manifest-template.md). Name processing purpose, data/derived
artifact inventory, access and egress boundary, review/correction owners,
retention decisions, rollback limits, required independent tests and approval.
Preserve [decision provenance](decision-provenance.md) in a minimized authorized
trace: explanation does not require publishing every private feature.

A denied/unknown external call is an unavailable route, not an automatic non-match.
Choose a permitted fallback or abstention and evaluate its changed population.
Minimization can change candidate/evidence semantics; revalidate affected retrieval,
calibration and resolution rather than report privacy improvement alone.

## Evaluation, acceptance and deferred guarantees

Use [EVAL-11-006](../evaluation/synthetic-metamorphic.md) for access-denied routing,
redaction, deletion/restore and stale-authorization witnesses, without real private
fixtures. Independently test controls and trace coverage under the project threat
model; passing behavioral witnesses does not establish cryptographic security.
Use [EVAL-11-005](../evaluation/incomplete-reference-quality.md) and
[entity quality](../evaluation/entity-resolution-quality.md) for changed matching
outcomes. Adoption needs authorized processing plus acceptable harm, disclosure
and cost; a better F-score cannot override denied processing. Unknown permissions
block the action; insufficient quality/security evidence makes proposed guarantees
inconclusive. Detailed PPRL, model unlearning and federated guarantees remain
deferred pending primary specialist support and a concrete consumer need.

## Sources

[45] https://doi.org/10.6028/NIST.CSWP.01162020 — NIST Privacy Framework (Version 1.0, January 2020)
