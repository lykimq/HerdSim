"""Registries for sheep dynamics, dog controllers, and observation models."""

from __future__ import annotations

from typing import Callable, TypeVar

from core.dog_controller import BaseDogController
from core.observation import BaseObservationModel
from core.sheep_dynamics import BaseSheepDynamics

T = TypeVar("T")


class PluginRegistry:
    """Simple id -> factory registry."""

    def __init__(self, kind: str):
        self.kind = kind
        self._factories: dict[str, Callable[[], T]] = {}

    def register(self, plugin_id: str, factory: Callable[[], T]) -> None:
        self._factories[plugin_id] = factory

    def get(self, plugin_id: str) -> T:
        if plugin_id not in self._factories:
            available = list(self._factories.keys())
            raise KeyError(
                f"Unknown {self.kind} '{plugin_id}'. Available: {available}"
            )
        return self._factories[plugin_id]()

    def names(self) -> list[str]:
        return list(self._factories.keys())

    def list_all(self) -> list[dict]:
        items = []
        for plugin_id in self._factories:
            plugin = self.get(plugin_id)
            entry = {"id": plugin.id, "name": getattr(plugin, "name", plugin.id)}
            defaults = getattr(plugin, "default_config", None)
            if defaults is not None:
                entry["default_config"] = dict(defaults)
            items.append(entry)
        return items


sheep_dynamics_registry: PluginRegistry[BaseSheepDynamics] = PluginRegistry(
    "sheep_model"
)
dog_controller_registry: PluginRegistry[BaseDogController] = PluginRegistry(
    "dog_controller"
)
observation_registry: PluginRegistry[BaseObservationModel] = PluginRegistry(
    "observation_model"
)


def _register_builtins() -> None:
    from core.observation_models import (
        BearingOnlyObservation,
        GlobalObservation,
        IntermittentObservation,
        LocalPositionsObservation,
        NoisyBearingObservation,
    )
    from plugins.sheep.jadhav import JadhavSheepDynamics
    from plugins.sheep.kubo import KuboSheepDynamics
    from plugins.sheep.strombom import StrombomSheepDynamics
    from plugins.dogs.adaptive import AdaptiveController
    from plugins.dogs.collect_drive import CollectDriveController
    from plugins.dogs.collect_drive_multi import CollectDriveMultiController
    from plugins.dogs.communication_free import CommunicationFreeController
    from plugins.dogs.fat import FatController
    from plugins.dogs.kubo_forces import KuboDogController
    from plugins.dogs.obstacle_aware_drive import ObstacleAwareDriveController
    from plugins.dogs.policy_file import PolicyFileController
    from plugins.dogs.v_formation import VFormationController

    sheep_dynamics_registry.register("strombom", StrombomSheepDynamics)
    sheep_dynamics_registry.register("kubo", KuboSheepDynamics)
    sheep_dynamics_registry.register("jadhav", JadhavSheepDynamics)

    dog_controller_registry.register("collect_drive", CollectDriveController)
    dog_controller_registry.register("collect_drive_multi", CollectDriveMultiController)
    dog_controller_registry.register("kubo_forces", KuboDogController)
    dog_controller_registry.register("v_formation", VFormationController)
    dog_controller_registry.register(
        "obstacle_aware_drive", ObstacleAwareDriveController
    )
    dog_controller_registry.register("fat", FatController)
    dog_controller_registry.register(
        "communication_free", CommunicationFreeController
    )
    dog_controller_registry.register("adaptive", AdaptiveController)
    dog_controller_registry.register("policy_file", PolicyFileController)

    observation_registry.register("global", GlobalObservation)
    observation_registry.register("local_positions", LocalPositionsObservation)
    observation_registry.register("bearing_only", BearingOnlyObservation)
    observation_registry.register("noisy_bearing", NoisyBearingObservation)
    observation_registry.register("intermittent", IntermittentObservation)


_register_builtins()
