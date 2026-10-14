"""Resolve the flat run config for one trial from a method bundle and a scenario."""

from __future__ import annotations

from typing import Any

from plugins.scenarios.base import BaseScenario

from core.methods import get_method
from core.plugin_registry import dog_controller_registry, sheep_dynamics_registry
from core.world.defaults import WORLD_DEFAULTS, scenario_world_config
from core.world.layouts import X0_FAMILIES, normalize_layout

COMMUNICATION_MODES = ("none", "neighbour_broadcast", "global_shared")


def resolve_experiment_config(
    *,
    scenario: BaseScenario,
    method: str,
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    algorithm_params: dict[str, Any] | None = None,
    world_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Flat config read by SimulationRunner, plugins, and metrics.

    Composition order (later wins):
      WORLD_DEFAULTS -> sheep defaults -> dog defaults -> method params
      -> scenario world keys -> model / information defaults
      -> ``algorithm_params`` -> ``world_overrides`` -> agent counts
    """
    bundle = get_method(method)
    sheep = sheep_dynamics_registry.get(bundle["sheep_model"])
    dogs = dog_controller_registry.get(bundle["dog_controller"])

    config: dict[str, Any] = dict(WORLD_DEFAULTS)
    config.update(sheep.default_config)
    config.update(dogs.default_config)
    config.update(bundle["default_config"])
    config.update(scenario_world_config(scenario.default_config))
    config.update(
        {
            "sheep_model": bundle["sheep_model"],
            "dog_controller": bundle["dog_controller"],
            "scenario_id": scenario.id,
            "obs_mode": "global",
            "communication": "none",
            "initial_layout": "compact",
        }
    )
    config.update(algorithm_params or {})
    config.update(world_overrides or {})
    if num_sheep is not None:
        config["n_sheep"] = int(num_sheep)
    if num_shepherds is not None:
        config["n_shepherds"] = int(num_shepherds)
    config.setdefault("n_sheep", 20)
    config.setdefault("n_shepherds", 1)

    if normalize_layout(config["initial_layout"]) not in X0_FAMILIES:
        raise ValueError(
            f"Unknown initial_layout '{config['initial_layout']}'. Use one of {X0_FAMILIES}."
        )
    if config["communication"] not in COMMUNICATION_MODES:
        raise ValueError(
            f"Unknown communication '{config['communication']}'. Use one of {COMMUNICATION_MODES}."
        )
    return config
