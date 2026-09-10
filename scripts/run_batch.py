#!/usr/bin/env python3
"""Run batch trials across seeds and export CSV/JSON via run_benchmark."""

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

    seeds = parse_seeds(args.seeds)
    request = {
        "algorithm_ids": [args.algorithm],
        "scenario_id": args.scenario,
        "preset": args.preset,
        "seeds": seeds,
        "num_sheep": args.n_sheep,
        "num_shepherds": args.n_shepherds,
    }
    payload = run_benchmark(
        algorithm_ids=[args.algorithm],
        scenario_id=args.scenario,
        seeds=seeds,
        preset=args.preset,
        num_sheep=args.n_sheep,
        num_shepherds=args.n_shepherds,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_to_csv(payload, request=request), encoding="utf-8")
    json_path = out_path.with_suffix(".json")
    package = build_report_package(payload, request=request)
    json_path.write_text(json.dumps(package, indent=2, default=str), encoding="utf-8")

    for row in payload["rows"]:
        print(
            f"seed={row['seed']} success={row['success']} ticks={row['total_ticks']}"
        )
    print(f"Wrote {out_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
