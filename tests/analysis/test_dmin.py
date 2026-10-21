"""Deadline relabelling and the D_min table, on synthetic trials."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from analysis.dmin import at_deadline, dmin_table
from analysis.frontier import Rules
from tests.helpers import BASE_PROTOCOL

RULES = Rules.from_settings(BASE_PROTOCOL.settings)
SPEED = {"strombom_multi": 1.0}
DRIVE = 100.0
LIMIT_MULTIPLE = 10.0


def trials(finish_by_d: dict[int, float], seeds: int = 60) -> pd.DataFrame:
    """Every seed of D finishes at the same time (a time over the limit means a failure)."""
    rows = []
    for d, finish in finish_by_d.items():
        ok = finish <= LIMIT_MULTIPLE * DRIVE
        for i in range(seeds):
            t = finish + 0.01 * i if ok else np.nan
            rows.append(
                {
                    "group_key": "g",
                    "method": "strombom_multi",
                    "n_shepherds": d,
                    "seed_index": i,
                    "success": ok,
                    "finish_ticks": t,
                    "finish_seconds": t,
                    "drive_distance": DRIVE,
                    "time_limit_seconds": LIMIT_MULTIPLE * DRIVE,
                    "dog_ticks": d * (finish if ok else LIMIT_MULTIPLE * DRIVE),
                    "path_per_dog": 50.0,
                }
            )
    return pd.DataFrame(rows)


CURVE = {1: 900.0, 2: 600.0, 4: 300.0, 8: 290.0}


def test_a_tighter_deadline_turns_late_successes_into_failures():
    out = at_deadline(trials(CURVE), 5.0, SPEED)  # 500 s
    by_d = out.groupby("n_shepherds")["success"].mean()
    assert by_d.to_dict() == {1: 0.0, 2: 0.0, 4: 1.0, 8: 1.0}
    assert out.loc[~out["success"], ["finish_ticks", "finish_seconds"]].isna().all().all()


def test_a_looser_deadline_than_the_run_is_refused():
    with pytest.raises(ValueError, match="looser"):
        at_deadline(trials(CURVE), 12.0, SPEED)


def test_dmin_falls_as_the_deadline_loosens():
    table = dmin_table(trials(CURVE), RULES, [3.5, 5.0, 7.0, 10.0], SPEED)
    d_min = dict(zip(table["deadline_multiple"], table["d_min"]))
    assert d_min[5.0] == 4 and d_min[7.0] == 2 and d_min[10.0] == 1
    assert pd.isna(d_min[2.0]) if 2.0 in d_min else True
    values = [d_min[m] for m in (5.0, 7.0, 10.0)]
    assert values == sorted(values, reverse=True)


def test_no_reliable_d_gives_a_missing_dmin():
    table = dmin_table(trials(CURVE), RULES, [2.0], SPEED)
    assert pd.isna(table["d_min"].iloc[0])
