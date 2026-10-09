# Run guide

Run commands from `/home/gwen/HerdSim`. The Makefile sets `PYTHONPATH` and wraps `scaling/scripts/campaign.py`.

## Inspect and test

```bash
make -C scaling help
uv run scaling/scripts/campaign.py help
make -C scaling scaling-test
```

The correctness target runs:

```bash
uv run pytest tests/backend/correctness/test_scaling_stack.py -q
```

Default worker count is 18 for the host documented by `scaling/Makefile`. Override it on smaller machines, for example `WORKERS=4`.

## Phase 1: baseline size

```bash
make -C scaling scaling-pilot
make -C scaling scaling-scout
make -C scaling scaling-claim-plan
make -C scaling scaling-claim-reseed
make -C scaling scaling-t1-plan
make -C scaling scaling-t1
```

Use this order. Pilot is a smoke check. Scout maps the full grid. Claim planning writes cell selections but runs no simulations. Claim reseed executes those cells and creates the merged claim dataset. T1 planning and execution are conditional on detected overcrowding.

The completed baseline map had no overcrowding cells, so Phase 1 T1 was not run. Do not run T1 merely to fill the directory unless the protocol's planner identifies cells.

## Phase 2: initial structure

```bash
make -C scaling scaling-pilot-state
make -C scaling scaling-phase2-scout
make -C scaling scaling-phase2-claim-plan
make -C scaling scaling-phase2-claim-reseed
```

Each layout and N receives its own frontier window.

## Phase 4: transfer controllers

Run size and structure campaigns separately for Kubo and FAT:

```bash
make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-size-claim-plan TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-size-claim-reseed TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-claim-plan TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-claim-reseed TRANSFER_METHOD=kubo
```

Repeat with `TRANSFER_METHOD=fat`. Package D is compiled jointly after the required maps exist.

## Phase 5: information ladders

Observation:

```bash
make -C scaling scaling-factor-sweep
make -C scaling scaling-phase5-obs-claim-plan
make -C scaling scaling-phase5-obs-claim-reseed
```

Sensing range:

```bash
make -C scaling scaling-phase5-range-scout
make -C scaling scaling-phase5-range-claim-plan
make -C scaling scaling-phase5-range-claim-reseed
```

Communication:

```bash
make -C scaling scaling-phase5-comm-scout
make -C scaling scaling-phase5-comm-claim-plan
make -C scaling scaling-phase5-comm-claim-reseed
```

These ladders are separate campaigns, not a Cartesian product.

## Direct campaign commands

The general form is:

```bash
uv run scaling/scripts/campaign.py VERB --protocol PROTOCOL_ID [OPTIONS]
```

Verbs are `run`, `claim-plan`, `claim-reseed`, `t1-plan`, and `t1`. A protocol identifier resolves under `scaling/configs/protocols/`.

Examples:

```bash
uv run scaling/scripts/campaign.py run --protocol phase1_scout --workers 8
uv run scaling/scripts/campaign.py claim-plan --protocol phase1_claim
uv run scaling/scripts/campaign.py claim-reseed --protocol phase1_claim --workers 8
```

Useful options include `--output`, `--workers`, `--upstream-trials`, `--methods`, `--layouts`, `--n`, `--d`, `--seeds`, `--max-ticks`, `--no-timeseries`, and `--no-resume`.

Make variables map to the common filters:

```bash
make -C scaling scaling-scout WORKERS=4 SCALING_N=100 SCALING_D=1 SCALING_SEEDS=2
```

Filters and seed overrides are useful for diagnostics. A filtered run is not the complete frozen campaign and must not be presented as one.

## Resume

Resume is enabled by default. Re-run the same command against the same output directory. The runner reads `manifest.jsonl` and skips trial keys whose status is `ok`. Trial keys include N, D, seed, layout, method, and any observation, range, or communication factor.

```bash
make -C scaling scaling-scout
```

Inspect `status.json` before and after resuming. It records planned, completed, pending-at-start, running, and timestamp fields. Avoid `--no-resume` unless a deliberate fresh execution is required, because it disables completed-key skipping.

## Outputs

A protocol output directory normally contains:

| Artifact | Meaning |
|---|---|
| `protocol.yaml` | Resolved recipe copied for the run |
| `provenance.json` | Protocol stamp, seed list, code and host metadata, metric identifiers, and timestamps |
| `manifest.jsonl` | Resume ledger; successful trial keys have `status=ok` |
| `status.json` | Planned and completed counts plus run timestamps |
| `trials.csv` | One row per simulation |
| `boundary_cells.csv` | Claim-plan selection, when applicable |
| `merged_trials.csv` | Claim rows replacing scout rows on reseeded cells |
| `timeseries/*.parquet` | Per-trial trajectories when enabled |
| `packages/` | Exported tables and figures |
| `README.md` | Human run note and links |

Typical locations are:

```text
scaling/results/phase1/pilot/
scaling/results/phase1/scout/
scaling/results/phase1/claim/
scaling/results/phase1/t1/
scaling/results/phase2/{pilot_state,scout,claim}/
scaling/results/phase4/{kubo,fat}_{size,structure}/{scout,claim}/
scaling/results/phase5/
```

## Provenance and interpretation

Before citing a result:

1. Confirm `status.json` reports completion.
2. Confirm the copied `protocol.yaml` has the expected protocol, grade, factors, and seed count.
3. Retain `provenance.json` and `manifest.jsonl`.
4. Use `merged_trials.csv` for claim analysis, not a manual concatenation.
5. Confirm the report labels the evidence CLAIM.
6. Treat D = 35 as a grid ceiling when D_overcrowd is empty.
7. Record a skipped conditional phase explicitly, including its trigger.

Scout figures may guide planning but cannot promote a claim. A protocol folder is the provenance unit: its resolved recipe and machine records take precedence over a generic example in prose.
