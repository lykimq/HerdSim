"""Information substitution curves for RQ5 (Cap I10)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.scaling.frontier import extract_frontier


# Ordinal ladders from the main plan (RQ5). Higher index = richer / farther / more shared.
OBS_LADDER = (
    "bearing_only",
    "local_positions",
    "global",
)

RANGE_MULTIPLIERS = (0.5, 1.0, 1.5, 2.0)

COMM_LADDER = (
    "none",
    "neighbour_broadcast",
    "global_shared",
)


def information_level(obs_mode: str) -> int:
    mode = str(obs_mode)
    if mode in OBS_LADDER:
        return OBS_LADDER.index(mode)
    return -1


def range_level(sensing_range: float, *, base_range: float) -> int:
    """Map an absolute sensing_range to the nearest plan multiplier index."""
    if base_range <= 0:
        return -1
    ratio = float(sensing_range) / float(base_range)
    best_i = min(
        range(len(RANGE_MULTIPLIERS)),
        key=lambda i: abs(RANGE_MULTIPLIERS[i] - ratio),
    )
    return int(best_i)


def communication_level(communication: str) -> int:
    mode = str(communication)
    if mode in COMM_LADDER:
        return COMM_LADDER.index(mode)
    return -1


def substitution_curves(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    info_col: str = "obs_mode",
    sheep_col: str = "n_sheep",
    level_fn=None,
) -> pd.DataFrame:
    """Compute D_min at each information level for each N.

    Supports claims about whether richer information reduces D_min at fixed R.
    ``level_fn(value) -> int`` overrides the default obs_mode ladder ranking.
    """
    if info_col not in df.columns:
        return pd.DataFrame(columns=[sheep_col, info_col, "info_level", "d_min", "hard_failure"])

    rank = level_fn or (lambda v: information_level(str(v)))
    rows: list[dict[str, Any]] = []
    for (n, info), g in df.groupby([sheep_col, info_col], dropna=False):
        front = extract_frontier(g, theta=theta)
        d_min = None if front.empty else front.iloc[0]["d_min"]
        rows.append(
            {
                sheep_col: int(n),
                info_col: info,
                "info_level": int(rank(info)),
                "d_min": d_min,
                "hard_failure": d_min is None,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values([sheep_col, "info_level", info_col]).reset_index(drop=True)


def substitution_curves_range(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    range_col: str = "sensing_range",
    base_range: float | None = None,
    sheep_col: str = "n_sheep",
) -> pd.DataFrame:
    """D_min vs sensing-range ladder (multiples of the method r_s)."""
    if base_range is None or float(base_range) <= 0:
        raise ValueError("base_range must be the method sensing radius (r_s)")
    return substitution_curves(
        df,
        theta=theta,
        info_col=range_col,
        sheep_col=sheep_col,
        level_fn=lambda v: range_level(float(v), base_range=base_range),
    )


def substitution_curves_communication(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    comm_col: str = "communication",
    sheep_col: str = "n_sheep",
) -> pd.DataFrame:
    """D_min vs communication ladder."""
    return substitution_curves(
        df,
        theta=theta,
        info_col=comm_col,
        sheep_col=sheep_col,
        level_fn=lambda v: communication_level(str(v)),
    )


def summarize_substitution(curves: pd.DataFrame) -> dict[str, Any]:
    """Summarise whether D_min falls as information level rises (first/second step)."""
    if curves.empty or curves["d_min"].isna().all():
        return {
            "n_compared": 0,
            "median_delta_dmin": None,
            "median_first_step_delta": None,
            "median_second_step_delta": None,
            "supports_substitution": False,
            "supports_diminishing_returns": False,
        }
    deltas = []
    first_steps = []
    second_steps = []
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
