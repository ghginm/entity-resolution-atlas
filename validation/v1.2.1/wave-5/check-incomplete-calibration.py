"""Bounded synthetic mathematical checks; not ER data or model evaluation.
Run from repository root: python validation/v1.2.1/wave-5/check-incomplete-calibration.py
Stdlib only. Prints JSON, reads no repository/benchmark input, writes no files.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json

results = {}

def record(name, **values):
    def clean(x):
        if isinstance(x, F):
            return {"exact": str(x), "decimal": float(x)}
        if isinstance(x, dict):
            return {k: clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [clean(v) for v in x]
        return x
    results[name] = clean(values)

# Exhaust all free binary pair assignments in a bounded family.
cases = assignments = 0
for p in range(1, 5):
    for a in range(p + 1):
        for ua, uo in product(range(4), repeat=2):
            d = a + ua + 1  # one known asserted negative, arbitrary outside positives
            observed_p, observed_r = [], []
            for bits in product((0, 1), repeat=ua + uo):
                x, z = sum(bits[:ua]), sum(bits[ua:])
                observed_p.append(F(a + x, d))
                observed_r.append(F(a + x, p + x + z))
                assignments += 1
            assert (min(observed_p), max(observed_p)) == (F(a, d), F(a + ua, d))
            assert (min(observed_r), max(observed_r)) == (F(a, p + uo), F(a + ua, p + ua))
            cases += 1
record("finite_pair_bounds", parameter_cases=cases, binary_assignments=assignments)

# A pair partition is stricter than freely choosing unknown pair statuses.
def partitions(items):
    if not items:
        yield []
        return
    head, *tail = items
    for blocks in partitions(tail):
        yield [{head}] + blocks
        for j in range(len(blocks)):
            yield blocks[:j] + [blocks[j] | {head}] + blocks[j + 1:]

feasible = []
for blocks in partitions(list(range(4))):
    truth = {pair for block in blocks for pair in combinations(sorted(block), 2)}
    if {(0, 1), (1, 2)} <= truth:
        feasible.append((F(int((0, 2) in truth)), F(int((0, 2) in truth), len(truth))))
assert len(feasible) == 2
assert min(p for p, r in feasible) == 1
assert (min(r for p, r in feasible), max(r for p, r in feasible)) == (F(1, 6), F(1, 3))
record("equivalence_constraints", free_precision_bounds=[0, 1], free_recall_bounds=[0, F(1, 3)],
       feasible_partitions=len(feasible), constrained_precision_bounds=[1, 1], constrained_recall_bounds=[F(1, 6), F(1, 3)])

# Fixed-size unequal-probability sample of one of two accepted units, y=(1,0).
q = [F(1, 10), F(9, 10)]
y = [1, 0]
ht_precision = [F(y[i], 2) / q[i] for i in range(2)]
ratio_precision = [F(v) for v in y]
e_ht = sum(q[i] * ht_precision[i] for i in range(2))
e_ratio = sum(q[i] * ratio_precision[i] for i in range(2))
assert e_ht == F(1, 2) and max(ht_precision) == 5 and e_ratio == F(1, 10)
# Same design, both outcomes positive, A={first}: estimated recall is 1 or 0.
recall_ratios = [F(1), F(0)]
assert sum(q[i] * recall_ratios[i] for i in range(2)) == F(1, 10)
record("ht_and_ratio", true_precision=F(1, 2), ht_realizations=ht_precision,
       expected_ht=e_ht, expected_normalized_precision=e_ratio,
       separate_true_recall=F(1, 2), expected_recall_ratio=F(1, 10))

# PU observational equivalence: same X distribution and g(x), different truth.
g = [F(1, 10), F(1, 5)]
models = []
for c in [F(1, 4), F(1, 2)]:
    posterior = [v / c for v in g]
    assert all(0 <= p <= 1 for p in posterior)
    assert [c * p for p in posterior] == g
    prevalence = sum(posterior) / 2
    # Mean g(X) on labeled positives = c E[f(X)^2]/E[f(X)], not generally c.
    e1_limit = sum(g[i] * g[i] for i in range(2)) / sum(g)
    models.append({"c": c, "truth_posteriors": posterior, "prevalence": prevalence,
                   "mean_g_on_labeled_positive": e1_limit})
assert models[0]["prevalence"] != models[1]["prevalence"]
record("pu_nonidentification", observed_label_posteriors=g, equal_feature_mass=True, models=models)

# Exact agreement blocking has candidate LR=1; prior-only double use is wrong.
prior_odds = F(1, 99)
q_m, q_u = F(4, 5), F(1, 10)
unconditional_lr = q_m / q_u
candidate_odds = prior_odds * unconditional_lr
posterior = candidate_odds / (1 + candidate_odds)
wrong_odds = candidate_odds * unconditional_lr
wrong_posterior = wrong_odds / (1 + wrong_odds)
assert posterior == F(8, 107) and wrong_posterior == F(64, 163)
record("exact_blocking", candidate_lr=1, compatible_posterior=posterior, double_counted_posterior=wrong_posterior)

# A OR B selection destroys independent feature factorization.
p00_before, selected_mass = F(1, 4), F(3, 4)
p_a0 = F(1, 4) / selected_mass
p_b0 = p_a0
assert p_a0 * p_b0 == F(1, 9)
record("or_selection", independent_bernoulli_half=True, candidate_joint_00=0,
       candidate_marginal_product_00=p_a0 * p_b0)

# Full-X deterministic selection leaves posterior unchanged within common support.
# Coarsen X to constant gamma: omitted selection feature can change it.
# P(X=easy)=P(X=hard)=1/2, true rates .8 and .2, include only easy.
record("omitted_selection_feature", posterior_given_easy=F(4, 5),
       posterior_given_constant_gamma=F(1, 2), posterior_given_gamma_and_candidate=F(4, 5))

# Correct class-only sampling odds adjustment; feature-dependent adjustment differs.
target_odds = F(1, 9)
sampled_odds = target_odds * F(1, 1) / F(1, 9)
assert sampled_odds == 1
record("labeled_selection", target_probability=F(1, 10), sampled_probability=F(1, 2),
       correct_odds_multiplier=F(1, 9),
       two_feature_specific_selection_ratios=[9, 3])

# All predictions .5, equal source masses: globally calibrated, unsafe slices.
source_rates = [F(9, 10), F(1, 10)]
pooled_rate = sum(source_rates) / 2
brier = sum(r * F(1, 4) + (1-r) * F(1, 4) for r in source_rates) / 2
assert pooled_rate == F(1, 2) and brier == F(1, 4)
context_posteriors = []
for prior in [F(1, 10), F(1, 2)]:
    odds = prior / (1 - prior) * 4
    context_posteriors.append(odds / (1 + odds))
record("pooled_calibration_and_context_priors", prediction=F(1, 2), source_rates=source_rates,
       pooled_ece=0, source_absolute_calibration_errors=[F(2, 5), F(2, 5)],
       pooled_brier=brier, constant_discrimination=True, identical_lr=4,
       context_posteriors=context_posteriors)

# Known true clusters of sizes one and three, prediction merges all four.
record_b3 = (F(1, 4) + 3 * F(3, 4)) / 4
entity_b3 = (F(1, 4) + F(3, 4)) / 2
assert record_b3 == F(5, 8) and entity_b3 == F(1, 2)
record("b3_denominators", record_precision=record_b3, entity_precision=entity_b3,
       recall=1, clipped_singleton_precision=1, full_singleton_precision=F(1, 4))

# Correct inclusion of an entity of size three among ten records, two draws.
wr = 1 - (1 - F(3, 10)) ** 2
wor = 1 - F(comb(7, 2), comb(10, 2))
assert wr == F(51, 100) and wor == F(8, 15)
record("entity_inclusion", entity_size=3, records=10, seed_draws=2,
       per_draw=F(3, 10), with_replacement_unique=wr, without_replacement_unique=wor)

# Invert zero errors under SRSWOR; enumerate all true K for coverage.
N, n, alpha = 100, 10, F(1, 20)
def zero_probability(k):
    return F(comb(N-k, n), comb(N, n)) if N-k >= n else F(0)
upper = max(k for k in range(N + 1) if zero_probability(k) >= alpha)
assert zero_probability(upper) >= alpha > zero_probability(upper + 1)
# For this zero branch only, exclusion probability for K>upper is <=alpha.
assert all(zero_probability(k) <= alpha for k in range(upper + 1, N + 1))
record("zero_discovery", population=N, sample=n, alpha=alpha, upper_error_total=upper,
       zero_probability_at_upper=zero_probability(upper), zero_probability_at_next=zero_probability(upper+1))

# Enumerate a genuine SRS of pairs sharing records; compare exact HT variance.
# Pair endpoints are labels only: the randomization is over fixed pair units.
pair_units = list(combinations(range(4), 2))
fixed_z = [F(int(0 in pair)) for pair in pair_units]
N_pairs, n_pairs = len(pair_units), 2
pi = F(n_pairs, N_pairs)
pi_joint = F(n_pairs * (n_pairs - 1), N_pairs * (N_pairs - 1))
estimates = [sum(fixed_z[i] / pi for i in sample)
             for sample in combinations(range(N_pairs), n_pairs)]
mean_estimate = sum(estimates) / len(estimates)
exact_variance = sum((value - mean_estimate) ** 2 for value in estimates) / len(estimates)
covariance_variance = sum(
    ((pi if i == j else pi_joint) - pi * pi) / (pi * pi) * fixed_z[i] * fixed_z[j]
    for i, j in product(range(N_pairs), repeat=2))
assert mean_estimate == sum(fixed_z) == 3
assert exact_variance == covariance_variance == F(18, 5)
record("shared_endpoint_srs", pair_units=N_pairs, sample_size=n_pairs,
       enumerated_samples=len(estimates), expected_ht=mean_estimate,
       enumeration_variance=exact_variance, covariance_formula_variance=covariance_variance)

# General candidate-conditioning identity with feature-dependent q_M/q_U.
prior = F(1, 5)
m, u = [F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]
qm, qu = [F(1, 2), F(1)], [F(1, 4), F(1, 2)]
p_cm = sum(qm[i] * m[i] for i in range(2))
p_cu = sum(qu[i] * u[i] for i in range(2))
prior_c_odds = prior / (1-prior) * p_cm / p_cu
candidate_posteriors = []
for i in range(2):
    m_c, u_c = qm[i] * m[i] / p_cm, qu[i] * u[i] / p_cu
    assert m_c / u_c == m[i] / u[i] * qm[i] / qu[i] * p_cu / p_cm
    odds_by_candidate = prior_c_odds * m_c / u_c
    odds_by_joint = prior / (1-prior) * m[i] / u[i] * qm[i] / qu[i]
    assert odds_by_candidate == odds_by_joint
    candidate_posteriors.append(odds_by_joint / (1 + odds_by_joint))
record("general_selection_identity", candidate_posteriors=candidate_posteriors,
       candidate_match_inclusion=p_cm, candidate_nonmatch_inclusion=p_cu)

print(json.dumps({"scope": "synthetic mathematics only; no measured ER claims", "checks": results,
                  "status": "all assertions passed"}, indent=2))
