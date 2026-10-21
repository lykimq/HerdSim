"""Helpers shared by dog controllers."""

from __future__ import annotations

import numpy as np

from sim.core.simulation_state import SimulationState


def move_dogs(state: SimulationState, velocities: np.ndarray, dt: float) -> SimulationState:
    """Advance every dog by ``dt * velocity`` and store the velocities."""
    return state.copy_with(
        shepherd_positions=state.shepherd_positions + dt * velocities,
        shepherd_velocities=velocities,
    )


def noise_angles(state: SimulationState) -> np.ndarray:
    """One heading-noise angle per dog, drawn once per tick in dog order from the dogs' stream."""
    return state.dog_rng.uniform(0.0, 2.0 * np.pi, state.n_shepherds)
