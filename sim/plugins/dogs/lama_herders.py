"""Distributed herders controller (Lama & di Bernardo 2024).

Each herder chases the sensed target farthest from the goal not claimed by a closer neighbor.
Herders with no active targets return to the goal center. Decisions evaluate synchronous
state snapshots at tick start.
"""

from __future__ import annotations

from typing import Any

from sim.core.simulation_state import SimulationState
from sim.methods.lama.dynamics import TARGETS_AT_TICK_START, herder_velocities

from .helpers import move_dogs


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    origin = state.world.goal.center
    targets = state.metadata.get(TARGETS_AT_TICK_START, state.sheep_positions)
    velocities, choice = herder_velocities(
        targets - origin,
        state.shepherd_positions - origin,
        state.world.goal.radius,
        config,
    )
    state.metadata["herder_target"] = choice.target
    return move_dogs(state, velocities, float(config["dt"]))
