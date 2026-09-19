"""Sheep motion models (how the flock moves each tick).

Plugins here implement BaseSheepDynamics and are selected by the sheep_model
factor. Dog decisions live under plugins.dogs; this package only updates sheep
positions and velocities.
"""

from plugins.sheep.jadhav import JadhavSheepDynamics
from plugins.sheep.kubo import KuboSheepDynamics
from plugins.sheep.strombom import StrombomSheepDynamics

__all__ = [
    "StrombomSheepDynamics",
    "KuboSheepDynamics",
    "JadhavSheepDynamics",
]
