"""Load and check a protocol: canonical defaults, optional ``extends`` chain, the protocol.

A protocol is one experiment written as data, in protocols/configs/protocols/. It names its
output folder, the methods with their time limits and parameter overrides, the grid
(layouts, flock sizes, dog counts) and any canonical value it changes. Everything else comes from
protocols/configs/canonical.yaml. A protocol can ``extends`` another and change only what
differs, which is how a variant of a finished run gets its own id and folder:

    protocol_id: dmin_f99_m6
    output: results/dmin_f99_m6
    extends: dmin_m6.yaml
    success_fraction: 0.99

Unknown keys are errors, so a typo stops the run instead of being ignored.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from records.provenance import stable_hash
from sim.drive_task import task as drive_task
from sim.drive_task.layouts import LAYOUTS
from sim.strombom import sheep
from sim.strombom.params import DEFAULTS, METHOD, NEUTRAL_PARAMS

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = REPO_ROOT / "results"
QUEUE_LOG = RESULTS_ROOT / "queue_log.jsonl"  # one line per protocol the study queue ran
CANONICAL = REPO_ROOT / "protocols" / "configs" / "canonical.yaml"  # the study's defaults
PROTOCOLS_DIR = REPO_ROOT / "protocols" / "configs" / "protocols"
STUDY_QUEUE = REPO_ROOT / "protocols" / "configs" / "study_queue.yaml"

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
PROTOCOL_KEYS = (*REQUIRED_KEYS, "description")
TIME_LIMIT_KEYS = ("time_limit_ticks", "time_limit_drive_multiple")
METHOD_KEYS = (*TIME_LIMIT_KEYS, "params")

# Canonical values that hold for the whole protocol: the task, the seed list, and the
# calibration of R_f, which runs once per method and flock size.
WHOLE_PROTOCOL_KEYS = (
    "task",
    "master_seed",
    "calibration_seeds",
    "calibration_seconds",
    "calibration_window_seconds",
    "calibration_starts",
)

# Canonical values that only steer the adaptive run; they do not change any trial, so they
# stay out of the physics hash.
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

# The tolerances of the calibration only decide whether it stops, never the R_f it measures,
# so they stay out of the physics hash too: a folder whose calibration passes a tighter
# tolerance holds the same trials.
CALIBRATION_CHECKS = ("settled_tolerance", "start_agreement")

# A setting at its neutral value changes no trial, so it stays out of the physics hash; a
# folder written before the setting existed keeps its hash.
NEUTRAL_SETTINGS = {"success_fraction": 1.0}

# The range each numeric canonical value must lie in, checked at load: the engine would
# otherwise meet a bad value only inside the workers, after calibration has run.
WHOLE_AT_LEAST_ONE = (
    "calibration_seeds",
    "batch_seeds",
    "max_seeds",
    "min_pairs",
    "bootstrap_resamples",
    "refine_min_gap",
)
WHOLE_AT_LEAST_ZERO = ("master_seed", "timeseries_seeds")
POSITIVE = (
    "goal_radius_multiple",
    "separation_scale",
    "measurement_radius",
    "lost_radius_multiple",
    "calibration_seconds",
    "calibration_window_seconds",
    "settled_tolerance",
    "start_agreement",
    "budget_hours",
)
AT_LEAST_ZERO = (
    "drive_distance_min",
    "field_clearance",
    "compact_spread",
    "wide_sigma",
    "split_ring",
    "outlier_near",
    "outlier_far",
    "dog_start_gap",
    "dog_overlap_distance",
    "time_margin",
    "prune_overlap",
)
FRACTIONS = ("outlier_fraction",)
OPEN_FRACTIONS = ("reliability_theta", "confidence")
# Checked by the task itself (drive_task.check_settings), which load_protocol also calls.
TASK_CHECKED = ("success_fraction", "dog_start_spacing", "drive_distance_multiple")
SWITCHES = ("decide_finish_times",)
LAYOUT_SCALE_TOLERANCE = 1e-9  # separation_scale and r_a are equal up to float noise


@dataclass(frozen=True)
class MethodSpec:
    name: str
    # Fixed limit in ticks, or None when the limit is a multiple of the drive time
    # (``time_limit_drive_multiple``), which depends on N and is resolved per cell.
    time_limit_ticks: int | None
    params: dict[str, Any] = field(default_factory=dict)
    time_limit_drive_multiple: float | None = None


@dataclass(frozen=True)
class Protocol:
    protocol_id: str
    output: Path
    settings: dict[str, Any]  # canonical values after overrides
    methods: tuple[MethodSpec, ...]
    layouts: tuple[str, ...]
    flock_sizes: tuple[int, ...]
    shepherd_counts: tuple[int, ...]
    resolved: dict[str, Any]  # the merged file contents, archived in the results folder
    # One line on what the protocol tests, for the protocol catalogue; never physics.
    description: str | None = None

    def method_config(self) -> dict[str, dict[str, Any]]:
        """Every parameter each method runs with: code defaults under the protocol's overrides."""
        return {m.name: {**DEFAULTS, **m.params} for m in self.methods}

    def physics_hash(self) -> str:
        return stable_hash(self.physics())

    def physics(self) -> dict[str, Any]:
        """Everything that changes a trial's outcome; input of the physics hash.

        The layout set and the largest D size the field and place the goal of every cell
        (the task's build_setup), so both are physics. The flock sizes, the smaller D, the
        strategy keys and the calibration tolerances are not, so a campaign can add flock
        sizes, intermediate D or seeds and still resume.
        """
        methods = self.method_config()
        return {
            "task": self.settings["task"],
            "layouts": sorted(set(self.layouts)),
            "max_dogs": max(self.shepherd_counts),
            "settings": {
                k: v
                for k, v in self.settings.items()
                if k not in (*STRATEGY_KEYS, *CALIBRATION_CHECKS) and NEUTRAL_SETTINGS.get(k) != v
            },
            "methods": {
                m.name: {
                    "time_limit_ticks": m.time_limit_ticks,
                    "time_limit_drive_multiple": m.time_limit_drive_multiple,
                    "config": {
                        k: v for k, v in methods[m.name].items() if NEUTRAL_PARAMS.get(k) != v
                    },
                }
                for m in self.methods
            },
        }


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


def study_queue() -> tuple[str, ...]:
    """The study's protocol ids in the order the queue runs them."""
    return tuple(yaml.safe_load(STUDY_QUEUE.read_text())["queue"])


def _read_chain(path: Path, seen: tuple[Path, ...] = ()) -> dict[str, Any]:
    """The file merged over its ``extends`` parent (child keys win).

    The parent's ``description`` is dropped: it says what the parent tests, so a child that
    inherited it would be catalogued under the wrong question.
    """
    if path in seen:
        raise ValueError(f"extends cycle: {' -> '.join(map(str, seen + (path,)))}")
    spec = yaml.safe_load(path.read_text()) or {}
    if not isinstance(spec, dict):
        raise ValueError(f"Protocol must be a mapping: {path}")
    parent = spec.pop("extends", None)
    if parent is None:
        return spec
    inherited = _read_chain((path.parent / parent).resolve(), seen + (path,))
    inherited.pop("description", None)
    return {**inherited, **spec}


def method_dt(params: Mapping[str, Any]) -> float:
    """Time step of the method: its default, or the protocol's override."""
    return float(params.get("dt", DEFAULTS["dt"]))


def sheep_speed_per_second(params: Mapping[str, Any]) -> float:
    """Fastest a sheep can move, in units per model second, under the protocol's overrides."""
    return sheep.top_speed({**DEFAULTS, **params})


def drive_limit_ticks(multiple: float, drive: float, params: Mapping[str, Any]) -> int:
    """Ticks in ``multiple`` x the drive time: the drive length at the top sheep speed."""
    seconds = multiple * drive / sheep_speed_per_second(params)
    return max(1, math.ceil(seconds / method_dt(params)))


def _time_limit(name: str, spec: dict[str, Any]) -> tuple[int | None, float | None]:
    """(ticks, drive multiple): exactly one of the two time-limit keys, the other None."""
    given = [k for k in TIME_LIMIT_KEYS if k in spec]
    if len(given) != 1:
        raise ValueError(f"Method {name!r}: give exactly one of {', '.join(TIME_LIMIT_KEYS)}")
    if given[0] == "time_limit_drive_multiple":
        multiple = spec["time_limit_drive_multiple"]
        if not (_is_number(multiple) and multiple > 0.0):
            raise ValueError(
                f"Method {name!r}: time_limit_drive_multiple must be positive, got {multiple!r}"
            )
        return None, multiple
    ticks = spec["time_limit_ticks"]
    whole = _is_number(ticks) and math.isclose(ticks, round(ticks)) and round(ticks) >= 1
    if not whole:
        wanted = "a whole number of ticks >= 1"
        raise ValueError(f"Method {name!r}: time_limit_ticks must be {wanted}, got {ticks!r}")
    return round(ticks), None


def _methods(raw: dict[str, Any]) -> tuple[MethodSpec, ...]:
    specs = []
    for name, spec in raw.items():
        if name != METHOD:
            raise ValueError(f"Unknown method {name!r}; available: {[METHOD]}")
        spec = spec or {}
        unknown = sorted(set(spec) - set(METHOD_KEYS))
        if unknown:
            raise ValueError(f"Method {name!r}: unknown keys {unknown}")
        params = dict(spec.get("params", {}))
        bad = sorted(set(params) - set(DEFAULTS))
        if bad:
            raise ValueError(f"Method {name!r} has no parameters {bad}")
        # A switch must be a YAML bool: "false" would read as on and escape the neutral
        # filter, and 1 would run as on but hash apart from true.
        for key, value in params.items():
            if isinstance(DEFAULTS[key], bool) and not isinstance(value, bool):
                raise ValueError(f"Method {name!r}: {key} must be true or false, not {value!r}")
        ticks, multiple = _time_limit(name, spec)
        specs.append(MethodSpec(name, ticks, params, multiple))
    return tuple(specs)


def _check_shape(name: str, spec: Mapping[str, Any], settings: Mapping[str, Any]) -> None:
    """The grid a run could not use; caught here, not after calibration."""
    missing = [k for k in REQUIRED_KEYS if k not in spec]
    if missing:
        raise ValueError(f"{name}: missing keys {missing}")
    for key in ("layouts", "flock_sizes", "shepherd_counts"):
        value = spec[key]
        if not isinstance(value, list) or not value:
            raise ValueError(f"{name}: {key} must be a non-empty list")
        if len({str(v) for v in value}) != len(value):
            raise ValueError(f"{name}: {key} has repeated values")
    if not isinstance(spec["methods"], dict) or not spec["methods"]:
        raise ValueError(f"{name}: methods must name at least one method")
    _check_task_and_layouts(name, spec["layouts"], settings["task"])
    if any(not (_is_number(v) and isinstance(v, int) and v >= 2) for v in spec["flock_sizes"]):
        raise ValueError(f"{name}: flock_sizes must be integers >= 2")
    if any(not (_is_number(v) and isinstance(v, int) and v >= 1) for v in spec["shepherd_counts"]):
        raise ValueError(f"{name}: shepherd_counts must be positive integers")


def _check_task_and_layouts(name: str, layouts: list[str], task: str) -> None:
    if task != drive_task.TASK:
        raise ValueError(f"{name}: unknown task {task!r}; available: {[drive_task.TASK]}")
    unknown = sorted(set(layouts) - set(LAYOUTS))
    if unknown:
        known = f"its layouts are {LAYOUTS}"
        raise ValueError(f"{name}: unknown layouts {unknown} for task {task!r}; {known}")


def _check_batches(name: str, settings: Mapping[str, Any]) -> None:
    batch, cap = settings["batch_seeds"], settings["max_seeds"]
    if batch > cap:
        raise ValueError(f"{name}: batch_seeds ({batch}) must not exceed max_seeds ({cap})")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_ranges(name: str, settings: Mapping[str, Any]) -> None:
    """Every numeric canonical value in its range, named with its value when it is not."""
    rules = (
        (WHOLE_AT_LEAST_ONE, lambda v: isinstance(v, int) and v >= 1, "a whole number >= 1"),
        (WHOLE_AT_LEAST_ZERO, lambda v: isinstance(v, int) and v >= 0, "a whole number >= 0"),
        (POSITIVE, lambda v: v > 0, "positive"),
        (AT_LEAST_ZERO, lambda v: v >= 0, "at least 0"),
        (FRACTIONS, lambda v: 0 <= v <= 1, "between 0 and 1"),
        (OPEN_FRACTIONS, lambda v: 0 < v < 1, "strictly between 0 and 1"),
    )
    ranged = {key for keys, _, _ in rules for key in keys} | set(TASK_CHECKED)
    unranged = sorted(k for k, v in settings.items() if _is_number(v) and k not in ranged)
    if unranged:  # a new canonical number must be given a range here
        raise ValueError(f"{name}: no range check for settings {unranged}")
    for keys, holds, wanted in rules:
        for key in keys:
            value = settings[key]
            if not (_is_number(value) and holds(value)):
                raise ValueError(f"{name}: {key} must be {wanted}, got {value!r}")
    for key in SWITCHES:
        if not isinstance(settings[key], bool):
            raise ValueError(f"{name}: {key} must be true or false, got {settings[key]!r}")


def _check_layout_scale(
    name: str, methods: tuple[MethodSpec, ...], settings: Mapping[str, Any]
) -> None:
    """The scattered layouts are sized by the collect distance r_a N^(2/3), so
    ``separation_scale`` must equal r_a of every Strombom method in the protocol.

    A protocol that changes r_a must change the scale with it, or its scattered starts stop
    meaning "beyond the distance where the dogs collect".
    """
    for m in methods:
        r_a = m.params.get("r_a", DEFAULTS["r_a"])
        if abs(settings["separation_scale"] - r_a) > LAYOUT_SCALE_TOLERANCE:
            scale = settings["separation_scale"]
            raise ValueError(
                f"{name}: separation_scale ({scale}) must equal r_a ({r_a}) of {m.name}; "
                + "set both in the protocol"
            )


def _check_calibration_windows(name: str, settings: Mapping[str, Any]) -> None:
    """calibration.measure averages the last two windows of a run; both must fit."""
    seconds = settings["calibration_seconds"]
    window = settings["calibration_window_seconds"]
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
    canonical_path = REPO_ROOT / spec["canonical"]
    canonical = yaml.safe_load(canonical_path.read_text())

    unknown = sorted(set(spec) - set(PROTOCOL_KEYS) - set(canonical))
    if unknown:
        raise ValueError(f"{path.name}: unknown keys {unknown}")
    settings = {**canonical, **{k: v for k, v in spec.items() if k in canonical}}
    _check_shape(path.name, spec, settings)
    _check_ranges(path.name, settings)
    drive_task.check_settings(settings)
    _check_batches(path.name, settings)
    description = spec.get("description")
    if description is not None and not (isinstance(description, str) and description.strip()):
        raise ValueError(f"{path.name}: description must be non-empty text, got {description!r}")

    methods = _methods(spec["methods"])
    _check_calibration_windows(path.name, settings)
    _check_layout_scale(path.name, methods, settings)

    return Protocol(
        protocol_id=spec["protocol_id"],
        output=resolve_output(output if output is not None else spec["output"]),
        settings=settings,
        methods=methods,
        layouts=tuple(spec["layouts"]),
        flock_sizes=tuple(spec["flock_sizes"]),
        shepherd_counts=tuple(sorted(spec["shepherd_counts"])),
        resolved={**spec, "canonical_values": canonical},
        description=description,
    )
