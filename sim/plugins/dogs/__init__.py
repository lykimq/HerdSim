"""Dog controller plugins."""

from plugins.dogs.adaptive import AdaptiveController
from plugins.dogs.collect_drive import CollectDriveController
from plugins.dogs.collect_drive_multi import CollectDriveMultiController
from plugins.dogs.communication_free import CommunicationFreeController
from plugins.dogs.fat import FatController
from plugins.dogs.kubo_forces import KuboDogController
from plugins.dogs.obstacle_aware_drive import ObstacleAwareDriveController
from plugins.dogs.policy_file import PolicyFileController
from plugins.dogs.v_formation import VFormationController

__all__ = [
    "CollectDriveController",
    "CollectDriveMultiController",
    "KuboDogController",
    "VFormationController",
    "ObstacleAwareDriveController",
    "FatController",
    "CommunicationFreeController",
    "AdaptiveController",
    "PolicyFileController",
]
