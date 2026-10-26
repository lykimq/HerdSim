"""Default parameters for the Kubo et al. 2022 force-based herding model."""

from __future__ import annotations

import math
from typing import Any

PAPER: dict[str, Any] = {
    "sheep_radius": 20.0,  # Sheep sensing and interaction radius
    "K_s1": 10.0,  # Sheep-sheep repulsion gain
    "K_s2": 0.5,  # Sheep velocity alignment gain
    "K_s3": 2.0,  # Sheep-sheep attraction/cohesion gain
    "K_s4": 5000.0,  # Sheep repulsion away from dogs
    "K_f1": 10.0,  # Dog attraction toward target sheep
    "K_f2": 200.0,  # Dog standoff repulsion from target sheep
    "K_f3": 8.0,  # Dog repulsion away from goal
    "K_f4": 3000.0,  # Dog-dog mutual repulsion
}

NOT_IN_PAPER: dict[str, Any] = {
    # Infinite repulsion radius: all dogs mutually repel without distance cutoff.
    "dog_repulsion_radius": math.inf,
    # Coverage threshold below which dogs are labeled disconnected from the flock.
    "low_coverage": 0.05,
    # Simulation integration timestep and agent speed caps.
    "dt": 0.05,
    "sheep_speed_max": 5.0,
    "dog_speed_max": 10.0,
}
