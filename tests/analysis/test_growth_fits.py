"""Growth-shape fits: intervals from the curve values, and a shape found on data made from it."""

from __future__ import annotations

import math

import numpy as np

from analysis.growth_fits import compare, interval_of, power_law, saturating

SIZES = [25, 50, 71, 100, 141, 200, 283, 400, 566, 800, 1131, 1600]


def test_intervals_from_decided_bracketed_and_open_curves():
    assert interval_of(4.0, 4.0) == (3.5, 4.5)
    assert interval_of(4.0, 2.0) == (1.5, 4.5)  # bracket 2-4
    assert interval_of(float("nan"), 9.0) == (8.5, math.inf)  # [9]: no reliable D yet
    assert interval_of(float("nan"), float("nan")) is None


def points_from(curve, params) -> list[tuple[int, tuple[float, float]]]:
    d = np.rint(curve(np.array(SIZES, dtype=float), np.array(params)))
    return [(n, (v - 0.5, v + 0.5)) for n, v in zip(SIZES, d)]


def test_each_shape_is_preferred_on_data_drawn_from_it():
    grows = points_from(power_law, [math.log(0.05), 0.7])  # 1 at N = 25, about 9 at 1600
    levels = points_from(saturating, [math.log(5.0), math.log(150.0)])  # tends to 6
    assert compare(grows)["log_odds_power_vs_saturating"] > 0.0
    assert compare(levels)["log_odds_power_vs_saturating"] < 0.0
    assert abs(compare(grows)["exponent_b"] - 0.7) < 0.15
