# Phase 2 claim

Claim-grade start-shape map: does layout change how many dogs we need? `strombom_multi`, layouts compact / wide / split / outlier_rich, N in {50, 100, 200}, D grid {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} on 24 reliability-window cells at 100 seeds (2,400 claim trials). Merge: 5,280 rows. Runtime 2h 59m 17s. Success on the claim windows at D = 1 is 1.0. `D_min` = 1 on every layout x N cell. No overcrowding. Path / time cost rises on wide and outlier_rich (on wide, cheap good setup `B*` shifts to 2 dogs while `D_min` stays 1).

### Claims

- **C1a** (for at least one N, `D_min` differs by at least one D-grid step across layouts at theta 0.90): **REJECTED**. `D_min` stays 1 on every layout x N cell.
- **C1b** (a state model beats a plain `(N, D)` model on leave-one-N NLL): **INCONCLUSIVE**. With no `D_min` shift, the state-vs-(N, D) comparison has nothing extra to explain.

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase2_claim
uv run cli/campaign.py claim-reseed --protocol phase2_claim --workers 16
```

Then Package B on `merged_trials.csv`. Output: `results/phase2/claim/`

Started: 2026-09-25T12:40:20Z. Finished: 2026-09-25T15:39:37Z.

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
