"""Preset registry facade used by scripts and docs sync.

Named instruments replace the old BaseAlgorithm registry.
"""

from __future__ import annotations

from core.presets import PRESETS, get_preset, list_presets


class AlgorithmRegistry:
    """Compatibility facade exposing preset instruments."""

    def get(self, algorithm_id: str):
        return _PresetView(get_preset(algorithm_id))

    def list_all(self) -> list[dict]:
        return list_presets()

    def names(self) -> list[str]:
        return list(PRESETS.keys())


class _PresetView:
    def __init__(self, preset: dict):
        self.id = preset["id"]
        self.name = preset["name"]
        self.default_config = dict(preset["default_config"])
        self.sheep_model = preset["sheep_model"]
        self.dog_controller = preset["dog_controller"]


algorithm_registry = AlgorithmRegistry()
