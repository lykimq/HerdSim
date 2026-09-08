"""Fujioka/Hayashi-style V-formation multi-shepherd heuristic.

Sheep: Strombom 2014 update. Shepherds: Collect on outliers when dispersed
(Strombom multi-dog assignment); Drive on a V-arc behind the GCM vs goal when
cohesive (Fujioka and Hayashi V-formation shepherding).
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.heuristics import (
    collect_offset,
    compute_threshold,
    drive_offset,
    shepherd_step_toward,
)
from algorithms.v_formation.config import V_FORMATION_DEFAULTS
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.simulation_state import SimulationState


def _v_arc_offset(state: SimulationState, config: dict) -> float:
    raw = config.get("v_arc_offset", None)
    if raw is not None:
        return float(raw)
    return drive_offset(state, config)


def v_arc_targets(state: SimulationState, config: dict) -> list[np.ndarray]:
    """Shepherd stand-off points on a V-arc behind GCM relative to goal."""
    m = state.n_shepherds
    centroid = state.sheep_centroid
    goal = resolve_goal_center(state, config)
    offset = _v_arc_offset(state, config)
    spacing = np.radians(float(config.get("v_angle_deg", 35.0)))

    behind = centroid - goal
    bn = float(np.linalg.norm(behind))
    if bn < 1e-10:
        behind_u = np.array([1.0, 0.0])
    else:
        behind_u = behind / bn

    targets: list[np.ndarray] = []
    for i in range(m):
        ang = (i - (m - 1) / 2.0) * spacing
        c, s = float(np.cos(ang)), float(np.sin(ang))
        rotated = np.array(
            [
                behind_u[0] * c - behind_u[1] * s,
                behind_u[0] * s + behind_u[1] * c,
            ]
        )
        targets.append(centroid + rotated * offset)
    return targets


class VFormationAlgorithm(StrombomAlgorithm):
    """V-formation drive with Strombom Collect fallback for dispersed flocks."""

    def __init__(self) -> None:
        super().__init__()
        self._last_assignment_lines: list[dict[str, Any]] = []
        self._last_mode: str = "drive"

    @property
    def id(self) -> str:
        return "v_formation"

    @property
    def name(self) -> str:
        return "V-Formation"

    @property
    def default_config(self) -> dict[str, Any]:
        return V_FORMATION_DEFAULTS.copy()

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        new_state = super().step(state, config)
        metadata = dict(new_state.metadata)
        metadata["assignment_lines"] = list(self._last_assignment_lines)
        metadata["herding_mode"] = self._last_mode
        return SimulationState(
            tick=new_state.tick,
            sheep_positions=new_state.sheep_positions,
            sheep_velocities=new_state.sheep_velocities,
            shepherd_positions=new_state.shepherd_positions,
            shepherd_velocities=new_state.shepherd_velocities,
            world=new_state.world,
            rng=new_state.rng,
            metadata=metadata,
        )

    def _update_shepherds(self, state: SimulationState, config: dict) -> np.ndarray:
        velocities = np.zeros_like(state.shepherd_positions)
        self._last_assignment_lines = []
        self._last_mode = "drive"
        m = state.n_shepherds
        if m == 0 or state.n_sheep == 0:
            return velocities

        scale = float(config.get("collect_threshold_scale", 1.0))
        threshold = compute_threshold(state.n_sheep, config["r_a"]) * scale
        distances = state.distances_to_centroid()
        outliers = np.where(distances > threshold)[0]
        centroid = state.sheep_centroid
        c_offset = collect_offset(config)

        if len(outliers) == 0:
            targets = v_arc_targets(state, config)
            for i in range(m):
                target = targets[i]
                velocities[i] = shepherd_step_toward(state, config, i, target)
                self._last_assignment_lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": target.tolist(),
                        "mode": "drive",
                    }
                )
            return velocities

        self._last_mode = "collect"
        order = outliers[np.argsort(-distances[outliers])]
        for i in range(m):
            sheep_idx = int(order[i % len(order)])
            target = position_behind_target(
                state.sheep_positions[sheep_idx], centroid, c_offset
            )
            tangential = np.array(
                [
                    -(state.sheep_positions[sheep_idx][1] - centroid[1]),
                    state.sheep_positions[sheep_idx][0] - centroid[0],
                ]
            )
            tn = float(np.linalg.norm(tangential))
            if tn > 1e-10:
                target = target + (tangential / tn) * (4.0 * (i - (m - 1) / 2.0))
            velocities[i] = shepherd_step_toward(state, config, i, target)
            self._last_assignment_lines.append(
                {
                    "from": state.shepherd_positions[i].tolist(),
                    "to": state.sheep_positions[sheep_idx].tolist(),
                    "mode": "collect",
                    "sheep_index": sheep_idx,
                }
            )
        return velocities
