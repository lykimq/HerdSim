"""Orchestrates the simulation tick loop for one trial."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from plugins.metrics.base import BaseMetric
from plugins.scenarios.base import BaseScenario

from core.history_recorder import HistoryRecorder
from core.plugin_registry import (
    dog_controller_registry,
    observation_registry,
    sheep_dynamics_registry,
)
from core.simulation_state import SimulationState


@dataclass
class RunResult:
    """Outcome of a completed simulation run."""

    success: bool
    total_ticks: int
    seed: int
    history: pd.DataFrame


class SimulationRunner:
    """Drives the simulation forward tick-by-tick.

    Tick order:
      sheep dynamics -> observations -> dog controller -> walls -> metrics
    """

    def __init__(
        self,
        scenario: BaseScenario,
        metrics: list[BaseMetric],
        config: dict[str, Any],
        seed: int = 42,
    ):
        self.scenario = scenario
        self.config = config
        self.seed = seed
        self.sheep_dynamics = sheep_dynamics_registry.get(config["sheep_model"])
        self.dog_controller = dog_controller_registry.get(config["dog_controller"])
        self.observation_model = observation_registry.get(config["obs_mode"])
        self.recorder = HistoryRecorder(metrics)
        self._state: SimulationState | None = None
        self._max_ticks = scenario.max_ticks(config)

    def initialize(self) -> SimulationState:
        """Set up the initial simulation state from the scenario."""
        rng = np.random.default_rng(self.seed)
        world = self.scenario.create_world(self.config)
        sheep_pos, shepherd_pos = self.scenario.initial_positions(self.config, rng)

        sensing = self.config.get("sensing_range")
        if sensing is None:
            sensing = self.config.get("r_s")
        influence = float(sensing) if sensing is not None else float("nan")
        metadata = {
            "r_a": float(self.config.get("r_a", 2.0)),
            "collect_threshold_scale": float(self.config.get("collect_threshold_scale", 1.0)),
            "measurement_radius": float(self.config.get("measurement_radius", 5.0)),
            "influence_radius": influence,
        }
        self._state = SimulationState(
            tick=0,
            sheep_positions=sheep_pos,
            sheep_velocities=np.zeros_like(sheep_pos),
            shepherd_positions=shepherd_pos,
            shepherd_velocities=np.zeros_like(shepherd_pos),
            world=world,
            rng=rng,
            metadata=metadata,
        )
        self.recorder.reset()
        self.recorder.record(self._state)
        return self._state

    def step(self) -> tuple[SimulationState, str]:
        """Execute one tick. Returns (state, status)."""
        if self._state is None:
            self.initialize()
        assert self._state is not None

        state = self.sheep_dynamics.step(self._state, self.config)
        observations = self.observation_model.observe_all(state, self.config)
        state = self.dog_controller.step(state, observations, self.config)

        state.tick += 1
        state.sheep_positions = state.world.reflect_positions(state.sheep_positions)
        state.shepherd_positions = state.world.reflect_positions(state.shepherd_positions)
        state.sheep_velocities = state.world.reflect_velocities(
            state.sheep_positions, state.sheep_velocities
        )
        state.shepherd_velocities = state.world.reflect_velocities(
            state.shepherd_positions, state.shepherd_velocities
        )

        self._state = state
        self.recorder.record(self._state)

        if self.scenario.is_success(self._state, self.config):
            return self._state, "success"
        if self._state.tick >= self._max_ticks:
            return self._state, "timeout"
        return self._state, "running"

    def run(self) -> RunResult:
        """Run simulation to completion (success or timeout)."""
        self.initialize()
        status = "running"
        while status == "running":
            _, status = self.step()

        assert self._state is not None
        return RunResult(
            success=(status == "success"),
            total_ticks=self._state.tick,
            seed=self.seed,
            history=self.recorder.to_dataframe(),
        )

    @property
    def state(self) -> SimulationState | None:
        return self._state
