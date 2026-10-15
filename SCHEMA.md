# Knowledge conventions

## Scope and precedence
This is a decision-support Atlas, not an ER implementation. [SCOPE.md](SCOPE.md), [AGENTS.md](AGENTS.md), this schema and the [evidence policy](references/evidence-policy.md) define the knowledge contract; no missing external master instruction is normative. External evidence and explicitly labeled reasoning refine content. Guides, taxonomy pages, indexes, source notes and deep dives are supporting documents, not extra knowledge-object types.

## Identity and classification
- IDs are permanent: `DEC-DD-NNN`, `SOL-DD-NNN`, `HYP-DD-NNN`, `EVAL-DD-NNN`, where DD is the two-digit primary domain. Architecture IDs are **AR-01 through AR-06**, preserving the requested archetype names; do not create parallel ARC aliases.
- Five types: `decision`, `solution`, `architecture`, `hypothesis`, `evaluation`. Domain is a quoted two-digit string, `"01"` through `"14"`. Architectures primarily belong to `"02"`; evaluations to `"11"`.
- One canonical location per object. Do not reuse an ID after deletion. Rename paths only with all links updated; the ID remains unchanged.
- Card frontmatter requires `id`, `type`, `title`, `domain`, `summary`, `tags`, `maturity`, `evidence`, and `relations`. Summary is an L1 discovery description of approximately 50–100 words, not an experimental outcome. L0 derives one concise applicability statement; generated per-domain L1 indexes retain the full summary and relation navigation. Neither index is another object type. Length recommendations are informational, not proof of depth.
- Maturity: `established`, `context-dependent`, `experimental`, `speculative`.
- Evidence (independent of maturity): `theoretically-motivated`, `supported-by-external-literature`, `empirically-validated-in-specific-context`, `unknown-or-insufficient`. No ER performance experiment has been run by the Atlas. Source-specific validation is described with its population, design and limitations, never treated as a universal win; documentation checks and agent-utility evaluation are separate evidence.

## Typed relation directions
Frontmatter `relations` is a mapping of relation names to lists of existing card IDs:
- `addresses`: solution → design decision.
- `alternative_to`: materially substitutable objects, not merely related topics.
- `complements`: useful joint use, explain the interaction in prose.
- `requires`: a necessary prerequisite object, not a preferred baseline.
- `conflicts_with`: an incompatibility between object responsibilities/configurations, with explicit condition explained in prose. It does not mean all realizations of the method families are incompatible.
- `used_by`: component → architecture (not architecture → component).
- `tests`: hypothesis/evaluation → tested solution or architecture.
- `evaluated_by`: decision/solution/architecture/hypothesis → evaluation.
Stored directions permit inferred reverse relationships. Non-obvious relations are explained in the body. Substantive cards have at least two typed outbound relationships unless an explicit exception is documented. Body references use ordinary relative Markdown links; a bare ID is not a navigation link.

## Composition semantics
Relations encode object navigation, not a configuration solver. Do not invent a card for a dataset assumption merely to populate `requires`. Explain meaningful interactions in the card body:
- **Prerequisite:** information, admissibility condition or capability necessary to operate. Distinguish this from useful optional context and independently available evaluation labels.
- **Compatibility:** another component's role and the artifact exchanged. An `alternative_to` relation means substitution for the same decision; a constituent retrieval pass is normally a complement, not a competitor to its union.
- **Interaction risk:** how two otherwise legitimate modules can undermine assumptions (for example changed candidates invalidate calibration, or a false link is amplified by closure).
- **Conditional exclusion:** a task constraint that makes a particular combination inappropriate, not a universal ban on the families.

Keep these explanations as prose rather than new structured fields: time scope, trust, cost and output semantics are too contextual to encode reliably as unconditional graph edges. A scorer need not `conflict_with` connected components; bridge risk belongs to the accepted-edge/closure configuration. Explicit `requires` edges are appropriate only for a genuinely necessary knowledge object. No requirement exists to populate every relation name.

## Depth and evidence
L0 is compact discovery; L1 is a selective domain/decision comparison index; L2 is usually 400–900 words of substantive card body; L3 is optional advanced material. Look for mechanisms, assumptions, failure modes, evaluation and meaningful alternatives, not token headings. Word counts and keyword presence cannot establish adequacy. Check whether the mechanism and experiment genuinely distinguish alternatives. Mathematical consequences must state their assumptions. Proposed performance improvements are hypotheses unless source-specific measurements are actually cited. Derived examples are illustrative, never measured results.

Use `$...$` for inline math and separate `$$` lines for display equations, compatible with GitHub-flavored Markdown math. Keep equations substantive and define their quantities.

External-source claims use ledger-issued `[n]` citations and a Sources block per document. The shared ledger is `references/source-ledger.json`; [reference policy](references/evidence-policy.md) governs support. Do not invent bibliography metadata, empirical findings or URLs. Decision, Solution, Architecture and Hypothesis Cards declare an `evaluated_by` route explaining how evaluation could support adoption, rejection or an inconclusive result. A resolved link is not proof that its estimand fits the target project's question.

## Controlled applicability tags
- Labels: `no-labels`, `few-labels`, `rich-labels`.
- Quality: `clean`, `noisy`, `sparse`, `conflicting`.
- Scale/compute: `small-scale`, `large-scale`, `low-cost`, `compute-intensive`.
- Entities: `person`, `organization`, `address`, `identifiers`, `entity-agnostic`.
- Language: `monolingual`, `multilingual`, `multiscript`.
- Objectives: `high-precision`, `high-recall`, `asymmetric-costs`.
- Interpretation: `interpretable`, `calibration`, `uncertainty`.
- Lifecycle: `batch`, `incremental`, `streaming`, `federated`.
- Technical retrieval: `candidate-generation`, `blocking`, `multi-pass`, `evidence-engineering`, `missingness`, `frequency-aware`, `source-aware`, `pairwise`, `assignment`, `clustering`, `collective`, `constraints`, `provenance`, `human-review`, `evaluation`, `experimentation`, `governance`, `privacy`, `monitoring`.
Tags aid discovery, not proof of applicability or universal research priority. Their applicability must be explained by the card; label scarcity or a shared entity type alone is not a recommendation. Semantic overlap, excessive tags, contradictory guidance and unsupported evidence strength require substantive judgment, not a mechanical verdict.
