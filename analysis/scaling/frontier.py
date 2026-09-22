"""Frontier extraction: D_min, D_overcrowd, D_max, B*, claim windows, bootstrap (Cap I2)."""

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


def select_claim_windows(
    df: pd.DataFrame,
    *,
    theta: float = 0.90,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    success_col: str = "success",
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Claim-reseed D values from a scout reliability map.

    Per (group, N): scout D_min and its grid neighbors; if two consecutive D
    after that candidate are below theta, those two plus the last D still at
    or above theta. If no D meets theta, the two largest D.
    """
    groups = list(group_cols or [])
    rates = reliability_table(
        df,
        sheep_col=sheep_col,
        dog_col=dog_col,
        success_col=success_col,
        group_cols=groups,
    )
    columns = groups + [sheep_col, dog_col, "reliability", "role"]
    if rates.empty:
        return pd.DataFrame(columns=columns)

    keys = groups + [sheep_col]
    rows: list[dict[str, Any]] = []
    for key_vals, g in rates.groupby(keys, dropna=False):
        if not isinstance(key_vals, tuple):
            key_vals = (key_vals,)
        meta = dict(zip(keys, key_vals))
        ordered = g.sort_values(dog_col)
        ds = [int(v) for v in ordered[dog_col].tolist()]
        rel = {int(row[dog_col]): float(row["reliability"]) for _, row in ordered.iterrows()}
        d_min = _d_min_for_rates(pd.Series(rel).sort_index(), theta)
        chosen: dict[int, str] = {}
        if d_min is None:
            for d in ds[-2:]:
                chosen[d] = "hard_failure_top"
        else:
            idx = ds.index(int(d_min))
            for j in (idx - 1, idx, idx + 1):
                if 0 <= j < len(ds):
                    chosen[ds[j]] = "reliability"
            d_over = None
            for i, d in enumerate(ds):
                if d <= int(d_min) or i + 1 >= len(ds):
                    continue
                nxt = ds[i + 1]
                if rel[d] < theta and rel[nxt] < theta:
                    d_over = d
                    break
            if d_over is not None:
                i = ds.index(d_over)
                for d in (d_over, ds[i + 1]):
                    chosen[d] = "overcrowd" if d not in chosen else f"{chosen[d]}_and_overcrowd"
                reliable = [d for d in ds if d < d_over and rel[d] >= theta]
                if reliable:
                    last = reliable[-1]
                    if last in chosen:
                        chosen[last] = f"{chosen[last]}_and_last_reliable"
                    else:
                        chosen[last] = "last_reliable"
        for d, role in chosen.items():
            rows.append({**meta, dog_col: d, "reliability": rel[d], "role": role})
    return pd.DataFrame(rows)


def merge_scout_and_claim(
    scout: pd.DataFrame,
    claim: pd.DataFrame,
    *,
    key_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Keep claim rows on reseeded cells and scout rows everywhere else."""
    if claim.empty:
        return scout.copy()
    if scout.empty:
        return claim.copy()
    keys = key_cols or [
        c
        for c in ("method", "initial_layout", "n_sheep", "n_shepherds")
        if c in scout.columns and c in claim.columns
    ]
    claim_keys = claim[keys].drop_duplicates()
    tagged = scout.merge(claim_keys, on=keys, how="left", indicator=True)
    kept = tagged[tagged["_merge"] == "left_only"].drop(columns="_merge")
    return pd.concat([kept, claim], ignore_index=True)


def _rank_endpoint(samples: np.ndarray, q: float) -> float:
    """Nearest-rank percentile. Values may include +inf."""
    ordered = np.sort(np.asarray(samples, dtype=float))
    n = len(ordered)
    if n == 0:
        return float("nan")
    idx = int(np.ceil(q * n) - 1)
    idx = min(max(idx, 0), n - 1)
    return float(ordered[idx])


def _grid_or_above(value: float) -> tuple[int | None, bool]:
    if not np.isfinite(value):
        return None, True
    return int(value), False


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

    1,000 resamples. A resample with no D_min stays in the sample as above the
    largest tested D. Endpoints are nearest-rank grid values.
    """
    groups = list(group_cols or [])
    keys = groups + [sheep_col]
    if df.empty or success_col not in df.columns:
        return pd.DataFrame(
            columns=keys + ["d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref"]
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
            seed_success = sub.groupby(seed_col)[success_col].max().astype(float).to_numpy()
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
            boot_dmins.append(float(dmin) if dmin is not None else float("inf"))

        samples = np.asarray(boot_dmins, dtype=float)
        low_raw = _rank_endpoint(samples, 0.025)
        high_raw = _rank_endpoint(samples, 0.975)
        low, low_above = _grid_or_above(low_raw)
        high, high_above = _grid_or_above(high_raw)
        rows.append(
            {
                **meta,
                "d_min": point,
                "d_min_ci_low": low,
                "d_min_ci_high": high,
                "d_min_ci_low_above_grid": low_above,
                "d_min_ci_high_above_grid": high_above,
                "n_boot": int(n_boot),
                "n_seeds_ref": int(n_seeds_ref),
                "n_boot_defined": int(np.isfinite(samples).sum()),
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
    effort_col: str = "shepherd_path",
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
        d_max = _d_max_for_rates(rates, d_min=d_min, d_overcrowd=d_overcrowd, theta=theta)

        b_star_d = None
        b_star_t = None
        b_star_effort = None
        if d_min is not None and effort_col in g.columns:
            candidates = []
            # Prefer (D, T) cells when time_limit varies; else one T per D.
            if time_limit_col in g.columns:
                cell_iter = g.groupby([dog_col, time_limit_col])
            else:
                cell_iter = (((d, None), sub) for d, sub in g.groupby(dog_col))
            for key, sub in cell_iter:
                if isinstance(key, tuple):
                    d, t_lim = key
                else:
                    d, t_lim = key, None
                r = float(sub[success_col].mean())
                if r < theta:
                    continue
                effort = float(sub[effort_col].median())
                t_s = float(sub[time_col].median()) if time_col in sub.columns else float("inf")
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
