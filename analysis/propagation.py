"""Information-propagation proxies from trajectory arrays."""

from __future__ import annotations

import numpy as np


def velocity_correlation_delay(
    velocities: np.ndarray,
    max_lag: int = 10,
) -> dict[str, float]:
    """Estimate mean pairwise velocity correlation peak lag.

    velocities: shape (T, N, 2)
    """
    if velocities.ndim != 3 or velocities.shape[0] < 3:
        return {"peak_lag": float("nan"), "peak_corr": float("nan")}
    t, n, _ = velocities.shape
    if n < 2:
        return {"peak_lag": float("nan"), "peak_corr": float("nan")}
    best_lag = 0
    best_corr = -1.0
    for lag in range(0, min(max_lag, t - 1) + 1):
        corrs = []
        for i in range(n):
            for j in range(i + 1, n):
                a = velocities[: t - lag, i]
                b = velocities[lag:, j]
                if len(a) < 2:
                    continue
                a_u = a / np.maximum(np.linalg.norm(a, axis=1, keepdims=True), 1e-9)
                b_u = b / np.maximum(np.linalg.norm(b, axis=1, keepdims=True), 1e-9)
                corrs.append(float(np.mean(np.sum(a_u * b_u, axis=1))))
        if corrs:
            m = float(np.mean(corrs))
            if m > best_corr:
                best_corr = m
                best_lag = lag
    return {"peak_lag": float(best_lag), "peak_corr": float(best_corr)}
