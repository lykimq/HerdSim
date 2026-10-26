"""Lama herders (dog_controller=lama_herders): eqs. 2 to 4 of Lama and di Bernardo 2024.

Each herder chases the target farthest from the goal centre among those it senses and that no
sensed neighbour is closer to, standing ``chase_offset`` beyond it; a herder with nothing to
chase returns to the goal centre and stands still inside the goal disc. The choice of every
herder is kept in ``state.metadata["herder_target"]`` for the task's end rule and metrics.

The herders decide on the targets' positions at the start of the tick, which the Lama target
step keeps (``TARGETS_AT_TICK_START``), so both sides use the state at time t as the paper's
explicit schemes do. A state no target step has touched (tick 0 in a hand-made test) has no such
record, and its current positions are the positions at the start.
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
