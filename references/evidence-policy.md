# Evidence and citation policy

## Claims have different evidential roles
- **Mathematical reasoning:** define quantities, state assumptions, and show the relevant argument. Set union preserves candidate coverage only without downstream caps; posterior odds need both evidence and a prior.
- **External support:** cite the actual checked source next to the claim, preserve its assumptions/population, and state whether the full text or only abstract was verified.
- **Empirical validation in a specific context:** identify the dataset, split/sampling design, comparator, metric and uncertainty. This repository contains no locally measured ER outcomes.
- **Untested hypothesis:** state proposed mechanism and a controlled falsifiable experiment, with practical effect/guardrails selected before inspecting final results.
- **Unresolved:** state what was not verified and what would resolve it. Absence of evidence is not proof of failure.

Maturity and evidence status are separate frontmatter fields; see [SCHEMA](../SCHEMA.md). Do not infer novelty from lack of a citation. Do not claim an algorithm is universally superior, a raw score is calibrated, or an oracle diagnostic is a population-wide upper bound.

## Bibliography and ledger
[Source ledger](source-ledger.json) maps retrieved URLs to stable numbers. [Research notes](research-notes.md) records checked claim scope and limitations; [retrieval status](retrieval-status.json) identifies admitted support and excludes failed or unverified exploratory sources from citation. The [bibliography](bibliography.md) lists verified references used by the Atlas. Use primary research or authors' technical materials for specific algorithm claims, and scholarly surveys for classification/context; a title or metadata record alone is not technical verification.

Source-bearing statements use `[n]` immediately after the supported sentence, with a Sources block mapping those stable ledger IDs to the cited works. Read the claim's scope and source limitations together; a bibliography entry does not support every nearby statement. Metadata and theory verification do not authorize invented benchmarks. Preserve source identifiers when quoting or combining Atlas evidence.

## Finite research budget
Seek additional evidence where it would materially change the decision: likelihood assumptions, selection/calibration, retrieval coverage and entity-centric evaluation. If access fails, try a verified author/publisher copy or explicitly mark abstract-only support, then continue. Do not keep cycling through mirrors. Bibliographic/provenance records and concise analytical summaries are not substitutes for unread technical claims; full copyrighted papers are not included in the Atlas.

## Changes over time
Record retrieved version when known. Later source revisions may change authors/claims; check them rather than treating a metadata search snippet as full-text verification. Updating evidence does not change card IDs. Project-specific positive/negative outcomes belong in contextual reports, never silently upgrade universal Atlas claims.
