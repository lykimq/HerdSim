"""Dog controllers, picked by the method's ``dog_controller``.

A controller is a function ``step(state, config) -> state`` that moves the dogs for one tick
and writes their positions and velocities. Every dog knows the position of every sheep and of
every other dog.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sim.core.simulation_state import SimulationState

from . import collect_drive_multi, fat, independent, kubo_forces

DogStep = Callable[[SimulationState, dict[str, Any]], SimulationState]

DOG_CONTROLLERS: dict[str, DogStep] = {
    "collect_drive_multi": collect_drive_multi.step,
    "kubo_forces": kubo_forces.step,
    "fat": fat.step,
    "independent": independent.step,
}
