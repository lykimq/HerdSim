"""Protocol path and naming conventions for campaign results.

Canonical layout:

    results/phase{k}/{protocol_slug}/
      protocol.yaml       # resolved protocol YAML for this run (extends merged)
      manifest.jsonl      # resume ledger (status=ok cells)
      provenance.json     # run stamp only (hash, seeds, metrics; no git / no protocol copy)
      status.json         # planned / done counts and timing
      trials.csv
      timeseries/         # one Parquet per cell when store_timeseries; stem == cell key
      packages/<letter>/  # analysis exports (A, D-G; written separately, not by the runner)
      README.md           # hand-written notes (the only file not auto-generated)

protocol_id in protocol.yaml must match the protocol_slug (folder name),
or the explicit id from protocols/configs/protocols/*.yaml.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from protocols.packaging.generated_notice import NOTICE_LINE, with_json_notice

# services/layout.py -> parents[1] = repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
PROTOCOLS_ROOT = REPO_ROOT / "protocols"
RESULTS_ROOT = REPO_ROOT / "results"
PROTOCOLS_DIR = PROTOCOLS_ROOT / "configs" / "protocols"
CANONICAL_PROTOCOL = PROTOCOLS_ROOT / "configs" / "canonical_grid.yaml"
CLI_DIR = REPO_ROOT / "cli"


def ensure_under_results(path: Path | str, *, label: str = "path") -> Path:
    """Require ``path`` under ``results/`` when it sits inside the repo.

    Paths outside the repository (for example pytest ``tmp_path``) are allowed
    so unit tests can write without touching ``results/``. Paths under the repo
    but outside ``results/`` (for example ``docs/report/``) are refused.
    """
    resolved = Path(path).resolve()
    results = RESULTS_ROOT.resolve()
    repo = REPO_ROOT.resolve()
    try:
        _ = resolved.relative_to(results)
        return resolved
    except ValueError:
        pass
    try:
        _ = resolved.relative_to(repo)
    except ValueError:
        return resolved
    raise ValueError(f"{label} must be under {results}, got {resolved}")


def load_protocol_spec(path: Path | str, *, _stack: tuple[Path, ...] = ()) -> dict[str, Any]:
    """Load a protocol YAML. Optional ``extends`` merges a parent file first.

    Child keys replace parent keys. ``protocol_id`` and ``output`` must end up
    set (usually on the child). Relative ``extends`` paths are resolved against
    the child file's directory.
    """
    path = Path(path).resolve()
    stack = _stack
    if path in stack:
        cycle = " -> ".join(str(p) for p in stack + (path,))
        raise ValueError(f"Protocol extends cycle: {cycle}")
    with path.open() as f:
        spec = yaml.safe_load(f) or {}
    if not isinstance(spec, dict):
        raise ValueError(f"Protocol spec must be a mapping: {path}")

    parent_name = spec.pop("extends", None)
    merged: dict[str, Any] = {}
    if parent_name is not None:
        parent_path = Path(str(parent_name))
        if not parent_path.is_absolute():
            parent_path = path.parent / parent_path
        merged = load_protocol_spec(parent_path, _stack=stack + (path,))
    merged.update(spec)

    if "protocol_id" not in merged:
        raise ValueError(f"Protocol spec missing protocol_id: {path}")
    if "output" not in merged:
        raise ValueError(f"Protocol spec missing output: {path}")
    return merged


def resolve_protocol_output(spec: dict[str, Any]) -> Path:
    """Resolve protocol output path relative to the repo root.

    Simulation and analysis outputs must land under ``results/``.
    """
    out = Path(spec["output"])
    if not out.is_absolute():
        out = REPO_ROOT / out
    return ensure_under_results(out, label="protocol output")


def find_protocol_path(name_or_path: str | Path) -> Path:
    """Resolve a protocol id (``phase1_scout``) or YAML path to an absolute path."""
    raw = Path(name_or_path)
    if raw.suffix == ".yaml":
        for candidate in (raw, PROTOCOLS_DIR / raw.name):
            if candidate.is_file():
                return candidate.resolve()
        raise FileNotFoundError(f"Protocol YAML not found: {name_or_path}")
    candidate = PROTOCOLS_DIR / f"{raw.name}.yaml"
    if candidate.is_file():
        return candidate.resolve()
    raise FileNotFoundError(f"Protocol '{raw.name}' not found under {PROTOCOLS_DIR}")


def load_campaign_protocol(name_or_path: str | Path) -> tuple[Path, dict[str, Any]]:
    path = find_protocol_path(name_or_path)
    return path, load_protocol_spec(path)


def load_run_protocol(
    name_or_path: str | Path,
) -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Protocol YAML path, its spec, the canonical grid, and canonical overlaid by spec.

    The overlaid ``effective`` dict is what cell expansion reads (task, grids,
    hold geometry on top of the frozen canonical defaults).
    """
    path, spec = load_campaign_protocol(name_or_path)
    canonical_path = Path(spec.get("canonical", CANONICAL_PROTOCOL))
    if not canonical_path.is_absolute():
        canonical_path = REPO_ROOT / canonical_path
    with canonical_path.open() as f:
        canonical: dict[str, Any] = yaml.safe_load(f)
    return path, spec, canonical, {**canonical, **spec}


def resolve_upstream_trials(
    spec: dict[str, Any],
    *,
    override: Path | None = None,
) -> Path:
    """Scout trials.csv that a claim protocol plans its windows from.

    Uses ``upstream_protocol`` (and optional ``upstream_trials`` file name, default
    ``trials.csv``) unless ``override`` is given.
    """
    if override is not None:
        path = Path(override)
        if not path.is_absolute():
            path = REPO_ROOT / path
        return path.resolve()

    upstream = spec.get("upstream_protocol")
    if upstream is None:
        raise ValueError("Claim needs upstream_protocol in the YAML or --upstream-trials")
    _, up_spec = load_campaign_protocol(str(upstream))
    up_out = resolve_protocol_output(up_spec)
    file_name = str(spec.get("upstream_trials", "trials.csv"))
    return (up_out / file_name).resolve()


def copy_protocol_spec(spec_path: Path | str, protocol_dir: Path | str) -> Path:
    """Write the resolved protocol YAML into the results folder.

    ``extends`` parents are merged so the archived file is self-contained.
    """
    src = Path(spec_path)
    dest = Path(protocol_dir) / "protocol.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    resolved = load_protocol_spec(src)
    body = yaml.safe_dump(resolved, sort_keys=False, default_flow_style=False)
    dest.write_text(f"{NOTICE_LINE}\n{body}")
    return dest


def read_status(protocol_dir: Path | str) -> dict[str, Any]:
    """Load status.json if present; empty dict otherwise."""
    path = Path(protocol_dir) / "status.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _elapsed_seconds(started_at: str | None, ended_at: str | None) -> float | None:
    """Wall seconds between two ISO timestamps; None if either is missing."""
    if not started_at or not ended_at:
        return None
    try:
        start = datetime.fromisoformat(started_at)
        end = datetime.fromisoformat(ended_at)
    except ValueError:
        return None
    return max(0.0, (end - start).total_seconds())


def write_status(
    protocol_dir: Path | str,
    *,
    protocol_id: str,
    n_planned: int,
    n_done: int,
    n_pending_at_start: int,
    started_at: str | None = None,
    updated_at: str | None = None,
    finished_at: str | None = None,
    running: bool | None = None,
    extra: dict[str, Any] | None = None,
) -> Path:
    """Write machine-readable protocol completion status.

    Timing fields are bookkeeping only. They do not change which cells run.
    ``started_at`` should be preserved across resumes by the caller.
    """
    out = Path(protocol_dir)
    out.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC).isoformat()
    started = started_at or now
    updated = updated_at or now
    complete = int(n_done) >= int(n_planned) and int(n_planned) > 0
    if running is None:
        running = not complete
    payload: dict[str, Any] = {
        "protocol_id": protocol_id,
        "n_planned": int(n_planned),
        "n_done": int(n_done),
        "n_pending_at_start": int(n_pending_at_start),
        "complete": complete,
        "running": bool(running),
        "started_at": started,
        "updated_at": updated,
        "elapsed_seconds": _elapsed_seconds(started, finished_at or updated),
        "trials_csv": "trials.csv",
        "manifest_jsonl": "manifest.jsonl",
    }
    if finished_at is not None:
        payload["finished_at"] = finished_at
    if extra:
        payload.update(extra)
    path = out / "status.json"
    path.write_text(json.dumps(with_json_notice(payload), indent=2) + "\n")
    return path
