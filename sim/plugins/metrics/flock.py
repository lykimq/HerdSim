"""Flock shape and spacing metrics. Each takes a state and returns one float."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial.distance import pdist, squareform

from .hull_geometry import aspect_ratio_of_points, hull_geometry, sheep_per_area


def cohesion(state: SimulationState) -> float:
    """Mean distance of sheep to the flock centroid (GCM), in world units."""
    if state.n_sheep == 0:
        return 0.0
    return float(state.distances_to_centroid().mean())


def polarization(state: SimulationState) -> float:
    """Mean alignment of sheep velocity unit vectors (0 = disordered, 1 = aligned)."""
    if state.n_sheep == 0:
        return 0.0
    speeds = np.linalg.norm(state.sheep_velocities, axis=1, keepdims=True)
    # Avoid division by zero for stationary sheep
    moving = speeds.flatten() > 1e-10
    if not np.any(moving):
        return 0.0
    unit_vecs = state.sheep_velocities[moving] / speeds[moving]
    mean_vec = np.mean(unit_vecs, axis=0)
    return float(np.linalg.norm(mean_vec))


def outlier_count(state: SimulationState) -> float:
    """Sheep farther from the GCM than f(N) = r_a * N^(2/3).

    Same formula for every algorithm so spread stays comparable. For Collect /
    Drive controllers this matches the mode switch; for others (e.g. Kubo) it
    is only a report score. Not sheep outside the goal.
    """
    if state.n_sheep == 0:
        return 0.0
    threshold = float(state.metadata["r_a"]) * (state.n_sheep ** (2.0 / 3.0))
    return float(np.sum(state.distances_to_centroid() > threshold))


def min_separation(state: SimulationState) -> float:
    """Minimum pairwise distance between any two sheep (collision risk)."""
    if state.n_sheep < 2:
        return 0.0
    return float(np.min(pdist(state.sheep_positions)))


def largest_component_fraction(positions: np.ndarray, radius: float) -> float:
    """Fraction of agents in the largest component (edges if distance <= radius)."""
    n = int(positions.shape[0])
    if n == 0:
        return 0.0
    if n == 1:
        return 1.0
    if radius <= 0.0:
        return 1.0 / float(n)

    # Connected components of the graph with edges where distance <= radius.
    adjacency = squareform(pdist(positions)) <= radius
    _, labels = connected_components(csr_matrix(adjacency), directed=False)
    return float(np.bincount(labels).max()) / float(n)


def fragmentation(state: SimulationState) -> float:
    """Largest connected-component size / N under the protocol measurement_radius.

    measurement_radius is an experiment parameter, not an algorithm interaction
    radius such as Kubo radius or Strombom r_a.
    """
    if state.n_sheep == 0:
        return 0.0
    radius = float(state.metadata["measurement_radius"])
    return largest_component_fraction(state.sheep_positions, radius)


def mean_spread(state: SimulationState) -> float:
    """Variance of sheep distances to the GCM (draft mean-spread)."""
    if state.n_sheep < 2:
        return 0.0
    return float(np.var(state.distances_to_centroid()))


def extent(state: SimulationState) -> float:
    """Radius of gyration: RMS distance of sheep to the GCM."""
    if state.n_sheep == 0:
        return 0.0
    distances = state.distances_to_centroid()
    return float(np.sqrt(np.mean(distances**2)))


def perimeter(state: SimulationState) -> float:
    """Length of the sheep convex hull boundary."""
    return hull_geometry(state.sheep_positions).perimeter


def hull_area(state: SimulationState) -> float:
    """Area enclosed by the sheep convex hull."""
    return hull_geometry(state.sheep_positions).area


def flock_density(state: SimulationState) -> float:
    """N / hull area. Zero when the hull area is degenerate."""
    return sheep_per_area(state.n_sheep, hull_geometry(state.sheep_positions).area)


def aspect_ratio(state: SimulationState) -> float:
    """Largest / smallest PCA axis of the sheep cloud (1.0 = isotropic)."""
    return aspect_ratio_of_points(state.sheep_positions)
