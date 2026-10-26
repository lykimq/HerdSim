"""Strombom et al. 2014 parameters (J. R. Soc. Interface 11: 20140719, Table 1).

``PAPER`` holds the Table 1 values. ``SHEPHERD_EXTENSIONS`` holds the one HerdSim setting
the paper does not have.
"""

from __future__ import annotations

import math
from typing import Any

PAPER: dict[str, Any] = {
    # Sheep (agents)
    # Agent-agent interaction distance (eq. 4.1 cutoff); the shepherd rule also uses it
    # for f(N) = r_a N^(2/3), the Pc and Pd offsets and the 3 r_a stop distance.
    "r_a": 2.0,
    "rho_a": 2.0,  # relative strength of repulsion from other agents (eq. 4.2 weight)
    "r_s": 65.0,  # shepherd detection distance
    "rs_weight": 1.0,  # rho_s, strength of repulsion from the shepherd
    "c": 1.05,  # attraction to the n nearest neighbours
    "inertia": 0.5,  # h, weight on the previous heading
    "noise_strength": 0.3,  # e, angular noise (sheep and shepherd)
    "sheep_speed": 1.0,  # delta, displacement per tick
    "graze_move_prob": 0.05,  # p, probability of a grazing step
    # Number of nearest neighbours n. -1 means all N - 1 (the paper's global case); a
    # string like "0.25N" means ceil(0.25 N). More than N - 1 is an error.
    "n_neighbors": -1,
    # Shepherd
    "shepherd_speed": 1.5,  # delta_s
    "shepherd_stop_multiple": 3.0,  # speed 0 within 3 r_a of any sheep
}

# One tick is one time step of the paper.
SHEPHERD_EXTENSIONS: dict[str, Any] = {"dt": 1.0}


def resolve_n_neighbors(value: int | str, n_sheep: int) -> int:
    """Neighbour count for a flock of ``n_sheep``: -1 -> N - 1, "fN" -> ceil(f N).

    A count above N - 1 is an error, not clipped: n is a parameter of the rule, and a
    cell whose N cannot supply it is a different cell.
    """
    if isinstance(value, str):
        if not value.endswith("N"):
            raise ValueError(f"n_neighbors {value!r}: use an int, -1, or a fraction like '0.25N'")
        k = math.ceil(float(value[:-1]) * n_sheep)
    else:
        k = n_sheep - 1 if value == -1 else value
    if k < 1 and n_sheep > 1:
        raise ValueError(f"n_neighbors {value!r} gives {k} neighbours for N = {n_sheep}")
    if k > n_sheep - 1:
        raise ValueError(f"n_neighbors {value!r} asks for {k} neighbours but N = {n_sheep}")
    return k
