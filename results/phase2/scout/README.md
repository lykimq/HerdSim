# Phase 2 scout

Cheap start-shape map for claim planning: `strombom_multi`, layouts compact / wide / split / outlier_rich, N in {50, 100, 200}, D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}, 30 seeds (3,600 trials). Runtime 3h 13m 53s. 

Scout Package B shows `D_min` = 1 on all four layouts; cost (`B*`) rises on wide and large outlier_rich. Scout only: claim-grade numbers live in `../claim/`.

## How we get this

```bash
uv run cli/campaign.py run --protocol phase2_scout --workers 16
```

Output: `results/phase2/scout/`

Started: 2026-09-25T09:25:40Z. Finished: 2026-09-25T12:39:33Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
- `packages/b/`: Package B structure tables (layout frontiers and state-vs-(N, D) predictors).
