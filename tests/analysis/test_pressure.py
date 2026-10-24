"""Pressure measures: the distance shares and their sum over a trial."""

from __future__ import annotations

import numpy as np
import pytest

from analysis.pressure import Pressure, near_shares


def test_near_shares_count_sheep_strictly_inside_each_radius():
    sheep = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 3.0], [100.0, 100.0]])
    dogs = np.array([[0.0, 1.0], [10.0, 5.0]])
    # nearest dog: 1, 5, 2, far. Inside 5 strictly: two of four; inside 1.5: one of four.
    assert near_shares(sheep, dogs, reach=5.0, close=1.5) == (0.5, 0.25)
    assert near_shares(sheep, np.empty((0, 2)), reach=5.0, close=1.5) == (0.0, 0.0)


def test_pressure_sums_the_shares_into_seconds_per_sheep():
    sheep = np.array([[0.0, 0.0], [10.0, 0.0]])
    pressure = Pressure(reach=5.0, close=1.5)
    pressure.add(sheep, np.array([[0.0, 1.0]]))  # flight 0.5, close 0.5
    pressure.add(sheep, np.array([[50.0, 50.0]]))  # flight 0, close 0
    out = pressure.summary(dt=2.0)
    assert out["flight_seconds_per_sheep"] == pytest.approx(1.0)
    assert out["close_seconds_per_sheep"] == pytest.approx(1.0)
    assert out["mean_flight_share"] == pytest.approx(0.25)
    assert out["peak_flight_share"] == pytest.approx(0.5)
