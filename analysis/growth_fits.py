"""Model comparison for D_min(N) scaling: power-law vs saturating growth.

Fits candidate scaling relationships to interval-censored D_min data:
- Power-law model: D(N) = max(1, c * N^b), representing unbounded team growth for b > 0.
- Saturating model: D(N) = 1 + (D_inf - 1) * N / (N + K), leveling off asymptotically at D_inf.

Because empirical D_min values are integer bounds or brackets [lo, hi], parameters are
estimated via maximum likelihood assuming log-normal observation error around the curve.
Model evidence is compared via log-likelihood ratios.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

Interval = tuple[float, float]  # (low, high) of true D_min; high may be math.inf


def interval_of(d_min: float | None, d_min_low: float | None) -> Interval | None:
    """Converts a point estimate and lower bound into an interval [low, high]."""
    if d_min is not None and not math.isnan(d_min):
        low = d_min_low if d_min_low is not None and not math.isnan(d_min_low) else d_min
        return min(low, d_min) - 0.5, d_min + 0.5
    if d_min_low is not None and not math.isnan(d_min_low):
        return d_min_low - 0.5, math.inf
    return None


def power_law(n: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Evaluates the power-law model D(N) = max(1, c * N^b)."""
    log_c, b = p
    return np.maximum(1.0, np.exp(log_c) * n**b)


def saturating(n: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Evaluates the saturating model D(N) = 1 + (D_inf - 1) * N / (N + K)."""
    log_extra, log_k = p  # D_inf = 1 + exp(log_extra), K = exp(log_k)
    return 1.0 + np.exp(log_extra) * n / (n + np.exp(log_k))


SHAPES = {"power law": power_law, "saturating": saturating}
STARTS = {
    "power law": [np.array([math.log(0.2), 0.4]), np.array([math.log(0.02), 0.8])],
    "saturating": [np.array([math.log(3.0), math.log(200.0)]), np.array([0.0, math.log(30.0)])],
}


@dataclass(frozen=True)
class Fit:
    """Maximum-likelihood fit parameters and statistics for a scaling shape."""

    shape: str
    params: tuple[float, ...]
    sigma: float
    log_likelihood: float


def log_likelihood(low: np.ndarray, high: np.ndarray, d: np.ndarray, sigma: float) -> float:
    """Computes the interval log-likelihood under log-normal scatter sigma around curve d."""
    lo = norm.cdf((np.log(np.maximum(low, 1e-9)) - np.log(d)) / sigma)
    hi = np.where(np.isinf(high), 1.0, norm.cdf((np.log(high) - np.log(d)) / sigma))
    return float(np.sum(np.log(np.maximum(hi - lo, 1e-300))))


def fit(points: list[tuple[int, Interval]], shape: str) -> Fit:
    """Fits a scaling curve to interval-censored (N, [low, high]) points via maximum likelihood."""
    n = np.array([p[0] for p in points], dtype=float)
    low = np.array([p[1][0] for p in points])
    high = np.array([p[1][1] for p in points])
    curve = SHAPES[shape]

    def cost(x: np.ndarray) -> float:
        return -log_likelihood(low, high, curve(n, x[:2]), math.exp(x[2]))

    best = None
    for start in STARTS[shape]:
        for log_sigma in (math.log(0.1), math.log(0.4)):
            result = minimize(
                cost,
                np.append(start, log_sigma),
                method="Nelder-Mead",
                options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-9},
            )
            if best is None or result.fun < best.fun:
                best = result
    assert best is not None
    return Fit(shape, tuple(float(v) for v in best.x[:2]), math.exp(best.x[2]), -float(best.fun))


# Parameter grids of the two shapes across N = 25 to 3200:
# (log c, b) for power law, (log(D_inf - 1), log K) for saturating.
GRIDS = {
    "power law": (np.linspace(math.log(0.002), math.log(3.0), 240), np.linspace(0.0, 1.5, 240)),
    "saturating": (np.linspace(math.log(0.01), math.log(100.0), 240), np.linspace(0.0, 11.5, 240)),
}


def consistent_range(
    points: list[tuple[int, Interval]], shape: str, size: int
) -> tuple[float, float]:
    """Finds the min and max predicted D at ``size`` across curves passing through all intervals."""
    n = np.array([p[0] for p in points], dtype=float)
    low = np.array([p[1][0] for p in points])
    high = np.array([p[1][1] for p in points])
    grid = np.array(np.meshgrid(*GRIDS[shape], indexing="ij")).reshape(2, -1)
    curve = SHAPES[shape]
    d = curve(n[:, None], grid[:, None, :])  # (points, grid)
    inside = np.all((d >= low[:, None]) & (d < high[:, None]), axis=0)
    if not inside.any():
        return math.nan, math.nan
    ahead = curve(np.array([float(size)]), grid[:, inside])
    return float(ahead.min()), float(ahead.max())


def compare(
    points: list[tuple[int, Interval]], ahead: tuple[int, ...] = (1600, 3200)
) -> dict[str, object]:
    """Compares power-law and saturating fits, log-odds, and projected prediction ranges."""
    fits = {shape: fit(points, shape) for shape in SHAPES}
    ratio = fits["power law"].log_likelihood - fits["saturating"].log_likelihood
    power, sat = fits["power law"].params, fits["saturating"].params
    out: dict[str, object] = {
        "points": len(points),
        "exponent_b": round(power[1], 2),
        "d_inf": round(1.0 + math.exp(sat[0]), 1),
        "log_odds_power_vs_saturating": round(ratio, 2),
    }
    for n in ahead:
        g = consistent_range(points, "power law", n)
        v = consistent_range(points, "saturating", n)
        out[f"N={n}: power / saturating"] = f"{g[0]:.1f}-{g[1]:.1f} / {v[0]:.1f}-{v[1]:.1f}"
    return out

