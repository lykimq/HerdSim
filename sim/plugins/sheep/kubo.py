"""Kubo sheep (sheep_model=kubo): one integration step of the paper forces."""

from __future__ import annotations

from typing import Any

from sim.core.simulation_state import SimulationState
from sim.methods.kubo.forces import sheep_velocities


def prepare(_config: dict[str, Any]) -> dict[str, Any]:
    """No model-specific checks or derived keys."""
    return {}


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    velocities = sheep_velocities(
        state.sheep_positions, state.sheep_velocities, state.shepherd_positions, config
    )
    return state.copy_with(
        sheep_positions=state.sheep_positions + float(config["dt"]) * velocities,
        sheep_velocities=velocities,
    )
