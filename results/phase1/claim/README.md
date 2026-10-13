# Phase 1 claim

Claim-grade size map: `strombom_multi`, compact, full freeze N in {5, 10, 25, 50, 75, 100, 150, 200, 300, 400} and D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}, but only 22 reliability-window cells reseeds at 100 seeds (2,200 claim trials). Merge with scout: 4,540 rows. Runtime 57m 31s. Overall success on the merge 0.963 (4,371 / 4,540). `D_min` = 2 for N in {5, 10}, and `D_min` = 1 for N >= 25. No overcrowding (`D_overcrowd`). Bootstrap band on `D_min` is one dog-list step for every N.

### Claims

- **C2a** (at theta 0.90 the baseline has overcrowding for at least one N, i.e. a `D_overcrowd`): **REJECTED**. Package A finds 0 overcrowding cells on this map.
- **C2b** (at least one D above `D_overcrowd` still fails at T = 20,000): **SKIPPED**. No overcrowding cells to extend, so T1 has nothing to run.
- **C6a** (a power law fits `D_min` vs N worse than piecewise / per-layout curves): **SUPPORTED (weak)**. Leave-one-N RMSE: power 0.247 > piecewise 0.132, but only two observed `D_min` levels, so not a strong scaling law.
- **C6b** (log `D_min` vs log N has slope below 1 on a stated band): **SUPPORTED**. On compact N in {25..400}, `D_min` = 1 flat (slope 0 < 1).
- **C7a** (held-out state AUROC beats the `(N, D)` baseline): **INCONCLUSIVE**. Package G folds empty; AUROC not computable. AUROC = Area Under the ROC Curve, a 0-to-1 score for how well a model ranks likely failures vs successes (0.5 = chance, 1.0 = perfect); here it asks whether flock-state features predict failure better than knowing only `(N, D)` on held-out data.
- **C7b** (at least 30% of failure trials have lead time >= 500 ticks): **REJECTED**. Only 14 / 169 failures (8.3%) meet that bar.

## How we get this

```bash
uv run cli/campaign.py claim-plan --protocol phase1_claim
uv run cli/campaign.py claim-reseed --protocol phase1_claim --workers 16
```

Then Package A / F / G on `merged_trials.csv`. Output: `results/phase1/claim/`

Started: 2026-09-22T12:07:52Z. Finished: 2026-09-22T13:05:23Z.

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
- `timeseries/`: one trajectory file per cell (per-tick history) for analyses such as Package G early warning.
- `packages/a/`: Package A size-map tables (reliability, frontier, regimes, bootstrap).
- `packages/f/`: Package F scaling fits (leave-one-N CV and model comparison for C6).
- `packages/g/`: Package G early-warning tables (lead time and AUROC evidence for C7).
