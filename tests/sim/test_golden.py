"""Regression: short real trials must reproduce frozen outcomes, and a seed must replay exactly.

Any change to the sheep or dog dynamics, the task setup, the config build or the metrics
shows up here. Update the values only on an intended behaviour change, in the same change,
with a note why.

The dynamics are chaotic, so the last floating-point bits (which differ across CPUs and
NumPy builds) grow over a few hundred ticks. Values are whole-trial summaries compared with
a tolerance; end-point positions are too chaotic to pin. Bit-exact replay on one machine is
the second test.
"""

from __future__ import annotations

import pandas as pd
import pytest

from records.trial_row import build_row
from sim.core.simulation_runner import run_trial
from tests.helpers import config_for

REL_TOL = 0.10

# name: (cell, success, total_ticks, mean_cohesion, shepherd_path, mean_fragmentation)
GOLDEN = {
    "multi": (
        dict(method="strombom_multi", n=20, d=3, ticks=400),
        True,
        128,
        3.495701412910934,
        373.5,
        0.9895348837209302,
    ),
    "multi_wide": (
        dict(method="strombom_multi", n=30, d=2, ticks=400, layout="wide"),
        True,
        137,
        4.282006953974045,
        324.0,
        0.9739130434782609,
    ),
    "fat": (
        dict(method="fat", n=20, d=2, ticks=400),
        True,
        132,
        3.4166937858792776,
        273.0,
        0.998872180451128,
    ),
    "kubo": (
        dict(method="kubo", n=20, d=2, ticks=3000),
        True,
        1472,
        4.522490845171206,
        438.5045696461979,
        1.0,
    ),
}


def _row(cell: dict) -> dict:
    cell = dict(cell)
    method, ticks = cell.pop("method"), cell.pop("ticks")
    config = config_for(method, ticks=ticks, flock_radius=7.0, **cell)
    return build_row({}, run_trial(config, 2026), config)


@pytest.mark.parametrize("name", GOLDEN)
def test_trial_matches_golden(name):
    cell, success, ticks, cohesion, path, fragmentation = GOLDEN[name]
    row = _row(cell)
    assert row["success"] == success
    assert row["total_ticks"] == pytest.approx(ticks, rel=0.05)
    assert row["mean_cohesion"] == pytest.approx(cohesion, rel=REL_TOL)
    assert row["shepherd_path"] == pytest.approx(path, rel=REL_TOL)
    assert row["mean_fragmentation"] == pytest.approx(fragmentation, rel=REL_TOL)


def test_same_seed_replays_exactly():
    cell = GOLDEN["multi_wide"][0]
    a, b = _row(cell), _row(cell)
    assert pd.Series(a).equals(pd.Series(b))  # equals treats NaN as equal
