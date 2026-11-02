"""Physics hash and provenance.json of a campaign folder.

What the hash covers and leaves out: docs/guides/configuration.md. It says nothing about the
code: ``code_identity`` records that per run sitting.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from .generated_notice import with_json_notice

REPO = Path(__file__).resolve().parents[1]
HASH_CHARS = 16  # hex characters kept of a SHA256, enough to tell two states apart
# The source that decides a trial's outcome and its row: the engine, the row packaging,
# the cell config and calibration that size each trial's task, the protocol code that sets
# its time limit, and the runner that adds the identity columns to the row.
TRIAL_CODE = (
    "sim",
    "records",
    "services/cells.py",
    "services/calibration.py",
    "services/protocol.py",
    "services/runner.py",
)
# Libraries whose numerics or output reach a trial or its row.
LIBRARIES = ("numpy", "scipy", "pandas", "pyarrow")


def normalise_numbers(value: Any) -> Any:
    """``value`` with every int turned into a float (bools kept), recursively.

    YAML reads ``13`` as an int and ``13.0`` as a float; both run the same physics, so
    they must hash the same.
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
    """Short SHA256 of a JSON-serialisable value, independent of key order and of whether a
    number was written as an int or a float."""
    text = json.dumps(normalise_numbers(payload), sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:HASH_CHARS]


def _trial_code_hash() -> str:
    """Hash of the path and bytes of every file in ``TRIAL_CODE``."""
    files = sorted(
        p
        for part in TRIAL_CODE
        for p in ([REPO / part] if part.endswith(".py") else (REPO / part).rglob("*.py"))
    )
    digest = hashlib.sha256()
    for path in files:
        digest.update(str(path.relative_to(REPO)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()[:HASH_CHARS]


def _git(*args: str) -> str | None:
    """Output of a git command in the repository, or None when it fails (no git, no repo)."""
    done = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=False)
    return done.stdout.strip() if done.returncode == 0 else None


def _installed(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def code_identity() -> dict[str, Any]:
    """The code a run sitting used. The physics hash covers configuration only, so without
    this a change to a dog or sheep rule would resume into an old folder unseen.

    ``code_hash`` hashes the trial code itself, so it also catches uncommitted edits; the
    commit, the dirty flag and the library versions are for a person tracing a result.
    """
    changes = _git("status", "--porcelain", "--", *TRIAL_CODE)
    return {
        "code_hash": _trial_code_hash(),
        "commit": _git("rev-parse", "HEAD"),
        "code_dirty": None if changes is None else bool(changes),
        "python": platform.python_version(),
        **{name: _installed(name) for name in LIBRARIES},
    }


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
