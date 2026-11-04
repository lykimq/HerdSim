"""One trial of each experiment, run through the engine, and the row it stores.

Every trial applies the paper's repulsion between sheep at any distance from the dog
(``graze_repulsion``). HerdSim's readings where the paper is silent: sheep and dog start
uniform in their squares;
the dog's square sits one side toward the goal from the sheep's (for Fig. 3 that is exactly
the lower left quarter of section 4.1).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from sim.drive_task.layouts import BOX_LAYOUT
from sim.drive_task.task import box_setup
from sim.state import SimulationState
from sim.strombom.params import METHOD
from sim.trial import build_config, initial_state, run_trial

from . import settings as paper

Box = tuple[float, float]  # (low, high) on both axes


@dataclass(frozen=True)
class Fig3Trial:
    n_sheep: int
    n_neighbors: int
    seed: int
    success: bool
    steps: int  # time steps run; MAX_STEPS when the trial did not finish


@dataclass(frozen=True)
class DistanceTrial:
    distance: int  # the paper's l
    seed: int
    success: bool
    steps: int


def seed_of(n_sheep: int, index: int) -> int:
    """Seed of trial ``index`` at flock size N, shared by every n so the start is paired."""
    return 1000 * n_sheep + index


def distance_seed(distance: int, index: int) -> int:
    """Seed of trial ``index`` of the distance study at distance l."""
    return 1_000_000 + 1000 * distance + index


def dog_box(sheep_box: Box) -> Box:
    """The dog's square: the sheep's square moved one side toward the goal on both axes."""
    low, high = sheep_box
    return low - (high - low), low


def distance_box(distance: int) -> Box:
    """The distance study's start square: side 50, centred at l + 25 sqrt 2 on both axes."""
    half = paper.DISTANCE_BOX_SIDE / 2
    centre = distance + half * math.sqrt(2.0)
    return centre - half, centre + half


def paper_config(
    n_sheep: int,
    n_neighbors: int,
    r_s: float = paper.FIG3_DETECTION,
    sheep_box: Box = paper.SHEEP_BOX,
) -> dict[str, Any]:
    """The run config of the paper's task: HerdSim's defaults with the paper's settings."""
    setup = box_setup(sheep_box, dog_box(sheep_box), paper.DONE_DISTANCE)
    return build_config(
        method=METHOD,
        params={"r_s": r_s, "n_neighbors": n_neighbors, "graze_repulsion": True},
        setup={**setup, **paper.METRIC_SETUP, "max_ticks": paper.MAX_STEPS},
        n_sheep=n_sheep,
        n_shepherds=1,
        initial_layout=BOX_LAYOUT,
    )


def run_fig3_trial(
    n_sheep: int,
    n_neighbors: int,
    seed: int,
    on_step: Callable[[SimulationState], None] | None = None,
) -> Fig3Trial:
    """One Fig. 3 trial. ``on_step`` sees tick 0 and every later tick (for the animation)."""
    config = paper_config(n_sheep, n_neighbors)
    if on_step is not None:
        on_step(initial_state(config, seed))
    result = run_trial(config, seed, on_tick=on_step, history=False)
    return Fig3Trial(n_sheep, n_neighbors, seed, result.success, result.total_ticks)


def run_distance_trial(distance: int, seed: int) -> DistanceTrial:
    """One trial of the distance study: 46 sheep, the global case, Table 1's r_s."""
    n = paper.DISTANCE_FLOCK
    box = distance_box(distance)
    config = paper_config(n, n - 1, r_s=paper.TABLE1_DETECTION, sheep_box=box)
    result = run_trial(config, seed, history=False)
    return DistanceTrial(distance, seed, result.success, result.total_ticks)
