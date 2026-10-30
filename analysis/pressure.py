"""Pressure on the flock in a replayed trial: how long the sheep spend near a dog.

    uv run cli/diagnostics/pressure_replay.py dmin_f99_m6 --out <csv>

The trial rows keep summaries of the tick metrics, and none of them says how close the dogs come
to the sheep, so these measures are taken while a stored trial is replayed (services/replay.py).
Two shares are recorded per tick:

- the share of sheep closer than the reaction radius to some dog, for Strombom sheep the sheep
  in flight
- the share closer than ``close``, by default the Strombom dog's stop distance 3 r_a, as close
  as the dog rule lets a dog get

Summed over the ticks and multiplied by dt, they give the seconds a sheep spends in each, on
average; ``pressure_table`` summarises them per cell.
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


def _median_of_done(done: pd.DataFrame, column: str) -> float:
    return float(done[column].median()) if len(done) else float("nan")


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
                "role": first["role"],
                "seeds": len(part),
                "success": round(float(part["success"].mean()), 2),
                "finish_s": _median_of_done(done, "finish_seconds"),
                "flight_s_per_sheep": _median_of_done(done, "flight_seconds_per_sheep"),
                "close_s_per_sheep": _median_of_done(done, "close_seconds_per_sheep"),
                "mean_flight_share": _median_of_done(done, "mean_flight_share"),
            }
        )
    return pd.DataFrame(out)


def cells_to_replay(curve: pd.Series, tested: list[int]) -> dict[int, str]:
    """D -> role, for D = 1, D_min, D_sat and the smallest tested D at or above 2 D_sat."""
    roles: dict[int, list[str]] = {1: ["1"]}
    if pd.notna(curve["d_min"]):
        roles.setdefault(int(curve["d_min"]), []).append("D_min")
    if pd.notna(curve["d_sat"]):
        sat = int(curve["d_sat"])
        roles.setdefault(sat, []).append("D_sat" + (" (open)" if curve["d_sat_undecided"] else ""))
        double = next((d for d in sorted(tested) if d >= 2 * sat), None)
        if double is not None:
            roles.setdefault(double, []).append("2 D_sat")
    return {d: ", ".join(r) for d, r in sorted(roles.items())}
