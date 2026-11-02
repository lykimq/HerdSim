"""Plan, run and check HerdSim protocols; without a protocol, the six of the study.

    uv run cli/campaign.py plan   dmin_f99_m6
    uv run cli/campaign.py run    dmin_f99_m6 --workers 20
    uv run cli/campaign.py status dmin_f99_m6

docs/guides/cli_reference.md has the verbs, flags and the checklist for a long run.
"""

from __future__ import annotations

import os

# One BLAS thread per process: the campaign already runs one trial per core.
# Must be set before NumPy is imported.
for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_var] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import traceback  # noqa: E402
from datetime import datetime  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.adaptive import STOP_DECIDED, run_campaign  # noqa: E402
from services.cells import describe  # noqa: E402
from services.protocol import RESULTS_ROOT, Protocol, load_protocol, study_queue  # noqa: E402
from services.store import CampaignStore, progress  # noqa: E402

QUEUE: tuple[str, ...] = study_queue()
LOG = RESULTS_ROOT / "queue_log.jsonl"


def stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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


def run_one(protocol: Protocol, workers: int) -> dict[str, object]:
    """Run one protocol into its folder; never raises."""
    started = time.time()
    entry: dict[str, object] = {
        "protocol": protocol.protocol_id,
        "started": stamp(),
        "workers": workers,
    }
    try:
        run_campaign(protocol, workers, log=lambda line: print(f"[{stamp()}] {line}", flush=True))
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
    ids = [p.protocol_id for p in protocols]
    print(f"[{stamp()}] {ids} with {workers} workers", flush=True)
    failed = False
    for protocol in protocols:
        state = folder_state(protocol.output)
        if skip_done and state == "done":
            print(f"[{stamp()}] {protocol.protocol_id}: done, skipped", flush=True)
            continue
        print(f"[{stamp()}] {protocol.protocol_id}: {state}, starting", flush=True)
        entry = run_one(protocol, workers)
        failed |= entry["outcome"] != "ran"
        if protocol.protocol_id in QUEUE:
            RESULTS_ROOT.mkdir(exist_ok=True)
            with LOG.open("a") as handle:
                handle.write(json.dumps(entry) + "\n")
        print(f"[{stamp()}] {protocol.protocol_id}: {json.dumps(entry)}", flush=True)
    print(f"[{stamp()}] finished", flush=True)
    return not failed


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
    elif args.protocols:
        print("\n\n".join(progress(CampaignStore(p.output)) for p in protocols))
    else:
        for protocol in protocols:
            print(f"{protocol.protocol_id:18s} {folder_state(protocol.output)}")


if __name__ == "__main__":
    main()
