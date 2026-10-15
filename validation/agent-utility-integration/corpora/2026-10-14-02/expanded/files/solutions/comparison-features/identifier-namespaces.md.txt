---
id: SOL-06-003
type: solution
title: Namespace-qualified identifier evidence
domain: "06"
summary: >-
  Compare identifiers only after establishing namespace, entity meaning,
  normalization, issuing scope and relevant validity or reuse semantics.
  Distinguish syntactic validity, authoritative assignment and uniqueness;
  equality alone can reflect a shared placeholder or an unrelated local number.
  Requires project-specific authority and identity assumptions. A trustworthy
  identifier can support a simple exact baseline, but disagreement is a hard
  contradiction only under justified uniqueness and temporal conditions;
  otherwise retain soft evidence or escalate unresolved admissibility.
tags: [identifiers, evidence-engineering, source-aware, provenance, uncertainty, constraints, high-precision]
maturity: context-dependent
evidence: theoretically-motivated
relations:
  addresses: [DEC-06-001]
  complements: [SOL-06-001, DEC-01-001, SOL-08-005]
  evaluated_by: [EVAL-11-002, EVAL-11-006]
---

# Namespace-qualified identifier evidence

## Summary and problem addressed

`0042` in one source is not necessarily the same identifier as `0042` in another. Conversely, two different identifier strings need not imply different entities. This solution establishes what an identifier observation means before exporting agreement or contradiction. It extends [evidence states](evidence-states.md), not the issuing authority's standard, a universal identifier registry or a new identity definition.

Fellegi–Sunter comparison-vector theory allows observations to contribute according to match/nonmatch distributions.[1] It does not establish any particular identifier's authority or universal uniqueness. The contract and examples below are **Atlas synthesis**; detailed primary specifications for particular identifier systems were not reviewed in this wave.

## Core mechanism, assumptions and theoretical explanation

Attach an identifier observation to its namespace, issuing scope, identifier kind, entity level, raw value, source, normalization/version and time evidence. Separate observation time, claimed validity interval and retrieval time if available. Unknown metadata remains unknown. A namespace may need issuer or jurisdiction qualifiers; a source column name alone does not establish it.

Then evaluate separate questions:

1. **Parsing and format:** is the value well formed under a known version? Preserve leading zeros, case and punctuation unless that namespace explicitly permits a transform.
2. **Validation:** does it pass available syntax/checksum checks? A successful check establishes only that check, not authoritative assignment, uniqueness, current validity or identity.
3. **Assignment semantics:** what does it identify—record, account, branch, legal entity, license, household or enduring person? Can an entity hold several at once?
4. **Reuse and time:** can the value be reissued, expire or change for one continuing entity? Are observations comparable in a relevant time scope?
5. **Authority and independence:** is the assignment verified, merely source-asserted or copied from another record? Several copies of one mistaken identifier remain one originating claim.

Only after these checks produce namespace-qualified evidence. If comparison prerequisites fail, return an incomparable, invalid or unresolved state with reasons—not a numeric disagreement by default.

The reasoning is semantic rather than a performance theorem: exact lexical equality inside a namespace is informative only to the extent that assignment rules and observation quality associate it with identity. Lexical inequality becomes an impossibility claim only when the domain's exclusivity rules actually imply it. Neither property follows from the string length or the word “unique” in a database schema.

## Worked examples and important variants

**Synthetic examples:** source A's customer `0042` and source B's supplier `0042` are unrelated local namespaces unless a verified mapping says otherwise. Do not strip leading zeros to join a textual identifier to numeric `42` without its declared encoding contract. A tested explicit crosswalk can establish compatible identities across namespaces; retain its direction, provenance, version and uncertainty rather than silently convert equality of unrelated values into truth.

A license renewal can issue a new license identifier to the same legal entity. Two unequal license values are not automatically a cannot-link. A building address or household account can be shared by different people. Recycled account numbers can agree lexically across disjoint assignment intervals while denoting different holders. A copied placeholder may pass a broad regular expression and occur in many records without meaningful identity support.

Variants include exact namespace equality, a verified crosswalk, set-valued historical comparison and partial identifiers. Truncated or masked equality requires explicit uncertainty; reconstructing the missing part is not justified. Multi-valued comparisons must distinguish one corroborating overlap from several conflicting assignments and retain which observations generated each outcome.

## Applicability, advantages, baseline and policy alternatives

Use a **simple exact baseline** when namespace compatibility, assignment semantics and sufficient observation reliability are established. Complex scoring is optional. Audit collisions, placeholders and known reassignment before treating equality as decisive; exact blocking still loses records with missing or erroneous identifiers.

For disagreements choose among:

- **Hard constraint:** only if the externally authorized identity definition, compatible namespace, validity time, exclusivity and reliable observations jointly justify impossibility. This is a claim about membership feasibility, not merely a negative score.
- **Soft evidence:** when different values are statistically informative but multiple assignments, errors or continuity changes remain possible. Its weight belongs to a population-specific [scorer](../../decisions/scoring-strategy.md).
- **Abstention or review:** when required compatibility/authority is unresolved and an action would otherwise cross a high-harm boundary. Optional missing context is distinct from a failed mandatory guard. [Ordered policies](../decision-resolution/ordered-rule-policies.md) owns that execution distinction.

A hard pre-merge constraint must be checked on proposed union membership, not just one endpoint pair; existing component contents may conflict. Post-merge diagnostics can flag problems but do not retroactively make an unsafe irreversible merge acceptable. Keep corrections reversible under the project's authorization and retention rules.

## Trade-offs, failure modes and relationships

Namespace/validity checks add reference-data maintenance, lookup latency, unavailable-authority cases and version dependencies. Local syntactic checks are cheaper than remote authority validation but support weaker conclusions. Prefer explicit unavailable results and bounded review over silently accepting a stale cached assignment.

Principal failures are over-trusting format, conflating stable identity with identifier continuity, mixing branch and parent identifiers, ignoring reuse time, and double-counting copied values. An identifier-derived training label later “validated” by the same identifier rule measures rule imitation, not independently established identity. Candidate admission by identifier agreement also changes the scored population; do not reuse unconditional agreement weights without checking applicability.

## How to evaluate and act on evidence

First use [behavioral tests](../../evaluation/synthetic-metamorphic.md) for different namespaces with the same lexical value, invalid placeholders, preserved zeros, renewal, reissued values, unresolved guards and conflicting component unions. Specify expected outcomes from independent namespace/identity requirements, not from the implementation under test. These checks validate a stated policy, not population precision.

Then compare namespace-aware exact rules with naïve lexical equality on fixed candidates using [pairwise evaluation](../../evaluation/pairwise-calibration.md), independently adjudicated identity evidence and slices for issuer, entity level, reuse, missingness and conflict. If identifiers helped construct reference truth, disclose that circularity and obtain another adjudication route. Independent outside-candidate evidence is necessary to assess retrieval loss; a within-block sample cannot reveal missing-identifier matches elsewhere.

Predeclare adoption criteria around prevented high-cost false merges, recovered continuing identities, review burden and latency. Reject a hard veto if independently supported same-entity cases violate its assumptions. Incomplete or disputed authority makes the result inconclusive, not proof that a softer rule is accurate. Revisit affected membership and master attributes separately after changing the rule.

## Research opportunities and evidence limits

Which namespaces actually meet the project's trusted-assignment assumptions, and how often are exceptions concentrated in particular sources or time periods? Those require external facts and independent review. No identifier-specific guarantee, regulatory claim or measured ER gain is supplied here. Comparison theory supports separating observations from their evidence weight; the namespace/policy contract remains theoretical synthesis.[1]

## Sources

[1] https://nhis.ipums.org/nhis/resources/Fellegi69.pdf — A Theory for Record Linkage
