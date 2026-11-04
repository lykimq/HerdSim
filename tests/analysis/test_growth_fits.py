"""Growth-shape fits: intervals from curve values, and which shape the data prefer."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import cast

import numpy as np

from analysis.growth_fits import Interval, compare_shapes, interval_of, power_law, saturating

SIZES = [25, 50, 71, 100, 141, 200, 283, 400, 566, 800, 1131, 1600]


def points_from(
    curve: Callable[[np.ndarray, np.ndarray], np.ndarray],
    params: list[float],
) -> list[tuple[int, Interval]]:
    """Round the curve at each size to an integer D, then a +/- 0.5 interval."""
    d = np.rint(curve(np.array(SIZES, dtype=float), np.array(params)))
    return [(n, (float(v) - 0.5, float(v) + 0.5)) for n, v in zip(SIZES, d, strict=True)]


# --- intervals ---------------------------------------------------------------


def test_intervals_from_decided_bracketed_and_open_curves() -> None:
    assert interval_of(4.0, 4.0) == (3.5, 4.5)
    assert interval_of(4.0, 2.0) == (1.5, 4.5)  # bracket 2-4
    assert interval_of(float("nan"), 9.0) == (8.5, math.inf)  # [9]: no reliable D yet
    assert interval_of(float("nan"), float("nan")) is None


# --- shape preference --------------------------------------------------------


def test_each_shape_is_preferred_on_data_drawn_from_it() -> None:
    grows = points_from(power_law, [math.log(0.05), 0.7])  # 1 at N = 25, about 9 at 1600
    levels = points_from(saturating, [math.log(5.0), math.log(150.0)])  # tends to 6
    grows_fit = compare_shapes(grows)
    levels_fit = compare_shapes(levels)
    assert cast(float, grows_fit["log_odds_power_vs_saturating"]) > 0.0
    assert cast(float, levels_fit["log_odds_power_vs_saturating"]) < 0.0
    assert abs(cast(float, grows_fit["exponent_b"]) - 0.7) < 0.15
