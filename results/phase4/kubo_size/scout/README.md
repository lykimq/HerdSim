# Phase 4 Kubo size scout

Cheap compact size map for Kubo: N in {5, 10, 25, 50, 75, 100, 150, 200, 300, 400}, D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}, 30 seeds (3,000 trials). Runtime 5h 31m 37s. `D_min` = 3 at N=5, `D_min` = 1 for N >= 10 through 400. No overcrowding. Scout only: claim-grade answer in `../claim/`.

## How we get this

```bash
uv run cli/campaign.py run --protocol phase4_kubo_size_scout --workers 16
```

Output: `results/phase4/kubo_size/scout/`

Started: 2026-09-25T16:12:20Z. Finished: 2026-09-25T21:43:57Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
- `packages/a/`: Package A size-map tables (reliability, frontier, regimes, bootstrap).
- `packages/f/`: Package F scaling fits (leave-one-N CV and model comparison for C6).
