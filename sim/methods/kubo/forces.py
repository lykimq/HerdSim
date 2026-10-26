"""Vectorized force calculations for the Kubo et al. 2022 herding model.

Computes sheep velocity components (repulsion, alignment, attraction, flee)
and dog velocity components (target approach, target standoff, goal repulsion,
and inter-dog repulsion).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.spatial.distance import cdist

# Floor on distances and speeds before dividing, so coincident agents give a large but
# finite force. Kept apart from vectors.EPS (1e-10), at which the 1/d^3 terms would reach 1e30.
FLOOR = 1e-6


def _weighted_offsets(positions: np.ndarray, others: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """sum_j w_ij (x_i - y_j) for every i, as matrix products: x_i sum_j w_ij - W y."""
    return positions * weights.sum(axis=1, keepdims=True) - weights @ others


def _per_count(total: np.ndarray, count: np.ndarray) -> np.ndarray:
    """Divide rows by their neighbour count; rows without neighbours become zero."""
    return np.where(count[:, None] > 0, total / np.maximum(count, 1)[:, None], 0.0)


def clamp_speed(velocities: np.ndarray, max_speed: float) -> np.ndarray:
    """Limit each velocity vector to ``max_speed``."""
    speeds = np.linalg.norm(velocities, axis=1, keepdims=True)
    return velocities * np.minimum(1.0, max_speed / np.maximum(speeds, FLOOR))


def sheep_velocities(
    positions: np.ndarray, velocities: np.ndarray, dogs: np.ndarray, config: dict[str, Any]
) -> np.ndarray:
    """Velocity of every sheep for one step, clamped to sheep_speed_max."""
    radius = float(config["sheep_radius"])
    dist = cdist(positions, positions)
    neighbours = (dist < radius) & (dist > 0.0)
    safe = np.maximum(dist, FLOOR)
    count = neighbours.sum(axis=1)
    a = _per_count(_weighted_offsets(positions, positions, neighbours / safe**2), count)
    c = -_per_count(_weighted_offsets(positions, positions, neighbours / safe), count)

    speeds = np.linalg.norm(velocities, axis=1)
    moving = speeds > 0.0
    headings = np.where(moving[:, None], velocities / np.maximum(speeds, FLOOR)[:, None], 0.0)
    aligned = neighbours & moving[None, :]
    b = _per_count(aligned.astype(float) @ headings, aligned.sum(axis=1))

    dog_dist = cdist(positions, dogs)
    seen = dog_dist < radius
    d = _per_count(
        _weighted_offsets(positions, dogs, seen / np.maximum(dog_dist, FLOOR) ** 3),
        seen.sum(axis=1),
    )

    u = (
        float(config["K_s1"]) * a
        + float(config["K_s2"]) * b
        + float(config["K_s3"]) * c
        + float(config["K_s4"]) * d
    )
    return clamp_speed(u, float(config["sheep_speed_max"]))


def dog_velocity(
    dog: np.ndarray,
    target: np.ndarray,
    goal: np.ndarray,
    other_dogs: np.ndarray,
    config: dict[str, Any],
) -> np.ndarray:
    """Calculate net velocity force vector for a single dog toward its assigned target."""
    to_target = dog - target
    d_t = max(float(np.linalg.norm(to_target)), FLOOR)
    to_goal = dog - goal
    d_g = max(float(np.linalg.norm(to_goal)), FLOOR)

    to_dogs = dog - other_dogs
    dist = np.linalg.norm(to_dogs, axis=1)
    near = dist < float(config["dog_repulsion_radius"])
    repulsion = (
        (to_dogs[near] / np.maximum(dist[near], FLOOR)[:, None] ** 3).mean(axis=0)
        if near.any()
        else np.zeros(2)
    )
    return (
        float(config["K_f1"]) * (-to_target / d_t)
        + float(config["K_f2"]) * (to_target / d_t**3)
        + float(config["K_f3"]) * (to_goal / d_g)
        + float(config["K_f4"]) * repulsion
    )


def reaction_radius(config: dict[str, Any]) -> float:
    """Distance at which a sheep reacts to a dog."""
    return float(config["sheep_radius"])
