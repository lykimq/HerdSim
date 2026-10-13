# Phase 5 range scout

Sensing-range ladder scout: `strombom_multi`, compact, N in {100, 200}, D in {1, 2, 3, 4, 6, 10}, `obs_mode=local_positions`, `sensing_range` in {32.5, 65, 97.5, 130}, 30 seeds (1,440 trials). Runtime 41m 21s. Overall success 0.989. By range: 32.5 R=0.956; 65 / 97.5 / 130 each R=1.000 (n=360 each). Shortest range is the weak cell.

## How we get this

```bash
uv run cli/campaign.py run --protocol phase5_range_scout --workers 18
```

Output: `results/phase5/range_scout/`

Started: 2026-10-13T05:40:56Z. Finished: 2026-10-13T06:22:17Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
