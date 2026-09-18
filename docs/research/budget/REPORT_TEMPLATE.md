# Human campaign report template
#
# Copy to: results/budget/phase{k}/{campaign}/REPORT.md
# Fill after reading auto packages under packages/{a-g}/.
# Do not replace auto `package_*.md` files with this document.

# Campaign report: `<campaign_id>`

## Executive summary

One short paragraph: what we ran, the main result, and the decision this implies.

## Intent

- Phase / formal RQ:
- Reader question (Size / Structure / Mechanism / Generality / follow-on):
- Claims targeted (C1a-C7b):
- Grade goal: SMOKE | SCOUT | CLAIM

## What we did (how)

- Protocol: `shepherding_budget_v1` (frozen date: )
- Task / success rule:
- Instrument(s):
- Layout(s) X0:
- Grid N:
- Grid D:
- Seeds (scout / claim):
- Time limit T0 (and T1 if used):
- Theta:
- Command used:
- Output path: `results/budget/phase{k}/{campaign}/`

## Completeness

- Planned cells:
- Completed cells:
- `status.json` complete? yes / no
- Resume notes:

## What happened (results)

- Overall success pattern:
- D_min / frontier (by N and layout if any):
- Regimes seen (too few / efficient / wasteful / overcrowding / hard failure):
- Surprises / anomalies:

## Figures to review

Link or list auto figures from `packages/*/figures/` (and any extra plots):

- [ ] Reliability heatmap R(N, D)
- [ ] Frontier D_min(N) (+ D_overcrowd / D_max if present)
- [ ] Regime counts
- [ ] Other (Phase 2+):

## Why we think that

Mechanism / structure / method interpretation in plain language. Point to metrics
(I_dir, coverage, fragmentation, predictors) when available.

## What we do not claim

Limits of grade, protocol drift vs Section 8, single-method scope, unfinished cells, etc.

## Claims board update

| Claim | Verdict | Evidence pointer |
|-------|---------|------------------|
| C? | UNEVALUATED / SUPPORTED / REJECTED / INCONCLUSIVE | `packages/...` |

## Decision / next action

- Keep grinding this grid? switch to harder X0? change method? raise seeds?
- Tracker updates needed:

## Links

- Auto Package A: `packages/a/package_a.md`
- Other packages:
- `status.json`, `provenance.json`, `campaign.yaml`
