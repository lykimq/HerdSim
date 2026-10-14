#!/usr/bin/env python3
"""CLI: run one scout protocol, either an N x D grid or an RQ5 information-factor sweep."""

from __future__ import annotations

import argparse
from pathlib import Path

from services.layout import copy_protocol_spec, load_run_protocol, resolve_protocol_output
from services.runner import expand_scaling_grid, run_scaling_grid


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a scaling grid or RQ5 factor sweep")
    parser.add_argument("--protocol", required=True, help="Protocol id or YAML path")
    parser.add_argument("--output", type=Path, default=None, help="Default: protocol output")
    parser.add_argument("--workers", type=int, default=1, help="Process pool size")
    # Manual overrides for smoke runs; protocol YAMLs normally set all of these.
    parser.add_argument("--methods", nargs="+", default=None)
    parser.add_argument("--layouts", nargs="+", default=None)
    parser.add_argument("--n", nargs="+", type=int, default=None, help="Flock sizes")
    parser.add_argument("--d", nargs="+", type=int, default=None, help="Shepherd counts")
    parser.add_argument("--seeds", type=int, default=None, help="Number of seeds")
    parser.add_argument("--max-ticks", type=int, default=None, help="Default: time_limit_t0")
    parser.add_argument("--no-timeseries", action="store_true", help="Skip Parquet timeseries")
    parser.add_argument("--no-resume", action="store_true", help="Rerun all cells")
    args = parser.parse_args()

    path, spec, canonical, effective = load_run_protocol(args.protocol)
    output = args.output or resolve_protocol_output(spec)
    factor = spec.get("runner") == "factor"
    if factor:
        # RQ5 sweep: one method and layout; obs_modes x sensing_ranges x communications.
        methods = args.methods or [spec["method"]]
        layouts = (args.layouts or spec["layouts"])[:1]
    else:
        methods = args.methods or spec.get("methods")
        layouts = args.layouts or spec.get("layouts")

    cells = expand_scaling_grid(
        effective,
        methods=methods,
        layouts=layouts,
        n_values=args.n or spec.get("flock_sizes"),
        d_values=args.d or spec.get("shepherd_counts"),
        n_seeds=args.seeds if args.seeds is not None else spec.get("seeds"),
        seed_mode=str(spec.get("seed_mode", "scout")),
        max_ticks=args.max_ticks,
        obs_modes=spec.get("obs_modes") if factor else None,
        sensing_ranges=spec.get("sensing_ranges") if factor else None,
        communications=spec.get("communications") if factor else None,
    )
    copy_protocol_spec(path, output)
    trials = run_scaling_grid(
        cells,
        output,
        # Factor sweeps were frozen hashing the canonical grid alone; keep that so
        # RQ5 provenance hashes stay comparable across stages.
        protocol=canonical if factor else effective,
        protocol_id=str(spec["protocol_id"]),
        max_workers=args.workers,
        store_timeseries=not args.no_timeseries and bool(spec.get("store_timeseries", True)),
        resume=not args.no_resume,
    )
    print(f"Wrote {len(trials)} trial rows to {output / 'trials.csv'}")


if __name__ == "__main__":
    main()
