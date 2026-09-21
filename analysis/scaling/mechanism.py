"""Mechanism hypothesis tests for overcrowding (Cap I8)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


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
) -> dict[str, Any]:
    """Compare mechanism metrics between efficient and overcrowding cells.

    Claim C3 style: overcrowding cells have higher median I_dir and/or
    fragmentation than efficient cells at the same N (rank test).
    """
    # Attach regime labels onto trial rows via (N, D).
    key = [sheep_col, dog_col]
    reg = regimes[key + ["regime"]].drop_duplicates(key)
    merged = trials.merge(reg, on=key, how="left")

    results: dict[str, Any] = {"by_n": [], "overall": {}}
    for metric, hyp in (
        (i_dir_col, "interference"),
        (fragmentation_col, "induced_fragmentation"),
        (coverage_col, "coverage_saturation"),
        (effort_col, "redundant_effort"),
    ):
        if metric not in merged.columns:
            results["overall"][hyp] = {
                "metric": metric,
                "available": False,
                "p_value": None,
                "supported": False,
            }
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
                "supported": False,
                "note": "insufficient samples",
            }
            continue

        # Higher I_dir / fragmentation in overcrowding supports those hypotheses.
        # Coverage: look for plateau -- compare variance; effort: higher in overcrowding.
        if hyp in ("interference", "induced_fragmentation", "redundant_effort"):
            stat = stats.mannwhitneyu(ovr, eff, alternative="greater")
            supported = bool(stat.pvalue < 0.05) and float(np.median(ovr)) > float(
                np.median(eff)
            )
        else:
            # Coverage saturation: overcrowding coverage not much higher than efficient
            # while effort is higher -- approximate with non-greater coverage.
            stat = stats.mannwhitneyu(ovr, eff, alternative="two-sided")
            supported = bool(abs(float(np.median(ovr)) - float(np.median(eff))) < 0.1)

        results["overall"][hyp] = {
            "metric": metric,
            "available": True,
            "n_efficient": int(len(eff)),
            "n_overcrowd": int(len(ovr)),
            "median_efficient": float(np.median(eff)),
            "median_overcrowd": float(np.median(ovr)),
            "p_value": float(stat.pvalue),
            "supported": supported,
        }

    # Per-N I_dir tests for C3 reporting.
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
                    "supported": bool(stat.pvalue < 0.05),
                }
            )
    return results
