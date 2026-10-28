"""The overview table feeds docs/report/summary_results.md, so a misplaced entry would put a
team size under the wrong flock size or rule without any error."""

import pandas as pd

from analysis.dmin_tables import overview, split_group_key


def _curve(key: str, d_min: float, d_max: float, at_top: bool) -> dict[str, object]:
    return {
        "group_key": key,
        "d_min": d_min,
        "d_min_low": d_min,
        "d_min_above_grid": False,
        "d_max": d_max,
        "d_max_at_grid_top": at_top,
        "d_overcrowd": float("nan"),
    }


def test_overview_puts_each_value_under_its_n_and_splits_a_swept_share():
    # Stored order is lexical (N=100 before N=25), and the share is a factor.
    groups = split_group_key(
        pd.DataFrame(
            [
                _curve("m|wide|goal_radius_multiple=2.5|success_fraction=0.9|N=100", 3, 24, True),
                _curve("m|wide|goal_radius_multiple=2.5|success_fraction=0.9|N=25", 1, 4, False),
                _curve("m|wide|goal_radius_multiple=2.5|success_fraction=0.99|N=25", 2, 24, True),
            ]
        )
    )

    rows = overview(groups, 0.99, ("wide",)).set_index("share")

    assert list(rows.columns) == ["layout", "variant", "N=25", "N=100"]
    assert rows.loc[0.9, "N=25"] == "1 (max 4)"
    assert rows.loc[0.9, "N=100"] == "3"
    assert rows.loc[0.99, "N=25"] == "2"
    assert rows.loc[0.99, "N=100"] == ""
    assert set(rows["variant"]) == {"goal 2.5 R_f"}
