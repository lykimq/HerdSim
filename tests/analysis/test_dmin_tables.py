"""Tables of D_min from finished runs, on synthetic folders and frames."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from analysis.dmin import at_arrival
from analysis.dmin_tables import (
    bracket,
    compare,
    dips,
    dmin_text,
    dsat_bracket,
    dsat_text,
    effort_table,
    growth_table,
    layout_against_n,
    layout_by_n,
    parse_group_key,
    run_record,
    slope_range,
)


def groups(rows: list[tuple[str, int, float, float]], factors: str = "") -> pd.DataFrame:
    """(layout, n, d_min, d_min_low) -> a groups table as groups_table makes it."""
    return pd.DataFrame(
        [
            {
                "method": "strombom_multi",
                "layout": lay,
                "factors": factors,
                "n": n,
                "d_min": lo_hi_high,
                "d_min_low": low,
                "d_min_above_grid": False,
                "group_key": f"strombom_multi|{lay}|N={n}",
            }
            for lay, n, lo_hi_high, low in rows
        ]
    )


def test_group_key_with_and_without_a_factor():
    assert parse_group_key("strombom_multi|wide|N=200") == {
        "method": "strombom_multi",
        "layout": "wide",
        "factors": "",
        "n": 200,
    }
    assert parse_group_key("strombom_multi|wide|dog_start_gap=15.0|N=100")["factors"] == (
        "dog_start_gap=15.0"
    )


def test_dmin_text_decided_bracketed_undecided_and_none_on_grid():
    base = {"d_min": 4.0, "d_min_low": 4.0, "d_min_above_grid": False}
    assert dmin_text(pd.Series(base)) == "4"
    # D = 4 is reliable but D = 3 is still open: the true D_min is 3 or 4, not 4.
    assert dmin_text(pd.Series({**base, "d_min_low": 3.0})) == "3-4"
    assert dmin_text(pd.Series({**base, "d_min": np.nan, "d_min_low": 3.0})) == "[3]"
    assert dmin_text(pd.Series({**base, "d_min": np.nan, "d_min_above_grid": True})) == (
        "none on grid"
    )


def test_slope_of_doubling_dmin_is_one_and_brackets_widen_the_range():
    exact = slope_range([(100, 1, 1), (200, 2, 2), (400, 4, 4)])
    assert exact is not None and exact[0] == pytest.approx(1.0) and exact[1] == pytest.approx(1.0)
    wide = slope_range([(100, 1, 2), (200, 2, 2), (400, 3, 4)])
    assert wide is not None and wide[0] < 1.0 <= wide[1] + 1e-9  # the steepest corner is 1
    assert slope_range([(100, 1, 1)]) is None


def test_flat_curves_are_named_and_left_out_sizes_say_why():
    table = groups(
        [
            ("compact", 100, 1.0, 1.0),
            ("compact", 200, 1.0, 1.0),
            ("wide", 100, 1.0, 1.0),
            ("wide", 200, 2.0, 2.0),
            ("wide", 400, np.nan, 3.0),
            ("split", 100, 1.0, 1.0),
            ("split", 200, np.nan, 5.0),
        ]
    )
    table.loc[table["layout"] == "split", "d_min_above_grid"] = table["n"] == 200
    out = growth_table(table).set_index("layout")
    assert out.loc["compact", "note"] == "D_min = 1 throughout"
    assert out.loc["wide", "slope_range"] == "1.00 to 1.00"
    assert "still open on reliability at N = 400" in out.loc["wide", "note"]
    assert out.loc["split", "slope_range"].startswith("0 (flat")
    assert "D_min = 1 where decided" in out.loc["split", "note"]
    assert "no reliable D on the grid at N = 200" in out.loc["split", "note"]


def test_layout_table_has_layouts_as_rows_and_n_as_columns():
    table = groups([("compact", 100, 1.0, 1.0), ("wide", 100, 2.0, 2.0), ("wide", 200, 4.0, 3.0)])
    wide = layout_by_n(table, ("compact", "wide", "split"))
    assert list(wide.index) == ["compact", "wide"]  # a layout without data is not listed
    assert wide.loc["wide", 200] == "3-4" and wide.loc["compact", 200] == "-"


def test_tables_keyed_by_layout_and_n_refuse_several_factor_levels():
    table = pd.concat(
        [
            groups([("wide", 100, 2.0, 2.0)], "gap=15.0"),
            groups([("wide", 100, 3.0, 3.0)], "gap=60.0"),
        ]
    )
    for build in (layout_by_n, growth_table, layout_against_n):
        with pytest.raises(ValueError, match="factor levels"):
            build(table)


def test_layout_and_n_spreads_are_in_doublings():
    table = groups(
        [
            ("compact", 100, 1.0, 1.0),
            ("compact", 200, 1.0, 1.0),
            ("wide", 100, 2.0, 2.0),
            ("wide", 200, 4.0, 4.0),
        ]
    )
    spread = layout_against_n(table)
    assert spread["layout_spread_at_fixed_n"] == pytest.approx((1.0 + 2.0) / 2)
    assert spread["n_spread_at_fixed_layout"] == pytest.approx((0.0 + 1.0) / 2)


def test_compare_puts_base_beside_variant_and_keeps_factor_levels():
    base = groups([("wide", 100, 2.0, 2.0), ("wide", 200, 4.0, 4.0)])
    variant = pd.concat(
        [
            groups([("wide", 100, 3.0, 3.0), ("wide", 200, 4.0, 4.0)], "dog_start_gap=15.0"),
            groups([("wide", 100, 2.0, 2.0), ("wide", 200, np.nan, 4.0)], "dog_start_gap=60.0"),
        ]
    )
    out = compare(base, variant)
    assert out.loc["dog_start_gap=15.0", "wide N=100"] == "2 / 3"
    assert out.loc["dog_start_gap=60.0", "wide N=200"] == "4 / [4]"


def test_dips_list_unreliable_cells_above_dmin_only():
    g = pd.DataFrame({"group_key": ["strombom_multi|wide|N=200"], "d_min": [4.0]})
    cells = pd.DataFrame(
        {
            "group_key": ["strombom_multi|wide|N=200"] * 4,
            "n_shepherds": [2, 4, 6, 8],
            "n_seeds": [60, 60, 60, 60],
            "success_rate": [0.2, 0.95, 0.5, 0.98],
            "reliability": ["unreliable", "reliable", "unreliable", "reliable"],
            "zone": ["too_few", "improving", "unreliable_dip", "recovered"],
        }
    )
    found = dips(cells, g)
    assert found["d"].tolist() == [6] and found["zone"].tolist() == ["unreliable_dip"]


def test_arrival_relabels_success_by_the_chosen_fraction():
    trials = pd.DataFrame(
        {
            "success": [True, False, False],
            "finish_seconds": [100.0, np.nan, np.nan],
            "finish_ticks": [100.0, np.nan, np.nan],
            "time_limit_seconds": [500.0, 500.0, 500.0],
            "dt": [1.0, 1.0, 1.0],
            "seconds_to_99pct_in_goal": [90.0, 300.0, np.nan],
        }
    )
    out = at_arrival(trials, 99)
    assert out["success"].tolist() == [True, True, False]  # the second reached 99 percent
    assert out["finish_seconds"].tolist()[:2] == [90.0, 300.0]


def test_run_record_keeps_the_last_entry_of_each_protocol(tmp_path):
    log = tmp_path / "queue_log.jsonl"
    entries = [
        {"protocol": "a", "trials": 10, "hours": 0.1},
        {"protocol": "b", "trials": 20, "hours": 0.2},
        {"protocol": "a", "trials": 30, "hours": 0.3},
    ]
    log.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
    out = run_record(log).set_index("protocol")
    assert out.loc["a", "trials"] == 30 and out.loc["b", "trials"] == 20
    assert run_record(tmp_path / "missing.jsonl").empty


def test_run_record_reads_current_counts_from_the_folder(tmp_path):
    """A folder topped up outside the queue shows its current trials, not the queue's."""
    log = tmp_path / "queue_log.jsonl"
    log.write_text(json.dumps({"protocol": "a", "trials": 10, "cells": 4, "hours": 0.1}) + "\n")
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "status.json").write_text(json.dumps({"trials_done": 15, "cells": 5}))
    out = run_record(log, tmp_path).set_index("protocol")
    assert out.loc["a", "trials"] == 15 and out.loc["a", "cells"] == 5
    assert out.loc["a", "hours"] == 0.1


def test_bracket_is_none_without_a_decided_dmin():
    assert bracket(pd.Series({"d_min": np.nan, "d_min_low": 2.0})) is None
    assert bracket(pd.Series({"d_min": 4.0, "d_min_low": 3.0})) == (3.0, 4.0)


def curve(**values) -> pd.Series:
    base = {
        "method": "strombom_multi",
        "layout": "wide",
        "factors": "",
        "n": 200,
        "d_min": 2.0,
        "d_min_low": 2.0,
        "d_sat": 3.0,
        "d_max": 24.0,
        "d_crowd": float("nan"),
        "d_sat_undecided": False,
        "still_improving_at_top": False,
    }
    return pd.Series({**base, **values})


def test_dsat_bracket_open_only_upward_and_censored_at_the_grid_top():
    assert dsat_bracket(curve()) == (3.0, 3.0) and dsat_text(curve()) == "3"
    # A larger reliable D is still open against D_sat: the true D_sat is 3 up to D_max.
    assert dsat_bracket(curve(d_sat_undecided=True)) == (3.0, 24.0)
    assert dsat_text(curve(d_sat_undecided=True)) == "3-24"
    top = curve(d_sat=24.0, still_improving_at_top=True)
    assert dsat_bracket(top) is None and dsat_text(top) == "[24]"
    assert dsat_text(curve(d_sat=float("nan"))) == "-"


def test_effort_is_relative_to_the_dsat_cell():
    key = "strombom_multi|wide|N=200"
    cells = pd.DataFrame(
        [
            # D, median finish, median dog ticks (= D x finish), path per dog
            {"n_shepherds": 2, "median_finish": 300.0, "median_path_per_dog": 400.0},
            {"n_shepherds": 4, "median_finish": 200.0, "median_path_per_dog": 300.0},
            {"n_shepherds": 8, "median_finish": 190.0, "median_path_per_dog": 250.0},
        ]
    ).assign(group_key=key, reliability="reliable")
    cells["median_dog_ticks"] = cells["n_shepherds"] * cells["median_finish"]
    table = pd.DataFrame([curve(d_sat=4.0, d_max=8.0)])
    row = effort_table(cells, table).iloc[0]
    assert row["d_double"] == 8 and row["d_top"] == 8
    assert row["time_double"] == round(190 / 200, 2)
    assert row["dog_time_double"] == round(8 * 190 / (4 * 200), 2)
    assert row["path_double"] == round(8 * 250 / (4 * 300), 2)
