"""Reciprocal interaction helpers for Flocking Dog dynamics."""

from __future__ import annotations

import numpy as np


def unit(vec: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(vec)
    if n < 1e-10:
        return np.zeros(2)
    return vec / n


def alignment_force(positions: np.ndarray, velocities: np.ndarray, index: int, radius: float) -> np.ndarray:
    diffs = positions - positions[index]
    dist = np.linalg.norm(diffs, axis=1)
    mask = (dist < radius) & (dist > 0)
    if not np.any(mask):
        return np.zeros(2)
    speeds = np.linalg.norm(velocities[mask], axis=1)
    valid = speeds > 1e-10
    if not np.any(valid):
        return np.zeros(2)
    return np.mean(velocities[mask][valid] / speeds[valid, None], axis=0)


def front_biased_dog_coupling(
    sheep_pos: np.ndarray,
    sheep_vel: np.ndarray,
    dog_pos: np.ndarray,
    radius: float,
    front_bias: float,
) -> np.ndarray:
    """Attraction/alignment toward dog stronger for sheep in front of flock motion."""
    to_dog = dog_pos - sheep_pos
    dist = np.linalg.norm(to_dog)
    if dist > radius or dist < 1e-10:
        return np.zeros(2)
    heading = unit(sheep_vel)
    facing = float(np.dot(heading, unit(to_dog))) if np.linalg.norm(heading) > 0 else 0.0
    weight = 1.0 + front_bias * max(facing, 0.0)
    return weight * unit(to_dog)
