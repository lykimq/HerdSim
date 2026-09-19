"""Named instruments as factor bundles (sheep_model x dog_controller)."""

from __future__ import annotations

from typing import Any

from instruments.flocking_dog.config import FLOCKING_DOG_DEFAULTS
from instruments.kubo.config import KUBO_DEFAULTS
from instruments.obstacle_aware.config import OBSTACLE_AWARE_DEFAULTS
from instruments.strombom.config import STROMBOM_DEFAULTS
from instruments.v_formation.config import V_FORMATION_DEFAULTS


def _bundle(
    *,
    instrument_id: str,
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
        "id": instrument_id,
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


INSTRUMENTS: dict[str, dict[str, Any]] = {
    "strombom": _bundle(
        instrument_id="strombom",
        name="Strombom 2014",
        sheep_model="strombom",
        dog_controller="collect_drive",
        params=STROMBOM_DEFAULTS.copy(),
        description="Strombom Collect/Drive with Strombom sheep.",
    ),
    "strombom_multi": _bundle(
        instrument_id="strombom_multi",
        name="Strombom Multi-Dog",
        sheep_model="strombom",
        dog_controller="collect_drive_multi",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 3},
        description="Multi-dog Collect/Drive assignment.",
    ),
    "strombom_noise": _bundle(
        instrument_id="strombom_noise",
        name="Strombom Noise",
        sheep_model="strombom",
        dog_controller="collect_drive",
        params={**STROMBOM_DEFAULTS, "noise_strength": 0.9, "inertia": 0.3},
        noise_strength=0.9,
        description="Strombom with elevated process noise.",
    ),
    "heterogeneous": _bundle(
        instrument_id="heterogeneous",
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
        instrument_id="kubo",
        name="Kubo 2022",
        sheep_model="kubo",
        dog_controller="kubo_forces",
        params=KUBO_DEFAULTS.copy(),
        description="Kubo force-based sheep and dogs.",
    ),
    "flocking_dog": _bundle(
        instrument_id="flocking_dog",
        name="Flocking Dog 2024",
        sheep_model="jadhav",
        dog_controller="collect_drive",
        params=FLOCKING_DOG_DEFAULTS.copy(),
        description="Jadhav sheep with Collect/Drive dogs.",
    ),
    "v_formation": _bundle(
        instrument_id="v_formation",
        name="V-Formation",
        sheep_model="strombom",
        dog_controller="v_formation",
        params=V_FORMATION_DEFAULTS.copy(),
        description="V-arc multi-dog drive.",
    ),
    "obstacle_aware": _bundle(
        instrument_id="obstacle_aware",
        name="Obstacle-Aware",
        sheep_model="strombom",
        dog_controller="obstacle_aware_drive",
        params=OBSTACLE_AWARE_DEFAULTS.copy(),
        description="Obstacle-deflected drive targets.",
    ),
    "fat": _bundle(
        instrument_id="fat",
        name="FAT",
        sheep_model="strombom",
        dog_controller="fat",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 2},
        description="Farthest-agent targeting under local observations.",
    ),
    "communication_free": _bundle(
        instrument_id="communication_free",
        name="Communication-Free",
        sheep_model="strombom",
        dog_controller="communication_free",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 3},
        description="Independent local Collect/Drive per dog.",
    ),
    "adaptive": _bundle(
        instrument_id="adaptive",
        name="Adaptive",
        sheep_model="strombom",
        dog_controller="adaptive",
        params={**STROMBOM_DEFAULTS, "n_shepherds": 2, "lead_enabled": True},
        description="Context-aware collect/drive/recover/lead.",
    ),
}


def list_instruments() -> list[dict[str, Any]]:
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "description": p.get("description", ""),
            "sheep_model": p["sheep_model"],
            "dog_controller": p["dog_controller"],
            "default_config": dict(p["default_config"]),
        }
        for p in INSTRUMENTS.values()
    ]


def find_instrument_for_models(sheep_model: str, dog_controller: str) -> str | None:
    """Return a named instrument id matching the model pair, if any.

    When several instruments share the same pair, prefer id == sheep_model
    (canonical package), otherwise the first id in sorted order.
    """
    matches = [
        p
        for p in INSTRUMENTS.values()
        if p["sheep_model"] == sheep_model and p["dog_controller"] == dog_controller
    ]
    if not matches:
        return None
    for instrument in matches:
        if instrument["id"] == sheep_model:
            return instrument["id"]
    return sorted(matches, key=lambda p: p["id"])[0]["id"]


def get_instrument(instrument_id: str) -> dict[str, Any]:
    if instrument_id not in INSTRUMENTS:
        raise KeyError(
            f"Unknown instrument '{instrument_id}'. Available: {list(INSTRUMENTS.keys())}"
        )
    return INSTRUMENTS[instrument_id]
