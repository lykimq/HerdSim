"""Early-warning evaluation for impending herding failure (Cap I12)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

_LOWER_IS_RISK = {"cohesion", "coverage"}


def _auroc(scores: np.ndarray, labels: np.ndarray) -> float:
    """Compute AUROC without sklearn."""
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=int)
    ok = np.isfinite(scores)
    scores = scores[ok]
    labels = labels[ok]
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    correct = 0.0
    for p in pos:
        correct += float(np.sum(p > neg)) + 0.5 * float(np.sum(p == neg))
    return float(correct / (len(pos) * len(neg)))


def _feature_matrix(
    ts: pd.DataFrame,
    feature_cols: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    used: list[str] = []
    cols: list[np.ndarray] = []
    for col in feature_cols:
        if col not in ts.columns:
            continue
        used.append(col)
        cols.append(ts[col].astype(float).to_numpy())
    if not cols:
        return np.zeros(len(ts)), np.zeros((len(ts), 0)), []
    ticks = ts["tick"].to_numpy() if "tick" in ts.columns else np.arange(len(ts))
    return ticks.astype(float), np.column_stack(cols), used


def _window_means(
    ticks: np.ndarray,
    values: np.ndarray,
    feature_names: list[str],
    query_ticks: np.ndarray,
    window_w: int,
) -> np.ndarray:
    """Mean of each feature on (t - window_w, t], higher means more risk."""
    out = np.full(len(query_ticks), np.nan)
    if values.size == 0 or len(feature_names) == 0:
        return out
    signs = np.array([-1.0 if name in _LOWER_IS_RISK else 1.0 for name in feature_names])
    w = max(1, int(window_w))
    for i, t in enumerate(query_ticks):
        mask = (ticks > float(t) - w) & (ticks <= float(t))
        if not np.any(mask):
            continue
        window = np.nanmean(values[mask], axis=0)
        out[i] = float(np.nanmean(window * signs))
    return out


def _opening_threshold(
    ticks: np.ndarray,
    scores: np.ndarray,
    window_w: int,
) -> tuple[float, float] | None:
    """Threshold from the opening of the series, before later rises."""
    if len(ticks) == 0:
        return None
    baseline_end = float(np.min(ticks) + 2 * max(1, window_w))
    base = scores[(ticks <= baseline_end) & np.isfinite(scores)]
    if len(base) == 0:
        return None
    sd = float(np.std(base))
    thr = float(np.mean(base) + (sd if sd > 1e-9 else 1e-6))
    return thr, baseline_end


def evaluate_early_warning(
    timeseries: pd.DataFrame,
    *,
    success: bool,
    horizon_k: int = 500,
    window_w: int = 200,
    feature_cols: list[str] | None = None,
    tick_col: str = "tick",
    eval_ticks: list[int] | None = None,
    time_limit: int | None = None,
) -> dict[str, Any]:
    """Score imminent failure from a causal feature window.

    At each eval tick t with t + horizon_k still inside the time limit, the
    score uses only ticks in (t - window_w, t]. The label is 1 when this trial
    fails inside (t, t + horizon_k]. Lead time is the gap from the first
    opening-threshold crossing until failure and may be longer than horizon_k.
    """
    feature_cols = feature_cols or [
        c
        for c in (
            "mean_spread",
            "cohesion",
            "fragmentation",
            "perimeter",
            "hull_area",
            "flock_density",
            "aspect_ratio",
            "i_dir",
            "coverage",
        )
        if c in timeseries.columns
    ]
    empty = {
        "auroc": float("nan"),
        "lead_time": None,
        "n_ticks": 0,
        "feature_cols": feature_cols,
        "failed_trial": not success,
        "horizon_k": horizon_k,
        "window_w": window_w,
    }
    if timeseries.empty or tick_col not in timeseries.columns:
        return empty

    ts = timeseries.sort_values(tick_col).reset_index(drop=True)
    ticks, values, used = _feature_matrix(ts, feature_cols)
    t_end = int(ts[tick_col].iloc[-1])
    limit = int(time_limit) if time_limit is not None else t_end
    if eval_ticks is None:
        candidates = [int(t) for t in ts[tick_col].tolist()]
    else:
        candidates = [int(t) for t in eval_ticks]
    valid = [t for t in candidates if t + int(horizon_k) <= limit]
    query = np.asarray(valid, dtype=float)
    scores = _window_means(ticks, values, used, query, window_w)
    labels = np.zeros(len(valid), dtype=int)
    if not success:
        for i, t in enumerate(valid):
            if t < t_end <= t + int(horizon_k):
                labels[i] = 1
    auroc = _auroc(scores, labels) if len(valid) else float("nan")

    lead_time = None
    if not success and used:
        all_scores = _window_means(ticks, values, used, ticks, window_w)
        opened = _opening_threshold(ticks, all_scores, window_w)
        if opened is not None:
            thr, baseline_end = opened
            hits = np.where((ticks > baseline_end) & (all_scores >= thr))[0]
            if len(hits):
                lead_time = int(t_end - int(ticks[int(hits[0])]))

    return {
        "auroc": auroc,
        "lead_time": lead_time,
        "n_ticks": int(len(ts)),
        "feature_cols": used,
        "horizon_k": horizon_k,
        "window_w": window_w,
        "failed_trial": not success,
        "eval_ticks": valid,
        "time_limit": limit,
    }


def default_eval_ticks(
    *,
    start: int = 1000,
    stop: int = 8000,
    step: int = 200,
) -> list[int]:
    """Frozen RQ7 evaluation grid (inclusive start, inclusive stop when aligned)."""
    return list(range(int(start), int(stop) + 1, int(step)))


def _fit_nd_scores(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
) -> np.ndarray:
    mu = x_train.mean(axis=0)
    sigma = x_train.std(axis=0)
    sigma = np.where(sigma < 1e-9, 1.0, sigma)
    xs = (x_train - mu) / sigma
    w = np.zeros(x_train.shape[1])
    b = 0.0
    n_tr = max(len(y_train), 1)
    for _ in range(200):
        z = xs @ w + b
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -50, 50)))
        err = p - y_train
        w -= 0.1 * ((xs.T @ err) / n_tr + 1e-3 * w)
        b -= 0.1 * float(err.mean())
    xs_te = (x_test - mu) / sigma
    return 1.0 / (1.0 + np.exp(-np.clip(xs_te @ w + b, -50, 50)))


def evaluate_early_warning_campaign(
    trial_rows: list[dict[str, Any]],
    *,
    horizon_k: int = 500,
    window_w: int = 200,
    eval_ticks: list[int] | None = None,
    n_col: str = "n_sheep",
    d_col: str = "n_shepherds",
    time_limit: int | None = None,
) -> dict[str, Any]:
    """Leave-one-N-out state scores versus an (N, D) logistic on the same labels.

    Each row is one eval tick. Features at t use only (t - window_w, t]. The
    (N, D) model is fit on other flock sizes and applied with that training
    standardization.
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

    records: list[dict[str, Any]] = []
    per_trial_eval: list[dict[str, Any]] = []
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
            time_limit=time_limit,
        )
        per_trial_eval.append(ev)
        frame = ts.sort_values("tick") if "tick" in ts.columns else ts
        tick_arr, values, used = _feature_matrix(frame.reset_index(drop=True), ev["feature_cols"])
        valid = ev.get("eval_ticks") or []
        scores = _window_means(tick_arr, values, used, np.asarray(valid, dtype=float), window_w)
        t_end = int(frame["tick"].iloc[-1]) if "tick" in frame.columns and len(frame) else 0
        limit = int(time_limit) if time_limit is not None else t_end
        for t, score in zip(valid, scores):
            if int(t) + int(horizon_k) > limit:
                continue
            label = 0
            if not success and int(t) < t_end <= int(t) + int(horizon_k):
                label = 1
            records.append(
                {
                    n_col: int(n_sheep),
                    d_col: int(n_shepherds),
                    "label": label,
                    "state_score": float(score),
                }
            )

    meta = pd.DataFrame(records)
    summary = summarise_early_warning(per_trial_eval)
    if meta.empty:
        return {
            "n_trials": len(per_trial_eval),
            "state_auroc_mean": None,
            "nd_auroc_mean": None,
            "beats_nd_baseline": False,
            "folds": [],
            "trial_summaries": summary,
        }

    folds = []
    state_aurocs = []
    nd_aurocs = []
    for hold_n in sorted(meta[n_col].unique()):
        test = meta.loc[meta[n_col] == hold_n].copy()
        train = meta.loc[meta[n_col] != hold_n].copy()
        if train.empty or test.empty or train["label"].nunique() < 2:
            continue
        y_train = train.loc[:, "label"].astype(float).to_numpy()
        x_train = train.loc[:, [n_col, d_col]].astype(float).to_numpy()
        x_te = test.loc[:, [n_col, d_col]].astype(float).to_numpy()
        nd_score = _fit_nd_scores(x_train, y_train, x_te)
        labels = test.loc[:, "label"].astype(int).to_numpy()
        st = _auroc(test.loc[:, "state_score"].to_numpy(), labels)
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
        "n_trials": len(per_trial_eval),
        "state_auroc_mean": state_mean,
        "nd_auroc_mean": nd_mean,
        "beats_nd_baseline": bool(
            state_mean is not None and nd_mean is not None and state_mean > nd_mean
        ),
        "folds": folds,
        "horizon_k": horizon_k,
        "window_w": window_w,
        "eval_ticks": ticks,
        "trial_summaries": summary,
    }


def summarise_early_warning(
    results: list[dict[str, Any]],
    *,
    min_lead: int = 500,
) -> dict[str, Any]:
    """Aggregate AUROC and lead time. Misses count in the lead-time fraction."""
    if not results:
        return {
            "n_trials": 0,
            "median_auroc": None,
            "median_lead_time": None,
            "frac_lead_ge_500": 0.0,
        }
    aurocs = [r["auroc"] for r in results if r.get("auroc") == r.get("auroc")]
    failed = [r for r in results if r.get("failed_trial")]
    leads = [r.get("lead_time") for r in failed]
    defined = [lt for lt in leads if lt is not None]
    if failed:
        frac = float(np.mean([1.0 if (lt is not None and lt >= min_lead) else 0.0 for lt in leads]))
    else:
        frac = 0.0
    return {
        "n_trials": len(results),
        "n_failures": len(failed),
        "median_auroc": float(np.median(aurocs)) if aurocs else None,
        "mean_auroc": float(np.mean(aurocs)) if aurocs else None,
        "median_lead_time": float(np.median(defined)) if defined else None,
        "n_with_lead_time": len(defined),
        "frac_lead_ge_500": frac,
    }
