#!/usr/bin/env python3
"""CLI: information-factor sweeps for RQ5 (Cap I10)."""

from __future__ import annotations

import argparse
from pathlib import Path

from services.scaling.layout import (
    PROTOCOLS_DIR,
    copy_protocol_spec,
    load_protocol_spec,
    protocol_path_for_spec,
    resolve_protocol_output,
)
from services.scaling.runner import (
    ScalingCell,
    load_canonical_protocol,
    run_scaling_grid,
    scaling_world_overrides,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RQ5 information factor sweep")
    parser.add_argument(
        "--protocol",
        type=Path,
        default=None,
        help="Default: scaling/configs/protocols/phase5_factor_sweep.yaml",
    )
    parser.add_argument(
        "--canonical",
        type=Path,
        default=None,
        help="Path to canonical_grid.yaml (default: from protocol YAML)",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--n", nargs="+", type=int, default=None)
    parser.add_argument("--d", nargs="+", type=int, default=None)
    parser.add_argument("--obs-modes", nargs="+", default=None)
    parser.add_argument(
        "--sensing-ranges",
        nargs="+",
        type=float,
        default=None,
        help="Absolute sensing ranges (range ladder); omit for obs_mode-only sweep",
    )
    parser.add_argument(
        "--communications",
        nargs="+",
        default=None,
        help="Communication ladder values; omit for obs_mode-only sweep",
    )
    parser.add_argument("--seeds", type=int, default=None)
    parser.add_argument("--method", default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--protocol-id", default=None)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    spec_path = args.protocol
    if spec_path is None:
        spec_path = PROTOCOLS_DIR / "phase5_factor_sweep.yaml"
    elif not spec_path.is_absolute() and not spec_path.exists():
        candidate = PROTOCOLS_DIR / spec_path.name
        if candidate.exists():
            spec_path = candidate
    spec = load_protocol_spec(spec_path) if spec_path.exists() else {}

    protocol_path = args.canonical
    if protocol_path is None and spec:
        protocol_path = protocol_path_for_spec(spec)
    protocol = load_canonical_protocol(protocol_path)

    output = args.output
    if output is None and spec:
        output = resolve_protocol_output(spec)
    if output is None:
        raise SystemExit("Provide --output or a protocol YAML with output")

    protocol_id = args.protocol_id or str(spec.get("protocol_id", "phase5_factor_sweep"))
    method = args.method or str(spec.get("method", "strombom_multi"))
    n_values = args.n or list(spec.get("flock_sizes") or [50, 100])
    d_values = args.d or list(spec.get("shepherd_counts") or [1, 2, 3, 4, 6, 10])
    obs_modes = args.obs_modes or list(
        spec.get("obs_modes") or ["bearing_only", "local_positions", "global"]
    )
    sensing_ranges = args.sensing_ranges
    if sensing_ranges is None and "sensing_ranges" in spec:
        sensing_ranges = [float(x) for x in spec["sensing_ranges"]]
    communications = args.communications
    if communications is None and "communications" in spec:
        communications = [str(x) for x in spec["communications"]]

    n_seeds = (
        args.seeds
        if args.seeds is not None
        else int(spec.get("seeds", protocol.get("scout_seeds", 30)))
    )
    layout = (list(spec.get("layouts") or ["compact"]) or ["compact"])[0]

    master = int(protocol.get("master_seed", 2026))
    max_ticks = int(protocol.get("time_limit_t0", 10000))
    seeds = [master + i for i in range(int(n_seeds))]

    # Default: obs ladder only. Optional range/comm expand as additional axes.
    obs_list = (
        list(obs_modes)
        if sensing_ranges is None and communications is None
        else (list(obs_modes) if args.obs_modes or "obs_modes" in spec else [None])
    )
    range_list = list(sensing_ranges) if sensing_ranges else [None]
    comm_list = list(communications) if communications else [None]

    cells: list[ScalingCell] = []
    for obs in obs_list:
        for sense in range_list:
            for comm in comm_list:
                for n in n_values:
                    arena = scaling_world_overrides(protocol, int(n))
                    for d in d_values:
                        for seed in seeds:
                            cells.append(
                                ScalingCell(
                                    n_sheep=int(n),
                                    n_shepherds=int(d),
                                    seed=int(seed),
                                    initial_layout=str(layout),
                                    method=method,
                                    obs_mode=str(obs) if obs is not None else None,
                                    sensing_range=float(sense) if sense is not None else None,
                                    communication=str(comm) if comm is not None else None,
                                    max_ticks=max_ticks,
                                    **arena,
                                )
                            )

    if spec_path.exists():
        copy_protocol_spec(spec_path, output)

    store_ts = bool(spec.get("store_timeseries", False))
    trials = run_scaling_grid(
        cells,
        output,
        protocol=protocol,
        protocol_id=protocol_id,
        max_workers=args.workers,
        store_timeseries=store_ts,
        resume=not args.no_resume,
    )
    print(f"Wrote {len(trials)} trial rows to {output / 'trials.csv'}")


if __name__ == "__main__":
    main()
