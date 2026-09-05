#!/usr/bin/env python3
"""Run batch trials across seeds for one algorithm and export CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from algorithms.registry import algorithm_registry
from core.experiment_config import resolve_experiment_config
from core.simulation_runner import SimulationRunner
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry


def parse_seeds(raw: str) -> list[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="HerdSim batch runner")
    parser.add_argument("--algorithm", default="strombom")
    parser.add_argument("--scenario", default="drive_to_goal")
    parser.add_argument("--preset", default="paper", choices=["paper", "scenario", "custom"])
    parser.add_argument("--seeds", default="1,2,3,4,5")
    parser.add_argument("--n-sheep", type=int, default=None)
    parser.add_argument("--n-shepherds", type=int, default=None)
    parser.add_argument("--out", default="results/batch.csv")
    args = parser.parse_args()

    algorithm = algorithm_registry.get(args.algorithm)
    scenario = scenario_registry.get(args.scenario)
    rows = []

    for seed in parse_seeds(args.seeds):
        config = resolve_experiment_config(
            algorithm,
            scenario,
            preset=args.preset,
            num_sheep=args.n_sheep,
            num_shepherds=args.n_shepherds,
        )
        runner = SimulationRunner(
            algorithm=algorithm,
            scenario=scenario,
            metrics=metric_registry.get_all(),
            config=config,
            seed=seed,
        )
        result = runner.run()
        summary = {
            "algorithm": args.algorithm,
            "scenario": args.scenario,
            "preset": args.preset,
            "seed": seed,
            "n_sheep": config["n_sheep"],
            "n_shepherds": config["n_shepherds"],
            "success": result.success,
            "total_ticks": result.total_ticks,
        }
        if not result.history.empty:
            final = result.history.iloc[-1].to_dict()
            summary.update({k: v for k, v in final.items() if k != "tick"})
        rows.append(summary)
        print(
            f"seed={seed} success={result.success} ticks={result.total_ticks}"
        )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
