"""Groups, cells, trials and their run configs.

A group is one D curve: method, layout and N. A cell is a group at one dog
count D; a trial is one seed of a cell. Seed i of every cell is ``master_seed + i``, so
cells share seeds and comparisons between them are paired.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from analysis import keys
from sim.drive_task import task as drive_task
from sim.trial import build_config

from .protocol import MethodSpec, Protocol, drive_limit_ticks


@dataclass(frozen=True)
class Group:
    """One D curve."""

    method: str
    layout: str
    n_sheep: int

    @property
    def key(self) -> str:
        return keys.group_key(self.method, self.layout, self.n_sheep)


@dataclass(frozen=True)
class Cell:
    """A group at one dog count."""

    group: Group
    n_shepherds: int

    @property
    def key(self) -> str:
        return keys.cell_key(self.group.key, self.n_shepherds)


def trial_key(cell: Cell, seed_index: int) -> str:
    return keys.trial_key(cell.key, seed_index)


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


def groups(protocol: Protocol) -> list[Group]:
    """Every D curve of the protocol."""
    return [
        Group(m.name, layout, n)
        for m in protocol.methods
        for layout in protocol.layouts
        for n in protocol.flock_sizes
    ]


def method_spec(protocol: Protocol, name: str) -> MethodSpec:
    return next(m for m in protocol.methods if m.name == name)


def _max_ticks(method: MethodSpec, drive: float) -> int:
    """Time limit of a cell in ticks: the method's fixed limit, or its multiple of the drive
    time.

    The drive time is the task's length (``drive_length``) over the top sheep
    speed, so a deadline written as a multiple asks the same of every N: how many dogs
    finish in m times what the sheep need.
    """
    if method.time_limit_ticks is not None:
        return method.time_limit_ticks
    assert method.time_limit_drive_multiple is not None
    return drive_limit_ticks(method.time_limit_drive_multiple, drive, method.params)


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
    geometry = drive_task.build_setup(
        settings,
        flock_radius=flock_radius,
        n_sheep=n_sheep,
        layouts=layouts,
        max_dogs=max_dogs,
    )
    drive = drive_task.drive_length(geometry)
    return {
        "max_ticks": _max_ticks(method, drive),
        "measurement_radius": settings["measurement_radius"],
        "dog_overlap_distance": settings["dog_overlap_distance"],
        **geometry,
    }


def cell_config(protocol: Protocol, cell: Cell, flock_radius: float) -> dict[str, Any]:
    """Run config of a cell."""
    group = cell.group
    spec = method_spec(protocol, group.method)
    return build_config(
        method=group.method,
        params=dict(spec.params),
        setup=setup_for(
            protocol.settings,
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
