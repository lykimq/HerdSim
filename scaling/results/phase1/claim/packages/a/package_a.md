# Package A -- Herdability map (phase1_claim)

Auto-generated evidence package. Interpretation belongs in the protocol `REPORT.md`.

## Setup

- Protocol id: `scaling_v2`
- Reliability theta: 0.9
- Methods: ['strombom_multi']
- Layouts: ['compact']
- N grid: [5, 10, 25, 50, 75, 100, 150, 200, 300, 400]
- D grid: [1, 2, 3, 4, 6, 10, 15, 20, 25, 35]
- Seeds in export: 100 unique
- Trial rows: 4467
- Frontier rows: 10

## Diagnostics

- Trial rows: 4467
- Overall success rate: 0.977
- Top failure_mode counts:
  - none: 4366
  - stuck: 58
  - oscillation: 43
- Ticks: median=183, p90=196, max=10000
- Regime counts:
  - wasteful_overspend: 88
  - efficient_operation: 10
  - under_resourced_failure: 2

## Claim stubs (auto, not final)

- C2a (overcrowding at theta=0.9): UNEVALUABLE on this export (no overcrowding regime / D_overcrowd).
- C2b (hard ceiling at T1): not evaluated here (requires extended-time campaign).
- C6 (scaling): frontier varies with N; run Package F fits before deciding C6a/C6b.

## Frontier summary

initial_layout  n_sheep  d_min d_overcrowd  d_max  b_star_d  b_star_t  b_star_effort  hard_failure
       compact        5      2        None     35         2   10000.0     335.075721         False
       compact       10      2        None     35         2   10000.0     328.756221         False
       compact       25      1        None     35         1   10000.0     163.500000         False
       compact       50      1        None     35         1   10000.0     157.500000         False
       compact       75      1        None     35         1   10000.0     155.891108         False
       compact      100      1        None     35         1   10000.0     161.351674         False
       compact      150      1        None     35         1   10000.0     153.027254         False
       compact      200      1        None     35         1   10000.0     144.171242         False
       compact      300      1        None     35         1   10000.0     130.811346         False
       compact      400      1        None     35         1   10000.0     119.833113         False

## Regime counts

regime
wasteful_overspend         88
efficient_operation        10
under_resourced_failure     2

## Figures

- heatmap: `figures/reliability_heatmap.png`
  ![heatmap](figures/reliability_heatmap.png)

- frontier: `figures/frontier_dmin.png`
  ![frontier](figures/frontier_dmin.png)

- regimes: `figures/regime_counts.png`
  ![regimes](figures/regime_counts.png)

## Artefacts

- trials.csv
- reliability.csv
- frontier.csv
- regimes.csv
- dmin_bootstrap.csv
- provenance.json
- figures/

