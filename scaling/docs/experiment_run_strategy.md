# Experiment run strategy

Protocol: `scaling_v2`.

This file is the operator narrative for **how and why** we stage simulation campaigns.
Frozen science rules (grids, frontiers, claims) live in [main_scaling_plan.md](main_scaling_plan.md).
YAML and make wiring live in [configs/protocols/README.md](../configs/protocols/README.md).
Run checklist lives in [progress_tracker.md](progress_tracker.md).

## Why stage runs instead of one full Phase 1

A claim-grade map needs precise success rates near frontiers (`D_min`, overcrowding). Running **every** `(N, D)` cell at 100 seeds is far more expensive than we need: interior cells that always succeed or always fail teach little at that depth.

The staged pipeline spends cheap seeds everywhere, learns which cells matter, then spends expensive seeds only on those cells. Same pattern applies to structure, transfer, and information ladders (Phase 2 / 4 / 5).

Rough Phase 1 size map (planning order of magnitude; recompute after scout):

- Scout: full frozen grid at 30 seeds (about 3,000 trials).
- Claim: up to about six `D` per `N` at 100 seeds (about 6,000 more).
- T1: long horizon only on overcrowding cells (extra cost per trial).

One flat 100-seed full grid would buy little extra science on obvious cells and burn the budget before structure and transfer runs.

## Grades (what you may cite)

| Grade | Role | Typical seeds | Cite for claims? |
|-------|------|---------------|------------------|
| SMOKE | Pipeline check (paths, resume, metrics) | tiny grid | No |
| SCOUT | Broad map; choose windows | 30 (`scout_seeds`) | No (planning / diagnostics only) |
| CLAIM | Precision on planned cells | 100 (`claim_grade_seeds`) | Yes, after REPORT.md |

Record the grade on every run report ([REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)). Do not promote a SCOUT figure to a Claim verdict.

## Verbs (make / campaign)

| Verb | What it does | Typical make target |
|------|--------------|---------------------|
| Pilot | SMOKE run; reduced grid | `scaling-pilot` |
| Scout | Full (or factor) grid at scout depth | `scaling-scout`, `scaling-phase2-scout`, ...|
| Claim plan | **No** new sims; write which cells to reseed | `scaling-claim-plan` |
| Claim reseed | Run planned cells at claim depth; merge | `scaling-claim-reseed` |
| Analyse | Build packages / figures from trials CSV | `scaling-analyse PACKAGE=...` |
| T1 | Claim-depth runs at `time_limit_t1` (20,000) on overcrowding cells | `scaling-t1` |

Help: `make -C scaling help` (wraps `scaling/scripts/campaign.py`).

## What each step produces and who consumes it

Example paths are Phase 1; other phases mirror under `scaling/results/phase{k}/…`.

| Step | Writes (main) | Used for |
|------|---------------|----------|
| Pilot | `phase1/pilot/trials.csv`, `status.json` | Confirm the host and code path |
| Scout | `phase1/scout/trials.csv`, timeseries if enabled | Reliability map; input to claim plan and early diagnostics |
| Claim plan | `phase1/claim/boundary_cells.csv` | Exact `(N, D[, layout, ...])` list for reseed |
| Claim reseed | `phase1/claim/trials.csv`, **`merged_trials.csv`** | Claim-grade frontiers, regimes, Packages A/C/F/G inputs |
| Analyse | `packages/{a,c,...}/` figures and tables | REPORT.md and Claims table |
| T1 | `phase1/t1/` | Overcrowding under the long time budget |

Merge rule (also in the main plan): on a cell that received claim seeds, analysis uses those claim rows only. Other cells keep scout rows. Scout and claim rows are not stacked on the same cell.

`upstream_protocol` on claim / T1 YAMLs points at the scout (or claim merge) whose `trials.csv` / `merged_trials.csv` feed planning.

## Claim windows (what “plan” selects)

Per (method, layout, N), after scout (see main plan, Claim-grade map):

1. Reliability window: scout `D_min`, plus previous and next grid `D`.
2. Overcrowding window (only if two consecutive `D` after that candidate stay below theta): those two `D`  and the last `D` still at or above theta.
3. If no `D` meets theta: the two largest tested `D`.

If the bootstrap CI on `D_min` spans more than one grid step, raise that window to 200 seeds before the structure claim.

## Same pattern on later phases

| Phase | Scout answers | Claim spends seeds on |
|-------|---------------|------------------------|
| 1 Size (RQ2) | Where does `R(N, D)` live? | Frontiers and hard failures |
| 2 Structure (RQ1) | How does `X0` move `D_min`? | Structure windows at {50, 100, 200} |
| 4 Transfer (RQ4) | Same maps for kubo / fat | Same window logic per method |
| 5 Information (RQ5) | Obs / range / comm ladders | Windows on each ladder |
| 3, 6, 7 | (mostly analyse) | Need merged claim trials / timeseries from above |

Phase 3 (mechanism), 6 (fits), and 7 (early warning) are mainly **analyse** packages on data you already collected. They stay blocked until the matching claim merge (and timeseries, for G) exists.

## Practical order (Phase 1)

1. `scaling-test` (cheap correctness).
2. Pilot (SMOKE).
3. Scout (SCOUT); inspect `status.json` / reliability.
4. Claim plan (no sims).
5. Claim reseed (CLAIM); confirm `merged_trials.csv`.
6. Analyse Package A (and F when ready).
7. T1 if overcrowding cells exist.
8. Only then promote Claims in the tracker.

Stop after scout if the map is broken, the grid must change, or the bootstrap interval is too wide. Fix the protocol, then continue. That is the point of staging.
