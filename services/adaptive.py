"""Adaptive campaign: seeds and dog counts go only where the answer is still open.

One run, one output folder. Each round:

1. every cell with fewer than one batch of seeds (new, or cut short by a
   kill or the budget stop) is filled up to one batch;
2. the frontier rules (analysis.frontier) mark the cells whose reliability
   or finish-time comparison is still undecided; those are filled to the end
   of their next batch, up to ``max_seeds`` (``seeds_wanted``);
3. wherever the zone changes between two neighbouring D on a curve and they
   are more than ``refine_min_gap`` dogs apart, the D halfway between is added.

Above a confirmed saturation, a cell whose dogs were copies of each other
gets no more seeds and no midpoints (``pruned_cells``): an added dog that only
duplicates another cannot change the answer, so seeds there are wasted. Such
cells are marked ``pruned`` in frontier_cells.csv.

A cell with an errored trial gets no further seeds and is never reliable: an
exception in a deterministic simulation is a bug to fix, not noise to
average; status.json names those cells. The run stops when no cell needs
seeds, or when ``budget_hours`` is spent; that budget counts from the start
of this run (after calibration), so a resumed run gets a new one. Resuming
continues from the trials already in the folder; rows of groups the protocol
no longer lists are ignored.
"""

from __future__ import annotations

import time
from collections import Counter
from collections.abc import Callable
from typing import Any

import pandas as pd

from analysis.frontier import SATURATED, UNDECIDED, Frontier, Rules, frontier
from protocols.packaging.provenance import stable_hash

from .calibration import CalibrationError, calibrate
from .cells import Cell, Group, Trial, cell_config, groups, make_trial, trial_key
from .protocol import Protocol
from .runner import run_batch
from .store import CampaignStore

STOP_DECIDED = "every cell decided, at max_seeds or errored"
STOP_BUDGET = "budget_hours spent"


def seeds_wanted(seeds_run: int, batch: int, flagged: bool) -> int:
    """How many seeds a cell gets this round: up to the end of its next batch when
    flagged, else up to one batch. Counts stay on whole batches (10, 20, ...), so
    a resumed run seeds a cell as an uninterrupted run would; a later batch cut short
    by a kill is filled even when the cell is decided."""
    if flagged:
        target = (seeds_run // batch + 1) * batch
    else:
        target = max(batch, -(-seeds_run // batch) * batch)
    return max(0, target - seeds_run)


def _flock_radii(
    protocol: Protocol, store: CampaignStore, physics_hash: str, workers: int
) -> dict[str, dict[int, float]]:
    table = store.load_calibration()
    needed = {(m.name, n) for m in protocol.methods for n in protocol.flock_sizes}
    if table is None or any(n not in table.get(m, {}) for m, n in needed):
        try:
            table = calibrate(protocol, workers)
        except CalibrationError:
            # No trial ran: let a corrected protocol reopen this folder.
            store.discard_if_empty()
            raise
        store.save_calibration(physics_hash, table)
    return table


def _next_seeds(
    cell: Cell, done: set[str], errored: set[str], batch: int, max_seeds: int
) -> list[int]:
    """The next ``batch`` seed indices of ``cell`` that have not run or failed."""
    todo = [
        i
        for i in range(max_seeds)
        if trial_key(cell, i) not in done and trial_key(cell, i) not in errored
    ]
    return todo[:batch]


def pruned_cells(front: Frontier, trials: pd.DataFrame, overlap: float) -> set[tuple[str, int]]:
    """(group, D) cells above a confirmed saturation whose dogs were copies.

    A curve's saturation is confirmed when D_sat is decided, the grid top does
    not censor it, and the next working D above it is ``saturated`` (as fast as
    D_best, decided). Above that D, a cell is pruned when its trials' mean
    ``dog_overlap`` is at least ``overlap`` and its zone is ``saturated`` or
    ``undecided``: never a cell that is slower or unreliable, since that would
    be a measured harm.
    """
    out: set[tuple[str, int]] = set()
    mean_overlap = trials.groupby(["group_key", "n_shepherds"])["mean_dog_overlap"].mean()
    for g in front.groups.to_dict("records"):
        if pd.isna(g["d_sat"]) or g["d_sat_undecided"] or g["still_improving_at_top"]:
            continue
        key, d_sat = str(g["group_key"]), int(g["d_sat"])
        cells = front.cells.loc[front.cells["group_key"] == key]
        zones = dict(zip(cells["n_shepherds"].astype(int), cells["zone"]))
        confirm = next((d for d in sorted(zones) if d > d_sat and zones[d] == SATURATED), None)
        if confirm is None:
            continue
        for d in (d for d in sorted(zones) if d > confirm):
            copies = float(mean_overlap.get((key, d), 0.0)) >= overlap
            if copies and zones[d] in (SATURATED, UNDECIDED):
                out.add((key, d))
    return out


def _refine(
    grid: dict[str, set[int]],
    front: Frontier,
    min_gap: int,
    pruned: frozenset[tuple[str, int]] | None = None,
    by_reliability: bool = False,
    max_seeds: int | None = None,
) -> int:
    """Add the midpoint D wherever the zone changes between neighbouring D more than
    ``min_gap`` apart, unless either is ``pruned``. Groups the grid does not list are
    skipped. Returns how many.

    An undecided neighbour below ``max_seeds`` may yet decide, so it waits. One at the cap
    stays undecided: the D between it and a decided neighbour is then added, or a D_min could
    sit above an untested D inside its own bracket. Without ``max_seeds`` every undecided
    cell waits. (The frontier flags an undecided cell as needing seeds even at the cap; the
    cap is applied when seeds are picked, so the seed count decides here.)"""
    pruned = pruned or frozenset()
    added = 0
    column = "reliability" if by_reliability else "zone"
    for key, cells in front.cells.groupby("group_key"):
        if str(key) not in grid:
            continue
        zones = dict(zip(cells["n_shepherds"].astype(int), cells[column]))
        d_all = cells["n_shepherds"].astype(int)
        capped = cells["n_seeds"] >= max_seeds if max_seeds is not None else None
        waiting = set(d_all if capped is None else d_all[~capped])
        ds = sorted(zones)
        for a, b in zip(ds, ds[1:]):
            if (str(key), a) in pruned or (str(key), b) in pruned:
                continue
            open_ = any(zones[d] == UNDECIDED and d in waiting for d in (a, b))
            if b - a > min_gap and zones[a] != zones[b] and not open_:
                mid = (a + b) // 2
                if mid not in grid[str(key)]:
                    grid[str(key)].add(mid)
                    added += 1
    return added


def _status(
    protocol: Protocol,
    physics_hash: str,
    rows: list[dict[str, Any]],
    front: Frontier | None,
    *,
    rounds: int,
    error_cells: dict[str, int],
    started: float,
    rows_at_start: int,
    rows_ignored: int,
    stop_reason: str | None,
    round_trials: int,
) -> dict[str, Any]:
    hours = (time.time() - started) / 3600.0
    new_rows = len(rows) - rows_at_start
    payload: dict[str, Any] = {
        "protocol_id": protocol.protocol_id,
        "physics_hash": physics_hash,
        "running": stop_reason is None,
        "stop_reason": stop_reason,
        "rounds": rounds,
        "trials_done": len(rows),
        "trials_ignored": rows_ignored,  # rows of groups the protocol no longer lists
        "trials_this_run": new_rows,
        "round_trials": round_trials,  # trials queued in the round that is starting
        "trial_errors": sum(error_cells.values()),
        "cells_with_errors": {"count": len(error_cells), "keys": sorted(error_cells)},
        "hours_this_run": round(hours, 3),
        "trials_per_hour": round(new_rows / hours, 1) if hours > 0 else None,
    }
    if front is not None:
        cells = front.cells
        # Errored and pruned cells may be undecided but get no seeds.
        open_cells = cells["needs_seeds"] & (cells["n_errors"] == 0) & ~cells["pruned"]
        payload["cells"] = int(len(cells))
        payload["cells_pruned"] = int(cells["pruned"].sum())
        payload["cells_needing_seeds"] = int(open_cells.sum())
        payload["cells_at_max_seeds_undecided"] = int(
            (open_cells & (cells["n_seeds"] >= int(protocol.settings["max_seeds"]))).sum()
        )
    return payload


def run_campaign(
    protocol: Protocol, workers: int, log: Callable[[str], None] = print
) -> CampaignStore:
    physics_hash = stable_hash(protocol.physics())
    store = CampaignStore(protocol.output)
    store.open(protocol, physics_hash)
    try:
        _run(protocol, store, physics_hash, workers, log)
    finally:
        store.close()
    return store


def _run(
    protocol: Protocol,
    store: CampaignStore,
    physics_hash: str,
    workers: int,
    log: Callable[[str], None],
) -> None:
    radii = _flock_radii(protocol, store, physics_hash, workers)
    rules = Rules.from_settings(protocol.settings)
    batch = int(protocol.settings["batch_seeds"])
    max_seeds = int(protocol.settings["max_seeds"])
    min_gap = int(protocol.settings["refine_min_gap"])
    prune_overlap = float(protocol.settings["prune_overlap"])

    by_key: dict[str, Group] = {g.key: g for g in groups(protocol)}
    grid: dict[str, set[int]] = {k: set(protocol.shepherd_counts) for k in by_key}
    loaded = store.load_rows()
    rows = [r for r in loaded if r["group_key"] in grid]
    rows_ignored = len(loaded) - len(rows)
    if rows_ignored:
        log(f"ignored {rows_ignored} trials of groups the protocol no longer lists")
    rows_at_start = len(rows)
    done = {r["trial_key"] for r in rows}
    seeds_run = Counter(r["cell_key"] for r in rows)

    def known_errors() -> tuple[set[str], dict[str, int]]:
        """Errored trial keys and counts per cell, of the groups the protocol lists."""
        cells = {k: n for k, n in store.error_cells().items() if k.rsplit("|D=", 1)[0] in grid}
        keys = {k for k in store.error_keys() if k.rsplit("|D=", 1)[0] in grid}
        return keys, cells

    errored, error_cells = known_errors()
    for r in rows:
        grid[r["group_key"]].add(int(r["n_shepherds"]))
    configs: dict[str, dict[str, Any]] = {}

    def config_of(cell: Cell) -> dict[str, Any]:
        if cell.key not in configs:
            radius = radii[cell.group.method][cell.group.n_sheep]
            configs[cell.key] = cell_config(protocol, cell, radius)
        return configs[cell.key]

    started = time.time()
    deadline = started + float(protocol.settings["budget_hours"]) * 3600.0
    rounds = 0
    stop_reason: str | None = None
    while True:
        table = pd.DataFrame(rows)
        front = frontier(table, rules, errors=error_cells) if rows else None
        needs: set[tuple[str, int]] = set()
        if front is not None:
            pruned = pruned_cells(front, table, prune_overlap)
            cell_ids = zip(front.cells["group_key"].astype(str), front.cells["n_shepherds"])
            front.cells["pruned"] = [(k, int(d)) in pruned for k, d in cell_ids]
            store.write_tables(rows, front.cells, front.groups)
            added = _refine(
                grid,
                front,
                min_gap,
                frozenset(pruned),
                not rules.decide_finish_times,
                max_seeds,
            )
            if added:
                log(f"added {added} intermediate dog counts")
            flagged = front.cells.loc[front.cells["needs_seeds"] & ~front.cells["pruned"]]
            needs = set(zip(flagged["group_key"].astype(str), flagged["n_shepherds"].astype(int)))
        plan: list[Trial] = []
        for key, ds in grid.items():
            for d in sorted(ds):
                cell = Cell(by_key[key], d)
                if cell.key in error_cells:
                    continue
                count = seeds_wanted(seeds_run[cell.key], batch, (key, d) in needs)
                if count == 0:
                    continue
                for i in _next_seeds(cell, done, errored, count, max_seeds):
                    plan.append(
                        make_trial(protocol, cell, i, config_of(cell), store.timeseries_dir)
                    )
        if not plan:
            stop_reason = STOP_DECIDED
        elif time.time() >= deadline:
            stop_reason = STOP_BUDGET
        store.write_status(
            _status(
                protocol,
                physics_hash,
                rows,
                front,
                rounds=rounds,
                error_cells=error_cells,
                started=started,
                rows_at_start=rows_at_start,
                rows_ignored=rows_ignored,
                stop_reason=stop_reason,
                round_trials=len(plan),
            )
        )
        if stop_reason is not None:
            break

        rounds += 1
        # Longest trials first: the big flocks and many-dog cells go to workers while the
        # small ones fill the gaps, so no worker waits at the end of a round for one slow trial.
        plan.sort(key=lambda t: (-t.cell.group.n_sheep, -t.cell.n_shepherds, t.seed_index))
        log(f"round {rounds}: {len(plan)} trials on {len({t.cell.key for t in plan})} cells")

        def keep(row: dict[str, Any]) -> None:
            rows.append(row)
            done.add(row["trial_key"])
            seeds_run[row["cell_key"]] += 1

        run_batch(plan, store, workers=workers, deadline=deadline, on_row=keep)
        errored, error_cells = known_errors()
    if error_cells:
        log(f"{len(error_cells)} cells had errors and got no further seeds; see errors.jsonl")
    log(f"stopped: {stop_reason}; {len(rows)} trials in {protocol.output}")
