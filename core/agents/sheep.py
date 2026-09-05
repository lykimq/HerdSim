"""Sheep agent flocking vector computations.

Provides pure functions that compute attraction, repulsion, and noise
vectors for sheep agents. No mutable state — operates on numpy arrays.
"""

from __future__ import annotations

import numpy as np


def compute_local_centroid(
    positions: np.ndarray, index: int, neighbour_radius: float
) -> np.ndarray:
    """Local centre of mass of neighbours within radius. Shape (2,)."""
    diffs = positions - positions[index]
    distances = np.linalg.norm(diffs, axis=1)
    mask = (distances < neighbour_radius) & (distances > 0)
    if not np.any(mask):
        return positions[index].copy()
    return np.mean(positions[mask], axis=0)


def compute_attraction(position: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    """Unit vector from sheep toward local centroid. Shape (2,)."""
    diff = centroid - position
    norm = np.linalg.norm(diff)
    if norm < 1e-10:
        return np.zeros(2)
    return diff / norm


def compute_repulsion_from_neighbours(
    positions: np.ndarray, index: int, repulsion_radius: float
) -> np.ndarray:
    """Sum of unit repulsion vectors from nearby sheep. Shape (2,)."""
    diffs = positions[index] - positions  # vectors AWAY from neighbours
    distances = np.linalg.norm(diffs, axis=1)
    mask = (distances < repulsion_radius) & (distances > 0)
    if not np.any(mask):
        return np.zeros(2)
    # Weight by inverse distance for stronger close-range repulsion
    weights = 1.0 / np.maximum(distances[mask], 1e-10)
    normed = diffs[mask] / np.maximum(distances[mask, np.newaxis], 1e-10)
    return np.sum(normed * weights[:, np.newaxis], axis=0)


def compute_repulsion_from_shepherds(
    sheep_pos: np.ndarray, shepherd_positions: np.ndarray, repulsion_radius: float
) -> np.ndarray:
    """Sum of unit repulsion vectors from nearby shepherds. Shape (2,)."""
    if shepherd_positions.shape[0] == 0:
        return np.zeros(2)
    diffs = sheep_pos - shepherd_positions  # vectors AWAY from shepherds
    distances = np.linalg.norm(diffs, axis=1)
    mask = distances < repulsion_radius
    if not np.any(mask):
        return np.zeros(2)
    normed = diffs[mask] / np.maximum(distances[mask, np.newaxis], 1e-10)
    return np.sum(normed, axis=0)


def compute_noise(rng: np.random.Generator, strength: float) -> np.ndarray:
    """Random perturbation vector. Shape (2,)."""
    angle = rng.uniform(0, 2 * np.pi)
    return strength * np.array([np.cos(angle), np.sin(angle)])
