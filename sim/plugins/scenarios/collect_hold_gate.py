"""Collect, hold, then exit through a right-wall gate (Phase 8 task)."""

from __future__ import annotations

from typing import Any

import numpy as np
from core.simulation_state import SimulationState
from core.world import GoalZone, World

from .base import BaseScenario

PHASE_COLLECT = "collect"
PHASE_HOLD = "hold"
PHASE_EXIT = "exit"


def hold_radius_for_n(
    n_sheep: int,
    *,
    scale: float = 2.5,
    radius_min: float = 23.0,
    radius_max: float = 27.0,
) -> float:
    """Draft-style containment radius: clamp(scale * sqrt(N), min, max)."""
    return float(
        np.clip(float(scale) * float(np.sqrt(max(int(n_sheep), 1))), radius_min, radius_max)
    )


class CollectHoldGateScenario(BaseScenario):
    """Gather into a hold disk, hold for N ticks, then push all sheep out the gate."""

    @property
    def id(self) -> str:
        return "collect_hold_gate"

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            "n_sheep": 50,
            "n_shepherds": 1,
            "world_width": 500.0,
            "world_height": 500.0,
            "goal_center": [250.0, 250.0],
            "goal_radius": 25.0,
            "initial_spread": 30.0,
            "shepherd_start_offset": 50.0,
            "shepherd_jitter": 5.0,
            "max_ticks": 10000,
            "success_fraction": 1.0,
            "hold_ticks": 800,
            "gate_half_width": 30.0,
            "hold_radius_scale": 2.5,
            "hold_radius_min": 23.0,
            "hold_radius_max": 27.0,
        }

    def create_world(self, config: dict[str, Any]) -> World:
        width = float(config.get("world_width", 500.0))
        height = float(config.get("world_height", 500.0))
        n_sheep = int(config.get("n_sheep", 50))
        hold_center = np.array(
            config.get("hold_center", config.get("goal_center", [250.0, 250.0])),
            dtype=float,
        )
        if "goal_radius" in config and config.get("hold_radius_scale") is None:
            hold_radius = float(config["goal_radius"])
        else:
            hold_radius = hold_radius_for_n(
                n_sheep,
                scale=float(config.get("hold_radius_scale", 2.5)),
                radius_min=float(config.get("hold_radius_min", 23.0)),
                radius_max=float(config.get("hold_radius_max", 27.0)),
            )
        gate_half = float(config.get("gate_half_width", 30.0))
        return World(
            width=width,
            height=height,
            goal=GoalZone(center=hold_center, radius=hold_radius),
            gate_half_width=gate_half,
            gate_center_y=0.5 * height,
        )

    def initial_positions(
        self, config: dict[str, Any], rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        from core.world.layouts import generate_initial_positions, normalize_layout

        n_sheep = int(config.get("n_sheep", 50))
        n_shepherds = int(config.get("n_shepherds", 1))
        world_width = float(config.get("world_width", 500.0))
        world_height = float(config.get("world_height", 500.0))
        hold_center = np.array(
            config.get("hold_center", config.get("goal_center", [250.0, 250.0])),
            dtype=float,
        )
        spread = float(config.get("initial_spread", 30.0))
        layout = normalize_layout(str(config.get("initial_layout", "compact")))
        measurement_radius = float(config.get("measurement_radius", 5.0))
        r_a = float(config.get("r_a", 2.0))
        lost_threshold = r_a * (float(n_sheep) ** (2.0 / 3.0))
        sheep_pos = generate_initial_positions(
            n_sheep,
            layout,
            hold_center,
            rng,
            spread=spread,
            interaction_radius=measurement_radius,
            lost_threshold=lost_threshold,
            world_width=world_width,
            world_height=world_height,
        )

        # Dogs start left of the flock (opposite the right-wall gate).
        shepherd_offset = float(config.get("shepherd_start_offset", 50.0))
        shepherd_base = hold_center + np.array([-shepherd_offset, 0.0])
        jitter = float(config.get("shepherd_jitter", 5.0))
        shepherd_pos = shepherd_base + rng.uniform(-jitter, jitter, size=(n_shepherds, 2))
        shepherd_pos[:, 0] = np.clip(shepherd_pos[:, 0], 1.0, world_width - 1.0)
        shepherd_pos[:, 1] = np.clip(shepherd_pos[:, 1], 1.0, world_height - 1.0)
        return sheep_pos, shepherd_pos

    def _update_phase(self, state: SimulationState, config: dict[str, Any]) -> None:
        meta = state.metadata
        phase = str(meta.get("chg_phase", PHASE_COLLECT))
        hold_ticks = int(config.get("hold_ticks", 800))
        goal = state.world.goal
        if goal is None:
            return
        contained = bool(np.all(goal.contains(state.sheep_positions)))

        if phase == PHASE_COLLECT:
            if contained:
                meta["chg_phase"] = PHASE_HOLD
                meta["chg_hold_count"] = 1
            else:
                meta["chg_hold_count"] = 0
        elif phase == PHASE_HOLD:
            if contained:
                count = int(meta.get("chg_hold_count", 0)) + 1
                meta["chg_hold_count"] = count
                if count >= hold_ticks:
                    meta["chg_phase"] = PHASE_EXIT
                    meta["chg_hold_complete"] = True
            else:
                meta["chg_phase"] = PHASE_COLLECT
                meta["chg_hold_count"] = 0
        # EXIT: stay until timeout or success.

        order = {PHASE_COLLECT: 0, PHASE_HOLD: 1, PHASE_EXIT: 2}
        reached = str(meta.get("chg_phase", PHASE_COLLECT))
        prev_max = str(meta.get("chg_phase_max", PHASE_COLLECT))
        if order.get(reached, 0) >= order.get(prev_max, 0):
            meta["chg_phase_max"] = reached

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        self._update_phase(state, config)
        if not bool(state.metadata.get("chg_hold_complete", False)):
            return False
        # Exited: past the right wall through the gate opening.
        exited = state.sheep_positions[:, 0] >= float(state.world.width)
        return bool(np.all(exited))

    def max_ticks(self, config: dict[str, Any]) -> int:
        return int(config.get("max_ticks", 10000))
