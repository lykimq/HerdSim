"""Pressure on the flock in a replayed trial: how long the sheep spend near a dog.

The trial rows keep summaries of the tick metrics, and none of them says how close the dogs
come to the sheep, so these measures are taken while a stored trial is replayed
(services/replay.py, cli/diagnostics/pressure_replay.py).

Two shares are recorded per tick: the share of sheep closer than the reaction radius to some
dog (for Strombom sheep, the sheep in flight: they react to a dog strictly closer than r_s),
and the share closer than ``close`` (the Strombom dog's stop distance, 3 r_a, by default), the
distance at which a dog is as close to a sheep as the dog rule lets it get. Summed over the
ticks and multiplied by dt they give the seconds a sheep spends in each, on average.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def near_shares(
    sheep: np.ndarray, dogs: np.ndarray, reach: float, close: float
) -> tuple[float, float]:
    """(share of sheep strictly closer than ``reach`` to some dog, share closer than ``close``)."""
    if len(dogs) == 0 or len(sheep) == 0:
        return 0.0, 0.0
    nearest = cdist(sheep, dogs).min(axis=1)
    return float(np.mean(nearest < reach)), float(np.mean(nearest < close))


@dataclass
class Pressure:
    """The two shares of every tick of one trial, and their summary."""

    reach: float
    close: float
    flight: list[float] = field(default_factory=list)
    near: list[float] = field(default_factory=list)

    def add(self, sheep: np.ndarray, dogs: np.ndarray) -> None:
        a, b = near_shares(sheep, dogs, self.reach, self.close)
        self.flight.append(a)
        self.near.append(b)

    def summary(self, dt: float) -> dict[str, float]:
        return {
            "flight_seconds_per_sheep": float(np.sum(self.flight)) * dt,
            "close_seconds_per_sheep": float(np.sum(self.near)) * dt,
            "mean_flight_share": float(np.mean(self.flight)) if self.flight else 0.0,
            "peak_flight_share": float(np.max(self.flight)) if self.flight else 0.0,
        }


def pressure_table(rows: pd.DataFrame) -> pd.DataFrame:
    """Per cell: success and the medians of the pressure measures over its successful seeds."""
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
