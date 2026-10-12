"""Build and write provenance.json next to a campaign or package export.

protocol.yaml records the planned config. This module records what the runner
actually used at execute time: when the stamp was written, a hash of that
config, the expanded seed list, and the metric ids that were computed. That
lets later analysis check the run without re-deriving those runtime details.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def config_hash(config: dict[str, Any]) -> str:
    """Stable SHA256 of a JSON-serialisable config dict."""
    payload = json.dumps(config, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def build_provenance_stamp(
    *,
    protocol: dict[str, Any],
    seed_list: list[int],
    metric_ids: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a run stamp with only fields not duplicated in protocol.yaml.

    Omits git metadata and the full protocol body (those live in protocol.yaml).
    Keeps a content hash, the expanded seed list, and runtime metric ids.
    """
    stamp: dict[str, Any] = {
        "created_at": datetime.now(UTC).isoformat(),
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
