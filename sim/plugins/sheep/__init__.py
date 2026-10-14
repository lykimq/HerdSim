"""Sheep motion models (how the flock moves each tick).

Each model is a ``step(state, config) -> state`` function that updates sheep
positions and velocities. The method's ``sheep_model`` key picks one from
SHEEP_MODELS. Dog decisions live under plugins.dogs.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from core.simulation_state import SimulationState

from . import kubo, strombom

SheepStep = Callable[[SimulationState, dict[str, Any]], SimulationState]

SHEEP_MODELS: dict[str, SheepStep] = {
    "strombom": strombom.step,
    "kubo": kubo.step,
}
