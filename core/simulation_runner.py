"""Orchestrates the simulation tick loop, connecting algorithm, scenario, and metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from core.base_algorithm import BaseAlgorithm
from core.base_metric import BaseMetric
from core.base_scenario import BaseScenario
from core.history_recorder import HistoryRecorder
from core.simulation_state import SimulationState


@dataclass
class RunResult:
    """Outcome of a completed simulation run."""

    success: bool
    total_ticks: int
    seed: int
    history: pd.DataFrame
    final_state: SimulationState


class SimulationRunner:
    """Drives the simulation forward tick-by-tick.

    Connects a scenario (WHAT), algorithm (HOW), and metrics (MEASURE).
    Manages seed-based reproducibility via numpy.random.Generator.
    """

    def __init__(
        self,
        algorithm: BaseAlgorithm,
        scenario: BaseScenario,
        metrics: list[BaseMetric],
        config: dict[str, Any],
        seed: int = 42,
    ):
        self.algorithm = algorithm
        self.scenario = scenario
        self.config = config
        self.seed = seed
        self.recorder = HistoryRecorder(metrics)
        self._state: SimulationState | None = None
        self._max_ticks = scenario.max_ticks(config)

    def initialize(self) -> SimulationState:
        """Set up the initial simulation state from the scenario."""
        rng = np.random.default_rng(self.seed)
        world = self.scenario.create_world(self.config)
        sheep_pos, shepherd_pos = self.scenario.initial_positions(self.config, rng)

        metadata = {
            "r_a": float(self.config.get("r_a", 2.0)),
            "algorithm_id": self.algorithm.id,
            "scenario_id": self.scenario.id,
            "seed": self.seed,
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

    def step(self) -> tuple[SimulationState, dict[str, float], str]:
        """Execute one tick. Returns (state, metrics_dict, status).

        Status is one of: 'running', 'success', 'timeout'.
        """
        if self._state is None:
            self.initialize()

        self._state = self.algorithm.step(self._state, self.config)
        self._state.tick += 1

        # Shared environment constraint: keep agents outside obstacle interiors.
        self._state.sheep_positions = self._state.world.resolve_obstacles(
            self._state.sheep_positions
        )
        self._state.shepherd_positions = self._state.world.resolve_obstacles(
            self._state.shepherd_positions
        )

        metrics_snapshot = self.recorder.record(self._state)

        if self.scenario.is_success(self._state, self.config):
            return self._state, metrics_snapshot, "success"
        if self._state.tick >= self._max_ticks:
            return self._state, metrics_snapshot, "timeout"
        return self._state, metrics_snapshot, "running"

    def run(self) -> RunResult:
        """Run simulation to completion (success or timeout)."""
        self.initialize()
        status = "running"
        while status == "running":
            _, _, status = self.step()

        return RunResult(
            success=(status == "success"),
            total_ticks=self._state.tick,
            seed=self.seed,
            history=self.recorder.to_dataframe(),
            final_state=self._state,
        )

    @property
    def state(self) -> SimulationState | None:
        return self._state
