"""Does a larger team put more pressure on the flock? Replays stored trials to find out.

    uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --layouts wide outlier_rich --n 100 400 \
        --seeds 12 --out results/diagnostics/pressure_dmin_f99_m6.csv

The trial rows don't say how close the dogs came to the sheep, so this runs the trials again
and measures it on every tick (analysis/pressure.py): how long each sheep spends fleeing a dog,
and how much of the flock flees at once.

For each layout and N it replays the cells at D = 1, D_min, D_sat and the smallest tested D at
or above 2 D_sat, taken from the folder's current frontier (where D_sat is still a range, its
low end). Only seeds the folder holds are replayed, and each replay must reproduce its stored
success and tick count, or the run stops (services/replay.py). The rows go to --out as CSV, the
per-cell summary to stdout as Markdown.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402

from analysis.dmin_tables import groups_table  # noqa: E402
from analysis.pressure import Pressure, pressure_table  # noqa: E402
from analysis.results import markdown  # noqa: E402
from services.protocol import results_folder  # noqa: E402
from services.replay import (  # noqa: E402
    ReplayJob,
    describe_cell_seed,
    open_run,
    replay_trial,
    run_replays,
    write_replays,
)

METHOD = "strombom_multi"


def cells_to_replay(curve: pd.Series, tested: list[int]) -> dict[int, str]:
    """D -> role, for D = 1, D_min, D_sat and the smallest tested D at or above 2 D_sat."""
    roles: dict[int, list[str]] = {1: ["1"]}
    if pd.notna(curve["d_min"]):
        roles.setdefault(int(curve["d_min"]), []).append("D_min")
    if pd.notna(curve["d_sat"]):
        sat = int(curve["d_sat"])
        roles.setdefault(sat, []).append("D_sat" + (" (open)" if curve["d_sat_undecided"] else ""))
        double = next((d for d in sorted(tested) if d >= 2 * sat), None)
        if double is not None:
            roles.setdefault(double, []).append("2 D_sat")
    return {d: ", ".join(r) for d, r in sorted(roles.items())}


def measure(job: ReplayJob) -> dict[str, Any]:
    """One unchanged replay with the pressure measures."""
    config = job.config
    pressure = Pressure(
        reach=float(config["reaction_radius"]),
        close=float(config["shepherd_stop_multiple"]) * float(config["r_a"]),
    )
    result = replay_trial(
        job, on_tick=lambda state: pressure.add(state.sheep_positions, state.shepherd_positions)
    )
    dt = float(config["dt"])
    return {
        **job.label,
        "success": result.success,
        "finish_seconds": result.total_ticks * dt,
        **pressure.summary(dt),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder")
    parser.add_argument("--layouts", nargs="+", default=["wide", "outlier_rich"])
    parser.add_argument("--n", nargs="+", type=int, default=[100, 400])
    parser.add_argument("--seeds", type=int, default=12)
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    run = open_run(args.folder)
    curves = groups_table(results_folder(args.folder)).set_index(["layout", "n"])
    jobs = []
    for layout in args.layouts:
        for n in args.n:
            tested = run.tested(METHOD, layout, n)
            for d, role in cells_to_replay(curves.loc[(layout, n)], tested).items():
                jobs += run.jobs(METHOD, layout, n, d, args.seeds, role=role)
    table = run_replays(measure, jobs, args.workers, describe_cell_seed)
    table = table.sort_values(["layout", "n", "d", "seed_index"])
    write_replays(table, args.out)
    print(markdown(pressure_table(table).round(2)))


if __name__ == "__main__":
    main()
