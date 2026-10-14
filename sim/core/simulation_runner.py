"""Tick loop for one trial."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from plugins.dogs import DOG_CONTROLLERS
from plugins.metrics import METRICS
from plugins.scenarios import SCENARIOS, Scenario
from plugins.sheep import SHEEP_MODELS

from core.observation import OBS_MODES
from core.simulation_state import SimulationState


@dataclass
class RunResult:
    """Outcome of a completed simulation run."""

    success: bool
    total_ticks: int
    history: pd.DataFrame


def _initial_state(scenario: Scenario, config: dict[str, Any], seed: int) -> SimulationState:
    rng = np.random.default_rng(seed)
    world = scenario.create_world(config)
    sheep_pos, shepherd_pos = scenario.initial_positions(config, rng)
    sensing = config.get("sensing_range")
    if sensing is None:
        sensing = config.get("r_s")
    return SimulationState(
        tick=0,
        sheep_positions=sheep_pos,
        sheep_velocities=np.zeros_like(sheep_pos),
        shepherd_positions=shepherd_pos,
        shepherd_velocities=np.zeros_like(shepherd_pos),
        world=world,
        rng=rng,
        metadata={
            "r_a": float(config["r_a"]),
            "measurement_radius": float(config["measurement_radius"]),
            # Kubo has no r_s; coverage is NaN for it unless sensing_range is set.
            "influence_radius": float(sensing) if sensing is not None else float("nan"),
            "shepherd_path": 0.0,
        },
    )


def _record(state: SimulationState) -> dict[str, Any]:
    return {"tick": state.tick, **{name: metric(state) for name, metric in METRICS.items()}}


def run_trial(config: dict[str, Any], seed: int) -> RunResult:
    """Run one trial to success or timeout and record every metric each tick.

    Tick order: sheep dynamics -> observations -> dog controller -> walls ->
    metrics -> success check.
    """
    scenario = SCENARIOS[config["scenario_id"]]
    sheep_step = SHEEP_MODELS[config["sheep_model"]]
    dog_step = DOG_CONTROLLERS[config["dog_controller"]]
    observe = OBS_MODES[config["obs_mode"]]
    max_ticks = int(config["max_ticks"])

    state = _initial_state(scenario, config, seed)
    history = [_record(state)]
    while True:
        prev_dogs = state.shepherd_positions
        state = sheep_step(state, config)
        observations = [observe(state, i, config) for i in range(state.n_shepherds)]
        state = dog_step(state, observations, config)

        state.tick += 1
        world = state.world
        state.sheep_positions = world.reflect_positions(state.sheep_positions)
        state.shepherd_positions = world.reflect_positions(state.shepherd_positions)
        state.sheep_velocities = world.reflect_velocities(
            state.sheep_positions, state.sheep_velocities
        )
        state.shepherd_velocities = world.reflect_velocities(
            state.shepherd_positions, state.shepherd_velocities
        )
        step_lengths = np.linalg.norm(state.shepherd_positions - prev_dogs, axis=1)
        state.metadata["shepherd_path"] += float(step_lengths.sum())

        history.append(_record(state))
        if scenario.is_success(state, config):
            return RunResult(True, state.tick, pd.DataFrame(history))
        if state.tick >= max_ticks:
            return RunResult(False, state.tick, pd.DataFrame(history))
