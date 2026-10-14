"""Information substitution ladders for RQ5 (Cap I10 / Package E).

Builds D_min vs observation mode, sensing range, or communication level on a
fixed N/D grid. Summaries support claims C5a/C5b (does one ladder step lower
D_min; does the next step save fewer dogs). Works on trial/frontier tables from
Phase 5 protocols; does not launch campaigns itself.
"""

from __future__ import annotations

from typing import Any, cast

import pandas as pd

from analysis.coerce import as_float, as_int
from analysis.frontier import extract_frontier

# Ordinal ladders from the main plan (RQ5). Higher index = richer / farther / more shared.
LADDERS: dict[str, tuple[str, ...]] = {
    "obs_mode": ("bearing_only", "local_positions", "global"),
    "communication": ("none", "neighbour_broadcast", "global_shared"),
}

# Sensing-range ladder: multiples of the method sensing radius r_s.
RANGE_MULTIPLIERS = (0.5, 1.0, 1.5, 2.0)


def range_level(sensing_range: float, *, base_range: float) -> int:
    """Map an absolute sensing_range to the nearest plan multiplier index."""
    ratio = float(sensing_range) / float(base_range)
    return min(range(len(RANGE_MULTIPLIERS)), key=lambda i: abs(RANGE_MULTIPLIERS[i] - ratio))


def info_level(factor: str, value: object, *, base_range: float | None = None) -> int:
    """Ladder index of one factor value; -1 when the value is not on the ladder."""
    if factor == "sensing_range":
        assert base_range is not None
        return range_level(as_float(value), base_range=base_range)
    ladder = LADDERS[factor]
    return ladder.index(str(value)) if str(value) in ladder else -1


def substitution_curves(
    df: pd.DataFrame,
    *,
    factor: str = "obs_mode",
    theta: float,
    base_range: float | None = None,
    sheep_col: str = "n_sheep",
) -> pd.DataFrame:
    """Compute D_min at each information level for each N.

    ``factor`` is the ladder column: ``obs_mode``, ``communication``, or
    ``sensing_range`` (then ``base_range`` must be the method sensing radius r_s).
    Supports claims about whether richer information reduces D_min at fixed R.
    """
    if factor == "sensing_range" and (base_range is None or float(base_range) <= 0):
        raise ValueError("base_range must be the method sensing radius (r_s)")
    if factor not in df.columns:
        return pd.DataFrame(columns=[sheep_col, factor, "info_level", "d_min", "hard_failure"])

    rows: list[dict[str, Any]] = []
    for key_vals, g in df.groupby([sheep_col, factor], dropna=False):
        n_raw, info = cast(tuple[Any, Any], key_vals)
        level = info_level(factor, info, base_range=base_range)
        if level < 0:
            # Unknown ladder values must not sort before richer levels.
            continue
        front = extract_frontier(g, theta=theta)
        d_min = None if front.empty else front.iloc[0]["d_min"]
        rows.append(
            {
                sheep_col: as_int(n_raw),
                factor: info,
                "info_level": level,
                "d_min": d_min,
                "hard_failure": d_min is None,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values([sheep_col, "info_level", factor]).reset_index(drop=True)


def summarize_substitution(curves: pd.DataFrame) -> dict[str, Any]:
    """Summarise whether D_min falls as information level rises (first/second step)."""
    deltas = []
    first_steps = []
    second_steps = []
    if not curves.empty:
        for _, g in curves.groupby("n_sheep"):
            g = g.dropna(subset=["d_min"]).sort_values("info_level")
            if len(g) < 2:
                continue
            deltas.append(float(g.iloc[-1]["d_min"]) - float(g.iloc[0]["d_min"]))
            first_steps.append(float(g.iloc[1]["d_min"]) - float(g.iloc[0]["d_min"]))
            if len(g) >= 3:
                second_steps.append(float(g.iloc[2]["d_min"]) - float(g.iloc[1]["d_min"]))
    if not deltas:
        return {
            "n_compared": 0,
            "median_delta_dmin": None,
            "median_first_step_delta": None,
            "median_second_step_delta": None,
            "supports_substitution": False,
            "supports_diminishing_returns": False,
        }
    med = float(pd.Series(deltas).median())
    med_first = float(pd.Series(first_steps).median()) if first_steps else None
    med_second = float(pd.Series(second_steps).median()) if second_steps else None
    diminishing = bool(
        med_first is not None
        and med_second is not None
        and abs(med_second) <= abs(med_first)
        and med_first < 0
    )
    return {
        "n_compared": len(deltas),
        "median_delta_dmin": med,
        "median_first_step_delta": med_first,
        "median_second_step_delta": med_second,
        "supports_substitution": bool(med < 0),
        "supports_diminishing_returns": diminishing,
    }
