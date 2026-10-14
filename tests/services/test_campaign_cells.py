"""Correctness: protocol YAMLs expand to the frozen cell grids and resume keys."""

from __future__ import annotations

from services.layout import load_run_protocol
from services.runner import _cell_key, expand_scaling_grid


def _cells(protocol_id: str, **kw):
    _, spec, _, effective = load_run_protocol(protocol_id)
    return spec, expand_scaling_grid(
        effective,
        methods=spec.get("methods") or ([spec["method"]] if "method" in spec else None),
        layouts=spec.get("layouts"),
        n_values=spec.get("flock_sizes"),
        d_values=spec.get("shepherd_counts"),
        n_seeds=spec.get("seeds"),
        **kw,
    )


def test_size_scout_grid_and_resume_keys():
    _, cells = _cells("phase1_scout")
    assert len(cells) == 10 * 10 * 30
    assert _cell_key(cells[0]) == "N5_D1_Lcompact_S2026_Mstrombom_multi"
    assert {c.seed for c in cells} == set(range(2026, 2056))


def test_factor_sweep_sets_information_axes():
    spec, cells = _cells(
        "phase5_range_scout",
        obs_modes=["local_positions"],
        sensing_ranges=[32.5, 65.0, 97.5, 130.0],
    )
    assert spec["runner"] == "factor"
    assert len(cells) == 4 * 2 * 6 * 30
    assert _cell_key(cells[0]).endswith("_Olocal_positions_R32.5")
