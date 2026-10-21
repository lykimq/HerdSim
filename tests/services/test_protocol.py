"""Protocol loading: strict keys, time limits, factor checks, physics hash."""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from protocols.packaging.provenance import stable_hash
from services.cells import Cell, Group, cell_config, groups
from services.protocol import PROTOCOLS_DIR, load_protocol
from sim.core.methods import METHODS
from sim.core.simulation_runner import run_trial
from tests.helpers import BASE_PROTOCOL, config_for, protocol_with

# Flock radii R_f calibrated by services.calibration (300 s, 3 seeds, starts of 1 and 3
# spacings), measured 2026-10-19 on the shipped protocols; above 400 the density rule applies.
# Calibration itself is not run in this test.
MEASURED_RF = {
    5: 3.14,
    10: 4.35,
    25: 6.2,
    50: 7.6,
    100: 9.08,
    200: 10.47,
    300: 11.05,
    400: 11.4,
}


def rule_rf(n_sheep: int) -> float:
    if n_sheep in MEASURED_RF:
        return MEASURED_RF[n_sheep]
    return MEASURED_RF[400] * math.sqrt(n_sheep / 400.0)


BASE = {
    "protocol_id": "t",
    "output": "results/t",
    "canonical": "protocols/configs/canonical.yaml",
    "methods": {"strombom_multi": {"time_limit_ticks": 100}},
    "layouts": ["compact"],
    "flock_sizes": [10],
    "shepherd_counts": [1, 2],
}


def write(tmp_path: Path, **changes) -> Path:
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump({**BASE, **changes}))
    return path


def test_minimal_protocol_loads(tmp_path):
    p = load_protocol(str(write(tmp_path)), output=tmp_path / "out")
    assert p.methods[0].time_limit_ticks == 100
    assert p.settings["reliability_theta"] == 0.90


def test_unknown_top_level_key_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="unknown keys"):
        load_protocol(str(write(tmp_path, seeds=30)), output=tmp_path / "out")


def test_unknown_method_parameter_is_rejected(tmp_path):
    methods = {"kubo": {"time_limit_ticks": 100, "params": {"r_s": 30.0}}}
    with pytest.raises(ValueError, match="no parameters"):
        load_protocol(str(write(tmp_path, methods=methods)), output=tmp_path / "out")


def test_time_limit_needs_exactly_one_unit(tmp_path):
    methods = {"kubo": {"time_limit_ticks": 100, "time_limit_seconds": 5}}
    with pytest.raises(ValueError, match="exactly one"):
        load_protocol(str(write(tmp_path, methods=methods)), output=tmp_path / "out")


def test_extends_merges_child_over_parent(tmp_path):
    parent = write(tmp_path)
    child = tmp_path / "child.yaml"
    child.write_text(
        yaml.safe_dump({"extends": parent.name, "protocol_id": "c", "flock_sizes": [20]})
    )
    p = load_protocol(str(child), output=tmp_path / "out")
    assert p.protocol_id == "c" and p.flock_sizes == (20,)


def test_output_inside_repo_must_be_under_results():
    with pytest.raises(ValueError, match="under"):
        load_protocol("dmin_pilot", output=Path("docs/out"))


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"layouts": "compact"}, "non-empty list"),
        ({"layouts": ["round"]}, "unknown layouts"),
        ({"flock_sizes": [10, 10]}, "repeated"),
        ({"shepherd_counts": [0, 1]}, "positive integers"),
        ({"factors": {"n_neighbors": []}}, "non-empty list"),
        ({"methods": {}}, "at least one method"),
        ({"methods": {"strombom_multi": {"time_limit_ticks": 0}}}, "ticks >= 1"),
        ({"batch_seeds": 20, "max_seeds": 10}, "batch_seeds"),
        ({"reliability_theta": 1.5}, "reliability_theta"),
    ],
)
def test_bad_protocol_shape_fails_at_load(tmp_path, changes, message):
    with pytest.raises(ValueError, match=message):
        load_protocol(str(write(tmp_path, **changes)), output=tmp_path / "out")


def test_missing_protocol_key_is_named(tmp_path):
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump({k: v for k, v in BASE.items() if k != "layouts"}))
    with pytest.raises(ValueError, match="missing keys"):
        load_protocol(str(path), output=tmp_path / "out")


def test_physics_hash_ignores_strategy_and_tracks_physics():
    base = stable_hash(BASE_PROTOCOL.physics())
    assert stable_hash(protocol_with(ticks=3000, settings={"max_seeds": 400}).physics()) == base
    assert stable_hash(protocol_with(ticks=3000, settings={"refine_min_gap": 4}).physics()) == base
    assert (
        stable_hash(protocol_with(ticks=3000, settings={"drive_distance_multiple": 14.0}).physics())
        != base
    )
    assert stable_hash(protocol_with(ticks=3000, params={"n_neighbors": 7}).physics()) != base


def test_success_fraction_is_in_the_hash_only_when_it_is_not_neutral():
    """Folders written before the setting existed must stay resumable."""
    strict = protocol_with(ticks=3000)
    relaxed = protocol_with(ticks=3000, settings={"success_fraction": 0.99})
    assert "success_fraction" not in strict.physics()["settings"]
    assert relaxed.physics()["settings"]["success_fraction"] == 0.99
    assert stable_hash(strict.physics()) != stable_hash(relaxed.physics())


def test_physics_hash_tracks_layouts_largest_d_and_method_defaults():
    """Layouts and the largest D size every cell's field; code defaults are physics too."""
    base = stable_hash(BASE_PROTOCOL.physics())
    top = max(BASE_PROTOCOL.shepherd_counts)
    assert stable_hash(replace(BASE_PROTOCOL, layouts=("compact", "wide")).physics()) != base
    assert (
        stable_hash(
            replace(
                BASE_PROTOCOL, shepherd_counts=(*BASE_PROTOCOL.shepherd_counts, 2 * top)
            ).physics()
        )
        != base
    )
    # Growing inward or in N still resumes.
    assert (
        stable_hash(
            replace(BASE_PROTOCOL, shepherd_counts=(*BASE_PROTOCOL.shepherd_counts, 3)).physics()
        )
        == base
    )
    assert (
        stable_hash(replace(BASE_PROTOCOL, flock_sizes=(*BASE_PROTOCOL.flock_sizes, 50)).physics())
        == base
    )
    config = BASE_PROTOCOL.physics()["methods"]["strombom_multi"]["config"]
    assert config["r_s"] == METHODS["strombom_multi"].defaults["r_s"]
    assert config["dt"] == 1.0 and BASE_PROTOCOL.physics()["task"] == "drive_to_goal"


def test_physics_hash_treats_ints_and_floats_alike():
    """YAML 13 and 13.0 run the same physics, so they must resume each other."""
    as_int = protocol_with(ticks=3000, settings={"drive_distance_multiple": 13})
    as_float = protocol_with(ticks=3000, settings={"drive_distance_multiple": 13.0})
    assert stable_hash(as_int.physics()) == stable_hash(as_float.physics())
    assert stable_hash({"a": [1, {"b": 2}]}) == stable_hash({"a": [1.0, {"b": 2.0}]})
    assert stable_hash({"a": True}) != stable_hash({"a": 1.0})


def test_layout_scale_must_follow_r_a(tmp_path):
    """Changing r_a without separation_scale would change what the scattered layouts mean."""
    methods = {
        "strombom_multi": {"time_limit_ticks": 100, "params": {"r_a": 1.0}},
    }
    with pytest.raises(ValueError, match="separation_scale"):
        load_protocol(str(write(tmp_path, methods=methods)), output=tmp_path / "out")
    ok = write(tmp_path, methods=methods, separation_scale=1.0, dog_overlap_distance=1.0)
    assert load_protocol(str(ok), output=tmp_path / "out").settings["separation_scale"] == 1.0
    kubo = {"kubo": {"time_limit_ticks": 100}}  # no r_a: any scale is accepted
    load_protocol(str(write(tmp_path, methods=kubo, separation_scale=3.0)), output=tmp_path / "out")


def test_calibration_run_must_hold_two_windows(tmp_path):
    bad = write(tmp_path, calibration_seconds=100.0, calibration_window_seconds=90.0)
    with pytest.raises(ValueError, match="calibration_seconds"):
        load_protocol(str(bad), output=tmp_path / "out")


def test_factor_must_be_a_sweepable_canonical_setting(tmp_path):
    ok = write(tmp_path, factors={"drive_distance_multiple": [13.0, 20.0]})
    loaded = load_protocol(str(ok), output=tmp_path / "out")
    assert loaded.factors == {"drive_distance_multiple": [13.0, 20.0]}
    for bad in ({"no_such_setting": [1]}, {"master_seed": [1, 2]}, {"n_neighbors": [-1, 7]}):
        with pytest.raises(ValueError, match="not sweepable"):
            load_protocol(str(write(tmp_path, factors=bad)), output=tmp_path / "out")


def test_time_limit_can_be_a_multiple_of_the_drive_time(tmp_path):
    methods = {"strombom_multi": {"time_limit_drive_multiple": 4}}
    p = load_protocol(str(write(tmp_path, methods=methods)), output=tmp_path / "out")
    assert p.methods[0].time_limit_ticks is None
    assert p.methods[0].time_limit_drive_multiple == 4.0
    for bad in (
        {"time_limit_drive_multiple": 0},
        {"time_limit_drive_multiple": 2, "time_limit_ticks": 9},
    ):
        with pytest.raises(ValueError):
            load_protocol(str(write(tmp_path, methods={"strombom_multi": bad})), output=tmp_path)


def test_drive_multiple_scales_the_limit_with_the_drive_and_enters_the_hash(tmp_path):
    def limit(multiple: float, n: int) -> int:
        methods = {"strombom_multi": {"time_limit_drive_multiple": multiple}}
        p = load_protocol(
            str(write(tmp_path, methods=methods, flock_sizes=[n])), output=tmp_path / "out"
        )
        group = Group("strombom_multi", "compact", (), n)
        return int(cell_config(p, Cell(group, 2), rule_rf(n))["max_ticks"])

    config = config_for(n=50, d=2, flock_radius=rule_rf(50))
    drive = abs(config["goal_center"][0] - config["flock_center"][0])
    assert limit(4.0, 50) == math.ceil(4.0 * drive)  # Strombom: one unit per second
    assert limit(8.0, 50) == pytest.approx(2 * limit(4.0, 50), abs=1)
    assert limit(4.0, 400) > limit(4.0, 50)  # longer drive, longer deadline

    def hash_of(multiple: float) -> str:
        methods = {"strombom_multi": {"time_limit_drive_multiple": multiple}}
        p = load_protocol(str(write(tmp_path, methods=methods)), output=tmp_path / "out")
        return stable_hash(p.physics())

    assert hash_of(4.0) != hash_of(8.0)


@pytest.mark.parametrize("path", sorted(PROTOCOLS_DIR.glob("*.yaml")), ids=lambda p: p.stem)
def test_shipped_protocol_builds_and_starts_every_group(path):
    """Every group of every shipped protocol builds a valid config at its largest D and ticks."""
    protocol = load_protocol(path.stem)
    for group in groups(protocol):
        radius = rule_rf(group.n_sheep)
        cell = Cell(group, max(protocol.shepherd_counts))
        config = cell_config(protocol, cell, radius)
        run_trial({**config, "max_ticks": 2}, protocol.settings["master_seed"])


def test_factor_can_sweep_a_setting_and_reaches_the_run_config(tmp_path):
    path = write(tmp_path, factors={"drive_distance_multiple": [13.0, 20.0]})
    protocol = load_protocol(str(path), output=tmp_path / "out")
    near = Cell(Group("strombom_multi", "compact", (("drive_distance_multiple", 13.0),), 20), 2)
    far = Cell(Group("strombom_multi", "compact", (("drive_distance_multiple", 20.0),), 20), 2)

    def drive(cell):
        config = cell_config(protocol, cell, 7.0)
        return config["goal_center"][0] - config["flock_center"][0]

    assert drive(near) == pytest.approx(13.0 * 7.0)
    assert drive(far) == pytest.approx(20.0 * 7.0)
    assert protocol.settings["drive_distance_multiple"] == 13.0  # the protocol default is untouched
