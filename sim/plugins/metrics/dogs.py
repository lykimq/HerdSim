"""Shepherd metrics. Each takes a state and returns one float."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState
from scipy.spatial.distance import pdist

# Shepherds slower than this are treated as stationary and excluded from I_dir.
_STATIONARY_SPEED = 1e-6


def shepherd_path(state: SimulationState) -> float:
    """Cumulative shepherd path length; the run loop keeps the running total."""
    return float(state.metadata["shepherd_path"])


def min_dog_separation(state: SimulationState) -> float:
    """Minimum pairwise distance between shepherds (stacking)."""
    if state.n_shepherds < 2:
        return float("inf")
    return float(np.min(pdist(state.shepherd_positions)))


def i_dir(state: SimulationState) -> float:
    """Directional conflict among moving shepherds.

    I_dir = 1 - ||sum u_i|| / M_active, where u_i are unit velocity directions of
    shepherds with speed above the stationary threshold. 0 means all moving
    shepherds agree in direction; 1 means maximal conflict.

    Caveat: uses realised (post-constraint) velocities, so wall reflections can
    inflate I_dir near boundaries.
    """
    vels = np.asarray(state.shepherd_velocities, dtype=float)
    if vels.size == 0:
        return 0.0
    speeds = np.linalg.norm(vels, axis=1)
    moving = speeds > _STATIONARY_SPEED
    m_active = int(moving.sum())
    if m_active == 0:
        return 0.0
    unit_vecs = vels[moving] / speeds[moving, np.newaxis]
    resultant = float(np.linalg.norm(unit_vecs.sum(axis=0)))
    return float(1.0 - resultant / m_active)


def coverage(state: SimulationState) -> float:
    """Fraction of peripheral sheep within at least one shepherd influence radius.

    Peripheral sheep are those farther from the flock centroid than the median
    sheep-centroid distance. Influence radius is ``influence_radius`` on
    state.metadata (the trial sensing range, else the method ``r_s``).
    """
    if state.n_sheep == 0 or state.n_shepherds == 0:
        return 0.0
    distances = state.distances_to_centroid()
    median = float(np.median(distances))
    peripheral = distances > median
    if not np.any(peripheral):
        # All sheep at the same distance (or single sheep): treat as covered
        # if any sheep is within range of a shepherd.
        peripheral = np.ones(state.n_sheep, dtype=bool)
    r_s = float(state.metadata["influence_radius"])
    if not np.isfinite(r_s):
        return float("nan")
    sheep = state.sheep_positions[peripheral]
    shepherds = state.shepherd_positions
    # Pairwise sheep-shepherd distances.
    diffs = sheep[:, np.newaxis, :] - shepherds[np.newaxis, :, :]
    dist = np.linalg.norm(diffs, axis=2)
    covered = np.any(dist <= r_s, axis=1)
    return float(np.mean(covered))
