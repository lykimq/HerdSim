"""Which shape D_min(N) follows: a power law that grows without limit, or a curve that levels off.

    uv run cli/dmin_tables.py fits dmin_f99_m12 dmin_f99_m6

The answer decides what a larger flock would need: a power law keeps adding dogs, a saturating
curve stops. Up to N = 566 both fit the data equally well, and this module says how far apart
their predictions lie beyond it.

Each D curve gives D_min at every N only as an interval, because D is an integer and some cells
stay undecided: a decided D_min d says the true value lies in [d - 0.5, d + 0.5], a bracket
lo-hi in [lo - 0.5, hi + 0.5], and a curve with no reliable D yet (a lower bound lo, or no D on
the grid) in [lo - 0.5, infinity). Two curves with two parameters each are fitted to these
intervals by maximum likelihood, with a log-normal scatter sigma around the curve:

- power law: D(N) = max(1, c N^b), which grows without limit for b > 0;
- saturating: D(N) = 1 + (D_inf - 1) N / (N + K), which starts at 1 and levels off at D_inf.

Both have three free numbers (two shape parameters and sigma), so their log likelihoods compare
directly: the likelihood ratio exp(logL_a - logL_b) is the odds of one shape against the other on
these data. With five to nine flock sizes the odds are weak evidence and are reported as such.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

Interval = tuple[float, float]  # (low, high) of the true D_min; high may be math.inf


def interval_of(d_min: float | None, d_min_low: float | None) -> Interval | None:
    """The interval a curve gives at one N, from its d_min and d_min_low (NaN as None)."""
    if d_min is not None and not math.isnan(d_min):
        low = d_min_low if d_min_low is not None and not math.isnan(d_min_low) else d_min
        return min(low, d_min) - 0.5, d_min + 0.5
    if d_min_low is not None and not math.isnan(d_min_low):
        return d_min_low - 0.5, math.inf
    return None


def power_law(n: np.ndarray, p: np.ndarray) -> np.ndarray:
    log_c, b = p
    return np.maximum(1.0, np.exp(log_c) * n**b)


def saturating(n: np.ndarray, p: np.ndarray) -> np.ndarray:
    log_extra, log_k = p  # D_inf = 1 + exp(log_extra), K = exp(log_k)
    return 1.0 + np.exp(log_extra) * n / (n + np.exp(log_k))


SHAPES = {"power law": power_law, "saturating": saturating}
STARTS = {
    "power law": [np.array([math.log(0.2), 0.4]), np.array([math.log(0.02), 0.8])],
    "saturating": [np.array([math.log(3.0), math.log(200.0)]), np.array([0.0, math.log(30.0)])],
}


@dataclass(frozen=True)
class Fit:
    shape: str
    params: tuple[float, ...]
    sigma: float
    log_likelihood: float


def log_likelihood(low: np.ndarray, high: np.ndarray, d: np.ndarray, sigma: float):
    """Sum over the points of log P(low <= D_true < high) with log D_true ~ N(log d, sigma)."""
    lo = norm.cdf((np.log(np.maximum(low, 1e-9)) - np.log(d)) / sigma)
    hi = np.where(np.isinf(high), 1.0, norm.cdf((np.log(high) - np.log(d)) / sigma))
    return float(np.sum(np.log(np.maximum(hi - lo, 1e-300))))


def fit(points: list[tuple[int, Interval]], shape: str) -> Fit:
    """Maximum-likelihood fit of one shape to (N, interval) points."""
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


# Parameter grids of the two shapes, wide enough to hold every curve with D from 1 to about 50
# over N = 25 to 3200: (log c, b) for the power law, (log(D_inf - 1), log K) for the other.
GRIDS = {
    "power law": (np.linspace(math.log(0.002), math.log(3.0), 240), np.linspace(0.0, 1.5, 240)),
    "saturating": (np.linspace(math.log(0.01), math.log(100.0), 240), np.linspace(0.0, 11.5, 240)),
}


def consistent_range(
    points: list[tuple[int, Interval]], shape: str, size: int
) -> tuple[float, float]:
    """Smallest and largest D at ``size`` over every curve of ``shape`` on its grid that passes
    through all the intervals; (nan, nan) when none does."""
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
    """Both fits, the odds of the power law against the saturating curve, and the range each
    shape allows at the sizes ``ahead``. Where both shapes pass through every interval, the data
    cannot tell them apart (odds 1); the ranges then say at which N a run could, which is where
    they no longer overlap."""
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
