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
    n_iter: int = 400,
    lr: float = 0.2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """L2 logistic regression. Returns weights, training mean, and training std."""
    mu = x.mean(axis=0)
    sigma = x.std(axis=0)
    sigma = np.where(sigma < 1e-9, 1.0, sigma)
    xs = (x - mu) / sigma
    n, d = xs.shape
    w = np.zeros(d)
    b = 0.0
    for _ in range(n_iter):
        z = xs @ w + b
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -50, 50)))
        err = p - y
        w -= lr * ((xs.T @ err) / max(n, 1) + 1e-3 * w)
        b -= lr * float(err.mean())
    return np.concatenate([[b], w]), mu, sigma


def _predict_proba(
    beta: np.ndarray,
    x: np.ndarray,
    mu: np.ndarray,
    sigma: np.ndarray,
) -> np.ndarray:
    b, w = beta[0], beta[1:]
    xs = (x - mu) / sigma
    z = xs @ w + b
    return 1.0 / (1.0 + np.exp(-np.clip(z, -50, 50)))


def _layout_dummies(
    frame: pd.DataFrame,
    layout_col: str,
    levels: list[str] | None,
) -> tuple[np.ndarray, list[str]]:
    if layout_col not in frame.columns:
        return np.zeros((len(frame), 0)), levels or []
    raw = frame[layout_col].astype(str)
    if levels is None:
        levels = sorted(raw.unique().tolist())
    if len(levels) < 2:
        return np.zeros((len(frame), 0)), levels
    cols = [(raw == level).to_numpy(dtype=float) for level in levels[1:]]
    return np.column_stack(cols), levels


def _numeric_block(frame: pd.DataFrame, cols: list[str]) -> np.ndarray:
    if not cols:
        return np.zeros((len(frame), 0))
    return frame[cols].astype(float).to_numpy()


def _default_state_cols(df: pd.DataFrame, nd_cols: list[str]) -> list[str]:
    """Early-window numeric columns. Full-trial means are not predictors."""
    cols = []
    for col in df.columns:
        if not str(col).startswith("early_"):
            continue
        if col in nd_cols:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue
        cols.append(col)
    return cols


def compare_state_vs_nd_predictors(
    df: pd.DataFrame,
    *,
    success_col: str = "success",
    nd_cols: list[str] | None = None,
    state_cols: list[str] | None = None,
    layout_col: str = "initial_layout",
    sheep_col: str = "n_sheep",
) -> dict[str, Any]:
    """Leave-one-N-out negative log-likelihood of (N, D) versus layout plus early state.

    Numeric columns are standardized on the training flocks and those moments
    are applied to the held-out flock. The state model is preferred when its
    out-of-sample negative log-likelihood is lower. One flock size cannot be
    cross-validated.
    """
    nd_cols = list(nd_cols or ["n_sheep", "n_shepherds"])
    if state_cols is None:
        state_cols = _default_state_cols(df, nd_cols)
    else:
        state_cols = [c for c in state_cols if c in df.columns and c not in nd_cols]

    needed = [c for c in nd_cols + [success_col, sheep_col] if c in df.columns]
    if (
        success_col not in df.columns
        or sheep_col not in df.columns
        or any(c not in df.columns for c in nd_cols)
    ):
        return {
            "n_folds": 0,
            "nd_nll": float("nan"),
            "state_nll": float("nan"),
            "prefers_state": False,
            "state_cols": state_cols,
            "note": "missing N, D, or success",
        }

    work = df.dropna(subset=needed + state_cols).copy()
    work["_y"] = work[success_col].astype(float)
    flocks = sorted(int(v) for v in work[sheep_col].dropna().unique())
    if len(flocks) < 2 or work["_y"].nunique() < 2:
        return {
            "n_folds": 0,
            "nd_nll": float("nan"),
            "state_nll": float("nan"),
            "prefers_state": False,
            "state_cols": state_cols,
            "note": "need at least two flock sizes and both outcomes",
        }

    y_nd: list[float] = []
    p_nd: list[float] = []
    y_st: list[float] = []
    p_st: list[float] = []
    for held in flocks:
        test = work[work[sheep_col] == held]
        train = work[work[sheep_col] != held]
        if train["_y"].nunique() < 2 or test.empty:
            continue
        y_train = train["_y"].to_numpy()
        y_test = test["_y"].to_numpy()
        x_nd_tr = _numeric_block(train, nd_cols)
        x_nd_te = _numeric_block(test, nd_cols)
        beta, mu, sigma = _fit_logistic(x_nd_tr, y_train)
        p_nd.extend(_predict_proba(beta, x_nd_te, mu, sigma).tolist())
        y_nd.extend(y_test.tolist())

        dummies_tr, levels = _layout_dummies(train, layout_col, None)
        dummies_te, _ = _layout_dummies(test, layout_col, levels)
        x_st_tr = np.column_stack([x_nd_tr, _numeric_block(train, state_cols), dummies_tr])
        x_st_te = np.column_stack([x_nd_te, _numeric_block(test, state_cols), dummies_te])
        if x_st_tr.shape[1] == 0:
            x_st_tr = np.zeros((len(train), 1))
            x_st_te = np.zeros((len(test), 1))
        beta_s, mu_s, sigma_s = _fit_logistic(x_st_tr, y_train)
        p_st.extend(_predict_proba(beta_s, x_st_te, mu_s, sigma_s).tolist())
        y_st.extend(y_test.tolist())

    if not y_nd or not y_st:
        nll_nd = float("nan")
        nll_st = float("nan")
    else:
        nll_nd = _logistic_nll(np.asarray(y_nd), np.asarray(p_nd))
        nll_st = _logistic_nll(np.asarray(y_st), np.asarray(p_st))
    return {
        "n_folds": int(len(flocks)),
        "nd_nll": nll_nd,
        "state_nll": nll_st,
        "prefers_state": bool(nll_st < nll_nd),
        "state_cols": state_cols,
        "layout_col": layout_col if layout_col in work.columns else None,
    }
