#!/usr/bin/env python3
"""CLI: run scaling N x D protocols (Cap I1)."""

from __future__ import annotations

import argparse
from pathlib import Path

from services.scaling.layout import (
    PROTOCOLS_DIR,
    copy_protocol_spec,
    load_protocol_spec,
    package_output_dir,
    protocol_path_for_spec,
    resolve_protocol_output,
)
from services.scaling.runner import (
    expand_scaling_grid,
    load_canonical_protocol,
    run_scaling_grid,
)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--protocol",
        type=Path,
        default=None,
        help="Protocol YAML under scaling/configs/protocols/ (sets output, grid, id)",
    )
    parser.add_argument(
        "--protocol",
        type=Path,
        default=None,
        help="Path to canonical_grid.yaml (default: from protocol or scaling/configs)",
    )
    parser.add_argument("--output", type=Path, default=None, help="Output directory")
    parser.add_argument(
        "--methods",
        nargs="+",
        default=None,
        help="Methods to run (default: baseline_method from protocol)",
    )
    parser.add_argument(
        "--layouts",
        nargs="+",
        default=None,
        help="X0 families (default: protocol x0_families)",
    )
    parser.add_argument("--n", nargs="+", type=int, default=None, help="Flock sizes")
    parser.add_argument("--d", nargs="+", type=int, default=None, help="Shepherd counts")
    parser.add_argument("--seeds", type=int, default=None, help="Override number of seeds")
    parser.add_argument(
        "--seed-mode",
        choices=("scout", "claim"),
        default=None,
        help="Use scout_seeds or claim_grade_seeds from protocol",
    )
    parser.add_argument("--workers", type=int, default=1, help="Process pool size")
    parser.add_argument(
        "--max-ticks",
        type=int,
        default=None,
        help="Override protocol time_limit_t0 per cell",
    )
    parser.add_argument(
        "--no-timeseries",
        action="store_true",
        help="Skip per-trial Parquet timeseries writes",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Ignore existing manifest and rerun all cells",
    )
    parser.add_argument("--protocol-id", default=None)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a scaling grid")
    _add_common_args(parser)
    args = parser.parse_args()

    spec: dict | None = None
    spec_path: Path | None = None
    if args.protocol is not None:
        spec_path = args.protocol
        if not spec_path.is_absolute() and not spec_path.exists():
            candidate = PROTOCOLS_DIR / spec_path.name
            if candidate.exists():
                spec_path = candidate
        spec = load_protocol_spec(spec_path)

    protocol_path = args.protocol
    if protocol_path is None and spec is not None:
        protocol_path = protocol_path_for_spec(spec)
    protocol = load_canonical_protocol(protocol_path)

    output = args.output
    if output is None and spec is not None:
        output = resolve_protocol_output(spec)
    if output is None:
        raise SystemExit("Provide --output or --protocol with an output field")

    protocol_id = args.protocol_id
    if protocol_id is None and spec is not None:
        protocol_id = str(spec["protocol_id"])
    if protocol_id is None:
        protocol_id = output.name

    methods = args.methods
    layouts = args.layouts
    n_values = args.n
    d_values = args.d
    n_seeds = args.seeds
    seed_mode = args.seed_mode or "scout"
    store_timeseries = not args.no_timeseries

    if spec is not None:
        methods = methods or list(spec.get("methods") or [])
        layouts = layouts or list(spec.get("layouts") or [])
        n_values = n_values or list(spec.get("flock_sizes") or [])
        d_values = d_values or list(spec.get("shepherd_counts") or [])
        if n_seeds is None and "seeds" in spec:
            n_seeds = int(spec["seeds"])
        if args.seed_mode is None and "seed_mode" in spec:
            seed_mode = str(spec["seed_mode"])
        if "store_timeseries" in spec and not args.no_timeseries:
            store_timeseries = bool(spec["store_timeseries"])

    cells = expand_scaling_grid(
        protocol,
        methods=methods or None,
        layouts=layouts or None,
        n_values=n_values or None,
        d_values=d_values or None,
        n_seeds=n_seeds,
        seed_mode=seed_mode,
        max_ticks=args.max_ticks,
    )
    if spec_path is not None:
        copy_protocol_spec(spec_path, output)

    trials = run_scaling_grid(
        cells,
        output,
        protocol=protocol,
        protocol_id=protocol_id,
        max_workers=args.workers,
        store_timeseries=store_timeseries,
        resume=not args.no_resume,
    )
    print(f"Wrote {len(trials)} trial rows to {output / 'trials.csv'}")
    packages = list((spec or {}).get("packages") or [])
    if packages:
        print(
            "Suggested analyse paths: "
            + ", ".join(str(package_output_dir(output, p)) for p in packages)
        )


if __name__ == "__main__":
    main()
