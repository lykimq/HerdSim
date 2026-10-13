# Phase 4 Kubo size claim

Claim-grade compact size map for Kubo: same N in {5..400} and D in {1..35} freeze, reliability windows at 100 seeds (2,100 claim trials). Merge: 4,470 rows. Runtime 4h 27m 49s. Frontier: `D_min` = 3 at N=5, `D_min` = 1 for N >= 10 through 400. No overcrowding. Feeds **C4**: Kubo shares `D_min` = 1 with Strombom for N >= 25 on compact (full verdict in `../../package_d/size/` and `../../README.md`).

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase4_kubo_size_claim
uv run cli/campaign.py claim-reseed --protocol phase4_kubo_size_claim --workers 16
```

Output: `results/phase4/kubo_size/claim/`

Started: 2026-09-25T21:45:04Z. Finished: 2026-09-26T02:12:52Z.

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
