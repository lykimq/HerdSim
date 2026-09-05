"""Records per-tick metric values into a Pandas DataFrame for export."""

from __future__ import annotations

from typing import Any

import pandas as pd

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class HistoryRecorder:
    """Accumulates metric snapshots per tick and produces a DataFrame."""

    def __init__(self, metrics: list[BaseMetric]):
        self._metrics = metrics
        self._records: list[dict] = []

    def record(self, state: SimulationState) -> dict[str, float]:
        """Compute all metrics for the current state and store the snapshot.

        Returns the metric values dict for immediate use (e.g. WebSocket frame).
        """
        row: dict[str, Any] = {"tick": state.tick}
        for metric in self._metrics:
            row[metric.id] = metric.compute(state)
        self._records.append(row)
        return {k: v for k, v in row.items() if k != "tick"}

    def latest(self) -> dict[str, float]:
        """Return the most recent metric snapshot without the tick column."""
        if not self._records:
            return {}
        return {k: v for k, v in self._records[-1].items() if k != "tick"}

    def to_dataframe(self) -> pd.DataFrame:
        """Return the full history as a DataFrame. Columns: tick + metric ids."""
        if not self._records:
            cols = ["tick"] + [m.id for m in self._metrics]
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(self._records)

    def get_summary(self) -> dict[str, Any]:
        """Compact summary used by websocket termination and exports."""
        if not self._records:
            return {"ticks": 0, "final_tick": 0, "final_metrics": {}}
        final = self._records[-1]
        return {
            "ticks": len(self._records),
            "final_tick": final.get("tick", 0),
            "final_metrics": {k: v for k, v in final.items() if k != "tick"},
        }

    def reset(self) -> None:
        """Clear recorded history and reset stateful metrics."""
        self._records.clear()
        for metric in self._metrics:
            reset = getattr(metric, "reset", None)
            if callable(reset):
                reset()
