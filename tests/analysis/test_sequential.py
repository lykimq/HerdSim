"""Exact decision rates of the per-cell stopping rule, on cases with a known answer."""

from __future__ import annotations

import pytest
from scipy.stats import binom

from analysis.frontier import (
    RELIABLE,
    UNDECIDED,
    UNRELIABLE,
    clopper_pearson,
    reliability_status,
)
from analysis.sequential import decision_rates

THETA, CONFIDENCE = 0.90, 0.99
BATCH, MAX_SEEDS = 10, 200


@pytest.mark.parametrize(("p", "certain"), [(0.0, UNRELIABLE), (1.0, RELIABLE)])
def test_a_certain_cell_is_always_decided_its_way(p: float, certain: str) -> None:
    rates = decision_rates(p, THETA, CONFIDENCE, BATCH, MAX_SEEDS)
    assert rates[certain] == pytest.approx(1.0, abs=1e-12)


@pytest.mark.parametrize("p", [0.5, 0.85, 0.90, 0.95, 0.97])
def test_every_cell_ends_reliable_unreliable_or_undecided(p: float) -> None:
    rates = decision_rates(p, THETA, CONFIDENCE, BATCH, MAX_SEEDS)
    assert sum(rates.values()) == pytest.approx(1.0, abs=1e-12)


@pytest.mark.parametrize("p", [0.85, 0.95])
def test_one_look_matches_the_binomial_sum(p: float) -> None:
    """With one batch of all the seeds there are no repeated looks to carry mass through."""
    n = 60
    expected = {RELIABLE: 0.0, UNRELIABLE: 0.0, UNDECIDED: 0.0}
    for k in range(n + 1):
        status = reliability_status(*clopper_pearson(k, n, CONFIDENCE), THETA)
        expected[status] += float(binom.pmf(k, n, p))
    rates = decision_rates(p, THETA, CONFIDENCE, batch=n, max_seeds=n)
    assert rates == pytest.approx(expected, abs=1e-12)
