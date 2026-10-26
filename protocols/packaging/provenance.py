"""Physics integrity hashing and provenance tracking for campaign output directories.

A physics hash captures all configuration parameters that alter simulation dynamics:
- The scenario task and method parameter definitions.
- Environmental field bounds and layout sets.
- Maximum shepherd count (which dictates field sizing and clearance).

Non-physical parameters (such as stopping rules, sample seed counts, and intermediate
shepherd counts) are excluded so campaigns can be resumed or deepened without altering
the physics hash. Output directories with mismatched physics hashes are rejected.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .generated_notice import with_json_notice


def normalise_numbers(value: Any) -> Any:
    """Recursively cast all integers to floats to ensure equivalent numeric hashing."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return float(value)
    if isinstance(value, dict):
        return {str(k): normalise_numbers(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalise_numbers(v) for v in value]
    return value


def stable_hash(payload: Any) -> str:
    """Generate a 16-character SHA-256 hash invariant to key order and numeric types."""
    text = json.dumps(normalise_numbers(payload), sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def write_provenance(path: Path, *, protocol_id: str, physics_hash: str) -> None:
    """Record protocol provenance and physics hash to a JSON file with an auto-generated notice."""
    payload = {
        "protocol_id": protocol_id,
        "physics_hash": physics_hash,
        "created_at": datetime.now(UTC).isoformat(),
    }
    path.write_text(json.dumps(with_json_notice(payload), indent=2) + "\n")


def read_provenance(path: Path) -> dict[str, str]:
    """Read protocol_id and physics_hash metadata from an existing provenance file."""
    data = json.loads(path.read_text())
    return {"protocol_id": str(data["protocol_id"]), "physics_hash": str(data["physics_hash"])}
