"""Plan, run and check HerdSim protocols; without a protocol, the six of the study.

    uv run cli/campaign.py plan   dmin_f99_m6
    uv run cli/campaign.py run    dmin_f99_m6 --workers 20
    uv run cli/campaign.py status dmin_f99_m6

docs/guides/cli_reference.md has the verbs, flags and the checklist for a long run.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.pool import limit_threads  # noqa: E402

# One BLAS thread per process: the campaign already runs one trial per core.
# Must be set before NumPy is imported, which the services below do.
limit_threads()

from records.provenance import read_provenance  # noqa: E402
from services.adaptive import STOP_DECIDED, run_campaign  # noqa: E402
from services.cells import groups  # noqa: E402
from services.protocol import (  # noqa: E402
    RESULTS_ROOT,
    MethodSpec,
    Protocol,
    load_protocol,
    study_queue,
)
from services.store import CampaignStore, progress  # noqa: E402

QUEUE: tuple[str, ...] = study_queue()
LOG = RESULTS_ROOT / "queue_log.jsonl"


def stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def say(message: str) -> None:
    """A line with the time, flushed so a log file shows it while the run goes on."""
    print(f"[{stamp()}] {message}", flush=True)


def folder_state(folder: Path) -> str:
    """done: every cell decided; partial: stopped or killed, resumes; new: nothing yet."""
    status = folder / "status.json"
    if not status.exists():
        return "new"
    info = json.loads(status.read_text())
    return "done" if info.get("stop_reason") == STOP_DECIDED else "partial"


def summary(folder: Path) -> dict[str, object]:
    """The numbers worth keeping from a finished or stopped folder."""
    info = json.loads((folder / "status.json").read_text())
    errors = folder / "errors.jsonl"
    return {
        "trials": info.get("trials_done"),
        "trial_errors": info.get("trial_errors"),
        "cells": info.get("cells"),
        "cells_needing_seeds": info.get("cells_needing_seeds"),
        "cells_at_max_seeds_undecided": info.get("cells_at_max_seeds_undecided"),
        "cells_pruned": info.get("cells_pruned"),
        "stop_reason": info.get("stop_reason"),
        "errors_file_lines": len(errors.read_text().splitlines()) if errors.exists() else 0,
    }


def _limit_text(m: MethodSpec) -> str:
    if m.time_limit_ticks is not None:
        return f"{m.time_limit_ticks} ticks"
    return f"{m.time_limit_drive_multiple:g} x drive time"


def _folder_note(protocol: Protocol) -> str:
    """Whether the output folder is new, resumes this protocol, or belongs to another."""
    provenance = protocol.output / "provenance.json"
    if not provenance.exists():
        return ""
    found = read_provenance(provenance)
    same = found["protocol_id"] == protocol.protocol_id
    same = same and found["physics_hash"] == protocol.physics_hash()
    return " (exists: resumes)" if same else " (exists with another protocol or physics: refused)"


def describe(protocol: Protocol) -> str:
    """What a run of ``protocol`` would do, without running anything."""
    s = protocol.settings
    curves = groups(protocol)
    cells = len(curves) * len(protocol.shepherd_counts)
    batch = s["batch_seeds"]
    lines = [
        f"protocol      {protocol.protocol_id}",
        f"output        {protocol.output}{_folder_note(protocol)}",
        "methods       " + ", ".join(f"{m.name} ({_limit_text(m)})" for m in protocol.methods),
        f"layouts       {', '.join(protocol.layouts)}",
        f"N             {list(protocol.flock_sizes)}",
        f"D             {list(protocol.shepherd_counts)}",
        f"D curves      {len(curves)}",
        f"cells         {cells}  (a midpoint D is added where the zone changes between"
        + f" neighbours more than {s['refine_min_gap']} dog(s) apart)",
        f"first round   {cells * batch} trials ({batch} seeds per cell)",
        f"seeds         up to {s['max_seeds']} per undecided cell",
        f"reliable      success rate above {s['reliability_theta']}, "
        + f"{s['confidence']:.0%} intervals",
        f"budget        {s['budget_hours']} h",
    ]
    return "\n".join(lines)


def run_one(protocol: Protocol, workers: int) -> dict[str, object]:
    """Run one protocol into its folder; never raises."""
    started = time.time()
    entry: dict[str, object] = {
        "protocol": protocol.protocol_id,
        "started": stamp(),
        "workers": workers,
    }
    try:
        run_campaign(protocol, workers, log=say)
        entry["outcome"] = "ran"
    except Exception as error:  # noqa: BLE001 - the next protocol goes on whatever this one did
        entry["outcome"] = f"failed: {error!r}"
        traceback.print_exc()
    entry["hours"] = round((time.time() - started) / 3600.0, 3)
    entry["finished"] = stamp()
    if (protocol.output / "status.json").exists():
        entry.update(summary(protocol.output))
    return entry


def run_all(protocols: list[Protocol], workers: int, skip_done: bool) -> bool:
    """Run the protocols in order; True when none failed. ``skip_done`` leaves out a folder
    with every cell decided: right for the study, wrong for a protocol whose grid was edited."""
    say(f"{[p.protocol_id for p in protocols]} with {workers} workers")
    failed = False
    for protocol in protocols:
        state = folder_state(protocol.output)
        if skip_done and state == "done":
            say(f"{protocol.protocol_id}: done, skipped")
            continue
        say(f"{protocol.protocol_id}: {state}, starting")
        entry = run_one(protocol, workers)
        failed |= entry["outcome"] != "ran"
        if protocol.protocol_id in QUEUE:
            RESULTS_ROOT.mkdir(exist_ok=True)
            with LOG.open("a") as handle:
                handle.write(json.dumps(entry) + "\n")
        say(f"{protocol.protocol_id}: {json.dumps(entry)}")
    say("finished")
    return not failed


def show_status(protocols: list[Protocol], detailed: bool) -> None:
    """Each named protocol's status.json with the running round, or one state line per protocol."""
    if detailed:
        print("\n\n".join(progress(CampaignStore(p.output)) for p in protocols))
        return
    for protocol in protocols:
        print(f"{protocol.protocol_id:18s} {folder_state(protocol.output)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("verb", choices=("plan", "run", "status"))
    parser.add_argument(
        "protocols", nargs="*", help="protocol ids or paths (default: the study's protocols)"
    )
    parser.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    args = parser.parse_args()

    # Loaded before anything runs, so a mistyped id stops the command, not hour three of it.
    protocols = [load_protocol(name) for name in args.protocols or QUEUE]
    if args.verb == "plan":
        print("\n\n".join(describe(p) for p in protocols))
    elif args.verb == "run":
        if not run_all(protocols, args.workers, skip_done=not args.protocols):
            sys.exit(1)
    else:
        show_status(protocols, detailed=bool(args.protocols))


if __name__ == "__main__":
    main()
