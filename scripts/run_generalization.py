"""CLI: train-domain vs held-out generalization gap report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.benchmark_runner import run_benchmark


TRAIN_DOMAIN = {
    "scenario_id": "drive_to_goal",
    "algorithm_params": {
        "obs_mode": "global",
        "stubborn_fraction": 0.0,
        "noise_strength": 0.3,
    },
}

TEST_DOMAINS = {
    "obstacles": {
        "scenario_id": "obstacle_course",
        "algorithm_params": {"obs_mode": "global"},
    },
    "local_sensing": {
        "scenario_id": "drive_to_goal",
        "algorithm_params": {"obs_mode": "local_positions", "sensing_range": 40.0},
    },
    "heterogeneous": {
        "scenario_id": "drive_to_goal",
        "algorithm_params": {"obs_mode": "global", "stubborn_fraction": 0.5},
    },
    "noisy_bearing": {
        "scenario_id": "drive_to_goal",
        "algorithm_params": {
            "obs_mode": "noisy_bearing",
            "sensing_range": 50.0,
            "noise_sigma": 0.25,
        },
    },
}


def success_rate(payload: dict) -> float:
    rows = payload["rows"]
    if not rows:
        return 0.0
    return sum(1 for r in rows if r["success"]) / len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instruments", default="strombom,kubo,adaptive")
    parser.add_argument("--seeds", default="1,2,3")
    parser.add_argument("--n-sheep", type=int, default=20)
    parser.add_argument("--n-shepherds", type=int, default=2)
    parser.add_argument("--out-dir", default="results/generalization")
    args = parser.parse_args()

    instruments = [s.strip() for s in args.instruments.split(",") if s.strip()]
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    report = []
    for instrument in instruments:
        train = run_benchmark(
            instruments=[instrument],
            scenario_id=TRAIN_DOMAIN["scenario_id"],
            seeds=seeds,
            preset="custom",
            num_sheep=args.n_sheep,
            num_shepherds=args.n_shepherds,
            algorithm_params=TRAIN_DOMAIN["algorithm_params"],
        )
        p_train = success_rate(train)
        entry = {"instrument": instrument, "p_train": p_train, "tests": {}}
        for name, domain in TEST_DOMAINS.items():
            test = run_benchmark(
                instruments=[instrument],
                scenario_id=domain["scenario_id"],
                seeds=seeds,
                preset="custom",
                num_sheep=args.n_sheep,
                num_shepherds=args.n_shepherds,
                algorithm_params=domain["algorithm_params"],
            )
            p_test = success_rate(test)
            entry["tests"][name] = {
                "p_test": p_test,
                "generalization_gap": p_train - p_test,
            }
        report.append(entry)

    path = out / "generalization_report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
