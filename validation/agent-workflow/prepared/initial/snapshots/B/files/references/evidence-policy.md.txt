# Evidence and citation policy

## Claims have different evidential roles
- **Mathematical reasoning:** define quantities, state assumptions, and show the relevant argument. Set union preserves candidate coverage only without downstream caps; posterior odds need both evidence and a prior.
- **External support:** cite the actual checked source next to the claim, preserve its assumptions/population, and state whether the full text or only abstract was verified.
- **Empirical validation in a specific context:** identify the dataset, split/sampling design, comparator, metric and uncertainty. This repository contains no locally measured ER outcomes.
- **Untested hypothesis:** state proposed mechanism and a controlled falsifiable experiment, with practical effect/guardrails selected before inspecting final results.
- **Unresolved:** state what was not verified and what would resolve it. Absence of evidence is not proof of failure.

Maturity and evidence status are separate frontmatter fields; see [SCHEMA](../SCHEMA.md). Do not infer novelty from lack of a citation. Do not claim an algorithm is universally superior, a raw score is calibrated, or an oracle diagnostic is a population-wide upper bound.

## Bibliography and ledger
[Source ledger](source-ledger.json) maps retrieved URLs to stable numbers. [Research notes](research-notes.md) records checked claim scope and limitations; [retrieval status](retrieval-status.json) excludes failed exploratory URLs. The [bibliography](bibliography.md) renders only verified references used in the pilot. Do not copy placeholder DOIs from manuscript templates. Use primary research, authors' technical materials, or a scholarly survey for classification/context; establish specific algorithms from their primary work before deep expansion.

Document source-bearing statements with `[n]` immediately after the supported sentence. Each document's Sources block is mechanically rendered from the ledger. Metadata and theory verification do not authorize invented benchmarks. Retain source identifiers when merging contributions; do not reset the ledger mid-iteration.

## Finite research budget
Research where accuracy materially improves: likelihood assumptions, selection/calibration, retrieval coverage and entity-centric evaluation. If access fails, try a verified author/publisher copy or explicitly mark abstract-only support, then continue. Do not keep cycling through mirrors. Do not vendor entire copyrighted papers into the repository; bibliographic/provenance records and concise analytical summaries suffice.

## Changes over time
Record retrieved version when known. Later source revisions may change authors/claims; check them rather than treating a metadata search snippet as full-text verification. Updating evidence does not change card IDs. Project-specific positive/negative outcomes belong in contextual reports, never silently upgrade universal Atlas claims.
