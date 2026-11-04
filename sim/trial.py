"""One trial: the flat run config and the tick loop.

The run config is a flat dict of the method's parameters, the task's setup keys and the
counts. Engine checks live in ``build_config``; the task and the sheep check their own
settings there too.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from sim.drive_task import goal, task
from sim.metrics import record
from sim.metrics.view import TickView
from sim.state import SimulationState
from sim.strombom import sheep, team
from sim.strombom.params import DEFAULTS

STOP_SUCCESS = "success"
STOP_TIMEOUT = "timeout"

# Setup keys the engine itself reads, on top of the task's own: the run loop and the
# constants the generic metrics read every tick.
ENGINE_KEYS = (
    "max_ticks",
    "measurement_radius",
    "lost_radius",
    "dog_overlap_distance",
)

# Speeds of the method; none may be negative.
SPEED_KEYS = ("sheep_speed", "shepherd_speed")


@dataclass
class RunResult:
    success: bool
    total_ticks: int
    stop_reason: str  # STOP_SUCCESS or STOP_TIMEOUT
    history: pd.DataFrame  # one row per tick, tick 0 included


def build_config(
    *,
    method: str,
    params: dict[str, Any],
    setup: dict[str, Any],
    n_sheep: int,
    n_shepherds: int,
    initial_layout: str,
) -> dict[str, Any]:
    """Flat run config from the method defaults, ``params``, task ``setup``, and counts."""
    missing = sorted(set(task.required_keys(initial_layout) + ENGINE_KEYS) - set(setup))
    if missing:
        raise KeyError(f"Task {task.TASK!r} needs setup keys {missing}")
    config: dict[str, Any] = {
        **DEFAULTS,
        **params,
        **setup,
        "method": method,
        "n_sheep": n_sheep,
        "n_shepherds": n_shepherds,
        "initial_layout": initial_layout,
    }
    _check(config)
    task.check(config)
    config.update(sheep.prepare(config))
    return config


def _check(config: dict[str, Any]) -> None:
    """The engine's own bounds: counts, time limit, time step and speeds."""
    if int(config["n_sheep"]) < 1:
        raise ValueError("n_sheep must be at least 1")
    if int(config["max_ticks"]) < 1:
        raise ValueError("max_ticks must be at least 1")
    if float(config["dt"]) <= 0.0:
        raise ValueError("dt must be positive")
    for key in SPEED_KEYS:
        if key in config and float(config[key]) < 0.0:
            raise ValueError(f"{key} must not be negative")


def seed_streams(seed: int) -> list[np.random.Generator]:
    """The layout, sheep and dog random streams of one seed, kept apart so D can be paired."""
    return [np.random.default_rng(child) for child in np.random.SeedSequence(seed).spawn(3)]


def initial_state(config: dict[str, Any], seed: int) -> SimulationState:
    """Tick 0: place agents with the seed's layout stream."""
    layout_rng, sheep_rng, dog_rng = seed_streams(seed)
    sheep_positions, dogs = task.initial_positions(config, layout_rng)
    return SimulationState(
        tick=0,
        sheep_positions=sheep_positions,
        sheep_velocities=np.zeros_like(sheep_positions),
        shepherd_positions=dogs,
        shepherd_velocities=np.zeros_like(dogs),
        world=goal.create_world(config),
        rng=sheep_rng,
        dog_rng=dog_rng,
        metadata={"shepherd_path": 0.0},
    )


def run_trial(
    config: dict[str, Any],
    seed: int,
    on_tick: Callable[[SimulationState], None] | None = None,
    history: bool = True,
) -> RunResult:
    """Run until success or the time limit: sheep, then dogs, then metrics each tick.

    ``shepherd_path`` sums |v| dt. ``on_tick`` sees the post-tick state (for tests).
    ``history=False`` skips the metrics, which only read the state, so the trial is the
    same and ``RunResult.history`` is empty; a caller that needs only the outcome saves
    most of the run time.
    """
    max_ticks = int(config["max_ticks"])
    dt = float(config["dt"])
    rows: list[dict[str, float]] = []

    def metrics(state: SimulationState) -> None:
        if history:
            rows.append({"tick": state.tick, **record(TickView(state, config), task.METRICS)})

    state = initial_state(config, seed)
    metrics(state)
    while True:
        state = sheep.step(state, config)
        state = team.step(state, config)
        state.metadata["shepherd_path"] += dt * float(
            np.linalg.norm(state.shepherd_velocities, axis=1).sum()
        )
        state.tick += 1
        metrics(state)
        if on_tick is not None:
            on_tick(state)

        if task.is_success(state):
            return RunResult(True, state.tick, STOP_SUCCESS, pd.DataFrame(rows))
        if state.tick >= max_ticks:
            return RunResult(False, state.tick, STOP_TIMEOUT, pd.DataFrame(rows))
