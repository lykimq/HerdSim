"""Registries for sheep dynamics, dog controllers, and observation models."""

from __future__ import annotations

from plugins.dogs.base import BaseDogController
from plugins.sheep.base import BaseSheepDynamics

from core.observation import BaseObservationModel
from core.registry import Registry

sheep_dynamics_registry: Registry[BaseSheepDynamics] = Registry("sheep_model")
dog_controller_registry: Registry[BaseDogController] = Registry("dog_controller")
observation_registry: Registry[BaseObservationModel] = Registry("observation_model")


def _register_builtins() -> None:
    from plugins.dogs.collect_drive_multi import CollectDriveMultiController
    from plugins.dogs.fat import FatController
    from plugins.dogs.kubo_forces import KuboDogController
    from plugins.sheep.kubo import KuboSheepDynamics
    from plugins.sheep.strombom import StrombomSheepDynamics

    from core.observation import (
        BearingOnlyObservation,
        GlobalObservation,
        LocalPositionsObservation,
    )

    sheep_dynamics_registry.register("strombom", StrombomSheepDynamics)
    sheep_dynamics_registry.register("kubo", KuboSheepDynamics)

    dog_controller_registry.register("collect_drive_multi", CollectDriveMultiController)
    dog_controller_registry.register("kubo_forces", KuboDogController)
    dog_controller_registry.register("fat", FatController)

    observation_registry.register("global", GlobalObservation)
    observation_registry.register("local_positions", LocalPositionsObservation)
    observation_registry.register("bearing_only", BearingOnlyObservation)


_register_builtins()
