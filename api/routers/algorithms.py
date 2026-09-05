"""API router for algorithm discovery and metadata."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from algorithms.registry import algorithm_registry

router = APIRouter()

_ALGORITHMS_ROOT = Path(__file__).resolve().parents[2] / "algorithms"


def _load_info(algorithm_id: str) -> dict:
    info_path = _ALGORITHMS_ROOT / algorithm_id / "info.json"
    if not info_path.is_file():
        return {}
    with info_path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _with_herder_meta(entry: dict) -> dict:
    """Attach display metadata for dog vs human shepherd sprites."""
    info = _load_info(entry["id"])
    herder_kind = info.get("herder_kind", "dog")
    herder_label = info.get(
        "herder_label",
        "Dog" if herder_kind == "dog" else "Shepherd",
    )
    return {
        **entry,
        "herder_kind": herder_kind,
        "herder_label": herder_label,
        "info": info or None,
    }


@router.get("")
@router.get("/")
def list_algorithms():
    """List all available registered algorithms."""
    return [_with_herder_meta(item) for item in algorithm_registry.list_all()]


@router.get("/{algorithm_id}")
def get_algorithm(algorithm_id: str):
    """Get metadata for a specific algorithm, including info.json when present."""
    try:
        algorithm = algorithm_registry.get(algorithm_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    payload = {
        "id": algorithm.id,
        "name": algorithm.name,
        "default_config": algorithm.default_config,
    }
    return _with_herder_meta(payload)
