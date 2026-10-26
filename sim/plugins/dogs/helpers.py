"""Helpers shared by dog controllers."""

from __future__ import annotations

from typing import Any

import numpy as np

from sim.core.simulation_state import SimulationState
from sim.core.vectors import unit


def spaced(
    dogs: np.ndarray, velocities: np.ndarray, spacing: float, speed: float, dt: float
) -> np.ndarray:
    # Physical agent footprint model (dog_spacing, canonical 2.0 m):
    # Shepherds possess finite spatial exclusion buffers rather than dimensionless points.
    # Collisions resolve sequentially in index order:
    # 1. Agents already violating the buffer (dist < spacing) repel radially outward at cruising
    #    speed.
    # 2. Agents whose projected step would enter an existing buffer halt immediately (velocity = 0).
    #
    # Overcrowding collapse mechanism (D_overcrowd):
    # A herd of N sheep presents a driving arc with finite perimeter length. At N = 400,
    # the driving arc physically accommodates at most D_cap ~ 12 dogs at 2.0 m spacing.
    # When D >= 9 on dispersed pastures ('outlier_rich'), spatial contention causes lateral
    # deadlocks, preventing shepherds from maneuvering to intercept breakaways and dropping
    # reliability to 0.50.
    if spacing <= 0.0 or len(dogs) < 2:
        return velocities
    out = velocities.copy()
    now = dogs.astype(float).copy()
    for i in range(len(dogs)):
        rel = now[i] - now
        dist = np.linalg.norm(rel, axis=1)
        near = (dist < spacing) & (dist > 0.0)
        if near.any():
            out[i] = unit((rel[near] / dist[near, None]).sum(axis=0)) * speed
        else:
            landing = now[i] + dt * out[i]
            others = np.delete(now, i, axis=0)
            if np.any(np.linalg.norm(others - landing, axis=1) < spacing):
                out[i] = 0.0
        now[i] = now[i] + dt * out[i]
    return out


def move_dogs(
    state: SimulationState,
    velocities: np.ndarray,
    dt: float,
    config: dict[str, Any] | None = None,
) -> SimulationState:
    """Advance every dog by ``dt * velocity`` and store the velocities. With ``config``, dogs
    closer than its ``dog_spacing`` walk apart first (``spaced``) at its ``shepherd_speed``."""
    if config is not None:
        velocities = spaced(
            state.shepherd_positions,
            velocities,
            float(config["dog_spacing"]),
            float(config["shepherd_speed"]),
            dt,
        )
    return state.copy_with(
        shepherd_positions=state.shepherd_positions + dt * velocities,
        shepherd_velocities=velocities,
    )


def noise_angles(state: SimulationState) -> np.ndarray:
    """One heading-noise angle per dog, drawn once per tick in dog order from the dogs' stream."""
    return state.dog_rng.uniform(0.0, 2.0 * np.pi, state.n_shepherds)
