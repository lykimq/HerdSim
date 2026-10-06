# Experiment results

This folder holds the simulation outputs for the scaling study. Each phase answers a different question about how many dogs are enough when the flock grows, when sheep start in a different shape, or when we swap the dog rule (controller).

For the documentation map, see the [English index](../docs/INDEX.md) or [Vietnamese index](../docs/INDEX_vi.md). For completed findings, see [summary/SUMMARY_REPORT.html](summary/SUMMARY_REPORT.html) or [SUMMARY_REPORT.md](summary/SUMMARY_REPORT.md).

## Layout

```text
scaling/results/
  phase1/                  # Flock size: how many dogs as N grows (tight start)
    pilot/                 # 150 trials (smoke check)
    scout/                 # 3,000 trials (cheap full map: 10 N x 10 D x 30 seeds)
    claim/                 # 2,200 trials (careful 100-seed windows on D_min edges)
    t1/                    # Longer deadline plan (skipped: no overcrowding cells)
    guides/                # HTML reports and figures

  phase2/                  # Start shape: compact, wide, split, outlier_rich
    pilot_state/           # 600 trials (smoke check)
    scout/                 # 3,600 trials (3 N x 4 layouts x 10 D x 30 seeds)
    claim/                 # 2,400 trials (careful 100-seed windows)
    guides/                # HTML reports and layout figures

  phase4/                  # Other dog rules: kubo and fat vs baseline
    kubo_size/             # Kubo size map (scout + claim)
    kubo_structure/        # Kubo start-shape map (scout + claim; claim 4,000 trials)
    fat_size/              # FAT size map (scout + claim)
    fat_structure/         # FAT start-shape map (scout + claim)
    package_d/             # Side-by-side transfer tables (size + structure)
    guides/                # HTML reports and comparison figures
                           # Current: Kubo outlier_rich N=200 has D_min=20 (200 seeds)

  summary/                 # Cross-phase results, readable data appendices, and HTML builds
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
| `packages/` | Auto tables and figures from analysis (Package A, B, F, ...) |
| `README.md` | Short human note: status, key numbers, links |

## Reports

| Report | Path |
|--------|------|
| Cross-phase results (Phases 1, 2, 4) | [summary/SUMMARY_REPORT.html](summary/SUMMARY_REPORT.html) / [`.md`](summary/SUMMARY_REPORT.md) |
| Same in Vietnamese | [summary/SUMMARY_REPORT_vi.html](summary/SUMMARY_REPORT_vi.html) / [`.md`](summary/SUMMARY_REPORT_vi.md) |
| Scientific plan | [`../docs/main_scaling_plan.md`](../docs/main_scaling_plan.md) |
| Methods | [`../docs/methods/README.md`](../docs/methods/README.md) |
| Setup and run reference | [`../docs/setup/README.md`](../docs/setup/README.md) |
| Data appendices | [`summary/data/README.md`](summary/data/README.md) |
| Credibility and comparison | [`../docs/credibility/README.md`](../docs/credibility/README.md) |
| Former research-plan path | [summary/RESEARCH_PLAN.html](summary/RESEARCH_PLAN.html) compatibility page |

Rebuild the HTML from the markdown with `python3 summary/_rebuild_html.py`.

Each phase also has its own browser reports under `phase{k}/guides/REPORT_en.html` and `REPORT_vi.html` (shared `assets/`).
