"""Small vector helpers shared by the sheep models, dog controllers and metrics."""

from __future__ import annotations

import numpy as np

# Vectors shorter than this have no direction.
EPS = 1e-10


def unit(vec: np.ndarray) -> np.ndarray:
    """Unit vector of one 2-vector; zeros when it has no direction."""
    norm = float(np.linalg.norm(vec))
    if norm < EPS:
        return np.zeros(2)
    return vec / norm


def unit_rows(vecs: np.ndarray) -> np.ndarray:
    """Unit vector of every row of an (n, 2) array; zero rows stay zero."""
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    out = np.zeros_like(vecs, dtype=float)
    ok = norms[:, 0] >= EPS
    out[ok] = vecs[ok] / norms[ok]
    return out


def angle_vectors(angles: np.ndarray) -> np.ndarray:
    """Unit vectors for an array of angles in radians, shape (n, 2)."""
    return np.stack([np.cos(angles), np.sin(angles)], axis=-1)


def behind(point: np.ndarray, reference: np.ndarray, distance: float) -> np.ndarray:
    """Point ``distance`` past ``point`` on the ray from ``reference`` through ``point``."""
    return point + unit(point - reference) * distance


def farthest_from(points: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """The row of ``points`` farthest from ``reference``."""
    return points[int(np.argmax(np.linalg.norm(points - reference, axis=1)))]


def rotate(vec: np.ndarray, angle: float) -> np.ndarray:
    """Rotate a 2-vector counter-clockwise by ``angle`` radians."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c * vec[0] - s * vec[1], s * vec[0] + c * vec[1]])
