# Shepherding-budget progress tracker

Last updated: 2026-09-18

Working notes for where we are. Definitions, claim criteria, Caps, and the Section 8
freeze stay in the main plan -- do not copy them here.

| Document | Role |
|----------|------|
| [herdsim_research_program.md](herdsim_research_program.md) | Program framing |
| [main_shepherding_budget_plan.md](main_shepherding_budget_plan.md) | Detailed plan |
| [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) | Human REPORT.md template |
| [results/budget/README.md](../../../results/budget/README.md) | Results layout conventions |
| This file | Where we are, what ran, what is next; hardware + ordered run plan |

Campaign subsets: `configs/budget/campaigns/` (each field has a WHY comment; new campaigns must follow `campaigns/README.md`).  
Operator entry: `make -f Makefile.budget help` (or `make budget-help`).
Protocol rationale: main plan Section 8.1 and comments in `configs/budget/canonical_grid.yaml`.

Wall-clock times depend on the machine. For claim-grade campaigns, note which host
you used (Section 6). Across machines, compare frontiers and regimes -- not hours.

---

## 1. Current snapshot

| Item | Status |
|------|--------|
| Protocol (Section 8) | DONE -- frozen 2026-09-17 as `shepherding_budget_v1` |
| Caps I1--I14 | BUILT (unit-tested); claim-grade use still pending for most |
| Results layout | Standardized 2026-09-18 (`phase{k}/{slug}/`, `packages/{a-g}/`) |
| Active phase | Phase 1 (Package A) -- IN PROGRESS |
| Blocking issue | Compact + `strombom_multi` still too easy (D_min=1); C2/C6 not evaluable yet |
| Recommended next | Prefer Phase 2 state pilot (harder X0) over more compact scout grind -- see Sections 5 and 7 |
| Primary machine | `gwen` -- Intel Ultra 7 165H, 64 GB RAM (see Section 6) |

Smallest publishable slice we are aiming for: **RQ1 + RQ2 + RQ3 + S8**.

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

Immediate (next three runs on this machine):

1. `make -f Makefile.budget budget-pilot` -- confirm Package A reports/figures after layout cleanup.
2. `make -f Makefile.budget budget-scout WORKERS=12` -- or skip finishing if compact remains flat (Gate A in Section 7).
3. `make -f Makefile.budget budget-pilot-state` -- then add a Phase-2 scout YAML if X0 metrics separate.

Longer path: Section 7 (ordered run plan). Do not advance claim verdicts until Section 8 seed rules are met, or log an exception here.

---

## 6. Hardware profile (primary machine)

So others know that wall times and `WORKERS` choices are machine-dependent.
Re-measure and add a row if the primary box changes or a campaign runs elsewhere.

| Field | Value (snapshot 2026-09-18) |
|-------|-----------------------------|
| Host | `gwen` |
| OS | Linux 7.0.0-27-generic |
| CPU | Intel Core Ultra 7 165H |
| Logical CPUs | 22 (16 cores / 2 threads per core; max ~5.0 GHz) |
| RAM | 61 GiB total (~54 GiB available at snapshot) |
| Disk (`/`) | 468G total, ~253G free |
| GPU | none (HerdSim budget sims are CPU-bound) |
| CPU governor | `powersave` at snapshot -- switch to `performance` for long campaigns |
| Recommended WORKERS | 8 safe; 12--16 if plugged in, no sleep, performance governor |

Notes for other machines:

- With the same protocol, seeds, and code revision, scientific results (R, D_min, regimes) should match; wall-clock will not.
- Timeout-heavy cells (hard X0, many failures to T0=10000) take much longer than the compact scout baseline below.
- Rough calibration on this host: historical compact scout ~1123 cells in ~2 h at `WORKERS=4` (many short successes). At `WORKERS=8--16`, similar scout ~1--4 h; harder layouts can be much longer.
- For claim-grade campaigns, copy this table into the campaign `REPORT.md` (or at least note host + `WORKERS` + governor).

If you run on a different machine, add a row here:

| Date | Host | CPU / RAM | WORKERS | Notes |
|------|------|-----------|---------|-------|
| 2026-09-18 | gwen | Ultra 7 165H / 64 GB | 8--16 planned | Primary; see table above |

---

## 7. Ordered run plan (one campaign at a time)

Finish the original program (Size -> Structure -> Mechanism -> Generality, then
follow-ons) without one giant grid. Run **one campaign**, write `REPORT.md`, update
this tracker, then the next. Times (`*`) are rough for the primary machine in
Section 6 and assume many short successes.

Finish line we are working toward:

- Core slice: **RQ1 + RQ2 + RQ3 + S8**
- Then: **RQ4 -> RQ5 -> RQ6 polish -> RQ7**
- Paper cross-check: **after** we have real HerdSim frontiers (not on the core path)

### Phase 0 -- done

Protocol freeze (`shepherding_budget_v1`). Section 8 frozen 2026-09-17.

### Wave 1 -- Size map (RQ2 data, feed RQ6)

| # | Campaign | Command / config | ~Time* | Done when |
|---|----------|------------------|--------|-----------|
| 1 | Smoke pilot | `make -f Makefile.budget budget-pilot` (optional `BUDGET_MAX_TICKS=3000`) | minutes | Pipeline + Package A + figures OK |
| 2 | Phase-1 scout (compact) | `make -f Makefile.budget budget-scout WORKERS=8-16` | ~1--4 h | R(N,D), frontier, regimes exported |

Gate A: if compact still has D_min ~ 1 and no overcrowding, do **not** grind more compact N/D -- go to Wave 2. If a real frontier appears, finish scout N=300/400 and high D, then still do Wave 2 for structure.

### Wave 2 -- Structure (RQ1)

| # | Campaign | Command / config | ~Time* | Done when |
|---|----------|------------------|--------|-----------|
| 3 | State smoke | `make -f Makefile.budget budget-pilot-state` | tens of min | All 4 X0 differ on metrics; Package B path runs |
| 4 | State scout | New campaign YAML: N/D like phase1 scout (or smaller), **all 4 X0**, 30 seeds, baseline only | ~4--12 h (longer if hard) | Path to C1a; D_min differs by layout |

Gate B: need some failure / D_min>1 / overcrowding contrast. If still all easy, harden (wider spread, split distance, noise, or stricter success) before mechanism.

### Wave 3 -- Mechanism (RQ3)

| # | Campaign | What | ~Time* | Done when |
|---|----------|------|--------|-----------|
| 5 | Mechanism contrast | Reuse Wave 2 trials + timeseries; Package C on efficient vs overcrowding (or under-budget) cells | mostly analyse | C3 evaluable path |
| 6 | Targeted re-sim (only if needed) | Few (N, X0, D) cells at claim seeds | ~1--3 h | Clear I_dir / coverage / fragmentation contrast |

### Wave 4 -- Generality (RQ4)

| # | Campaign | What | ~Time* | Done when |
|---|----------|------|--------|-----------|
| 7 | Transfer scout method 2 | Same grid as best Wave 1/2 setup, `kubo` | ~same as that scout | -- |
| 8 | Method 3 | `fat` | ~same | -- |
| 9 | Method 4 | `communication_free` | ~same | Package D transfer table; C4 path |

Run **one method per campaign**, not all four in one job.

Gate C -- core program closable: claim path for **C1 + C2 + C3** (and S8) with honest
grades. RQ4 can be partial (>=3 methods) for a first paper cut.

### Wave 5 -- Follow-ons (after core)

| # | Campaign | RQ | ~Time* |
|---|----------|----|--------|
| 10 | Factor sweep obs ladder | RQ5 | ~half day--1 day |
| 11 | Scaling fits on non-flat frontiers | RQ6 | analyse-heavy |
| 12 | Early warning on failure trajectories | RQ7 | needs failures + timeseries |
| 13 | (Optional) Paper cross-check | later validation | separate campaign |

### Claim-grade rule

When a frontier exists: for important boundary cells, re-run **100 seeds** (not the full grid). Usually hours, not days -- do this **after** scout finds the boundary.

### Operator rules (keep manageable)

1. One campaign -> `REPORT.md` -> update this tracker -> next.
2. `WORKERS=8` is safe; `12--16` if plugged in / no sleep / performance governor.
3. Always resume; never delete `manifest.jsonl`.
4. Keep timeseries for mechanism / early-warning; optional off for pure RQ5 sweeps.
5. Stop at each Gate; do not "just add more N."

\*Hard layouts that often hit T0=10000 can multiply wall time; still fine one campaign
at a time if you resume.

---

## 8. Caps in use

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

## 9. Protocol drift (latest primary campaign)

Defaults: main plan Section 8. Gaps only.

| Item | Frozen | Latest scout (historical partial) | Gap |
|------|--------|-----------------------------------|-----|
| Layout X0 | all four | compact only | Phase 2 not run |
| N | 25..400 | through 100 (+ partial 150) | unfinished |
| Methods | baseline + transfer | strombom_multi only | transfer unused |
| Package paths | `packages/{a-g}/` | older runs may use `package_a/` | migrate on next analyse |

---

## 10. Latest results

Paths below are the canonical locations after the 2026-09-18 layout cleanup.
Run data under `results/budget/` is kept in git once committed.

### `phase1_scout` (2026-09-17) -- STOPPED (historical)

| Field | Value |
|-------|-------|
| Grade | SCOUT incomplete |
| Path | `results/budget/phase1/scout/` |
| Planned | 1440 cells (6 N x 8 D x 30 seeds, compact) |
| Completed | 1123/1440 (78%) when stopped |
| Outcome | R=1.0; D_min=1; no overcrowding |
| Analyse | `packages/a/`, `packages/f/` |
| Hardware | Primary machine (Section 6); historical run used WORKERS=4 |

Resume: `make -f Makefile.budget budget-scout WORKERS=12` (keep `manifest.jsonl`).

### `budget_pilot` / `phase1_pilot` (2026-09-17) -- SMOKE

Path: `results/budget/phase1/pilot/`. Same qualitative picture on small N.

---

## 11. Campaign log

| Date | Campaign | Grade | Packages | Outcome | Path |
|------|----------|-------|----------|---------|------|
| 2026-09-18 | run plan + hardware | -- | -- | Ordered waves + machine profile in tracker | this file Sec 6--7 |
| 2026-09-18 | layout cleanup | -- | -- | Standardized paths + campaign YAMLs | `results/budget/README.md` |
| 2026-09-17 | phase1_scout (stopped) | SCOUT incomplete | A, F | R=1; D_min=1 | `phase1/scout/` |
| 2026-09-17 | phase1_pilot | SMOKE | A | R=1; flat scaling | `phase1/pilot/` |

---

## 12. Tracker update checklist

- [ ] Section 1 snapshot
- [ ] Section 3 phase row
- [ ] Section 4 claims (if claim-grade)
- [ ] Section 5 next actions
- [ ] Section 6 hardware row (if machine or WORKERS change)
- [ ] Section 7 wave status / gates
- [ ] Section 8 Cap use
- [ ] Section 9 drift
- [ ] Section 10 primary campaign + REPORT.md (note host / WORKERS)
- [ ] Section 11 log row
- [ ] Last updated date
