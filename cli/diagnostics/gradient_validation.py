"""Validates how accurately Local Density Gradients approximate Global Center of Mass (GCM).

In canonical Strömbom dynamics, sheep compute social cohesion attracted to the GCM of
the whole flock (LCM with n = N - 1). This diagnostic evaluates whether individuals can
estimate the flock centroid direction purely from local density gradients over their
k-nearest topological neighbors, without requiring omniscient global sensing.

For each sheep i:
1. True GCM direction: v_GCM = (GCM - x_i) / ||GCM - x_i||
2. Local density gradient: g_local = sum_{j in N_k(i)} (x_j - x_i) / ||x_j - x_i||
3. Angular error: theta_err = arccos(clip(v_GCM . (g_local / ||g_local||), -1, 1))

Outputs the mean and median angular errors (in degrees) across k for each layout.
"""

from __future__ import annotations

import argparse
from typing import Any

import numpy as np
from scipy.spatial import cKDTree

from sim.core.world.layouts import LAYOUTS, place_flock
from tests.helpers import config_for


def evaluate_flock_gradient_error(
    positions: np.ndarray,
    k_neighbors: int,
    *,
    outer_only: bool = True,
) -> np.ndarray:
    """Computes angular error (in degrees) between local density gradient and GCM for sheep.

    Parameters
    ----------
    positions:
        Array of shape (N, 2) containing sheep coordinates.
    k_neighbors:
        Number of nearest topological neighbors to include in density gradient.
    outer_only:
        If True, only evaluate sheep farther than median distance from centroid,
        where heading toward the flock center is physically meaningful.

    Returns
    -------
    Array of angular errors in degrees for the evaluated sheep.
    """
    n = len(positions)
    if n <= k_neighbors:
        return np.array([0.0])

    centroid = positions.mean(axis=0)
    dists_to_centroid = np.linalg.norm(positions - centroid, axis=1)

    if outer_only:
        mask = dists_to_centroid >= np.median(dists_to_centroid)
    else:
        mask = np.ones(n, dtype=bool)

    if not mask.any():
        return np.array([0.0])

    tree = cKDTree(positions)
    # Query k + 1 neighbors (first neighbor is self at distance 0)
    _, indices = tree.query(positions[mask], k=k_neighbors + 1)

    eval_positions = positions[mask]
    to_gcm = centroid - eval_positions
    norm_to_gcm = np.linalg.norm(to_gcm, axis=1, keepdims=True)
    norm_to_gcm[norm_to_gcm == 0] = 1.0
    u_gcm = to_gcm / norm_to_gcm

    angular_errors: list[float] = []
    for i, row in enumerate(indices):
        neighbor_idx = row[1:]  # Exclude self
        rel_vectors = positions[neighbor_idx] - eval_positions[i]
        dists = np.linalg.norm(rel_vectors, axis=1, keepdims=True)
        dists[dists == 0] = 1.0
        # Local density gradient points toward average neighbor direction
        g_local = np.sum(rel_vectors / dists, axis=0)
        norm_g = np.linalg.norm(g_local)
        if norm_g == 0:
            continue
        u_local = g_local / norm_g
        dot_prod = float(np.clip(np.dot(u_gcm[i], u_local), -1.0, 1.0))
        angle_deg = float(np.degrees(np.arccos(dot_prod)))
        angular_errors.append(angle_deg)

    return np.array(angular_errors)


def run_gradient_validation(
    *,
    flock_sizes: tuple[int, ...] = (25, 100, 400),
    layouts: tuple[str, ...] = LAYOUTS,
    k_values: tuple[int, ...] = (3, 5, 7, 10, 15),
    n_seeds: int = 10,
) -> dict[str, Any]:
    """Runs density gradient benchmark across flock sizes, layouts, and neighbor counts."""
    results: dict[str, Any] = {}

    for layout in layouts:
        results[layout] = {}
        for n in flock_sizes:
            results[layout][n] = {}
            for k in k_values:
                if k >= n:
                    continue
                errors: list[float] = []
                for seed in range(n_seeds):
                    rng = np.random.default_rng(2026 + seed)
                    config = config_for("strombom_multi", n=n, layout=layout)
                    positions = place_flock(config, rng)
                    errs = evaluate_flock_gradient_error(positions, k)
                    errors.extend(errs.tolist())

                results[layout][n][k] = {
                    "mean_deg": float(np.mean(errors)),
                    "median_deg": float(np.median(errors)),
                    "std_deg": float(np.std(errors)),
                }

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Local Density Gradient vs GCM.")
    parser.add_argument("--seeds", type=int, default=10, help="Number of random seeds per cell.")
    args = parser.parse_args()

    print("=" * 80)
    print("HerdSim Diagnostic: Local Density Gradient vs Global Center of Mass (GCM)")
    print("=" * 80)
    print(
        f"Sampling {args.seeds} seeds per layout across N in [25, 100, 400] and k in [3..15]...\n"
    )

    results = run_gradient_validation(n_seeds=args.seeds)


    for layout in LAYOUTS:
        print(f"\n--- Layout: {layout.upper()} ---")
        print(f"{'N':>5} | {'k':>4} | {'Mean Error':>12} | {'Median Error':>14} | {'Std Dev':>10}")
        print("-" * 55)
        for n in (25, 100, 400):
            for k in (3, 5, 7, 10, 15):
                if k not in results[layout][n]:
                    continue
                stats = results[layout][n][k]
                line = (
                    f"{n:5d} | {k:4d} | {stats['mean_deg']:10.1f} deg | "
                    + f"{stats['median_deg']:12.1f} deg | {stats['std_deg']:8.1f} deg"
                )
                print(line)



if __name__ == "__main__":
    main()
