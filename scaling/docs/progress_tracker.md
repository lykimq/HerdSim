# Scaling progress tracker

Role: status (1 = code, 2 = experiment runs, then Claims)
Why / what: [herdsim_research_program.md](herdsim_research_program.md)
How: [main_scaling_plan.md](main_scaling_plan.md)
Run strategy (pilot / scout / plan / reseed): [experiment_run_strategy.md](experiment_run_strategy.md)
Report form: [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)
Help: `make -C scaling help` (wraps `scaling/scripts/campaign.py`)

Protocol: `scaling_v2`
Host: `gwen` (prefer `WORKERS=8`, up to 12-16 if plugged in)
Results: `scaling/results/` is gitignored.

How to read this file:
- Section 1 = is the code ready?
- Section 2 = have the experiments been run?
- Code DONE does not mean the experiment ran.

## 1. Implementation (code only)

| Phase | RQ | Package | Code status | In the tree | Still missing |
|-------|----|---------|-------------|-------------|---------------|
| 0 | S8 | all | DONE | `canonical_grid.yaml` (`scaling_v2`) | nothing |
| 1 | RQ2 | A | DONE | pilot, scout, claim windows, merge, bootstrap, T1 | nothing |
| 2 | RQ1 | B | DONE | smoke, structure scout, structure claim | nothing |
| 3 | RQ3 | C | DONE | Package C (within-N tests) | needs Phase 1-2 data |
| 4 | RQ4 | D | DONE | Package D; kubo/fat size and structure scout+claim YAMLs | nothing |
| 5 | RQ5 | E | DONE | obs/range/comm scout and claim protocols | nothing |
| 6 | RQ6 | F | DONE | Package F (leave-one-N-out RMSE) | needs frontiers |
| 7 | RQ7 | G | DONE | Package G (causal window, lead time) | needs timeseries |

E1 intended velocities: not built. Add only if a claim-grade map shows I_dir spikes only at walls.

### Optional later

| Next | Add | Blocks | Status |
|------|-----|--------|--------|
| F | E1 intended velocities | C3 robustness | SKIP unless needed |

All Section 2 experiment steps can run with the current code. No campaign YAML is missing.

## 2. Experiment runs

Default from repo root. Example: `WORKERS=8`. Transfer examples use `TRANSFER_METHOD=kubo` (repeat with `fat`).

| # | Step | Grade | Command | Output | Status |
|---|------|-------|---------|--------|--------|
| 0 | Sanity tests | n/a | `make -C scaling scaling-test` | pytest | TODO |
| 1 | Phase 1 smoke | SMOKE | `make -C scaling scaling-pilot WORKERS=8` | `scaling/results/phase1/pilot/` | TODO |
| 2 | Phase 1 scout | SCOUT | `make -C scaling scaling-scout WORKERS=8` | `scaling/results/phase1/scout/` | TODO |
| 3 | Plan claim windows | n/a | `make -C scaling scaling-claim-plan` | `scaling/results/phase1/claim/boundary_cells.csv` | TODO |
| 4 | Phase 1 claim reseed | CLAIM | `make -C scaling scaling-claim-reseed WORKERS=8` | `scaling/results/phase1/claim/` | TODO |
| 5 | Analyse Package A and F on the merge | CLAIM | `make -C scaling scaling-analyse PACKAGE=A TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/a` | packages | TODO |
| 6 | Phase 1 T1 | CLAIM | `make -C scaling scaling-t1 WORKERS=8` | `scaling/results/phase1/t1/` | TODO |
| 7 | Phase 2 structure scout | SCOUT | `make -C scaling scaling-phase2-scout WORKERS=8` | `scaling/results/phase2/scout/` | TODO |
| 8 | Phase 2 claim | CLAIM | `make -C scaling scaling-phase2-claim-reseed WORKERS=8` | `scaling/results/phase2/claim/` | TODO |
| 9 | Phase 3 mechanism | CLAIM | `make -C scaling scaling-analyse PACKAGE=C TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/c` | Package C | BLOCKED on steps 4-5 |
| 10 | Phase 6 fits | CLAIM | `make -C scaling scaling-analyse PACKAGE=F TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/f` | Package F | BLOCKED on step 5 |
| 11 | Phase 4 size (kubo then fat) | SCOUT then CLAIM | `make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo WORKERS=8` then claim-reseed; repeat `fat` | `scaling/results/phase4/` | TODO |
| 12 | Phase 4 structure (kubo then fat) | SCOUT then CLAIM | `make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo WORKERS=8` then claim-reseed; repeat `fat` | `scaling/results/phase4/` | TODO |
| 13 | Phase 4 transfer table | CLAIM | `make -C scaling scaling-analyse PACKAGE=D TRIALS=... --trials-by-method ...` | packages/d | BLOCKED on 11-12 |
| 14 | Phase 5 obs scout/claim | SCOUT then CLAIM | `make -C scaling scaling-factor-sweep` then `scaling-phase5-obs-claim-reseed` | `scaling/results/phase5/` | TODO |
| 15 | Phase 5 range | SCOUT then CLAIM | `scaling-phase5-range-scout` then `scaling-phase5-range-claim-reseed` | `scaling/results/phase5/` | TODO |
| 16 | Phase 5 communication | SCOUT then CLAIM | `scaling-phase5-comm-scout` then `scaling-phase5-comm-claim-reseed` | `scaling/results/phase5/` | TODO |
| 17 | Phase 7 early warning | CLAIM | `make -C scaling scaling-analyse PACKAGE=G TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/g` | Package G | BLOCKED on steps 4-8 |

After step 2, if the bootstrap interval on D_min covers more than one grid step, raise that window to 200 seeds before the structure claim.

### After every run

1. Check `status.json` and `manifest.jsonl`.
2. Write `REPORT.md` from the template into the protocol folder.
3. Set the checklist Status (`TODO` / `RUNNING` / `DONE` / `SKIPPED`).
4. If the grade is CLAIM, update Claims.

## Claims

Criteria: [main_scaling_plan.md](main_scaling_plan.md). Update after a claim-grade `REPORT.md`.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C1a | UNEVALUATED | |
| C1b | UNEVALUATED | |
| C2a | UNEVALUATED | |
| C2b | UNEVALUATED | |
| C3 | UNEVALUATED | |
| C4 | UNEVALUATED | |
| C5a | UNEVALUATED | |
| C5b | UNEVALUATED | |
| C6a | UNEVALUATED | |
| C6b | UNEVALUATED | |
| C7a | UNEVALUATED | |
| C7b | UNEVALUATED | |
