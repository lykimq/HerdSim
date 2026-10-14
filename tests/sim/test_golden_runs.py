"""Regression: short real trials must reproduce frozen outcomes exactly.

Any change to sheep / dog dynamics, observation, scenarios, config resolution,
or metrics shows up here. Values were recorded from the campaign engine; only
update them on an intended behaviour change (and note it with the protocol).
"""

from __future__ import annotations

import pytest
import yaml

from services.layout import CANONICAL_PROTOCOL, PROTOCOLS_DIR
from services.runner import ScalingCell, _run_cell, scaling_world_overrides

CANONICAL = yaml.safe_load(CANONICAL_PROTOCOL.read_text())
PHASE8 = {**CANONICAL, **yaml.safe_load((PROTOCOLS_DIR / "phase8_size_scout.yaml").read_text())}


def _cell(n: int, d: int, *, proto=CANONICAL, ticks: int = 400, **kw) -> ScalingCell:
    return ScalingCell(
        n_sheep=n,
        n_shepherds=d,
        seed=2026 + d,
        max_ticks=ticks,
        scenario=str(proto["task"]),
        **scaling_world_overrides(proto, n),
        **kw,
    )


# (cell, success, total_ticks, mean_cohesion, final_gcm_goal, shepherd_path, mean_fragmentation)
GOLDEN = [
    (
        _cell(20, 3),
        True,
        183,
        3.8348651491877095,
        3.671246297606474,
        498.8258677839863,
        0.9570652173913043,
    ),
    (
        _cell(30, 2, initial_layout="wide"),
        False,
        400,
        59.860693227810394,
        96.29737191768065,
        1176.0000000000002,
        0.21679135494596843,
    ),
    (
        _cell(20, 2, method="kubo"),
        False,
        400,
        10.656476803388827,
        62.35571527523866,
        123.3761380607948,
        0.7384039900249374,
    ),
    (
        _cell(20, 2, method="fat"),
        False,
        400,
        3.9261566144334217,
        131.60847796370726,
        616.5,
        0.9734413965087281,
    ),
    (
        _cell(20, 2, obs_mode="bearing_only"),
        False,
        400,
        3.836214263024984,
        128.6381194036311,
        736.4999999999999,
        0.9744389027431422,
    ),
    (
        _cell(20, 3, obs_mode="local_positions", sensing_range=60.0, communication="global_shared"),
        True,
        179,
        3.8676160505882007,
        4.201639040435136,
        496.97780007606013,
        0.9533333333333335,
    ),
    (
        _cell(20, 2, proto=PHASE8, ticks=1500),
        False,
        1500,
        3.627523125294327,
        88.88412676913025,
        2222.290859250705,
        0.9907061958694205,
    ),
]


@pytest.mark.parametrize(
    "cell, success, ticks, cohesion, gcm_goal, path, fragmentation",
    GOLDEN,
    ids=["multi", "multi_wide", "kubo", "fat", "bearing_only", "global_shared", "hold_gate"],
)
def test_trial_matches_golden(cell, success, ticks, cohesion, gcm_goal, path, fragmentation):
    row = _run_cell(cell)["row"]
    assert (row["success"], row["total_ticks"]) == (success, ticks)
    assert row["mean_cohesion"] == pytest.approx(cohesion, rel=1e-9)
    assert row["final_gcm_goal"] == pytest.approx(gcm_goal, rel=1e-9)
    assert row["shepherd_path"] == pytest.approx(path, rel=1e-9)
    assert row["mean_fragmentation"] == pytest.approx(fragmentation, rel=1e-9)
