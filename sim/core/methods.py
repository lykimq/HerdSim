"""Catalog of named methods: sheep model, dog controller, and default parameters.

Unknown override names are rejected. Every method must define ``dt``. New methods
are one entry here; unknown plugin names fail at import.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from sim.methods.strombom import config as strombom
from sim.plugins.dogs import DOG_CONTROLLERS
from sim.plugins.sheep import SHEEP_MODELS

ENGINE_PARAMS = ("dt",)  # required in every method's defaults


@dataclass(frozen=True)
class Method:
    sheep_model: str
    dog_controller: str
    defaults: Mapping[str, Any]


METHODS: dict[str, Method] = {
    "strombom_multi": Method(  # Strombom sheep + multi-dog collect/drive
        sheep_model="strombom",
        dog_controller="collect_drive_multi",
        defaults={**strombom.PAPER, **strombom.SHEPHERD_EXTENSIONS},
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
