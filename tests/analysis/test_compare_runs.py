"""Paired comparison of two folders and the non-monotone curve finder: a swapped side or a
missed unreliable D would flip a conclusion silently."""

from __future__ import annotations

import pandas as pd
import pytest

from analysis import keys
from analysis.compare_runs import nonmonotone_curves, paired_outcomes
from analysis.frontier import RELIABLE, UNRELIABLE

GROUP = keys.group_key("strombom_multi", "wide", 200)


def trials(success: list[bool]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "group_key": GROUP,
            "n_shepherds": 2,
            "seed_index": range(len(success)),
            "success": success,
        }
    )


def test_paired_outcomes_count_each_side_and_run_the_sign_test() -> None:
    a = trials([True, True, True, False])
    b = trials([False, False, True, False])
    pooled = paired_outcomes(a, b).iloc[-1]
    assert (pooled["pairs"], pooled["finish only in a"], pooled["finish only in b"]) == (4, 2, 0)
    assert float(pooled["p"]) == pytest.approx(0.5)  # two of two one way: 2 * 0.5**2
    swapped = paired_outcomes(b, a).iloc[-1]
    assert (swapped["finish only in a"], swapped["finish only in b"]) == (0, 2)


def test_nonmonotone_curve_gives_the_unreliable_d_and_d_min_stable() -> None:
    status = {1: UNRELIABLE, 2: RELIABLE, 3: UNRELIABLE, 4: RELIABLE}
    cells = pd.DataFrame(
        {"group_key": GROUP, "n_shepherds": list(status), "reliability": list(status.values())}
    )
    groups = pd.DataFrame({"group_key": [GROUP], "d_min_low": [2]})
    row = nonmonotone_curves(cells, groups).iloc[0]
    assert (row["unreliable above"], row["D_min_stable"]) == ("3", 4)
