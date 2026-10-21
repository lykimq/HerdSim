"""Flock shape metrics. Each takes a TickView and returns one float."""

from __future__ import annotations

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from .view import TickView


def cohesion(view: TickView) -> float:
    """Mean distance of sheep to the flock centroid."""
    return float(view.distances_to_centroid.mean())


def extent(view: TickView) -> float:
    """Radius of gyration: RMS distance of sheep to the flock centroid."""
    return float(np.sqrt(np.mean(view.distances_to_centroid**2)))


def aspect_ratio(view: TickView) -> float:
    """Long / short principal axis of the flock (1 = round).

    NaN with fewer than 3 sheep or when the short axis is zero (all sheep on
    one line or one point): zero means below float64 rounding of the long axis.
    """
    pts = view.state.sheep_positions
    if pts.shape[0] < 3:
        return float("nan")
    small, large = np.linalg.eigvalsh(np.cov(pts.T))
    if small <= np.finfo(float).eps * large:
        return float("nan")
    return float(np.sqrt(large / small))


def perimeter(view: TickView) -> float:
    """Length of the sheep convex hull boundary; grows when the flock stretches or splits."""
    return view.hull[0]


def hull_area(view: TickView) -> float:
    """Area of the sheep convex hull; a few stragglers inflate it, so read it with lost_sheep."""
    return view.hull[1]


def flock_density(view: TickView) -> float:
    """Sheep per unit hull area (NaN when the hull is flat)."""
    area = view.hull[1]
    return view.state.n_sheep / area if area > 0.0 else float("nan")


def fragmentation(view: TickView) -> float:
    """Largest group / N, where sheep within ``measurement_radius`` are linked."""
    n = view.state.n_sheep
    pairs = view.sheep_tree.query_pairs(
        float(view.config["measurement_radius"]), output_type="ndarray"
    )
    graph = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n))
    _, labels = connected_components(graph, directed=False)
    return float(np.bincount(labels).max()) / n


def lost_sheep(view: TickView) -> float:
    """Sheep farther than ``lost_radius`` from the flock centroid."""
    return float(np.sum(view.distances_to_centroid > float(view.config["lost_radius"])))


def min_separation(view: TickView) -> float:
    """Smallest distance between two sheep (NaN with one sheep)."""
    if view.state.n_sheep < 2:
        return float("nan")
    nearest, _ = view.sheep_tree.query(view.state.sheep_positions, k=2)
    return float(nearest[:, 1].min())
