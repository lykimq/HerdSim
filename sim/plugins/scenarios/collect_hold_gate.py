"""Collect, hold, then exit through a right-wall gate (Phase 8 task).

The goal zone is the hold disk (``goal_center``, ``goal_radius``); the flock
starts on it. Sheep must stay in the disk for ``hold_ticks`` in a row, then all
leave through the gate centred on the right wall.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from core.simulation_state import SimulationState
from core.world import GoalZone, World
from core.world.layouts import place_dogs, place_flock

# Setup keys this task reads on top of the shared ones.
EXTRA_KEYS = ("hold_ticks", "gate_half_width")

PHASE_COLLECT = "collect"
PHASE_HOLD = "hold"
PHASE_EXIT = "exit"


def create_world(config: dict[str, Any]) -> World:
    return World(
        width=float(config["world_width"]),
        height=float(config["world_height"]),
        goal=GoalZone(
            center=np.array(config["goal_center"], dtype=float),
            radius=float(config["goal_radius"]),
        ),
        gate_half_width=float(config["gate_half_width"]),
    )


def initial_positions(
    config: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    # Flock starts on the hold disk; dogs start on the side away from the gate.
    hold_center = np.array(config["goal_center"], dtype=float)
    gate = create_world(config).gate_center
    sheep_pos = place_flock(config, hold_center, rng, keep_out_of_goal=False)
    shepherd_pos = place_dogs(config, hold_center, gate, rng)
    return sheep_pos, shepherd_pos


def _update_phase(state: SimulationState, config: dict[str, Any]) -> None:
    meta = state.metadata
    phase = str(meta.get("chg_phase", PHASE_COLLECT))
    hold_ticks = int(config["hold_ticks"])
    contained = bool(np.all(state.world.goal.contains(state.sheep_positions)))

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


def is_success(state: SimulationState, config: dict[str, Any]) -> bool:
    """Advance the collect / hold / exit phase, then check that all sheep exited."""
    _update_phase(state, config)
    if not bool(state.metadata.get("chg_hold_complete", False)):
        return False
    # Exited: past the right wall through the gate opening.
    exited = state.sheep_positions[:, 0] >= float(state.world.width)
    return bool(np.all(exited))
