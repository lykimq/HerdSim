# Protocol report template
#
# Copy to: scaling/results/phase{k}/{protocol}/REPORT.md
# Fill after looking at packages/{a-g}/.
# Leave the auto package_*.md files alone; this file is the hand-written note.

# Protocol report: `<protocol_id>`

## Summary

What we ran, what came out, what to do next.

## Intent

- Phase / RQ:
- Size / Structure / Mechanism / Generality / follow-on:
- Claims (C1a-C7b):
- Grade: SMOKE | SCOUT | CLAIM

## Setup

- Protocol: `scaling_v1` (frozen: )
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
- Host (see tracker Section 6 if not primary):
- WORKERS / CPU governor:

## Completeness

- Planned cells:
- Done:
- `status.json` complete? yes / no
- Resume notes:

## Results

- Success pattern:
- D_min / frontier (by N / layout):
- Regimes (too few / efficient / wasteful / overcrowding / hard failure):
- Surprises:

## Figures

From `packages/*/figures/` (tick what you looked at):

- [ ] Reliability heatmap R(N, D)
- [ ] Frontier D_min(N) (+ D_overcrowd / D_max if present)
- [ ] Regime counts
- [ ] Other (Phase 2+):

## Interpretation

What we think is going on (mechanism / structure / method). Cite I_dir,
coverage, fragmentation, predictors if you have them.

## Limits

What this run does **not** support (grade, protocol drift, single method,
unfinished cells, etc.).

## Claims update

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
