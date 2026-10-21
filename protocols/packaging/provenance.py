"""Physics hash and provenance.json of a campaign folder.

The physics hash covers everything that changes a trial's outcome: the task,
every canonical setting that is not a stopping rule, each method's full
resolved configuration (code defaults under the protocol's overrides) and
time limit, the protocol's layout set and its largest dog count. The last
two size the field and place the goal of every cell, so adding a layout or
a D above the old maximum changes the physics and needs a new folder. The
flock sizes, the smaller D and the stopping rules are not hashed, so a
campaign can add flock sizes, intermediate D or seeds and still resume. A
folder whose hash differs from the protocol is refused.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .generated_notice import with_json_notice


def normalise_numbers(value: Any) -> Any:
    """``value`` with every int turned into a float (bools kept), recursively.

    YAML reads ``13`` as an int and ``13.0`` as a float; both run the same
    physics, so they must hash the same.
    """
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
    """Short SHA256 of a JSON-serialisable value, independent of key order and of
    whether a number was written as an int or a float."""
    text = json.dumps(normalise_numbers(payload), sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def write_provenance(path: Path, *, protocol_id: str, physics_hash: str) -> None:
    payload = {
        "protocol_id": protocol_id,
        "physics_hash": physics_hash,
        "created_at": datetime.now(UTC).isoformat(),
    }
    path.write_text(json.dumps(with_json_notice(payload), indent=2) + "\n")


def read_provenance(path: Path) -> dict[str, str]:
    """protocol_id and physics_hash of a folder."""
    data = json.loads(path.read_text())
    return {"protocol_id": str(data["protocol_id"]), "physics_hash": str(data["physics_hash"])}
