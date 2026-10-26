"""Default parameters for the Lama & di Bernardo 2024 distributed herding model."""

from __future__ import annotations

from typing import Any

PAPER: dict[str, Any] = {
    # Targets (eq. 1): dT/dt = sqrt(2 D) noise + beta sum over herders within lambda of
    # (lambda - distance) x unit vector away from the herder.
    "target_diffusion": 1.0,  # D, diffusion coefficient of the Brownian targets
    "repulsion_strength": 3.0,  # beta, push per unit of distance inside the repulsion radius
    "repulsion_radius": 2.5,  # lambda, a herder farther than this does not push
    # Herders (eqs. 2 to 4).
    "sensing_radius": 10.0,  # xi, a herder sees the targets and herders within this distance
    "herder_speed": 8.0,  # v_H, top speed, both when chasing and when returning to the origin
    "herder_gain": 5.0,  # alpha, gain toward the chase point, saturated at v_H
    "chase_offset": 1.25,  # delta = lambda / 2, the herder stands this far beyond its target
    # Forward Euler for the herders, Euler-Maruyama for the targets (p. 5).
    "dt": 0.03,
}


def target_top_speed(config: dict[str, Any]) -> float:
    """Calculate maximum target escaping speed v_T = beta * lambda."""
    return float(config["repulsion_strength"]) * float(config["repulsion_radius"])


def check(config: dict[str, Any]) -> None:
    """Validate parameter bounds: herder_speed must exceed target top speed (v_H > v_T)."""
    for key in ("repulsion_strength", "repulsion_radius", "herder_speed", "herder_gain"):
        if float(config[key]) <= 0.0:
            raise ValueError(f"{key} must be positive")
    if float(config["target_diffusion"]) < 0.0:
        raise ValueError("target_diffusion must not be negative")
    if float(config["sensing_radius"]) <= 0.0:
        raise ValueError("sensing_radius must be positive (inf for herders that see everything)")
    if float(config["chase_offset"]) < 0.0:
        raise ValueError("chase_offset must not be negative")
    if float(config["herder_speed"]) <= target_top_speed(config):
        raise ValueError(
            "herder_speed must exceed targets' top speed (repulsion_strength * repulsion_radius)"
        )
