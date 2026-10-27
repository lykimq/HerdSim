"""Physics hash and provenance.json of a campaign folder.

The physics hash covers everything that changes a trial's outcome:

- the task and every canonical setting except the sampling strategy;
- each method's full parameter set (code defaults under the protocol's overrides) and its
  time limit;
- the set of layouts and the largest dog count, because they size the field and place the
  goal of every cell.

It leaves out what a campaign may add or change without changing a trial:

- the flock sizes, the smaller dog counts and the factor levels;
- the sampling strategy (theta, seed batches, budget);
- settings still at their neutral value, so folders written before a setting existed keep
  their hash.

What follows from that:

- more flock sizes, intermediate dog counts or seeds resume into the same folder;
- a new layout or a dog count above the old maximum changes the hash and needs a new folder;
- a folder whose hash differs from the protocol is refused.

The hash says nothing about the code: ``code_identity`` records the code of each run
sitting, so a resume after a change to the trial code is logged and can be traced.
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
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def code_identity() -> dict[str, Any]:
    """The code a run sitting used. The physics hash covers configuration only, so without
    this a change to a dog or sheep rule would resume into an old folder unseen.

    ``code_hash`` hashes the trial code itself, so it also catches uncommitted edits; the
    commit, the dirty flag and the library versions are for a person tracing a result.
    """
    files = sorted(
        p
        for part in TRIAL_CODE
        for p in ([REPO / part] if part.endswith(".py") else (REPO / part).rglob("*.py"))
    )
    digest = hashlib.sha256()
    for path in files:
        digest.update(str(path.relative_to(REPO)).encode())
        digest.update(path.read_bytes())

    def git(*args: str) -> str | None:
        done = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=False)
        return done.stdout.strip() if done.returncode == 0 else None

    def installed(name: str) -> str | None:
        try:
            return version(name)
        except PackageNotFoundError:
            return None

    commit = git("rev-parse", "HEAD")
    changes = git("status", "--porcelain", "--", *TRIAL_CODE)
    return {
        "code_hash": digest.hexdigest()[:16],
        "commit": commit,
        "code_dirty": None if changes is None else bool(changes),
        "python": platform.python_version(),
        **{name: installed(name) for name in LIBRARIES},
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
