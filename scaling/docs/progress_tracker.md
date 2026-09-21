# Scaling progress tracker

Role: **status** (now / next / done / claim verdicts)
Why / what: [herdsim_research_program.md](herdsim_research_program.md)
How: [main_scaling_plan.md](main_scaling_plan.md) (Work map, Section 8, Claims)
Report form: [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)
Help: `make -C scaling help`

Last updated: 2026-09-21

---

## Now

- Phase 0 **DONE** (`scaling_v1` frozen).
- Caps I1-I14 **BUILT** (unit-tested). Claim-grade Phases 1-7 **NOT STARTED**.

| Phase | Status |
|-------|--------|
| 0 | DONE |
| 1 | NOT STARTED |
| 2 | NOT STARTED |
| 3 | BLOCKED (needs contrast from 1-2) |
| 4 | NOT STARTED |
| 5 | NOT STARTED |
| 6 | NOT STARTED |
| 7 | NOT STARTED |

---

## Next

1. `make -C scaling scaling-pilot WORKERS=4` -> `scaling/results/phase1/pilot/`
2. If compact still D_min ~ 1: skip scout grind; run `make -C scaling scaling-pilot-state WORKERS=4` -> `scaling/results/phase2/pilot_state/`
3. After each run: write `REPORT.md` from the template, then update **Now** / **Done** here.

Host: `gwen`. Prefer `WORKERS=8` (up to 12-16 if plugged in, performance governor).

---

## Done

| Date | Run | Result |
|------|-----|--------|
| 2026-09-17 | `phase1/scout` (stopped) | R=1, D_min=1, no overcrowding; 1123/1440 cells |
| 2026-09-17 | `phase1/pilot` (smoke) | Same picture on small N |

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
