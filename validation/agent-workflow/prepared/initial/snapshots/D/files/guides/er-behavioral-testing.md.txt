# ER behavioral testing: fixtures, relations, and counterexamples

This supporting guide develops [EVAL-11-006](../evaluation/synthetic-metamorphic.md); it is not a sixth card type, an ER implementation, or measured accuracy evidence. All ER examples below are proposed illustrative tests, not reported experiments. Synthetic success cannot establish world accuracy.

## Separate three testing roles

- **Example/controlled fixture:** author a small world with explicit entities, observations, namespaces, validity times, and expected decisions. The oracle comes from that construction, not from the resolver being tested.
- **Metamorphic relation:** transform a base input and check a domain-justified relation between outputs even when the full correct output is unavailable. Chen, Cheung, and Yiu motivate follow-up cases from apparently successful input/output cases, with examples whose relations depend on the problem domain.[19]
- **Property-based test:** generate admissible inputs and check a stated contract. The Hypothesis introduction illustrates input strategies, assertions, and equivalence to a reference implementation, and treats these tests as additions to example tests.[22] This guide does not prescribe that library or any implementation framework.

A metamorphic relation can be checked with a property generator. A controlled fixture can anchor both. Nevertheless, relation satisfaction, constructed-world identity accuracy, and real-population accuracy are distinct outputs.

## Write a behavior specification before generating cases

For each test, record:

1. **Contract owner/artifact:** normalization output, candidates, scorer, disposition policy, assignment, partition, or stable identity state; link the relevant card and version.
2. **Semantic preconditions:** same-as scope, source roles, namespaces, validity time, cardinality, loss policy, admissible context, and state assumptions.
3. **Input construction:** base fixture, transformations, seed/family, generator support, expected boundary cases, and untouched facts.
4. **Expected relation/oracle:** what must remain equal, change, stay feasible, abstain, or escalate; define semantic equality and any tolerance before results.
5. **Observation and triage:** output differences, first violating stage, error/timeout, oracle uncertainty, counterexample, and exception rationale.

Do not require bitwise-equal entity identifiers when only partition equality is promised; compare co-membership under a record mapping. Conversely, persistent-ID continuity needs its own state contract and cannot be inferred from partition equality. A graph trace may change ordering while memberships remain identical.

## Controlled duplicates without impossible cardinality

Construct latent entity `E` with two observations in a deduplication fixture, varying only policy-approved formatting while preserving reliable identity evidence. Add a distinct same-name entity `F` with different namespace-qualified identity and source/time facts. Check the expected duplicate pair and the collision control; matching everything passes an invariance-only test but fails this known fixture.

For [one-to-one linkage](../solutions/decision-resolution/one-to-one-assignment.md), construct one observation of `E` in source A and one in source B, with unmatched records elsewhere. Do not insert a second same-entity A row and demand both match the one B row. That violates the duplicate-free prerequisite. Test either documented rejection/escalation of this out-of-contract input or audited entity units after within-source deduplication. Neither response proves identity accuracy.

Separate **duplicate observation** from **duplicate delivery**: repeated ingestion of the same versioned event should leave identity state unchanged only if replay idempotency is promised. A genuinely new observation has different provenance and may legitimately alter evidence, membership, and attributes. Preserve that distinction when building regression cases.

## Required patterns and their invalid generalizations

| Pattern | Legitimate conditional expectation | Counterexample / boundary |
|---|---|---|
| Formatting only | Under an explicit policy that collapses trailing whitespace and case for a particular field/source, those edits preserve the declared representation or downstream identity disposition | Leading zeros in an identifier, legal suffixes, script distinctions, or case-sensitive namespaces may be meaningful; do not normalize them by default |
| Irrelevant metadata | Changing a field explicitly excluded from evidence, routing, policy, and state does not change promised identity output | A source-trust flag, observation time, review authorization, or routing hint is not irrelevant merely because it is not a name |
| Record/order permutation | A stateless batch contract promising order independence, with canonical tie rules, produces semantically equivalent output on the same record set and fixed graph | Stateful/adaptive resolution or a documented greedy processing order may legitimately differ; freeze initial state and test its promised replay/ordering rule instead |
| Namespace reuse | The token `417` in two distinct registries does not by itself imply identity | A separately audited crosswalk can establish same-as; absent a crosswalk, token equality alone has no universal positive or negative truth |
| Subsidiary versus parent | In a legal-entity identity task, ownership is related-to, not same-as; shared brand/address does not erase distinct legal entities | In an explicitly defined corporate-group task, grouping may be intended; changing the identity unit changes the oracle |
| Weak bridge | One weak agreement must not silently acquire policy authority as a cluster-wide identity assertion | If that edge is accepted and fixed-graph connected components is the promised resolver, closure joins its components; universal bridge rejection would contradict its mechanism |

These are Atlas test proposals conditioned on project policy, not external empirical findings. Include both preserving and identity-changing transformations. Without the latter, a constant output can satisfy many preserving relations while being useless.

## Weak bridges: test the policy and the resolver separately

Construct two internally connected groups with distinct fixture identities. Provide one weak cross-group similarity below the declared acceptance boundary. At the **policy** boundary, check that it remains rejected or deferred and is not silently converted into an accepted same-as edge. At the **resolver** boundary, inspect the actual accepted graph, not a raw similarity graph.

Then deliberately accept the bridge in a controlled diagnostic. [Connected components](../solutions/decision-resolution/connected-components.md) should join the groups: this is conformance to closure and, in the constructed world, an identity error. Report both facts. It is not a closure implementation defect. Removing the bridge splits only if no alternative accepted path exists.

For [constrained partitioning](../solutions/decision-resolution/constrained-clustering.md), add an independently valid cannot-link across the groups. Check that a hard-admissibility variant does not produce a violating cluster and escalates an infeasible must-link/cannot-link combination. A soft-penalty variant has a different contract. Do not invent a hard cannot-link from an unscored or merely weak pair; satisfying fabricated constraints would reward undermerge.

## Property patterns beyond fixed examples

- **Representation round trip:** raw observation plus lineage survives permitted serialization/reconstruction. Normalization may be lossy, so reconstructing the raw string from normalized text is not automatically required.
- **Pair symmetry:** swapping endpoints preserves evidence/disposition only for a contract with symmetric source roles and comparison semantics. Directional authority or assignment output requires a role-aware mapped relation instead.
- **Normalization idempotency:** applying a declared canonicalization twice equals applying it once. Context enrichment that changes with state/time is not necessarily canonicalization.
- **Membership feasibility:** every required record is represented once in a complete partition; explicit unresolved outputs remain distinguishable. Partial partitions must follow their own representation contract.
- **Unmatched capacity:** multiple unrelated endpoints can remain unmatched in partial assignment; do not force them through a single capacity-limited shared dummy.
- **Unknown-state preservation:** missing candidates, invalid fields, deferred decisions, and independently adjudicated nonmatches remain distinct artifacts.
- **Reference equivalence:** compare an optimized stage against a transparent trusted stage only on their shared valid domain and semantics. Agreement between two implementations of the same mistaken policy is not truth.

Generate boundary cases around threshold ties, missing/invalid/conflicting evidence, duplicate names, trusted constraint conflicts, and alternate paths. Minimize a failure while preserving the preconditions that make it a counterexample. A two-record simplification that removes the namespace/time conflict may no longer explain the original bug.

## Discovery, confirmation, and regression suites

Keep development fixture discovery separate from confirmation. Inspecting a final holdout to invent properties or tune transformations spends that holdout; it cannot remain untouched final evidence. Version generators, oracle rules, transformation sets, and initial state. If a confirmed failure motivates a repair, retain the original evidence and acquire fresh confirmation rather than silently reclassify the repaired rerun as the original prospective test.

Maintain a compact regression suite containing reviewed failures and boundary controls, with rationale for each expected output. Add a new case after distinguishing implementation failure from a bad property or unsupported fixture. Do not update expectations solely to match the current resolver. Keep quarantined/unknown cases visible. Regression suites are intentionally selected and their violation fraction is not a random-world failure rate.

Use a separate fixed-generator confirmation sample to estimate behavior under that generated domain. Compare baseline/challenger on paired fixture families. Record eligible/evaluated counts, errors, unknown oracles, violations by contract, and run variation; apply [EVAL-11-006](../evaluation/synthetic-metamorphic.md#statistical-uncertainty) for uncertainty instead of treating every transformed row as independent. Predeclare critical contract guardrails rather than dilute severe violations in a global average.

## Output artifact and decision

A behavioral report should contain contract/version, generator/suite scope, fixture mapping, frozen configurations, denominators, execution coverage, paired differences, uncertainty where justified, minimized counterexamples, triage dispositions, and unresolved limits. Link the [controlled comparison](../solutions/experimentation/controlled-comparison.md) and [plan template](experiment-plan-template.md) for adoption/rejection/inconclusive rules. Passing these checks only removes specific behavioral objections; use independent [entity quality](../evaluation/entity-resolution-quality.md) and other output-appropriate references before claiming deployment accuracy.

## Evidence limitations

Source [19] supports general metamorphic testing and domain-dependent follow-up relations; source [22] supports property-based generation/assertion concepts and the need for appropriate input domains. Neither evaluates these ER fixtures, authorizes a library installation, or proves correctness. No proposed test is executed in this knowledge repository.

## Sources

[19] https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf — Metamorphic Testing: A New Approach for Generating Next Test Cases
[22] https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html — Hypothesis: Introduction to property-based testing
