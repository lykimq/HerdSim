"""Pressure on the flock in a replayed trial: how long the sheep spend near a dog.

The trial rows keep summaries of the tick metrics, and none of them says how close the dogs
come to the sheep. A replay runs a stored trial again from its seed. A trial is deterministic in
its config and seed, so the replay is the same trial; ``replay`` checks this against the stored
outcome and raises when it differs, because a replay that is not the stored trial says nothing
about the stored results.

Two shares are recorded per tick: the share of sheep closer than the reaction radius to some
dog (for Strombom sheep, the sheep in flight: they react to a dog strictly closer than r_s),
and the share closer than ``close`` (the Strombom dog's stop distance, 3 r_a, by default), the
distance at which a dog is as close to a sheep as the dog rule lets it get. Summed over the
ticks and multiplied by dt they give the seconds a sheep spends in each, on average.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

from sim.core.simulation_runner import run_trial
from sim.core.simulation_state import SimulationState


class ReplayMismatch(RuntimeError):
    """A replayed trial did not reproduce the stored outcome."""


def near_shares(
    sheep: np.ndarray, dogs: np.ndarray, reach: float, close: float
) -> tuple[float, float]:
    """(share of sheep strictly closer than ``reach`` to some dog, share closer than ``close``)."""
    if len(dogs) == 0 or len(sheep) == 0:
        return 0.0, 0.0
    nearest = cdist(sheep, dogs).min(axis=1)
    return float(np.mean(nearest < reach)), float(np.mean(nearest < close))


@dataclass(frozen=True)
class ReplayJob:
    config: dict[str, Any]
    seed: int
    stored_success: bool
    stored_ticks: int
    label: dict[str, Any]  # layout, n, d, seed_index: carried into the result row


def replay(job: ReplayJob) -> dict[str, Any]:
    """One stored trial run again, with the pressure measures; raises ReplayMismatch."""
    config = job.config
    reach = float(config["reaction_radius"])
    close = float(config["shepherd_stop_multiple"]) * float(config["r_a"])
    flight: list[float] = []
    near: list[float] = []

    def watch(state: SimulationState) -> None:
        a, b = near_shares(state.sheep_positions, state.shepherd_positions, reach, close)
        flight.append(a)
        near.append(b)

    result = run_trial(config, job.seed, on_tick=watch)
    if result.success != job.stored_success or result.total_ticks != job.stored_ticks:
        got = f"success={result.success} ticks={result.total_ticks}"
        want = f"success={job.stored_success} ticks={job.stored_ticks}"
        raise ReplayMismatch(f"{job.label}: replay gave {got}, stored {want}")
    dt = float(config["dt"])
    return {
        **job.label,
        "success": result.success,
        "finish_seconds": result.total_ticks * dt,
        "flight_seconds_per_sheep": float(np.sum(flight)) * dt,
        "close_seconds_per_sheep": float(np.sum(near)) * dt,
        "mean_flight_share": float(np.mean(flight)) if flight else 0.0,
        "peak_flight_share": float(np.max(flight)) if flight else 0.0,
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
