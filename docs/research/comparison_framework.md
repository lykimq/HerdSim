# Comparison framework

HerdSim is an experimental platform for comparing multi-shepherd herding models
under shared scenarios and algorithm-independent metrics.

## Contribution framing

The research goal is not only to implement individual herding controllers. It is
to run equivalent experiments across fundamentally different models and report
outcomes with reproducible provenance.

Core model families used for comparison:

| Plugin id | Model family |
|-----------|--------------|
| `strombom` | Strombom et al. 2014 behavioural Collect/Drive heuristics |
| `kubo` | Kubo et al. 2022 force-based multi-dog model |
| `flocking_dog` | Jadhav et al. 2024 empirically informed flocking sheep + dog |

Variants (`strombom_noise`, `strombom_multi`, and others) are useful for
robustness and teaching; they are not separate model families.

## Task vs performance vs behaviour vs cost

| Layer | Question | Examples |
|-------|----------|----------|
| Task success | Did the scenario criterion succeed? | `success`, failure/timeout rate |
| Performance | How quickly / completely? | `total_ticks`, `first_success_tick`, `final_gcm_goal` |
| Behaviour | How did the flock evolve? | `auc_cohesion`, `auc_fragmentation`, `auc_polarization` |
| Cost | How much control effort? | `shepherd_path`, `control_efficiency` |

## Fair-comparison protocol

1. Scenario: shared (default `drive_to_goal`).
2. Preset: `custom` (or equivalent Arena overrides), **not** paper when agent counts differ by model.
3. Lock `n_sheep` and `n_shepherds` for every algorithm.
4. Same `max_ticks` / success criterion from the scenario.
5. Seeds: at least 30 independent seeds per algorithm for distribution reporting.
6. Report distributions (success probability, median/IQR ticks), not only means.

CLI recipe:

```bash
python scripts/run_fair_compare.py \
  --algorithms strombom,kubo,flocking_dog \
  --scenario drive_to_goal \
  --preset custom \
  --n-sheep 40 \
  --n-shepherds 4 \
  --seeds 1,2,3,...,30 \
  --out-dir results/fair_compare
```

Default seeds in the script are `1..30`.

## Statistical reporting norms

- Success and failure rates across seeds.
- Median and IQR of completion ticks on successful trials.
- Trajectory AUC cohesion and fragmentation (mean over trials).
- Mean shepherd path and control efficiency.
- Document tick/`dt` caveats when comparing path across Strombom-family and Kubo.

## Paper preset vs fair comparison

Paper preset keeps each algorithm's published default agent counts and gains.
That is appropriate for model-faithful single-algorithm demos. Cross-model
tables must override counts so every model faces the same experiment knobs.
