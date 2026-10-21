"""Kubo et al. 2022 parameters (Artif. Life Robot. 27: 416-427, Table 1).

``dt`` and the two speed caps are not in the paper; they come from a public
MATLAB port of the method, PatrickHup/Force-Based-Sheep-Herding-Algorithm,
src/main.m (dt = 0.05, speed caps 5 and 10, radius 60 for every range), and
are labelled as such. With dt = 0.05 a time limit of 10,000 ticks is the
paper's 500 s. Measured for the port's caps and step (2026-10-19, N = 50,
D = 2, seeds 2026-2028): sheep sit at the cap in 15-17% of sheep-ticks and
dogs never reach theirs; the finish time is insensitive to dt over 0.01-0.1
(67-83 s, at most 5 s apart for one seed).
"""

from __future__ import annotations

import math
from typing import Any

PAPER: dict[str, Any] = {
    # rs: sheep field of view, used for neighbour sheep and for dogs seen by a sheep.
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
    # Range of the dog-dog term (eq. 12 is a mean over the dogs in a dog's
    # field of view, whose size the paper never gives). Infinite: every other
    # dog counts, as in the paper's fixed-point analysis (eqs. 13-15, p.420),
    # which has the dog-dog term with no cutoff. A finite 20 (the sheep field
    # of view) pinned D = 2 dogs at the cutoff (measured median minimum dog
    # separation 20.1-20.3 against 50-52 without it); the MATLAB port used 60.
    "dog_repulsion_radius": math.inf,
    # Coverage below which the failure label dogs_out_of_range applies (drive task's
    # failure rules, sim/plugins/scenarios/drive_failures.py).
    # A working Kubo drive has coverage 0.1-0.2 (measured, N = 25-100), because the sheep flee
    # term K_s4 / d^2 = 12.5 at d = 20 exceeds the sheep speed cap 5 and holds them at the
    # edge of the 20-unit view; half of the lower value separates a stalled drive from that.
    "low_coverage": 0.05,
    # From the MATLAB port.
    "dt": 0.05,
    "sheep_speed_max": 5.0,
    "dog_speed_max": 10.0,
}
