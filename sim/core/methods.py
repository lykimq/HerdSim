"""Named methods as factor bundles (sheep_model x dog_controller).

Catalog is limited to methods used by scaling campaigns (plus base Strombom).
"""

from __future__ import annotations

from typing import Any

from methods.kubo.config import KUBO_DEFAULTS
from methods.strombom.config import STROMBOM_DEFAULTS


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
    "kubo": _bundle(
        method_id="kubo",
        name="Kubo 2022",
        sheep_model="kubo",
        dog_controller="kubo_forces",
        params=KUBO_DEFAULTS.copy(),
        description="Kubo force-based sheep and dogs.",
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


def get_method(method_id: str) -> dict[str, Any]:
    if method_id not in METHODS:
        raise KeyError(f"Unknown method '{method_id}'. Available: {list(METHODS.keys())}")
    return METHODS[method_id]
