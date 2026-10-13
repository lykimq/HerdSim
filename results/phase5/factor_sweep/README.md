# Phase 5 observation scout (`factor_sweep`)

Observation ladder scout: `strombom_multi`, compact, N in {100, 200}, D in {1, 2, 3, 4, 6, 10}, `obs_mode` in {bearing_only, local_positions, global}, 30 seeds (1,080 trials). Runtime 7h 6m 20s. Overall success 0.735. By mode: global R=1.000; local_positions R=1.000; bearing_only R=0.206 (n=360 each). Feeds obs claim windows. Full ladder verdicts: **C5a / C5b SUPPORTED** on the range claim.

## How we get this

```bash
uv run cli/campaign.py run --protocol phase5_factor_sweep --workers 18
```

Started: 2026-10-12T14:42:21Z. Finished: 2026-10-12T21:48:40Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
