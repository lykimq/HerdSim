"""Resolve experiment configuration from experimental factors and presets."""

from __future__ import annotations

from typing import Any

from core.base_scenario import BaseScenario
from core.experimental_factors import ExperimentalFactors
from core.plugin_registry import dog_controller_registry, sheep_dynamics_registry
from core.presets import get_preset
from core.shared_defaults import (
    SHARED_WORLD_DEFAULTS,
    WORLD_KEYS,
    scenario_world_config,
)

__all__ = ["WORLD_KEYS", "resolve_experiment_config", "resolve_from_factors"]


def resolve_from_factors(
    factors: ExperimentalFactors,
    scenario: BaseScenario,
) -> dict[str, Any]:
    """Build the flat run config used by SimulationRunner from factors."""
    factors.validate()
    sheep = sheep_dynamics_registry.get(factors.model.sheep_model)
    dogs = dog_controller_registry.get(factors.model.dog_controller)

    config = dict(SHARED_WORLD_DEFAULTS)
    config.update(dict(sheep.default_config))
    config.update(dict(dogs.default_config))
    if factors.params:
        config.update(factors.params)

    scenario_defaults = dict(getattr(scenario, "default_config", {}) or {})
    preset = (factors.model.preset or "paper").lower()
    if preset not in {"paper", "scenario", "custom"}:
        raise ValueError(f"Unknown preset '{preset}'. Use paper|scenario|custom.")

    if preset == "scenario":
        config.update(scenario_defaults)
    else:
        config.update(scenario_world_config(scenario_defaults))

    if factors.environment.world_overrides:
        config.update(factors.environment.world_overrides)

    if factors.flock.n_sheep is not None:
        config["n_sheep"] = int(factors.flock.n_sheep)
    if factors.shepherds.n_shepherds is not None:
        config["n_shepherds"] = int(factors.shepherds.n_shepherds)
    if factors.flock.initial_spread is not None:
        config["initial_spread"] = float(factors.flock.initial_spread)
    if factors.flock.noise_strength is not None:
        config["noise_strength"] = float(factors.flock.noise_strength)

    config["sheep_model"] = factors.model.sheep_model
    config["dog_controller"] = factors.model.dog_controller
    config["scenario_id"] = factors.model.scenario
    config["obs_mode"] = factors.observation.mode
    config["observation_frequency"] = int(factors.observation.observation_frequency)
    config["noise_sigma"] = float(factors.observation.noise_sigma)
    config["communication"] = factors.observation.communication
    if factors.observation.sensing_range is not None:
        config["sensing_range"] = float(factors.observation.sensing_range)
    config["stubborn_fraction"] = float(factors.flock.stubborn_fraction)
    config["stubborn_rs_scale"] = float(factors.flock.stubborn_response_scale)
    config["stubborn_response_scale"] = float(factors.flock.stubborn_response_scale)
    config["cohesion_scale"] = float(factors.flock.cohesion_scale)
    config["initial_layout"] = factors.flock.initial_layout
    config["speed_scale"] = float(factors.shepherds.speed_scale)
    config["failure_mode"] = factors.shepherds.failure_mode
    config["failure_tick"] = int(factors.shepherds.failure_tick)
    config["sensing_scale"] = float(factors.shepherds.sensing_scale)
    config["goal_mode"] = factors.environment.goal_mode
    config["goal_velocity"] = list(factors.environment.goal_velocity)
    if factors.shepherds.v_max is not None:
        config["v_max"] = float(factors.shepherds.v_max)
    if factors.shepherds.a_max is not None:
        config["a_max"] = float(factors.shepherds.a_max)
    if factors.shepherds.omega_max is not None:
        config["omega_max"] = float(factors.shepherds.omega_max)
    config["latency"] = int(factors.shepherds.latency)

    config.setdefault("n_sheep", int(sheep.default_config.get("n_sheep", 20)))
    config.setdefault("n_shepherds", int(dogs.default_config.get("n_shepherds", 1)))
    return config


def resolve_experiment_config(
    *,
    scenario: BaseScenario,
    factors: ExperimentalFactors | dict[str, Any] | None = None,
    instrument: str | None = None,
    preset: str = "paper",
    num_sheep: int | None = None,
    num_shepherds: int | None = None,
    algorithm_params: dict[str, Any] | None = None,
    world_overrides: dict[str, Any] | None = None,
    sheep_model: str | None = None,
    dog_controller: str | None = None,
) -> dict[str, Any]:
    """Resolve config from factors and/or a named instrument preset.

    ``instrument`` replaces the old algorithm_id selector. When provided, its
    sheep_model, dog_controller, and default params are applied first.
    Explicit ``algorithm_params`` and ``world_overrides`` win last.
    """
    raw: dict[str, Any] = {}
    explicit_params = dict(algorithm_params or {})
    if instrument:
        bundle = get_preset(instrument)
        raw.update(bundle["factors"])
        raw.setdefault("params", {})
        raw["params"] = {
            **dict(bundle["default_config"]),
            **dict(raw.get("params") or {}),
        }
        raw.setdefault("model", {})
        raw["model"] = {
            **dict(raw.get("model") or {}),
            "sheep_model": bundle["sheep_model"],
            "dog_controller": bundle["dog_controller"],
            "preset": preset,
            "scenario": getattr(scenario, "id", "drive_to_goal"),
        }

    if isinstance(factors, ExperimentalFactors):
        merged = factors.to_dict()
    else:
        merged = dict(factors or {})
    for key in ("flock", "shepherds", "observation", "environment", "model", "params"):
        if key in merged or key in raw:
            base = dict(raw.get(key) or {})
            base.update(dict(merged.get(key) or {}))
            raw[key] = base
    for key, value in merged.items():
        if key not in ("flock", "shepherds", "observation", "environment", "model", "params"):
            raw[key] = value

    raw.setdefault("model", {})
    raw["model"]["preset"] = preset
    raw["model"]["scenario"] = getattr(scenario, "id", "drive_to_goal")
    if sheep_model:
        raw["model"]["sheep_model"] = sheep_model
    if dog_controller:
        raw["model"]["dog_controller"] = dog_controller
    if num_sheep is not None:
        raw.setdefault("flock", {})
        raw["flock"]["n_sheep"] = int(num_sheep)
    if num_shepherds is not None:
        raw.setdefault("shepherds", {})
        raw["shepherds"]["n_shepherds"] = int(num_shepherds)
    if world_overrides:
        raw.setdefault("environment", {})
        env = dict(raw["environment"])
        overrides = dict(env.get("world_overrides") or {})
        overrides.update(world_overrides)
        env["world_overrides"] = overrides
        raw["environment"] = env

    # Map known factor keys from explicit params into factor groups.
    if explicit_params:
        raw.setdefault("observation", {})
        raw.setdefault("flock", {})
        raw.setdefault("shepherds", {})
        raw.setdefault("environment", {})
        obs_keys = {
            "obs_mode": ("observation", "mode"),
            "sensing_range": ("observation", "sensing_range"),
            "noise_sigma": ("observation", "noise_sigma"),
            "observation_frequency": ("observation", "observation_frequency"),
            "communication": ("observation", "communication"),
            "stubborn_fraction": ("flock", "stubborn_fraction"),
            "stubborn_rs_scale": ("flock", "stubborn_response_scale"),
            "stubborn_response_scale": ("flock", "stubborn_response_scale"),
            "cohesion_scale": ("flock", "cohesion_scale"),
            "noise_strength": ("flock", "noise_strength"),
            "failure_mode": ("shepherds", "failure_mode"),
            "failure_tick": ("shepherds", "failure_tick"),
            "speed_scale": ("shepherds", "speed_scale"),
            "goal_mode": ("environment", "goal_mode"),
            "v_max": ("shepherds", "v_max"),
            "a_max": ("shepherds", "a_max"),
            "omega_max": ("shepherds", "omega_max"),
            "latency": ("shepherds", "latency"),
        }
        for src, (group, dest) in obs_keys.items():
            if src in explicit_params:
                raw[group][dest] = explicit_params[src]

    config = resolve_from_factors(ExperimentalFactors.from_dict(raw), scenario)
    # Explicit caller overrides win after scenario composition.
    if explicit_params:
        config.update(explicit_params)
    if world_overrides:
        config.update(world_overrides)
    if num_sheep is not None:
        config["n_sheep"] = int(num_sheep)
    if num_shepherds is not None:
        config["n_shepherds"] = int(num_shepherds)
    return config
