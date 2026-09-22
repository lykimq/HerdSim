"""Mechanism hypothesis tests for overcrowding (Cap I8)."""

from __future__ import annotations

from typing import Any, cast

import numpy as np
import pandas as pd
from scipy import stats


def _holm_adjust(p_values: list[float | None]) -> list[float | None]:
    """Holm-Bonferroni adjusted p-values (None stays None)."""
    indexed = [(i, p) for i, p in enumerate(p_values) if p is not None]
    out: list[float | None] = [None] * len(p_values)
    if not indexed:
        return out
    indexed.sort(key=lambda ip: ip[1])
    m = len(indexed)
    adjusted: list[tuple[int, float]] = []
    running = 0.0
    for rank, (i, p) in enumerate(indexed):
        cand = (m - rank) * float(p)
        running = max(running, cand)
        adjusted.append((i, min(1.0, running)))
    for i, p_adj in adjusted:
        out[i] = float(p_adj)
    return out


def evaluate_overcrowding_mechanisms(
    trials: pd.DataFrame,
    regimes: pd.DataFrame,
    *,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    i_dir_col: str = "mean_i_dir",
    coverage_col: str = "mean_coverage",
    fragmentation_col: str = "mean_fragmentation",
    effort_col: str = "shepherd_path",
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Compare mechanism metrics between efficient and overcrowding cells.

    One median per (N, D) cell. Rank tests stay inside each N. Holm correction
    is across the rank-test hypotheses at that N. Fragmentation is the largest
    component fraction, so induced fragmentation is a lower value in
    overcrowding cells. Coverage saturation is descriptive and is not a
    near-zero curve.
    """
    key = [sheep_col, dog_col]
    reg = regimes.loc[:, key + ["regime"]].drop_duplicates(subset=key)
    merged = trials.merge(reg, on=key, how="left")

    metric_cols = [
        c for c in (i_dir_col, fragmentation_col, coverage_col, effort_col) if c in merged.columns
    ]
    if not metric_cols:
        return {"by_n": [], "overall": {}, "correction": "holm"}

    cells = merged.groupby(key + ["regime"], dropna=False)[metric_cols].median().reset_index()

    hyp_specs = (
        (i_dir_col, "interference", "greater"),
        (fragmentation_col, "induced_fragmentation", "less"),
        (effort_col, "redundant_effort", "greater"),
    )
    by_n: list[dict[str, Any]] = []
    overall: dict[str, Any] = {}

    for n_key, g in cells.groupby(sheep_col):
        n = int(cast(Any, n_key))
        g = g.copy()
        eff = g.loc[g["regime"] == "efficient_operation"].copy()
        ovr = g.loc[g["regime"] == "overcrowding_collapse"].copy()
        raw_p: list[float | None] = []
        payloads: list[dict[str, Any]] = []
        for metric, hyp, alternative in hyp_specs:
            payload: dict[str, Any] = {
                "n_sheep": n,
                "hypothesis": hyp,
                "metric": metric,
                "available": metric in g.columns,
                "n_efficient_cells": int(len(eff)),
                "n_overcrowd_cells": int(len(ovr)),
            }
            if metric not in g.columns or len(eff) < 2 or len(ovr) < 2:
                payload.update(
                    {
                        "p_value": None,
                        "p_value_holm": None,
                        "supported": False,
                        "note": "insufficient cells",
                    }
                )
                raw_p.append(None)
            else:
                a = pd.Series(ovr.loc[:, metric]).dropna()
                b = pd.Series(eff.loc[:, metric]).dropna()
                if len(a) < 2 or len(b) < 2:
                    payload.update(
                        {"p_value": None, "supported": False, "note": "insufficient cells"}
                    )
                    raw_p.append(None)
                else:
                    stat = stats.mannwhitneyu(a, b, alternative=alternative)
                    med_o = float(np.median(a))
                    med_e = float(np.median(b))
                    direction = med_o > med_e if alternative == "greater" else med_o < med_e
                    p_value = float(cast(Any, stat).pvalue)
                    payload.update(
                        {
                            "median_efficient": med_e,
                            "median_overcrowd": med_o,
                            "p_value": p_value,
                            "direction_ok": bool(direction),
                        }
                    )
                    raw_p.append(p_value)
            payloads.append(payload)

        adjusted = _holm_adjust(raw_p)
        for payload, p_adj in zip(payloads, adjusted):
            payload["p_value_holm"] = p_adj
            payload["supported"] = bool(
                p_adj is not None and p_adj < alpha and payload.get("direction_ok")
            )
            by_n.append(payload)

        # Coverage saturation on reliable cells at this N.
        sat: dict[str, Any] = {
            "n_sheep": n,
            "hypothesis": "coverage_saturation",
            "metric": coverage_col,
            "supported": False,
        }
        if coverage_col in eff.columns and effort_col in eff.columns and len(eff) >= 2:
            cov = pd.Series(eff.loc[:, coverage_col]).dropna()
            ordered = eff.sort_values(by=dog_col)
            effort = pd.Series(ordered.loc[:, effort_col]).dropna()
            if len(cov) >= 2 and len(effort) >= 2:
                cov_range = float(cov.max() - cov.min())
                effort_up = float(effort.iloc[-1] - effort.iloc[0])
                high = float(np.median(cov)) > 0.5
                sat["median_coverage"] = float(np.median(cov))
                sat["coverage_range"] = cov_range
                sat["effort_rise"] = effort_up
                sat["supported"] = bool(high and cov_range < 0.1 and effort_up > 0)
        by_n.append(sat)

    for hyp in (
        "interference",
        "induced_fragmentation",
        "redundant_effort",
        "coverage_saturation",
    ):
        rows = [r for r in by_n if r["hypothesis"] == hyp]
        holm_vals = [r["p_value_holm"] for r in rows if r.get("p_value_holm") is not None]
        overall[hyp] = {
            "supported": any(bool(r.get("supported")) for r in rows),
            "n_flocks_tested": len(rows),
            "n_flocks_supported": int(sum(bool(r.get("supported")) for r in rows)),
            "p_value_holm": float(min(holm_vals)) if holm_vals else None,
        }
    return {"by_n": by_n, "overall": overall, "correction": "holm"}


def evaluate_temporal_order(
    timeseries_by_trial: list[dict[str, Any]],
    *,
    tick_col: str = "tick",
    i_dir_col: str = "i_dir",
    fragmentation_col: str = "fragmentation",
    success_key: str = "success",
    regime_key: str = "regime",
    rise_z: float = 1.0,
) -> dict[str, Any]:
    """Test whether I_dir / fragmentation rise before failure on overcrowding trials.

    Each item needs: timeseries (DataFrame), success (bool), optional regime.
    For failed overcrowding trials, lead time is ticks from first sustained metric
    rise (z-score >= rise_z vs early-window baseline) to trial end.
    """
    leads_i: list[int] = []
    leads_f: list[int] = []
    n_failed_overcrowd = 0
    for item in timeseries_by_trial:
        ts = item.get("timeseries")
        if ts is None or getattr(ts, "empty", True):
            continue
        if item.get(success_key, True):
            continue
        regime = item.get(regime_key)
        if regime is not None and regime != "overcrowding_collapse":
            continue
        n_failed_overcrowd += 1
        frame = ts.sort_values(tick_col).reset_index(drop=True)
        t_end = int(frame[tick_col].iloc[-1])
        early_n = max(1, len(frame) // 5)

        for col, bucket in ((i_dir_col, leads_i), (fragmentation_col, leads_f)):
            if col not in frame.columns:
                continue
            x = frame[col].astype(float).to_numpy()
            base = x[:early_n]
            mu = float(np.nanmean(base))
            sd = float(np.nanstd(base)) or 1.0
            z = (x - mu) / sd
            hits = np.where(z >= rise_z)[0]
            if len(hits) == 0:
                continue
            t_rise = int(frame.loc[int(hits[0]), tick_col])
            if t_rise < t_end:
                bucket.append(int(t_end - t_rise))

    def _summary(leads: list[int]) -> dict[str, Any]:
        if not leads:
            return {
                "n_with_lead": 0,
                "median_lead_time": None,
                "fraction_with_lead": 0.0,
            }
        return {
            "n_with_lead": len(leads),
            "median_lead_time": float(np.median(leads)),
            "fraction_with_lead": float(len(leads) / max(n_failed_overcrowd, 1)),
        }

    return {
        "n_failed_overcrowd": n_failed_overcrowd,
        "i_dir": _summary(leads_i),
        "fragmentation": _summary(leads_f),
        "supports_temporal_lead": bool(
            n_failed_overcrowd > 0
            and (
                (leads_i and float(np.median(leads_i)) > 0)
                or (leads_f and float(np.median(leads_f)) > 0)
            )
        ),
    }
