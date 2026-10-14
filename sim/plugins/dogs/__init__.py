"""Dog controllers (how the shepherds move each tick).

Each controller is a ``step(state, observations, config) -> state`` function.
Controllers use ``observations`` for sensing and write shepherd positions,
velocities, and metadata on the state. The method's ``dog_controller`` key
picks one from DOG_CONTROLLERS.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from core.observation import ShepherdObservation
from core.simulation_state import SimulationState

from . import collect_drive_multi, fat, kubo_forces

DogStep = Callable[[SimulationState, list[ShepherdObservation], dict[str, Any]], SimulationState]

DOG_CONTROLLERS: dict[str, DogStep] = {
    "collect_drive_multi": collect_drive_multi.step,
    "kubo_forces": kubo_forces.step,
    "fat": fat.step,
}
