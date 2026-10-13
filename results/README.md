# Experiment results

Simulation outputs for the scaling study: how many dogs are enough when the flock grows, when sheep start in a different shape, when we swap the dog rule, or when we change observation, range, or communication.

| Phase | Main answer | Claims |
|-------|-------------|--------|
| 1 | `D_min` = 2 for tiny N, else 1; no overcrowding | C2a REJECTED; C2b SKIPPED; C6a weak SUPPORT; C6b SUPPORT; C7a INCONCLUSIVE; C7b REJECTED |
| 2 | `D_min` = 1 on all four layouts; cost rises on wide / outlier_rich | C1a REJECTED; C1b INCONCLUSIVE |
| 4 | Kubo shares compact mid/large N; FAT absent; Kubo wide absent; Kubo outlier_rich N=200 shifts to 20 | C4 SUPPORTED (partial) |
| 5 | Obs/range/comm ladders complete; range step lowers `D_min`, further steps save 0 more | C5a SUPPORTED; C5b SUPPORTED |

## How we get this

```bash
uv run cli/campaign.py run --protocol <protocol_id> --workers 16
uv run cli/campaign.py claim-reseed --protocol <protocol_id> --workers 16
```

```text
results/
  phase1/     flock size (compact + strombom_multi)
  phase2/     start shape (four layouts)
  phase4/     transfer (kubo / fat size + structure; package_d)
  phase5/     information ladders (obs / range / comm)
```

Each protocol-folder README has that run's command, runtime, and start / finish times.

## Files from this run

Machine-written outputs live under each protocol folder. Typical names: `protocol.yaml`, `provenance.json`, `status.json`, `manifest.jsonl`, `trials.csv`; claim extras `boundary_*`, `merged_trials.csv`, `*dmin_bootstrap.csv`; `packages/`; `timeseries/` only when retained (Phase 1 claim has it). Each protocol README lists only what is present there.
