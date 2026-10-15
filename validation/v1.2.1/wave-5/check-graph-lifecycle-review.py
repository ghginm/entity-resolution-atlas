"""Finite mathematical review witnesses, not an ER engine or population experiment.
Run from any cwd; JSON results are written only beside this uniquely named script.
"""
from itertools import combinations
from fractions import Fraction
import json
from pathlib import Path

results = []

def record(name, **details):
    results.append(dict(name=name, status="passed", **details))


def partition(vertices, edges):
    # Equivalence closure computed as repeated relation composition.
    relation = {(v, v) for v in vertices}
    relation |= {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    while True:
        enlarged = relation | {(a, d) for a, b in relation for c, d in relation if b == c}
        if enlarged == relation:
            break
        relation = enlarged
    return {frozenset(b for a, b in relation if a == v) for v in vertices}


def pairs(parts):
    return {frozenset(p) for group in parts for p in combinations(sorted(group), 2)}


def partitions(vertices):
    if not vertices:
        yield []
        return
    first, *tail = vertices
    for rest in partitions(tail):
        yield [{first}] + rest
        for i in range(len(rest)):
            yield rest[:i] + [rest[i] | {first}] + rest[i + 1:]

# Fixed graph order and deletion monotonicity, including isolated vertices.
v = list(range(4))
universe = list(combinations(v, 2))
examined = deletions = 0
for mask in range(1 << len(universe)):
    edges = [e for i, e in enumerate(universe) if mask & (1 << i)]
    base = partition(v, edges)
    assert base == partition(v, list(reversed(edges)))
    assert set().union(*base) == set(v)
    for edge in edges:
        revised = partition(v, [e for e in edges if e != edge])
        assert pairs(revised) <= pairs(base)
        deletions += 1
    examined += 1
record("fixed_graph_order_and_deletion", graphs=examined, edge_deletions=deletions)

for m, n in [(3, 3), (20, 30)]:
    left, right = list(range(m)), list(range(m, m + n))
    true = {frozenset(left), frozenset(right)}
    edges = list(zip(left, left[1:])) + list(zip(right, right[1:])) + [(left[-1], right[0])]
    false_pairs = pairs(partition(left + right, edges)) - pairs(true)
    assert len(false_pairs) == m * n
    record("bridge_amplification", sizes=[m, n], false_pairs=len(false_pairs), beyond_false_edge=len(false_pairs)-1)

tri = [(0, 1), (1, 2), (0, 2)]
assert len(partition([0, 1, 2], tri[:-1])) == 1
assert len(partition([0, 1, 2], [(0, 1)])) == 2
record("alternate_path_and_actual_split", triangle_after_one_deletion=1, chain_after_one_deletion=2)

chain = [(0, 1), (1, 2)]
chain_bridges = sum(len(partition([0, 1, 2], [x for x in chain if x != e])) > 1 for e in chain)
dense = list(combinations(range(6), 2))
dense_bridges = sum(len(partition(list(range(6)), [x for x in dense if x != e])) > 1 for e in dense)
assert chain_bridges == 2 and dense_bridges == 0
assert len(pairs(partition(list(range(6)), dense)) - pairs({frozenset(range(3)), frozenset(range(3,6))})) == 9
record("bridge_count_not_accuracy", true_chain_bridges=chain_bridges, wrong_dense_union_bridges=dense_bridges)

p3 = list(partitions(["a", "b", "c"]))
def together(p, a, b):
    return any(a in group and b in group for group in p)

feasible = [p for p in p3 if together(p, "a", "b") and together(p, "b", "c") and not together(p, "a", "c")]
assert not feasible
assert any(together(p, "a", "b") and not together(p, "a", "c") and not together(p, "b", "c") for p in p3)
record("constraint_logic", partitions_enumerated=len(p3), inconsistent_must_cannot_feasible=0, cannot_link_transitive=False)

# A preformed {a,b} cluster cannot union with {c} under cannot(a,c),
# although proposed endpoint pair b,c is itself not prohibited.
cl = frozenset(("a", "c"))
assert cl not in {frozenset(("b", "c"))}
assert cl <= {"a", "b", "c"}
record("whole_union_not_endpoint_check", endpoint_allowed=True, union_allowed=False)

# Finite optimization witness: capacity two, optional positive merges only.
weighted = {frozenset(("a", "b")): 10, frozenset(("a", "c")): 9, frozenset(("b", "d")): 9}
feasible4 = [p for p in partitions(["a", "b", "c", "d"]) if all(len(g) <= 2 for g in p)]
objective = lambda p: sum(w for edge, w in weighted.items() if any(edge <= group for group in p))
optimum = max(map(objective, feasible4))
greedy = [{"a", "b"}, {"c"}, {"d"}]
assert objective(greedy) == 10 and optimum == 18
record("feasible_greedy_not_optimal", greedy_value=objective(greedy), optimum=optimum)

# Signed inconsistent triangle: no partition can honor all labels as hard facts.
cost = lambda p: int(not together(p,"a","b")) + int(not together(p,"b","c")) + int(together(p,"a","c"))
assert min(map(cost, p3)) == 1
record("soft_labels_not_hard_admissibility", minimum_disagreements=1)

# Two coherent partition distributions with identical AB/BC marginals.
model1 = [(Fraction(8,10), [{"a","b","c"}]), (Fraction(1,10), [{"a","b"},{"c"}]), (Fraction(1,10), [{"a"},{"b","c"}])]
model2 = [(Fraction(9,10), [{"a","b","c"}]), (Fraction(1,10), [{"a"},{"b"},{"c"}])]
for model in (model1, model2):
    assert sum(w for w,p in model) == 1
    assert sum(w for w,p in model if together(p,"a","b")) == Fraction(9,10)
    assert sum(w for w,p in model if together(p,"b","c")) == Fraction(9,10)
joints = [sum(w for w,p in model if len(p)==1) for model in (model1, model2)]
assert joints == [Fraction(8,10), Fraction(9,10)]
record("edge_marginals_not_cluster_probability", edge_marginals=["9/10","9/10"], all_same_probabilities=list(map(str,joints)), independent_product="81/100")

# Countermodel to disjoint validity => cannot-link under single occupancy.
observations = [("same-person", "address-A", 0, 1), ("same-person", "address-B", 1, 2)]
for t in [Fraction(0), Fraction(1,2), Fraction(1), Fraction(3,2)]:
    assert sum(start <= t < end for _,_,start,end in observations) <= 1
assert observations[0][3] <= observations[1][2]
assert observations[0][0] == observations[1][0]
record("disjoint_validity_single_occupancy_countermodel", intervals=[[0,1],[1,2]], single_occupancy=True, same_enduring_entity=True)

# Deletion reveals an eligible but previously unstored top-1 competitor.
ranked = [("b", 9), ("c", 8)]
stored = ranked[:1]
repaired_from_stored = [x for x in stored if x[0] != "b"][:1]
requeried = [x for x in ranked if x[0] != "b"][:1]
assert repaired_from_stored == [] and requeried == [("c", 8)]
record("delete_top_k_requires_new_retrieval", stored_only=repaired_from_stored, full_eligible=requeried)

# Source revision precedence independent of ingestion order.
events = [(2, "tombstone"), (1, "live")]
assert events[-1][1] == "live" and max(events)[1] == "tombstone"
record("stale_update_not_resurrection", last_arrival="live", revision_order="tombstone")

# Distinct valid-time and system-time projections.
obs = [("old-address", 0, 1, 2), ("new-address", 1, 3, 1)]
current = [name for name,start,end,received in obs if start <= 2 < end]
last_arrival = max(obs, key=lambda x:x[3])[0]
assert current == ["new-address"] and last_arrival == "old-address"
record("valid_time_not_ingestion", valid_current=current, last_arrival=last_arrival)

# A read-version check followed by a separate write allows stale publication.
base = 1
validated = base == 1
base = 2  # concurrent correction
assert validated and base != 1
record("check_then_write_race", prior_check_passed=validated, atomic_compare_would_reject=base != 1)

# Membership equality cannot remove split identifier ambiguity.
old = {"a","b"}
children = [{"a"},{"b"}]
assert set().union(*children) == old and len(children) == 2
record("split_not_single_target_redirect", historical_members=sorted(old), possible_children=len(children))

output = {"scope": "adversarial finite mathematical witnesses only; not canonical implementation or empirical utility validation", "checks": results, "check_count": len(results), "failed": 0}
path = Path(__file__).with_name("check-graph-lifecycle-review.output.json")
path.write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))
