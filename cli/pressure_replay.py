"""Replay stored trials and record the pressure on the flock (analysis/pressure.py).

    uv run cli/pressure_replay.py dmin_f99_m6 --layouts wide outlier_rich --n 100 400 --seeds 12

For each layout and N, the cells replayed are D = 1, D_min, D_sat and the smallest tested D at
or above 2 D_sat, read from the folder's frontier_groups.csv (where D_sat is still open, its low
end). Seed i of a cell is replayed only if the folder holds it, and every replay must reproduce
the stored success and tick count, or the run stops. Each finished trial prints one line, so a
watcher can tell a stalled run from a slow one. The rows go to --out as CSV, the per-cell
summary to stdout as Markdown.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from analysis.dmin_tables import groups_table, read_table  # noqa: E402
from analysis.pressure import ReplayJob, pressure_table, replay  # noqa: E402
from cli.dmin_tables import folder_of, markdown  # noqa: E402
from services.cells import Cell, Group, cell_config  # noqa: E402
from services.pool import worker_pool  # noqa: E402
from services.protocol import load_protocol  # noqa: E402

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

    folder = folder_of(args.folder)
    protocol = load_protocol(args.folder, output=folder)
    radii = json.loads((folder / "calibration.json").read_text())["flock_radius"][METHOD]
    curves = groups_table(folder).set_index(["layout", "n"])
    trials = read_table(folder / "trials.csv")
    master = int(protocol.settings["master_seed"])

    jobs = []
    for layout in args.layouts:
        for n in args.n:
            key = f"{METHOD}|{layout}|N={n}"
            mine = trials[trials["group_key"] == key]
            tested = sorted(int(d) for d in mine["n_shepherds"].unique())
            for d, role in cells_to_replay(curves.loc[(layout, n)], tested).items():
                config = cell_config(protocol, Cell(Group(METHOD, layout, (), n), d), radii[str(n)])
                stored = mine[mine["n_shepherds"] == d]
                outcome = {
                    int(t["seed_index"]): (bool(t["success"]), int(t["total_ticks"]))
                    for _, t in stored.iterrows()
                }
                for i in [i for i in range(args.seeds) if i in outcome]:
                    label = {"layout": layout, "n": n, "d": d, "role": role, "seed_index": i}
                    jobs.append(ReplayJob(config, master + i, *outcome[i], label))
    print(f"{len(jobs)} replays", flush=True)

    rows = []
    with worker_pool(args.workers) as pool:
        futures = [pool.submit(replay, job) for job in jobs]
        for done, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows.append(row)
            where = f"{row['layout']} N={row['n']} D={row['d']} seed {row['seed_index']}"
            print(f"{done}/{len(jobs)} {where}", flush=True)
    table = pd.DataFrame(rows).sort_values(["layout", "n", "d", "seed_index"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.out, index=False)
    print(markdown(pressure_table(table).round(2)))


if __name__ == "__main__":
    main()
