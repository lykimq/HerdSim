# Protocol note: `phase4_kubo_structure_scout`

## Summary

Cheap Kubo structure map: 3,600 trials (3 N x 4 layouts x 10 D x 30 seeds). Used to plan claim windows. Not claim-grade by itself.

## Intent

- Phase / RQ: Phase 4 / RQ4
- Focus: Structure reliability map for claim windows
- Claims touched: none (SCOUT)
- Grade: SCOUT

## Setup

- Protocol: `scaling_v2`
- Method(s): kubo
- Layout(s) X0: compact, split, outlier_rich, wide
- N grid: {50, 100, 200}
- Seeds: 30
- Theta: 0.90
- T0: 10000
- obs_mode: global
- Output: `scaling/results/phase4/kubo_structure/scout/`

## Completeness

- Planned / done: 3,600 / 3,600 (`status.json` complete)

## Results

Scout Package B (`packages/b/frontier_by_layout.csv`) is a 30-seed sketch only. For outlier_rich N=200 the claim merge supersedes it: current answer is `D_min` = 20 at 200 seeds (no overcrowding). Read `../claim/README.md` and `../claim/outlier_rich_n200_window.json`.

## Links

- Claim (authoritative frontiers): `../claim/README.md`
- Phase note: `../../README.md`
- Guides: `../../guides/REPORT_en.html`
