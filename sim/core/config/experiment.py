"""Build the flat run config of one trial and check it before anything runs.

The checks here are the engine's own. Each plugin checks its settings: the task its layouts
and start geometry, the sheep model its parameters (and it derives keys such as Strombom's
neighbour count), so a new plugin brings its checks along instead of editing this file.
"""

from __future__ import annotations

from typing import Any

from sim.core.methods import METHODS
from sim.plugins.scenarios import SCENARIOS
from sim.plugins.sheep import SHEEP_MODELS

# Setup keys the engine itself reads (on top of the task's own keys): the run
# loop and the per-trial constants the generic metrics read every tick.
ENGINE_KEYS = (
    "max_ticks",
    "measurement_radius",
    "lost_radius",
    "dog_overlap_distance",
)

# Speeds a method may define; none may be negative.
SPEED_KEYS = ("sheep_speed", "shepherd_speed", "sheep_speed_max", "dog_speed_max")


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
    """Method defaults, overridden by ``params``, plus the task ``setup`` and agent counts.

    ``setup`` must hold every key the task and the engine read; there are no
    defaults for them here. The sheep model adds the keys it derives, and
    ``reaction_radius`` (how close a dog must be for a sheep to react) is
    added for the coverage metric.
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
        "n_sheep": int(n_sheep),
        "n_shepherds": int(n_shepherds),
        "initial_layout": initial_layout,
    }
    _check(config)
    scenario.check(config)
    sheep = SHEEP_MODELS[bundle.sheep_model]
    config.update(sheep.prepare(config))
    config["reaction_radius"] = sheep.reaction_radius(config)
    return config


def _check(config: dict[str, Any]) -> None:
    if int(config["n_sheep"]) < 1:
        raise ValueError("n_sheep must be at least 1")
    if int(config["max_ticks"]) < 1:
        raise ValueError("max_ticks must be at least 1")
    if float(config["dt"]) <= 0.0:
        raise ValueError("dt must be positive")
    for key in SPEED_KEYS:
        if key in config and float(config[key]) < 0.0:
            raise ValueError(f"{key} must not be negative")
