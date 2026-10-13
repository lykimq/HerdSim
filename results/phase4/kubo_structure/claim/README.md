# Phase 4 Kubo structure claim

Claim-grade Kubo start-shape map: layouts compact / wide / split / outlier_rich, N in {50, 100, 200}, D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}, 100 seeds on standard windows plus 200 seeds on outlier_rich N=200 for D in {1, 2, 3, 4, 6, 10, 15, 20, 25} (4,000 claim rows). Merge: 6,670 rows. Runtime 9d 16h 1m 48s.

| Layout | N | D_min | Notes |
|--------|--:|------:|-------|
| compact / split | 50, 100, 200 | 1 | shared with baseline |
| outlier_rich | 50, 100 | 1 | shared |
| outlier_rich | 200 | 20 | 200 seeds; bootstrap [2, 20]; no overcrowding |
| wide | 50, 100, 200 | none | hard failure (best R about 0.47 to 0.54) |

### Claims

- **C4** (`D_min` or overcrowding is shared across the three required methods, including structure): **SUPPORTED (partial)**. 

Compact/split match baseline; wide is absent for Kubo; outlier_rich N=200 is shifted to `D_min` = 20. See also `../../package_d/structure/`.

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase4_kubo_structure_claim
uv run cli/campaign.py claim-reseed --protocol phase4_kubo_structure_claim --workers 16
```

Output: `results/phase4/kubo_structure/claim/`

Started: 2026-09-26T18:52:44Z. Finished: 2026-10-06T10:54:32Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
- `boundary_cells.csv`, `boundary_plan.json`: which (N, D, layout) cells get denser claim reseed, and how that list was built.
- `merged_trials.csv`: claim-grade table (dense claim windows plus scout rows for the rest). Same columns as `trials.csv`.
- `dmin_bootstrap.csv`, `merged_dmin_bootstrap.csv`: bootstrap point `D_min` and CI on claim trials and on the merge.
- `outlier_rich_n200_window.json`: rates by D, seed counts, point `D_min`, and bootstrap for Kubo outlier_rich N=200.
- `packages/b/`: Package B structure tables (layout frontiers and state-vs-(N, D) predictors).
