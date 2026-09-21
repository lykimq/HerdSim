"""Frontier extraction: D_min, D_overcrowd, D_max, B*, boundary cells, bootstrap (Cap I2)."""

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


def select_boundary_cells(
    df: pd.DataFrame,
    *,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    group_cols: list[str] | None = None,
    low_r: float = 0.80,
    high_r: float = 0.95,
) -> pd.DataFrame:
    """Select claim-reseed boundary D values from a scout reliability map.

    Per (group, N), in ordered D-grid order: first D with R > low_r and first
    with R < high_r (plan D_min procedure step 2). Returns unique (group, N, D)
    rows; empty when the scout surface has no such crossings.
    """
    groups = list(group_cols or [])
    rates = reliability_table(
        df,
        sheep_col=sheep_col,
        dog_col=dog_col,
        success_col=success_col,
        group_cols=groups,
    )
    if rates.empty:
        return pd.DataFrame(columns=groups + [sheep_col, dog_col, "reliability", "role"])

    keys = groups + [sheep_col]
    rows: list[dict[str, Any]] = []
    for key_vals, g in rates.groupby(keys, dropna=False):
        if not isinstance(key_vals, tuple):
            key_vals = (key_vals,)
        meta = dict(zip(keys, key_vals))
        ordered = g.sort_values(dog_col)
        d_enter = None
        d_exit = None
        for _, cell in ordered.iterrows():
            r = float(cell["reliability"])
            d = int(cell[dog_col])
            if d_enter is None and r > low_r:
                d_enter = d
            if d_exit is None and r < high_r:
                d_exit = d
        chosen: dict[int, str] = {}
        if d_enter is not None:
            chosen[d_enter] = "enter_above_low_r"
        if d_exit is not None:
            chosen[d_exit] = (
                "exit_below_high_r"
                if d_exit not in chosen
                else "enter_and_exit"
            )
        for d, role in chosen.items():
            sub = ordered[ordered[dog_col] == d]
            r = float(sub.iloc[0]["reliability"]) if not sub.empty else float("nan")
            rows.append({**meta, dog_col: d, "reliability": r, "role": role})
    return pd.DataFrame(rows)


def bootstrap_d_min_ci(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    n_boot: int = 1000,
    seed: int = 2026,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    seed_col: str = "seed",
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Bootstrap 95% CI on D_min by resampling seeds within each (N, D) cell.

    Plan step 5: 1,000 resamples of the (claim-grade) seeds. Requires a seed
    column so each (group, N, D) cell can be resampled with replacement.
    """
    groups = list(group_cols or [])
    keys = groups + [sheep_col]
    if df.empty or success_col not in df.columns:
        return pd.DataFrame(
            columns=keys
            + ["d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref"]
        )

    rng = np.random.default_rng(seed)
    rows: list[dict[str, Any]] = []
    for key_vals, g in df.groupby(keys, dropna=False):
        if not isinstance(key_vals, tuple):
            key_vals = (key_vals,)
        meta = dict(zip(keys, key_vals))
        point = _d_min_for_rates(g.groupby(dog_col)[success_col].mean().sort_index(), theta)

        if seed_col not in g.columns:
            rows.append(
                {
                    **meta,
                    "d_min": point,
                    "d_min_ci_low": None,
                    "d_min_ci_high": None,
                    "n_boot": 0,
                    "n_seeds_ref": None,
                    "note": "missing seed column",
                }
            )
            continue

        # Build per-D success vectors aligned on the union of seeds.
        by_d: dict[int, np.ndarray] = {}
        n_seeds_ref = 0
        for d, sub in g.groupby(dog_col):
            # One success flag per seed (last wins if duplicates).
            seed_success = (
                sub.groupby(seed_col)[success_col].max().astype(float).to_numpy()
            )
            by_d[int(d)] = seed_success
            n_seeds_ref = max(n_seeds_ref, len(seed_success))

        if n_seeds_ref < 1 or not by_d:
            rows.append(
                {
                    **meta,
                    "d_min": point,
                    "d_min_ci_low": None,
                    "d_min_ci_high": None,
                    "n_boot": 0,
                    "n_seeds_ref": int(n_seeds_ref),
                }
            )
            continue

        boot_dmins: list[float] = []
        ordered_d = sorted(by_d.keys())
        for _ in range(int(n_boot)):
            rates = {}
            for d in ordered_d:
                vec = by_d[d]
                if len(vec) == 0:
                    rates[d] = 0.0
                    continue
                idx = rng.integers(0, len(vec), size=len(vec))
                rates[d] = float(np.mean(vec[idx]))
            dmin = _d_min_for_rates(pd.Series(rates).sort_index(), theta)
            # Use +inf so percentile stays defined when some resamples have no D_min.
            boot_dmins.append(float(dmin) if dmin is not None else float("inf"))

        finite = [x for x in boot_dmins if np.isfinite(x)]
        if not finite:
            low = high = None
        else:
            low = float(np.percentile(finite, 2.5))
            high = float(np.percentile(finite, 97.5))
        rows.append(
            {
                **meta,
                "d_min": point,
                "d_min_ci_low": low,
                "d_min_ci_high": high,
                "n_boot": int(n_boot),
                "n_seeds_ref": int(n_seeds_ref),
                "n_boot_defined": len(finite),
            }
        )
    return pd.DataFrame(rows)


def extract_frontier(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    effort_col: str = "mean_shepherd_path",
    time_col: str = "first_success_tick",
    time_limit_col: str = "time_limit",
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Extract D_min, D_overcrowd, D_max, and B* per flock size (and optional groups).

    B* is the (D, T) achieving R >= theta at minimum median effort; ties by smaller D,
    then faster median time-to-success. When time_limit is constant, B* still records
    that T as b_star_t.
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
                "b_star_t",
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
        b_star_t = None
        b_star_effort = None
        if d_min is not None and effort_col in g.columns:
            candidates = []
            # Prefer (D, T) cells when time_limit varies; else one T per D.
            if time_limit_col in g.columns:
                cell_iter = g.groupby([dog_col, time_limit_col])
            else:
                cell_iter = (( (d, None), sub) for d, sub in g.groupby(dog_col))
            for key, sub in cell_iter:
                if isinstance(key, tuple):
                    d, t_lim = key
                else:
                    d, t_lim = key, None
                r = float(sub[success_col].mean())
                if r < theta:
                    continue
                effort = float(sub[effort_col].median())
                t_s = (
                    float(sub[time_col].median())
                    if time_col in sub.columns
                    else float("inf")
                )
                t_val = (
                    float(t_lim)
                    if t_lim is not None
                    else (
                        float(sub[time_limit_col].median())
                        if time_limit_col in sub.columns
                        else float("nan")
                    )
                )
                candidates.append((effort, int(d), t_s, t_val))
            if candidates:
                candidates.sort(key=lambda x: (x[0], x[1], x[2]))
                b_star_effort, b_star_d, _, b_star_t = candidates[0]
                if b_star_t != b_star_t:  # NaN
                    b_star_t = None

        row = {
            **meta,
            "d_min": d_min,
            "d_overcrowd": d_overcrowd,
            "d_max": d_max,
            "b_star_d": b_star_d,
            "b_star_t": b_star_t,
            "b_star_effort": b_star_effort,
            "hard_failure": d_min is None,
            "rates": {int(k): float(v) for k, v in rates.items()},
        }
        rows.append(row)
    return pd.DataFrame(rows)
