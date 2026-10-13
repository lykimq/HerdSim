# Phase 1 pilot

Smoke check for the Phase 1 size map: baseline dog rule (`strombom_multi`), compact start, N in {5, 10, 25, 50, 100}, D in {1, 2, 3, 4, 6, 10}, 5 seeds (150 trials). Runtime 43 seconds. Overall success 0.947. Failures only at tiny flocks with one dog (N=5 D=1 fails; N=10 D=1 is weak). Fewest dogs (`D_min`) is 2 for N in {5, 10}, and 1 for N in {25, 50, 100}. No overcrowding on this small grid. Smoke only: not claim-grade.

## How we get this

```bash
uv run cli/campaign.py run --protocol phase1_pilot --workers 16
```

Output: `results/phase1/pilot/`

Started: 2026-09-22T10:45:41Z. Finished: 2026-09-22T10:46:24Z.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `protocol.yaml`: frozen settings for this run (method, layouts, N/D grids, seeds, grade). Use this copy to replay or audit without depending on live YAML under `protocols/`.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `status.json`: progress counters and wall time (`n_planned`, `n_done`, `complete`, `elapsed_seconds`).
- `manifest.jsonl`: one JSON line per planned cell; rows already `status=ok` are skipped on resume.
- `trials.csv`: one row per seed (N, D, layout, success, ticks, path/effort, failure tags, state metrics). Raw table everything else is built from.
- `packages/a/`: Package A size-map tables (reliability, frontier, regimes, bootstrap).
