"""CLI: run factorial factor-grid experiments with provenance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.benchmark_runner import run_benchmark


def parse_grid(raw: str) -> list[dict]:
    """Parse 'key=v1,v2;key2=a,b' into sweep specs."""
    specs = []
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        key, values = part.split("=", 1)
        vals: list = []
        for item in values.split(","):
            item = item.strip()
            try:
                num = float(item)
                vals.append(int(num) if num.is_integer() else num)
            except ValueError:
                vals.append(item)
        specs.append({"key": key.strip(), "values": vals})
    return specs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instrument", default="strombom")
    parser.add_argument("--scenario", default="drive_to_goal")
    parser.add_argument("--preset", default="custom")
    parser.add_argument("--seeds", default="1,2,3")
    parser.add_argument(
        "--grid",
        required=True,
        help="Factor grid, e.g. n_sheep=20,50;n_shepherds=1,2,4",
    )
    parser.add_argument("--out-dir", default="results/factor_grid")
    parser.add_argument("--max-ticks", type=int, default=None)
    args = parser.parse_args()

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    sweep = parse_grid(args.grid)
    algorithm_params = {"max_ticks": args.max_ticks} if args.max_ticks else None
    payload = run_benchmark(
        instruments=[args.instrument],
        scenario_id=args.scenario,
        seeds=seeds,
        preset=args.preset,
        sweep=sweep,
        algorithm_params=algorithm_params,
    )
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows_path = out / "trials.csv"
    summary_path = out / "summary.json"
    pd.DataFrame(payload["rows"]).to_csv(rows_path, index=False)
    summary_path.write_text(json.dumps(payload["summary"], indent=2), encoding="utf-8")
    meta = {
        "instrument": args.instrument,
        "scenario": args.scenario,
        "preset": args.preset,
        "seeds": seeds,
        "grid": sweep,
        "n_trials": len(payload["rows"]),
    }
    (out / "provenance.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {rows_path} ({len(payload['rows'])} trials)")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
