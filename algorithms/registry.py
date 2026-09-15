"""Instrument registry facade used by scripts and docs sync.

Named instruments live in ``core.presets``. This module keeps a small
discovery API for callers that previously used ``algorithm_registry``.
Prefer ``core.presets`` / ``instrument`` in new code.
"""

from __future__ import annotations

from core.presets import PRESETS, get_preset, list_presets


class InstrumentRegistry:
    """Facade exposing preset instruments by id."""

    def get(self, instrument_id: str):
        return _PresetView(get_preset(instrument_id))

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


instrument_registry = InstrumentRegistry()
# Legacy alias for older imports / tests.
AlgorithmRegistry = InstrumentRegistry
algorithm_registry = instrument_registry
