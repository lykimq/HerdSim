# Scaling progress tracker

Role: status (1 = code, 2 = experiment runs, then Claims)
Why / what: [herdsim_research_program.md](herdsim_research_program.md)
How: [main_scaling_plan.md](main_scaling_plan.md)
Report form: [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)
Help: `make -C scaling help`

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
| 1 | RQ2 | A | DONE | pilot, full scout, claim windows, merge, bootstrap | T1 protocol (`max_ticks=20000` on overcrowding D) |
| 2 | RQ1 | B | PARTIAL | smoke `phase2_pilot_state.yaml`; Package B | `phase2_claim.yaml` for N={50,100,200}, 4 X0, full D |
| 3 | RQ3 | C | DONE | Package C (within-N tests) | needs Phase 1-2 data |
| 4 | RQ4 | D | PARTIAL | Package D transfer table | claim YAMLs for `kubo` and `fat` (size and structure) |
| 5 | RQ5 | E | PARTIAL | scout `phase5_factor_sweep.yaml` (obs ladder, N={100,200}, 30 seeds) | claim protocol; range and communication campaigns |
| 6 | RQ6 | F | DONE | Package F (leave-one-N-out RMSE) | needs frontiers |
| 7 | RQ7 | G | DONE | Package G (causal window, lead time) | needs timeseries |

E1 intended velocities: not built. Add only if a claim-grade map shows I_dir spikes only at walls.

### Code still to add

| Next | Add | Blocks | Status |
|------|-----|--------|--------|
| B | `phase1_t1.yaml` + `make scaling-t1` on overcrowding D, `max_ticks=20000` | C2b | TODO |
| C | `phase2_claim.yaml` + `make scaling-phase2-claim` | C1a, C1b | TODO |
| D | Claim protocols for `kubo` and `fat` (size map and structure contrast) | C4 | TODO |
| E | `phase5_claim.yaml` plus range and communication ladders | C5a, C5b | TODO |
| F | E1 intended velocities | C3 robustness | SKIP unless needed |

Section 2 steps 0-5 can run with the current code.

## 2. Experiment runs

Default from repo root. Example: `WORKERS=8`.

| # | Step | Grade | Command | Output | Status |
|---|------|-------|---------|--------|--------|
| 0 | Sanity tests | n/a | `make -C scaling scaling-test` | pytest | TODO |
| 1 | Phase 1 smoke | SMOKE | `make -C scaling scaling-pilot WORKERS=4` | `scaling/results/phase1/pilot/` | TODO |
| 2 | Phase 1 scout | SCOUT | `make -C scaling scaling-scout WORKERS=8` | `scaling/results/phase1/scout/` | TODO |
| 3 | Plan claim windows | n/a | `make -C scaling scaling-claim-plan` | `scaling/results/phase1/claim/boundary_cells.csv` | TODO |
| 4 | Phase 1 claim reseed | CLAIM | `make -C scaling scaling-claim-reseed WORKERS=8` | `scaling/results/phase1/claim/` | TODO |
| 5 | Analyse Package A and F on the merge | CLAIM | `make -C scaling scaling-analyse PACKAGE=A TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/a` | packages | TODO |
| 6 | Phase 1 T1 | CLAIM | needs code item B | `scaling/results/phase1/t1/` | BLOCKED on code B |
| 7 | Phase 2 claim | CLAIM | needs code item C | `scaling/results/phase2/claim/` | BLOCKED on code C |
| 8 | Phase 3 mechanism | CLAIM | `make -C scaling scaling-analyse PACKAGE=C TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/c` | Package C | BLOCKED on steps 4-5 |
| 9 | Phase 6 fits | CLAIM | `make -C scaling scaling-analyse PACKAGE=F TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/f` | Package F | BLOCKED on step 5 |
| 10 | Phase 4 transfer | CLAIM | needs code item D | packages/d | BLOCKED on code D |
| 11 | Phase 5 ladders | SCOUT then CLAIM | scout: `make -C scaling scaling-factor-sweep WORKERS=8` | `scaling/results/phase5/` | TODO for scout; claim BLOCKED on code E |
| 12 | Phase 7 early warning | CLAIM | `make -C scaling scaling-analyse PACKAGE=G TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/g` | Package G | BLOCKED on steps 4-8 |

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
