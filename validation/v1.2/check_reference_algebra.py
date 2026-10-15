#!/usr/bin/env python3
"""Finite algebra sanity checks for documentation; no ER data or matcher."""
from fractions import Fraction
from itertools import combinations, product
import json
from math import comb


def check():
    bounds = 0
    for positive_count in range(1, 6):
        for accepted_positive in range(positive_count + 1):
            for unknown_inside in range(5):
                for unknown_outside in range(5):
                    values = [
                        Fraction(accepted_positive + x, positive_count + x + z)
                        for x in range(unknown_inside + 1)
                        for z in range(unknown_outside + 1)
                    ]
                    assert min(values) == Fraction(
                        accepted_positive, positive_count + unknown_outside)
                    assert max(values) == Fraction(
                        accepted_positive + unknown_inside,
                        positive_count + unknown_inside)
                    bounds += 1

    variances = 0
    for population_size in range(2, 7):
        for sample_size in range(1, population_size):
            pi = Fraction(sample_size, population_size)
            joint = Fraction(sample_size * (sample_size - 1),
                             population_size * (population_size - 1))
            for outcome in product((0, 1), repeat=population_size):
                totals = [
                    sum(Fraction(outcome[i], 1) / pi for i in sample)
                    for sample in combinations(range(population_size), sample_size)
                ]
                mean = sum(totals) / len(totals)
                variance = sum((value - mean) ** 2 for value in totals) / len(totals)
                indicator_variance = sum(
                    ((pi if i == j else joint) - pi * pi)
                    * outcome[i] * outcome[j] / (pi * pi)
                    for i in range(population_size)
                    for j in range(population_size)
                )
                assert mean == sum(outcome)
                assert variance == indicator_variance
                variances += 1

    zero_events = 0
    for population_size in range(2, 10):
        for sample_size in range(1, population_size + 1):
            for error_count in range(population_size + 1):
                zeros = sum(
                    1 for sample in combinations(range(population_size), sample_size)
                    if not any(i < error_count for i in sample)
                )
                numerator = (comb(population_size - error_count, sample_size)
                             if population_size - error_count >= sample_size else 0)
                assert Fraction(zeros, comb(population_size, sample_size)) == Fraction(
                    numerator, comb(population_size, sample_size))
                zero_events += 1

    # Review counterexamples: definitions/finite-set arithmetic, not an ER run.
    universe = set(combinations(range(4), 2))
    truth = {(0, 1), (2, 3)}
    opaque_candidates = {(0, 1), (0, 2)}
    pi = Fraction(3, len(universe))
    samples = list(combinations(universe, 3))
    mean_inside = sum(sum(Fraction(1, 1) / pi for i in s
                          if i in truth & opaque_candidates)
                      for s in samples) / len(samples)
    mean_outside = sum(sum(Fraction(1, 1) / pi for i in s
                           if i in truth - opaque_candidates)
                       for s in samples) / len(samples)
    assert mean_inside == mean_outside == 1
    assert Fraction(len(truth - opaque_candidates), len(truth)) == Fraction(1, 2)

    asserted = {(0, 1), (0, 2), (1, 2)}
    cross_file = {(0, 2), (1, 2)}
    assert Fraction(len(asserted & cross_file), len(asserted)) == Fraction(2, 3)
    assert Fraction(len(asserted & cross_file), len(asserted & cross_file)) == 1

    assert (4 * Fraction(1, 4) + 1) / 5 == Fraction(2, 5)
    assert (Fraction(1, 4) + 1) / 2 == Fraction(5, 8)
    assert Fraction(1, 5) * Fraction(1, 2) == Fraction(1, 2) * Fraction(1, 5)

    retained = [k for k in range(101)
                if Fraction(comb(100-k, 10) if 100-k >= 10 else 0,
                            comb(100, 10)) >= Fraction(1, 20)]
    assert max(retained) == 24

    return {
        'kind': 'algebraic sanity checks, not ER experiments or proof of asymptotic coverage',
        'recall_bound_configurations': bounds,
        'HT_mean_and_variance_configurations': variances,
        'hypergeometric_zero_event_configurations': zero_events,
        'review_regression_checks': [
            'frozen black-box output needs evaluation, not production, inclusion',
            'pair denominators restricted to the same semantic universe',
            'record-average versus entity-average B-cubed',
            'SCAR propensity and true posterior can trade off',
            'discrete fixed-size zero-event endpoint',
        ],
        'passed': True,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
