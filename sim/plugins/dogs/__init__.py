"""Dog controllers (``step(state, config) -> state``), keyed by ``dog_controller``."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sim.core.simulation_state import SimulationState

from . import collect_drive_multi

DogStep = Callable[[SimulationState, dict[str, Any]], SimulationState]

DOG_CONTROLLERS: dict[str, DogStep] = {
    "collect_drive_multi": collect_drive_multi.step,
}
