"""Dog controller plugins."""

from controllers.adaptive import AdaptiveController
from controllers.collect_drive import CollectDriveController
from controllers.collect_drive_multi import CollectDriveMultiController
from controllers.communication_free import CommunicationFreeController
from controllers.fat import FatController
from controllers.kubo_forces import KuboDogController
from controllers.obstacle_aware_drive import ObstacleAwareDriveController
from controllers.policy_file import PolicyFileController
from controllers.v_formation import VFormationController

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
