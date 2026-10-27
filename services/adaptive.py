"""Adaptive campaign: seeds and dog counts go only where the answer is still open.

One run, one output folder. Each round:

1. every cell with fewer than one batch of seeds (new, or cut short by a kill or the
   budget stop) is filled up to one batch;
2. the frontier rules (analysis.frontier) mark the cells whose reliability or finish-time
   comparison is still undecided; those get their next batch, up to ``max_seeds``;
3. wherever the zone changes between two neighbouring D on a curve more than
   ``refine_min_gap`` dogs apart, the D halfway between is added.

Above a confirmed saturation, a cell whose dogs were copies of each other gets no more
seeds and no midpoints (``pruned_cells``); such cells are marked ``pruned`` in
frontier_cells.csv. A cell with an errored trial gets no further seeds and is never
reliable: an exception in a deterministic simulation is a bug to fix, not noise to average;
status.json names those cells.

The run stops when no cell needs seeds, or when ``budget_hours`` is spent; the budget
counts from the start of this run (after calibration), so a resumed run gets a new one.
Resuming continues from the trials already in the folder; rows of groups the protocol no
longer lists are ignored.
"""

from __future__ import annotations

import time
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from analysis import keys
from analysis.frontier import SATURATED, UNDECIDED, Frontier, Rules, frontier
from records.provenance import stable_hash
from sim.plugins.scenarios import SCENARIOS

from .calibration import CalibrationError, calibrate
from .cells import Cell, Group, Trial, cell_config, groups, make_trial, trial_key
from .protocol import Protocol
from .runner import run_batch
from .store import CampaignStore

STOP_DECIDED = "every cell decided, at max_seeds or errored"
STOP_BUDGET = "budget_hours spent"

CellId = tuple[str, int]  # (group key, D)


def seeds_wanted(seeds_run: int, batch: int, flagged: bool) -> int:
    """Seeds to add to a cell this round, keeping its count at whole batches.

    A cell that is not flagged is only filled up to one batch (a new cell, or one cut
    short by a kill); a flagged cell gets its next batch. Whole batches keep a resumed run
    on the same seed boundaries as an uninterrupted one.
    """
    if flagged:
        target = (seeds_run // batch + 1) * batch
    else:
        target = max(batch, -(-seeds_run // batch) * batch)
    return max(0, target - seeds_run)


def _flock_radii(
    protocol: Protocol, store: CampaignStore, physics_hash: str, workers: int
) -> dict[str, dict[int, float]]:
    """R_f per method and flock size, calibrated once and kept in the folder. A task that
    sizes itself (``Scenario.calibrates`` false) has none: every cell gets NaN, and its
    setup ignores it."""
    if not SCENARIOS[protocol.settings["task"]].calibrates:
        nan = float("nan")
        return {m.name: {n: nan for n in protocol.flock_sizes} for m in protocol.methods}
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


def pruned_cells(front: Frontier, trials: pd.DataFrame, overlap: float) -> set[CellId]:
    """Cells above a confirmed saturation whose dogs were copies of each other (mean
    dog_overlap at least ``overlap``): an added dog that duplicates another cannot change
    the answer, so seeds there are wasted.

    Saturation is confirmed when D_sat is decided and a larger D is already zoned
    saturated. Only cells zoned saturated or undecided are pruned, never a slower or an
    unreliable one: those are the answers being measured.
    """
    out: set[CellId] = set()
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
    pruned: frozenset[CellId] | None = None,
    column: str = "zone",
    max_seeds: int | None = None,
) -> int:
    """Add the midpoint D wherever ``column`` (the zone, or the reliability when finish times
    are not decided) changes between neighbouring D more than ``min_gap`` apart, unless
    either is ``pruned``. Groups the grid does not list are
    skipped. Returns how many.

    An undecided neighbour below ``max_seeds`` may yet decide, so it waits. One at the cap
    stays undecided: the D between it and a decided neighbour is then added, or a D_min
    could sit above an untested D inside its own bracket. Without ``max_seeds`` every
    undecided cell waits.
    """
    pruned = pruned or frozenset()
    added = 0
    for key, cells in front.cells.groupby("group_key"):
        group_key = str(key)
        if group_key not in grid:
            continue
        zones = dict(zip(cells["n_shepherds"].astype(int), cells[column]))
        d_all = cells["n_shepherds"].astype(int)
        capped = cells["n_seeds"] >= max_seeds if max_seeds is not None else None
        waiting = set(d_all if capped is None else d_all[~capped])
        ds = sorted(zones)
        for a, b in zip(ds, ds[1:]):
            if (group_key, a) in pruned or (group_key, b) in pruned:
                continue
            open_ = any(zones[d] == UNDECIDED and d in waiting for d in (a, b))
            if b - a > min_gap and zones[a] != zones[b] and not open_:
                mid = (a + b) // 2
                if mid not in grid[group_key]:
                    grid[group_key].add(mid)
                    added += 1
    return added


@dataclass
class _Ledger:
    """What the run knows of its folder: the rows, which trials ran or raised, and the grid
    of D per group (the protocol's counts plus the ones added or found in the folder)."""

    groups: dict[str, Group]
    grid: dict[str, set[int]]
    rows: list[dict[str, Any]]
    rows_ignored: int  # rows of groups the protocol no longer lists
    done: set[str] = field(default_factory=set)
    seeds_run: Counter[str] = field(default_factory=Counter)
    errored: set[str] = field(default_factory=set)
    error_cells: dict[str, int] = field(default_factory=dict)

    @classmethod
    def load(cls, protocol: Protocol, store: CampaignStore) -> _Ledger:
        by_key = {g.key: g for g in groups(protocol)}
        grid = {k: set(protocol.shepherd_counts) for k in by_key}
        loaded = store.load_rows()
        rows = [r for r in loaded if r["group_key"] in grid]
        ledger = cls(by_key, grid, rows, len(loaded) - len(rows))
        for row in rows:
            ledger._index(row)
        ledger.refresh_errors(store)
        return ledger

    def _index(self, row: dict[str, Any]) -> None:
        self.done.add(row["trial_key"])
        self.seeds_run[row["cell_key"]] += 1
        self.grid[row["group_key"]].add(int(row["n_shepherds"]))

    def keep(self, row: dict[str, Any]) -> None:
        """Record a trial that just finished."""
        self.rows.append(row)
        self._index(row)

    def refresh_errors(self, store: CampaignStore) -> None:
        """Errored trial keys and counts per cell, of the groups the protocol lists."""

        def listed(key: str) -> bool:
            return keys.group_of_cell(key) in self.grid

        self.errored = {k for k in store.error_keys() if listed(k)}
        self.error_cells = {k: n for k, n in store.error_cells().items() if listed(k)}


def _assess(
    ledger: _Ledger, rules: Rules, prune_overlap: float, store: CampaignStore
) -> tuple[Frontier | None, set[CellId]]:
    """The frontier of the rows so far, with pruned cells marked, written to the folder's
    tables; and the pruned cells. (None, empty) before any trial ran."""
    if not ledger.rows:
        return None, set()
    table = pd.DataFrame(ledger.rows)
    front = frontier(table, rules, errors=ledger.error_cells)
    pruned = pruned_cells(front, table, prune_overlap)
    cell_ids = zip(front.cells["group_key"].astype(str), front.cells["n_shepherds"])
    front.cells["pruned"] = [(k, int(d)) in pruned for k, d in cell_ids]
    store.write_tables(ledger.rows, front.cells, front.groups)
    return front, pruned


def _cells_needing_seeds(front: Frontier | None) -> set[CellId]:
    if front is None:
        return set()
    flagged = front.cells.loc[front.cells["needs_seeds"] & ~front.cells["pruned"]]
    return set(zip(flagged["group_key"].astype(str), flagged["n_shepherds"].astype(int)))


def _plan_round(
    protocol: Protocol,
    ledger: _Ledger,
    needs: set[CellId],
    config_of: Callable[[Cell], dict[str, Any]],
    timeseries_dir: Any,
) -> list[Trial]:
    """The trials of the next round: every cell's missing seeds (``seeds_wanted``), skipping
    cells that errored. Longest trials first, so the big flocks and many-dog cells go to
    the workers while the small ones fill the gaps."""
    batch = protocol.settings["batch_seeds"]
    max_seeds = protocol.settings["max_seeds"]
    plan: list[Trial] = []
    for key, ds in ledger.grid.items():
        for d in sorted(ds):
            cell = Cell(ledger.groups[key], d)
            if cell.key in ledger.error_cells:
                continue
            count = seeds_wanted(ledger.seeds_run[cell.key], batch, (key, d) in needs)
            if count == 0:
                continue
            for i in _next_seeds(cell, ledger.done, ledger.errored, count, max_seeds):
                plan.append(make_trial(protocol, cell, i, config_of(cell), timeseries_dir))
    plan.sort(key=lambda t: (-t.cell.group.n_sheep, -t.cell.n_shepherds, t.seed_index))
    return plan


def _status(
    protocol: Protocol,
    physics_hash: str,
    ledger: _Ledger,
    front: Frontier | None,
    *,
    rounds: int,
    started: float,
    rows_at_start: int,
    stop_reason: str | None,
    round_trials: int,
) -> dict[str, Any]:
    hours = (time.time() - started) / 3600.0
    new_rows = len(ledger.rows) - rows_at_start
    payload: dict[str, Any] = {
        "protocol_id": protocol.protocol_id,
        "physics_hash": physics_hash,
        "running": stop_reason is None,
        "stop_reason": stop_reason,
        "rounds": rounds,
        "trials_done": len(ledger.rows),
        "trials_ignored": ledger.rows_ignored,
        "trials_this_run": new_rows,
        "round_trials": round_trials,  # trials queued in the round that is starting
        "trial_errors": sum(ledger.error_cells.values()),
        "cells_with_errors": {"count": len(ledger.error_cells), "keys": sorted(ledger.error_cells)},
        "hours_this_run": round(hours, 3),
        "trials_per_hour": round(new_rows / hours, 1) if hours > 0 else None,
    }
    if front is not None:
        cells = front.cells
        # Errored and pruned cells may be undecided but get no seeds.
        open_cells = cells["needs_seeds"] & (cells["n_errors"] == 0) & ~cells["pruned"]
        payload["cells"] = len(cells)
        payload["cells_pruned"] = int(cells["pruned"].sum())
        payload["cells_needing_seeds"] = int(open_cells.sum())
        payload["cells_at_max_seeds_undecided"] = int(
            (open_cells & (cells["n_seeds"] >= protocol.settings["max_seeds"])).sum()
        )
    return payload


def run_campaign(
    protocol: Protocol, workers: int, log: Callable[[str], None] = print
) -> CampaignStore:
    physics_hash = stable_hash(protocol.physics())
    store = CampaignStore(protocol.output)
    store.open(protocol, physics_hash)
    try:
        before, now = store.record_sitting(protocol)
        if before is not None and before.get("code_hash") != now["code_hash"]:
            # Warn, not refuse: a refactor changes the hash too. Each sitting records its code
            # and how many trials came before it, so a reader can tell which ran on which code.
            change = f"{before.get('code_hash')} -> {now['code_hash']}"
            log(f"warning: the trial code changed since the last run of this folder ({change})")
        _run(protocol, store, physics_hash, workers, log)
    finally:
        store.close()
    return store


def refresh_tables(protocol: Protocol) -> CampaignStore:
    """Decide every cell again from the stored trials and rewrite the folder's tables, without
    running a trial or adding a dog count. A change to the frontier rules reaches a finished
    run this way, with no simulation."""
    if not (protocol.output / "provenance.json").exists():
        raise FileNotFoundError(f"no results to refresh in {protocol.output}")
    store = CampaignStore(protocol.output)
    store.open(protocol, stable_hash(protocol.physics()))
    try:
        ledger = _Ledger.load(protocol, store)
        s = protocol.settings
        _assess(ledger, Rules.from_settings(s), s["prune_overlap"], store)
    finally:
        store.close()
    return store


def _config_builder(
    protocol: Protocol, radii: dict[str, dict[int, float]]
) -> Callable[[Cell], dict[str, Any]]:
    """The run config of a cell, built once per cell and reused across rounds."""
    configs: dict[str, dict[str, Any]] = {}

    def config_of(cell: Cell) -> dict[str, Any]:
        if cell.key not in configs:
            radius = radii[cell.group.method][cell.group.n_sheep]
            configs[cell.key] = cell_config(protocol, cell, radius)
        return configs[cell.key]

    return config_of


def _decide(
    ledger: _Ledger,
    rules: Rules,
    settings: dict[str, Any],
    store: CampaignStore,
    log: Callable[[str], None],
) -> Frontier | None:
    """Decide every cell from the rows so far, write the tables, and add the midpoint D the
    rules ask for. Without decided finish times the midpoints follow reliability alone."""
    front, pruned = _assess(ledger, rules, settings["prune_overlap"], store)
    if front is not None:
        column = "zone" if rules.decide_finish_times else "reliability"
        added = _refine(
            ledger.grid,
            front,
            settings["refine_min_gap"],
            frozenset(pruned),
            column,
            settings["max_seeds"],
        )
        if added:
            log(f"added {added} intermediate dog counts")
    return front


def _stop_reason(plan: list[Trial], deadline: float) -> str | None:
    if not plan:
        return STOP_DECIDED
    if time.time() >= deadline:
        return STOP_BUDGET
    return None


def _run(
    protocol: Protocol,
    store: CampaignStore,
    physics_hash: str,
    workers: int,
    log: Callable[[str], None],
) -> None:
    """Rounds until nothing is planned or the budget is spent: decide, plan, run."""
    radii = _flock_radii(protocol, store, physics_hash, workers)
    s = protocol.settings
    rules = Rules.from_settings(s)
    ledger = _Ledger.load(protocol, store)
    if ledger.rows_ignored:
        log(f"ignored {ledger.rows_ignored} trials of groups the protocol no longer lists")
    rows_at_start = len(ledger.rows)
    config_of = _config_builder(protocol, radii)

    started = time.time()
    deadline = started + s["budget_hours"] * 3600.0
    rounds = 0
    while True:
        front = _decide(ledger, rules, s, store, log)
        needs = _cells_needing_seeds(front)
        plan = _plan_round(protocol, ledger, needs, config_of, store.timeseries_dir)
        stop_reason = _stop_reason(plan, deadline)
        store.write_status(
            _status(
                protocol,
                physics_hash,
                ledger,
                front,
                rounds=rounds,
                started=started,
                rows_at_start=rows_at_start,
                stop_reason=stop_reason,
                round_trials=len(plan),
            )
        )
        if stop_reason is not None:
            break
        rounds += 1
        log(f"round {rounds}: {len(plan)} trials on {len({t.cell.key for t in plan})} cells")
        run_batch(plan, store, workers=workers, deadline=deadline, on_row=ledger.keep)
        ledger.refresh_errors(store)
    if ledger.error_cells:
        log(
            f"{len(ledger.error_cells)} cells had errors and got no further seeds; see errors.jsonl"
        )
    log(f"stopped: {stop_reason}; {len(ledger.rows)} trials in {protocol.output}")
