"""Campaign orchestration for scaling protocols.

The Makefile and ``run/scripts/campaign.py`` call into this module. Each
protocol YAML remains the source of truth for output path, packages, and grid.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from services.scaling.layout import (
    PROTOCOLS_DIR,
    REPO_ROOT,
    load_protocol_spec,
    resolve_protocol_output,
)

SCRIPTS_DIR = REPO_ROOT / "run" / "scripts"


def find_protocol_path(name_or_path: str | Path) -> Path:
    """Resolve a protocol id or path to an absolute YAML path."""
    raw = Path(name_or_path)
    if raw.suffix.lower() in {".yaml", ".yml"}:
        if raw.is_file():
            return raw.resolve()
        candidate = PROTOCOLS_DIR / raw.name
        if candidate.is_file():
            return candidate.resolve()
        if not raw.is_absolute():
            alt = (REPO_ROOT / raw).resolve()
            if alt.is_file():
                return alt
        raise FileNotFoundError(f"Protocol YAML not found: {name_or_path}")

    stem = raw.name
    for candidate in (
        PROTOCOLS_DIR / f"{stem}.yaml",
        PROTOCOLS_DIR / f"{stem}.yml",
    ):
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(
        f"Protocol '{stem}' not found under {PROTOCOLS_DIR}"
    )


def load_campaign_protocol(name_or_path: str | Path) -> tuple[Path, dict[str, Any]]:
    path = find_protocol_path(name_or_path)
    return path, load_protocol_spec(path)


def resolve_upstream_trials(
    spec: dict[str, Any],
    *,
    override: Path | None = None,
) -> Path:
    """Trials used as the scout/source table for claim or T1.

    Prefer ``upstream_protocol`` (and optional ``upstream_trials`` file name).
    Default file is ``trials.csv``; Phase-1 T1 usually wants ``merged_trials.csv``.
    """
    if override is not None:
        path = Path(override)
        if not path.is_absolute():
            path = REPO_ROOT / path
        return path.resolve()

    upstream = spec.get("upstream_protocol")
    if upstream is None:
        raise ValueError(
            "Claim/T1 needs upstream_protocol in the YAML or --upstream-trials"
        )
    _, up_spec = load_campaign_protocol(str(upstream))
    up_out = resolve_protocol_output(up_spec)
    file_name = str(spec.get("upstream_trials", "trials.csv"))
    return (up_out / file_name).resolve()


def runner_kind(spec: dict[str, Any]) -> str:
    """Which trial runner a ``run`` verb should use."""
    explicit = spec.get("runner")
    if explicit in ("grid", "factor"):
        return str(explicit)
    if any(k in spec for k in ("sensing_ranges", "communications", "obs_modes")):
        return "factor"
    return "grid"


def _script_cmd(script: str, args: Sequence[str]) -> list[str]:
    return [sys.executable, str(SCRIPTS_DIR / script), *args]


def _run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)


def _override_flags(args: argparse.Namespace, *, kind: str) -> list[str]:
    flags: list[str] = []
    if kind == "factor":
        if getattr(args, "methods", None) and len(args.methods) == 1:
            flags.extend(["--method", args.methods[0]])
        if getattr(args, "n", None):
            flags.extend(["--n", *[str(x) for x in args.n]])
        if getattr(args, "d", None):
            flags.extend(["--d", *[str(x) for x in args.d]])
        if getattr(args, "seeds", None) is not None:
            flags.extend(["--seeds", str(args.seeds)])
        if getattr(args, "no_resume", False):
            flags.append("--no-resume")
        return flags

    if getattr(args, "methods", None):
        flags.extend(["--methods", *args.methods])
    if getattr(args, "layouts", None):
        flags.extend(["--layouts", *args.layouts])
    if getattr(args, "n", None):
        flags.extend(["--n", *[str(x) for x in args.n]])
    if getattr(args, "d", None):
        flags.extend(["--d", *[str(x) for x in args.d]])
    if getattr(args, "seeds", None) is not None:
        flags.extend(["--seeds", str(args.seeds)])
    if getattr(args, "max_ticks", None) is not None:
        flags.extend(["--max-ticks", str(args.max_ticks)])
    if getattr(args, "no_timeseries", False):
        flags.append("--no-timeseries")
    if getattr(args, "no_resume", False):
        flags.append("--no-resume")
    return flags


def run_campaign(args: argparse.Namespace) -> None:
    verb = str(args.verb)
    path, spec = load_campaign_protocol(args.protocol)
    output = (
        Path(args.output).resolve()
        if args.output is not None
        else resolve_protocol_output(spec)
    )
    output.mkdir(parents=True, exist_ok=True)
    workers = str(int(args.workers))

    if verb == "run":
        if str(spec.get("seed_mode", "scout")) == "claim":
            raise SystemExit(
                f"Protocol {spec['protocol_id']} has seed_mode=claim; "
                "use claim-reseed or t1, not run"
            )
        kind = runner_kind(spec)
        script = "run_factor_sweep.py" if kind == "factor" else "run_grid.py"
        cmd = _script_cmd(
            script,
            [
                "--protocol",
                str(path),
                "--output",
                str(output),
                "--workers",
                workers,
                *_override_flags(args, kind=kind),
            ],
        )
        _run(cmd)
        return

    if verb in ("claim-plan", "claim-reseed"):
        upstream = resolve_upstream_trials(
            spec, override=getattr(args, "upstream_trials", None)
        )
        if not upstream.is_file():
            raise SystemExit(f"Upstream trials not found: {upstream}")
        cmd = _script_cmd(
            "plan_claim_cells.py",
            [
                "--scout-trials",
                str(upstream),
                "--protocol",
                str(path),
                "--output",
                str(output),
            ],
        )
        if verb == "claim-plan":
            cmd.append("--plan-only")
        else:
            cmd.extend(["--workers", workers])
            if args.no_timeseries:
                cmd.append("--no-timeseries")
            if args.no_resume:
                cmd.append("--no-resume")
        _run(cmd)
        return

    if verb in ("t1-plan", "t1"):
        upstream = resolve_upstream_trials(
            spec, override=getattr(args, "upstream_trials", None)
        )
        if not upstream.is_file():
            raise SystemExit(f"Upstream trials not found: {upstream}")
        cmd = _script_cmd(
            "plan_t1_cells.py",
            [
                "--trials",
                str(upstream),
                "--protocol",
                str(path),
                "--output",
                str(output),
            ],
        )
        if verb == "t1-plan":
            cmd.append("--plan-only")
        else:
            cmd.extend(["--workers", workers])
            if args.no_timeseries:
                cmd.append("--no-timeseries")
            if args.no_resume:
                cmd.append("--no-resume")
        _run(cmd)
        return

    raise SystemExit(f"Unknown verb: {verb}")


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
            "t1-plan",
            "t1",
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
        help="Override upstream trials.csv for claim/T1",
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

  uv run scaling/scripts/campaign.py <verb> --protocol <id> [options]

Verbs:
  run            Scout/smoke grid or factor sweep (from protocol)
  claim-plan     Write claim windows from upstream scout (no trials)
  claim-reseed   100-seed reseed on those windows
  t1-plan        Write overcrowding cells from upstream trials
  t1             Run T1 at time_limit_t1

Protocol id resolves under scaling/configs/protocols/<id>.yaml.
Claim/T1 YAMLs set upstream_protocol (and optional upstream_trials).

Make wrappers: make -C scaling help
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
