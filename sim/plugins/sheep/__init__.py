"""Sheep motion models (how the flock moves each tick).

Plugins here implement BaseSheepDynamics and are selected by the sheep_model
factor. Dog decisions live under plugins.dogs; this package only updates sheep
positions and velocities.
"""

from .base import BaseSheepDynamics

__all__ = ["BaseSheepDynamics"]
