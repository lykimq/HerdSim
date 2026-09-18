# Shepherding-budget progress tracker

Last updated: 2026-09-18

Living execution ledger. Definitions, claim criteria, Caps, and Section 8 freeze
live in the main plan -- do not duplicate them here.

| Document | Role |
|----------|------|
| [herdsim_research_program.md](herdsim_research_program.md) | Plain-language framing |
| [main_shepherding_budget_plan.md](main_shepherding_budget_plan.md) | Source of truth |
| [../budget/REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) | Human REPORT.md template |
| [results/budget/README.md](../../../results/budget/README.md) | Results layout conventions |
| This file | Where we are, what ran, what is next |

Campaign subsets: `configs/budget/campaigns/` (each field has a WHY comment; new campaigns must follow `campaigns/README.md`).  
Operator entry: `make -f Makefile.budget help` (or `make budget-help`).
Protocol rationale: main plan Section 8.1 and comments in `configs/budget/canonical_grid.yaml`.

---

## 1. Current snapshot

| Item | Status |
|------|--------|
| Protocol (Section 8) | DONE -- frozen 2026-09-17 as `shepherding_budget_v1` |
| Caps I1--I14 | BUILT (unit-tested); claim-grade use still pending for most |
| Results layout | Standardized 2026-09-18 (`phase{k}/{slug}/`, `packages/{a-g}/`) |
| Active phase | Phase 1 (Package A) -- IN PROGRESS |
| Blocking issue | Compact + `strombom_multi` still too easy (D_min=1); C2/C6 not evaluable yet |
| Recommended next | Prefer Phase 2 state pilot (harder X0) over more compact scout grind -- see Section 5 |

Minimum publishable unit: **RQ1 + RQ2 + RQ3 + S8**.

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

Claim verdicts: UNEVALUATED / SUPPORTED / REJECTED / INCONCLUSIVE.

---

## 3. Phase board

Done-when criteria: main plan Section 9. Update only status and evidence here.

| Phase | Focus | Formal RQ | Package | Status | Evidence / note |
|-------|-------|-----------|---------|--------|-----------------|
| 0 | Protocol freeze | S8 | Section 8 | DONE | Frozen 2026-09-17 |
| 1 | Herdability maps | RQ2 (+ RQ6 data) | A | IN PROGRESS | Pilot + partial scout historically; compact R=1, D_min=1. Path: `results/budget/phase1/{pilot,scout}/` |
| 2 | State beyond N | RQ1 | B | NOT STARTED | `make budget-pilot-state` -> `results/budget/phase2/pilot_state/` |
| 3 | Overcrowding mechanism | RQ3 | C | BLOCKED | Needs overcrowding / efficient contrast cells |
| 4 | Cross-method transfer | RQ4 | D | NOT STARTED | -- |
| 5 | Information substitution | RQ5 | E | NOT STARTED | `make budget-factor-sweep` -> `results/budget/phase5/factor_sweep/` |
| 6 | Scaling fits | RQ6 | F | SMOKE | Flat D_min on compact; not publishable |
| 7 | Early warning | RQ7 | G | NOT STARTED | -- |

---

## 4. Claims board

Criteria: main plan Part III. Verdict + pointer only.

| Claim | Verdict | Evidence pointer |
|-------|---------|------------------|
| C1a | UNEVALUATED | -- |
| C1b | UNEVALUATED | -- |
| C2a | UNEVALUATED | Compact scout (partial): no overcrowding |
| C2b | UNEVALUATED | -- |
| C3 | UNEVALUATED | -- |
| C4 | UNEVALUATED | -- |
| C5a | UNEVALUATED | -- |
| C5b | UNEVALUATED | -- |
| C6a | UNEVALUATED | Flat D_min; AIC degenerate |
| C6b | UNEVALUATED | Alpha ~ 0 on flat D_min |
| C7a | UNEVALUATED | -- |
| C7b | UNEVALUATED | -- |

---

## 5. Next actions

1. **Choose Phase 1 continuation**
   - Option A: resume scout: `make budget-scout WORKERS=16` (resume-safe if `manifest.jsonl` present).
   - Option B (recommended if compact stays easy): `make budget-pilot-state`.
2. **If Option B:** Package B toward C1a/C1b; verify X0 metric gates.
3. **Only after real frontiers:** Phase 3 (C3); re-fit Package F (C6).
4. **Later:** Phase 4 (C4); Phase 5 (`make budget-factor-sweep`); Phase 7 (C7).

Do not advance claim verdicts until Section 8 seed rules are met, or log an exception here.

---

## 6. Caps in use

Designs: main plan Section 10.1. Here only campaign use.

| Cap | Used in a campaign? | Note |
|-----|---------------------|------|
| I1 grid runner | yes | Pilot + partial scout |
| I2 frontier | yes | Package A |
| I3 regimes | yes | Package A |
| I4 mean-spread, extent | yes | Timeseries |
| I5 X0 generators | no | Awaiting Phase 2 |
| I6 state predictors | no | Needs Package B |
| I7 I_dir, coverage | smoke | Timeseries present historically |
| I8 mechanism tests | no | Phase 3 |
| I9 transfer table | no | Phase 4 |
| I10 factor sweep | no | `budget-factor-sweep` ready |
| I11 scaling fits | yes | Package F (degenerate) |
| I12 early warning | no | Phase 7 |
| I13 protocol + dossier | yes | Exports |
| I14 timeseries Parquet | yes | Stem == cell key (post-cleanup) |

---

## 7. Protocol drift (latest primary campaign)

Defaults: main plan Section 8. Gaps only.

| Item | Frozen | Latest scout (historical partial) | Gap |
|------|--------|-----------------------------------|-----|
| Layout X0 | all four | compact only | Phase 2 not run |
| N | 25..400 | through 100 (+ partial 150) | unfinished |
| Methods | baseline + transfer | strombom_multi only | transfer unused |
| Package paths | `packages/{a-g}/` | older runs may use `package_a/` | migrate on next analyse |

---

## 8. Latest results

Artefacts may be absent on a fresh clone (gitignored). Paths below are the canonical locations after the 2026-09-18 layout cleanup.

### `phase1_scout` (2026-09-17) -- STOPPED (historical)

| Field | Value |
|-------|-------|
| Grade | SCOUT incomplete |
| Path | `results/budget/phase1/scout/` |
| Planned | 1440 cells (6 N x 8 D x 30 seeds, compact) |
| Completed | 1123/1440 (78%) when stopped |
| Outcome | R=1.0; D_min=1; no overcrowding |
| Analyse | `packages/a/`, `packages/f/` |

Resume: `make budget-scout WORKERS=16` (keep `manifest.jsonl`).

### `budget_pilot` / `phase1_pilot` (2026-09-17) -- SMOKE

Path: `results/budget/phase1/pilot/`. Same qualitative picture on small N.

---

## 9. Campaign log

| Date | Campaign | Grade | Packages | Outcome | Path |
|------|----------|-------|----------|---------|------|
| 2026-09-18 | layout cleanup | -- | -- | Standardized paths + campaign YAMLs | `results/budget/README.md` |
| 2026-09-17 | phase1_scout (stopped) | SCOUT incomplete | A, F | R=1; D_min=1 | `phase1/scout/` |
| 2026-09-17 | phase1_pilot | SMOKE | A | R=1; flat scaling | `phase1/pilot/` |

---

## 10. Tracker update checklist

- [ ] Section 1 snapshot
- [ ] Section 3 phase row
- [ ] Section 4 claims (if claim-grade)
- [ ] Section 5 next actions
- [ ] Section 6 Cap use
- [ ] Section 7 drift
- [ ] Section 8 primary campaign + REPORT.md
- [ ] Section 9 log row
- [ ] Last updated date
