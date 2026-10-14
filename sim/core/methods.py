"""Named methods: a sheep_model x dog_controller pair plus default parameters.

Catalog is limited to methods run by scaling campaigns.
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
) -> dict[str, Any]:
    return {
        "id": method_id,
        "name": name,
        "description": description,
        "sheep_model": sheep_model,
        "dog_controller": dog_controller,
        "default_config": dict(params),
    }


METHODS: dict[str, dict[str, Any]] = {
    "strombom_multi": _bundle(
        method_id="strombom_multi",
        name="Strombom Multi-Dog",
        sheep_model="strombom",
        dog_controller="collect_drive_multi",
        params=STROMBOM_DEFAULTS,
        description="Multi-dog Collect/Drive assignment.",
    ),
    "kubo": _bundle(
        method_id="kubo",
        name="Kubo 2022",
        sheep_model="kubo",
        dog_controller="kubo_forces",
        params=KUBO_DEFAULTS,
        description="Kubo force-based sheep and dogs.",
    ),
    "fat": _bundle(
        method_id="fat",
        name="FAT",
        sheep_model="strombom",
        dog_controller="fat",
        params=STROMBOM_DEFAULTS,
        description="Farthest-agent targeting under local observations.",
    ),
}


def get_method(method_id: str) -> dict[str, Any]:
    if method_id not in METHODS:
        raise KeyError(f"Unknown method '{method_id}'. Available: {list(METHODS.keys())}")
    return METHODS[method_id]
