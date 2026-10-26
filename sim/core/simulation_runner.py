"""Tick loop for one trial."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from sim.core.simulation_state import SimulationState
from sim.plugins.dogs import DOG_CONTROLLERS
from sim.plugins.metrics import record
from sim.plugins.metrics.view import TickView
from sim.plugins.scenarios import SCENARIOS
from sim.plugins.sheep import SHEEP_MODELS

STOP_SUCCESS = "success"
STOP_TIMEOUT = "timeout"
STOP_ENDED = "ended"  # the task ended the trial before the time limit, without success


@dataclass
class RunResult:
    success: bool
    total_ticks: int
    stop_reason: str  # STOP_SUCCESS, STOP_ENDED or STOP_TIMEOUT
    history: pd.DataFrame  # one row per tick, tick 0 included


def initial_state(config: dict[str, Any], seed: int) -> SimulationState:
    """State at tick 0: agents placed by the task, with one random stream per use.

    The seed spawns three independent generators: one for the start positions, one for
    the sheep and one for the dogs. Changing the dog count only draws from the dogs'
    stream, so two cells with the same seed start from the same flock and the sheep
    see the same noise until the dogs act differently (paired comparisons).
    """
    layout_rng, sheep_rng, dog_rng = (
        np.random.default_rng(child) for child in np.random.SeedSequence(seed).spawn(3)
    )
    scenario = SCENARIOS[config["scenario_id"]]
    sheep, dogs = scenario.initial_positions(config, layout_rng)
    return SimulationState(
        tick=0,
        sheep_positions=sheep,
        sheep_velocities=np.zeros_like(sheep),
        shepherd_positions=dogs,
        shepherd_velocities=np.zeros_like(dogs),
        world=scenario.create_world(config),
        rng=sheep_rng,
        dog_rng=dog_rng,
        metadata={"shepherd_path": 0.0},
    )


def run_trial(
    config: dict[str, Any],
    seed: int,
    on_tick: Callable[[SimulationState], None] | None = None,
) -> RunResult:
    """Run one trial until success, the task's own end rule, or the time limit.

    Each tick the sheep move, then the dogs, then the metrics are recorded and the stop
    rules checked. ``shepherd_path`` sums |v| dt over every dog. Metrics are recorded at
    tick 0, every ``metrics_stride`` ticks and at the last tick; the stop rules run every
    tick. ``on_tick`` sees the state after each tick (tests use it to check invariants).
    """
    scenario = SCENARIOS[config["scenario_id"]]
    sheep_step = SHEEP_MODELS[config["sheep_model"]].step
    dog_step = DOG_CONTROLLERS[config["dog_controller"]]
    max_ticks = int(config["max_ticks"])
    dt = float(config["dt"])
    stride = int(config["metrics_stride"])

    def metrics(state: SimulationState) -> dict[str, float]:
        return {"tick": state.tick, **record(TickView(state, config), scenario.metrics)}

    def finish(state: SimulationState, success: bool, reason: str) -> RunResult:
        # The last tick is always in the history, whatever the stride.
        if state.tick % stride:
            history.append(metrics(state))
        return RunResult(success, state.tick, reason, pd.DataFrame(history))

    state = initial_state(config, seed)
    history = [metrics(state)]
    while True:
        state = sheep_step(state, config)
        state = dog_step(state, config)
        state.metadata["shepherd_path"] += dt * float(
            np.linalg.norm(state.shepherd_velocities, axis=1).sum()
        )
        state.tick += 1
        if state.tick % stride == 0:
            history.append(metrics(state))
        if on_tick is not None:
            on_tick(state)

        if scenario.is_success(state):
            return finish(state, True, STOP_SUCCESS)
        if scenario.is_over(state, config):
            return finish(state, False, STOP_ENDED)
        if state.tick >= max_ticks:
            return finish(state, False, STOP_TIMEOUT)
