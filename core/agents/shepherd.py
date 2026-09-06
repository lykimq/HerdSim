"""Shepherd positioning helpers (Collect/Drive stand-off geometry)."""

from __future__ import annotations

import numpy as np


def move_toward(
    current_pos: np.ndarray, target_pos: np.ndarray, speed: float
) -> np.ndarray:
    """Velocity from current toward target at most `speed` (zeros if at target)."""
    diff = target_pos - current_pos
    dist = np.linalg.norm(diff)
    if dist < 1e-10:
        return np.zeros(2)
    return (diff / dist) * min(speed, dist)


def position_behind_target(
    target_pos: np.ndarray, reference_pos: np.ndarray, offset_distance: float
) -> np.ndarray:
    """Point beyond `target_pos` on the ray from `reference_pos` through target.

    Collect: behind furthest sheep relative to centroid.
    Drive: behind centroid relative to goal.
    """
    direction = target_pos - reference_pos
    norm = np.linalg.norm(direction)
    if norm < 1e-10:
        return target_pos.copy()
    unit = direction / norm
    return target_pos + unit * offset_distance
