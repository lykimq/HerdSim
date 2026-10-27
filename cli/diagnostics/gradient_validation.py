"""How well a sheep could find the flock centre from its nearest neighbours alone.

    uv run cli/diagnostics/gradient_validation.py --seeds 10

Strombom 2014 attracts a sheep toward the centre of its n nearest neighbours, which with
n = N - 1 is the centre of the whole flock. This asks how far off a sheep would be with a
small n: for each sheep in the outer half of a start layout, the angle between the direction
to the flock centroid and the sum of unit vectors toward its k nearest neighbours. Start
layouts only, no dynamics. Prints the mean, median and spread of that angle per layout, N
and k.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from services.cells import Cell, Group, cell_config  # noqa: E402
from services.protocol import load_protocol  # noqa: E402
from sim.core.world.layouts import LAYOUTS, place_flock  # noqa: E402

# Flock radii R_f of results/dmin_m12/calibration.json, rounded; they only size the compact
# layout here, so the check does not need that folder.
FLOCK_RADIUS = {25: 6.2, 100: 9.08, 400: 11.4}
PROTOCOL = "dmin_pilot"  # any drive protocol with the four layouts; only its settings are used
FLOCK_SIZES = (25, 100, 400)
K_VALUES = (3, 5, 7, 10, 15)


def evaluate_flock_gradient_error(
    positions: np.ndarray, k_neighbors: int, *, outer_only: bool = True
) -> np.ndarray:
    """Angle in degrees, per evaluated sheep, between the direction to the centroid and the
    sum of unit vectors toward its ``k_neighbors`` nearest neighbours.

    With ``outer_only`` only the sheep beyond the median distance from the centroid are
    evaluated, where "toward the centre" has a meaning. A sheep whose neighbour sum is zero
    is skipped. One zero for a flock too small to have k neighbours.
    """
    n = len(positions)
    if n <= k_neighbors:
        return np.array([0.0])
    centroid = positions.mean(axis=0)
    to_centroid = centroid - positions
    radius = np.linalg.norm(to_centroid, axis=1)
    chosen = radius >= np.median(radius) if outer_only else np.ones(n, dtype=bool)
    if not chosen.any():
        return np.array([0.0])

    _, neighbours = cKDTree(positions).query(positions[chosen], k=k_neighbors + 1)
    neighbours = neighbours[:, 1:]  # the first neighbour is the sheep itself
    offsets = positions[neighbours] - positions[chosen][:, None, :]  # (m, k, 2)
    lengths = np.linalg.norm(offsets, axis=2, keepdims=True)
    gradient = (offsets / np.maximum(lengths, 1e-12)).sum(axis=1)

    gradient_length = np.linalg.norm(gradient, axis=1)
    ok = gradient_length > 0.0
    unit_centroid = to_centroid[chosen][ok] / np.maximum(radius[chosen][ok], 1e-12)[:, None]
    unit_gradient = gradient[ok] / gradient_length[ok][:, None]
    cosine = np.clip(np.sum(unit_centroid * unit_gradient, axis=1), -1.0, 1.0)
    return np.degrees(np.arccos(cosine))


def _start_config(protocol: Any, n: int, layout: str) -> dict[str, Any]:
    cell = Cell(Group("strombom_multi", layout, (), n), 1)
    return cell_config(protocol, cell, FLOCK_RADIUS[n])


def run_gradient_validation(
    *,
    flock_sizes: tuple[int, ...] = FLOCK_SIZES,
    layouts: tuple[str, ...] = LAYOUTS,
    k_values: tuple[int, ...] = K_VALUES,
    n_seeds: int = 10,
) -> dict[str, Any]:
    """results[layout][n][k] = mean, median and standard deviation of the angle in degrees
    over ``n_seeds`` start flocks."""
    protocol = load_protocol(PROTOCOL)
    results: dict[str, Any] = {}
    for layout in layouts:
        results[layout] = {}
        for n in flock_sizes:
            config = _start_config(protocol, n, layout)
            flocks = [place_flock(config, np.random.default_rng(2026 + s)) for s in range(n_seeds)]
            results[layout][n] = {}
            for k in k_values:
                if k >= n:
                    continue
                errors = np.concatenate([evaluate_flock_gradient_error(f, k) for f in flocks])
                results[layout][n][k] = {
                    "mean_deg": float(errors.mean()),
                    "median_deg": float(np.median(errors)),
                    "std_deg": float(errors.std()),
                }
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--seeds", type=int, default=10, help="start flocks per layout and N")
    args = parser.parse_args()

    results = run_gradient_validation(n_seeds=args.seeds)
    for layout in LAYOUTS:
        print(f"\n{layout}")
        print(f"{'N':>5} {'k':>4} {'mean':>8} {'median':>8} {'sd':>8}  (degrees)")
        for n in FLOCK_SIZES:
            for k, stats in sorted(results[layout][n].items()):
                line = f"{n:5d} {k:4d} {stats['mean_deg']:8.1f} {stats['median_deg']:8.1f}"
                print(line + f" {stats['std_deg']:8.1f}")


if __name__ == "__main__":
    main()
