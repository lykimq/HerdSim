"""API router for instrument / preset discovery (legacy path /api/algorithms)."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from core.experimental_factors import (
    COMMUNICATION_MODES,
    FACTOR_GRID_KEYS,
    FAILURE_MODES,
    GOAL_MODES,
    MAX_FACTOR_GRID_CELLS,
    OBSERVATION_MODES,
)
from core.plugin_registry import dog_controller_registry, sheep_dynamics_registry
from core.presets import get_preset, list_presets

router = APIRouter()

_FACTOR_LABELS = {
    "n_sheep": "Sheep count",
    "n_shepherds": "Shepherd count",
    "sheep_model": "Sheep model",
    "dog_controller": "Dog controller",
    "scenario": "Scenario",
    "preset": "Settings source",
    "obs_mode": "Observation mode",
    "sensing_range": "Sensing range",
    "noise_sigma": "Observation noise",
    "observation_frequency": "Observation frequency",
    "communication": "Communication",
    "stubborn_fraction": "Stubborn fraction",
    "stubborn_response_scale": "Stubborn response scale",
    "cohesion_scale": "Cohesion scale",
    "failure_mode": "Failure mode",
    "failure_tick": "Failure tick",
    "speed_scale": "Shepherd speed scale",
    "goal_mode": "Goal mode",
    "initial_layout": "Initial layout",
    "initial_spread": "Initial spread",
    "noise_strength": "Process noise",
    "v_max": "Robot v_max",
    "a_max": "Robot a_max",
    "omega_max": "Robot omega_max",
    "latency": "Control latency",
}

_FACTOR_DESCRIPTIONS = {
    "obs_mode": "What each shepherd observes each tick.",
    "sensing_range": "Local sensing radius when observation is limited.",
    "noise_sigma": "Noise on bearing observations.",
    "communication": "Inter-shepherd information sharing.",
    "stubborn_fraction": "Fraction of sheep with reduced shepherd response.",
    "cohesion_scale": "Scale on sheep flocking cohesion forces.",
    "failure_mode": "How shepherds fail after failure_tick.",
    "failure_tick": "Tick when failure_mode activates (-1 = never).",
    "speed_scale": "Shared multiplier on shepherd speed.",
    "goal_mode": "Static goal or moving goal.",
    "sheep_model": "Sheep dynamics plugin.",
    "dog_controller": "Shepherd controller plugin.",
}

_ENUM_LABELS = {
    "global": "Global state",
    "local_positions": "Local positions",
    "bearing_only": "Bearing only",
    "noisy_bearing": "Noisy bearings",
    "intermittent": "Intermittent",
    "none": "None",
    "neighbour_broadcast": "Neighbour broadcast",
    "global_shared": "Global shared",
    "inactive_after_tick": "Inactive after tick",
    "reduced_speed_after_tick": "Reduced speed after tick",
    "blind_after_tick": "Blind after tick",
    "static": "Static",
    "moving": "Moving",
}


def _enum_items(values: tuple[str, ...] | list[str]) -> list[dict]:
    return [{"id": value, "label": _ENUM_LABELS.get(value, value)} for value in values]


def _factor_catalog() -> dict:
    return {
        "max_grid_cells": MAX_FACTOR_GRID_CELLS,
        "grid_keys": sorted(FACTOR_GRID_KEYS),
        "enums": {
            "obs_mode": _enum_items(OBSERVATION_MODES),
            "communication": _enum_items(COMMUNICATION_MODES),
            "failure_mode": _enum_items(FAILURE_MODES),
            "goal_mode": _enum_items(GOAL_MODES),
        },
        "fields": [
            {
                "key": key,
                "label": _FACTOR_LABELS.get(key, key),
                "description": _FACTOR_DESCRIPTIONS.get(key, ""),
                "kind": (
                    "enum"
                    if key in {"obs_mode", "communication", "failure_mode", "goal_mode"}
                    else "string"
                    if key in {"sheep_model", "dog_controller", "scenario", "preset"}
                    else "number"
                ),
            }
            for key in sorted(FACTOR_GRID_KEYS)
        ],
        "dependencies": {
            "sensing_range": {"when": {"obs_mode": ["local_positions", "bearing_only", "noisy_bearing", "intermittent"]}},
            "noise_sigma": {"when": {"obs_mode": ["noisy_bearing"]}},
            "observation_frequency": {"when": {"obs_mode": ["intermittent"]}},
            "failure_tick": {
                "when": {
                    "failure_mode": [
                        "inactive_after_tick",
                        "reduced_speed_after_tick",
                        "blind_after_tick",
                    ]
                }
            },
            "goal_velocity": {"when": {"goal_mode": ["moving"]}},
        },
    }

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
    """List orthogonal sheep models, dog controllers, and factor metadata."""
    return {
        "sheep_models": sheep_dynamics_registry.list_all(),
        "dog_controllers": dog_controller_registry.list_all(),
        "factors": _factor_catalog(),
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
