"""Why do more dogs slow the split layout? Replays stored trials with two changes to find out.

    uv run cli/diagnostics/split_diagnostic.py --out results/diagnostics/split_diagnostic.csv

On a flock that starts in three clusters, adding dogs past a few makes the drive slower. Two
causes were suspected: the collecting dogs all go to the same cluster, and dogs near a cluster
stand still under the paper's stop rule. This replays the stored trials with each cause
removed, and both, and compares.

It covers split N = 100 and 200, D = 2, 4, 8, 16, at 6 and 3 drive times (dmin_f99_m6,
dmin_f99_m3, 99 percent rule), 12 stored seeds per cell, in four versions of the team rule:

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
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from analysis.results import markdown  # noqa: E402
from services.replay import ReplayJob, open_run, replay_trial, run_replays  # noqa: E402
from sim.methods.strombom.heuristics import collect_threshold  # noqa: E402

METHOD = "strombom_multi"
VERSIONS = {"base": (3.0, False), "stop": (1.0, False), "spread": (3.0, True), "both": (1.0, True)}


def run(job: ReplayJob) -> dict[str, Any]:
    result = replay_trial(job)
    return {
        **job.label,
        "success": result.success,
        "finish_seconds": result.total_ticks * float(job.config["dt"])
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
        stored_run = open_run(name)
        for n in (100, 200):
            for d in (2, 4, 8, 16):
                base = stored_run.config(METHOD, "split", n, d)
                stored = stored_run.outcomes(METHOD, "split", n, d)
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
                        jobs.append(ReplayJob(config, stored_run.master_seed + i, check, label))

    table = run_replays(
        run,
        jobs,
        args.workers,
        lambda r: f"{r['deadline']} N={r['n']} D={r['d']} {r['version']}",
    )
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
