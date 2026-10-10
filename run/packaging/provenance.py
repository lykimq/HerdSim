"""Provenance stamps for scaling protocols (Cap I13 support / Cap I1)."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _git_hash(repo_root: Path | None = None) -> str:
    try:
        cwd = str(repo_root) if repo_root else None
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "unknown"


def config_hash(config: dict[str, Any]) -> str:
    """Stable SHA256 of a JSON-serialisable config dict."""
    payload = json.dumps(config, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def build_provenance_stamp(
    *,
    protocol_id: str,
    protocol: dict[str, Any],
    seed_list: list[int],
    metric_ids: list[str] | None = None,
    repo_root: Path | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a reproducible provenance record for a scaling protocol."""
    stamp: dict[str, Any] = {
        "protocol_id": protocol_id,
        "created_at": datetime.now(UTC).isoformat(),
        "git_hash": _git_hash(repo_root),
        "protocol": dict(protocol),
        "protocol_hash": config_hash(protocol),
        "seed_list": list(seed_list),
        "n_seeds": len(seed_list),
        "metric_ids": list(metric_ids or []),
    }
    if extra:
        stamp["extra"] = dict(extra)
    return stamp


def write_provenance(path: Path, stamp: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(stamp, indent=2, default=str) + "\n")
