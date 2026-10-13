# Phase 4 FAT structure scout

Cheap FAT start-shape map: layouts compact / wide / split / outlier_rich, N in {50, 100, 200}, D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}, 30 seeds (3,600 trials). Runtime 1d 10h 0m 6s. Hard failure on every layout x N cell (success never reaches theta = 0.90). Scout only: claim confirms the same in `../claim/`.

## How we get this

```bash
uv run cli/campaign.py run --protocol phase4_fat_structure_scout --workers 16
```

Output: `results/phase4/fat_structure/scout/`

Started: 2026-09-29T19:38:44Z. Finished: 2026-10-01T05:38:50Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
- `packages/b/`: Package B structure tables (layout frontiers and state-vs-(N, D) predictors).
