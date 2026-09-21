"""Named methods as factor bundles (sheep_model x dog_controller)."""

from __future__ import annotations

from typing import Any

from methods.flocking_dog.config import FLOCKING_DOG_DEFAULTS
from methods.kubo.config import KUBO_DEFAULTS
from methods.obstacle_aware.config import OBSTACLE_AWARE_DEFAULTS
from methods.strombom.config import STROMBOM_DEFAULTS
from methods.v_formation.config import V_FORMATION_DEFAULTS


def _bundle(
    *,
    method_id: str,
    name: str,
    sheep_model: str,
    dog_controller: str,
    params: dict[str, Any],
    description: str = "",
    stubborn_fraction: float = 0.0,
    noise_strength: float | None = None,
) -> dict[str, Any]:
    flock_extra: dict[str, Any] = {"stubborn_fraction": stubborn_fraction}
    if noise_strength is not None:
        flock_extra["noise_strength"] = noise_strength
    return {
        "id": method_id,
        "name": name,
        "description": description,
        "sheep_model": sheep_model,
        "dog_controller": dog_controller,
        "default_config": dict(params),
        "factors": {
            "model": {
                "sheep_model": sheep_model,
                "dog_controller": dog_controller,
                "preset": "paper",
            },
            "flock": flock_extra,
            "params": dict(params),
        },
    }


METHODS: dict[str, dict[str, Any]] = {
    "strombom": _bundle(
        method_id="strombom",
        name="Strombom 2014",
        sheep_model="strombom",
        dog_controller="collect_drive",
        params=STROMBOM_DEFAULTS.copy(),
        description="Strombom Collect/Drive with Strombom sheep.",
    ),
    "strombom_multi": _bundle(
        method_id="strombom_multi",
        name="Strombom Multi-Dog",
        sheep_model="strombom",
        dog_controller="collect_drive_multi",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 3},
        description="Multi-dog Collect/Drive assignment.",
    ),
    "strombom_noise": _bundle(
        method_id="strombom_noise",
        name="Strombom Noise",
        sheep_model="strombom",
        dog_controller="collect_drive",
        params={**STROMBOM_DEFAULTS, "noise_strength": 0.9, "inertia": 0.3},
        noise_strength=0.9,
        description="Strombom with elevated process noise.",
    ),
    "heterogeneous": _bundle(
        method_id="heterogeneous",
        name="Heterogeneous Sheep",
        sheep_model="strombom",
        dog_controller="collect_drive",
        params={
            **STROMBOM_DEFAULTS,
            "stubborn_fraction": 0.2,
            "stubborn_rs_scale": 0.25,
        },
        stubborn_fraction=0.2,
        description="Strombom with stubborn sheep fraction factor.",
    ),
    "kubo": _bundle(
        method_id="kubo",
        name="Kubo 2022",
        sheep_model="kubo",
        dog_controller="kubo_forces",
        params=KUBO_DEFAULTS.copy(),
        description="Kubo force-based sheep and dogs.",
    ),
    "flocking_dog": _bundle(
        method_id="flocking_dog",
        name="Flocking Dog 2024",
        sheep_model="jadhav",
        dog_controller="collect_drive",
        params=FLOCKING_DOG_DEFAULTS.copy(),
        description="Jadhav sheep with Collect/Drive dogs.",
    ),
    "v_formation": _bundle(
        method_id="v_formation",
        name="V-Formation",
        sheep_model="strombom",
        dog_controller="v_formation",
        params=V_FORMATION_DEFAULTS.copy(),
        description="V-arc multi-dog drive.",
    ),
    "obstacle_aware": _bundle(
        method_id="obstacle_aware",
        name="Obstacle-Aware",
        sheep_model="strombom",
        dog_controller="obstacle_aware_drive",
        params=OBSTACLE_AWARE_DEFAULTS.copy(),
        description="Obstacle-deflected drive targets.",
    ),
    "fat": _bundle(
        method_id="fat",
        name="FAT",
        sheep_model="strombom",
        dog_controller="fat",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 2},
        description="Farthest-agent targeting under local observations.",
    ),
    "communication_free": _bundle(
        method_id="communication_free",
        name="Communication-Free",
        sheep_model="strombom",
        dog_controller="communication_free",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 3},
        description="Independent local Collect/Drive per dog.",
    ),
    "adaptive": _bundle(
        method_id="adaptive",
        name="Adaptive",
        sheep_model="strombom",
        dog_controller="adaptive",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 2, "lead_enabled": True},
        description="Context-aware collect/drive/recover/lead.",
    ),
}


def list_methods() -> list[dict[str, Any]]:
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "description": p.get("description", ""),
            "sheep_model": p["sheep_model"],
            "dog_controller": p["dog_controller"],
            "default_config": dict(p["default_config"]),
        }
        for p in METHODS.values()
    ]


def find_method_for_models(sheep_model: str, dog_controller: str) -> str | None:
    """Return a named method id matching the model pair, if any.

    When several methods share the same pair, prefer id == sheep_model
    (canonical package), otherwise the first id in sorted order.
    """
    matches = [
        p
        for p in METHODS.values()
        if p["sheep_model"] == sheep_model and p["dog_controller"] == dog_controller
    ]
    if not matches:
        return None
    for method in matches:
        if method["id"] == sheep_model:
            return method["id"]
    return sorted(matches, key=lambda p: p["id"])[0]["id"]


def get_method(method_id: str) -> dict[str, Any]:
    if method_id not in METHODS:
        raise KeyError(
            f"Unknown method '{method_id}'. Available: {list(METHODS.keys())}"
        )
    return METHODS[method_id]
