"""Campaign CLI for scaling protocols.

Each protocol YAML remains the source of truth for output path, packages, and grid.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from services.layout import (
    CLI_DIR,
    REPO_ROOT,
    load_campaign_protocol,
    resolve_protocol_output,
    resolve_upstream_trials,
)


def _run(script: str, args: Sequence[str]) -> None:
    cmd = [sys.executable, str(CLI_DIR / script), *args]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)


def _override_flags(args: argparse.Namespace) -> list[str]:
    """Pass manual grid overrides (smoke runs) through to run_grid.py."""
    flags: list[str] = []
    for name in ("methods", "layouts", "n", "d"):
        values = getattr(args, name)
        if values:
            flags.extend([f"--{name}", *[str(v) for v in values]])
    if args.seeds is not None:
        flags.extend(["--seeds", str(args.seeds)])
    if args.max_ticks is not None:
        flags.extend(["--max-ticks", str(args.max_ticks)])
    return flags


def run_campaign(args: argparse.Namespace) -> None:
    path, spec = load_campaign_protocol(args.protocol)
    output = (
        Path(args.output).resolve() if args.output is not None else resolve_protocol_output(spec)
    )
    common = ["--protocol", str(path), "--output", str(output), "--workers", str(args.workers)]
    if args.no_timeseries:
        common.append("--no-timeseries")

    if args.verb == "run":
        if str(spec.get("seed_mode", "scout")) == "claim":
            raise SystemExit(
                f"Protocol {spec['protocol_id']} has seed_mode=claim; "
                + "use claim-reseed, not run"
            )
        if args.no_resume:
            common.append("--no-resume")
        _run("run_grid.py", [*common, *_override_flags(args)])
        return

    # claim-plan / claim-reseed
    upstream = resolve_upstream_trials(spec, override=args.upstream_trials)
    if not upstream.is_file():
        raise SystemExit(f"Upstream trials not found: {upstream}")
    cmd = ["--scout-trials", str(upstream), *common]
    if args.verb == "claim-plan":
        cmd.append("--plan-only")
    elif args.no_resume:
        cmd.append("--no-resume")
    _run("plan_claim_cells.py", cmd)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a scaling campaign from a protocol YAML",
    )
    parser.add_argument(
        "verb",
        choices=(
            "run",
            "claim-plan",
            "claim-reseed",
            "help",
        ),
        help="Campaign action",
    )
    parser.add_argument(
        "--protocol",
        default=None,
        help="Protocol id (phase1_scout) or path to YAML",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--upstream-trials",
        type=Path,
        default=None,
        help="Override upstream trials.csv for claim-reseed",
    )
    parser.add_argument("--methods", nargs="+", default=None)
    parser.add_argument("--layouts", nargs="+", default=None)
    parser.add_argument("--n", nargs="+", type=int, default=None)
    parser.add_argument("--d", nargs="+", type=int, default=None)
    parser.add_argument("--seeds", type=int, default=None)
    parser.add_argument("--max-ticks", type=int, default=None)
    parser.add_argument("--no-timeseries", action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    return parser


def print_help() -> None:
    text = """HerdSim scaling campaigns

  uv run cli/campaign.py <verb> --protocol <id> [options]

Verbs:
  run            Scout/smoke grid or factor sweep (from protocol)
  claim-plan     Write claim windows from upstream scout (no trials)
  claim-reseed   100-seed reseed on those windows

Protocol id resolves under protocols/configs/protocols/<id>.yaml.
Claim YAMLs set upstream_protocol (and optional upstream_trials).
--methods/--layouts/--n/--d/--seeds/--max-ticks override the grid for smoke runs.
"""
    print(text)


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.verb == "help":
        print_help()
        return
    if not args.protocol:
        parser.error("--protocol is required")
    run_campaign(args)


if __name__ == "__main__":
    main()
