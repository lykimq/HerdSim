"""Groups, cells, trials and their run configs.

A group is one D curve: method, layout, factor levels and N. A cell is a group at one dog
count D; a trial is one seed of a cell. Seed i of every cell is ``master_seed + i``, so
cells share seeds and comparisons between them are paired.
"""

from __future__ import annotations

import itertools
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from analysis import keys
from protocols.packaging.provenance import read_provenance, stable_hash
from sim.core.config.experiment import build_config
from sim.plugins.scenarios import SCENARIOS

from .protocol import MethodSpec, Protocol, drive_limit_ticks, factor_settings


@dataclass(frozen=True)
class Group:
    """One D curve."""

    method: str
    layout: str
    factors: tuple[tuple[str, Any], ...]  # sorted (name, value) pairs
    n_sheep: int

    @property
    def key(self) -> str:
        return keys.group_key(self.method, self.layout, self.factors, self.n_sheep)


@dataclass(frozen=True)
class Cell:
    """A group at one dog count."""

    group: Group
    n_shepherds: int

    @property
    def key(self) -> str:
        return keys.cell_key(self.group.key, self.n_shepherds)


@dataclass(frozen=True)
class Trial:
    """One seed of one cell, with everything a worker needs."""

    cell: Cell
    seed_index: int
    seed: int
    config: dict[str, Any]
    timeseries_path: Path | None

    @property
    def key(self) -> str:
        return trial_key(self.cell, self.seed_index)


def trial_key(cell: Cell, seed_index: int) -> str:
    return keys.trial_key(cell.key, seed_index)


def groups(protocol: Protocol) -> list[Group]:
    """Every D curve of the protocol."""
    names = sorted(protocol.factors)
    combos = [
        tuple(zip(names, values))
        for values in itertools.product(*(protocol.factors[n] for n in names))
    ]
    return [
        Group(m.name, layout, factors, n)
        for m in protocol.methods
        for layout in protocol.layouts
        for factors in combos
        for n in protocol.flock_sizes
    ]


def method_spec(protocol: Protocol, name: str) -> MethodSpec:
    return next(m for m in protocol.methods if m.name == name)


def setup_for(
    settings: Mapping[str, Any],
    method: MethodSpec,
    *,
    flock_radius: float,
    n_sheep: int,
    layouts: tuple[str, ...],
    max_dogs: int,
) -> dict[str, Any]:
    """Setup of one method, flock size and flock radius: engine keys plus the task's own.

    The geometry (drive length, goal radius, lost radius, field) is per method because R_f
    is per method: each method's flock has its own driven size, so its task is sized to
    its own flock rather than to one shared field.
    """
    task = SCENARIOS[settings["task"]]
    geometry = task.build_setup(
        settings,
        flock_radius=flock_radius,
        n_sheep=n_sheep,
        layouts=layouts,
        max_dogs=max_dogs,
    )
    hold = settings["hold_drive_multiple"]
    if hold < 0.0:
        raise ValueError("hold_drive_multiple must not be negative")
    drive = task.drive_length(geometry)
    return {
        "max_ticks": _max_ticks(method, drive),
        "hold_ticks": drive_limit_ticks(hold, drive, method.name, method.params) if hold else 0,
        "metrics_stride": settings["metrics_stride"],
        "measurement_radius": settings["measurement_radius"],
        "dog_overlap_distance": settings["dog_overlap_distance"],
        **geometry,
    }


def _max_ticks(method: MethodSpec, drive: float) -> int:
    """Time limit of a cell in ticks: the method's fixed limit, or its multiple of the drive
    time.

    The drive time is the task's length (``Scenario.drive_length``) over the top sheep
    speed, so a deadline written as a multiple asks the same of every N: how many dogs
    finish in m times what the sheep need.
    """
    if method.time_limit_ticks is not None:
        return method.time_limit_ticks
    assert method.time_limit_drive_multiple is not None
    return drive_limit_ticks(method.time_limit_drive_multiple, drive, method.name, method.params)


def cell_config(protocol: Protocol, cell: Cell, flock_radius: float) -> dict[str, Any]:
    """Run config of a cell. Factors override canonical settings."""
    group = cell.group
    spec = method_spec(protocol, group.method)
    settings = factor_settings(dict(group.factors), protocol.settings)
    return build_config(
        task=protocol.settings["task"],
        method=group.method,
        params=dict(spec.params),
        setup=setup_for(
            {**protocol.settings, **settings},
            spec,
            flock_radius=flock_radius,
            n_sheep=group.n_sheep,
            layouts=protocol.layouts,
            max_dogs=max(protocol.shepherd_counts),
        ),
        n_sheep=group.n_sheep,
        n_shepherds=cell.n_shepherds,
        initial_layout=group.layout,
    )


def make_trial(
    protocol: Protocol,
    cell: Cell,
    seed_index: int,
    config: dict[str, Any],
    timeseries_dir: Path,
) -> Trial:
    """Trial ``seed_index`` of ``cell``; keeps its per-tick history for the first seeds."""
    keep = seed_index < protocol.settings["timeseries_seeds"]
    file_name = trial_key(cell, seed_index).replace("|", "__").replace("=", "-") + ".parquet"
    return Trial(
        cell=cell,
        seed_index=seed_index,
        seed=protocol.settings["master_seed"] + seed_index,
        config=config,
        timeseries_path=timeseries_dir / file_name if keep else None,
    )


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
    same = same and found["physics_hash"] == stable_hash(protocol.physics())
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
        "factors       " + (str(dict(protocol.factors)) if protocol.factors else "none"),
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
