"""API router for algorithm discovery and metadata."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from algorithms.registry import algorithm_registry

router = APIRouter()

_ALGORITHMS_ROOT = Path(__file__).resolve().parents[2] / "algorithms"


@router.get("")
@router.get("/")
def list_algorithms():
    """List all available registered algorithms."""
    return algorithm_registry.list_all()


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

    info_path = _ALGORITHMS_ROOT / algorithm_id / "info.json"
    if info_path.is_file():
        with info_path.open(encoding="utf-8") as fh:
            payload["info"] = json.load(fh)

    return payload
