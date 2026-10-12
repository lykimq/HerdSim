# Protocols (`protocols/`)

This folder defines scaling campaigns: shared frozen defaults, per-phase protocol YAMLs, and end-of-trial packaging used while writing `trials.csv`. Execution lives under `cli/` and `services/`.

## Layout

```text
protocols/
|-- configs/             Canonical grid + protocol YAMLs
|   |-- canonical_grid.yaml
|   `-- protocols/       One YAML per phase / ladder stage
`-- packaging/           Failure labels, aggregates, provenance
```

## Phases and research questions

| Phase | RQ | Role | Protocol ids (under `configs/protocols/`) |
|-------|----|------|-------------------------------------------|
| 1 | RQ2 | Size / regime map (baseline `strombom_multi`) | `phase1_pilot`, `phase1_scout`, `phase1_claim`, `phase1_t1` |
| 2 | RQ1 | Structure at fixed N (layouts) | `phase2_pilot_state`, `phase2_scout`, `phase2_claim` |
| 3 | RQ3 | Mechanism contrasts | Analyse-only (uses T1 / overcrowding cells from phase 1 or 2) |
| 4 | RQ4 | Transfer across methods | `phase4_{kubo,fat}_{size,structure}_{scout,claim}` |
| 5 | RQ5 | Information ladders (obs / range / comm) | `phase5_factor_sweep`, `phase5_obs_claim`, `phase5_range_{scout,claim}`, `phase5_comm_{scout,claim}` |
| 6 | RQ6 | Scaling fits | Analyse-only on claim frontiers |
| 7 | RQ7 | Early warning | Analyse-only on claim timeseries |

Typical grade flow: scout map, then claim-plan / claim-reseed on selected windows. Phase 1 also has conditional T1 for overcrowding cells.

```bash
uv run cli/campaign.py help
uv run cli/campaign.py run --protocol phase1_scout --workers 18
uv run cli/campaign.py claim-plan --protocol phase1_claim
uv run cli/campaign.py claim-reseed --protocol phase1_claim --workers 18
```
