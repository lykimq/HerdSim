# Package A: Herdability map (phase1_scout)

Evidence package export. Interpretation belongs in the protocol `README.md`.

## Setup

- Protocol id: `scaling_v2`
- Reliability theta: 0.9
- Methods: strombom_multi
- Layouts: compact
- N grid: 5, 10, 25, 50, 75, 100, 150, 200, 300, 400
- D grid: 1, 2, 3, 4, 6, 10, 15, 20, 25, 35
- Seeds in export: 30 unique
- Trial rows: 3000
- Frontier rows: 10

## Diagnostics

- Trial rows: 3000
- Overall success rate: 0.983
- Top failure_mode counts:
  - none: 2949
  - oscillation: 33
  - stuck: 18
- Ticks: median=182, p90=192, max=10000
- Regime counts:
  - wasteful_overspend: 88
  - efficient_operation: 10
  - under_resourced_failure: 2

## Claim stubs (auto, not final)

- C2a (overcrowding at theta=0.9): UNEVALUABLE on this export (no overcrowding regime / D_overcrowd).
- C2b (hard ceiling at T1): not evaluated here (requires extended-time campaign).
- C6 (scaling): frontier varies with N; run Package F fits before deciding C6a/C6b.

## Frontier summary

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | b_star_t | b_star_effort | hard_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compact | 5 | 2 |  | 35 | 2 | 10000 | 337.899 | no |
| compact | 10 | 2 |  | 35 | 2 | 10000 | 330.492 | no |
| compact | 25 | 1 |  | 35 | 1 | 10000 | 163.5 | no |
| compact | 50 | 1 |  | 35 | 1 | 10000 | 157.5 | no |
| compact | 75 | 1 |  | 35 | 1 | 10000 | 154.897 | no |
| compact | 100 | 1 |  | 35 | 1 | 10000 | 161.414 | no |
| compact | 150 | 1 |  | 35 | 1 | 10000 | 153.216 | no |
| compact | 200 | 1 |  | 35 | 1 | 10000 | 143.619 | no |
| compact | 300 | 1 |  | 35 | 1 | 10000 | 131.329 | no |
| compact | 400 | 1 |  | 35 | 1 | 10000 | 119.505 | no |

## Regime counts

| regime | count |
| --- | --- |
| wasteful_overspend | 88 |
| efficient_operation | 10 |
| under_resourced_failure | 2 |

## Artefacts

- trials.csv
- reliability.csv
- frontier.csv
- regimes.csv
- dmin_bootstrap.csv
- provenance.json
- figures/ (moved to docs)

