# Phase 2: start-shape map

If flock size is fixed, does a different sheep layout at the start change how many dogs we need?

Baseline is `strombom_multi`, with layouts compact / wide / split / outlier_rich. Pilot (N in {5, 10, 25, 50, 100}, D in {1, 2, 3, 4, 6, 10}, 5 seeds, 600 trials, 7m 1s), then scout (N in {50, 100, 200}, full D, 30 seeds, 3,600 trials, 3h 13m 53s), then claim (24 windows at 100 seeds, 2,400 trials, merge 5,280, 2h 59m 17s). Sim total about **6h 20m**.

Claim-grade: `D_min` = 1 on all four layouts at every N; cost rises on wide / outlier_rich. **C1a REJECTED** (the claim was "layout changes `D_min`"; it does not). **C1b INCONCLUSIVE**.

## How we get this

| Folder | Grade | Command (typical) | Trials |
|--------|-------|-------------------|-------:|
| [pilot_state/](pilot_state/) | SMOKE | `run --protocol phase2_pilot_state --workers 16` | 600 |
| [scout/](scout/) | SCOUT | `run --protocol phase2_scout --workers 16` | 3,600 |
| [claim/](claim/) | CLAIM | `claim-reseed --protocol phase2_claim --workers 16` | 2,400 (merge 5,280) |

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

Each protocol folder lists what is present. Common names: `protocol.yaml`, `provenance.json`, `status.json`, `manifest.jsonl`, `trials.csv`, `packages/b/`. Claim also has merge / boundary / bootstrap files.
