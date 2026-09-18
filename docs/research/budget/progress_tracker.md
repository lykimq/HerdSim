# Shepherding-budget progress tracker

Last updated: 2026-09-18

Living execution ledger for the shepherding-budget program. Use this to resume work. Do not copy scientific definitions, claim criteria, Cap designs, or protocol defaults here -- those live in the main plan.

| Document | Role |
|----------|------|
| [herdsim_research_program.md](herdsim_research_program.md) | Plain-language framing (Size / Structure / Mechanism / Generality) |
| [main_shepherding_budget_plan.md](main_shepherding_budget_plan.md) | Source of truth: formal RQs, claims, Caps, Section 8 freeze |
| This file | Where we are, what ran, what is next |
| [results/budget/](../../../results/budget/) | Campaign artefacts and REPORT.md files |

---

## 1. Current snapshot

| Item | Status |
|------|--------|
| Protocol (Section 8) | DONE -- frozen 2026-09-17 as `shepherding_budget_v1` |
| Caps I1--I14 | BUILT (unit-tested); claim-grade use still pending for most |
| Active phase | Phase 1 (Package A) -- IN PROGRESS |
| Blocking issue | Compact + `strombom_multi` still too easy (D_min=1); C2/C6 not evaluable yet |
| Recommended next | Prefer Phase 2 state pilot (harder X0) over more compact scout grind -- see Section 5 |

Minimum publishable unit (from main plan): **RQ1 + RQ2 + RQ3 + S8**.

---

## 2. Status legend

| Tag | Meaning |
|-----|---------|
| NOT STARTED | No work yet |
| BUILT | Code exists and is unit-tested; not yet used for claim evaluation |
| SMOKE | Pipeline works on a reduced grid; not claim-grade |
| IN PROGRESS | Scout/claim campaign running or partial |
| DONE | Phase done-when met, or claim decided |
| BLOCKED | Waiting on a dependency |

Claim verdicts (only with claim-grade evidence): UNEVALUATED / SUPPORTED / REJECTED / INCONCLUSIVE.

---

## 3. Phase board

Done-when criteria and package contents: main plan Sections 3.1 and 9. Update only status and evidence here.

| Phase | Focus | Formal RQ | Package | Status | Evidence / note |
|-------|-------|-----------|---------|--------|-----------------|
| 0 | Protocol freeze | S8 | Section 8 | DONE | Frozen 2026-09-17 |
| 1 | Herdability maps | RQ2 (+ data for RQ6) | A | IN PROGRESS | Pilot SMOKE + scout 1123/1440 stopped; compact R=1, D_min=1; C2 unevaluable. [phase1/REPORT.md](../../../results/budget/phase1/REPORT.md) |
| 2 | State beyond N | RQ1 | B | NOT STARTED | X0 Cap I5 built; no Package B run yet |
| 3 | Overcrowding mechanism | RQ3 | C | BLOCKED | Needs overcrowding / efficient contrast cells |
| 4 | Cross-method transfer | RQ4 | D | NOT STARTED | -- |
| 5 | Information substitution | RQ5 | E | NOT STARTED | -- |
| 6 | Scaling fits | RQ6 | F | SMOKE | Flat D_min=1 on completed compact N; not publishable |
| 7 | Early warning | RQ7 | G | NOT STARTED | -- |

---

## 4. Claims board

Claim criteria: main plan Part III. Record only verdict + pointer here.

| Claim | Verdict | Evidence pointer |
|-------|---------|------------------|
| C1a | UNEVALUATED | -- |
| C1b | UNEVALUATED | -- |
| C2a | UNEVALUATED | Compact scout (1 method, partial): no overcrowding |
| C2b | UNEVALUATED | -- |
| C3 | UNEVALUATED | -- |
| C4 | UNEVALUATED | -- |
| C5a | UNEVALUATED | -- |
| C5b | UNEVALUATED | -- |
| C6a | UNEVALUATED | Flat D_min; AIC comparison degenerate |
| C6b | UNEVALUATED | Alpha effectively 0 on flat D_min |
| C7a | UNEVALUATED | -- |
| C7b | UNEVALUATED | -- |

---

## 5. Next actions

Ordered. Move finished items into the campaign log; keep this list short.

1. **Choose Phase 1 continuation**
   - Option A: resume remaining ~317 compact scout cells: `make budget-scout WORKERS=16` (resume-safe; see Section 7).
   - Option B (recommended if compact stays easy): start Phase 2 harder X0 via `make budget-pilot-state`.
2. **If Option B:** run Package B path toward C1a/C1b; verify X0 families differ on intended metrics.
3. **Only after real frontiers exist:** Phase 3 (C3); re-fit Package F for C6a/C6b.
4. **Later:** Phase 4 transfer (C4); Phase 5 information (C5); Phase 7 early warning (C7).

Do not advance claim verdicts until Section 8 scout/claim seed rules are met, or an explicit protocol exception is logged in Section 8 below.

---

## 6. Caps in use

Full Cap table and designs: main plan Section 10.1. Here only whether each Cap has been used in a campaign.

| Cap | Used in a campaign? | Note |
|-----|---------------------|------|
| I1 grid runner + provenance | yes | Pilot + partial scout |
| I2 frontier | yes | Scout Package A |
| I3 regimes | yes | Scout Package A |
| I4 mean-spread, extent | yes | Timeseries columns |
| I5 X0 generators | no | Awaiting Package B |
| I6 state predictors | no | Needs Package B |
| I7 I_dir, coverage | smoke | In scout timeseries; not claim-tested |
| I8 mechanism tests | no | Phase 3 |
| I9 transfer table | no | Phase 4 |
| I10 factor sweep / substitution | no | Phase 5 |
| I11 scaling fits | yes | Scout Package F (degenerate) |
| I12 early warning | no | Phase 7 |
| I13 canonical protocol + dossier | yes | Phase-1 exports |
| I14 timeseries Parquet | yes | Scout timeseries present |

Operator entry points: `make budget-help`, `budget-test`, `budget-pilot`, `budget-pilot-state`, `budget-analyse`, `budget-scout`.

---

## 7. Protocol drift (scout vs freeze)

Defaults: main plan Section 8. List only gaps vs the freeze for the latest primary campaign.

| Item | Frozen | Latest scout (partial) | Gap |
|------|--------|------------------------|-----|
| Layout X0 | compact, wide, split, outlier_rich | compact only | Package B not run |
| N | 25..400 | 25..100 complete; 150 partial; 200+ not started | unfinished / incomplete grid |
| D | through 35 | through 20 for N<=100 | D=25/35 unused |
| Methods | baseline + transfer set | `strombom_multi` only | transfer unused |
| theta | 0.90 (+ report 0.50, 0.70) | 0.90 only | sensitivity not reported |
| Claim seeds | 100 on boundary | not used | -- |

---

## 8. Latest results (keep one primary campaign)

### `phase1_scout` (2026-09-17) -- STOPPED

| Field | Value |
|-------|-------|
| Grade | SCOUT incomplete |
| Planned | 6 N x 8 D x 30 seeds x compact x strombom_multi = 1440 |
| Completed | 1123/1440 (78%) |
| Outcome | R=1.0 on all completed cells; D_min=1; no overcrowding |
| Artefacts | `results/budget/phase1/scout/` |
| Report | [scout/REPORT.md](../../../results/budget/phase1/scout/REPORT.md) |

Scientific reading: compact + strombom_multi remains easy through the completed band. Do not cite for C2/C6.

Resume remaining cells (do not delete `manifest.jsonl`):

```bash
make budget-scout WORKERS=16
```

Re-analyse Packages A/F from existing `trials.csv`:

```bash
make budget-analyse PACKAGE=A TRIALS=results/budget/phase1/scout/trials.csv OUT=results/budget/phase1/scout/package_a
make budget-analyse PACKAGE=F TRIALS=results/budget/phase1/scout/trials.csv OUT=results/budget/phase1/scout/package_f
```

### Prior smoke: `budget_pilot` (2026-09-17)

Same qualitative picture on N in {25,50,100}. Report: [pilot/REPORT.md](../../../results/budget/phase1/pilot/REPORT.md).

---

## 9. Campaign log

Newest first. One row per campaign or notable re-analyse.

| Date | Campaign | Grade | Packages | Outcome | Report |
|------|----------|-------|----------|---------|--------|
| 2026-09-17 | phase1_scout (stopped 1123/1440) | SCOUT incomplete | A, F | R=1; D_min=1; compact easy | [scout](../../../results/budget/phase1/scout/REPORT.md) |
| 2026-09-17 | budget_pilot | SMOKE | A, F | R=1; D_min=1; flat scaling | [pilot](../../../results/budget/phase1/pilot/REPORT.md) |

---

## 10. Tracker update checklist

When finishing a campaign or Cap change:

- [ ] Refresh Section 1 snapshot
- [ ] Update phase row in Section 3
- [ ] Update claim verdicts in Section 4 if claim-grade
- [ ] Adjust Section 5 next actions
- [ ] Mark Cap "used" in Section 6 if newly exercised
- [ ] Refresh Section 7 drift table if protocol subset changed
- [ ] Rewrite Section 8 for the primary campaign (or point to a new REPORT)
- [ ] Append Section 9 log row
- [ ] Set "Last updated" at top
