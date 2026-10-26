"""Target dynamics under stochastic repulsion (Lama & di Bernardo 2024).

Integrates target motion via Euler-Maruyama with herder repulsion and Gaussian noise.
Stores pre-step positions in `state.metadata[TARGETS_AT_TICK_START]` to ensure herders
evaluate synchronous state snapshots.
"""

from __future__ import annotations

from typing import Any

from sim.core.simulation_state import SimulationState
from sim.methods.lama import config as lama
from sim.methods.lama.dynamics import TARGETS_AT_TICK_START, noise_step, target_velocities


def prepare(config: dict[str, Any]) -> dict[str, Any]:
    """Validate parameters (ensuring positive values and herder_speed > target_top_speed).

    Returns an empty dict as this model produces no derived configuration keys.
    """
    lama.check(config)
    return {}


def top_speed(config: dict[str, Any]) -> float:
    """Target speed scale v_T = beta * lambda."""
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
