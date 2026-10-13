"""Scaling model fits for D_min(N) / D_min(N, X) (Cap I11 / RQ6).

Pipeline:
1. Take a frontier table of (N, D_min) points (usually from Package A).
2. Fit candidate curves on those points: constant, linear, power, piecewise.
3. Score each curve with leave-one-N-out RMSE (how well it predicts a held-out flock size).
4. Pick the lowest leave-one-N RMSE as ``best``; also report whether piecewise or
   per-layout curves beat a single power law (``prefers_piecewise_or_state``, C6a).

The fits describe this frontier only. A low piecewise RMSE on a two-level step does
not imply a universal scaling law.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import Any, cast

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from analysis.coerce import as_float


def _rmse(y: np.ndarray, yhat: np.ndarray) -> float:
    """Root-mean-square error between observed and predicted D_min."""
    return float(np.sqrt(np.mean((y - yhat) ** 2)))


def _aic(sse: float, m: int, k: int) -> float:
    """Akaike information criterion (AIC) from residual SSE (sum of squared errors).

    Idea: reward a small fit error, but pay a penalty for using more free
    parameters so a more flexible curve does not win only by over-fitting.

    Here: AIC = 2*k + m*log(SSE/m), with ``m`` points and ``k`` parameters
    (constant k=1, linear/power k=2, piecewise k=5). Lower is better.

    The ``+ 1e-12`` inside the log is only a numerical floor: if SSE is exactly
    zero (or tiny), plain log(SSE/m) would go to -inf. That can happen when a
    flexible fit (for example piecewise on a two-level step) matches the points
    almost perfectly. The floor keeps the log defined; it is not a modeling
    choice and does not change rankings in ordinary cases.

    Used as a secondary in-sample comparison (for example delta-AIC vs power).
    Primary ranking for RQ6 still uses leave-one-N-out RMSE.
    """
    return float(2 * k + m * np.log(sse / m + 1e-12))


def _bic(sse: float, m: int, k: int) -> float:
    """Bayesian information criterion (BIC) from residual SSE.

    Same idea as AIC (fit quality minus a complexity penalty), but the
    parameter penalty grows with log(m), so BIC is usually stricter about
    extra parameters when there are more data points.

    Here: BIC = k*log(m) + m*log(SSE/m). Lower is better.

    Uses the same ``+ 1e-12`` floor inside the log as AIC, so a near-perfect
    residual SSE cannot produce log(0).

    Also secondary to leave-one-N-out RMSE for choosing the RQ6 winner.
    """
    return float(k * np.log(max(m, 1)) + m * np.log(sse / m + 1e-12))


# Predictor used by leave-one-N CV: fit on (n_train, d_train), then predict D_min at n_i.
PredictFn = Callable[[np.ndarray, np.ndarray, float], float | None]


def _leave_one_n_rmse(
    n: np.ndarray,
    d: np.ndarray,
    predict_fn: PredictFn,
) -> float | None:
    """Leave-one-flock-size RMSE for one candidate curve family.

    Why: in-sample RMSE can look good just by matching noise. Holding out each N
    asks whether the curve still predicts D_min for a flock size it did not see.

    How:
    1. For each distinct held-out N, fit ``predict_fn`` on all other rows.
    2. Predict D_min for every held-out row at that N.
    3. Collect squared errors, then return sqrt(mean(...)).

    Returns None when there are fewer than 3 distinct N (CV would be unstable).
    """
    unique = np.unique(n)
    if len(unique) < 3:
        return None
    errs = []
    for held in unique:
        # Train on every row whose flock size is not ``held``.
        mask = n != held
        if int(mask.sum()) < 2:
            continue
        # Test rows: all observations at the held-out N (usually one frontier row).
        for n_i, d_i in zip(n[~mask], d[~mask]):
            yhat_i = predict_fn(n[mask], d[mask], float(n_i))
            if yhat_i is None or yhat_i != yhat_i:
                continue
            errs.append((float(d_i) - float(yhat_i)) ** 2)
    if not errs:
        return None
    return float(np.sqrt(np.mean(errs)))


def _fit_power_params(n: np.ndarray, d: np.ndarray) -> tuple[float, float, float] | None:
    """Fit D = A * N^alpha on positive rows.

    Starts from a log-log linear guess, then refines with least squares in D-space
    so power is scored in the same units as constant / linear / piecewise.

    Returns (A, alpha, log_log_slope). log_log_slope is the plain log-log fit slope
    (useful for C6b-style reporting); alpha is the refined power exponent.
    """
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
    """Fit a power law on the training rows, then predict D_min at ``n_i``."""
    if n_i <= 0:
        return None
    fitted = _fit_power_params(n_tr, d_tr)
    if fitted is None:
        return None
    amp, alpha, _ = fitted
    return float(amp * (n_i**alpha))


def _fit_piecewise(n: np.ndarray, d: np.ndarray) -> dict[str, Any] | None:
    """Two-segment linear fit with an automatically chosen breakpoint.

    Why: a single smooth curve can miss a step-shaped frontier (for example
    D_min = 2 on tiny N, then D_min = 1 for larger N). Two linear pieces can
    capture that change without assuming a power law.

    How:
    1. Sort points by N.
    2. Try every legal break index (at least two points on each side).
    3. Fit one line on the left of the break and one on the right.
    4. Keep the break with the smallest residual SSE.

    ``break_n`` is therefore data-driven (not a fixed constant in the code).
    On a flat two-level frontier the winning pieces are often nearly constant
    levels with a break between the last high-D_min N and the first low-D_min N.
    """
    m = len(d)
    if m < 4:
        return None
    order = np.argsort(n)
    n_s = n[order]
    d_s = d[order]
    best: dict[str, Any] | None = None
    # Break after index i: left = n_s[0 : i+1], right = n_s[i+1 :].
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
    # Map ordered predictions back to the original row order for RMSE.
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
    """Fit and compare candidate scaling models to D_min(N).

    Flow:
    1. Keep positive (N, D_min) rows from ``frontier``.
    2. Fit constant / linear / power / piecewise on the full set (in-sample metrics).
    3. Re-score each family with leave-one-N-out RMSE via the ``_pred_*`` helpers.
    4. Set ``best`` to the family with the lowest leave-one-N RMSE.
    5. Optionally fit the same pipeline per layout (``state_models``) and a
       separate-curves leave-one-N score for C6a.

    Candidates: constant, linear, power-law, piecewise. When ``state_col`` is
    present with multiple levels, also fit per-state models and a pooled
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

    # Constant: one shared D_min for every N.
    c = float(np.mean(d))
    yhat = np.full_like(d, c)
    sse = float(np.sum((d - yhat) ** 2))
    models["constant"] = {
        "params": {"c": c},
        "rmse": _rmse(d, yhat),
        "aic": _aic(sse, m, 1),
        "bic": _bic(sse, m, 1),
    }

    # Linear: D_min = a + b * N.
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

    # Power law: D_min = A * N^alpha, least squares in D (same space as the others).
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

    # CV predictors refit from scratch on each train fold (same families as above).
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
        # Use the fold's own auto-chosen break when predicting the held-out N.
        if float(n_i) <= as_float(params["break_n"]):
            return float(as_float(params["a1"]) + as_float(params["b1"]) * n_i)
        return float(as_float(params["a2"]) + as_float(params["b2"]) * n_i)

    # Leave-one-N RMSE per family; this is the primary ranking used for ``best``.
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
        # Fallback only if CV could not run (too few distinct N).
        best = min(models.items(), key=lambda kv: kv[1]["rmse"])[0]
    else:
        best = None

    # Optional: repeat the same fits inside each layout / state bucket.
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

    # Secondary comparison: how much better/worse each model is than power on AIC.
    delta_aic: dict[str, float] = {}
    if best and "power" in models:
        for name, payload in models.items():
            if name == "power":
                continue
            delta_aic[name] = float(payload["aic"] - models["power"]["aic"])

    # C6a: does piecewise, or separate per-layout curves, beat one shared power law?
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
    """Leave-one-N RMSE when each layout gets its own power law.

    For a held-out N, train a power law inside each layout on the other sizes,
    then predict that layout's D_min at the held-out N. Used as an alternative
    challenger to a single pooled power law in C6a.
    """
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
