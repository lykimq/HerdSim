# Comparison framework

HerdSim is an experimental platform for studying multi-shepherd herding under shared scenarios, seeds, and instrument-independent metrics. Instruments are factor bundles over sheep models and dog controllers.

## Contribution framing

The research goal is not only to implement individual herding controllers. It is to run equivalent experiments across mechanisms and conditions, then report outcomes with reproducible provenance.

Core instruments:

| Instrument | Sheep model | Dog controller |
|------------|-------------|----------------|
| `strombom` | strombom | collect_drive |
| `kubo` | kubo | kubo_forces |
| `flocking_dog` | jadhav | collect_drive |

Variants (`strombom_noise`, `heterogeneous`, `fat`, `adaptive`, ...) are presets over the same factor space.

## Fair-comparison protocol

1. Scenario: shared (default `drive_to_goal`).
2. Preset: `custom` when locking agent counts.
3. Lock `n_sheep` and `n_shepherds`.
4. Same `max_ticks` / success criterion.
5. Seeds: at least 30 for distribution reporting.
6. Report distributions, not only means.

Run this in the **Experiments** tab (Compare instruments mode) with shared
custom counts, then export CSV/JSON. Prefer `custom` over paper presets when
models declare different agent counts.

## Factor experiments

Use **Experiments** → factor grid for one instrument. Example axes:

- Herdability: `n_sheep` x `n_shepherds`
- Information: `obs_mode` x `stubborn_fraction` (and sensing/noise when relevant)

Export includes trial rows, summary, experiment design, and caveats.

## Statistical reporting norms

- Success and failure rates across seeds.
- Median and IQR of completion ticks on successful trials.
- Trajectory AUC cohesion and fragmentation.
- Mean shepherd path and control efficiency.
- Failure-mode counts on unsuccessful trials (`failure_mode` in trial rows).
- Document tick/`dt` caveats when comparing Strombom-family and Kubo path lengths.
