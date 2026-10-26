"""Dog metrics. Each takes a TickView and returns one float."""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import squareform

from .view import TickView

# Dogs slower than this count as stopped.
STOPPED_SPEED = 1e-9


def shepherd_path(view: TickView) -> float:
    """Total distance the dogs' controllers walked so far: the sum of |v| dt of the
    commanded velocities."""
    return float(view.state.metadata["shepherd_path"])


def min_dog_separation(view: TickView) -> float:
    """Smallest distance between two dogs (NaN with one dog)."""
    pairs = view.dog_pair_distances
    return float(pairs.min()) if pairs.size else float("nan")


def dog_overlap(view: TickView) -> float:
    """Fraction of dogs with another dog closer than ``dog_overlap_distance``: dogs doing
    the same work as a twin. 0 with one dog, NaN without dogs."""
    n = view.state.n_shepherds
    if n == 0:
        return float("nan")
    if n == 1:
        return 0.0
    close = squareform(view.dog_pair_distances) < float(view.config["dog_overlap_distance"])
    np.fill_diagonal(close, False)
    return float(close.any(axis=1).mean())


def dogs_stopped(view: TickView) -> float:
    """Fraction of dogs whose commanded velocity is zero this tick, e.g. under the stop
    rule (NaN without dogs). A dog held by the stop rule but moved apart by ``dog_spacing``
    counts as moving."""
    if view.state.n_shepherds == 0:
        return float("nan")
    return float(np.mean(view.dog_speeds < STOPPED_SPEED))


def i_dir(view: TickView) -> float:
    """Directional conflict among moving dogs: 1 - |sum of unit headings| / moving dogs.

    Headings are the commanded velocities. 0 when no dog moves. Clamped to [0, 1]: parallel
    headings can sum to a length one rounding error above the count.
    """
    speeds = view.dog_speeds
    moving = speeds > STOPPED_SPEED
    if not moving.any():
        return 0.0
    headings = view.state.shepherd_velocities[moving] / speeds[moving, None]
    return float(np.clip(1.0 - np.linalg.norm(headings.sum(axis=0)) / moving.sum(), 0.0, 1.0))


def coverage(view: TickView) -> float:
    """Fraction of outer sheep (beyond the median centroid distance) within a dog's reach.

    Reach is the sheep model's reaction radius: a sheep closer than it to a dog
    responds (strictly closer, as in the sheep models). NaN without dogs.
    """
    state = view.state
    if state.n_shepherds == 0:
        return float("nan")
    dist = view.distances_to_centroid
    outer = dist > np.median(dist)
    if not outer.any():
        outer = np.ones(state.n_sheep, dtype=bool)
    reach = float(view.config["reaction_radius"])
    to_dogs = state.sheep_positions[outer][:, None, :] - state.shepherd_positions[None, :, :]
    return float(np.mean((np.linalg.norm(to_dogs, axis=2) < reach).any(axis=1)))


def collect_mode(view: TickView) -> float:
    """Returns 1.0 if any sheep is outside the collection boundary f(N) = r_a * N^(2/3),
    indicating that the flock requires active outlier gathering, and 0.0 otherwise.

    When averaged over trial history, this yields the fraction of time spent in
    the gathering/collecting phase versus the cohesive driving phase.
    """
    r_a = float(view.config.get("r_a", 2.0))
    n_sheep = int(view.config.get("n_sheep", view.state.n_sheep))
    threshold = r_a * (float(n_sheep) ** (2.0 / 3.0))
    return float(np.any(view.distances_to_centroid > threshold))

