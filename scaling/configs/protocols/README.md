# Scaling protocol YAMLs

This folder holds **run recipes** for `scaling_v2`: which method, N, D, layouts, seeds, grade, and output path. The campaign CLI loads them by `protocol_id`.

| Doc | Role |
|-----|------|
| [experiment_run_strategy.md](../../docs/experiment_run_strategy.md) | Why we stage pilot / scout / plan / reseed |
| [main_scaling_plan.md](../../docs/main_scaling_plan.md) | Science protocol, frontiers, claims |
| [progress_tracker.md](../../docs/progress_tracker.md) | What has been run |
| `make -C scaling help` | Make aliases over `campaign.py` |

Frozen defaults come from `scaling/configs/canonical_grid.yaml` via `canonical:`. Child YAMLs may `extends:` a parent; child keys replace parent keys.

## Grades (on every YAML)

| `grade` | Meaning |
|---------|---------|
| SMOKE | Tiny grid; pipeline check only |
| SCOUT | Full (or factor) grid at scout seed depth |
| CLAIM | Planned cells at claim seed depth |

Do not cite below the grade you ran. Details: experiment run strategy.

## Phases and files (order)

Phases 3, 6, and 7 have **no** grid YAML here. They are analyse packages on merged claim data (see tracker steps 9, 10, 17).

### Phase 1: size map (RQ2, Package A)

Purpose: baseline `strombom_multi`, compact layout, map `R(N, D)` and frontiers (`D_min`, overcrowding, `D_max`, `B*`).

| Order | File | Grade | Make (typical) | Role |
|-------|------|-------|----------------|------|
| 1 | `phase1_pilot.yaml` | SMOKE | `scaling-pilot` | Smoke reduced grid |
| 2 | `phase1_scout.yaml` | SCOUT | `scaling-scout` | Full N x D map at 30 seeds |
| 3 | `phase1_claim.yaml` | CLAIM | `scaling-claim-plan` then `scaling-claim-reseed` | Plan windows from scout; reseed at 100; write merge |
| 4 | `phase1_t1.yaml` | CLAIM | `scaling-t1` | Long horizon (20k ticks) on overcrowding cells |

`phase1_claim` sets `upstream_protocol: phase1_scout`. The runner does not execute the full claim grid; `plan_claim_cells` selects windows, then reseed runs those cells. `phase1_t1` prefers the claim merge as upstream.

### Phase 2: structure (RQ1, Package B)

Purpose: does `D_min` change with initial layout `X0` at fixed N in {50, 100, 200}?

| Order | File | Grade | Make (typical) | Role |
|-------|------|-------|----------------|------|
| 1 | `phase2_pilot_state.yaml` | SMOKE | `scaling-pilot-state` | Smoke all X0 families |
| 2 | `phase2_scout.yaml` | SCOUT | `scaling-phase2-scout` | Structure sizes x layouts x D |
| 3 | `phase2_claim.yaml` | CLAIM | `scaling-phase2-claim-plan` / `…-reseed` | Claim windows on structure scout |

### Phase 4: transfer (RQ4, Package D)

Purpose: repeat size and structure maps for required methods `kubo` and `fat` (beside baseline). Each method has its own scout then claim pair.

| Axis | Scout | Claim | Make pattern |
|------|-------|-------|--------------|
| Size | `phase4_{kubo,fat}_size_scout.yaml` | `phase4_{kubo,fat}_size_claim.yaml` | `scaling-transfer-size-scout` then claim-reseed; `TRANSFER_METHOD=kubo\|fat` |
| Structure | `phase4_{kubo,fat}_structure_scout.yaml` | `phase4_{kubo,fat}_structure_claim.yaml` | `scaling-transfer-structure-scout` then claim-reseed |
 
Size scouts `extends` Phase 1 scout; structure scouts `extends` Phase 2 scout. Claims set `upstream_protocol` to the matching scout id.

### Phase 5: information vs dogs (RQ5, Package E)

Purpose: change information `I` (observation, sensing range, communication) and see how control demand moves. **One campaign per axis** (do not mix ladders).

| Order | Scout | Claim | Notes |
|-------|-------|-------|-------|
| 1 | `phase5_factor_sweep.yaml` | `phase5_obs_claim.yaml` | Observation ladder; scout uses `runner: factor` |
| 2 | `phase5_range_scout.yaml` | `phase5_range_claim.yaml` | Sensing-range multiples; leave obs unset |
| 3 | `phase5_comm_scout.yaml` | `phase5_comm_claim.yaml` | Communication modes |

Make: `scaling-factor-sweep`, `scaling-phase5-*-scout`, `scaling-phase5-*-claim-*`.

### Phases without YAML here

| Phase | RQ / Package | How you run it |
|-------|--------------|----------------|
| 3 Mechanism | RQ3 / C | `scaling-analyse PACKAGE=C` on merged claim trials |
| 6 Fits | RQ6 / F | `scaling-analyse PACKAGE=F` on frontiers / merged trials |
| 7 Early warning | RQ7 / G | `scaling-analyse PACKAGE=G` (needs timeseries) |

## Author checklist (new or edited YAML)

1. Set `canonical:` to `scaling/configs/canonical_grid.yaml` (or a dated fork).
2. For every override (N, D, layouts, seeds, methods, ticks, factors), add a one-line WHY comment. "Faster" alone is not enough.
3. Set `grade: SMOKE | SCOUT | CLAIM`.
4. Set `output: scaling/results/phase{k}/{slug}/` matching `protocol_id`.
5. List `packages:` this run is meant to feed (A-G).
6. After a real run, log status in `progress_tracker.md`.
7. If you change a frozen Section 8 default, bump id in `canonical_grid.yaml` and update main plan Section 8.
8. Claim grids: use claim YAML + plan/reseed after a scout exists. Do not run a flat 100-seed full grid unless you intentionally accept draft-style cost.
9. Prefer `extends:` for method or grade overlays so the N/D grid stays in one place.
10. Claim / T1: set `upstream_protocol` to the scout (or claim) id. Optional `upstream_trials` (default `trials.csv`; T1 often `merged_trials.csv`).
11. T1: `phase1_t1.yaml` with `time_budget: t1`.
12. Phase 5: one axis per campaign; do not put `sensing_ranges` on the obs scout.
13. Entry: `uv run scaling/scripts/campaign.py <verb> --protocol <id>`.

### Template

```yaml
protocol_id: phaseK_short_name
phase: K
grade: SMOKE
output: scaling/results/phaseK/short_name
canonical: scaling/configs/canonical_grid.yaml
methods: [...]          # why these methods
layouts: [...]          # why these X0
flock_sizes: [...]      # why this N subset vs full freeze
shepherd_counts: [...]
seeds: N
seed_mode: scout        # or claim
store_timeseries: true
packages: [A]
# upstream_protocol: phaseK_scout   # claim / T1 only
```
