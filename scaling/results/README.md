# Experiment results

Output data from scaling protocols across phases.

## Layout

```text
scaling/results/
  phase1/                  # Baseline flock size scaling
    pilot/                 # 150 trials (smoke)
    scout/                 # 3,000 trials (10 N x 10 D x 30 seeds)
    claim/                 # 2,200 trials (100 seeds on D_min boundary cells)
    t1/                    # T1 long-budget evaluation (skipped: 0 overcrowding cells)
    guides/                # HTML reports and figures
    
  phase2/                  # Spatial structure across 4 layouts (compact, wide, split, outlier_rich)
    pilot_state/           # 600 trials (smoke)
    scout/                 # 3,600 trials (3 N x 4 layouts x 10 D x 30 seeds)
    claim/                 # 2,400 trials (100 seeds on boundary cells)
    guides/                # HTML reports and layout figures
    
  phase4/                  # Transfer across controllers (kubo, fat vs baseline)
    kubo_size/             # Kubo size scaling (scout + claim)
    kubo_structure/        # Kubo structure scaling (scout + claim)
    fat_size/              # FAT size scaling (scout + claim)
    fat_structure/         # FAT structure scaling (scout + claim)
    package_d/             # Transfer tables (size and structure)
    guides/                # HTML reports and comparison figures
```

## Folder contents

Each protocol folder contains:
- `protocol.yaml`: configuration used for the run.
- `provenance.json`: commit hash, platform metadata, and execution timestamp.
- `manifest.jsonl`: append-only resume ledger. Completed trials (`status=ok`) are skipped on re-run.
- `status.json`: run progress and completion state.
- `trials.csv`: trial-level results (and `merged_trials.csv` for claim-grade merges).
- `timeseries/`: per-trial trajectory frames (`.parquet`). Ignored in Git to save disk space.
- `packages/`: generated analysis tables and figures (`packages/a/`, `packages/b/`, etc.).

## Reports

Each phase includes standalone HTML reports in `phase{k}/guides/share_en/REPORT_en.html` for reviewing figures, tables, and claim summaries in a browser.
