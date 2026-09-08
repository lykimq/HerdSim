"""Sheep flocking vector helpers (Strombom and shared topological tools)."""

from __future__ import annotations

import numpy as np


def unit_vector(vec: np.ndarray) -> np.ndarray:
    """Return unit vector, or zeros if near-zero length."""
    norm = np.linalg.norm(vec)
    if norm < 1e-10:
        return np.zeros(2)
    return vec / norm


def nearest_neighbor_indices(
    positions: np.ndarray, index: int, k: int
) -> np.ndarray:
    """Indices of up to k nearest other agents (topological neighbourhood)."""
    n = positions.shape[0]
    if n <= 1:
        return np.array([], dtype=int)
    k = min(int(k), n - 1)
    if k <= 0:
        return np.array([], dtype=int)
    distances = np.linalg.norm(positions - positions[index], axis=1)
    distances[index] = np.inf
    return np.argpartition(distances, k - 1)[:k]


def compute_local_centroid_knn(
    positions: np.ndarray, index: int, n_neighbors: int
) -> np.ndarray:
    """Local centre of mass of the n nearest neighbours (Strombom 2014).

    If n_neighbors < 0, uses all other agents (global case n = N-1).
    """
    n = positions.shape[0]
    if n <= 1:
        return positions[index].copy()
    k = n - 1 if n_neighbors < 0 else min(int(n_neighbors), n - 1)
    if k <= 0:
        return positions[index].copy()
    nearest = nearest_neighbor_indices(positions, index, k)
    return np.mean(positions[nearest], axis=0)


def compute_attraction(position: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    """Unit vector from sheep toward local centroid."""
    return unit_vector(centroid - position)


def compute_repulsion_from_neighbours(
    positions: np.ndarray, index: int, repulsion_radius: float
) -> np.ndarray:
    """Neighbour repulsion (Strombom 2014 eq. 4.1).

    R_a = sum_j (A_i - A_j) / |A_i - A_j| for neighbours within r_a
    (sum of unit vectors away from neighbours). Callers normalise and
    scale by weight ra when composing headings.
    """
    diffs = positions[index] - positions
    distances = np.linalg.norm(diffs, axis=1)
    mask = (distances < repulsion_radius) & (distances > 0)
    if not np.any(mask):
        return np.zeros(2)
    normed = diffs[mask] / np.maximum(distances[mask, np.newaxis], 1e-10)
    return np.sum(normed, axis=0)


def compute_repulsion_from_shepherds(
    sheep_pos: np.ndarray, shepherd_positions: np.ndarray, repulsion_radius: float
) -> np.ndarray:
    """Sum of unit repulsion vectors from shepherds within radius."""
    if shepherd_positions.shape[0] == 0:
        return np.zeros(2)
    diffs = sheep_pos - shepherd_positions
    distances = np.linalg.norm(diffs, axis=1)
    mask = distances < repulsion_radius
    if not np.any(mask):
        return np.zeros(2)
    normed = diffs[mask] / np.maximum(distances[mask, np.newaxis], 1e-10)
    return np.sum(normed, axis=0)


def compute_noise(rng: np.random.Generator, strength: float) -> np.ndarray:
    """Angular noise e * e_hat."""
    angle = rng.uniform(0, 2 * np.pi)
    return strength * np.array([np.cos(angle), np.sin(angle)])


def compose_strombom_heading(
    prev_velocity: np.ndarray,
    attraction: np.ndarray,
    repulsion_sheep: np.ndarray,
    repulsion_shepherd: np.ndarray,
    noise: np.ndarray,
    *,
    inertia: float,
    c: float,
    ra_weight: float,
    rs_weight: float,
) -> np.ndarray:
    """Strombom eq. (4.2): H' = h H_hat + c C_hat + ra Ra_hat + rs Rs_hat + e e_hat."""
    heading = (
        inertia * unit_vector(prev_velocity)
        + c * unit_vector(attraction)
        + ra_weight * unit_vector(repulsion_sheep)
        + rs_weight * unit_vector(repulsion_shepherd)
        + noise
    )
    return unit_vector(heading)
