# Scaling progress tracker

Role: **status** (1 = code, 2 = experiment runs, then Done / Claims)
Why / what: [herdsim_research_program.md](herdsim_research_program.md)
How: [main_scaling_plan.md](main_scaling_plan.md)
Report form: [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)
Help: `make -C scaling help`

Last updated: 2026-09-21
Host: `gwen` (prefer `WORKERS=8`, up to 12-16 if plugged in, performance governor)
Results: `scaling/results/` is gitignored; keep campaign folders on this host.

How to read this file:
- **Section 1** = is the *code* ready? (Caps, protocols, make targets)
- **Section 2** = have we *run* the experiments? (commands + checklist Status)
- Do not mix the two. Code DONE does not mean the experiment ran.

---

## 1. Implementation (code only)

### Phase code board

Code / protocol / analyse path for each phase. Experiment run status lives only in Section 2.

| Phase | RQ | Package | Code status | What is in the tree | What code is still missing |
|-------|----|---------|-------------|---------------------|----------------------------|
| 0 | S8 | all | DONE | `canonical_grid.yaml` (`scaling_v1`) | nothing |
| 1 | RQ2 | A | DONE | pilot + scout + claim YAMLs; claim-plan/reseed make targets; Package A (+ bootstrap) | T1 hard-ceiling protocol / make target (needed for C2b only) |
| 2 | RQ1 | B | PARTIAL | smoke: `phase2_pilot_state.yaml`; Package B analyse | `phase2_claim.yaml` + make target (claim N={50,100,200} x 4 X0) |
| 3 | RQ3 | C | DONE | Package C analyse (mechanism + temporal order) | nothing for code; needs Phase 1-2 *data* (Section 2) |
| 4 | RQ4 | D | PARTIAL | Package D analyse (transfer table) | claim protocol YAMLs per transfer method (`kubo`, `fat`, ...) |
| 5 | RQ5 | E | PARTIAL | scout: `phase5_factor_sweep.yaml`; Package E | claim protocol at N={100,200} (obs/range/comm) |
| 6 | RQ6 | F | DONE | Package F analyse (fits + AIC/BIC/CV) | nothing for code; needs frontiers from Section 2 |
| 7 | RQ7 | G | DONE | Package G analyse (early warning campaign) | nothing for code; needs timeseries from Section 2 |

Caps I1-I14: **built and unit-tested**. E1 (intended velocities): **not built** on purpose (only if walls confound I_dir).

### Code still to add (do in this order)

Only *implementation* gaps, in the order the program needs them. Tick when the YAML/make target exists. Experiment execution is Section 2.

| Next | Add this code | Why | Blocks claims | Status |
|------|---------------|-----|---------------|--------|
| A | *(none for Phase 1 baseline path)* | Pilot / scout / claim already coded | Phase 1 C2a path is runnable now | DONE |
| B | `phase1_t1.yaml` + `make scaling-t1` (overcrowding cells, `max_ticks=20000`) | Hard-ceiling vs timeout | C2b | TODO |
| C | `phase2_claim.yaml` + `make scaling-phase2-claim` (N={50,100,200}, 4 X0, full D, claim seeds) | Structure claim map | C1a, C1b | TODO |
| D | Phase 4 claim YAMLs (or one multi-method claim protocol) for `strombom_multi`, `kubo`, `fat` (+ recommended `communication_free`) | Transfer grids | C4 | TODO |
| E | `phase5_claim.yaml` (N={100,200}, obs/range/comm ladders, claim seeds) | Information substitution claim | C5a, C5b | TODO |
| F | E1 intended velocities (optional) | Only if RQ3 I_dir is wall-confounded | C3 robustness | SKIP unless needed |

After A-E exist, Section 1 code for the full program is complete. Until then, you can still run Section 2 steps 0-5 (Phase 1) with current code.

---

## 2. Experiment runs (order + commands)

Run top to bottom. Update the Status column only here (`TODO` / `RUNNING` / `DONE` / `SKIPPED`).

Default from repo root. Example workers: `WORKERS=8`.

### Checklist

| # | Step | Grade | Command | Output | Status |
|---|------|-------|---------|--------|--------|
| 0 | Sanity tests | n/a | `make -C scaling scaling-test` | pytest | optional |
| 1 | Phase 1 smoke | SMOKE | `make -C scaling scaling-pilot WORKERS=4` | `scaling/results/phase1/pilot/` | TODO |
| 2a | If compact D_min ~ 1: Phase 2 smoke | SMOKE | `make -C scaling scaling-pilot-state WORKERS=4` | `scaling/results/phase2/pilot_state/` | TODO (branch) |
| 2b | Phase 1 scout map | SCOUT | `make -C scaling scaling-scout WORKERS=8` | `scaling/results/phase1/scout/` | TODO |
| 3 | Plan claim boundaries (no sims) | n/a | `make -C scaling scaling-claim-plan` | `scaling/results/phase1/claim/boundary_cells.csv` | TODO |
| 4 | Phase 1 claim reseed | CLAIM | `make -C scaling scaling-claim-reseed WORKERS=8` | `scaling/results/phase1/claim/` | TODO |
| 5 | Analyse Package A (and F) on claim | CLAIM | `make -C scaling scaling-analyse PACKAGE=A TRIALS=results/phase1/claim/trials.csv OUT=results/phase1/claim/packages/a` | packages | TODO |
| 6 | Phase 1 T1 hard-ceiling | CLAIM | *(needs code item B first)* | `scaling/results/phase1/t1/` | BLOCKED on code B |
| 7 | Phase 2 claim structure | CLAIM | *(needs code item C first)* | `scaling/results/phase2/claim/` | BLOCKED on code C |
| 8 | Phase 3 mechanism | CLAIM | `make -C scaling scaling-analyse PACKAGE=C TRIALS=results/phase1/claim/trials.csv OUT=results/phase1/claim/packages/c` | Package C | BLOCKED on steps 4-5 (+ timeseries) |
| 9 | Phase 6 fits | CLAIM | `make -C scaling scaling-analyse PACKAGE=F TRIALS=results/phase1/claim/trials.csv OUT=results/phase1/claim/packages/f` | Package F | BLOCKED on step 5 |
| 10 | Phase 4 transfer methods | CLAIM | *(needs code item D first)* | `packages/d` | BLOCKED on code D |
| 11 | Phase 5 info ladders | SCOUT then CLAIM | scout: `make -C scaling scaling-factor-sweep WORKERS=8`; claim needs code item E | `scaling/results/phase5/` | scout ready; claim BLOCKED on code E |
| 12 | Phase 7 early warning | CLAIM | `make -C scaling scaling-analyse PACKAGE=G TRIALS=... OUT=.../packages/g` | Package G | BLOCKED on steps 4-8 timeseries |

### Branch rule after step 1 (pilot)

- Compact still easy (D_min ~ 1, R high everywhere): prefer **2a** before full scout.
- Frontier already visible on smoke: go **2b** scout, then **3-4** claim.
- Soft frontier (bootstrap CI spans more than one D step): raise boundary seeds to 200 before Phase 2 claim.

### After every run

1. Check `status.json` / `manifest.jsonl`.
2. Write `REPORT.md` from the template into the protocol folder.
3. Set checklist Status (`TODO` / `RUNNING` / `DONE` / `SKIPPED`).
4. Add a row under **Done**.
5. If grade is CLAIM, update **Claims**.

---

## Done

| Date | Run | Result |
|------|-----|--------|
| 2026-09-17 | `phase1/scout` (stopped) | R=1, D_min=1, no overcrowding; 1123/1440 cells (local only) |
| 2026-09-17 | `phase1/pilot` (smoke) | Same picture on small N (local only) |
| 2026-09-21 | Cap gap close (no sims) | Claim procedure, I8-I12 depth, `phase1_claim` + make targets |

---

## Claims

Verdicts only. Criteria: [main_scaling_plan.md](main_scaling_plan.md) Claims. Update after a claim-grade `REPORT.md`.

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
