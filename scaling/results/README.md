# Scaling experiment results

Protocol outputs for the scaling research program live here. Aggregated run data under `scaling/results/` is tracked in git (trial metrics, packages, provenance, status ledgers, and interactive HTML dossiers) so finished campaigns stay permanently available for analysis, peer review, and publication claims.

Science and protocol specifications: [scaling/docs/main_scaling_plan.md](../docs/main_scaling_plan.md)  
Run progress & claim statuses: [scaling/docs/progress_tracker.md](../docs/progress_tracker.md)  
Protocol subsets: [scaling/configs/protocols/](../configs/protocols/)  
Report template: [scaling/docs/REPORT_TEMPLATE.md](../docs/REPORT_TEMPLATE.md)

---

## 1. Directory Layout

```text
scaling/results/
  README.md                # This document (conventions & navigation)
  
  phase1/                  # RQ2: Flock Size Scaling (Baseline strombom_multi)
    pilot/                 # 150 trials (smoke test)
    scout/                 # 3,000 trials (10 N x 10 D x 30 seeds, compact)
    claim/                 # 2,200 trials (100 seeds reseed on D_min boundary cells)
    t1/                    # T1 long-budget evaluation (skipped: 0 overcrowding cells)
    guides/                # Interactive standalone HTML reports & visualization assets
    
  phase2/                  # RQ1: Spatial Structure (4 layout families, N in {50, 100, 200})
    pilot_state/           # 600 trials (smoke test across layouts)
    scout/                 # 3,600 trials (3 N x 4 layouts x 10 D x 30 seeds)
    claim/                 # 2,400 trials (24 boundary cells reseeded at 100 seeds)
    guides/                # Standalone HTML reports & layout diagrams (compact, wide, split, outlier)
    
  phase4/                  # RQ4: Algorithm Generality (kubo, fat vs baseline)
    kubo_size/             # Size scaling for Kubo controller (scout + claim)
    kubo_structure/        # Structure scaling for Kubo controller (scout + claim)
    fat_size/              # Size scaling for FAT controller (scout + claim)
    fat_structure/         # Structure scaling for FAT controller (scout + claim)
    package_d/             # Cross-method transfer tables (size & structure evidence)
    guides/                # Standalone HTML reports & comparison dashboards
```

---

## 2. Protocol Folder Standard Contents

Each protocol execution folder (e.g. `phase1/claim/`, `phase2/scout/`, `phase4/kubo_structure/claim/`) contains:

```text
phase{k}/{slug}/
  protocol.yaml            # Exact copy of the protocol YAML subset used
  provenance.json          # Execution provenance (commit SHA, timestamp, platform info)
  manifest.jsonl           # Append-only resume ledger (cell keys & run status)
  status.json              # Planned / done counts, elapsed time, running flag
  trials.csv               # Primary trial table (one row per completed simulation trial)
  merged_trials.csv        # (Claim folders) Combined 100-seed claim rows + 30-seed scout interior
  boundary_cells.csv       # (Claim folders) List of planned boundary cells
  boundary_plan.json       # (Claim folders) Parameters used by plan_claim_cells.py
  dmin_bootstrap.csv       # (Claim folders) 1,000 bootstrap resamples on D_min
  timeseries/              # Trajectory frames (*.parquet) keyed by cell stem
  packages/                # Auto-generated evidence packages:
    a/ ... g/              # Package A-G (tables, figures, and package_*.md)
  REPORT.md                # Markdown analysis summary note
```

---

## 3. Conventions

1. **Path Structure**: `phase{k}/{protocol_slug}/` (e.g. `phase1/scout`, `phase2/claim`, `phase4/fat_size/scout`).
2. **Resume Ledger**: `manifest.jsonl` is the sole source of truth for resumed runs. Completed trials (`status=ok`) are skipped automatically.
3. **Trial Naming**: Trial tables are always `trials.csv` (or `merged_trials.csv` for claim merges), never `summary.csv`.
4. **Timeseries Parquet Files**: Stored in `timeseries/` with keys matching cell stems, e.g.:
   `N50_D2_Lcompact_S2026_Mstrombom_multi.parquet`.
5. **Git Storage Policy**:
   - `trials.csv`, `status.json`, `manifest.jsonl`, `packages/`, and `guides/` are **tracked in Git**.
   - `timeseries/*.parquet` files are **ignored via `.gitignore`** to keep repository size small (~5.4 GB total across 21,250 files). They remain persisted on local disk for mechanism (RQ3) and early-warning (RQ7) investigations.
6. **HTML Guides**: Standalone interactive reports in `guides/share_en/REPORT_en.html` provide single-page navigable dossiers with interactive zoomable figures, tables, and claim summaries suitable for sharing via browser.

---

## 4. Operator Commands Quick Reference

```bash
# Phase 1: Size scaling
make -C scaling scaling-scout WORKERS=16
make -C scaling scaling-claim-plan
make -C scaling scaling-claim-reseed WORKERS=16
make -C scaling scaling-analyse PACKAGE=A TRIALS=results/phase1/claim/merged_trials.csv

# Phase 2: Structure scaling
make -C scaling scaling-phase2-scout WORKERS=16
make -C scaling scaling-phase2-claim-reseed WORKERS=16
make -C scaling scaling-analyse PACKAGE=B TRIALS=results/phase2/claim/merged_trials.csv

# Phase 4: Transfer across methods
make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo WORKERS=16
make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo WORKERS=16
make -C scaling scaling-analyse PACKAGE=D TRIALS=... --trials-by-method ...
```

---

## 5. Resuming an Interrupted Run

- Never delete `manifest.jsonl` in an active protocol folder.
- If a simulation crashes or is cancelled, re-run the exact same command.
- The runner detects already completed seeds in `manifest.jsonl` and resumes instantly from the exact point of interruption.
