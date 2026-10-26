"""Flock pressure metrics evaluated during trial replays.

Computes how long sheep spend in proximity to herders during a simulation:
- Flight share: Fraction of sheep within reaction distance (r_s) to any dog.
- Close proximity share: Fraction of sheep within dog stopping distance (e.g. 3 * r_a).
Integrated over simulation ticks, these yield the average flight and close-contact
seconds experienced per sheep.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def near_shares(
    sheep: np.ndarray, dogs: np.ndarray, reach: float, close: float
) -> tuple[float, float]:
    """Computes the fraction of sheep within ``reach`` and within ``close`` distance of any dog."""
    if len(dogs) == 0 or len(sheep) == 0:
        return 0.0, 0.0
    nearest = cdist(sheep, dogs).min(axis=1)
    return float(np.mean(nearest < reach)), float(np.mean(nearest < close))


@dataclass
class Pressure:
    """Accumulates per-tick flock proximity shares for a single trial."""

    reach: float
    close: float
    flight: list[float] = field(default_factory=list)
    near: list[float] = field(default_factory=list)

    def add(self, sheep: np.ndarray, dogs: np.ndarray) -> None:
        """Records sheep proximity shares for the current tick."""
        a, b = near_shares(sheep, dogs, self.reach, self.close)
        self.flight.append(a)
        self.near.append(b)

    def summary(self, dt: float) -> dict[str, float]:
        """Calculates integrated flight seconds and mean/peak proximity shares."""
        return {
            "flight_seconds_per_sheep": float(np.sum(self.flight)) * dt,
            "close_seconds_per_sheep": float(np.sum(self.near)) * dt,
            "mean_flight_share": float(np.mean(self.flight)) if self.flight else 0.0,
            "peak_flight_share": float(np.max(self.flight)) if self.flight else 0.0,
        }


def pressure_table(rows: pd.DataFrame) -> pd.DataFrame:
    """Aggregates median pressure metrics across successful seeds for each (layout, N, D) cell."""
    out = []
    for _, part in rows.groupby(["layout", "n", "d"], sort=True):
        first = part.iloc[0]
        done = part[part["success"]]
        out.append(
            {
                "layout": first["layout"],
                "n": int(first["n"]),
                "d": int(first["d"]),
                "role": part["role"].iloc[0],
                "seeds": len(part),
                "success": round(float(part["success"].mean()), 2),
                "finish_s": done["finish_seconds"].median() if len(done) else float("nan"),
                "flight_s_per_sheep": done["flight_seconds_per_sheep"].median()
                if len(done)
                else float("nan"),
                "close_s_per_sheep": done["close_seconds_per_sheep"].median()
                if len(done)
                else float("nan"),
                "mean_flight_share": done["mean_flight_share"].median()
                if len(done)
                else float("nan"),
            }
        )
    return pd.DataFrame(out)
