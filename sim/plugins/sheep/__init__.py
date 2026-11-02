"""Sheep models keyed by ``sheep_model``: step, top_speed, prepare."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sim.core.simulation_state import SimulationState

from . import strombom


@dataclass(frozen=True)
class SheepModel:
    step: Callable[[SimulationState, dict[str, Any]], SimulationState]
    top_speed: Callable[[dict[str, Any]], float]
    prepare: Callable[[dict[str, Any]], dict[str, Any]]


SHEEP_MODELS: dict[str, SheepModel] = {
    "strombom": SheepModel(strombom.step, strombom.top_speed, strombom.prepare),
}
