"""Lama targets (sheep_model=lama_targets): one Euler-Maruyama step of eq. 1.

The stored velocity is the displacement of the step over dt, push and noise together, so
positions minus the previous positions equal dt x velocity as for the other models.

The paper integrates targets and herders from the same state at time t. HerdSim's engine
moves the sheep first and the dogs after, so the step keeps the targets' positions from
before it moved them in ``state.metadata[TARGETS_AT_TICK_START]``, and the Lama herders
read those. With herders reading the moved targets instead, a team of 16 gathered 400
targets; with the paper's order, 17.

``prepare`` checks the whole parameter set, the herders' side included, because the paper's
assumption v_H > v_T ties the two sides together.
"""

from __future__ import annotations

from typing import Any

from sim.core.simulation_state import SimulationState
from sim.methods.lama import config as lama
from sim.methods.lama.dynamics import TARGETS_AT_TICK_START, noise_step, target_velocities


def prepare(config: dict[str, Any]) -> dict[str, Any]:
    """Check the paper's assumptions on the parameters; no derived keys."""
    lama.check(config)
    return {}


def top_speed(config: dict[str, Any]) -> float:
    """v_T = beta lambda, the paper's maximum escaping speed from one herder. Two herders can
    push harder and the noise is unbounded; v_T is the paper's own speed scale."""
    return lama.target_top_speed(config)


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    dt = float(config["dt"])
    origin = state.world.goal.center
    push = target_velocities(
        state.sheep_positions - origin, state.shepherd_positions - origin, config
    )
    moved = dt * push + noise_step(state.rng, state.n_sheep, config)
    state.metadata[TARGETS_AT_TICK_START] = state.sheep_positions
    return state.copy_with(
        sheep_positions=state.sheep_positions + moved,
        sheep_velocities=moved / dt,
    )
