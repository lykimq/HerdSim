# Experiment results

This folder holds simulation run outputs for the scaling study. Each phase answers a different question about how many dogs are enough when the flock grows, when sheep start in a different shape, or when we swap the dog rule (controller).

Completed narrative: [final report](../docs/final_report.md) ([HTML](../docs/final_report.html)). Plan and status: [main scaling plan](../docs/main_scaling_plan.md), [progress tracker](../docs/progress_tracker.md). Figures for the report live under [`../docs/figures/`](../docs/figures/).

## Layout

```text
scaling/results/
  phase1/                  # Flock size: how many dogs as N grows (tight start)
    pilot/                 # 150 trials (smoke check)
    scout/                 # 3,000 trials (cheap full map: 10 N x 10 D x 30 seeds)
    claim/                 # 2,200 trials (careful 100-seed windows on D_min edges)
    t1/                    # Longer deadline plan (skipped: no overcrowding cells)

  phase2/                  # Start shape: compact, wide, split, outlier_rich
    pilot_state/           # 600 trials (smoke check)
    scout/                 # 3,600 trials (3 N x 4 layouts x 10 D x 30 seeds)
    claim/                 # 2,400 trials (careful 100-seed windows)

  phase4/                  # Other dog rules: kubo and fat vs baseline
    kubo_size/             # Kubo size map (scout + claim)
    kubo_structure/        # Kubo start-shape map (scout + claim; claim 4,000 trials)
    fat_size/              # FAT size map (scout + claim)
    fat_structure/         # FAT start-shape map (scout + claim)
    package_d/             # Side-by-side transfer tables (size + structure)
                           # Current: Kubo outlier_rich N=200 has D_min=20 (200 seeds)

  phase5/                  # Information ladders: observation, range, communication
```

## What sits in a protocol folder

| File or folder | Meaning |
|----------------|---------|
| `protocol.yaml` | Frozen settings for that run |
| `provenance.json` | Git commit, host, and timestamps |
| `manifest.jsonl` | Resume ledger: finished trials (`status=ok`) are skipped on re-run |
| `status.json` | Progress and whether the run finished |
| `trials.csv` | One row per simulation (claim folders also have `merged_trials.csv`) |
| `timeseries/` | Per-trial trajectory files (`.parquet`). Usually not kept in Git |
| `packages/` | Auto tables from analysis (Package A, B, F, ...); figures live under `docs/figures/packages/` |
| `README.md` | Short human note: status, key numbers, links |
