"""State vs (N, D) predictor comparison for RQ1 (Cap I6)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _logistic_nll(y: np.ndarray, p: np.ndarray) -> float:
    p = np.clip(p, 1e-6, 1.0 - 1e-6)
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def _fit_logistic(
    x: np.ndarray,
    y: np.ndarray,
    *,
    n_iter: int = 200,
    lr: float = 0.1,
) -> tuple[np.ndarray, float]:
    """Simple L2-regularised logistic regression via gradient descent."""
    n, d = x.shape
    # Standardise features.
    mu = x.mean(axis=0)
    sigma = x.std(axis=0)
    sigma[sigma < 1e-9] = 1.0
    xs = (x - mu) / sigma
    w = np.zeros(d)
    b = 0.0
    for _ in range(n_iter):
        z = xs @ w + b
        p = 1.0 / (1.0 + np.exp(-z))
        err = p - y
        w -= lr * ((xs.T @ err) / n + 1e-3 * w)
        b -= lr * float(err.mean())
    return np.concatenate([[b], w]), float("nan")  # AIC filled by caller


def _predict_proba(beta: np.ndarray, x: np.ndarray) -> np.ndarray:
    b, w = beta[0], beta[1:]
    mu = x.mean(axis=0)
    sigma = x.std(axis=0)
    sigma[sigma < 1e-9] = 1.0
    xs = (x - mu) / sigma
    z = xs @ w + b
    return 1.0 / (1.0 + np.exp(-np.clip(z, -50, 50)))


def compare_state_vs_nd_predictors(
    df: pd.DataFrame,
    *,
    success_col: str = "success",
    nd_cols: list[str] | None = None,
    state_cols: list[str] | None = None,
    test_fraction: float = 0.3,
    seed: int = 2026,
) -> dict[str, Any]:
    """Compare (N, D) logistic predictor vs (N, D + state features).

    Returns out-of-sample negative log-likelihood and AIC-like scores. A state
    model is preferred when delta_aic > 4 (plan claim C1b threshold).
    """
    nd_cols = nd_cols or ["n_sheep", "n_shepherds"]
    state_cols = state_cols or [
        c
        for c in (
            "mean_cohesion",
            "mean_mean_spread",
            "mean_extent",
            "mean_fragmentation",
            "mean_outlier_count",
            "initial_mean_spread",
            "initial_cohesion",
        )
        if c in df.columns
    ]
    needed = nd_cols + [success_col]
    work = df.dropna(subset=[c for c in needed if c in df.columns]).copy()
    if work.empty or success_col not in work.columns:
        return {
            "n_train": 0,
            "n_test": 0,
            "nd_nll": float("nan"),
            "state_nll": float("nan"),
            "delta_aic": float("nan"),
            "prefers_state": False,
            "state_cols": state_cols,
        }

    y = work[success_col].astype(float).to_numpy()
    x_nd = work[nd_cols].astype(float).to_numpy()
    x_state = work[nd_cols + state_cols].astype(float).to_numpy() if state_cols else x_nd

    rng = np.random.default_rng(seed)
    idx = np.arange(len(work))
    rng.shuffle(idx)
    n_test = max(1, int(round(test_fraction * len(idx))))
    test_idx = idx[:n_test]
    train_idx = idx[n_test:] if len(idx) > n_test else idx

    beta_nd, _ = _fit_logistic(x_nd[train_idx], y[train_idx])
    beta_st, _ = _fit_logistic(x_state[train_idx], y[train_idx])
    p_nd = _predict_proba(beta_nd, x_nd[test_idx])
    p_st = _predict_proba(beta_st, x_state[test_idx])
    nll_nd = _logistic_nll(y[test_idx], p_nd)
    nll_st = _logistic_nll(y[test_idx], p_st)

    # AIC ≈ 2k + 2n*NLL (using mean NLL * n)
    n_te = len(test_idx)
    aic_nd = 2 * (1 + len(nd_cols)) + 2 * n_te * nll_nd
    aic_st = 2 * (1 + x_state.shape[1]) + 2 * n_te * nll_st
    delta = aic_nd - aic_st
    return {
        "n_train": int(len(train_idx)),
        "n_test": int(n_te),
        "nd_nll": nll_nd,
        "state_nll": nll_st,
        "aic_nd": aic_nd,
        "aic_state": aic_st,
        "delta_aic": float(delta),
        "prefers_state": bool(delta > 4.0),
        "state_cols": state_cols,
    }
