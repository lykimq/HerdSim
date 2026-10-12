"""Scaling model fits for D_min(N) / D_min(N, X) (Cap I11)."""

from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import Any, cast

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from analysis.coerce import as_float


def _rmse(y: np.ndarray, yhat: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - yhat) ** 2)))


def _aic(sse: float, m: int, k: int) -> float:
    return float(2 * k + m * np.log(sse / m + 1e-12))


def _bic(sse: float, m: int, k: int) -> float:
    return float(k * np.log(max(m, 1)) + m * np.log(sse / m + 1e-12))


PredictFn = Callable[[np.ndarray, np.ndarray, float], float | None]


def _leave_one_n_rmse(
    n: np.ndarray,
    d: np.ndarray,
    predict_fn: PredictFn,
) -> float | None:
    """Leave-one-flock-size RMSE. None when fewer than 3 distinct N."""
    unique = np.unique(n)
    if len(unique) < 3:
        return None
    errs = []
    for held in unique:
        mask = n != held
        if int(mask.sum()) < 2:
            continue
        for n_i, d_i in zip(n[~mask], d[~mask]):
            yhat_i = predict_fn(n[mask], d[mask], float(n_i))
            if yhat_i is None or yhat_i != yhat_i:
                continue
            errs.append((float(d_i) - float(yhat_i)) ** 2)
    if not errs:
        return None
    return float(np.sqrt(np.mean(errs)))


def _fit_power_params(n: np.ndarray, d: np.ndarray) -> tuple[float, float, float] | None:
    """Fit D = A * N^alpha on positive rows. Returns (A, alpha, log_log_slope)."""
    ok = (n > 0) & (d > 0)
    if int(ok.sum()) < 2:
        return None
    nn = n[ok]
    dd = d[ok]
    log_alpha, log_a = np.polyfit(np.log(nn), np.log(dd), 1)
    guess = (float(np.exp(log_a)), float(log_alpha))

    def _model(x: np.ndarray, amp: float, alpha: float) -> np.ndarray:
        return amp * np.power(x, alpha)

    try:
        (amp, alpha), _ = curve_fit(_model, nn, dd, p0=guess, maxfev=4000)
    except (RuntimeError, ValueError):
        amp, alpha = guess
    return float(amp), float(alpha), float(log_alpha)


def _power_predict(n_tr: np.ndarray, d_tr: np.ndarray, n_i: float) -> float | None:
    """Power law fit by linear-space least squares."""
    if n_i <= 0:
        return None
    fitted = _fit_power_params(n_tr, d_tr)
    if fitted is None:
        return None
    amp, alpha, _ = fitted
    return float(amp * (n_i**alpha))


def _fit_piecewise(n: np.ndarray, d: np.ndarray) -> dict[str, Any] | None:
    """Two-segment linear fit with breakpoint chosen to minimise SSE."""
    m = len(d)
    if m < 4:
        return None
    order = np.argsort(n)
    n_s = n[order]
    d_s = d[order]
    best: dict[str, Any] | None = None
    # Break after index i (need >=2 points each side).
    for i in range(1, m - 2):
        n1, d1 = n_s[: i + 1], d_s[: i + 1]
        n2, d2 = n_s[i + 1 :], d_s[i + 1 :]
        if len(n1) < 2 or len(n2) < 2:
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", np.exceptions.RankWarning)
            b1, a1 = np.polyfit(n1, d1, 1)
            b2, a2 = np.polyfit(n2, d2, 1)
        yhat = np.empty(m)
        yhat[: i + 1] = a1 + b1 * n1
        yhat[i + 1 :] = a2 + b2 * n2
        sse = float(np.sum((d_s - yhat) ** 2))
        cand = {
            "params": {
                "break_n": float(n_s[i]),
                "a1": float(a1),
                "b1": float(b1),
                "a2": float(a2),
                "b2": float(b2),
            },
            "sse": sse,
            "yhat_ordered": yhat,
            "order": order,
        }
        if best is None or sse < best["sse"]:
            best = cand
    if best is None:
        return None
    yhat_full = np.empty(m)
    yhat_full[best["order"]] = best["yhat_ordered"]
    k = 5  # break + 2 slopes + 2 intercepts
    return {
        "params": best["params"],
        "rmse": _rmse(d, yhat_full),
        "aic": _aic(best["sse"], m, k),
        "bic": _bic(best["sse"], m, k),
    }


def fit_scaling_models(
    frontier: pd.DataFrame,
    *,
    sheep_col: str = "n_sheep",
    dmin_col: str = "d_min",
    state_col: str | None = "initial_layout",
) -> dict[str, Any]:
    """Fit candidate scaling models to D_min(N).

    Candidates: constant, linear, power-law, piecewise. When ``state_col`` is
    present with multiple levels, also fit per-state power laws and a pooled
    state-conditioned summary (RQ6 / C6a-C6b).
    """
    work = frontier.dropna(subset=[sheep_col, dmin_col]).copy()
    if work.empty:
        return {"models": {}, "best": None, "n_points": 0, "state_models": {}, "cv": {}}

    n_all = work[sheep_col].astype(float).to_numpy()
    d_all = work[dmin_col].astype(float).to_numpy()
    # Score every candidate on the same positive (N, D_min) rows so AIC/BIC match.
    positive = (n_all > 0) & (d_all > 0)
    if int(positive.sum()) < 1:
        return {"models": {}, "best": None, "n_points": 0, "state_models": {}, "cv": {}}
    n = n_all[positive]
    d = d_all[positive]
    m = len(d)
    models: dict[str, Any] = {}

    # Constant
    c = float(np.mean(d))
    yhat = np.full_like(d, c)
    sse = float(np.sum((d - yhat) ** 2))
    models["constant"] = {
        "params": {"c": c},
        "rmse": _rmse(d, yhat),
        "aic": _aic(sse, m, 1),
        "bic": _bic(sse, m, 1),
    }

    # Linear D = a + b N
    if m >= 2:
        b, a = np.polyfit(n, d, 1)
        yhat = a + b * n
        sse = float(np.sum((d - yhat) ** 2))
        models["linear"] = {
            "params": {"a": float(a), "b": float(b)},
            "rmse": _rmse(d, yhat),
            "aic": _aic(sse, m, 2),
            "bic": _bic(sse, m, 2),
        }

    # Power law D = A * N^alpha, least squares in D (same space as the other models).
    power = _fit_power_params(n, d)
    if power is not None:
        amp, alpha, log_alpha = power
        yhat = amp * np.power(n, alpha)
        sse = float(np.sum((d - yhat) ** 2))
        models["power"] = {
            "params": {
                "A": float(amp),
                "alpha": float(alpha),
                "log_log_slope": float(log_alpha),
            },
            "rmse": _rmse(d, yhat),
            "aic": _aic(sse, m, 2),
            "bic": _bic(sse, m, 2),
        }

    piecewise = _fit_piecewise(n, d)
    if piecewise is not None:
        models["piecewise"] = piecewise

    def _pred_const(_n_tr: np.ndarray, d_tr: np.ndarray, _n_i: float) -> float | None:
        return float(np.mean(d_tr))

    def _pred_linear(n_tr: np.ndarray, d_tr: np.ndarray, n_i: float) -> float | None:
        if len(d_tr) < 2:
            return None
        b_, a_ = np.polyfit(n_tr, d_tr, 1)
        return float(a_ + b_ * n_i)

    def _pred_piecewise(n_tr: np.ndarray, d_tr: np.ndarray, n_i: float) -> float | None:
        fitted = _fit_piecewise(n_tr, d_tr)
        if fitted is None:
            return None
        params = cast(dict[str, Any], fitted["params"])
        if float(n_i) <= as_float(params["break_n"]):
            return float(as_float(params["a1"]) + as_float(params["b1"]) * n_i)
        return float(as_float(params["a2"]) + as_float(params["b2"]) * n_i)

    cv: dict[str, Any] = {}
    for name, fn in (
        ("constant", _pred_const),
        ("linear", _pred_linear),
        ("power", _power_predict),
        ("piecewise", _pred_piecewise),
    ):
        if name in models:
            cv[name] = _leave_one_n_rmse(n, d, fn)

    scored = {name: rmse for name, rmse in cv.items() if rmse is not None}
    if scored:
        best = min(scored.items(), key=lambda kv: kv[1])[0]
    elif models:
        best = min(models.items(), key=lambda kv: kv[1]["rmse"])[0]
    else:
        best = None

    # State-conditioned power laws (compact vs other X0, etc.).
    state_models: dict[str, Any] = {}
    if (
        state_col is not None
        and state_col in work.columns
        and work[state_col].nunique(dropna=True) >= 2
    ):
        for state, sub in work.groupby(state_col, dropna=False):
            sub_fit = fit_scaling_models(
                sub,
                sheep_col=sheep_col,
                dmin_col=dmin_col,
                state_col=None,
            )
            state_models[str(state)] = {
                "best": sub_fit.get("best"),
                "n_points": sub_fit.get("n_points"),
                "models": {
                    k: {kk: vv for kk, vv in v.items() if kk != "yhat_ordered"}
                    for k, v in sub_fit.get("models", {}).items()
                },
            }

    delta_aic: dict[str, float] = {}
    if best and "power" in models:
        for name, payload in models.items():
            if name == "power":
                continue
            delta_aic[name] = float(payload["aic"] - models["power"]["aic"])

    power_loo = cv.get("power")
    piece_loo = cv.get("piecewise")
    separate_loo = _separate_curve_loo(
        work, state_col=state_col, sheep_col=sheep_col, dmin_col=dmin_col
    )
    if separate_loo is not None:
        cv["separate_curves"] = separate_loo
    prefers = _cv_beats(piece_loo, power_loo) or _cv_beats(separate_loo, power_loo)

    return {
        "models": models,
        "best": best,
        "n_points": m,
        "state_models": state_models,
        "cv": cv,
        "delta_aic_vs_power": delta_aic,
        "prefers_piecewise_or_state": prefers,
    }


def _cv_beats(challenger: float | None, baseline: float | None) -> bool:
    """True when challenger leave-one-N RMSE beats baseline by a clear margin.

    Near-zero baselines count as ties so floating-point noise does not flip
    C6a when a single power law already fits to machine precision.
    """
    if challenger is None or baseline is None:
        return False
    margin = max(1e-6, 0.01 * abs(float(baseline)))
    return float(challenger) < float(baseline) - margin


def _separate_curve_loo(
    work: pd.DataFrame,
    *,
    state_col: str | None,
    sheep_col: str,
    dmin_col: str,
) -> float | None:
    """Leave-one-N RMSE of a separate power law per layout."""
    if (
        state_col is None
        or state_col not in work.columns
        or work[state_col].nunique(dropna=True) < 2
    ):
        return None
    n = work[sheep_col].astype(float).to_numpy()
    unique = np.unique(n)
    if len(unique) < 3:
        return None
    errs = []
    for held in unique:
        train = work.loc[work[sheep_col] != held].copy()
        test = work.loc[work[sheep_col] == held].copy()
        for _, row in test.iterrows():
            sub = train.loc[train[state_col] == row.at[state_col]].copy()
            yhat = _power_predict(
                pd.Series(sub.loc[:, sheep_col]).astype(float).to_numpy(),
                pd.Series(sub.loc[:, dmin_col]).astype(float).to_numpy(),
                float(row.at[sheep_col]),
            )
            if yhat is None:
                continue
            errs.append((float(row.at[dmin_col]) - yhat) ** 2)
    if not errs:
        return None
    return float(np.sqrt(np.mean(errs)))
