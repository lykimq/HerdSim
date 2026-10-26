"""Strömböm sheep flock kinematics and state integration (`sheep_model=strombom`).

Integrates flock locomotion over discrete timestep dt:
- Resolves agent velocity from neighbor attraction, pairwise repulsion, shepherd evasion,
  heading inertia, and stochastic angular noise.
- Returns updated simulation state with new sheep positions and velocities.
"""

from __future__ import annotations

from typing import Any

from sim.core.simulation_state import SimulationState
from sim.methods.strombom import sheep
from sim.methods.strombom.config import resolve_n_neighbors


def prepare(config: dict[str, Any]) -> dict[str, Any]:
    """Derive runtime neighbor count `k_neighbors` based on flock size and configuration."""
    return {"k_neighbors": resolve_n_neighbors(config["n_neighbors"], int(config["n_sheep"]))}


def top_speed(config: dict[str, Any]) -> float:
    """Maximum sheep speed in distance units per second."""
    return float(config["sheep_speed"])


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    """Advance sheep positions and velocities by one timestep dt."""
    draws = sheep.draw(state.rng, state.n_sheep)
    velocities = sheep.velocities(
        state.sheep_positions,
        state.sheep_velocities,
        state.shepherd_positions,
        draws,
        config,
        int(config["k_neighbors"]),
    )
    return state.copy_with(
        sheep_positions=state.sheep_positions + float(config["dt"]) * velocities,
        sheep_velocities=velocities,
    )
