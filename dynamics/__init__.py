"""Sheep motion models (how the flock moves each tick).

Plugins here implement BaseSheepDynamics and are selected by the sheep_model
factor. Dog decisions live under controllers/; this package only updates sheep
positions and velocities.
"""

from dynamics.jadhav import JadhavSheepDynamics
from dynamics.kubo import KuboSheepDynamics
from dynamics.strombom import StrombomSheepDynamics

__all__ = [
    "StrombomSheepDynamics",
    "KuboSheepDynamics",
    "JadhavSheepDynamics",
]
