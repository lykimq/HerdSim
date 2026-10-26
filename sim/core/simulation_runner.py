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
    """Initialize agents with mathematically decoupled pseudo-random number streams.

    Uses `SeedSequence(seed).spawn(3)` to derive three independent PRNG generators:
    1. layout_rng: Initial flock and shepherd spatial coordinate placement.
    2. sheep_rng: Sheep Brownian angular diffusion noise throughout the trial.
    3. dog_rng: Shepherd heading noise and stochastic tie-breaking.

    Crucial Common Random Numbers (CRN) invariant:
    Spawning distinct generators guarantees that varying team size D (e.g. D=1 vs D=12)
    consumes draws exclusively from dog_rng. It never draws from or desynchronizes sheep_rng.
    Consequently, trials with identical seed_index experience identical environmental flock
    trajectories until physical canine interaction exerts divergent force.
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
    """Run one trial until success, the task's end rule or the time limit.

    Tick order: sheep move, dogs move, metrics are recorded, then the stop checks. A trial
    stops on success, when the task says it is over (``Scenario.is_over``, a failure; the
    drive task never does) or at ``max_ticks``; otherwise a failure runs to the limit. Every
    dog knows every sheep and every other dog. ``shepherd_path`` sums the commanded displacement
    |v| dt of every dog. Metrics are recorded at tick 0, every ``metrics_stride`` ticks and at
    the last tick (1: every tick); the stop checks run every tick. ``on_tick`` sees the state
    after each tick; tests use it to check invariants.
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
