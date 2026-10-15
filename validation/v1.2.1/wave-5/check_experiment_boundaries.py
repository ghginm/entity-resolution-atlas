#!/usr/bin/env python3
"""Finite documentation counterexamples, NOT ER/model/engineering measurements."""
from fractions import Fraction as F
from itertools import product
import json
from math import log


def check():
    # DEC-12-001: an interaction is specific to its response scale.
    cells = {(0, 0): F(1, 5), (1, 0): F(2, 5),
             (0, 1): F(3, 10), (1, 1): F(1, 2)}
    interaction = (cells[1, 1] - cells[1, 0]) - (cells[0, 1] - cells[0, 0])
    logits = {key: log(float(p / (1 - p))) for key, p in cells.items()}
    logit_interaction = (logits[1, 1] - logits[1, 0]) - (logits[0, 1] - logits[0, 0])
    assert interaction == 0 and abs(logit_interaction) > 0.1

    # Fixed-pool recall is not recall over all true pairs in an eligible frame.
    truth_count = 100
    a_retrieved, a_correct = 20, 20
    b_retrieved, b_correct = 90, 72
    conditional = (F(a_correct, a_retrieved), F(b_correct, b_retrieved))
    end_to_end = (F(a_correct, truth_count), F(b_correct, truth_count))
    assert conditional[0] > conditional[1] and end_to_end[0] < end_to_end[1]

    # EVAL-11-007: equal marginal edge inclusion need not imply equal graph law.
    # Three vertices, three possible edges; any two edges connect all vertices.
    law_a = {(0, 0, 0): F(1, 2), (1, 1, 1): F(1, 2)}
    law_b = {(0, 0, 0): F(1, 4), (1, 1, 0): F(1, 4),
             (1, 0, 1): F(1, 4), (0, 1, 1): F(1, 4)}
    marginals = [tuple(sum(state[i] * p for state, p in law.items())
                       for i in range(3)) for law in (law_a, law_b)]
    connectivity = [sum(p for state, p in law.items() if sum(state) >= 2)
                    for law in (law_a, law_b)]
    assert marginals[0] == marginals[1] == (F(1, 2),) * 3
    assert connectivity == [F(1, 2), F(3, 4)]

    # A count match is not required logical-unit completion.
    required, completed = {'pair-a/route-1', 'pair-b/route-1'}, {'pair-a/route-1', 'pair-c/route-1'}
    assert len(required) == len(completed) and required != completed
    assert len(required - completed) == 1 and not completed <= required

    # SOL-02-002: repeated consumption of a cached draw is not independent draws.
    n = 4
    independent_means = [F(sum(draws), n) for draws in product((0, 1), repeat=n)]
    cached_means = [F(0), F(1)]
    independent_variance = sum((x - F(1, 2)) ** 2 for x in independent_means) / len(independent_means)
    cached_variance = sum((x - F(1, 2)) ** 2 for x in cached_means) / len(cached_means)
    assert independent_variance == F(1, 4 * n)
    assert cached_variance == F(1, 4) > independent_variance

    # An interval containing zero can fail a declared equivalence criterion.
    low, high, margin = F(-3, 10), F(3, 10), F(1, 20)
    assert low <= 0 <= high and not (-margin < low and high < margin)

    return {
        'kind': 'finite-documentation-counterexamples-not-empirical-results',
        'checks': 6,
        'passed': True,
        'interaction_raw_scale': str(interaction),
        'interaction_logit_scale': logit_interaction,
        'conditional_recall_A_B': list(map(str, conditional)),
        'eligible_truth_recall_A_B': list(map(str, end_to_end)),
        'edge_marginals_A_B': [list(map(str, m)) for m in marginals],
        'connected_probability_A_B': list(map(str, connectivity)),
        'missing_required_units': sorted(required - completed),
        'independent_mean_variance': str(independent_variance),
        'cached_mean_variance': str(cached_variance),
        'interval': [str(low), str(high)],
        'equivalence_margin': str(margin),
        'limits': ['Invented finite mathematical examples only; no observed project data.',
                   'No asymptotic coverage, production correctness or utility claim.',
                   'These challenge prohibited inferences already bounded in the reviewed text.'],
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
