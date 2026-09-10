"""Empirical sheep calibration report stub for Jadhav-style models.

Compares idealized Strombom sheep vs Jadhav sheep under the same Collect/Drive
controller and reports success / cohesion differences as a model-validity map.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.benchmark_runner import run_benchmark


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", default="1,2,3")
    parser.add_argument("--out-dir", default="results/empirical_gap")
    args = parser.parse_args()
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]

    ideal = run_benchmark(
        instruments=["strombom"],
        scenario_id="drive_to_goal",
        seeds=seeds,
        preset="custom",
        num_sheep=14,
        num_shepherds=1,
    )
    empirical = run_benchmark(
        instruments=["flocking_dog"],
        scenario_id="drive_to_goal",
        seeds=seeds,
        preset="custom",
        num_sheep=14,
        num_shepherds=1,
    )

    def rate(payload):
        rows = payload["rows"]
        return sum(1 for r in rows if r["success"]) / max(len(rows), 1)

    report = {
        "ideal_strombom_success": rate(ideal),
        "jadhav_sheep_success": rate(empirical),
        "ranking_changed": rate(ideal) != rate(empirical),
        "note": (
            "Full UWB trajectory fitting can replace flocking_dog defaults; "
            "this report compares instrument-level empirical vs idealized sheep."
        ),
    }
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "model_validity.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
