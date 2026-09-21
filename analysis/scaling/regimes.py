"""Herdability regime labelling for (N, D) cells (Cap I3)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.scaling.frontier import extract_frontier, reliability_table


REGIME_UNDER = "under_budget_failure"
REGIME_EFFICIENT = "efficient_operation"
REGIME_WASTEFUL = "wasteful_overspend"
REGIME_OVERCROWD = "overcrowding_collapse"
REGIME_HARD = "hard_failure"


def label_regimes(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    wasteful_effort_tol: float = 0.20,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    effort_col: str = "mean_shepherd_path",
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Label each (group, N, D) cell with a herdability regime.

    Wasteful overspend: R >= theta and median effort >= (1 + tol) * efficient effort,
    where efficient effort is median effort at D_min (or B* when available).
    """
    groups = list(group_cols or [])
    rates = reliability_table(
        df,
        sheep_col=sheep_col,
        dog_col=dog_col,
        success_col=success_col,
        group_cols=groups,
    )
    frontier = extract_frontier(
        df,
        theta=theta,
        sheep_col=sheep_col,
        dog_col=dog_col,
        success_col=success_col,
        effort_col=effort_col,
        group_cols=groups,
    )

    # Effort by cell.
    effort_keys = groups + [sheep_col, dog_col]
    if effort_col in df.columns:
        efforts = (
            df.groupby(effort_keys, dropna=False)[effort_col]
            .median()
            .reset_index()
            .rename(columns={effort_col: "median_effort"})
        )
        rates = rates.merge(efforts, on=effort_keys, how="left")
    else:
        rates["median_effort"] = float("nan")

    front_keys = groups + [sheep_col]
    front_map = frontier.set_index(front_keys)

    rows: list[dict[str, Any]] = []
    for _, cell in rates.iterrows():
        key = tuple(cell[k] for k in front_keys)
        if len(front_keys) == 1:
            key = key[0]
        try:
            fr = front_map.loc[key]
            if isinstance(fr, pd.DataFrame):
                fr = fr.iloc[0]
        except KeyError:
            fr = None

        r = float(cell["reliability"])
        d = int(cell[dog_col])
        d_min = None if fr is None else fr.get("d_min")
        d_overcrowd = None if fr is None else fr.get("d_overcrowd")
        hard = True if fr is None else bool(fr.get("hard_failure"))
        efficient_effort = None
        if fr is not None and fr.get("b_star_effort") is not None:
            efficient_effort = float(fr["b_star_effort"])
        elif (
            fr is not None
            and d_min is not None
            and effort_col in df.columns
        ):
            mask = df[sheep_col] == cell[sheep_col]
            for gcol in groups:
                mask = mask & (df[gcol] == cell[gcol])
            mask = mask & (df[dog_col] == d_min)
            if mask.any():
                efficient_effort = float(df.loc[mask, effort_col].median())

        if hard or d_min is None:
            regime = REGIME_HARD if r < theta else REGIME_EFFICIENT
        elif r < theta:
            if d_overcrowd is not None and d >= int(d_overcrowd):
                regime = REGIME_OVERCROWD
            else:
                regime = REGIME_UNDER
        else:
            # Reliable cell.
            if d_overcrowd is not None and d >= int(d_overcrowd):
                # Still >= theta but past overcrowding onset: treat as wasteful
                # if effort is high, else efficient edge.
                regime = REGIME_EFFICIENT
            elif (
                efficient_effort is not None
                and cell["median_effort"] == cell["median_effort"]
                and float(cell["median_effort"])
                >= efficient_effort * (1.0 + wasteful_effort_tol)
            ):
                regime = REGIME_WASTEFUL
            elif d_min is not None and d <= int(d_min) + 1:
                regime = REGIME_EFFICIENT
            elif (
                efficient_effort is not None
                and cell["median_effort"] == cell["median_effort"]
                and float(cell["median_effort"])
                >= efficient_effort * (1.0 + wasteful_effort_tol)
            ):
                regime = REGIME_WASTEFUL
            else:
                # Reliable above D_min without large effort inflation.
                regime = REGIME_EFFICIENT

        # Overcrowding collapse overrides when R dropped.
        if (
            d_overcrowd is not None
            and d >= int(d_overcrowd)
            and r < theta
        ):
            regime = REGIME_OVERCROWD

        row = {k: cell[k] for k in rates.columns}
        row["regime"] = regime
        row["d_min"] = d_min
        row["d_overcrowd"] = d_overcrowd
        rows.append(row)
    return pd.DataFrame(rows)
