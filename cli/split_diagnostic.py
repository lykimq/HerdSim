"""Why more dogs slow the split layout (plan design_min_max RQ-B1): replays with two changes.

    uv run cli/split_diagnostic.py --out results/diagnostics/split_diagnostic.csv

For split N = 100 and 200, D = 2, 4, 8, 16, at 6 and 3 drive times (dmin_f99_m6, dmin_f99_m3,
99 percent rule), 12 stored seeds per cell, four versions of the team rule:

- base: the rule as run; every base replay must reproduce its stored trial or the run stops;
- stop: the dog stop distance 3 r_a shortened to r_a (shepherd_stop_multiple 1), so fewer dogs
  stand still near a cluster;
- spread: the collecting dogs take outliers at least f(N) apart (collect_min_gap), so they do
  not all go to one cluster;
- both.

Each trial prints one line. The rows go to --out as CSV, the per-cell summary to stdout.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import as_completed
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from analysis.dmin_tables import read_table  # noqa: E402
from cli.dmin_tables import folder_of, markdown  # noqa: E402
from services.cells import Cell, Group, cell_config  # noqa: E402
from services.pool import worker_pool  # noqa: E402
from services.protocol import load_protocol  # noqa: E402
from sim.core.simulation_runner import run_trial  # noqa: E402
from sim.methods.strombom.heuristics import collect_threshold  # noqa: E402

VERSIONS = {"base": (3.0, False), "stop": (1.0, False), "spread": (3.0, True), "both": (1.0, True)}


def run(job: tuple[dict[str, Any], int, dict[str, Any], tuple[bool, int] | None]) -> dict[str, Any]:
    config, seed, label, stored = job
    result = run_trial(config, seed)
    if stored is not None and (result.success, result.total_ticks) != stored:
        raise RuntimeError(
            f"{label}: base replay gave {result.success, result.total_ticks}, stored {stored}"
        )
    return {
        **label,
        "success": result.success,
        "finish_seconds": result.total_ticks * float(config["dt"])
        if result.success
        else float("nan"),
        "dogs_stopped": float(result.history["dogs_stopped"].mean()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--seeds", type=int, default=12)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    jobs = []
    for name, deadline in (("dmin_f99_m6", 6), ("dmin_f99_m3", 3)):
        folder = folder_of(name)
        protocol = load_protocol(name, output=folder)
        radii = json.loads((folder / "calibration.json").read_text())["flock_radius"][
            "strombom_multi"
        ]
        trials = read_table(folder / "trials.csv")
        master = int(protocol.settings["master_seed"])
        for n in (100, 200):
            for d in (2, 4, 8, 16):
                base = cell_config(
                    protocol, Cell(Group("strombom_multi", "split", (), n), d), radii[str(n)]
                )
                mine = trials[
                    (trials["group_key"] == f"strombom_multi|split|N={n}")
                    & (trials["n_shepherds"] == d)
                ]
                stored = {
                    int(t["seed_index"]): (bool(t["success"]), int(t["total_ticks"]))
                    for _, t in mine.iterrows()
                }
                for version, (stop, spread) in VERSIONS.items():
                    config = {**base, "shepherd_stop_multiple": stop}
                    if spread:
                        config["collect_min_gap"] = collect_threshold(n, float(base["r_a"]))
                    for i in range(args.seeds):
                        label = {
                            "deadline": deadline,
                            "n": n,
                            "d": d,
                            "version": version,
                            "seed_index": i,
                        }
                        check = stored.get(i) if version == "base" else None
                        jobs.append((config, master + i, label, check))
    print(f"{len(jobs)} trials", flush=True)
    rows = []
    with worker_pool(args.workers) as pool:
        futures = [pool.submit(run, job) for job in jobs]
        for done, future in enumerate(as_completed(futures), start=1):
            row = future.result()
            rows.append(row)
            print(
                f"{done}/{len(jobs)} {row['deadline']} N={row['n']} D={row['d']} {row['version']}",
                flush=True,
            )
    table = pd.DataFrame(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.out, index=False)
    summary = (
        table.groupby(["deadline", "n", "d", "version"], sort=True)
        .agg(
            success=("success", "mean"),
            median_finish=("finish_seconds", "median"),
            stopped=("dogs_stopped", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print(markdown(summary))


if __name__ == "__main__":
    main()
