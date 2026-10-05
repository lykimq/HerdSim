# Package A -- Herdability map (phase4_fat_size_scout)

Auto-generated evidence package. Interpretation belongs in the protocol `REPORT.md`.

## Setup

- Protocol id: `scaling_v2`
- Reliability theta: 0.9
- Methods: ['fat']
- Layouts: ['compact']
- N grid: [5, 10, 25, 50, 75, 100, 150, 200, 300, 400]
- D grid: [1, 2, 3, 4, 6, 10, 15, 20, 25, 35]
- Seeds in export: 30 unique
- Trial rows: 3000
- Frontier rows: 10

## Diagnostics

- Trial rows: 3000
- Overall success rate: 0.501
- Top failure_mode counts:
  - none: 1503
  - oscillation: 1169
  - stuck: 199
  - timeout: 129
- Ticks: median=9370, p90=10000, max=10000
- Regime counts:
  - hard_failure: 80
  - wasteful_overspend: 17
  - efficient_operation: 3

## Claim stubs (auto, not final)

- C2a (overcrowding at theta=0.9): UNEVALUABLE on this export (no overcrowding regime / D_overcrowd).
- C2b (hard ceiling at T1): not evaluated here (requires extended-time campaign).
- C6 (scaling): DEGENERATE on this domain (constant D_min=1.0). Prefer harder X0 / larger N.

## Frontier summary

initial_layout  n_sheep  d_min d_overcrowd  d_max  b_star_d  b_star_t  b_star_effort  hard_failure
       compact        5    1.0        None   35.0       1.0   10000.0         534.00         False
       compact       10    1.0        None   35.0       3.0   10000.0         519.75         False
       compact       25    NaN        None    NaN       NaN       NaN            NaN          True
       compact       50    NaN        None    NaN       NaN       NaN            NaN          True
       compact       75    NaN        None    NaN       NaN       NaN            NaN          True
       compact      100    NaN        None    NaN       NaN       NaN            NaN          True
       compact      150    NaN        None    NaN       NaN       NaN            NaN          True
       compact      200    NaN        None    NaN       NaN       NaN            NaN          True
       compact      300    NaN        None    NaN       NaN       NaN            NaN          True
       compact      400    NaN        None    NaN       NaN       NaN            NaN          True

## Regime counts

regime
hard_failure           80
wasteful_overspend     17
efficient_operation     3

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

