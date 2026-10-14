"""Resolve the flat run config for one trial from a method bundle and a scenario."""

from __future__ import annotations

from typing import Any

from plugins.scenarios import SCENARIOS

from core.methods import get_method
from core.world.layouts import X0_FAMILIES, normalize_layout

COMMUNICATION_MODES = ("none", "neighbour_broadcast", "global_shared")


def resolve_experiment_config(
    *,
    task: str,
    method: str,
    num_sheep: int,
    num_shepherds: int,
    scenario_params: dict[str, Any],
    algorithm_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Flat config read by run_trial, plugins, and metrics.

    Composition order (later wins):
      method params -> information defaults -> ``algorithm_params``
      -> ``scenario_params`` -> agent counts

    ``scenario_params`` is the task setup from the protocol YAML (arena, goal,
    start, time limit). It must hold every key the task's scenario requires;
    there are no code-side fallbacks for these.
    """
    missing = [k for k in SCENARIOS[task].required_keys if k not in scenario_params]
    if missing:
        raise KeyError(f"Scenario '{task}' needs {missing} in scenario_params.")

    bundle = get_method(method)
    config: dict[str, Any] = dict(bundle["default_config"])
    config.update(
        {
            "sheep_model": bundle["sheep_model"],
            "dog_controller": bundle["dog_controller"],
            "scenario_id": task,
            "obs_mode": "global",
            "communication": "none",
        }
    )
    config.update(algorithm_params or {})
    config.update(scenario_params)
    config["n_sheep"] = int(num_sheep)
    config["n_shepherds"] = int(num_shepherds)

    if normalize_layout(config["initial_layout"]) not in X0_FAMILIES:
        raise ValueError(
            f"Unknown initial_layout '{config['initial_layout']}'. Use one of {X0_FAMILIES}."
        )
    if config["communication"] not in COMMUNICATION_MODES:
        raise ValueError(
            f"Unknown communication '{config['communication']}'. Use one of {COMMUNICATION_MODES}."
        )
    return config
