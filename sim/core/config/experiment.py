"""Assemble and validate flat trial configuration dictionaries.

Integrates method defaults, parameter overrides, scenario setup parameters, and agent
counts, delegating domain validation to respective scenario and agent model plugins.
"""

from __future__ import annotations

from typing import Any

from sim.core.methods import METHODS
from sim.plugins.scenarios import SCENARIOS
from sim.plugins.sheep import SHEEP_MODELS

# Core simulation runner and metric evaluation configuration keys.
ENGINE_KEYS = (
    "max_ticks",
    "metrics_stride",
    "measurement_radius",
    "lost_radius",
    "dog_overlap_distance",
)

# Speeds a method may define; none may be negative.
SPEED_KEYS = ("sheep_speed", "shepherd_speed", "sheep_speed_max", "dog_speed_max", "herder_speed")


def build_config(
    *,
    task: str,
    method: str,
    params: dict[str, Any],
    setup: dict[str, Any],
    n_sheep: int,
    n_shepherds: int,
    initial_layout: str,
) -> dict[str, Any]:
    """Assemble a validated trial configuration dictionary.

    Merges method defaults, parameter overrides, scenario setup keys, and agent counts.
    Validates required keys against engine and scenario schemas, invokes plugin
    preparation hooks, and attaches derived properties (e.g. `reaction_radius`).

    Args:
        task: Scenario identifier (e.g., 'drive_to_goal', 'gather').
        method: Method bundle identifier (e.g., 'strombom', 'lama', 'kubo').
        params: Explicit parameter overrides for the method bundle.
        setup: Environmental and scenario setup parameters.
        n_sheep: Number of sheep agents.
        n_shepherds: Number of shepherd agents.
        initial_layout: Starting spatial layout identifier.

    Returns:
        Fully assembled and validated configuration dictionary for one trial.
    """
    bundle = METHODS[method]
    unknown = sorted(set(params) - set(bundle.defaults))
    if unknown:
        raise KeyError(f"Method {method!r} has no parameters {unknown}")
    scenario = SCENARIOS[task]
    missing = sorted(set(scenario.required_keys + ENGINE_KEYS) - set(setup))
    if missing:
        raise KeyError(f"Task {task!r} needs setup keys {missing}")
    config: dict[str, Any] = {
        **bundle.defaults,
        **params,
        **setup,
        "scenario_id": task,
        "method": method,
        "sheep_model": bundle.sheep_model,
        "dog_controller": bundle.dog_controller,
        "n_sheep": n_sheep,
        "n_shepherds": n_shepherds,
        "initial_layout": initial_layout,
    }
    _check(config)
    scenario.check(config)
    sheep = SHEEP_MODELS[bundle.sheep_model]
    config.update(sheep.prepare(config))
    config["reaction_radius"] = sheep.reaction_radius(config)
    return config


def _check(config: dict[str, Any]) -> None:
    """Validate core engine bounds and speed parameters."""
    if int(config["n_sheep"]) < 1:
        raise ValueError("n_sheep must be at least 1")
    if int(config["max_ticks"]) < 1:
        raise ValueError("max_ticks must be at least 1")
    if int(config["metrics_stride"]) < 1:
        raise ValueError("metrics_stride must be at least 1")
    if float(config["dt"]) <= 0.0:
        raise ValueError("dt must be positive")
    for key in SPEED_KEYS:
        if key in config and float(config[key]) < 0.0:
            raise ValueError(f"{key} must not be negative")
