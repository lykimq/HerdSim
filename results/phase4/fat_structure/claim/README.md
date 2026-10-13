# Phase 4 FAT structure claim

Claim-grade FAT start-shape map: layouts compact / wide / split / outlier_rich, N in {50, 100, 200}, D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}, 100 seeds on window cells (2,400 claim trials). Merge: 5,280 rows. Runtime 23h 37m 29s. Hard failure on every layout x N cell. Feeds **C4**: FAT structure transfer is absent vs baseline (baseline still has `D_min` = 1 on these cells). Full table in `../../package_d/structure/`.

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase4_fat_structure_claim
uv run cli/campaign.py claim-reseed --protocol phase4_fat_structure_claim --workers 16
```

Output: `results/phase4/fat_structure/claim/`

Started: 2026-10-01T05:38:59Z. Finished: 2026-10-02T05:16:28Z.

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
- `packages/b/`: Package B structure tables (layout frontiers and state-vs-(N, D) predictors).
