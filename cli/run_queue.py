"""Run the D_min protocols one after another, resumably, and keep a log of each.

    uv run cli/run_queue.py --workers 20            run every protocol that is not done
    uv run cli/run_queue.py --only dmin_m12 dmin_m6  run just these, in this order
    uv run cli/run_queue.py --list                   show the queue and the state of each folder

Each protocol writes to its own folder results/<protocol_id>. A protocol whose folder says "every
cell decided" is skipped, a folder that stopped for any other reason is resumed, and a protocol
that raises is logged and the queue goes on. After each protocol one line goes to
results/queue_log.jsonl: when it ran, for how long, the trials, errors and open cells.
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
from services.protocol import RESULTS_ROOT, load_protocol  # noqa: E402

# Order of the plan: the main table first, then the sensitivities, then the other method.
QUEUE = (
    "dmin_m12",
    "dmin_m6",
    "dmin_m3",
    "dmin_s_base",
    "dmin_s_matched",
    "dmin_s_handler",
    "dmin_s_ring",
    "dmin_s_goal",
    "dmin_s_dogspeed",
    "dmin_s_gap",
    "dmin_kubo",
    "dmin_f99_m6",
    "dmin_f99_m3",
    "dmin_f99_m12",
    "dmin_f99_s_base",
    "dmin_f99_s_matched",
    "dmin_f99_s_dogspeed",
)
LOG = RESULTS_ROOT / "queue_log.jsonl"


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


def stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run_one(protocol_id: str, workers: int) -> dict[str, object]:
    """Run one protocol into its own folder; never raises."""
    protocol = load_protocol(protocol_id)
    started = time.time()
    entry: dict[str, object] = {"protocol": protocol_id, "started": stamp(), "workers": workers}
    try:
        run_campaign(protocol, workers, log=lambda line: print(f"[{stamp()}] {line}", flush=True))
        entry["outcome"] = "ran"
    except Exception as error:  # noqa: BLE001 - the queue goes on whatever one protocol did
        entry["outcome"] = f"failed: {error!r}"
        traceback.print_exc()
    entry["hours"] = round((time.time() - started) / 3600.0, 3)
    entry["finished"] = stamp()
    if (protocol.output / "status.json").exists():
        entry.update(summary(protocol.output))
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--only", nargs="+", default=None, help="protocol ids, run in this order")
    parser.add_argument("--list", action="store_true", help="show the queue and exit")
    args = parser.parse_args()

    queue = tuple(args.only) if args.only else QUEUE
    unknown = [p for p in queue if p not in QUEUE]
    if unknown:
        raise SystemExit(f"not in the queue: {unknown}; the queue is {list(QUEUE)}")
    if args.list:
        for protocol_id in queue:
            print(f"{protocol_id:18s} {folder_state(RESULTS_ROOT / protocol_id)}")
        return

    print(f"[{stamp()}] queue {list(queue)} with {args.workers} workers", flush=True)
    for protocol_id in queue:
        state = folder_state(RESULTS_ROOT / protocol_id)
        if state == "done":
            print(f"[{stamp()}] {protocol_id}: done, skipped", flush=True)
            continue
        print(f"[{stamp()}] {protocol_id}: {state}, starting", flush=True)
        entry = run_one(protocol_id, args.workers)
        RESULTS_ROOT.mkdir(exist_ok=True)
        with LOG.open("a") as handle:
            handle.write(json.dumps(entry) + "\n")
        print(f"[{stamp()}] {protocol_id}: {json.dumps(entry)}", flush=True)
    print(f"[{stamp()}] queue finished", flush=True)


if __name__ == "__main__":
    main()
