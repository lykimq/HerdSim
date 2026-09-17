"""Frontier extraction: D_min, D_overcrowd, D_max, B* (Cap I2)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def reliability_table(
    df: pd.DataFrame,
    *,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Mean success rate per (group, N, D) cell."""
    keys = list(group_cols or []) + [sheep_col, dog_col]
    rates = (
        df.groupby(keys, dropna=False)[success_col]
        .mean()
        .reset_index()
        .rename(columns={success_col: "reliability"})
    )
    return rates


def _ordered_d_values(rates: pd.DataFrame, dog_col: str) -> list[int]:
    return sorted({int(d) for d in rates[dog_col].tolist()})


def _d_min_for_rates(rates: pd.Series, theta: float) -> int | None:
    for d, r in rates.items():
        if float(r) >= theta:
            return int(d)
    return None


def _d_overcrowd_for_rates(
    rates: pd.Series,
    *,
    d_min: int | None,
    theta: float,
) -> int | None:
    """Smallest D > D_min where R stays below theta for >= 2 consecutive grid steps."""
    if d_min is None:
        return None
    ds = list(rates.index)
    below_run: list[int] = []
    for d in ds:
        if int(d) <= d_min:
            continue
        if float(rates[d]) < theta:
            below_run.append(int(d))
            if len(below_run) >= 2:
                return below_run[0]
        else:
            below_run = []
    return None


def _d_max_for_rates(
    rates: pd.Series,
    *,
    d_min: int | None,
    d_overcrowd: int | None,
    theta: float,
) -> int | None:
    if d_min is None:
        return None
    achieving = [int(d) for d, r in rates.items() if float(r) >= theta]
    if not achieving:
        return None
    if d_overcrowd is None:
        return max(achieving)
    below = [d for d in achieving if d < d_overcrowd]
    return max(below) if below else d_min


def extract_frontier(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    effort_col: str = "mean_shepherd_path",
    time_col: str = "first_success_tick",
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Extract D_min, D_overcrowd, D_max, and B* per flock size (and optional groups).

    B* is the (D) achieving R >= theta at minimum median effort; ties by smaller D,
    then faster median time-to-success.
    """
    groups = list(group_cols or [])
    keys = groups + [sheep_col]
    rows: list[dict[str, Any]] = []

    if df.empty:
        return pd.DataFrame(
            columns=groups
            + [
                sheep_col,
                "d_min",
                "d_overcrowd",
                "d_max",
                "b_star_d",
                "b_star_effort",
                "hard_failure",
            ]
        )

    for key_vals, g in df.groupby(keys, dropna=False):
        if not isinstance(key_vals, tuple):
            key_vals = (key_vals,)
        meta = dict(zip(keys, key_vals))
        rates = g.groupby(dog_col)[success_col].mean().sort_index()
        d_min = _d_min_for_rates(rates, theta)
        d_overcrowd = _d_overcrowd_for_rates(rates, d_min=d_min, theta=theta)
        d_max = _d_max_for_rates(
            rates, d_min=d_min, d_overcrowd=d_overcrowd, theta=theta
        )

        b_star_d = None
        b_star_effort = None
        if d_min is not None and effort_col in g.columns:
            candidates = []
            for d, sub in g.groupby(dog_col):
                r = float(sub[success_col].mean())
                if r < theta:
                    continue
                effort = float(sub[effort_col].median())
                t_s = (
                    float(sub[time_col].median())
                    if time_col in sub.columns
                    else float("inf")
                )
                candidates.append((effort, int(d), t_s))
            if candidates:
                candidates.sort(key=lambda x: (x[0], x[1], x[2]))
                b_star_effort, b_star_d, _ = candidates[0]

        row = {
            **meta,
            "d_min": d_min,
            "d_overcrowd": d_overcrowd,
            "d_max": d_max,
            "b_star_d": b_star_d,
            "b_star_effort": b_star_effort,
            "hard_failure": d_min is None,
            "rates": {int(k): float(v) for k, v in rates.items()},
        }
        rows.append(row)
    return pd.DataFrame(rows)


def bootstrap_d_min_ci(
    df: pd.DataFrame,
    *,
    n_sheep: int,
    theta: float = 0.90,
    n_boot: int = 1000,
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    sheep_col: str = "n_sheep",
    seed: int = 2026,
) -> dict[str, Any]:
    """Bootstrap 95% CI on D_min for one flock size."""
    sub = df[df[sheep_col] == n_sheep]
    if sub.empty:
        return {"d_min": None, "ci_low": None, "ci_high": None}
    rng = np.random.default_rng(seed)
    ds = sorted(sub[dog_col].unique())
    # Resample seeds within each D cell.
    estimates: list[int | None] = []
    for _ in range(n_boot):
        parts = []
        for d in ds:
            cell = sub[sub[dog_col] == d]
            if cell.empty:
                continue
            idx = rng.integers(0, len(cell), size=len(cell))
            parts.append(cell.iloc[idx])
        if not parts:
            estimates.append(None)
            continue
        boot = pd.concat(parts, ignore_index=True)
        rates = boot.groupby(dog_col)[success_col].mean().sort_index()
        estimates.append(_d_min_for_rates(rates, theta))
    valid = [e for e in estimates if e is not None]
    point = _d_min_for_rates(
        sub.groupby(dog_col)[success_col].mean().sort_index(), theta
    )
    if not valid:
        return {"d_min": point, "ci_low": None, "ci_high": None}
    return {
        "d_min": point,
        "ci_low": int(np.percentile(valid, 2.5)),
        "ci_high": int(np.percentile(valid, 97.5)),
    }
