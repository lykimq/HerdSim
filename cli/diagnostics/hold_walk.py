"""How far does a flock walk while the dogs withdraw? Replays stored holding trials to find out.

    uv run cli/diagnostics/hold_walk.py --out results/diagnostics/hold_walk.csv

In the holding task the dogs withdraw beyond r_s once the share is inside the goal, and the
flock keeps walking until no dog is within r_s of any sheep. That walk decides how large a goal
must be to hold the flock, so this measures it: the distance the flock centre moves from the
first tick with the share inside to the first tick no dog is within r_s, the time that takes,
and the distance of the farthest sheep from the centre at that tick.

It replays the cells of dmin_f99_hold_goal at a goal of 3.0 R_f, which is large enough that the
first sheep out does not end the hold mid-walk and call the dogs back. Only seeds the folder
holds are replayed, and each replay must reproduce its stored success and tick count, or the
run stops (services/replay.py). A trial whose dogs never clear r_s has no walk.

The summary estimates the goal a hold needs. A flock that enters with its last sheep at the near
edge and walks w keeps every sheep inside only if the goal radius exceeds about w / 2 plus the
distance of its farthest sheep from the centre; the median of that sum is printed per N. The
rows go to --out as CSV, the summaries to stdout as Markdown.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from docs.generate_docs.report.text import markdown  # noqa: E402
from services.replay import (  # noqa: E402
    ReplayJob,
    describe_cell_seed,
    open_run,
    replay_trial,
    run_replays,
    write_replays,
)
from sim.core.simulation_state import SimulationState  # noqa: E402

METHOD = "strombom_multi"
FOLDER = "dmin_f99_hold_goal"


class Walk:
    """Flock centre at the first tick with the share inside and at the first tick after it
    with every dog beyond r_s."""

    def __init__(self, reach: float) -> None:
        self.reach = reach
        self.start: tuple[int, np.ndarray] | None = None
        self.end: tuple[int, np.ndarray, float] | None = None

    def add(self, state: SimulationState) -> None:
        sheep = state.sheep_positions
        if self.start is None:
            if state.world.goal.reached(sheep):
                self.start = (state.tick, sheep.mean(axis=0))
            return
        if self.end is not None:
            return
        gaps = np.linalg.norm(sheep[:, None] - state.shepherd_positions[None], axis=2)
        if gaps.min() > self.reach:
            centre = sheep.mean(axis=0)
            farthest = float(np.linalg.norm(sheep - centre, axis=1).max())
            self.end = (state.tick, centre, farthest)

    def summary(self, dt: float) -> dict[str, float]:
        if self.start is None or self.end is None:
            return {"walk": np.nan, "seconds": np.nan, "farthest": np.nan}
        return {
            "walk": float(np.linalg.norm(self.end[1] - self.start[1])),
            "seconds": (self.end[0] - self.start[0]) * dt,
            "farthest": self.end[2],
        }


def measure(job: ReplayJob) -> dict[str, Any]:
    """One unchanged replay with the walk measured."""
    walk = Walk(float(job.config["reaction_radius"]))
    result = replay_trial(job, on_tick=walk.add)
    return {**job.label, "success": result.success, **walk.summary(float(job.config["dt"]))}


def summary(table: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    """Medians per group over the replays whose dogs cleared r_s."""
    cleared = table.dropna(subset=["walk"]).assign(
        goal_needed=lambda t: t["walk"] / 2 + t["farthest"]
    )
    out = cleared.groupby(by)[["walk", "seconds", "farthest", "goal_needed"]].median()
    out.insert(0, "cleared", cleared.groupby(by).size())
    out.insert(0, "replays", table.groupby(by).size())
    return out.round(1).reset_index()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--goal", type=float, default=3.0, help="goal_radius_multiple level")
    parser.add_argument(
        "--layouts", nargs="+", default=["compact", "wide", "split", "outlier_rich"]
    )
    parser.add_argument("--n", nargs="+", type=int, default=[25, 50, 100])
    parser.add_argument("--d", nargs="+", type=int, default=[1, 2, 4, 8])
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    run = open_run(FOLDER)
    factors = (("goal_radius_multiple", args.goal),)
    jobs = [
        job
        for layout in args.layouts
        for n in args.n
        for d in args.d
        for job in run.jobs(METHOD, layout, n, d, args.seeds, factors)
    ]
    table = run_replays(measure, jobs, args.workers, describe_cell_seed)
    table = table.sort_values(["layout", "n", "d", "seed_index"])
    write_replays(table, args.out)
    print(markdown(summary(table, ["n"])))
    print()
    print(markdown(summary(table, ["n", "d"])))


if __name__ == "__main__":
    main()
