"""Orchestrates the simulation tick loop for factor-based experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from core.agent_attributes import (
    apply_environment_updates,
    apply_failure_factors,
    apply_robot_constraints,
    init_agent_attributes,
)
from core.base_metric import BaseMetric
from core.base_scenario import BaseScenario
from core.dog_controller import BaseDogController
from core.history_recorder import HistoryRecorder
from core.observation import BaseObservationModel
from core.plugin_registry import (
    dog_controller_registry,
    observation_registry,
    sheep_dynamics_registry,
)
from core.sheep_dynamics import BaseSheepDynamics
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

    Tick order:
      environment updates -> sheep dynamics -> observations -> dog controller
      -> robot constraints -> obstacles/walls -> metrics
    """

    def __init__(
        self,
        scenario: BaseScenario,
        metrics: list[BaseMetric],
        config: dict[str, Any],
        seed: int = 42,
        sheep_dynamics: BaseSheepDynamics | None = None,
        dog_controller: BaseDogController | None = None,
        observation_model: BaseObservationModel | None = None,
        instrument: str | None = None,
    ):
        self.scenario = scenario
        self.config = config
        self.seed = seed
        self.instrument = instrument or config.get("instrument")
        self.sheep_dynamics = sheep_dynamics or sheep_dynamics_registry.get(
            str(config.get("sheep_model", "strombom"))
        )
        self.dog_controller = dog_controller or dog_controller_registry.get(
            str(config.get("dog_controller", "collect_drive"))
        )
        obs_mode = str(config.get("obs_mode", "global"))
        self.observation_model = observation_model or observation_registry.get(obs_mode)
        self.recorder = HistoryRecorder(metrics)
        self._state: SimulationState | None = None
        self._max_ticks = scenario.max_ticks(config)
        self._prev_dog_vel: np.ndarray | None = None

    def initialize(self) -> SimulationState:
        """Set up the initial simulation state from the scenario."""
        rng = np.random.default_rng(self.seed)
        world = self.scenario.create_world(self.config)
        sheep_pos, shepherd_pos = self.scenario.initial_positions(self.config, rng)

        metadata = {
            "r_a": float(self.config.get("r_a", 2.0)),
            "collect_threshold_scale": float(
                self.config.get("collect_threshold_scale", 1.0)
            ),
            "measurement_radius": float(self.config.get("measurement_radius", 5.0)),
            "sheep_model": self.sheep_dynamics.id,
            "dog_controller": self.dog_controller.id,
            "obs_mode": self.observation_model.id,
            "scenario_id": self.scenario.id,
            "seed": self.seed,
            "instrument": self.instrument,
        }
        state = SimulationState(
            tick=0,
            sheep_positions=sheep_pos,
            sheep_velocities=np.zeros_like(sheep_pos),
            shepherd_positions=shepherd_pos,
            shepherd_velocities=np.zeros_like(shepherd_pos),
            world=world,
            rng=rng,
            metadata=metadata,
        )
        self._state = init_agent_attributes(state, self.config)
        self._prev_dog_vel = np.zeros_like(self._state.shepherd_velocities)
        self.recorder.reset()
        self.recorder.record(self._state)
        return self._state

    def step(self) -> tuple[SimulationState, dict[str, float], str]:
        """Execute one tick. Returns (state, metrics_dict, status)."""
        if self._state is None:
            self.initialize()

        state = apply_environment_updates(self._state, self.config)
        state = apply_failure_factors(state, self.config)
        state = self.sheep_dynamics.step(state, self.config)

        observations = self.observation_model.observe_all(state, self.config)
        # Optional message passing for communication factor.
        comm = str(self.config.get("communication", "none"))
        if comm == "global_shared":
            summary = {
                "type": "flock_summary",
                "gcm": state.sheep_centroid.tolist(),
                "n_sheep": state.n_sheep,
            }
            for obs in observations:
                obs.messages.append(summary)
        elif comm == "neighbour_broadcast":
            for obs in observations:
                for other in observations:
                    if other.shepherd_index == obs.shepherd_index:
                        continue
                    obs.messages.append(
                        {
                            "from": other.shepherd_index,
                            "position": other.self_position.tolist(),
                            "n_sheep_seen": other.n_sheep_seen,
                        }
                    )

        state = self.dog_controller.step(state, observations, self.config)
        constrained = apply_robot_constraints(
            state,
            state.shepherd_velocities,
            self.config,
            self._prev_dog_vel
            if self._prev_dog_vel is not None
            else np.zeros_like(state.shepherd_velocities),
        )
        # Re-integrate dog positions if constraints changed velocities.
        if not np.allclose(constrained, state.shepherd_velocities):
            delta = constrained - state.shepherd_velocities
            state = state.copy_with(
                shepherd_positions=state.shepherd_positions + delta,
                shepherd_velocities=constrained,
            )
        self._prev_dog_vel = state.shepherd_velocities.copy()

        state.tick += 1
        state.sheep_positions = state.world.resolve_obstacles(state.sheep_positions)
        state.shepherd_positions = state.world.resolve_obstacles(
            state.shepherd_positions
        )
        state.sheep_positions = state.world.reflect_positions(state.sheep_positions)
        state.shepherd_positions = state.world.reflect_positions(
            state.shepherd_positions
        )
        state.sheep_velocities = state.world.reflect_velocities(
            state.sheep_positions, state.sheep_velocities
        )
        state.shepherd_velocities = state.world.reflect_velocities(
            state.shepherd_positions, state.shepherd_velocities
        )

        self._state = state
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
