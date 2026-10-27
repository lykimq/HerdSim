"""Results folder of one campaign.

    <output>/
      protocol.yaml           merged protocol and canonical values, as run, plus
                              method_config: every parameter each method ran with
      provenance.json         protocol id and physics hash
      calibration.json        R_f(N) per method, with the physics hash it belongs to
      trials.jsonl            one JSON line per finished trial, appended as trials finish
      trials.jsonl.gz         the committed copy of trials.jsonl, which can pass GitHub's
                              100 MB file limit; packed when a campaign closes the folder
                              and unpacked when a clone has only the .gz
      errors.jsonl            one line per trial that raised
      trials.csv              table form of trials.jsonl, rewritten after each round
      frontier_cells.csv      per (group, D): reliability, finish times, zone, errored trials
      frontier_groups.csv     per group: D_min, D_min_low, D_best, D_sat, D_crowd,
                              D_overcrowd, D_max, flags
      status.json             progress of the adaptive run
      timeseries/             per-tick Parquet for the first seeds of every cell

Only the campaign process writes here; workers return their rows to it. ``open`` takes an
advisory lock on .lock for the whole run, so a second campaign on the folder is refused. A
kill in the middle of a write leaves at worst a cut last line, which is dropped on the next
load.
"""

from __future__ import annotations

import fcntl
import gzip
import json
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Any

import pandas as pd
import yaml

from protocols.packaging.generated_notice import NOTICE_LINE, with_json_notice, write_csv
from protocols.packaging.provenance import read_provenance, write_provenance

from .protocol import Protocol


class PhysicsMismatch(RuntimeError):
    """The folder holds trials from a different physics or protocol than the one given."""


class FolderBusy(RuntimeError):
    """Another campaign process holds the folder's lock."""


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(with_json_notice(payload), indent=2, default=str) + "\n")
    tmp.replace(path)


def _read_jsonl(path: Path, repair: bool) -> list[dict[str, Any]]:
    """Rows after the notice line. A cut last line (kill during a write) is dropped,
    and removed from the file when ``repair`` is set, so the next append starts on a
    line of its own."""
    lines = path.read_text().splitlines()
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(lines[1:], start=2):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            if number != len(lines):
                raise
            if repair:
                path.write_text("\n".join(lines[:-1]) + "\n")
    return rows


def _pack(plain: Path, packed: Path) -> None:
    """gzip with no name or time in the header, so the same trials give the same bytes
    and git sees no change when nothing ran. The .gz takes the mtime of its source,
    which is how ``pack_trials`` tells that it is current."""
    tmp = packed.with_suffix(".gz.tmp")
    with plain.open("rb") as src, tmp.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=6, mtime=0, filename="") as dst:
            shutil.copyfileobj(src, dst)
    tmp.replace(packed)
    stat = plain.stat()
    os.utime(packed, ns=(stat.st_atime_ns, stat.st_mtime_ns))


def _unpack(packed: Path, plain: Path) -> None:
    """The unpacked file takes the .gz's mtime, so a folder that runs nothing is not repacked."""
    tmp = plain.with_suffix(".jsonl.tmp")
    with gzip.open(packed, "rb") as src, tmp.open("wb") as dst:
        shutil.copyfileobj(src, dst)
    tmp.replace(plain)
    stat = packed.stat()
    os.utime(plain, ns=(stat.st_atime_ns, stat.st_mtime_ns))


class CampaignStore:
    def __init__(self, output: Path) -> None:
        """A clone holds only trials.jsonl.gz. It is unpacked here, before anything reads
        the folder, because a folder with provenance.json and no trials.jsonl counts as
        empty and ``discard_if_empty`` would reset it. An existing trials.jsonl is never
        overwritten: it may hold trials the .gz does not have yet."""
        self.root = output
        self.trials_jsonl = output / "trials.jsonl"
        self.trials_gz = output / "trials.jsonl.gz"
        self.errors_jsonl = output / "errors.jsonl"
        self.timeseries_dir = output / "timeseries"
        self._lock: IO[str] | None = None
        if self.trials_gz.exists() and not self.trials_jsonl.exists():
            _unpack(self.trials_gz, self.trials_jsonl)

    def pack_trials(self) -> None:
        """Write trials.jsonl.gz unless it already matches trials.jsonl."""
        if not self.trials_jsonl.exists():
            return
        if (
            self.trials_gz.exists()
            and self.trials_gz.stat().st_mtime_ns == self.trials_jsonl.stat().st_mtime_ns
        ):
            return
        _pack(self.trials_jsonl, self.trials_gz)

    def open(self, protocol: Protocol, physics_hash: str) -> None:
        """Lock the folder, then create it or check that it ran the same protocol and physics.

        provenance.json is written last, so a folder without it has no trials and
        is set up again from scratch.
        """
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = (self.root / ".lock").open("w")
        try:
            fcntl.flock(self._lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self._lock.close()
            self._lock = None
            raise FolderBusy(f"another campaign is running in {self.root}") from None
        try:
            self._check_or_create(protocol, physics_hash)
        except BaseException:
            self.close()
            raise

    def _check_or_create(self, protocol: Protocol, physics_hash: str) -> None:
        provenance = self.root / "provenance.json"
        if provenance.exists():
            found = read_provenance(provenance)
            if found["protocol_id"] != protocol.protocol_id:
                ran = f"{self.root} belongs to protocol {found['protocol_id']!r}"
                raise PhysicsMismatch(f"{ran}, not {protocol.protocol_id!r}; set its own output")
            if found["physics_hash"] != physics_hash:
                ran = f"{self.root} was run with physics {found['physics_hash']}"
                now = f"the protocol now gives {physics_hash}"
                raise PhysicsMismatch(f"{ran}, {now}. Use a new output folder for changed physics.")
            return
        self.timeseries_dir.mkdir(exist_ok=True)
        archive = {**protocol.resolved, "method_config": protocol.method_config()}
        body = yaml.safe_dump(archive, sort_keys=False)
        (self.root / "protocol.yaml").write_text(f"{NOTICE_LINE}\n{body}")
        write_provenance(provenance, protocol_id=protocol.protocol_id, physics_hash=physics_hash)

    def is_running(self) -> bool:
        """Whether a campaign process holds the folder's lock right now."""
        path = self.root / ".lock"
        if not path.exists():
            return False
        with path.open("r") as f:
            try:
                fcntl.flock(f, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            fcntl.flock(f, fcntl.LOCK_UN)
            return False

    def close(self) -> None:
        """Pack the trials while the lock is still held, then release it. Packing here,
        not after every round, costs a few seconds once per run instead of per round."""
        if self._lock is not None:
            self.pack_trials()
            self._lock.close()
            self._lock = None

    def discard_if_empty(self) -> bool:
        """Remove provenance.json and calibration.json when no trial ever ran, so a
        changed protocol can reopen the folder and calibrates afresh. Returns whether
        the folder was reset."""
        provenance = self.root / "provenance.json"
        if self.trials_jsonl.exists() or not provenance.exists():
            return False
        provenance.unlink()
        (self.root / "calibration.json").unlink(missing_ok=True)
        return True

    # --- trials --------------------------------------------------------------

    def load_rows(self, repair: bool = True) -> list[dict[str, Any]]:
        """Every finished trial. A cut last line (kill during a write) is dropped, and
        removed from the file when ``repair`` is set; a reader of a running campaign
        must pass ``repair=False`` so it never rewrites a file the campaign appends to."""
        if not self.trials_jsonl.exists():
            return []
        rows = _read_jsonl(self.trials_jsonl, repair)
        keys = [r["trial_key"] for r in rows]
        if len(keys) != len(set(keys)):
            raise RuntimeError(f"{self.trials_jsonl} has duplicate trial keys")
        return rows

    def append_row(self, row: dict[str, Any]) -> None:
        new = not self.trials_jsonl.exists()
        with self.trials_jsonl.open("a") as f:
            if new:
                f.write(NOTICE_LINE + "\n")
            f.write(json.dumps(row, default=str, allow_nan=True) + "\n")

    def append_error(self, trial_key: str, message: str) -> None:
        new = not self.errors_jsonl.exists()
        with self.errors_jsonl.open("a") as f:
            if new:
                f.write(NOTICE_LINE + "\n")
            f.write(json.dumps({"trial_key": trial_key, "error": message}) + "\n")

    def error_keys(self) -> set[str]:
        """Keys of the trials that raised. A cut last line is dropped from the file (that
        trial reruns); only the campaign process calls this, so the repair is safe."""
        if not self.errors_jsonl.exists():
            return set()
        return {row["trial_key"] for row in _read_jsonl(self.errors_jsonl, repair=True)}

    def error_cells(self) -> dict[str, int]:
        """Errored trials per cell key, parsed from the trial keys (``<cell>|seed=<i>``)."""
        counts: dict[str, int] = {}
        for key in self.error_keys():
            cell_key = key.rsplit("|seed=", 1)[0]
            counts[cell_key] = counts.get(cell_key, 0) + 1
        return counts

    # --- calibration, tables, status -----------------------------------------

    def load_calibration(self) -> dict[str, dict[int, float]] | None:
        """R_f table of the folder; ``open`` has checked the folder's physics already."""
        path = self.root / "calibration.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return {
            m: {int(n): float(r) for n, r in t.items()} for m, t in data["flock_radius"].items()
        }

    def save_calibration(self, physics_hash: str, table: dict[str, dict[int, float]]) -> None:
        _write_json(
            self.root / "calibration.json",
            {"physics_hash": physics_hash, "flock_radius": table},
        )

    def write_tables(
        self, rows: list[dict[str, Any]], cells: pd.DataFrame, groups: pd.DataFrame
    ) -> None:
        write_csv(pd.DataFrame(rows), self.root / "trials.csv")
        write_csv(cells, self.root / "frontier_cells.csv")
        write_csv(groups, self.root / "frontier_groups.csv")

    def write_status(self, payload: dict[str, Any]) -> None:
        _write_json(
            self.root / "status.json", {**payload, "updated_at": datetime.now(UTC).isoformat()}
        )

    def read_status(self) -> dict[str, Any]:
        return json.loads((self.root / "status.json").read_text())


def progress(store: CampaignStore) -> str:
    """The folder's status.json plus the progress of the running round and its time left.

    ``running`` comes from the folder lock, not from the file, so a campaign that
    was killed is shown as stopped.
    """
    status = store.read_status()
    status["running"] = store.is_running()
    started = datetime.fromisoformat(status["updated_at"])
    in_file = len(store.load_rows(repair=False))
    done = in_file - int(status["trials_done"]) - int(status.get("trials_ignored", 0))
    planned = int(status["round_trials"])
    lines = [json.dumps(status, indent=2)]
    if status["running"] and planned > 0:
        seconds = (datetime.now(UTC) - started).total_seconds()
        rate = done / seconds if seconds > 0 and done > 0 else 0.0
        eta = (
            f"about {(planned - done) / rate / 60:.0f} min left in this round"
            if rate
            else "no rate yet"
        )
        lines.append(f"round {status['rounds']}: {done}/{planned} trials done, {eta}")
    return "\n".join(lines)
