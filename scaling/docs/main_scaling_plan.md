# Collective Herdability Under Shepherding

Protocol `scaling_v2`. Why / what: [herdsim_research_program.md](herdsim_research_program.md). Status: [progress_tracker.md](progress_tracker.md). Run strategy: [experiment_run_strategy.md](experiment_run_strategy.md). Report form: [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md). Draft reference: [sheep-scaling_paper2025.md](sheep-scaling_paper2025.md).

| Abbreviation | Meaning |
|--------------|---------|
| *method* | Dog algorithm |
| *R* / *theta* | Success rate; reliability threshold |
| *I_dir* | Shepherd interference index |
| *C* | Shepherd coverage of peripheral sheep |
| `B*` | Best (D, T) at target R with least path |
| *AUROC* | Ranking quality for early warning |
| *GCM* | Flock centre of mass |
| *S_bar* | Variance of distances to the centroid |

## Work map

| Phase | Focus | RQ | Package | Done when |
|-------|-------|----|---------|-----------|
| 0 | Freeze protocol | S8 | all | Section 8 matches `canonical_grid.yaml` |
| 1 | Size map | RQ2 | A | Merged R(N, D); D_min, D_overcrowd, D_max, B*; regimes |
| 2 | Structure at fixed N | RQ1 | B | D_min(N, X0) on {50, 100, 200}; predictor comparison |
| 3 | Mechanism | RQ3 | C | Within-N rank tests on contrast cells |
| 4 | Other methods | RQ4 | D | Transfer table for the three required methods, including structure |
| 5 | Information vs dogs | RQ5 | E | D_min(N, I) on {100, 200} |
| 6 | Scaling fits | RQ6 | F | Leave-one-N-out RMSE for power, piecewise, and per-layout curves |
| 7 | Early warning | RQ7 | G | Held-out AUROC and lead time on failure trials |

Smallest publishable unit: RQ1 + RQ2 + RQ3 + S8. RQ4 repeats the size map and the structure contrast. RQ5 and RQ7 come after that.

## How we measure

```text
R(m, tau, N, D, T, X0, I) = P(success | locked seeds)
```

Herdable at theta when R >= theta. Default theta = 0.90. Also report 0.50 and 0.70.

| Kind | Symbol | Meaning |
|------|--------|---------|
| Input | D | Shepherd count |
| Input | T | Time limit (ticks) |
| Outcome | S | Success (binary): every sheep inside the goal disk |
| Outcome | t_s | Time to success |
| Outcome | E | Total shepherd path length (`shepherd_path`) |
| Context | N | Flock size |
| Context | m | Method |
| Context | X0 | Initial layout family |
| Context | I | Information condition |

### Arena

Scaling runs use a 500 by 500 field. The flock starts at the center `(250, 250)`. The goal center is `(370, 250)`, so the drive length is 120 at every N. Goal radius is `15 * sqrt(N/50)` (15 at N = 50, about 42 at N = 400). Sheep start outside the goal and inside the field. The app's 150-field corner goal is unchanged.

Success is every sheep inside that disk. Strombom's collect switch `r_a * N^(2/3)` is wider than this goal (about 27 vs 15 at N = 50, about 109 vs 42 at N = 400). The pen is not opened up to that switch. A Strombom failure on this task is not read as a packing failure.

### Collective state and mechanism metrics

| Variable | Definition | Source |
|----------|------------|--------|
| Cohesion | Mean distance of sheep to the GCM | `plugins/metrics/cohesion.py` |
| Fragmentation | Largest connected-component fraction, radius 5 | `plugins/metrics/fragmentation.py` |
| Outlier count | Sheep beyond `r_a * N^(2/3)` | `plugins/metrics/outlier_count.py` |
| Spread | Variance of distances to the centroid | `plugins/metrics/mean_spread.py` |
| Extent | RMS distance to the centroid | `plugins/metrics/extent.py` |

| Metric | Definition |
|--------|------------|
| I_dir(t) | `1 - \|\|sum u_hat\|\| / M_active` for shepherds with speed above 1e-6. 0 = aligned, 1 = conflict. If none move, I_dir = 0. Uses realised velocities. |
| C(t) | Fraction of peripheral sheep (distance to GCM above the median) inside the trial's influence radius. That radius is `sensing_range` when set, otherwise the method `r_s`. Missing radius yields NaN. |

### Frontiers and regimes

| Quantity | Definition |
|----------|------------|
| D_min | Smallest D with R >= theta |
| D_overcrowd | Smallest D > D_min such that this grid D and the next grid D both have R < theta |
| D_max | Largest D with R >= theta that is still below D_overcrowd. If that run does not exist, the largest tested D that still meets theta (a grid ceiling) |
| B* | (D, T) with R >= theta and minimum median path. Ties: smaller D, then faster median t_s |

| Regime | Rule |
|--------|------|
| Under-resourced failure | R < theta and D is below D_overcrowd |
| Efficient operation | R >= theta and median path is below the wasteful bar |
| Wasteful overspend | R >= theta and median path >= 20% above B* (also report 10% and 30%) |
| Overcrowding collapse | R < theta for D >= D_overcrowd |
| Hard failure | No tested D reaches R >= theta |

Effects are in grid steps. The dog-count gap equals the local spacing of `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.

### Claim-grade map

Operator narrative (verbs, artifacts, why we stage): [experiment_run_strategy.md](experiment_run_strategy.md).

Scout: 30 seeds on every frozen (N, D) cell.

Then, per (method, layout, N), reseed at 100 seeds:

- Reliability window: scout D_min, plus the previous and next grid D.
- Overcrowding window, only if two consecutive D after that candidate are below theta: those two D and the last D still at or above theta.
- If no D meets theta: the two largest D.

Merge: a cell with claim seeds is analysed at those 100 only. Other cells stay at 30. Scout rows are not stacked on claim rows.

Bootstrap: 1,000 resamples of seeds within each D. A resample with no D_min stays in the sample as above the largest tested D. The 2.5 and 97.5 percentiles use rank order and are grid D values, or "above grid" when that tail is censored.

If the interval on D_min covers more than one grid step, raise that window to 200 seeds before the structure claim.

At R = 0.90 and n = 100 the interval on R is about +/-0.06. That is an interval on R.

### Trial totals

Planning figures. Recompute after the scout. One size map: 100 cells at 30, plus up to 6 D per N at 100, about 3,000 + 6,000 simulations. One structure contrast (3 N x 4 layouts x 10 D): about 3,600 + 7,200. T1: 100 seeds at 20,000 ticks on the D that define D_overcrowd. Core (baseline size + T1 + structure) is on the order of 20,000 simulations. Each required transfer method repeats the size map and the structure contrast. The structure row of the transfer table waits for those runs. `communication_free` is recommended and is outside the minimum set (`strombom_multi`, `kubo`, `fat`).

These trials support claim-grade D_min and regimes for the baseline, a structure contrast at three sizes, and mechanism tests on cells already collected. They do not support a method-general law from the baseline alone, a universal law for other tasks or real farms, or a dog-count gap smaller than one grid step.

## How we run each RQ

### RQ1 Structure (Package B, Phase 2)

Does the same N have a different D_min under a different X0?

N in {50, 100, 200}. Layouts: compact, wide, split, outlier_rich. Full D grid. Compare D_min in grid steps. The regression compares (N, D) with (N, D plus layout and the first 100 ticks), holding out whole N. Supported when the state model has lower out-of-sample negative log-likelihood. Full-trial means are not predictors.

### RQ2 Size (Package A, Phase 1)

R(N, D) at T0 on the frozen grids, baseline method, compact layout. Label regimes. T1 on the overcrowding D values.

### RQ3 Mechanism (Package C, Phase 3)

Compare efficient and overcrowding cells at the same N. One median per (N, D) cell. Rank tests, Holm across hypotheses.

| Hypothesis | Signature |
|------------|-----------|
| Interference | Higher median I_dir in overcrowding cells |
| Induced fragmentation | Lower largest-component fraction in overcrowding cells |
| Coverage saturation | Among reliable cells, median coverage stays above 0.5, the range across D is under 0.1, and median path rises. A near-zero curve is not saturation |
| Redundant effort | Higher median path while reliability does not gain |

No new grid. If a method has no overcrowding label, this contrast is undefined for it.

### RQ4 Generality (Package D, Phase 4)

Required: `strombom_multi`, `kubo`, `fat`. Recommended: `communication_free`.

| Property | shared | shifted | absent |
|----------|--------|---------|--------|
| D_min | equal grid D | different grid D | one side has no D_min |
| Overcrowding | present on both, D/N within 1.5x | present at a wider gap | not on both |
| I_dir | r(I_dir, success) < -0.3 on both | the sign pattern differs in magnitude | not significant |
| Coverage saturation | the saturation rule holds on both | it holds on one | it holds on neither |

State-dependent D_min is filled only when each method has the structure contrast.

### RQ5 Information (Package E, Phase 5)

N in {100, 200}. Ladders: obs `bearing_only`, `local_positions`, `global`; range `0.5, 1, 1.5, 2` times the method `r_s` (65 for Strombom); comm `none`, `neighbour_broadcast`, `global_shared`.

On `strombom_multi`: `none` uses each dog's own observation; `neighbour_broadcast` adds dogs inside that dog's sensing radius; `global_shared` uses the union of sensed sheep, not true positions from the simulator. Report the ladder as what this controller consumes.

C5a: one step lowers D_min by at least one grid step. C5b: the second step saves fewer dogs than the first.

### RQ6 Fits (Package F, Phase 6)

Candidates: constant, linear, power law `A * N^alpha` fit in dog-count units, and a two-piece linear model. Choice is leave-one-N-out RMSE. C6a: power law loses to the piecewise model or to separate curves per layout on that RMSE. C6b: in a stated N and X0 band, the slope of log D on log N is below 1.

### RQ7 Early warning (Package G, Phase 7)

At ticks 1,000, 1,200, ..., 8,000, features use only `(t - 200, t]`. The label is failure within the next 500 ticks, and only when t + 500 is still inside T0. The state model and the (N, D) logistic are fit on other N. Lead time is the gap from the first crossing of the training threshold until failure, and it may exceed 500. The fraction with lead time >= 500 uses every failure trial. C7a: held-out state AUROC above the (N, D) baseline. C7b: that fraction is at least 30%.

## Claims

| Claim | RQ | Supported when |
|-------|----|----------------|
| C1a | RQ1 | For at least one N, D_min differs by at least one D-grid step across X0 at theta 0.90 |
| C1b | RQ1 | State model has lower out-of-sample negative log-likelihood than (N, D), leave-one-N-out |
| C2a | RQ2 | Baseline method shows overcrowding at theta 0.90 for at least one N |
| C2b | RQ2 | Some D above D_overcrowd still has R < theta at T = 20,000 |
| C3 | RQ3 | Overcrowding cells differ from efficient cells on I_dir and/or fragmentation at the same N (rank p < 0.05, Holm) |
| C4 | RQ4 | D_min or overcrowding is shared across the three required methods. The structure row needs the structure runs |
| C5a | RQ5 | One ladder step lowers D_min by at least one grid step at N in {100, 200} |
| C5b | RQ5 | The second step saves fewer dogs than the first |
| C6a | RQ6 | Power law has higher leave-one-N-out RMSE than piecewise or per-layout curves |
| C6b | RQ6 | Slope of log D_min on log N is below 1 in a stated N and X0 band |
| C7a | RQ7 | Held-out state AUROC above the (N, D) baseline |
| C7b | RQ7 | Lead time >= 500 ticks on at least 30% of failure trials |

Verdicts: UNEVALUATED / SUPPORTED / REJECTED / INCONCLUSIVE. The tracker holds them. Fill only at CLAIM grade.

## Protocol freeze (Section 8)

Machine-readable: [../configs/canonical_grid.yaml](../configs/canonical_grid.yaml). Subsets: [../configs/protocols/](../configs/protocols/).

| Item | Value |
|------|-------|
| Task | `drive_to_goal` |
| Field | 500 by 500, flock at center, goal center `(370, 250)` |
| Goal radius | `15 * sqrt(N/50)` |
| Theta | 0.90 (also report 0.50, 0.70) |
| Baseline | `strombom_multi` |
| Required transfer | `strombom_multi`, `kubo`, `fat` |
| N | {5, 10, 25, 50, 75, 100, 150, 200, 300, 400} |
| D | {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} |
| X0 | compact, wide, split, outlier_rich |
| Structure N | {50, 100, 200} |
| Information N | {100, 200} |
| T0 / T1 | 10,000 / 20,000 |
| Scout / claim seeds | 30 / 100 |
| Master seed | 2026 |
| Bootstrap | 1,000 |
| Predictor window | first 100 ticks |
| RQ7 k / w / eval | 500 / 200 / 1,000..8,000 step 200 |
| Wasteful bar | 20% (report 10% and 30%) |

### Why these values

**Radius 15 at N = 50.** This is the app's goal at the default flock. Packed radius there is about 8. Radius 8 would jam. Radius 30 would be a pasture and would lower D_min because the target got easier.

**`sqrt(N/50)`.** Area per sheep stays constant. A fixed radius jams by N = 400 (packed radius about 23). Strombom's switch `2 * N^(2/3)` belongs to one controller and would make large N easier for every method.

**Drive 120.** At speed 1 a straight crossing takes 120 ticks. At N = 400 the near edge of the goal is 78 from the flock: outside a compact start and past one wide sigma. Length 80 sits inside the wide cloud. Length 200 puts the far edge of the goal on the wall of a 500 field.

**Field 500, goal at `(370, 250)`.** Half-width 250 covers a wide 3-sigma draw (180) with margin about 70, and the N = 400 outlier reach (about 174). A 150 field cannot. A 400 field leaves about 20 on the wide draw. A 1000 field adds empty space. The goal is on the midline so the vertical margins match. The field is square so split clusters on a circle are not pushed into a short side.

**N floor 5.** Below that there is no collective: no sheep-sheep interaction at N = 1, an 80/20 split is a different factor at N = 2 to 4, and periphery-by-median is almost everyone. N = 5 and 10 keep the small-flock regime. The floor is not 20.

**N points.** Ten sizes, tighter around 100, where one dog stops being enough in the draft. 75 and 150 locate that change. 300 and 400 give the large-N slope more than one step. 250 and 350 are omitted because each extra N is a full dog sweep. A step of 50 from 50 to 400 is more sizes than a two-piece fit uses.

**D points.** Steps of 1 from 1 to 4, where D_min usually sits. Wider after that, because the question is whether a large increase helps or hurts, and a 2-dog gap is smaller than the high-D step. The cap is 35 because that is where a few shepherds ends. Every integer to 35 would make the scout about 10,500 trials instead of 3,000.

**Theta 0.90.** Reliable band, the same cut as the draft. 0.50 is reported and is not the bar for D_min. 0.99 at 100 seeds would mark stable cells as short.

**T0 = 10,000.** About 80 straight crossings, so timeout means loss of control. The scenario default 3,000 would mix slow successes into failures. T1 = 20,000 is only for overcrowding cells.

**Seeds 30 and 100.** At R = 0.90 the standard error is about 0.055 at 30 (enough to separate a broken cell from a solid one) and about 0.03 at 100. Ten seeds flip the window. 200 is the raise when the D_min interval covers more than one grid step. The seed base 2026 is a fixed integer so the two stages share a list.

**Bootstrap 1,000.** The interval resamples seeds already run. 1,000 puts about 25 draws in each 2.5% tail. 100 leaves two or three.

**Layouts.** Spread 30. Compact sigma 9 matches the packed radius at N = 50. Wide sigma 60 is a clear cohesion gap that still fits; sigma 120 would leave the field. Split uses 2 clusters below N = 12 (three clusters of five sheep are not subflocks) and gaps of at least 10. Outliers are 20% (50% would be a second flock; 5% is not one sheep at N = 5).

**Fragmentation radius 5.** Neighbors in a compact flock sit near 2 to 4, so radius 5 joins them. Split gaps are at least 10, so radius 5 leaves them apart. Radius 2 would split a slightly loose compact flock. Radius 15 would bridge the split.

**Coverage radius.** The distance at which sheep react to a dog (`r_s = 65` for Strombom, or `sensing_range` when that factor is set). Radius 2 is sheep-sheep repulsion.

**Outlier threshold `r_a * N^(2/3)`.** Same distance the collect/drive switch uses. A fixed 15 would mean a different fraction of the flock at N = 5 and at N = 400.

**I_dir cutoff 1e-6.** Numerical dust. A cutoff of 0.1 would drop dogs that are still steering.

**Wasteful 20%.** 10% sits in the noise of path length. 50% would only mark extreme overspend. 10% and 30% are reported beside 20%.

**Predictor window 100.** Shorter than the 120-tick drive, so a straight success is not inside the features. The first 200 ticks would include easy arrivals.

**Early warning.** Eval starts at 1,000 because tick 0 is the layout. It stops at 8,000 so that 8,000 + 500 is still before timeout. Step 200 matches the feature window. Window 200 is longer than one burst and shorter than the 500-tick horizon. A horizon of 100 is less than one drive. A horizon of 2,000 is a fifth of the trial.

**Information ladder.** Relative steps so another method's base range uses the same rungs. Four rungs support a first step and a second step. Claim N is 100 and 200. N = 50 is skipped when D_min is already 1.

**Structure N {50, 100, 200}.** Easy size, size edge, and the steep band. Four layouts: spread, fragmentation, outliers, and compact as the reference.

**Claim window.** One cell is not enough: 30 seeds can place the crossing on the wrong D. The whole grid at 100 seeds spends the draft's budget on interiors that do not move D_min. Overcrowding needs two consecutive D below theta: one dip can be noise, and requiring the rest of the grid to stay down would miss a collapse that later recovers.

**Transfer of D_min.** Shared means the same grid D. "Within 2 dogs" is smaller than the high-D step.

**Leave-one-N-out.** Holding out random trials keeps other seeds of the same size in training.

### Layout contract

| Layout | Definition | Gate |
|--------|------------|------|
| compact | Gaussian, sigma = 0.3 x spread | Lower cohesion distance than wide |
| wide | Gaussian, sigma = 2.0 x spread | Higher cohesion distance than compact |
| split | 2 clusters below N = 12, else 3, gap >= 2 x measurement radius | Lower fragmentation index than compact |
| outlier_rich | Core about 80%, outliers about 20% beyond `r_a * N^(2/3)` | Higher outlier count than compact |

Points that would leave the field or land in the goal are redrawn. They are not moved onto the boundary.

### Caps

| Cap | Role | Location |
|-----|------|----------|
| I1 | Grid runner, resume, provenance | `scaling/services/scaling/runner.py` |
| I2 | Frontiers, claim windows, bootstrap | `analysis/scaling/frontier.py` |
| I3 | Regimes | `analysis/scaling/regimes.py` |
| I4 | Mean-spread, extent | `plugins/metrics/mean_spread.py`, `extent.py` |
| I5 | X0 generators | `core/x0_generators.py` |
| I6 | State vs (N, D) | `analysis/scaling/predictors.py` |
| I7 | I_dir, coverage | `plugins/metrics/shepherd_interference.py`, `shepherd_coverage.py` |
| I8 | Mechanism tests | `analysis/scaling/mechanism.py` |
| I9 | Transfer table | `analysis/scaling/transfer.py` |
| I10 | Factor sweeps | `scaling/scripts/run_factor_sweep.py`, `analysis/scaling/substitution.py` |
| I11 | Fits | `analysis/scaling/fits.py` |
| I12 | Early warning | `analysis/scaling/early_warning.py` |
| I13 | Canonical config, export | `scaling/configs/canonical_grid.yaml`, `analysis/scaling/export.py` |
| I14 | Parquet timeseries | runner write path |

### Paths

```text
analysis/scaling/          # packages A-G
scaling/services/scaling/  # runner
scaling/configs/           # canonical_grid.yaml + protocols/
scaling/scripts/           # campaign, run_grid, plan_claim_cells, plan_t1_cells,
                           # run_factor_sweep, analyse
scaling/results/phase{k}/{protocol}/
```

CLI: `make -C scaling help` or `uv run scaling/scripts/campaign.py help`.
Campaigns: Phase 1 size/claim/T1, Phase 2 structure, Phase 4 transfer
(`TRANSFER_METHOD=kubo|fat`), Phase 5 obs/range/communication.

### Do not modify, and E1

Leave the app's default 150 field and radius-15 goal. Leave sheep models and dog force laws. E1 (intended velocities) is unbuilt until a claim-grade map shows I_dir spikes only at walls.

### Threats

| Threat | What we do |
|--------|------------|
| Single task | RQ4 changes method. A second task is optional after RQ1-RQ3 |
| Strombom switch wider than the goal | Stated in the arena section. Not treated as packing |
| Discrete ticks, sheep speed 1 | Report both. Results are at this resolution |
| Simulated methods | Claims stay inside the simulation |
| Soft frontier | If the D_min interval covers more than one grid step, raise the window to 200 seeds |
