"""Mechanism hypothesis tests for overcrowding (Cap I8)."""

from __future__ import annotations

from typing import Any

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
    effort_col: str = "mean_shepherd_path",
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Compare mechanism metrics between efficient and overcrowding cells.

    Claim C3 style: overcrowding cells have higher median I_dir and/or
    fragmentation than efficient cells at the same N (rank test). p-values are
    Holm-corrected across the four primary hypotheses.
    """
    key = [sheep_col, dog_col]
    reg = regimes[key + ["regime"]].drop_duplicates(key)
    merged = trials.merge(reg, on=key, how="left")

    results: dict[str, Any] = {"by_n": [], "overall": {}, "correction": "holm"}
    hyp_order: list[str] = []
    raw_p: list[float | None] = []

    for metric, hyp in (
        (i_dir_col, "interference"),
        (fragmentation_col, "induced_fragmentation"),
        (coverage_col, "coverage_saturation"),
        (effort_col, "redundant_effort"),
    ):
        hyp_order.append(hyp)
        if metric not in merged.columns:
            results["overall"][hyp] = {
                "metric": metric,
                "available": False,
                "p_value": None,
                "p_value_holm": None,
                "supported": False,
            }
            raw_p.append(None)
            continue

        eff = merged[merged["regime"] == "efficient_operation"][metric].dropna()
        ovr = merged[merged["regime"] == "overcrowding_collapse"][metric].dropna()
        if len(eff) < 2 or len(ovr) < 2:
            results["overall"][hyp] = {
                "metric": metric,
                "available": True,
                "n_efficient": int(len(eff)),
                "n_overcrowd": int(len(ovr)),
                "p_value": None,
                "p_value_holm": None,
                "supported": False,
                "note": "insufficient samples",
            }
            raw_p.append(None)
            continue

        if hyp in ("interference", "induced_fragmentation", "redundant_effort"):
            stat = stats.mannwhitneyu(ovr, eff, alternative="greater")
            raw_supported = bool(stat.pvalue < alpha) and float(np.median(ovr)) > float(
                np.median(eff)
            )
        else:
            # Coverage saturation: overcrowding coverage not much higher than efficient.
            stat = stats.mannwhitneyu(ovr, eff, alternative="two-sided")
            raw_supported = bool(abs(float(np.median(ovr)) - float(np.median(eff))) < 0.1)

        results["overall"][hyp] = {
            "metric": metric,
            "available": True,
            "n_efficient": int(len(eff)),
            "n_overcrowd": int(len(ovr)),
            "median_efficient": float(np.median(eff)),
            "median_overcrowd": float(np.median(ovr)),
            "p_value": float(stat.pvalue),
            "p_value_holm": None,
            "supported_uncorrected": raw_supported,
            "supported": False,
        }
        raw_p.append(float(stat.pvalue))

    adjusted = _holm_adjust(raw_p)
    for hyp, p_adj in zip(hyp_order, adjusted):
        payload = results["overall"][hyp]
        payload["p_value_holm"] = p_adj
        if hyp == "coverage_saturation":
            # Saturation is a similarity claim; keep the descriptive flag.
            payload["supported"] = bool(payload.get("supported_uncorrected"))
        elif p_adj is None:
            payload["supported"] = False
        else:
            payload["supported"] = bool(
                p_adj < alpha
                and float(payload.get("median_overcrowd", 0))
                > float(payload.get("median_efficient", 0))
            )

    if i_dir_col in merged.columns:
        for n, g in merged.groupby(sheep_col):
            eff = g[g["regime"] == "efficient_operation"][i_dir_col].dropna()
            ovr = g[g["regime"] == "overcrowding_collapse"][i_dir_col].dropna()
            if len(eff) < 2 or len(ovr) < 2:
                continue
            stat = stats.mannwhitneyu(ovr, eff, alternative="greater")
            results["by_n"].append(
                {
                    "n_sheep": int(n),
                    "p_value": float(stat.pvalue),
                    "median_efficient": float(np.median(eff)),
                    "median_overcrowd": float(np.median(ovr)),
                    "supported": bool(stat.pvalue < alpha),
                }
            )
    return results


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
