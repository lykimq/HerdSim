# Package A: Herdability map (phase4_fat_size_claim)

Evidence package export. Interpretation belongs in the protocol `README.md`.

## Setup

- Protocol id: `scaling_v2`
- Reliability theta: 0.9
- Methods: fat
- Layouts: compact
- N grid: 5, 10, 25, 50, 75, 100, 150, 200, 300, 400
- D grid: 1, 2, 3, 4, 6, 10, 15, 20, 25, 35
- Seeds in export: 100 unique
- Trial rows: 4400
- Frontier rows: 10

## Diagnostics

- Trial rows: 4400
- Overall success rate: 0.499
- Top failure_mode counts:
  - none: 2194
  - oscillation: 1707
  - stuck: 295
  - timeout: 204
- Ticks: median=10000, p90=10000, max=10000
- Regime counts:
  - hard_failure: 80
  - wasteful_overspend: 17
  - efficient_operation: 3

## Claim stubs (auto, not final)

- C2a (overcrowding at theta=0.9): UNEVALUABLE on this export (no overcrowding regime / D_overcrowd).
- C2b (hard ceiling at T1): not evaluated here (requires extended-time campaign).
- C6 (scaling): DEGENERATE on this domain (constant D_min=1.0). Prefer harder X0 / larger N.

## Frontier summary

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | b_star_t | b_star_effort | hard_failure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compact | 5 | 1 |  | 35 | 1 | 10000 | 630 | no |
| compact | 10 | 1 |  | 35 | 3 | 10000 | 519.75 | no |
| compact | 25 |  |  |  |  |  |  | yes |
| compact | 50 |  |  |  |  |  |  | yes |
| compact | 75 |  |  |  |  |  |  | yes |
| compact | 100 |  |  |  |  |  |  | yes |
| compact | 150 |  |  |  |  |  |  | yes |
| compact | 200 |  |  |  |  |  |  | yes |
| compact | 300 |  |  |  |  |  |  | yes |
| compact | 400 |  |  |  |  |  |  | yes |

## Regime counts

| regime | count |
| --- | --- |
| hard_failure | 80 |
| wasteful_overspend | 17 |
| efficient_operation | 3 |

## Artefacts

- trials.csv
- reliability.csv
- frontier.csv
- regimes.csv
- dmin_bootstrap.csv
- provenance.json
- figures/ (moved to docs)

