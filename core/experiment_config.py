"""Resolve experiment configuration from paper / scenario / custom presets."""

from __future__ import annotations

from typing import Any

from core.base_algorithm import BaseAlgorithm
from core.base_scenario import BaseScenario

WORLD_KEYS = (
    "world_width",
    "world_height",
    "goal_center",
    "goal_radius",
    "max_ticks",
    "pen_center",
    "pen_radius",
    "obstacles",
    "initial_spread",
    "shepherd_start_offset",
    "success_fraction",
    "n_clusters",
    "gate_width",
    "gate_y",
    # Extension (not in Strombom 2014): allows a scenario to widen the
    # collect/drive switching threshold without changing r_a.  Default 1.0
    # reproduces paper behaviour.  Flows from scenario config into all presets.
    "collect_threshold_scale",
)


def _scenario_world_config(scenario_defaults: dict[str, Any]) -> dict[str, Any]:
    """World / layout keys from the selected scenario (goal, obstacles, etc.)."""
    return {k: v for k, v in scenario_defaults.items() if k in WORLD_KEYS}


def resolve_experiment_config(
    algorithm: BaseAlgorithm,
    scenario: BaseScenario,
    *,
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    algorithm_params: dict[str, Any] | None = None,
    world_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the run config used by SimulationRunner.

    Presets:
    - paper: algorithm paper parameters and agent counts; world layout from scenario
    - scenario: algorithm defaults, then full scenario.default_config overlay
    - custom: algorithm paper params; scenario world as base; caller overrides
    """
    preset = (preset or "paper").lower()
    if preset not in {"paper", "scenario", "custom"}:
        raise ValueError(f"Unknown preset '{preset}'. Use paper|scenario|custom.")

    config = dict(algorithm.default_config)
    scenario_defaults = dict(getattr(scenario, "default_config", {}) or {})

    if preset == "scenario":
        config.update(scenario_defaults)
    else:
        # paper and custom: keep algorithm behavior params, use scenario layout.
        config.update(_scenario_world_config(scenario_defaults))

    if algorithm_params:
        config.update(algorithm_params)
    if world_overrides:
        config.update(world_overrides)

    if num_sheep is not None:
        config["n_sheep"] = int(num_sheep)
    if num_shepherds is not None:
        config["n_shepherds"] = int(num_shepherds)

    # Ensure required agent counts always exist.
    config.setdefault("n_sheep", int(algorithm.default_config.get("n_sheep", 20)))
    config.setdefault(
        "n_shepherds", int(algorithm.default_config.get("n_shepherds", 1))
    )
    return config
