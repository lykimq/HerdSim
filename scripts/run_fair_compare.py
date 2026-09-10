#!/usr/bin/env python3
"""Fair multi-model comparison batch using the Analytics benchmark runner.

Locks shared sheep/dog counts across algorithms (custom-style overrides) and
writes JSON + CSV with full provenance. Prefer this over paper preset when
comparing Strombom, Kubo, and Flocking Dog.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.benchmark_report import build_report_package, report_to_csv
from api.benchmark_runner import run_benchmark


def parse_seeds(raw: str) -> list[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def parse_algorithms(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="HerdSim fair comparison batch (shared N/M, outcome+trajectory schema)"
    )
    parser.add_argument(
        "--algorithms",
        default="strombom,kubo,flocking_dog",
        help="Comma-separated algorithm ids",
    )
    parser.add_argument("--scenario", default="drive_to_goal")
    parser.add_argument(
        "--preset",
        default="custom",
        choices=["paper", "scenario", "custom"],
        help="Use custom (default) with --n-sheep/--n-shepherds for fair comparison",
    )
    parser.add_argument(
        "--seeds",
        default=",".join(str(i) for i in range(1, 31)),
        help="Comma-separated seeds (default 1..30)",
    )
    parser.add_argument("--n-sheep", type=int, default=40)
    parser.add_argument("--n-shepherds", type=int, default=4)
    parser.add_argument("--out-dir", default="results/fair_compare")
    args = parser.parse_args()

    algorithm_ids = parse_algorithms(args.algorithms)
    seeds = parse_seeds(args.seeds)
    request = {
        "algorithm_ids": algorithm_ids,
        "scenario_id": args.scenario,
        "preset": args.preset,
        "seeds": seeds,
        "num_sheep": args.n_sheep,
        "num_shepherds": args.n_shepherds,
    }
    payload = run_benchmark(
        algorithm_ids=algorithm_ids,
        scenario_id=args.scenario,
        seeds=seeds,
        preset=args.preset,
        num_sheep=args.n_sheep,
        num_shepherds=args.n_shepherds,
    )
    package = build_report_package(payload, request=request)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "report.json"
    csv_path = out_dir / "trials.csv"
    json_path.write_text(json.dumps(package, indent=2, default=str), encoding="utf-8")
    csv_path.write_text(report_to_csv(payload, request=request), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")
    for row in payload["summary"]:
        print(
            f"{row['algorithm']}: success={row['success_rate']:.1%} "
            f"failure={row['failure_rate']:.1%} "
            f"median_ticks={row.get('median_ticks_success')} "
            f"auc_cohesion={row.get('mean_auc_cohesion')} "
            f"ctrl_eff={row.get('mean_control_efficiency')}"
        )


if __name__ == "__main__":
    main()
