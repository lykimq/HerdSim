"""Scaling model fits for D_min(N) / D_min(N, X) (Cap I11)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _rmse(y: np.ndarray, yhat: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - yhat) ** 2)))


def fit_scaling_models(
    frontier: pd.DataFrame,
    *,
    sheep_col: str = "n_sheep",
    dmin_col: str = "d_min",
) -> dict[str, Any]:
    """Fit candidate scaling models to D_min(N).

    Candidates: constant, linear, power-law (log-log). Returns RMSE and AIC-like
    scores so RQ6 can choose among C6a/C6b style conclusions.
    """
    work = frontier.dropna(subset=[sheep_col, dmin_col]).copy()
    if work.empty:
        return {"models": {}, "best": None}
    n = work[sheep_col].astype(float).to_numpy()
    d = work[dmin_col].astype(float).to_numpy()
    m = len(d)
    models: dict[str, Any] = {}

    # Constant
    c = float(np.mean(d))
    yhat = np.full_like(d, c)
    sse = float(np.sum((d - yhat) ** 2))
    models["constant"] = {
        "params": {"c": c},
        "rmse": _rmse(d, yhat),
        "aic": 2 * 1 + m * np.log(sse / m + 1e-12),
    }

    # Linear D = a + b N
    if m >= 2:
        b, a = np.polyfit(n, d, 1)
        yhat = a + b * n
        sse = float(np.sum((d - yhat) ** 2))
        models["linear"] = {
            "params": {"a": float(a), "b": float(b)},
            "rmse": _rmse(d, yhat),
            "aic": 2 * 2 + m * np.log(sse / m + 1e-12),
        }

    # Power law D = A * N^alpha  (positive only)
    mask = (n > 0) & (d > 0)
    if int(mask.sum()) >= 2:
        nn = n[mask]
        dd = d[mask]
        alpha, log_a = np.polyfit(np.log(nn), np.log(dd), 1)
        A = float(np.exp(log_a))
        yhat = A * (n ** alpha)
        sse = float(np.sum((d - yhat) ** 2))
        models["power"] = {
            "params": {"A": A, "alpha": float(alpha)},
            "rmse": _rmse(d, yhat),
            "aic": 2 * 2 + m * np.log(sse / m + 1e-12),
        }

    best = min(models.items(), key=lambda kv: kv[1]["aic"])[0] if models else None
    return {"models": models, "best": best, "n_points": m}
