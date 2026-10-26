"""Named methods: a sheep model, a dog controller and their default parameters.

A protocol may override any default by name; a name that is not a default is
rejected, so every parameter a trial used is listed here. Every method carries
dt, which the engine reads whatever the method. A new method is one entry here,
naming a sheep model and a dog controller from their plugin tables; a name
that is not in them fails at import.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from sim.methods.kubo import config as kubo
from sim.methods.lama import config as lama
from sim.methods.strombom import config as strombom
from sim.plugins.dogs import DOG_CONTROLLERS
from sim.plugins.sheep import SHEEP_MODELS

# Keys every method must define, because the engine reads them for any method.
ENGINE_PARAMS = ("dt",)


@dataclass(frozen=True)
class Method:
    sheep_model: str
    dog_controller: str
    defaults: Mapping[str, Any]


METHODS: dict[str, Method] = {
    # Strömböm flock with multi-dog collect/drive heuristic.
    "strombom_multi": Method(
        sheep_model="strombom",
        dog_controller="collect_drive_multi",
        defaults={**strombom.PAPER, **strombom.SHEPHERD_EXTENSIONS},
    ),
    # Strömböm flock with independent farthest-agent targeting dogs.
    "fat": Method(
        sheep_model="strombom",
        dog_controller="fat",
        defaults={**strombom.PAPER, **strombom.SHEPHERD_EXTENSIONS},
    ),
    # Strömböm flock with independent single-agent dogs (no team coordination layer).
    "independent": Method(
        sheep_model="strombom",
        dog_controller="independent",
        defaults={**strombom.PAPER, **strombom.SHEPHERD_EXTENSIONS},
    ),
    # Kubo force-based sheep and dog dynamics.
    "kubo": Method(
        sheep_model="kubo",
        dog_controller="kubo_forces",
        defaults={**kubo.PAPER, **kubo.NOT_IN_PAPER},
    ),
    # Lama & di Bernardo distributed herding with stochastic targets.
    "lama": Method(
        sheep_model="lama_targets",
        dog_controller="lama_herders",
        defaults=dict(lama.PAPER),
    ),
}


def _check_catalog() -> None:
    """Every method names known plugins and defines the engine's keys."""
    for name, method in METHODS.items():
        if method.sheep_model not in SHEEP_MODELS:
            raise ValueError(f"method {name!r}: unknown sheep_model {method.sheep_model!r}")
        if method.dog_controller not in DOG_CONTROLLERS:
            raise ValueError(f"method {name!r}: unknown dog_controller {method.dog_controller!r}")
        missing = [k for k in ENGINE_PARAMS if k not in method.defaults]
        if missing:
            raise ValueError(f"method {name!r} does not define {missing}")


_check_catalog()
