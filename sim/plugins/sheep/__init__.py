"""Sheep models, picked by the method's ``sheep_model``.

A model has a ``step`` that moves the flock one tick, a ``reaction_radius``
(how close a dog must be before a sheep reacts), used by the coverage metric,
and a ``prepare`` that checks the model's own settings when a run config is
built and returns any keys it derives from them.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sim.core.simulation_state import SimulationState
from sim.methods.kubo import forces as kubo_forces
from sim.methods.strombom import sheep as strombom_sheep

from . import kubo, strombom


@dataclass(frozen=True)
class SheepModel:
    step: Callable[[SimulationState, dict[str, Any]], SimulationState]
    reaction_radius: Callable[[dict[str, Any]], float]
    prepare: Callable[[dict[str, Any]], dict[str, Any]]


SHEEP_MODELS: dict[str, SheepModel] = {
    "strombom": SheepModel(strombom.step, strombom_sheep.reaction_radius, strombom.prepare),
    "kubo": SheepModel(kubo.step, kubo_forces.reaction_radius, kubo.prepare),
}
