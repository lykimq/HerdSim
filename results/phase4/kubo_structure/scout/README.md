# Phase 4 Kubo structure scout

Cheap Kubo start-shape map: layouts compact / wide / split / outlier_rich, N in {50, 100, 200}, D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}, 30 seeds (3,600 trials). Runtime 16h 39m 37s. Scout sketch: compact / split keep `D_min` = 1; wide is hard failure; outlier_rich N=200 looks borderline at 30 seeds. Scout only: claim merge supersedes that row (`D_min` = 20 at 200 seeds). See `../claim/`.

## How we get this

```bash
uv run cli/campaign.py run --protocol phase4_kubo_structure_scout --workers 16
```

Output: `results/phase4/kubo_structure/scout/`

Started: 2026-09-26T02:13:01Z. Finished: 2026-09-26T18:52:38Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
- `packages/b/`: Package B structure tables (layout frontiers and state-vs-(N, D) predictors).
