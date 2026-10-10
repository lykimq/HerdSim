# Protocol configurations

YAML run recipes for scaling experiments. Protocols define the method, flock sizes $N$, shepherd counts $D$, initial layouts $X_0$, and seeds.

## Protocol files by phase

### Phase 1: Size scaling
- `phase1_pilot.yaml`: smoke test on reduced $N$ and $D$.
- `phase1_scout.yaml`: full grid (10 $N \times 10 D \times 30$ seeds).
- `phase1_claim.yaml`: 100 seeds on boundary cells around $D_{\min}$.
- `phase1_t1.yaml`: 20,000 ticks on overcrowding cells (if any).

### Phase 2: Spatial structure
- `phase2_pilot_state.yaml`: smoke test across all 4 layouts.
- `phase2_scout.yaml`: 3 $N \times 4$ layouts $\times 10 D \times 30$ seeds.
- `phase2_claim.yaml`: 100 seeds on boundary cells.

### Phase 4: Transfer across controllers
- `phase4_kubo_size_scout.yaml` / `phase4_kubo_size_claim.yaml`: Kubo size scaling.
- `phase4_kubo_structure_scout.yaml` / `phase4_kubo_structure_claim.yaml`: Kubo structure scaling.
- `phase4_fat_size_scout.yaml` / `phase4_fat_size_claim.yaml`: FAT size scaling.
- `phase4_fat_structure_scout.yaml` / `phase4_fat_structure_claim.yaml`: FAT structure scaling.

*Note*: Scout YAMLs set `store_timeseries: false` to reduce disk I/O. Claim YAMLs set `store_timeseries: true` to record trajectories for boundary cells. Package D is compiled jointly across all three methods.

### Phase 5: Information ladders
- `phase5_factor_sweep.yaml` / `phase5_obs_claim.yaml`: observation modes (bearing, local, global).
- `phase5_range_scout.yaml` / `phase5_range_claim.yaml`: sensing range sweeps.
- `phase5_comm_scout.yaml` / `phase5_comm_claim.yaml`: communication modes.

## Conventions

- `canonical`: references `run/configs/canonical_grid.yaml` for frozen defaults.
- `extends`: inherits from a parent protocol YAML; only overrides need to be specified.
- `grade`: `SMOKE` (5 seeds), `SCOUT` (30 seeds), or `CLAIM` (100 seeds).
- `output`: destination folder under `results/`.
