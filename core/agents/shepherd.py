"""Shepherd agent utility functions.

Provides pure functions for shepherd positioning and movement.
No mutable state — operates on numpy arrays.
"""

from __future__ import annotations

import numpy as np


def move_toward(
    current_pos: np.ndarray, target_pos: np.ndarray, speed: float
) -> np.ndarray:
    """Compute velocity vector moving from current toward target at given speed.

    Returns velocity vector (2,). If already at target, returns zeros.
    """
    diff = target_pos - current_pos
    dist = np.linalg.norm(diff)
    if dist < 1e-10:
        return np.zeros(2)
    return (diff / dist) * min(speed, dist)


def position_behind_target(
    target_pos: np.ndarray, reference_pos: np.ndarray, offset_distance: float
) -> np.ndarray:
    """Compute a position that is behind `target_pos` relative to `reference_pos`.

    Used for both collecting (behind furthest sheep relative to centroid)
    and driving (behind centroid relative to goal).

    Returns position (2,) that is offset_distance beyond target_pos,
    on the line from reference_pos through target_pos.
    """
    direction = target_pos - reference_pos
    norm = np.linalg.norm(direction)
    if norm < 1e-10:
        return target_pos.copy()
    unit = direction / norm
    return target_pos + unit * offset_distance
