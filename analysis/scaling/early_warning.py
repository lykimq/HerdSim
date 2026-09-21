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
    correct = 0.0
    for p in pos:
        correct += float(np.sum(p > neg)) + 0.5 * float(np.sum(p == neg))
    return float(correct / (len(pos) * len(neg)))


def _risk_score(
    ts: pd.DataFrame,
    feature_cols: list[str],
    *,
    window_w: int,
    tick_col: str,
) -> np.ndarray:
    score = np.zeros(len(ts), dtype=float)
    used = 0
    for col in feature_cols:
        if col not in ts.columns:
            continue
        x = ts[col].astype(float).to_numpy()
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
    return score


def evaluate_early_warning(
    timeseries: pd.DataFrame,
    *,
    success: bool,
    horizon_k: int = 500,
    window_w: int = 200,
    feature_cols: list[str] | None = None,
    tick_col: str = "tick",
    eval_ticks: list[int] | None = None,
) -> dict[str, Any]:
    """Evaluate whether state features anticipate failure within horizon k.

    For failed trials, a positive label is assigned to ticks in
    [T_end - k, T_end). Feature score is a simple z-scored rise in mean_spread
    / drop in cohesion / rise in fragmentation over the last window_w ticks.

    When ``eval_ticks`` is set (plan: 1000..8000 step 200), AUROC uses only those
    evaluation times that exist in the series.
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

    score = _risk_score(ts, feature_cols, window_w=window_w, tick_col=tick_col)

    if eval_ticks:
        mask = ts[tick_col].isin(eval_ticks).to_numpy()
        if mask.any() and labels[mask].sum() > 0 and labels[mask].sum() < int(mask.sum()):
            auroc = _auroc(score[mask], labels[mask])
        elif mask.any():
            auroc = float("nan")
        else:
            auroc = float("nan")
    else:
        auroc = (
            _auroc(score, labels)
            if labels.sum() > 0 and labels.sum() < len(labels)
            else float("nan")
        )

    lead_time = None
    if not success and feature_cols:
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
        "eval_ticks": list(eval_ticks) if eval_ticks else None,
    }


def default_eval_ticks(
    *,
    start: int = 1000,
    stop: int = 8000,
    step: int = 200,
) -> list[int]:
    """Frozen RQ7 evaluation grid (inclusive start, inclusive stop when aligned)."""
    return list(range(int(start), int(stop) + 1, int(step)))


def evaluate_early_warning_campaign(
    trial_rows: list[dict[str, Any]],
    *,
    horizon_k: int = 500,
    window_w: int = 200,
    eval_ticks: list[int] | None = None,
    n_col: str = "n_sheep",
    d_col: str = "n_shepherds",
) -> dict[str, Any]:
    """Leave-one-N-out early-warning eval vs (N, D) logistic baseline.

    Each trial_rows item: timeseries, success, n_sheep, n_shepherds (and optional id).
    State AUROC is computed per held-out N from per-trial risk at mid eval tick;
    baseline AUROC uses (N, D) failure probability on the same held-out trials.
    """
    ticks = eval_ticks if eval_ticks is not None else default_eval_ticks()
    if not trial_rows:
        return {
            "n_trials": 0,
            "state_auroc_mean": None,
            "nd_auroc_mean": None,
            "beats_nd_baseline": False,
            "folds": [],
        }

    # Per-trial state score: mean risk on eval ticks (or whole-series fallback).
    records = []
    per_trial_eval = []
    for item in trial_rows:
        ts = item.get("timeseries")
        success = bool(item.get("success", False))
        n_sheep = item.get(n_col)
        n_shepherds = item.get(d_col)
        if ts is None or n_sheep is None or n_shepherds is None:
            continue
        ev = evaluate_early_warning(
            ts,
            success=success,
            horizon_k=horizon_k,
            window_w=window_w,
            eval_ticks=ticks,
        )
        per_trial_eval.append(ev)
        frame = ts.sort_values("tick") if "tick" in ts.columns else ts
        score = _risk_score(
            frame.reset_index(drop=True),
            ev.get("feature_cols") or [],
            window_w=window_w,
            tick_col="tick",
        )
        if "tick" in frame.columns:
            mask = frame["tick"].isin(ticks).to_numpy()
            state_score = float(np.nanmean(score[mask])) if mask.any() else float(np.nanmean(score))
        else:
            state_score = float(np.nanmean(score))
        records.append(
            {
                n_col: int(n_sheep),
                d_col: int(n_shepherds),
                "success": success,
                "failed": not success,
                "state_score": state_score,
            }
        )

    meta = pd.DataFrame(records)
    if meta.empty:
        return {
            "n_trials": 0,
            "state_auroc_mean": None,
            "nd_auroc_mean": None,
            "beats_nd_baseline": False,
            "folds": [],
            "trial_summaries": summarise_early_warning(per_trial_eval),
        }

    folds = []
    state_aurocs = []
    nd_aurocs = []
    for hold_n in sorted(meta[n_col].unique()):
        test = meta[meta[n_col] == hold_n]
        train = meta[meta[n_col] != hold_n]
        if train.empty or test.empty:
            continue
        # Fit ND baseline on train folds; score held-out N.
        y_train = (~train["success"].astype(bool)).astype(float).to_numpy()
        x_train = train[[n_col, d_col]].astype(float).to_numpy()
        mu = x_train.mean(axis=0)
        sigma = x_train.std(axis=0)
        sigma[sigma < 1e-9] = 1.0
        xs = (x_train - mu) / sigma
        w = np.zeros(2)
        b = 0.0
        n_tr = len(y_train)
        for _ in range(200):
            z = xs @ w + b
            p = 1.0 / (1.0 + np.exp(-np.clip(z, -50, 50)))
            err = p - y_train
            w -= 0.1 * ((xs.T @ err) / max(n_tr, 1) + 1e-3 * w)
            b -= 0.1 * float(err.mean())
        x_te = test[[n_col, d_col]].astype(float).to_numpy()
        xs_te = (x_te - mu) / sigma
        nd_score = 1.0 / (1.0 + np.exp(-np.clip(xs_te @ w + b, -50, 50)))
        labels = test["failed"].astype(int).to_numpy()
        st = _auroc(test["state_score"].to_numpy(), labels)
        nd = _auroc(nd_score, labels)
        folds.append(
            {
                "hold_n": int(hold_n),
                "n_test": int(len(test)),
                "state_auroc": st,
                "nd_auroc": nd,
            }
        )
        if st == st:
            state_aurocs.append(st)
        if nd == nd:
            nd_aurocs.append(nd)

    state_mean = float(np.mean(state_aurocs)) if state_aurocs else None
    nd_mean = float(np.mean(nd_aurocs)) if nd_aurocs else None
    return {
        "n_trials": int(len(meta)),
        "state_auroc_mean": state_mean,
        "nd_auroc_mean": nd_mean,
        "beats_nd_baseline": bool(
            state_mean is not None and nd_mean is not None and state_mean > nd_mean
        ),
        "folds": folds,
        "horizon_k": horizon_k,
        "window_w": window_w,
        "eval_ticks": ticks,
        "trial_summaries": summarise_early_warning(per_trial_eval),
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
        "frac_lead_ge_500": (
            float(np.mean([1.0 if (lt is not None and lt >= 500) else 0.0 for lt in leads]))
            if leads
            else 0.0
        ),
    }
