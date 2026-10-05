# Protocol report template
#
# Copy to: scaling/results/phase{k}/{protocol}/REPORT.md
# Fill after looking at packages/{a-g}/.
# Leave the auto package_*.md files alone; this file is the hand-written note.
# Claim criteria: main_scaling_plan.md (Claims). Copy verdicts into progress_tracker.md.

# Protocol report: `<protocol_id>`

## Summary

What we ran, what came out, what to do next.

## Intent

- Phase / RQ:
- Focus (Size / Structure / Mechanism / Generality / follow-on):
- Claims touched (C1a-C7b): leave blank at run start; fill Claims update after packages
- Grade: SMOKE | SCOUT | CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule:
- Method(s):
- Layout(s) X0:
- N grid:
- D grid:
- Seeds (scout / claim):
- T0 (and T1 if used):
- Theta:
- Command:
- Output: `scaling/results/phase{k}/{protocol}/`
- Host:
- WORKERS / CPU governor:

## Completeness

- Planned cells:
- Done:
- `status.json` complete? yes / no
- Resume notes:

## Results

- Success pattern:
- D_min / frontier (by N / layout):
- Regimes (under-resourced / efficient / wasteful / overcrowding / hard failure):
- Surprises:

## Figures

From `packages/*/figures/` (tick what you looked at):

- [ ] Reliability heatmap R(N, D)
- [ ] Frontier D_min(N) (+ D_overcrowd / D_max if present)
- [ ] Regime counts
- [ ] Other (Phase 2+):

## Interpretation

What we think is going on (mechanism / structure / method). Cite I_dir, coverage, fragmentation, predictors if present.

## Limits

What this run does **not** support (grade, protocol drift, single method, unfinished cells, etc.).

## Claims update

CLAIM grade only, after `packages/*/`. Criteria: [main_scaling_plan.md](main_scaling_plan.md) Claims. Then copy rows into the tracker.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C? | UNEVALUATED / SUPPORTED / REJECTED / INCONCLUSIVE | `packages/...` |

## Next

- Keep this grid / harder X0 / other method / more seeds?
- Tracker updates:

## Links

- Package A: `packages/a/package_a.md`
- Other packages:
- `status.json`, `provenance.json`, `protocol.yaml`, `trials.csv`
