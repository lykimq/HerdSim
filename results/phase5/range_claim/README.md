# Phase 5 range claim

Claim-grade sensing-range ladder: `strombom_multi`, compact, N in {100, 200}, D in {1, 2, 3, 4, 6, 10}, `sensing_range` in {32.5, 65, 97.5, 130}, 100 seeds on windows (1,700 claim trials). Merge: 2,630 rows. Runtime 1h 17m 52s. Overall success on the merge 0.972. By range: 32.5 R=0.897 (n=710); 65 / 97.5 / 130 each R=1.000 (n=640). Shortest range stays the weak band: `D_min` = 3 at N=100 and `D_min` = 2 at N=200 for sensing_range 32.5; longer ranges have `D_min` = 1. This is the main evidence for **C5a SUPPORTED** (32.5 -> 65 lowers `D_min`) and **C5b SUPPORTED** (further range steps save 0 more dogs).

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase5_range_claim
uv run cli/campaign.py claim-reseed --protocol phase5_range_claim --workers 18
```

Upstream scout: `../range_scout/`. Output: `results/phase5/range_claim/`

Started: 2026-10-13T06:22:21Z. Finished: 2026-10-13T07:40:13Z.

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
- `scout_dmin_bootstrap_preview.csv`: scout-side `D_min` bootstrap preview used while planning claim windows.
