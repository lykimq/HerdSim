"""Shared helpers for backend tests (DRY runners and state builders)."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.experiment_config import resolve_experiment_config
from core.simulation_runner import RunResult, SimulationRunner
from core.simulation_state import SimulationState
from core.world import GoalZone, World
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry


def make_world(
    *,
    width: float = 150.0,
    height: float = 150.0,
    goal_center: tuple[float, float] = (15.0, 15.0),
    goal_radius: float = 15.0,
) -> World:
    return World(
        width=width,
        height=height,
        goal=GoalZone(center=np.array(goal_center, dtype=float), radius=goal_radius),
    )


def make_state(
    sheep: np.ndarray,
    shepherds: np.ndarray,
    *,
    world: World | None = None,
    seed: int = 0,
    tick: int = 0,
    metadata: dict[str, Any] | None = None,
) -> SimulationState:
    sheep = np.asarray(sheep, dtype=float)
    shepherds = np.asarray(shepherds, dtype=float)
    return SimulationState(
        tick=tick,
        sheep_positions=sheep,
        sheep_velocities=np.zeros_like(sheep),
        shepherd_positions=shepherds,
        shepherd_velocities=np.zeros_like(shepherds),
        world=world or make_world(),
        rng=np.random.default_rng(seed),
        metadata=metadata or {"r_a": 2.0},
    )


def build_runner(
    algorithm_id: str,
    scenario_id: str = "drive_to_goal",
    *,
    preset: str = "paper",
    seed: int = 1,
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    config_overrides: dict[str, Any] | None = None,
) -> SimulationRunner:
    scenario = scenario_registry.get(scenario_id)
    config = resolve_experiment_config(
        scenario=scenario,
        instrument=algorithm_id,
        preset=preset,
        num_sheep=num_sheep,
        num_shepherds=num_shepherds,
        algorithm_params=config_overrides,
    )
    return SimulationRunner(
        scenario=scenario,
        metrics=metric_registry.get_all(),
        config=config,
        seed=seed,
        instrument=algorithm_id,
    )


def run_trial(
    algorithm_id: str,
    scenario_id: str = "drive_to_goal",
    *,
    preset: str = "paper",
    seed: int = 1,
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    config_overrides: dict[str, Any] | None = None,
) -> RunResult:
    runner = build_runner(
        algorithm_id,
        scenario_id,
        preset=preset,
        seed=seed,
        num_sheep=num_sheep,
        num_shepherds=num_shepherds,
        config_overrides=config_overrides,
    )
    return runner.run()


def snapshot_positions(runner: SimulationRunner, ticks: int) -> list[tuple[np.ndarray, np.ndarray]]:
    runner.initialize()
    out: list[tuple[np.ndarray, np.ndarray]] = []
    for _ in range(ticks):
        state, _, _ = runner.step()
        out.append(
            (state.sheep_positions.copy(), state.shepherd_positions.copy())
        )
    return out
