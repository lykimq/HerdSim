"""Exact decision rates of the per-cell rule: a cell with true success rate p, looked at after
every batch of seeds until it is decided or has max_seeds.

Computed, not simulated: the distribution of successes is carried batch by batch, and the mass
that a look decides is taken out, so the rates count the repeated looks.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import binom

from .frontier import RELIABLE, UNRELIABLE, clopper_pearson, reliability_status


def decision_rates(
    p: float, theta: float, confidence: float, batch: int, max_seeds: int
) -> dict[str, float]:
    """Chance that a cell with success rate ``p`` ends reliable, unreliable or open."""
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"success rate {p} is not in [0, 1]")
    open_mass = np.array([1.0])  # open_mass[k]: chance of k successes and still open
    decided = {RELIABLE: 0.0, UNRELIABLE: 0.0}
    looks = [*range(batch, max_seeds, batch), max_seeds]  # the last batch may be partial
    for prev, n in zip([0, *looks], looks):
        open_mass = np.convolve(open_mass, binom.pmf(np.arange(n - prev + 1), n - prev, p))
        for k in range(n + 1):
            status = reliability_status(*clopper_pearson(k, n, confidence), theta)
            if status in decided:
                decided[status] += float(open_mass[k])
                open_mass[k] = 0.0
    return {**decided, "open": float(open_mass.sum())}
