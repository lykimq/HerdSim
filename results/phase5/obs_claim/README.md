# Phase 5 observation claim

Claim-grade observation ladder: `strombom_multi`, compact, N in {100, 200}, D in {1, 2, 3, 4, 6, 10}, `obs_mode` in {bearing_only, local_positions, global}, 100 seeds on windows (1,200 claim trials). Merge: 1,920 rows. Runtime 7h 52m 10s. Overall success on the merge 0.740. By mode: global R=1.000; local_positions R=1.000; bearing_only R=0.219 (each n=640). Bearing_only never reaches theta (no `D_min`); global / local_positions have `D_min` = 1. Primary **C5a / C5b** support is on the range ladder: **C5a SUPPORTED**, **C5b SUPPORTED**.

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase5_obs_claim
uv run cli/campaign.py claim-reseed --protocol phase5_obs_claim --workers 18
```

Upstream scout: `../factor_sweep/`. Output: `results/phase5/obs_claim/`

Started: 2026-10-12T21:48:44Z. Finished: 2026-10-13T05:40:54Z.

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
