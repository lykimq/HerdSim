"""Early-warning evaluation for impending herding failure (Cap I12)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _auroc(scores: np.ndarray, labels: np.ndarray) -> float:
    """Compute AUROC without sklearn."""
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=int)
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    # Mann-Whitney U form of AUROC.
    correct = 0.0
    for p in pos:
        correct += float(np.sum(p > neg)) + 0.5 * float(np.sum(p == neg))
    return float(correct / (len(pos) * len(neg)))


def evaluate_early_warning(
    timeseries: pd.DataFrame,
    *,
    success: bool,
    horizon_k: int = 500,
    window_w: int = 200,
    feature_cols: list[str] | None = None,
    tick_col: str = "tick",
) -> dict[str, Any]:
    """Evaluate whether state features anticipate failure within horizon k.

    For failed trials, a positive label is assigned to ticks in
    [T_end - k, T_end). Feature score is a simple z-scored rise in mean_spread
    / drop in cohesion / rise in fragmentation over the last window_w ticks.
    """
    feature_cols = feature_cols or [
        c
        for c in ("mean_spread", "cohesion", "fragmentation", "i_dir", "coverage")
        if c in timeseries.columns
    ]
    if timeseries.empty or tick_col not in timeseries.columns:
        return {
            "auroc": float("nan"),
            "lead_time": None,
            "n_ticks": 0,
            "feature_cols": feature_cols,
        }

    ts = timeseries.sort_values(tick_col).reset_index(drop=True)
    t_end = int(ts[tick_col].iloc[-1])
    labels = np.zeros(len(ts), dtype=int)
    if not success:
        labels[(ts[tick_col] >= max(0, t_end - horizon_k)).to_numpy()] = 1

    # Build a simple risk score: average of available normalised features.
    # Higher spread / fragmentation / i_dir and lower cohesion / coverage => risk.
    score = np.zeros(len(ts), dtype=float)
    used = 0
    for col in feature_cols:
        x = ts[col].astype(float).to_numpy()
        # Rolling mean over window_w.
        w = max(1, window_w)
        kernel = np.ones(w) / w
        smooth = np.convolve(x, kernel, mode="same")
        mu = float(np.nanmean(smooth))
        sd = float(np.nanstd(smooth)) or 1.0
        z = (smooth - mu) / sd
        if col in ("cohesion", "coverage"):
            z = -z
        score += z
        used += 1
    if used:
        score /= used

    auroc = _auroc(score, labels) if labels.sum() > 0 and labels.sum() < len(labels) else float("nan")

    lead_time = None
    if not success and used:
        # First tick where score exceeds 1 std above mean among labelled region.
        thr = float(np.nanmean(score) + np.nanstd(score))
        hits = np.where((labels == 1) & (score >= thr))[0]
        if len(hits):
            lead_time = int(t_end - int(ts.loc[int(hits[0]), tick_col]))

    return {
        "auroc": auroc,
        "lead_time": lead_time,
        "n_ticks": int(len(ts)),
        "feature_cols": feature_cols,
        "horizon_k": horizon_k,
        "window_w": window_w,
        "failed_trial": not success,
    }


def summarise_early_warning(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate AUROC and lead-time distribution across trials."""
    if not results:
        return {"n_trials": 0, "median_auroc": None, "median_lead_time": None}
    aurocs = [r["auroc"] for r in results if r.get("auroc") == r.get("auroc")]
    leads = [r["lead_time"] for r in results if r.get("lead_time") is not None]
    return {
        "n_trials": len(results),
        "median_auroc": float(np.median(aurocs)) if aurocs else None,
        "mean_auroc": float(np.mean(aurocs)) if aurocs else None,
        "median_lead_time": float(np.median(leads)) if leads else None,
        "n_with_lead_time": len(leads),
    }
