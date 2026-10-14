"""Records per-tick metric values into a Pandas DataFrame for export."""

from __future__ import annotations

from typing import Any

import pandas as pd
from plugins.metrics.base import BaseMetric

from core.simulation_state import SimulationState


class HistoryRecorder:
    """Accumulates metric snapshots per tick and produces a DataFrame."""

    def __init__(self, metrics: list[BaseMetric]):
        self._metrics = metrics
        self._records: list[dict[str, Any]] = []

    def record(self, state: SimulationState) -> None:
        """Compute all metrics for the current state and store the snapshot."""
        row: dict[str, Any] = {"tick": state.tick}
        for metric in self._metrics:
            row[metric.id] = metric.compute(state)
        self._records.append(row)

    def to_dataframe(self) -> pd.DataFrame:
        """Return the full history as a DataFrame. Columns: tick + metric ids."""
        if not self._records:
            cols = ["tick"] + [m.id for m in self._metrics]
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(self._records)

    def reset(self) -> None:
        """Clear recorded history and reset stateful metrics."""
        self._records.clear()
        for metric in self._metrics:
            reset = getattr(metric, "reset", None)
            if callable(reset):
                reset()
