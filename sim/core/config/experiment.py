"""Build and check the flat run config of one trial.

Engine checks live here; each plugin checks its own settings when it prepares.
"""

from __future__ import annotations

from typing import Any

from sim.core.methods import METHODS
from sim.plugins.scenarios import SCENARIOS
from sim.plugins.sheep import SHEEP_MODELS

# Setup keys the engine itself reads, on top of the task's own: the run loop and the
# constants the generic metrics read every tick.
ENGINE_KEYS = (
    "max_ticks",
    "measurement_radius",
    "lost_radius",
    "dog_overlap_distance",
)

# Speeds of the method; none may be negative.
SPEED_KEYS = ("sheep_speed", "shepherd_speed")


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
    """Flat run config from method defaults, ``params``, task ``setup``, and counts."""
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
    """The engine's own bounds: counts, time limit, time step and speeds."""
    if int(config["n_sheep"]) < 1:
        raise ValueError("n_sheep must be at least 1")
    if int(config["max_ticks"]) < 1:
        raise ValueError("max_ticks must be at least 1")
    if float(config["dt"]) <= 0.0:
        raise ValueError("dt must be positive")
    for key in SPEED_KEYS:
        if key in config and float(config[key]) < 0.0:
            raise ValueError(f"{key} must not be negative")
