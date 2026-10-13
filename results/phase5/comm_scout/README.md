# Phase 5 communication scout

Communication ladder scout: `strombom_multi`, compact, N in {100, 200}, D in {1, 2, 3, 4, 6, 10}, `obs_mode=local_positions`, `communication` in {none, neighbour_broadcast, global_shared}, 30 seeds (1,080 trials). Runtime 26m 12s. Overall success 1.000 on every communication setting (n=360 each).

## How we get this

```bash
uv run cli/campaign.py run --protocol phase5_comm_scout --workers 18
```

Output: `results/phase5/comm_scout/`

Started: 2026-10-13T07:40:16Z. Finished: 2026-10-13T08:06:28Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
