"""Shared convex-hull geometry for flock shape metrics.

Returns perimeter, area, and aspect ratio from sheep positions. Metrics call
these helpers so hull math is not duplicated across plugins.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial import ConvexHull, QhullError


_EPS = 1e-12


@dataclass(frozen=True)
class HullGeometry:
    """Flock hull scalars in world units (aspect_ratio is dimensionless)."""

    perimeter: float
    area: float
    aspect_ratio: float


def aspect_ratio_of_points(positions: np.ndarray) -> float:
    """PCA axis ratio (largest / smallest std). 1.0 if isotropic or N < 2."""
    pts = np.asarray(positions, dtype=float)
    n = int(pts.shape[0])
    if n < 2:
        return 1.0
    centered = pts - pts.mean(axis=0, keepdims=True)
    # 2x2 covariance; eigvalsh is ascending.
    cov = (centered.T @ centered) / float(max(n - 1, 1))
    evals = np.linalg.eigvalsh(cov)
    lo = float(max(evals[0], 0.0))
    hi = float(max(evals[-1], 0.0))
    if hi < _EPS:
        return 1.0
    if lo < _EPS:
        # Degenerate to a line: treat as highly elongated but finite.
        return float(np.sqrt(hi / _EPS))
    return float(np.sqrt(hi / lo))


def _segment_perimeter(positions: np.ndarray) -> float:
    """Twice the diameter along the principal axis (flat / collinear flock)."""
    pts = np.asarray(positions, dtype=float)
    if pts.shape[0] < 2:
        return 0.0
    # Max pairwise distance among endpoints of the diameter is enough for N=2;
    # for collinear N>=3 use projected span on the first PCA axis.
    centered = pts - pts.mean(axis=0, keepdims=True)
    cov = (centered.T @ centered) / float(max(pts.shape[0] - 1, 1))
    evals, evecs = np.linalg.eigh(cov)
    axis = evecs[:, int(np.argmax(evals))]
    proj = centered @ axis
    span = float(proj.max() - proj.min())
    return 2.0 * span


def hull_geometry(positions: np.ndarray) -> HullGeometry:
    """Convex-hull perimeter and area, plus PCA aspect ratio.

    N == 0 or 1: perimeter 0, area 0, aspect 1.
    N == 2 or collinear: perimeter = 2 * span, area 0, aspect from PCA.
    """
    pts = np.asarray(positions, dtype=float)
    n = int(pts.shape[0])
    aspect = aspect_ratio_of_points(pts)
    if n == 0 or n == 1:
        return HullGeometry(perimeter=0.0, area=0.0, aspect_ratio=aspect)
    if n == 2:
        return HullGeometry(
            perimeter=_segment_perimeter(pts),
            area=0.0,
            aspect_ratio=aspect,
        )
    try:
        hull = ConvexHull(pts)
    except QhullError:
        return HullGeometry(
            perimeter=_segment_perimeter(pts),
            area=0.0,
            aspect_ratio=aspect,
        )
    return HullGeometry(
        perimeter=float(hull.area),  # in 2D, SciPy stores perimeter in .area
        area=float(hull.volume),  # in 2D, SciPy stores area in .volume
        aspect_ratio=aspect,
    )


def flock_density(n_sheep: int, area: float) -> float:
    """Sheep per unit hull area; 0 when area is degenerate."""
    if n_sheep <= 0 or area <= _EPS:
        return 0.0
    return float(n_sheep) / float(area)
