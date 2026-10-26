"""Load and check a protocol: canonical defaults, optional ``extends`` chain, the protocol.

A protocol is one experiment written as data, in protocols/configs/protocols/. It names its
output folder, the methods with their time limits and parameter overrides, the grid (layouts,
flock sizes, dog counts), optional factors (a sweepable canonical setting; each value is its own
D curve), and any canonical value it changes. Everything else comes from
protocols/configs/canonical.yaml. A protocol can ``extends`` another and change only what
differs, which is how a variant of a finished run gets its own id and folder:

    protocol_id: dmin_f99_hold_spacing
    output: results/dmin_f99_hold_spacing
    extends: dmin_f99_hold.yaml
    dog_spacing: 2.0

Unknown keys are errors, so a typo stops the run instead of being ignored.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from sim.core.methods import METHODS
from sim.plugins.scenarios import SCENARIOS
from sim.plugins.sheep import SHEEP_MODELS

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = REPO_ROOT / "results"
PROTOCOLS_DIR = REPO_ROOT / "protocols" / "configs" / "protocols"

# Keys a protocol file must set, and the optional ones, besides canonical values
# (``extends`` is resolved by _read_chain before these are checked).
REQUIRED_KEYS = (
    "protocol_id",
    "output",
    "canonical",
    "methods",
    "layouts",
    "flock_sizes",
    "shepherd_counts",
)
PROTOCOL_KEYS = (*REQUIRED_KEYS, "factors")
TIME_LIMIT_KEYS = ("time_limit_ticks", "time_limit_seconds", "time_limit_drive_multiple")
METHOD_KEYS = (*TIME_LIMIT_KEYS, "params", "calibrate_as")

# Canonical values that hold for the whole protocol, so they cannot be swept as
# factors: the task, the seed list, and the calibration of R_f, which runs once
# per method and flock size whatever the factors.
WHOLE_PROTOCOL_KEYS = (
    "task",
    "master_seed",
    "calibration_seeds",
    "calibration_seconds",
    "calibration_window_seconds",
    "calibration_starts",
    "settled_tolerance",
    "start_agreement",
    "impose_radius_above",
    "imposed_radius_scale",
)

# Canonical values that only steer the adaptive run; they do not change any
# trial, so they stay out of the physics hash and cannot be swept either.
STRATEGY_KEYS = (
    "reliability_theta",
    "confidence",
    "batch_seeds",
    "max_seeds",
    "time_margin",
    "min_pairs",
    "bootstrap_resamples",
    "timeseries_seeds",
    "budget_hours",
    "refine_min_gap",
    "prune_overlap",
    "decide_finish_times",
)


# Settings added after the first runs. At their neutral value they do not change any trial, so
# they stay out of the physics hash and the folders written before them remain resumable.
NEUTRAL_SETTINGS = {
    "success_fraction": 1.0,
    "hold_drive_multiple": 0.0,
    "hold_withdraw": False,
    "dog_spacing": 0.0,
    "impose_radius_above": 0,
    "drive_offset_cap": 0.0,
    "sensing_range": 0.0,
    "communication": "none",
    "imposed_radius_scale": 1.0,
    # Hashed when not 1: it leaves the outcome of a trial as it is but changes the rows (the
    # arrival columns, the metric summaries), which must agree within a folder.
    "metrics_stride": 1,
}


@dataclass(frozen=True)
class MethodSpec:
    name: str
    # Fixed limit in ticks, or None when the limit is a multiple of the drive time
    # (``time_limit_drive_multiple``), which depends on N and is resolved per cell.
    time_limit_ticks: int | None
    params: dict[str, Any] = field(default_factory=dict)
    time_limit_drive_multiple: float | None = None
    # Method whose single dog drives the calibration flock, when not this one. R_f then
    # comes from the same reference drive as that method's, so both run the same task
    # (goal, drive, deadline). Only between methods with the same sheep model.
    calibrate_as: str | None = None


@dataclass(frozen=True)
class Protocol:
    protocol_id: str
    output: Path
    settings: dict[str, Any]  # canonical values after overrides
    methods: tuple[MethodSpec, ...]
    layouts: tuple[str, ...]
    flock_sizes: tuple[int, ...]
    shepherd_counts: tuple[int, ...]
    factors: dict[str, list[Any]]
    resolved: dict[str, Any]  # the merged file contents, archived in the results folder

    def method_config(self) -> dict[str, dict[str, Any]]:
        """Every parameter each method runs with: code defaults under the protocol's overrides."""
        return {m.name: {**METHODS[m.name].defaults, **m.params} for m in self.methods}

    def physics(self) -> dict[str, Any]:
        """Everything that changes a trial's outcome; input of the physics hash.

        The layout set and the largest D size the field and place the goal of
        every cell (the task's build_setup), so both are physics. The flock
        sizes, the smaller D and the strategy keys are not, so a campaign can
        add flock sizes, intermediate D or seeds and still resume. Settings
        owned by another task are not read by this one, so they are left out.
        """
        task = str(self.settings["task"])
        others = {k for name, t in SCENARIOS.items() if name != task for k in t.own_settings}
        return {
            "task": task,
            "layouts": sorted(set(self.layouts)),
            "max_dogs": max(self.shepherd_counts),
            "settings": {
                k: v
                for k, v in self.settings.items()
                if k not in STRATEGY_KEYS and k not in others and NEUTRAL_SETTINGS.get(k) != v
            },
            "methods": {
                m.name: {
                    "time_limit_ticks": m.time_limit_ticks,
                    "time_limit_drive_multiple": m.time_limit_drive_multiple,
                    "config": config,
                    # Left out when unset, so folders written before it keep their hash.
                    **({"calibrate_as": m.calibrate_as} if m.calibrate_as else {}),
                }
                for m, config in zip(self.methods, self.method_config().values())
            },
        }


def sweepable(settings: Mapping[str, Any]) -> list[str]:
    """Canonical settings a protocol may sweep as factors: every one that changes a
    trial and is set per D curve (so not a whole-protocol or strategy key)."""
    fixed = set(WHOLE_PROTOCOL_KEYS) | set(STRATEGY_KEYS)
    return sorted(k for k in settings if k not in fixed)


def factor_settings(factors: Mapping[str, Any], settings: Mapping[str, Any]) -> dict[str, Any]:
    """The canonical settings a factor assignment sets.

    A factor is a sweepable canonical setting. A method parameter is refused: R_f is calibrated
    once per method without factors, so a sheep-side parameter would run every level on the
    radius of the default flock. Run each level of a method parameter as its own protocol,
    which calibrates on its own.
    """
    swept = sweepable(settings)
    unknown = sorted(set(factors) - set(swept))
    if unknown:
        raise ValueError(f"factors {unknown} are not sweepable canonical settings ({swept})")
    return dict(factors)


def find_protocol(name_or_path: str) -> Path:
    """Protocol id under protocols/configs/protocols/, or a path to a YAML file."""
    path = Path(name_or_path)
    if path.suffix in (".yaml", ".yml"):
        if path.is_file():
            return path.resolve()
        raise FileNotFoundError(f"Protocol file not found: {name_or_path}")
    candidate = PROTOCOLS_DIR / f"{name_or_path}.yaml"
    if candidate.is_file():
        return candidate
    raise FileNotFoundError(f"Protocol {name_or_path!r} not found under {PROTOCOLS_DIR}")


def _read_chain(path: Path, seen: tuple[Path, ...] = ()) -> dict[str, Any]:
    """The file merged over its ``extends`` parent (child keys win)."""
    if path in seen:
        raise ValueError(f"extends cycle: {' -> '.join(map(str, seen + (path,)))}")
    spec = yaml.safe_load(path.read_text()) or {}
    if not isinstance(spec, dict):
        raise ValueError(f"Protocol must be a mapping: {path}")
    parent = spec.pop("extends", None)
    if parent is None:
        return spec
    return {**_read_chain((path.parent / str(parent)).resolve(), seen + (path,)), **spec}


def method_dt(name: str, params: Mapping[str, Any]) -> float:
    """Time step of a method: its default, or the protocol's override."""
    return float(params.get("dt", METHODS[name].defaults["dt"]))


def sheep_speed_per_second(method: str, params: Mapping[str, Any]) -> float:
    """Fastest a sheep of ``method`` can move, in units per model second: the sheep model's
    ``top_speed`` on the method's parameters under the protocol's overrides."""
    bundle = METHODS[method]
    return SHEEP_MODELS[bundle.sheep_model].top_speed({**bundle.defaults, **params})


def drive_limit_ticks(multiple: float, drive: float, method: str, params: Mapping[str, Any]) -> int:
    """Ticks in ``multiple`` x the drive time: the drive length at the top sheep speed."""
    seconds = multiple * drive / sheep_speed_per_second(method, params)
    return max(1, math.ceil(seconds / method_dt(method, params)))


def _time_limit(name: str, spec: dict[str, Any]) -> tuple[int | None, float | None]:
    """(ticks, drive multiple): exactly one of the three time-limit keys, the other None."""
    given = [k for k in TIME_LIMIT_KEYS if k in spec]
    if len(given) != 1:
        raise ValueError(f"Method {name!r}: give exactly one of {', '.join(TIME_LIMIT_KEYS)}")
    if given[0] == "time_limit_drive_multiple":
        multiple = float(spec["time_limit_drive_multiple"])
        if not multiple > 0.0:
            raise ValueError(f"Method {name!r}: time_limit_drive_multiple must be positive")
        return None, multiple
    if given[0] == "time_limit_ticks":
        ticks = float(spec["time_limit_ticks"])
    else:
        ticks = float(spec["time_limit_seconds"]) / method_dt(name, spec.get("params", {}))
    if not math.isclose(ticks, round(ticks)) or round(ticks) < 1:
        raise ValueError(f"Method {name!r}: the time limit must be a whole number of ticks >= 1")
    return int(round(ticks)), None


def _methods(raw: dict[str, Any]) -> tuple[MethodSpec, ...]:
    specs = []
    for name, spec in raw.items():
        if name not in METHODS:
            raise ValueError(f"Unknown method {name!r}; available: {sorted(METHODS)}")
        spec = spec or {}
        unknown = sorted(set(spec) - set(METHOD_KEYS))
        if unknown:
            raise ValueError(f"Method {name!r}: unknown keys {unknown}")
        params = dict(spec.get("params", {}))
        bad = sorted(set(params) - set(METHODS[name].defaults))
        if bad:
            raise ValueError(f"Method {name!r} has no parameters {bad}")
        ticks, multiple = _time_limit(name, spec)
        source = spec.get("calibrate_as")
        if source is not None:
            if source not in METHODS:
                raise ValueError(f"Method {name!r}: calibrate_as {source!r} is not a method")
            if METHODS[source].sheep_model != METHODS[name].sheep_model:
                raise ValueError(
                    f"Method {name!r}: calibrate_as {source!r} has another sheep model"
                )
            if set(METHODS[source].defaults) != set(METHODS[name].defaults):
                raise ValueError(f"Method {name!r}: calibrate_as {source!r} has other parameters")
            source = None if source == name else str(source)
        specs.append(MethodSpec(name, ticks, params, multiple, source))
    return tuple(specs)


def _check_shape(name: str, spec: Mapping[str, Any], settings: Mapping[str, Any]) -> None:
    """Grid and decision values a run could not use; caught here, not after calibration."""
    missing = [k for k in REQUIRED_KEYS if k not in spec]
    if missing:
        raise ValueError(f"{name}: missing keys {missing}")
    lists = {k: spec[k] for k in ("layouts", "flock_sizes", "shepherd_counts")}
    lists.update({f"factor {k}": v for k, v in (spec.get("factors") or {}).items()})
    for key, value in lists.items():
        if not isinstance(value, list) or not value:
            raise ValueError(f"{name}: {key} must be a non-empty list")
        if len({str(v) for v in value}) != len(value):
            raise ValueError(f"{name}: {key} has repeated values")
    if not isinstance(spec["methods"], dict) or not spec["methods"]:
        raise ValueError(f"{name}: methods must name at least one method")
    task = str(settings["task"])
    if task not in SCENARIOS:
        raise ValueError(f"{name}: unknown task {task!r}; available: {sorted(SCENARIOS)}")
    layouts = SCENARIOS[task].layouts
    unknown = sorted(set(spec["layouts"]) - set(layouts))
    if unknown:
        raise ValueError(f"{name}: unknown layouts {unknown} for task {task!r}; its are {layouts}")
    for key in ("flock_sizes", "shepherd_counts"):
        if any(not isinstance(v, int) or v < 1 for v in spec[key]):
            raise ValueError(f"{name}: {key} must be positive integers")
    if not 0.0 < float(settings["reliability_theta"]) < 1.0:
        raise ValueError(f"{name}: reliability_theta must lie between 0 and 1")
    if not 0.0 < float(settings["confidence"]) < 1.0:
        raise ValueError(f"{name}: confidence must lie between 0 and 1")
    if not 1 <= int(settings["batch_seeds"]) <= int(settings["max_seeds"]):
        raise ValueError(f"{name}: need 1 <= batch_seeds <= max_seeds")


def _check_layout_scale(
    name: str, methods: tuple[MethodSpec, ...], settings: Mapping[str, Any]
) -> None:
    """The scattered layouts are sized by the collect distance r_a N^(2/3), so
    ``separation_scale`` must equal r_a of every Strombom method in the protocol.

    A protocol that changes r_a (the field-matched sheep set) must change the scale with it,
    or its scattered starts stop meaning "beyond the distance where the dogs collect".
    """
    for m in methods:
        r_a = m.params.get("r_a", METHODS[m.name].defaults.get("r_a"))
        if r_a is not None and abs(float(settings["separation_scale"]) - float(r_a)) > 1e-9:
            scale = settings["separation_scale"]
            raise ValueError(
                f"{name}: separation_scale ({scale}) must equal r_a ({r_a}) of {m.name}; "
                + "set both in the protocol"
            )


def _check_calibration_windows(name: str, settings: Mapping[str, Any]) -> None:
    """calibration.measure averages the last two windows of a run; both must fit."""
    seconds = float(settings["calibration_seconds"])
    window = float(settings["calibration_window_seconds"])
    if seconds < 2.0 * window:
        need = f"at least 2 x calibration_window_seconds ({window:g})"
        raise ValueError(f"{name}: calibration_seconds ({seconds:g}) must be {need}")


def resolve_output(output: str | Path) -> Path:
    """Output folder: under results/ when inside the repo; anywhere outside it."""
    path = Path(output)
    if not path.is_absolute():
        path = REPO_ROOT / path
    path = path.resolve()
    inside_repo = path.is_relative_to(REPO_ROOT)
    if inside_repo and not path.is_relative_to(RESULTS_ROOT):
        raise ValueError(f"Output inside the repo must be under {RESULTS_ROOT}, got {path}")
    return path


def results_folder(name: str) -> Path:
    """A finished run's folder: a path as given, else results/<protocol_id>."""
    path = Path(name)
    return path if path.exists() else RESULTS_ROOT / name


def load_protocol(name_or_path: str, output: Path | None = None) -> Protocol:
    path = find_protocol(name_or_path)
    spec = _read_chain(path)
    if "canonical" not in spec:
        raise ValueError(f"{path.name}: missing key 'canonical'")
    canonical_path = REPO_ROOT / str(spec["canonical"])
    canonical = yaml.safe_load(canonical_path.read_text())

    unknown = sorted(set(spec) - set(PROTOCOL_KEYS) - set(canonical))
    if unknown:
        raise ValueError(f"{path.name}: unknown keys {unknown}")
    settings = {**canonical, **{k: v for k, v in spec.items() if k in canonical}}
    _check_shape(path.name, spec, settings)

    factors = dict(spec.get("factors") or {})
    methods = _methods(spec["methods"])
    try:
        factor_settings(factors, settings)
    except ValueError as error:
        raise ValueError(f"{path.name}: {error}") from error
    _check_calibration_windows(path.name, settings)
    _check_layout_scale(path.name, methods, settings)

    return Protocol(
        protocol_id=str(spec["protocol_id"]),
        output=resolve_output(output if output is not None else spec["output"]),
        settings=settings,
        methods=methods,
        layouts=tuple(spec["layouts"]),
        flock_sizes=tuple(spec["flock_sizes"]),
        shepherd_counts=tuple(sorted(spec["shepherd_counts"])),
        factors=factors,
        resolved={**spec, "canonical_values": canonical},
    )
