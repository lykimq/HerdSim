"""Campaign path and naming conventions for shepherding-budget results.

Canonical layout:

    results/budget/phase{k}/{campaign_slug}/
      campaign.yaml       # frozen subset used for this run (copied)
      manifest.jsonl      # resume ledger (status=ok cells)
      provenance.json     # campaign stamp
      status.json         # planned / done counts
      trials.csv
      timeseries/         # one file per cell; stem == cell key
      packages/{a-g}/     # auto analysis exports
      REPORT.md           # human scientific narrative only

campaign_id in provenance must match the campaign_slug (folder name),
or the explicit id from configs/budget/campaigns/*.yaml.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BUDGET_RESULTS_ROOT = REPO_ROOT / "results" / "budget"
CAMPAIGNS_DIR = REPO_ROOT / "configs" / "budget" / "campaigns"
CANONICAL_PROTOCOL = REPO_ROOT / "configs" / "budget" / "canonical_grid.yaml"

_PACKAGE_LETTER_RE = re.compile(r"^[A-Ga-g]$")


def package_output_dir(campaign_dir: Path | str, package: str) -> Path:
    """Return packages/<letter>/ under a campaign directory."""
    letter = str(package).strip().lower()
    if not _PACKAGE_LETTER_RE.match(letter):
        raise ValueError(f"package must be A-G, got {package!r}")
    return Path(campaign_dir) / "packages" / letter


def load_campaign_spec(path: Path | str) -> dict[str, Any]:
    """Load a campaign YAML (subset of the frozen protocol + path metadata)."""
    path = Path(path)
    with path.open() as f:
        spec = yaml.safe_load(f) or {}
    if not isinstance(spec, dict):
        raise ValueError(f"Campaign spec must be a mapping: {path}")
    if "campaign_id" not in spec:
        raise ValueError(f"Campaign spec missing campaign_id: {path}")
    if "output" not in spec:
        raise ValueError(f"Campaign spec missing output: {path}")
    return spec


def resolve_campaign_output(spec: dict[str, Any]) -> Path:
    """Resolve campaign output path relative to the repo root."""
    out = Path(spec["output"])
    if not out.is_absolute():
        out = REPO_ROOT / out
    return out


def protocol_path_for_spec(spec: dict[str, Any]) -> Path:
    """Protocol YAML for a campaign (default: canonical_grid.yaml)."""
    raw = spec.get("protocol")
    if raw is None:
        return CANONICAL_PROTOCOL
    path = Path(raw)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


def copy_campaign_spec(spec_path: Path | str, campaign_dir: Path | str) -> Path:
    """Copy the campaign YAML into the results folder for provenance."""
    src = Path(spec_path)
    dest = Path(campaign_dir) / "campaign.yaml"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest


def write_status(
    campaign_dir: Path | str,
    *,
    campaign_id: str,
    n_planned: int,
    n_done: int,
    n_pending_at_start: int,
    extra: dict[str, Any] | None = None,
) -> Path:
    """Write machine-readable campaign completion status."""
    out = Path(campaign_dir)
    out.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "campaign_id": campaign_id,
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


def campaign_id_from_dir(campaign_dir: Path | str) -> str:
    """Default campaign_id = leaf folder name (e.g. pilot, scout, pilot_state)."""
    return Path(campaign_dir).resolve().name
