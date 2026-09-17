# Shepherding-budget progress tracker

Status: living document (update after each campaign or Cap change)  
Last updated: 2026-09-17

This file tracks **plan coverage**, **implementation**, and **experimental results** for the shepherding-budget program. It does not replace the scientific source of truth.

| Document | Role |
|----------|------|
| [herdsim_research_program.md](herdsim_research_program.md) | Parent framing (size, structure, mechanism, transfer) |
| [main_shepherding_budget_plan.md](main_shepherding_budget_plan.md) | Single source of truth (RQs, claims, phases, Caps, Section 8) |
| This file | Execution ledger: what is built, what ran, what claims are evaluable |
| [results/budget/pilot/REPORT.md](../../../results/budget/pilot/REPORT.md) | Latest pilot campaign narrative |

How to use: after a run or Cap change, update Sections 2-6 and append a row to Section 7. Keep verdicts honest (pilot != claim-grade).

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
| 1 | Herdability maps (baseline) | RQ2 (+ data for RQ6) | A | SMOKE | C2 evaluable on baseline; frontier+regimes exported | Pilot Package A only; C2 not evaluable |
| 2 | Collective-state manipulation | RQ1 | B | NOT STARTED | C1a/C1b evaluable; X0 families verified | `budget-pilot-state` not run |
| 3 | Overcrowding mechanism | RQ3 | C | NOT STARTED | C3 evaluable; I_dir/C series stored | Needs overcrowding cells from Phase 1 |
| 4 | Cross-method transfer | RQ4 | D | NOT STARTED | Transfer table for >= 3 methods | -- |
| 5 | Information substitution | RQ5 | E | NOT STARTED | C5a/C5b evaluable | -- |
| 6 | Scaling regimes | RQ6 | F | SMOKE | C6a or C6b decided | Pilot Package F degenerate (flat D_min=1) |
| 7 | Early warning | RQ7 | G | NOT STARTED | C7a/C7b evaluable | -- |

### Map from research-program progression

| Research program step | Main-plan phases / RQs | Status |
|-----------------------|------------------------|--------|
| 1. Size scaling `D_min(N)` | Phase 1 + Phase 6 (RQ2 data, RQ6) | SMOKE |
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
| RQ2 | Boundary and regimes? | A | C2a, C2b | SMOKE | Pilot: R=1 everywhere; no overcrowding; C2 unevaluable |
| RQ3 | Why diminishing returns? | C | C3 | BLOCKED | Needs overcrowding / efficient contrast cells |
| RQ4 | Cross-method generality? | D | C4 | NOT STARTED | Baseline instrument only so far |
| RQ5 | Information vs shepherds? | E | C5a, C5b | NOT STARTED | -- |
| RQ6 | Scaling with N and state? | F | C6a, C6b | SMOKE | Pilot: constant D_min=1; not publishable |
| RQ7 | Early warning of failure? | G | C7a, C7b | NOT STARTED | -- |
| S8 | Reproducible protocol | all | (infra) | DONE | Config + provenance path in place |

### Claim detail

| Claim | Criterion (short) | Verdict | Evidence pointer |
|-------|-------------------|---------|------------------|
| C1a | D_min differs by >= 2 across X0 at some N | UNEVALUATED | -- |
| C1b | State features beat (N, D) predictors (dAIC > 4) | UNEVALUATED | -- |
| C2a | Overcrowding for >= 2 methods at theta=0.90 | UNEVALUATED | Pilot (1 method): no overcrowding |
| C2b | Hard ceiling: R < theta at T1=20000 past D_overcrowd | UNEVALUATED | -- |
| C3 | Overcrowding cells higher I_dir and/or fragmentation | UNEVALUATED | -- |
| C4 | Shared mechanism label across >= 3 methods | UNEVALUATED | -- |
| C5a | Info step reduces D_min by >= 1 at N in {100,200} | UNEVALUATED | -- |
| C5b | Second info step saves fewer shepherds than first | UNEVALUATED | -- |
| C6a | Global power law rejected vs piecewise/state (dAIC > 10) | UNEVALUATED | Pilot AIC comparison degenerate |
| C6b | Stable sublinear alpha < 1 in a stated domain | UNEVALUATED | Pilot alpha effectively 0 on flat D_min |
| C7a | State warning AUROC > (N, D) baseline | UNEVALUATED | -- |
| C7b | Lead time >= 500 ticks on >= 30% failure trajectories | UNEVALUATED | -- |

---

## 4. Implementation Caps (main plan Section 10.1)

| Cap | Capability | Code | Built? | Used in a campaign? | Notes |
|-----|------------|------|--------|---------------------|-------|
| I1 | Grid runner + provenance | `api/budget_runner.py`, `analysis/budget/provenance.py` | yes | SMOKE | Pilot grid |
| I2 | Frontier extraction | `analysis/budget/frontier.py` | yes | SMOKE | `package_a/frontier.csv` |
| I3 | Regime labelling | `analysis/budget/regimes.py` | yes | SMOKE | `package_a/regimes.csv` |
| I4 | Mean-spread, extent | `metrics/mean_spread.py`, `metrics/extent.py` | yes | SMOKE | Timeseries columns |
| I5 | X0 generators + wiring | `core/x0_generators.py`, `scenarios/drive_to_goal.py` | yes | no | Awaiting Package B run |
| I6 | State vs (N, D) predictors | `analysis/budget/predictors.py` | yes | no | Needs Package B |
| I7 | I_dir, coverage metrics | `metrics/shepherd_interference.py`, `metrics/shepherd_coverage.py` | yes | no | Phase 3 |
| I8 | Mechanism tests | `analysis/budget/mechanism.py` | yes | no | Phase 3 |
| I9 | Transfer table | `analysis/budget/transfer.py` | yes | no | Phase 4 |
| I10 | Factor sweep + substitution | `scripts/budget/run_factor_sweep.py`, `analysis/budget/substitution.py` | yes | no | Phase 5 |
| I11 | Scaling fits | `analysis/budget/scaling.py` | yes | SMOKE | `package_f/scaling_fits.csv` |
| I12 | Early warning | `analysis/budget/early_warning.py` | yes | no | Phase 7 |
| I13 | Canonical protocol + dossier | `configs/budget/canonical_grid.yaml`, `analysis/budget/export.py` | yes | SMOKE | Pilot exports |
| I14 | Timeseries Parquet | `api/budget_runner.py` | yes | SMOKE | `results/budget/pilot/timeseries/` |

Operator entry points: `make budget-help`, `budget-test`, `budget-pilot`, `budget-pilot-state`, `budget-analyse`, `budget-scout`.

Tests: `make budget-test` (12 passed as of pilot date).

---

## 5. Protocol coverage vs Section 8 freeze

| Item | Frozen default | Latest pilot | Gap |
|------|----------------|--------------|-----|
| Task | `drive_to_goal` | same | none |
| Instrument | `strombom_multi` (+ transfer set later) | baseline only | transfer methods unused |
| Theta | 0.90 (also 0.50, 0.70) | 0.90 only | sensitivity not reported |
| N | {25,50,75,100,150,200,300,400} | {25,50,100} | missing larger N |
| D | {1,2,3,4,6,10,15,20,25,35} | {1,2,3,4,6,10} | missing D >= 15 |
| X0 | compact, wide, split, outlier_rich | compact only | Package B not run |
| T0 | 10000 | 3000 | restore T0 for scout/claim |
| T1 | 20000 (C2b) | not used | -- |
| Scout seeds | 30 | 5 | raise for scout |
| Claim seeds | 100 on boundary | not used | -- |
| Master seed | 2026 | 2026..2030 (5 seeds) | ok for pilot |

---

## 6. Latest experimental results summary

### Campaign: `budget_pilot` (2026-09-17)

| Field | Value |
|-------|-------|
| Grade | SMOKE (not scout, not claim) |
| Grid | 3 N x 6 D x 5 seeds x 1 layout x 1 instrument = 90 trials |
| Wall time | ~8.3 min (`WALL_SEC=496.82`) |
| Success | 90/90 (R=1.0 all cells) |
| Artefacts | `results/budget/pilot/` (trials, package_a, package_f, timeseries, REPORT.md) |

Frontier (compact, theta=0.90): D_min=1 for N in {25,50,100}; no D_overcrowd; no hard_failure; B*_D=1.

Regimes: 3 efficient_operation (D=1); 15 wasteful_overspend (D>1); 0 other.

Scaling: best model constant (c=1); comparison degenerate.

Scientific reading: pipeline Cap I1-I3 / I11 smoke-tested. Easy compact band does not stress herdability limits. Do not cite for C2 or C6.

Full narrative: [REPORT.md](../../../results/budget/pilot/REPORT.md).

---

## 7. Campaign log

Append one row per campaign (or notable re-analyse). Newest at top.

| Date | Campaign id | Command / notes | Grade | Packages | Key outcome | Report |
|------|-------------|-----------------|-------|----------|-------------|--------|
| 2026-09-17 | budget_pilot | `make budget-test`; `make budget-pilot BUDGET_MAX_TICKS=3000 WORKERS=1`; Package F analyse | SMOKE | A, F | R=1; D_min=1; wasteful overspend for D>1; scaling flat | [REPORT.md](../../../results/budget/pilot/REPORT.md) |

---

## 8. Next actions (ordered)

Update this list when priorities change; mark items done by moving detail into Sections 2-7.

1. **Phase 1 scout (RQ2 / Package A toward claim-grade)**
   - Expand N/D toward frozen ranges; restore `T0=10000`; raise seeds toward scout=30.
   - Goal: obtain non-trivial reliability variation and/or overcrowding so C2 becomes testable on `strombom_multi`.
   - Suggested entry: `make budget-scout` (long-running; see Makefile defaults).

2. **Phase 2 state pilot (RQ1 / Package B)**
   - Run `make budget-pilot-state` (or fuller X0 scout) once Phase 1 tooling time budget allows.
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
