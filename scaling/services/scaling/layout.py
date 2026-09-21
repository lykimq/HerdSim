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
import shutil
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
    """Load a protocol YAML (subset of the frozen protocol + path metadata)."""
    path = Path(path)
    with path.open() as f:
        spec = yaml.safe_load(f) or {}
    if not isinstance(spec, dict):
        raise ValueError(f"Protocol spec must be a mapping: {path}")
    if "protocol_id" not in spec:
        raise ValueError(f"Protocol spec missing protocol_id: {path}")
    if "output" not in spec:
        raise ValueError(f"Protocol spec missing output: {path}")
    return spec


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
    """Copy the protocol YAML into the results folder for provenance."""
    src = Path(spec_path)
    dest = Path(protocol_dir) / "protocol.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest


def write_status(
    protocol_dir: Path | str,
    *,
    protocol_id: str,
    n_planned: int,
    n_done: int,
    n_pending_at_start: int,
    extra: dict[str, Any] | None = None,
) -> Path:
    """Write machine-readable protocol completion status."""
    out = Path(protocol_dir)
    out.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "protocol_id": protocol_id,
        "n_planned": int(n_planned),
        "n_done": int(n_done),
        "n_pending_at_start": int(n_pending_at_start),
        "complete": int(n_done) >= int(n_planned) and int(n_planned) > 0,
        "trials_csv": "trials.csv",
        "manifest_jsonl": "manifest.jsonl",
    }
    if extra:
        payload.update(extra)
    path = out / "status.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def protocol_id_from_dir(protocol_dir: Path | str) -> str:
    """Default protocol_id = leaf folder name (e.g. pilot, scout, pilot_state)."""
    return Path(protocol_dir).resolve().name
