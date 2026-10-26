"""Strombom sheep (sheep_model=strombom): one tick of the paper heading."""

from __future__ import annotations

from typing import Any

from sim.core.simulation_state import SimulationState
from sim.methods.strombom import sheep
from sim.methods.strombom.config import resolve_n_neighbors


def prepare(config: dict[str, Any]) -> dict[str, Any]:
    """Return the keys this model derives (the neighbour count k)."""
    return {"k_neighbors": resolve_n_neighbors(config["n_neighbors"], int(config["n_sheep"]))}


def top_speed(config: dict[str, Any]) -> float:
    """A heading of length ``sheep_speed`` moved dt x heading per tick (Table 1, delta = 1 at
    dt = 1), so sheep_speed is already units per second."""
    return float(config["sheep_speed"])


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    """Advance every sheep by ``dt * velocity`` (dt = 1 is the paper's one step per tick)."""
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
