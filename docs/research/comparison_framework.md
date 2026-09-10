# Comparison framework

HerdSim is an experimental platform for studying multi-shepherd herding under
shared scenarios, seeds, and algorithm-independent metrics. Instruments are
factor bundles over sheep models and dog controllers.

## Contribution framing

The research goal is not only to implement individual herding controllers. It is
to run equivalent experiments across mechanisms and conditions, then report
outcomes with reproducible provenance.

Core instruments:

| Instrument | Sheep model | Dog controller |
|------------|-------------|----------------|
| `strombom` | strombom | collect_drive |
| `kubo` | kubo | kubo_forces |
| `flocking_dog` | jadhav | collect_drive |

Variants (`strombom_noise`, `heterogeneous`, `fat`, `adaptive`, ...) are
presets over the same factor space.

## Fair-comparison protocol

1. Scenario: shared (default `drive_to_goal`).
2. Preset: `custom` when locking agent counts.
3. Lock `n_sheep` and `n_shepherds`.
4. Same `max_ticks` / success criterion.
5. Seeds: at least 30 for distribution reporting.
6. Report distributions, not only means.

```bash
python scripts/run_fair_compare.py \
  --algorithms strombom,kubo,flocking_dog \
  --scenario drive_to_goal \
  --preset custom \
  --n-sheep 40 \
  --n-shepherds 4 \
  --out-dir results/fair_compare
```

## Factor experiments

```bash
python scripts/run_factor_grid.py \
  --instrument strombom \
  --grid 'n_sheep=20,50,100;n_shepherds=1,2,4' \
  --seeds 1,2,3,4,5 \
  --out-dir results/herdability
```

Observation and heterogeneity axes:

```bash
python scripts/run_factor_grid.py \
  --instrument strombom \
  --grid 'obs_mode=global,local_positions,bearing_only;stubborn_fraction=0.0,0.5' \
  --seeds 1,2,3 \
  --out-dir results/information
```

## Statistical reporting norms

- Success and failure rates across seeds.
- Median and IQR of completion ticks on successful trials.
- Trajectory AUC cohesion and fragmentation.
- Mean shepherd path and control efficiency.
- Document tick/`dt` caveats when comparing Strombom-family and Kubo path lengths.
