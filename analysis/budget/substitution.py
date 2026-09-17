"""Information substitution curves for RQ5 (Cap I10)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.budget.frontier import extract_frontier


# Ordinal information ladder used by the protocol (higher = richer information).
INFO_LADDER = (
    "bearing_only",
    "noisy_bearing",
    "local_positions",
    "global",
)


def information_level(obs_mode: str) -> int:
    mode = str(obs_mode)
    if mode in INFO_LADDER:
        return INFO_LADDER.index(mode)
    return -1


def substitution_curves(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    info_col: str = "obs_mode",
    sheep_col: str = "n_sheep",
) -> pd.DataFrame:
    """Compute D_min at each information level for each N.

    Supports claims about whether richer information reduces D_min at fixed R.
    """
    if info_col not in df.columns:
        return pd.DataFrame(
            columns=[sheep_col, info_col, "info_level", "d_min", "hard_failure"]
        )

    rows: list[dict[str, Any]] = []
    for (n, info), g in df.groupby([sheep_col, info_col], dropna=False):
        front = extract_frontier(g, theta=theta)
        d_min = None if front.empty else front.iloc[0]["d_min"]
        rows.append(
            {
                sheep_col: int(n),
                info_col: info,
                "info_level": information_level(str(info)),
                "d_min": d_min,
                "hard_failure": d_min is None,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values([sheep_col, "info_level", info_col]).reset_index(drop=True)


def summarize_substitution(curves: pd.DataFrame) -> dict[str, Any]:
    """Summarise whether D_min falls as information level rises."""
    if curves.empty or curves["d_min"].isna().all():
        return {"n_compared": 0, "median_delta_dmin": None, "supports_substitution": False}
    deltas = []
    for n, g in curves.groupby("n_sheep"):
        g = g.dropna(subset=["d_min"]).sort_values("info_level")
        if len(g) < 2:
            continue
        deltas.append(float(g.iloc[-1]["d_min"]) - float(g.iloc[0]["d_min"]))
    if not deltas:
        return {"n_compared": 0, "median_delta_dmin": None, "supports_substitution": False}
    med = float(pd.Series(deltas).median())
    return {
        "n_compared": len(deltas),
        "median_delta_dmin": med,
        "supports_substitution": bool(med < 0),
    }
