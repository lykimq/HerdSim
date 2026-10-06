# Glossary

| Term | Definition |
|---|---|
| B* | Reliable `(D, T)` with the least median total shepherd path; ties favor smaller D, then faster median success |
| C, coverage | Fraction of peripheral sheep within the trial influence radius |
| cell | One fixed combination of method, layout, N, D, and any information factor, repeated over seeds |
| CLAIM | Precision grade, normally 100 seeds on planned cells; eligible for claims after documentation |
| cohesion | Mean distance of sheep to the flock centre of mass |
| D | Number of dogs or shepherds |
| D grid | Tested counts `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}` |
| D_max | Last reliable tested D before overcrowding, or tested-grid ceiling when no collapse is observed |
| D_min | Smallest tested D whose reliability reaches theta |
| D_overcrowd | First member of two consecutive post-D_min grid values below theta |
| efficient operation | Reliable cell whose median path is below the wasteful threshold |
| extent | Root-mean-square sheep distance to the centroid |
| finish time, `t_s` | First tick at which all sheep are inside the goal |
| fragmentation | Largest radius-5 connected sheep component divided by N |
| GCM | Geometric centre of mass of the flock |
| grade | Evidence level: SMOKE, SCOUT, CLAIM, or conditional T1 |
| grid ceiling | Largest tested value, D = 35; not a physical limit |
| hard failure | No D on the tested grid reaches theta |
| hull area | Area of the sheep convex hull |
| I | Information condition, such as observation, sensing range, or communication |
| `I_dir` | Directional conflict among moving shepherds; zero is aligned and one is fully cancelling |
| layout, X0 | Initial sheep arrangement: compact, wide, split, or outlier-rich |
| m, method | Dog controller |
| manifest | `manifest.jsonl`, the append-only ledger used to skip completed trial keys on resume |
| mean spread | Exported flock-spread score used by layout and prediction analysis |
| merged trials | Claim rows on reseeded cells plus scout rows on all other cells |
| N | Number of sheep |
| N grid | Tested sizes `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}` |
| overcrowding collapse | Unreliable cell at or above D_overcrowd after a reliable band |
| path, `shepherd_path` | Total Euclidean travel summed over every shepherd |
| path per dog | Total shepherd path divided by D |
| perimeter | Perimeter of the sheep convex hull |
| Pilot, SMOKE | Small pipeline check that is not evidence for claims |
| protocol | Resolved recipe defining factors, seeds, grade, output, and inherited canonical settings |
| provenance | Machine-readable record of protocol, seed list, code state, host, metrics, and timestamps |
| R | Fraction of independent seeds in a cell that succeed by the deadline |
| regime | Under-resourced, efficient, wasteful, overcrowding, or hard-failure classification |
| SCOUT | Broad 30-seed map used for planning and diagnostics, not claim verdicts |
| seed | Independent random repeat; the base list begins at master seed 2026 |
| success | Every sheep inside the goal disk before the deadline |
| T0 | Main deadline, 10,000 ticks |
| T1 | Conditional long deadline, 20,000 ticks, for overcrowding cells only |
| theta | Reliability threshold, 0.90 by default; 0.50 and 0.70 are sensitivities |
| tick | One discrete simulation update, not a wall-clock second |
| timeseries | Per-trial Parquet history used by trajectory and early-warning analysis |
| under-resourced failure | R below theta before a reliable or overcrowding band |
| wasteful overspend | Reliable cell whose median path exceeds B* by the configured tolerance |
| X0 | Initial-layout family |

## Failure labels

Failed trials may receive analysis-only labels: `stacking`, `split`, `scatter`, `oscillation`, `stuck`, or `timeout`. These labels describe heuristic failure modes and do not alter the binary success rule.

## Controller names

| Name | Short description |
|---|---|
| `strombom_multi` | Coordinated multi-dog collect-and-drive baseline |
| `kubo` | Local force-based sheep and dog controller with sensing and integration |
| `fat` | Strombom sheep with independent farthest-from-dog targeting |
| `communication_free` | Recommended transfer controller outside the required three-method set |
