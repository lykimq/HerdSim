# Shepherding-budget progress tracker

Status: living document (update after each campaign or Cap change)  
Last updated: 2026-09-17 (after stopped `phase1_scout`)

This file tracks **plan coverage**, **implementation**, and **experimental results** for the shepherding-budget program. It does not replace the scientific source of truth.

| Document | Role |
|----------|------|
| [herdsim_research_program.md](herdsim_research_program.md) | Parent framing (size, structure, mechanism, transfer) |
| [main_shepherding_budget_plan.md](main_shepherding_budget_plan.md) | Single source of truth (RQs, claims, phases, Caps, Section 8) |
| This file | Execution ledger: what is built, what ran, what claims are evaluable |
| [results/budget/README.md](../../../results/budget/README.md) | Results directory index by phase |
| [results/budget/phase1/REPORT.md](../../../results/budget/phase1/REPORT.md) | Phase-1 rollup |
| [results/budget/phase1/scout/REPORT.md](../../../results/budget/phase1/scout/REPORT.md) | Phase-1 scout (stopped early) |
| [results/budget/phase1/pilot/REPORT.md](../../../results/budget/phase1/pilot/REPORT.md) | Phase-1 smoke pilot |

How to use: after a run or Cap change, update Sections 2-6 and append a row to Section 7. Keep verdicts honest (pilot/scout != claim-grade).

---

## 1. Status legend

| Tag | Meaning |
|-----|---------|
| NOT STARTED | No work yet |
| BUILT | Code exists and is unit-tested; not yet used for claim evaluation |
| SMOKE | Exercised on a reduced grid; pipeline works; not claim-grade |
| IN PROGRESS | Scout or claim campaign running / partial |
| DONE | Phase "done when" met, or claim decided (support / reject / inconclusive domain) |
| BLOCKED | Waiting on a dependency (data, Cap, or harder grid) |

Claim verdicts (only when claim-grade evidence exists):

| Verdict | Meaning |
|---------|---------|
| UNEVALUATED | Insufficient evidence |
| SUPPORTED | Claim criteria met |
| REJECTED | Claim criteria failed in the stated domain |
| INCONCLUSIVE | Ran claim-grade protocol; result ambiguous |

---

## 2. Phase checklist (main plan Section 9)

Minimum publishable scientific unit: **RQ1 + RQ2 + RQ3 + S8**.

| Phase | Focus | RQ | Package | Status | Done when (plan) | Current evidence |
|-------|-------|----|---------|--------|------------------|------------------|
| 0 | Freeze protocol | -- | Section 8 | DONE | All Section 8 rows frozen | Frozen 2026-09-17; `shepherding_budget_v1` |
| 1 | Herdability maps (baseline) | RQ2 (+ data for RQ6) | A | IN PROGRESS | C2 evaluable on baseline; frontier+regimes exported | Pilot + partial scout; R=1 on completed compact cells; C2 still unevaluable |
| 2 | Collective-state manipulation | RQ1 | B | NOT STARTED | C1a/C1b evaluable; X0 families verified | `budget-pilot-state` not run |
| 3 | Overcrowding mechanism | RQ3 | C | NOT STARTED | C3 evaluable; I_dir/C series stored | Needs overcrowding cells from Phase 1 |
| 4 | Cross-method transfer | RQ4 | D | NOT STARTED | Transfer table for >= 3 methods | -- |
| 5 | Information substitution | RQ5 | E | NOT STARTED | C5a/C5b evaluable | -- |
| 6 | Scaling regimes | RQ6 | F | SMOKE | C6a or C6b decided | Pilot + partial scout: flat D_min=1 |
| 7 | Early warning | RQ7 | G | NOT STARTED | C7a/C7b evaluable | -- |

### Map from research-program progression

| Research program step | Main-plan phases / RQs | Status |
|-----------------------|------------------------|--------|
| 1. Size scaling `D_min(N)` | Phase 1 + Phase 6 (RQ2 data, RQ6) | IN PROGRESS (compact still flat) |
| 2. Structure `D_min(N, X)` | Phase 2 (RQ1) | NOT STARTED |
| 3. Mechanism | Phase 3 (RQ3) | NOT STARTED |
| 4. Method transfer | Phase 4 (RQ4) | NOT STARTED |
| 5. Information / time | Phase 5 (RQ5); T0/T1 in protocol | NOT STARTED |
| 6. Early warning / generality | Phase 7 (RQ7); later extensions | NOT STARTED |

---

## 3. Research questions and claims

| RQ | Question (short) | Package | Claims | Status | Result note |
|----|------------------|---------|--------|--------|-------------|
| RQ1 | State beyond N? | B | C1a, C1b | NOT STARTED | Need multi-X0 campaign |
| RQ2 | Boundary and regimes? | A | C2a, C2b | IN PROGRESS | Scout partial: R=1 through N=100 (+ partial 150); no overcrowding; C2 unevaluable |
| RQ3 | Why diminishing returns? | C | C3 | BLOCKED | Needs overcrowding / efficient contrast cells |
| RQ4 | Cross-method generality? | D | C4 | NOT STARTED | Baseline instrument only so far |
| RQ5 | Information vs shepherds? | E | C5a, C5b | NOT STARTED | -- |
| RQ6 | Scaling with N and state? | F | C6a, C6b | SMOKE | Constant D_min=1 on completed compact N; not publishable |
| RQ7 | Early warning of failure? | G | C7a, C7b | NOT STARTED | -- |
| S8 | Reproducible protocol | all | (infra) | DONE | Config + provenance path in place |

### Claim detail

| Claim | Criterion (short) | Verdict | Evidence pointer |
|-------|-------------------|---------|------------------|
| C1a | D_min differs by >= 2 across X0 at some N | UNEVALUATED | -- |
| C1b | State features beat (N, D) predictors (dAIC > 4) | UNEVALUATED | -- |
| C2a | Overcrowding for >= 2 methods at theta=0.90 | UNEVALUATED | Compact scout (1 method, partial): no overcrowding |
| C2b | Hard ceiling: R < theta at T1=20000 past D_overcrowd | UNEVALUATED | -- |
| C3 | Overcrowding cells higher I_dir and/or fragmentation | UNEVALUATED | -- |
| C4 | Shared mechanism label across >= 3 methods | UNEVALUATED | -- |
| C5a | Info step reduces D_min by >= 1 at N in {100,200} | UNEVALUATED | -- |
| C5b | Second info step saves fewer shepherds than first | UNEVALUATED | -- |
| C6a | Global power law rejected vs piecewise/state (dAIC > 10) | UNEVALUATED | Flat D_min; AIC comparison degenerate |
| C6b | Stable sublinear alpha < 1 in a stated domain | UNEVALUATED | Alpha effectively 0 on flat D_min |
| C7a | State warning AUROC > (N, D) baseline | UNEVALUATED | -- |
| C7b | Lead time >= 500 ticks on >= 30% failure trajectories | UNEVALUATED | -- |

---

## 4. Implementation Caps (main plan Section 10.1)

| Cap | Capability | Code | Built? | Used in a campaign? | Notes |
|-----|------------|------|--------|---------------------|-------|
| I1 | Grid runner + provenance | `api/budget_runner.py`, `analysis/budget/provenance.py` | yes | IN PROGRESS | Pilot + partial scout; `trials.csv` only flushed at end (kill required timeseries rebuild) |
| I2 | Frontier extraction | `analysis/budget/frontier.py` | yes | IN PROGRESS | `phase1/scout/package_a/frontier.csv` |
| I3 | Regime labelling | `analysis/budget/regimes.py` | yes | IN PROGRESS | `phase1/scout/package_a/regimes.csv` |
| I4 | Mean-spread, extent | `metrics/mean_spread.py`, `metrics/extent.py` | yes | IN PROGRESS | Timeseries columns |
| I5 | X0 generators + wiring | `core/x0_generators.py`, `scenarios/drive_to_goal.py` | yes | no | Awaiting Package B run |
| I6 | State vs (N, D) predictors | `analysis/budget/predictors.py` | yes | no | Needs Package B |
| I7 | I_dir, coverage metrics | `metrics/shepherd_interference.py`, `metrics/shepherd_coverage.py` | yes | SMOKE | Present in scout timeseries; not claim-tested |
| I8 | Mechanism tests | `analysis/budget/mechanism.py` | yes | no | Phase 3 |
| I9 | Transfer table | `analysis/budget/transfer.py` | yes | no | Phase 4 |
| I10 | Factor sweep + substitution | `scripts/budget/run_factor_sweep.py`, `analysis/budget/substitution.py` | yes | no | Phase 5 |
| I11 | Scaling fits | `analysis/budget/scaling.py` | yes | IN PROGRESS | `phase1/scout/package_f/scaling_fits.csv` |
| I12 | Early warning | `analysis/budget/early_warning.py` | yes | no | Phase 7 |
| I13 | Canonical protocol + dossier | `configs/budget/canonical_grid.yaml`, `analysis/budget/export.py` | yes | IN PROGRESS | Phase-1 exports |
| I14 | Timeseries Parquet | `api/budget_runner.py` | yes | IN PROGRESS | `results/budget/phase1/scout/timeseries/` (1123 files) |

Operator entry points: `make budget-help`, `budget-test`, `budget-pilot`, `budget-pilot-state`, `budget-analyse`, `budget-scout`.

Results layout: `results/budget/phase<N>/<campaign>/` with per-campaign `REPORT.md` and phase rollup `REPORT.md`.

Tests: `make budget-test` (12 passed as of pilot date).

---

## 5. Protocol coverage vs Section 8 freeze

| Item | Frozen default | Latest scout (partial) | Gap |
|------|----------------|------------------------|-----|
| Task | `drive_to_goal` | same | none |
| Instrument | `strombom_multi` (+ transfer set later) | baseline only | transfer methods unused |
| Theta | 0.90 (also 0.50, 0.70) | 0.90 only | sensitivity not reported |
| N | {25,50,75,100,150,200,300,400} | 25..100 complete; 150 partial; 200 not started | finish 150/200; still missing 300/400 |
| D | {1,2,3,4,6,10,15,20,25,35} | through 20 for N<=100; N=150 missing D=15/20 (and part of D=10) | D=25/35 unused |
| X0 | compact, wide, split, outlier_rich | compact only | Package B not run |
| T0 | 10000 | 10000 | none for scout |
| T1 | 20000 (C2b) | not used | -- |
| Scout seeds | 30 | 30 on completed cells | remaining cells unfinished |
| Claim seeds | 100 on boundary | not used | -- |
| Master seed | 2026 | 2026..2055 (30 seeds) | ok |

---

## 6. Latest experimental results summary

### Campaign: `phase1_scout` (2026-09-17) — STOPPED

| Field | Value |
|-------|-------|
| Grade | SCOUT incomplete (operator stop) |
| Planned grid | 6 N x 8 D x 30 seeds x compact x strombom_multi = 1440 |
| Completed | **1123/1440 (78%)** before stop |
| Wall time | ~2h 8m (`WORKERS=4`) |
| Success on completed | 1123/1123 (R=1.0 all completed cells) |
| Artefacts | `results/budget/phase1/scout/` (trials reconstructed from timeseries; package_a; package_f; REPORT.md) |

Coverage: N in {25,50,75,100} full; N=150 at 163/240 (no D=15/20); N=200 at 0/240.

Frontier: D_min=1 for all completed N; no overcrowding; B*_D=1.

Regimes: 5 efficient_operation; 33 wasteful_overspend; 0 failure/overcrowding labels.

Scaling: best model constant (c=1); degenerate.

**Why slow:** not because every trial hit T0=10000. Median ticks stayed ~120–150 through N=100, but N=150 developed a heavy tail (max 7786 ticks on a *successful* trial). The longest ~10% of trials consumed ~33% of simulated ticks. Combined with 16x more cells than the pilot and Parquet I/O, wall time grew steeply once N=150 started.

Scientific reading: compact + strombom_multi remains easy through the completed band. Do not cite for C2/C6. Full narrative: [scout/REPORT.md](../../../results/budget/phase1/scout/REPORT.md).

### Campaign: `budget_pilot` (2026-09-17)

| Field | Value |
|-------|-------|
| Grade | SMOKE |
| Grid | 90 trials (N={25,50,100}, D through 10, 5 seeds, T=3000) |
| Wall time | ~8.3 min |
| Success | 90/90 |
| Artefacts | `results/budget/phase1/pilot/` |

Same qualitative picture as scout on the overlapping band. Report: [pilot/REPORT.md](../../../results/budget/phase1/pilot/REPORT.md).

---

## 6.1 Reproduce and resume commands

Run from the repo root (`/path/to/HerdSim`). Keep `results/budget/phase1/scout/` intact when moving machines
(at minimum `manifest.jsonl` + `trials.csv`; timeseries optional for analyse, required only if you must rebuild trials again).

### Resume Phase-1 scout (remaining ~317 cells)

Resume skips keys already listed as `ok` in `manifest.jsonl`, then rewrites Packages A and F.

```bash
# On a stronger machine, raise WORKERS (e.g. 8 or 16). Do not pass --no-resume.
make budget-scout WORKERS=16

# Equivalent explicit form (same defaults as Makefile):
make budget-scout \
  WORKERS=16 \
  SCOUT_OUT=results/budget/phase1/scout \
  SCOUT_CAMPAIGN_ID=phase1_scout \
  SCOUT_LAYOUT=compact \
  SCOUT_N="25 50 75 100 150 200" \
  SCOUT_D="1 2 3 4 6 10 15 20" \
  SCOUT_SEEDS=30 \
  BUDGET_INSTRUMENT=strombom_multi
```

Notes:

- Leave `BUDGET_MAX_TICKS` unset so protocol `T0=10000` is used.
- Do **not** delete `manifest.jsonl` or you will rerun all 1440 cells.
- After a clean finish, `trials.csv` is rewritten with all completed rows and Packages A/F are regenerated automatically by `budget-scout`.

### Re-analyse only (reproduce Package A/F from existing `trials.csv`)

Use this if the grid is already finished (or you only want to refresh exports / report tables):

```bash
make budget-analyse \
  PACKAGE=A \
  TRIALS=results/budget/phase1/scout/trials.csv \
  OUT=results/budget/phase1/scout/package_a

make budget-analyse \
  PACKAGE=F \
  TRIALS=results/budget/phase1/scout/trials.csv \
  OUT=results/budget/phase1/scout/package_f
```

Report narrative to refresh after a successful full scout: `results/budget/phase1/scout/REPORT.md`
and the phase rollup `results/budget/phase1/REPORT.md` (edit Section 6 / campaign log in this tracker too).

### Reproduce smoke pilot (optional)

```bash
make budget-test
make budget-pilot BUDGET_MAX_TICKS=3000 WORKERS=1
make budget-analyse \
  PACKAGE=F \
  TRIALS=results/budget/phase1/pilot/trials.csv \
  OUT=results/budget/phase1/pilot/package_f
```

---

## 7. Campaign log

Append one row per campaign (or notable re-analyse). Newest at top.

| Date | Campaign id | Command / notes | Grade | Packages | Key outcome | Report |
|------|-------------|-----------------|-------|----------|-------------|--------|
| 2026-09-17 | phase1_scout | `make budget-scout WORKERS=4`; stopped at 1123/1440; trials rebuilt from timeseries; Packages A/F. Resume later: `make budget-scout WORKERS=16` (see Section 6.1) | SCOUT incomplete | A, F | R=1; D_min=1; slow due to N=150 long-tail successes; N=200 not run | [scout/REPORT.md](../../../results/budget/phase1/scout/REPORT.md) |
| 2026-09-17 | budget_pilot | `make budget-test`; `make budget-pilot BUDGET_MAX_TICKS=3000 WORKERS=1`; Package F | SMOKE | A, F | R=1; D_min=1; wasteful overspend for D>1; scaling flat | [pilot/REPORT.md](../../../results/budget/phase1/pilot/REPORT.md) |

---

## 8. Next actions (ordered)

Update this list when priorities change; mark items done by moving detail into Sections 2-7.

1. **Decide Phase 1 continuation strategy**
   - Option A: resume remaining ~317 scout cells on a stronger machine:
     `make budget-scout WORKERS=16`
     (full command block in Section 6.1). Then refresh reports from new Package A/F outputs.
   - Option B (recommended if compact stays easy): skip more compact grind and start **Phase 2** harder X0 (`make budget-pilot-state`) where D_min>1 / failures are more likely.
   - Optional engineering: flush `trials.csv` incrementally in `api/budget_runner.py` so kills do not require timeseries reconstruction.

2. **Phase 2 state pilot (RQ1 / Package B)** — if choosing Option B
   - Goal: C1a/C1b path; verify X0 families via metric stats.

3. **Only after real frontiers exist**
   - Phase 3 mechanism Package C (C3).
   - Re-fit Package F for C6a/C6b on non-flat D_min(N[, X0]).

4. **Later**
   - Phase 4 transfer (C4); Phase 5 information (C5); Phase 7 early warning (C7).

Do not advance claim verdicts until scout/claim seed and grid rules in Section 8 are met (or an explicit, documented protocol exception is recorded here).

---

## 9. Update checklist (for editors)

When finishing a campaign or Cap change:

- [ ] Update phase row in Section 2
- [ ] Update RQ/claim rows in Section 3
- [ ] Update Cap "used in a campaign" in Section 4 if newly exercised
- [ ] Refresh Section 5 if protocol subset changed
- [ ] Rewrite Section 6 for the latest primary campaign (or add a subsection)
- [ ] Append Section 7 campaign log row
- [ ] Adjust Section 8 next actions
- [ ] Set "Last updated" at top
- [ ] Link the campaign REPORT under `results/budget/...`
- [ ] Keep Section 6.1 commands in sync with Makefile defaults
