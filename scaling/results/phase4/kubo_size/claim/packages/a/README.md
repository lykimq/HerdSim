# Package A: Herdability map (phase4_kubo_size_claim)

Evidence package export. Interpretation belongs in the protocol `README.md`.

## Setup

- Protocol id: `scaling_v2`
- Reliability theta: 0.9
- Methods: kubo
- Layouts: compact
- N grid: 5, 10, 25, 50, 75, 100, 150, 200, 300, 400
- D grid: 1, 2, 3, 4, 6, 10, 15, 20, 25, 35
- Seeds in export: 100 unique
- Trial rows: 4470
- Frontier rows: 10

## Diagnostics

- Trial rows: 4470
- Overall success rate: 0.991
- Top failure_mode counts:
  - none: 4428
  - timeout: 42
- Ticks: median=829, p90=1848, max=10000
- Regime counts:
  - wasteful_overspend: 87
  - efficient_operation: 11
  - under_resourced_failure: 2

## Claim stubs (auto, not final)

- C2a (overcrowding at theta=0.9): UNEVALUABLE on this export (no overcrowding regime / D_overcrowd).
- C2b (hard ceiling at T1): not evaluated here (requires extended-time campaign).
- C6 (scaling): frontier varies with N; run Package F fits before deciding C6a/C6b.

## Frontier summary

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | b_star_t | b_star_effort | hard_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compact | 5 | 3 |  | 35 | 3 | 10000 | 994.939 | no |
| compact | 10 | 1 |  | 35 | 1 | 10000 | 117.988 | no |
| compact | 25 | 1 |  | 35 | 1 | 10000 | 116.53 | no |
| compact | 50 | 1 |  | 35 | 1 | 10000 | 117.067 | no |
| compact | 75 | 1 |  | 35 | 1 | 10000 | 114.147 | no |
| compact | 100 | 1 |  | 35 | 1 | 10000 | 112.988 | no |
| compact | 150 | 1 |  | 35 | 1 | 10000 | 111.519 | no |
| compact | 200 | 1 |  | 35 | 1 | 10000 | 111.428 | no |
| compact | 300 | 1 |  | 35 | 1 | 10000 | 107.317 | no |
| compact | 400 | 1 |  | 35 | 1 | 10000 | 104.364 | no |

## Regime counts

| regime | count |
| --- | --- |
| wasteful_overspend | 87 |
| efficient_operation | 11 |
| under_resourced_failure | 2 |

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

