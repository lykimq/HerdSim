# Scaling progress tracker

Role: status (1 = code, 2 = experiment runs, then Claims)
Why / what: [herdsim_research_program.md](herdsim_research_program.md)
How: [main_scaling_plan.md](main_scaling_plan.md)
Findings: [final_report.md](final_report.md) ([HTML](final_report.html))
Help: `make -C scaling help` (wraps `scaling/scripts/campaign.py`)

Protocol: `scaling_v2`
Host: `gwen` (Intel Core Ultra 7 165H, 22 threads, 61 GiB RAM)
Workers: prefer `WORKERS=16` on AC (leave headroom; not all 22). Cap at 18 if the machine stays cool.
CPU: set governor to `performance` before long campaigns (see below).
Results: run data in `scaling/results/` (trials, packages) is kept in git; timeseries parquet files are ignored via `.gitignore`. Figures live under `scaling/docs/figures/`.

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

Default from repo root: `WORKERS=16` on this host (AC). Transfer examples use
`TRANSFER_METHOD=kubo` (repeat with `fat`).

Before a long scout or claim (once per boot, as root or with sudo):

```bash
for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance | sudo tee "$g" >/dev/null; done
```

Check: `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor` should print `performance`.
When finished or on battery, you can switch back to `powersave` the same way.

| # | Step | Grade | Command | Output | Status |
|---|------|-------|---------|--------|--------|
| 0 | Sanity tests | n/a | `make -C scaling scaling-test` | pytest | DONE |
| 1 | Phase 1 smoke | SMOKE | `make -C scaling scaling-pilot WORKERS=16` | `scaling/results/phase1/pilot/` | DONE |
| 2 | Phase 1 scout | SCOUT | `make -C scaling scaling-scout WORKERS=16` | `scaling/results/phase1/scout/` | DONE |
| 3 | Plan claim windows | n/a | `make -C scaling scaling-claim-plan` | `scaling/results/phase1/claim/boundary_cells.csv` | DONE |
| 4 | Phase 1 claim reseed | CLAIM | `make -C scaling scaling-claim-reseed WORKERS=16` | `scaling/results/phase1/claim/` | DONE |
| 5 | Analyse Package A and F on the merge | CLAIM | `make -C scaling scaling-analyse PACKAGE=A TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/a` | packages | DONE |
| 6 | Phase 1 T1 | CLAIM | `make -C scaling scaling-t1 WORKERS=16` | `scaling/results/phase1/t1/` | SKIPPED (0 overcrowding cells) |
| 7 | Phase 2 structure scout | SCOUT | `make -C scaling scaling-phase2-scout WORKERS=16` | `scaling/results/phase2/scout/` | DONE |
| 8 | Phase 2 claim | CLAIM | `make -C scaling scaling-phase2-claim-reseed WORKERS=16` | `scaling/results/phase2/claim/` | DONE |
| 9 | Phase 3 mechanism | CLAIM | `make -C scaling scaling-analyse PACKAGE=C TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/c` | Package C | SKIPPED (0 overcrowding cells in Phase 1) |
| 10 | Phase 6 fits | CLAIM | `make -C scaling scaling-analyse PACKAGE=F TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/f` | Package F | DONE |
| 11 | Phase 4 size (kubo then fat) | SCOUT then CLAIM | `make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo WORKERS=16` then claim-reseed; repeat `fat` | `scaling/results/phase4/` | DONE |
| 12 | Phase 4 structure (kubo then fat) | SCOUT then CLAIM | `make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo WORKERS=16` then claim-reseed; repeat `fat` | `scaling/results/phase4/` | DONE |
| 13 | Phase 4 transfer table | CLAIM | `make -C scaling scaling-analyse PACKAGE=D TRIALS=... --trials-by-method ...` | packages/d | DONE |
| 14 | Phase 5 obs scout/claim | SCOUT then CLAIM | `make -C scaling scaling-factor-sweep WORKERS=18` then `scaling-phase5-obs-claim-reseed` | `scaling/results/phase5/` | DONE |
| 15 | Phase 5 range | SCOUT then CLAIM | `scaling-phase5-range-scout WORKERS=18` then `scaling-phase5-range-claim-reseed` | `scaling/results/phase5/` | DONE |
| 16 | Phase 5 communication | SCOUT then CLAIM | `scaling-phase5-comm-scout WORKERS=18` then `scaling-phase5-comm-claim-reseed` | `scaling/results/phase5/` | DONE |
| 17 | Phase 7 early warning | CLAIM | `make -C scaling scaling-analyse PACKAGE=G TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/g` | Package G | DONE |

After step 2, if the bootstrap interval on D_min covers more than one grid step, raise that window to 200 seeds before the structure claim.

### After every run

1. Check `status.json` and `manifest.jsonl`.
2. Write `README.md` from the template into the protocol folder.
3. Set the checklist Status (`TODO` / `RUNNING` / `DONE` / `SKIPPED`).
4. If the grade is CLAIM, update Claims.

## Claims

Criteria: [main_scaling_plan.md](main_scaling_plan.md). Update after a claim-grade `README.md`.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C1a | REJECTED | Phase 2 Package B: D_min = 1 across all 4 layouts at N in {50, 100, 200} |
| C1b | INCONCLUSIVE | Phase 2 Package B: Cannot evaluate state predictor superiority when D_min does not shift |
| C2a | REJECTED | Phase 1 Package A: 0 overcrowding cells on strombom_multi at theta=0.90 |
| C2b | SKIPPED | Phase 1: No overcrowding cells to extend to T=20,000 |
| C3 | INCONCLUSIVE | Phase 1: Mechanism contrast undefined without overcrowding cells |
| C4 | SUPPORTED (partial) | Phase 4 Package D: size map shared for N>=25 (Strombom/Kubo); Kubo wide has no D_min; Kubo outlier_rich N=200 shifts to D_min=20 at 200 seeds (bootstrap [2, 20]; no overcrowding); FAT absent for N>=25 |
| C5a | REJECTED | Phase 5 Package E: no ladder step lowers a defined D_min by a grid step at N in {100, 200} (obs: bearing hard-fails; local/global D_min=1; range and comm flat D_min=1) |
| C5b | INCONCLUSIVE | Phase 5 Package E: no first-step dog saving to test diminishing returns (median_first_step_delta=0 on all ladders) |
| C6a | SUPPORTED | Phase 1/6 Package F: leave-one-N RMSE power 0.247 > piecewise 0.132 (power worse than piecewise) |
| C6b | SUPPORTED | Phase 1/6 Package F: on compact N in {25..400}, D_min=1 flat so log-log slope = 0 (< 1); power fit log_log_slope = -0.165 |
| C7a | INCONCLUSIVE | Phase 7 Package G: held-out state and (N, D) AUROC null; folds empty; beats_nd_baseline=False |
| C7b | REJECTED | Phase 7 Package G: frac_lead_ge_500=0.083 (<0.30); 14/169 failures have measured lead time |
