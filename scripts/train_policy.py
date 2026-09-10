"""Offline train/eval harness stub for policy_file controllers.

Trains a simple linear policy on relative GCM/goal features using random
rollouts under a chosen instrument, then writes a JSON policy for
`dog_controller=policy_file`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.experiment_config import resolve_experiment_config
from core.simulation_runner import SimulationRunner
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry


def collect_dataset(instrument: str, seeds: list[int], ticks: int) -> tuple[np.ndarray, np.ndarray]:
    xs = []
    ys = []
    scenario = scenario_registry.get("drive_to_goal")
    for seed in seeds:
        config = resolve_experiment_config(
            scenario=scenario,
            instrument=instrument,
            preset="custom",
            num_sheep=20,
            num_shepherds=1,
            algorithm_params={"obs_mode": "global", "max_ticks": ticks},
        )
        runner = SimulationRunner(
            scenario=scenario,
            metrics=metric_registry.get_all(),
            config=config,
            seed=seed,
            instrument=instrument,
        )
        runner.initialize()
        for _ in range(ticks):
            state, _, status = runner.step()
            if state.n_shepherds == 0 or state.n_sheep == 0:
                break
            gcm = state.sheep_centroid
            dog = state.shepherd_positions[0]
            goal = state.world.goal.center
            feat = np.concatenate([gcm - dog, goal - dog])
            action = state.shepherd_velocities[0]
            xs.append(feat)
            ys.append(action)
            if status != "running":
                break
    return np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)


def fit_linear(x: np.ndarray, y: np.ndarray) -> dict:
    # Least squares for 2D action from features.
    # y ~= x @ W.T + b  -> solve per output dim.
    ones = np.ones((x.shape[0], 1))
    xb = np.concatenate([x, ones], axis=1)
    sol, *_ = np.linalg.lstsq(xb, y, rcond=None)
    weights = sol[:-1].T
    bias = sol[-1]
    return {
        "type": "linear",
        "feature": "relative_gcm_goal",
        "weights": weights.tolist(),
        "bias": bias.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--teacher", default="strombom")
    parser.add_argument("--seeds", default="1,2,3")
    parser.add_argument("--ticks", type=int, default=80)
    parser.add_argument("--out", default="results/policies/linear_policy.json")
    args = parser.parse_args()
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    x, y = collect_dataset(args.teacher, seeds, args.ticks)
    policy = fit_linear(x, y)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(policy, indent=2), encoding="utf-8")
    print(f"Wrote {out} from {len(x)} samples")


if __name__ == "__main__":
    main()
