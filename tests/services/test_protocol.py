"""Protocol loading: validation guards, extends inheritance, physics hash, cell configs."""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
import yaml

from protocols.packaging.provenance import stable_hash
from services.cells import Cell, Group, cell_config, groups
from services.protocol import PROTOCOLS_DIR, load_protocol
from sim.core.simulation_runner import run_trial
from tests.helpers import BASE_PROTOCOL, protocol_with

BASE: dict[str, Any] = {
    "protocol_id": "t",
    "output": "results/t",
    "canonical": "protocols/configs/canonical.yaml",
    "methods": {"strombom_multi": {"time_limit_ticks": 100}},
    "layouts": ["compact"],
    "flock_sizes": [10],
    "shepherd_counts": [1, 2],
}


def write_protocol(tmp_path: Path, **changes: Any) -> Path:
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump({**BASE, **changes}))
    return path


def test_protocol_loading_and_inheritance(tmp_path: Path) -> None:
    # 1. Base protocol loading with defaults
    base_file = write_protocol(tmp_path)
    p = load_protocol(str(base_file), output=tmp_path / "out")
    assert p.methods[0].time_limit_ticks == 100
    assert p.settings["reliability_theta"] == 0.90

    # 2. Child protocol inheritance via extends
    child_file = tmp_path / "child.yaml"
    child_file.write_text(
        yaml.safe_dump({"extends": base_file.name, "protocol_id": "c", "flock_sizes": [20]})
    )
    child = load_protocol(str(child_file), output=tmp_path / "out")
    assert child.protocol_id == "c"
    assert child.flock_sizes == (20,)

    # 3. calibrate_as method mapping
    fat_file = write_protocol(
        tmp_path,
        methods={
            "strombom_multi": {"time_limit_ticks": 100},
            "fat": {"time_limit_ticks": 100, "calibrate_as": "strombom_multi"},
        },
    )
    p_fat = load_protocol(str(fat_file), output=tmp_path / "out")
    fat_spec = next(m for m in p_fat.methods if m.name == "fat")
    assert fat_spec.calibrate_as == "strombom_multi"


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"seeds": 30}, "unknown keys"),
        (
            {"methods": {"kubo": {"time_limit_ticks": 100, "params": {"r_s": 30.0}}}},
            "no parameters",
        ),
        (
            {"methods": {"kubo": {"time_limit_ticks": 100, "time_limit_seconds": 5}}},
            "exactly one",
        ),
        ({"layouts": "compact"}, "non-empty list"),
        ({"layouts": ["unknown_layout"]}, "unknown layouts"),
        ({"flock_sizes": [10, 10]}, "repeated"),
        ({"shepherd_counts": [0, 1]}, "positive integers"),
        ({"methods": {}}, "at least one method"),
        ({"methods": {"strombom_multi": {"time_limit_ticks": 0}}}, "ticks >= 1"),
        ({"batch_seeds": 20, "max_seeds": 10}, "batch_seeds"),
        ({"reliability_theta": 1.5}, "reliability_theta"),
        ({"factors": {"master_seed": [1, 2]}}, "not sweepable"),
        ({"methods": {"fat": {"time_limit_ticks": 100, "calibrate_as": "nope"}}}, "not a method"),
    ],
)
def test_protocol_validation_guards(tmp_path: Path, changes: dict[str, Any], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        load_protocol(str(write_protocol(tmp_path, **changes)), output=tmp_path / "out")


def test_protocol_missing_key_and_output_guards(tmp_path: Path) -> None:
    incomplete = {k: v for k, v in BASE.items() if k != "layouts"}
    bad_file = tmp_path / "bad.yaml"
    bad_file.write_text(yaml.safe_dump(incomplete))
    with pytest.raises(ValueError, match="missing keys"):
        load_protocol(str(bad_file), output=tmp_path / "out")

    with pytest.raises(ValueError, match="under"):
        load_protocol("dmin_pilot", output=Path("docs/out"))


def test_layout_scale_must_follow_r_a(tmp_path: Path) -> None:
    """Changing r_a without separation_scale changes physical meaning of scattered layouts."""
    methods = {"strombom_multi": {"time_limit_ticks": 100, "params": {"r_a": 1.0}}}
    with pytest.raises(ValueError, match="separation_scale"):
        load_protocol(str(write_protocol(tmp_path, methods=methods)), output=tmp_path / "out")

    ok = write_protocol(
        tmp_path, methods=methods, separation_scale=1.0, dog_overlap_distance=1.0
    )
    assert load_protocol(str(ok), output=tmp_path / "out").settings["separation_scale"] == 1.0


def test_physics_hash_invariance_and_sensitivity() -> None:
    """Strategy settings stay out of physics hash; physical parameters change it."""
    base = stable_hash(BASE_PROTOCOL.physics())

    assert stable_hash(protocol_with(ticks=3000, settings={"max_seeds": 400}).physics()) == base
    assert stable_hash(protocol_with(ticks=3000, settings={"refine_min_gap": 4}).physics()) == base

    assert (
        stable_hash(protocol_with(ticks=3000, settings={"drive_distance_multiple": 14.0}).physics())
        != base
    )
    assert stable_hash(protocol_with(ticks=3000, params={"n_neighbors": 7}).physics()) != base

    assert stable_hash(replace(BASE_PROTOCOL, layouts=("compact", "wide")).physics()) != base
    top = max(BASE_PROTOCOL.shepherd_counts)
    assert (
        stable_hash(
            replace(
                BASE_PROTOCOL, shepherd_counts=(*BASE_PROTOCOL.shepherd_counts, 2 * top)
            ).physics()
        )
        != base
    )

    strict = protocol_with(ticks=3000)
    relaxed = protocol_with(ticks=3000, settings={"success_fraction": 0.99})
    assert "success_fraction" not in strict.physics()["settings"]
    assert relaxed.physics()["settings"]["success_fraction"] == 0.99
    assert stable_hash(strict.physics()) != stable_hash(relaxed.physics())


def test_physics_hash_numeric_equivalence() -> None:
    """YAML ints and floats run identical physics and must resume each other."""
    as_int = protocol_with(ticks=3000, settings={"drive_distance_multiple": 13})
    as_float = protocol_with(ticks=3000, settings={"drive_distance_multiple": 13.0})
    assert stable_hash(as_int.physics()) == stable_hash(as_float.physics())
    assert stable_hash({"a": [1, {"b": 2}]}) == stable_hash({"a": [1.0, {"b": 2.0}]})
    assert stable_hash({"a": True}) != stable_hash({"a": 1.0})


def test_cell_config_factor_expansion(tmp_path: Path) -> None:
    """Factors sweep canonical settings and propagate into runner cell configs."""
    path = write_protocol(tmp_path, factors={"drive_distance_multiple": [13.0, 20.0]})
    protocol = load_protocol(str(path), output=tmp_path / "out")
    assert protocol.factors == {"drive_distance_multiple": [13.0, 20.0]}

    near = Cell(Group("strombom_multi", "compact", (("drive_distance_multiple", 13.0),), 20), 2)
    far = Cell(Group("strombom_multi", "compact", (("drive_distance_multiple", 20.0),), 20), 2)

    cfg_near = cell_config(protocol, near, 7.0)
    cfg_far = cell_config(protocol, far, 7.0)
    drive_near = cfg_near["goal_center"][0] - cfg_near["flock_center"][0]
    drive_far = cfg_far["goal_center"][0] - cfg_far["flock_center"][0]

    assert drive_near == pytest.approx(13.0 * 7.0)
    assert drive_far == pytest.approx(20.0 * 7.0)


def test_time_limit_drive_multiple(tmp_path: Path) -> None:
    """Deadline can scale with drive distance and enters physics hash."""
    methods = {"strombom_multi": {"time_limit_drive_multiple": 4.0}}
    p = load_protocol(
        str(write_protocol(tmp_path, methods=methods, flock_sizes=[50])), output=tmp_path / "out"
    )
    assert p.methods[0].time_limit_ticks is None
    assert p.methods[0].time_limit_drive_multiple == 4.0

    group = Group("strombom_multi", "compact", (), 50)
    cfg = cell_config(p, Cell(group, 2), flock_radius=7.0)
    drive_dist = abs(cfg["goal_center"][0] - cfg["flock_center"][0])
    assert cfg["max_ticks"] == math.ceil(4.0 * drive_dist)

    p_fast = load_protocol(
        str(
            write_protocol(
                tmp_path, methods={"strombom_multi": {"time_limit_drive_multiple": 8.0}}
            )
        ),
        output=tmp_path / "out2",
    )
    assert stable_hash(p.physics()) != stable_hash(p_fast.physics())


def test_shipped_protocols_validity() -> None:
    """All shipped protocol files parse, resolve extends, and build valid runner cells."""
    protocol_files = sorted(PROTOCOLS_DIR.glob("*.yaml"))
    assert len(protocol_files) > 0

    for path in protocol_files:
        protocol = load_protocol(path.stem)
        assert protocol.protocol_id == path.stem
        assert len(protocol.methods) >= 1
        for group in groups(protocol):
            cell = Cell(group, max(protocol.shepherd_counts))
            config = cell_config(protocol, cell, flock_radius=10.0)
            assert "method" in config and "goal_center" in config

    pilot = load_protocol("dmin_pilot")
    first_group = next(iter(groups(pilot)))
    cfg = cell_config(pilot, Cell(first_group, max(pilot.shepherd_counts)), flock_radius=10.0)
    result = run_trial({**cfg, "max_ticks": 2}, pilot.settings["master_seed"])
    assert result.total_ticks <= 2

