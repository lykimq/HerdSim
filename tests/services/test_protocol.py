"""Protocol loading: extends, drive-time deadlines, and the physics hash behind resume."""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path
from typing import Any, TypeAlias

import pytest
import yaml

from records.provenance import read_provenance
from services.cells import Cell, Group, cell_config, groups
from services.protocol import PROTOCOLS_DIR, Protocol, load_protocol, results_folder, study_queue
from sim.trial import run_trial
from tests.helpers import BASE_PROTOCOL, config_for, protocol_with

FlockSize: TypeAlias = int  # N sheep
FlockRadius: TypeAlias = float  # R_f in metres

METHOD = "strombom_multi"
N_DOGS = 2
SMOKE_TICKS = 2
# Anchor for the missing-N stand-in in radius_for (largest measured table entry).
RADIUS_ANCHOR_N: FlockSize = 400

# Measured R_f by N from the study runs (main sizes). Tests do not recalibrate.
# Midpoint sizes (71, 141, ...) are absent on purpose; radius_for scales those.
FLOCK_RADIUS_BY_N: dict[FlockSize, FlockRadius] = {
    25: 6.2,
    50: 7.6,
    100: 9.08,
    200: 10.47,
    400: 11.4,
}

# Minimal YAML body for draft protocols written under tmp_path.
DRAFT = {
    "protocol_id": "t",
    "output": "results/t",
    "canonical": "protocols/configs/canonical.yaml",
    "methods": {METHOD: {"time_limit_ticks": 100}},
    "layouts": ["compact"],
    "flock_sizes": [10],
    "shepherd_counts": [1, 2],
}


# --- helpers -----------------------------------------------------------------


def radius_for(n_sheep: FlockSize) -> FlockRadius:
    """R_f for a smoke-test config: table lookup, or a stand-in if N is missing.

    Real runs calibrate every N. Here, sizes absent from FLOCK_RADIUS_BY_N (for example
    71, 141, 283, 566) get R_f(400) * sqrt(N/400), a constant-density guess anchored at
    the largest table entry. Good enough to build a config and tick twice; not a fit.
    """
    if n_sheep in FLOCK_RADIUS_BY_N:
        return FLOCK_RADIUS_BY_N[n_sheep]
    anchor = FLOCK_RADIUS_BY_N[RADIUS_ANCHOR_N]
    return anchor * math.sqrt(n_sheep / float(RADIUS_ANCHOR_N))


def write_draft(tmp_path: Path, **changes: Any) -> Path:
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump({**DRAFT, **changes}))
    return path


def load_draft(tmp_path: Path, **changes: Any) -> Protocol:
    return load_protocol(str(write_draft(tmp_path, **changes)), output=tmp_path / "out")


def physics_hash(protocol: Protocol) -> str:
    return protocol.physics_hash()


def ticks_for_drive_multiple(tmp_path: Path, multiple: float, n_sheep: FlockSize) -> int:
    """max_ticks for a compact cell under a drive-time deadline."""
    protocol = load_draft(
        tmp_path,
        methods={METHOD: {"time_limit_drive_multiple": multiple}},
        flock_sizes=[n_sheep],
    )
    group = Group(METHOD, "compact", n_sheep)
    return int(cell_config(protocol, Cell(group, N_DOGS), radius_for(n_sheep))["max_ticks"])


# --- loading -----------------------------------------------------------------


def test_extends_merges_child_over_parent(tmp_path: Path) -> None:
    parent = write_draft(tmp_path)
    child = tmp_path / "child.yaml"
    child.write_text(
        yaml.safe_dump({"extends": parent.name, "protocol_id": "c", "flock_sizes": [20]})
    )
    protocol = load_protocol(str(child), output=tmp_path / "out")
    assert protocol.protocol_id == "c"
    assert protocol.flock_sizes == (20,)


# --- physics hash ------------------------------------------------------------


def test_physics_hash_matches_only_when_trial_outcomes_match() -> None:
    """Resume gate: same trial physics -> same hash; a real physics change -> new hash.

    Strategy and sampling stay out of the hash so a campaign can raise seeds and still
    resume. Layouts and the largest D size every cell's field, so they are in. Extra flock
    sizes or intermediate D are not. Neutral success_fraction (strict 1.0) stays out so
    folders written before that setting remain resumable; a relaxed fraction is in.
    YAML 13 and 13.0 must hash alike so int/float spelling does not block resume.
    """
    base = physics_hash(BASE_PROTOCOL)
    top_d = max(BASE_PROTOCOL.shepherd_counts)

    assert physics_hash(protocol_with(ticks=3000, settings={"max_seeds": 400})) == base
    assert physics_hash(protocol_with(ticks=3000, settings={"refine_min_gap": 4})) == base
    assert (
        physics_hash(replace(BASE_PROTOCOL, flock_sizes=(*BASE_PROTOCOL.flock_sizes, 50))) == base
    )
    assert (
        physics_hash(replace(BASE_PROTOCOL, shepherd_counts=(*BASE_PROTOCOL.shepherd_counts, 3)))
        == base
    )

    assert (
        physics_hash(protocol_with(ticks=3000, settings={"drive_distance_multiple": 14.0})) != base
    )
    assert physics_hash(protocol_with(ticks=3000, params={"n_neighbors": 7})) != base
    assert physics_hash(replace(BASE_PROTOCOL, layouts=("compact", "wide"))) != base
    assert (
        physics_hash(
            replace(BASE_PROTOCOL, shepherd_counts=(*BASE_PROTOCOL.shepherd_counts, 2 * top_d))
        )
        != base
    )

    strict = protocol_with(ticks=3000)
    relaxed = protocol_with(ticks=3000, settings={"success_fraction": 0.99})
    assert "success_fraction" not in strict.physics()["settings"]
    assert relaxed.physics()["settings"]["success_fraction"] == 0.99
    assert physics_hash(strict) != physics_hash(relaxed)

    as_int = protocol_with(ticks=3000, settings={"drive_distance_multiple": 13})
    as_float = protocol_with(ticks=3000, settings={"drive_distance_multiple": 13.0})
    assert physics_hash(as_int) == physics_hash(as_float)

    # A graze-off protocol must resume into folders written before the switch existed.
    assert physics_hash(protocol_with(ticks=3000, params={"graze_repulsion": False})) == base
    assert physics_hash(protocol_with(ticks=3000, params={"graze_repulsion": True})) != base


@pytest.mark.parametrize("bad", ["false", 0])
def test_a_model_switch_must_be_a_real_boolean(tmp_path: Path, bad: object) -> None:
    """ "false" or 0 would read as on and escape the neutral filter of the hash."""
    with pytest.raises(ValueError, match="graze_repulsion"):
        load_draft(tmp_path, methods={METHOD: {"params": {"graze_repulsion": bad}}})


# --- drive-time deadlines ----------------------------------------------------


def test_time_limit_can_be_a_multiple_of_the_drive_time(tmp_path: Path) -> None:
    protocol = load_draft(tmp_path, methods={METHOD: {"time_limit_drive_multiple": 4}})
    assert protocol.methods[0].time_limit_ticks is None
    assert protocol.methods[0].time_limit_drive_multiple == 4.0

    for bad in (
        {"time_limit_drive_multiple": 0},
        {"time_limit_drive_multiple": 2, "time_limit_ticks": 9},
    ):
        with pytest.raises(ValueError):
            load_draft(tmp_path, methods={METHOD: bad})


def test_drive_multiple_scales_the_limit_with_the_drive_and_enters_the_hash(
    tmp_path: Path,
) -> None:
    config = config_for(n=50, d=N_DOGS, flock_radius=radius_for(50))
    drive = abs(config["goal_center"][0] - config["flock_center"][0])

    # Strombom: one length unit per second, so ticks == seconds == multiple x drive.
    assert ticks_for_drive_multiple(tmp_path, 4.0, 50) == math.ceil(4.0 * drive)
    assert ticks_for_drive_multiple(tmp_path, 8.0, 50) == pytest.approx(
        2 * ticks_for_drive_multiple(tmp_path, 4.0, 50), abs=1
    )
    assert ticks_for_drive_multiple(tmp_path, 4.0, 400) > ticks_for_drive_multiple(
        tmp_path, 4.0, 50
    )

    def hash_at(multiple: float) -> str:
        return physics_hash(
            load_draft(tmp_path, methods={METHOD: {"time_limit_drive_multiple": multiple}})
        )

    assert hash_at(4.0) != hash_at(8.0)


# --- shipped protocols -------------------------------------------------------


@pytest.mark.parametrize("path", sorted(PROTOCOLS_DIR.glob("*.yaml")), ids=lambda p: p.stem)
def test_shipped_protocol_builds_and_starts_every_group(path: Path) -> None:
    """Every group of every shipped protocol builds a valid config at its largest D and ticks."""
    protocol = load_protocol(path.stem)
    largest_d = max(protocol.shepherd_counts)
    for group in groups(protocol):
        config = cell_config(protocol, Cell(group, largest_d), radius_for(group.n_sheep))
        run_trial({**config, "max_ticks": SMOKE_TICKS}, protocol.settings["master_seed"])


@pytest.mark.parametrize("protocol_id", study_queue())
def test_stored_results_still_match_their_protocol(protocol_id: str) -> None:
    """A folder resumes only while its stored physics hash equals the protocol's hash now."""
    stored = read_provenance(results_folder(protocol_id) / "provenance.json")
    assert physics_hash(load_protocol(protocol_id)) == stored["physics_hash"]
