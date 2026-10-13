# Phase 4 FAT size claim

Claim-grade compact size map for FAT: same N in {5..400} and D in {1..35} freeze, reliability windows at 100 seeds (2,000 claim trials). Merge: 4,400 rows. Runtime 5d 4h 42m 35s. `D_min` = 1 at N in {5, 10}; hard failure for N >= 25 through 400. Feeds **C4**: FAT does not share the mid/large-N size map with Strombom/Kubo (full verdict in `../../package_d/size/` and `../../README.md`).

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase4_fat_size_claim
uv run cli/campaign.py claim-reseed --protocol phase4_fat_size_claim --workers 16
```

Output: `results/phase4/fat_size/claim/`

Started: 2026-09-29T06:08:34Z. Finished: 2026-10-04T10:51:08Z.

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
- `packages/a/`, `packages/f/`: Package A size-map tables plus Package F scaling fits for this run.
