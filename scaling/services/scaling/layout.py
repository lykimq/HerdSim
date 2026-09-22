"""Protocol path and naming conventions for scaling results.

Canonical layout:

    scaling/results/phase{k}/{protocol_slug}/
      protocol.yaml       # frozen subset used for this run (copied)
      manifest.jsonl      # resume ledger (status=ok cells)
      provenance.json     # protocol stamp
      status.json         # planned / done counts
      trials.csv
      timeseries/         # one file per cell; stem == cell key
      packages/{a-g}/     # auto analysis exports
      REPORT.md           # human scientific narrative only

protocol_id in provenance must match the protocol_slug (folder name),
or the explicit id from scaling/configs/protocols/*.yaml.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# scaling/services/scaling/layout.py -> parents[2] = scaling/, parents[3] = repo root
SCALING_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = SCALING_ROOT.parent
SCALING_RESULTS_ROOT = SCALING_ROOT / "results"
PROTOCOLS_DIR = SCALING_ROOT / "configs" / "protocols"
CANONICAL_PROTOCOL = SCALING_ROOT / "configs" / "canonical_grid.yaml"

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
        merged = _load_protocol_spec_resolved(
            parent_path, stack=stack + (path,)
        )
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


def copy_protocol_spec(spec_path: Path | str, protocol_dir: Path | str) -> Path:
    """Write the resolved protocol YAML into the results folder for provenance.

    ``extends`` parents are merged so the archived file is self-contained.
    """
    src = Path(spec_path)
    dest = Path(protocol_dir) / "protocol.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    resolved = load_protocol_spec(src)
    dest.write_text(
        yaml.safe_dump(resolved, sort_keys=False, default_flow_style=False)
    )
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
    return datetime.now(timezone.utc).isoformat()


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
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def protocol_id_from_dir(protocol_dir: Path | str) -> str:
    """Default protocol_id = leaf folder name (e.g. pilot, scout, pilot_state)."""
    return Path(protocol_dir).resolve().name
