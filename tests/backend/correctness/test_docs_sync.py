"""Ensure registered algorithms have research docs and info.json."""

from __future__ import annotations

from pathlib import Path

from algorithms.registry import algorithm_registry

ROOT = Path(__file__).resolve().parents[3]
ALG_DOCS = ROOT / "docs" / "research" / "algorithms"
# Map algorithm id -> docs page stem (when names differ)
DOC_BY_ID = {
    "strombom": "strombom_2014",
    "strombom_noise": "strombom_noise",
    "strombom_multi": "strombom_multi",
    "kubo": "kubo_2022",
    "flocking_dog": "flocking_dog_2024",
    "v_formation": "v_formation",
    "heterogeneous": "heterogeneous",
    "obstacle_aware": "obstacle_aware",
    "fat": "fat",
    "communication_free": "communication_free",
    "adaptive": "adaptive",
}


def test_each_registered_algorithm_has_info_and_docs():
    for alg_id in algorithm_registry.names():
        info = ROOT / "algorithms" / alg_id / "info.json"
        assert info.is_file(), f"missing info.json for {alg_id}"
        stem = DOC_BY_ID.get(alg_id, alg_id)
        page = ALG_DOCS / f"{stem}.md"
        assert page.is_file(), f"missing docs page {page} for {alg_id}"
