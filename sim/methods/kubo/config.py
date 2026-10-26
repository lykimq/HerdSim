"""Kubo et al. 2022 parameters (Artif. Life Robot. 27: 416-427, Table 1).

``dt`` and the two speed caps are not in the paper; they come from a public MATLAB port of
the method (PatrickHup/Force-Based-Sheep-Herding-Algorithm, src/main.m) and are labelled as
such. With dt = 0.05 a time limit of 10,000 ticks is the paper's 500 s. The finish time is
insensitive to dt over 0.01 to 0.1.
"""

from __future__ import annotations

import math
from typing import Any

PAPER: dict[str, Any] = {
    # rs: the sheep field of view, for neighbour sheep and for the dogs a sheep sees.
    "sheep_radius": 20.0,
    "K_s1": 10.0,  # sheep-sheep repulsion (eq. 3)
    "K_s2": 0.5,  # alignment (eq. 4)
    "K_s3": 2.0,  # attraction (eq. 5)
    "K_s4": 5000.0,  # repulsion from dogs (eq. 6)
    "K_f1": 10.0,  # dog toward the target sheep (eq. 9)
    "K_f2": 200.0,  # dog away from the target sheep (eq. 10)
    "K_f3": 8.0,  # dog away from the goal (eq. 11)
    "K_f4": 3000.0,  # dog-dog repulsion (eq. 12); the paper uses 1000 and 3000
}

NOT_IN_PAPER: dict[str, Any] = {
    # Range of the dog-dog term. Eq. 12 is a mean over the dogs in a dog's field of view,
    # whose size the paper never gives; its fixed-point analysis (eqs. 13-15) has the term
    # with no cutoff, so every other dog counts. A finite 20 pinned D = 2 dogs at the cutoff.
    "dog_repulsion_radius": math.inf,
    # Coverage below which the drive task labels a failure dogs_out_of_range
    # (sim/plugins/scenarios/drive_failures.py). A working Kubo drive has coverage 0.1 to
    # 0.2, because the flee term K_s4 / d^2 is 12.5 at d = 20, above the speed cap 5, so
    # the sheep hold the dogs at the edge of their view; half of that separates a stall.
    "low_coverage": 0.05,
    # From the MATLAB port.
    "dt": 0.05,
    "sheep_speed_max": 5.0,
    "dog_speed_max": 10.0,
}
