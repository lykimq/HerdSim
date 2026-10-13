# Phase 5: information ladders (RQ5)

Do observation mode, sensing range, or communication change how many dogs we need (**C5a / C5b**)?

Three ladders share the same base: `strombom_multi`, compact, N in {100, 200}, D in {1, 2, 3, 4, 6, 10}. Obs varies `obs_mode`; range varies `sensing_range` in {32.5, 65, 97.5, 130}; comm varies `communication` in {none, neighbour_broadcast, global_shared}.

All six stages finished (2026-10-13T08:38:30Z). Sim total about **17h 55m** (sum of protocol `elapsed_seconds`).

**Obs:** global and local_positions have `D_min` = 1 at N in {100, 200}; bearing_only never reaches theta = 0.90 (merge R about 0.22). **Range:** sensing_range 32.5 needs more dogs (`D_min` = 3 at N=100, `D_min` = 2 at N=200); 65 / 97.5 / 130 all have `D_min` = 1. **Comm:** all modes `D_min` = 1 (merge R = 1.000).

### Claims

- **C5a** (one ladder step lowers `D_min` by at least one D-grid step at N in {100, 200}): **SUPPORTED** on the range ladder. Stepping from sensing_range 32.5 to 65 lowers `D_min` by 2 at N=100 (3 -> 1) and by 1 at N=200 (2 -> 1). Obs mainly turns a hard failure (bearing_only) into `D_min` = 1; comm does not change `D_min`.
- **C5b** (the second ladder step saves fewer dogs than the first): **SUPPORTED** on the same range ladder. First step (32.5 -> 65) saves 1 to 2 dogs; further steps (65 -> 97.5 -> 130) save 0 more (`D_min` already 1).

## How we get this

```bash
uv run cli/campaign.py run --protocol phase5_factor_sweep --workers 18
uv run cli/campaign.py claim-reseed --protocol phase5_obs_claim --workers 18
uv run cli/campaign.py run --protocol phase5_range_scout --workers 18
uv run cli/campaign.py claim-reseed --protocol phase5_range_claim --workers 18
uv run cli/campaign.py run --protocol phase5_comm_scout --workers 18
uv run cli/campaign.py claim-reseed --protocol phase5_comm_claim --workers 18
```

| Folder | Stage | Status | Runtime |
|--------|-------|--------|---------|
| [factor_sweep/](factor_sweep/) | obs scout | complete (1,080) | 7h 6m 20s |
| [obs_claim/](obs_claim/) | obs claim | complete (1,200; merge 1,920) | 7h 52m 10s |
| [range_scout/](range_scout/) | range scout | complete (1,440) | 41m 21s |
| [range_claim/](range_claim/) | range claim | complete (1,700; merge 2,630) | 1h 17m 52s |
| [comm_scout/](comm_scout/) | comm scout | complete (1,080) | 26m 12s |
| [comm_claim/](comm_claim/) | comm claim | complete (1,200; merge 1,920) | 31m 56s |

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

Each subfolder holds that stage's run outputs (`protocol.yaml`, `status.json`, `trials.csv`, claim merges, ...). See that folder's README for the file list.
