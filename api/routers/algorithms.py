"""API router for instrument / preset discovery (legacy path /api/algorithms)."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from core.plugin_registry import dog_controller_registry, sheep_dynamics_registry
from core.presets import get_preset, list_presets

router = APIRouter()

_ALGORITHMS_ROOT = Path(__file__).resolve().parents[2] / "algorithms"
_INFO_FALLBACK = {
    "strombom": {"herder_kind": "human", "herder_label": "Shepherd"},
    "strombom_multi": {"herder_kind": "human", "herder_label": "Shepherd"},
    "strombom_noise": {"herder_kind": "human", "herder_label": "Shepherd"},
    "heterogeneous": {"herder_kind": "human", "herder_label": "Shepherd"},
    "v_formation": {"herder_kind": "dog", "herder_label": "Dog"},
    "obstacle_aware": {"herder_kind": "dog", "herder_label": "Dog"},
    "kubo": {"herder_kind": "dog", "herder_label": "Dog"},
    "flocking_dog": {"herder_kind": "dog", "herder_label": "Dog"},
    "fat": {"herder_kind": "dog", "herder_label": "Dog"},
    "communication_free": {"herder_kind": "dog", "herder_label": "Dog"},
    "adaptive": {"herder_kind": "dog", "herder_label": "Dog"},
}


def _load_info(preset_id: str) -> dict:
    info_path = _ALGORITHMS_ROOT / preset_id / "info.json"
    if info_path.is_file():
        with info_path.open(encoding="utf-8") as fh:
            return json.load(fh)
    return dict(_INFO_FALLBACK.get(preset_id, {"herder_kind": "dog"}))


def _with_herder_meta(entry: dict) -> dict:
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
    """List named instrument presets (sheep_model x dog_controller bundles)."""
    return [_with_herder_meta(item) for item in list_presets()]


@router.get("/meta/models")
def list_models():
    """List orthogonal sheep models and dog controllers."""
    return {
        "sheep_models": sheep_dynamics_registry.list_all(),
        "dog_controllers": dog_controller_registry.list_all(),
    }


@router.get("/{algorithm_id}")
def get_algorithm(algorithm_id: str):
    try:
        preset = get_preset(algorithm_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    payload = {
        "id": preset["id"],
        "name": preset["name"],
        "default_config": dict(preset["default_config"]),
        "sheep_model": preset["sheep_model"],
        "dog_controller": preset["dog_controller"],
        "description": preset.get("description", ""),
    }
    return _with_herder_meta(payload)
