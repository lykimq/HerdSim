"""Sheep and dog interaction helpers for Flocking Dog 2024.

Jadhav et al., Communications Biology 2024 Methods / Fig. 7
and authors' MATLAB `herding_model.m`.
"""

from __future__ import annotations

import numpy as np

from core.agents.sheep import nearest_neighbor_indices, unit_vector

__all__ = [
    "nearest_neighbor_indices",
    "sheep_repulsion",
    "random_attraction",
    "random_alignment",
    "dog_repulsion_unit",
]


def sheep_repulsion(
    positions: np.ndarray, index: int, radius: float
) -> np.ndarray:
    """Unit repulsion away from neighbours within radius (normalised sum)."""
    diffs = positions - positions[index]
    dist = np.linalg.norm(diffs, axis=1)
    mask = (dist < radius) & (dist > 0)
    if not np.any(mask):
        return np.zeros(2)
    # Toward neighbours then flip (MATLAB -sum((rj-ri)/|rj-ri|)).
    toward = diffs[mask] / dist[mask, None]
    return -unit_vector(np.sum(toward, axis=0))


def random_attraction(
    positions: np.ndarray,
    index: int,
    neighbor_idx: np.ndarray,
    n_attraction: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Unit attraction toward a random subset of topological neighbours."""
    if neighbor_idx.size == 0:
        return np.zeros(2), neighbor_idx
    n_pick = min(n_attraction, neighbor_idx.size)
    chosen = rng.choice(neighbor_idx, size=n_pick, replace=False)
    diffs = positions[chosen] - positions[index]
    dist = np.linalg.norm(diffs, axis=1)
    safe = np.maximum(dist, 1e-10)
    atr = np.sum(diffs / safe[:, None], axis=0)
    return unit_vector(atr), chosen


def random_alignment(
    velocities: np.ndarray,
    candidate_idx: np.ndarray,
    n_alignment: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Unit mean heading of a random alignment subset."""
    if candidate_idx.size == 0:
        return np.zeros(2)
    n_pick = min(n_alignment, candidate_idx.size)
    chosen = rng.choice(candidate_idx, size=n_pick, replace=False)
    return unit_vector(np.sum(velocities[chosen], axis=0))


def dog_repulsion_unit(sheep_pos: np.ndarray, dog_pos: np.ndarray) -> np.ndarray:
    """Unit vector away from the dog."""
    return unit_vector(sheep_pos - dog_pos)
