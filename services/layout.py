"""Protocol path and naming conventions for campaign results.

Canonical layout:

    results/phase{k}/{protocol_slug}/
      protocol.yaml       # frozen subset used for this run (copied)
      manifest.jsonl      # resume ledger (status=ok cells)
      provenance.json     # run stamp only (hash, seeds, metrics; no git / no protocol copy)
      status.json         # planned / done counts
      trials.csv
      timeseries/         # one file per cell; stem == cell key
      packages/{a-g}/     # analysis exports (written separately, not by the runner)
      README.md           # folder index and hand-written notes

protocol_id in protocol.yaml must match the protocol_slug (folder name),
or the explicit id from protocols/configs/protocols/*.yaml.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from protocols.packaging.generated_notice import with_json_notice, yaml_banner_line

# services/layout.py -> parents[1] = repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
PROTOCOLS_ROOT = REPO_ROOT / "protocols"
RESULTS_ROOT = REPO_ROOT / "results"
PROTOCOLS_DIR = PROTOCOLS_ROOT / "configs" / "protocols"
CANONICAL_PROTOCOL = PROTOCOLS_ROOT / "configs" / "canonical_grid.yaml"
CLI_DIR = REPO_ROOT / "cli"

_PACKAGE_LETTER_RE = re.compile(r"^[A-Ga-g]$")


def package_output_dir(protocol_dir: Path | str, package: str) -> Path:
    """Return packages/<letter>/ under a protocol directory."""
    letter = str(package).strip().lower()
    if not _PACKAGE_LETTER_RE.match(letter):
        raise ValueError(f"package must be A-G, got {package!r}")
    return Path(protocol_dir) / "packages" / letter


def load_protocol_spec(path: Path | str) -> dict[str, Any]:
    """Load a protocol YAML. Optional ``extends`` merges a parent file first.

    Child keys replace parent keys. ``protocol_id`` and ``output`` must end up
    set (usually on the child). Relative ``extends`` paths are resolved against
    the child file's directory.
    """
    path = Path(path)
    return _load_protocol_spec_resolved(path, stack=())


def _load_protocol_spec_resolved(
    path: Path,
    *,
    stack: tuple[Path, ...],
) -> dict[str, Any]:
    path = path.resolve()
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
        merged = _load_protocol_spec_resolved(parent_path, stack=stack + (path,))
    merged.update(spec)

    if "protocol_id" not in merged:
        raise ValueError(f"Protocol spec missing protocol_id: {path}")
    if "output" not in merged:
        raise ValueError(f"Protocol spec missing output: {path}")
    return merged


def resolve_protocol_output(spec: dict[str, Any]) -> Path:
    """Resolve protocol output path relative to the repo root."""
    out = Path(spec["output"])
    if not out.is_absolute():
        out = REPO_ROOT / out
    return out


def protocol_path_for_spec(spec: dict[str, Any]) -> Path:
    """Canonical freeze YAML for a protocol run (default: canonical_grid.yaml)."""
    raw = spec.get("canonical", spec.get("protocol"))
    if raw is None:
        return CANONICAL_PROTOCOL
    path = Path(raw)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


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
    raise FileNotFoundError(f"Protocol '{stem}' not found under {PROTOCOLS_DIR}")


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
        raise ValueError("Claim/T1 needs upstream_protocol in the YAML or --upstream-trials")
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


def copy_protocol_spec(spec_path: Path | str, protocol_dir: Path | str) -> Path:
    """Write the resolved protocol YAML into the results folder.

    ``extends`` parents are merged so the archived file is self-contained.
    """
    src = Path(spec_path)
    dest = Path(protocol_dir) / "protocol.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    resolved = load_protocol_spec(src)
    body = yaml.safe_dump(resolved, sort_keys=False, default_flow_style=False)
    dest.write_text(f"{yaml_banner_line()}\n{body}")
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


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


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
    now = _utc_now_iso()
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
