# Task design and experimental method

How HerdSim sizes the herding task, places the flock and dogs, samples cells adaptively, and turns each curve of trials into critical team sizes and zones.

## 1. Task geometry and scale

### Why the field grows with the flock

As in Strombom et al. (2014), the field is open and has no walls or boundaries; it only sets the start and goal coordinates. Because a fixed goal radius would be oversized for $N = 25$ and too small to hold $N = 400$, HerdSim scales the goal and drive distance by the calibrated flock radius $R_f(N)$, the radius a flock of $N$ sheep settles to when driven by one dog (Figure 1, Table 1).

![Task geometry and physical scaling](../figures/fig6_task_geometry.png)

**Figure 1: Task geometry drawn to scale.** The flock and goal radii grow slowly with $N$, and the drive distance is the largest of three terms.

- Marks: each dot in the middle and right panels is one of the five main flock sizes ($N = 25, 50, 100, 200, 400$).
- Left: the field at $N = 200$, showing the settled flock circle ($R_f = 10.5$ m, solid black ring around the flock centre `+`), the maximum start radius across all four [start layouts](#flock-start-layouts) ($l_{\mathrm{reach}} = 109.4$ m, outer ring of `outlier_rich`, dashed blue circle), the goal ($R_{\mathrm{goal}} = 19.9$ m, green circle), and the drive distance $l = 139.8$ m between centres.
- Middle: the drive distance $l$ against $N$ with its three terms from Table 1; the largest (grey) sets $l$.
- Right: $R_f(N)$ and the goal radius $1.9 R_f$.

### Sizing by the calibrated flock radius

At the start of a campaign, calibration measures $R_f(N)$ once for each flock size $N$, defined as $\sqrt{2}$ times the root-mean-square (RMS) distance of the sheep from the flock centre (the radius of a uniform disc with the same RMS). One dog drives a compact flock for 300 s toward an unreachable goal from two Gaussian start spacings ($s = 1$ m and $s = 3$ m, $\sigma = 0.5\,s\sqrt{N/\pi}$ truncated at $3\sigma$) and 3 seeds each, and $R_f(N)$ is the median over seeds and spacings of the mean radius during the last 90 s. Calibration stops with an error if the radius drifts by more than 5% between the last two 90 s windows, differs by more than 5% between the two start spacings, or if the flock centre comes within $2\,R_f$ of the goal ([calibration settings](../guides/settings.md#calibration-of-r_f)).

Table 1 gives the arena lengths computed from $R_f(N)$ and $l_{\mathrm{reach}}$ (the farthest distance any sheep can start from the flock centre across the protocol's layouts):

**Table 1: Lengths of the drive task.**

| Quantity | Rule (lengths in m) |
| :--- | :--- |
| Flock radius $R_f(N)$ | Calibrated per $N$ (Table 2) |
| Goal radius $R_{\mathrm{goal}}$ | $1.9\,R_f(N)$ |
| Drive distance $l$ (start centre to goal centre) | $\max(13\,R_f(N),\ 80,\ l_{\mathrm{reach}} + R_{\mathrm{goal}} + R_f)$ |

Up to $N = 141$ (blue curve in Figure 1, middle), $13\,R_f(N)$ is the largest term ($80.6$ m at $N = 25$, so the 80 m floor never binds), giving $l = 13\,R_f(N)$. From $N = 200$ on (orange curve), the widest start layout (`outlier_rich`, $l_{\mathrm{reach}} = 1.6\,f(N) \propto N^{2/3}$) grows faster than $R_f(N)$, so the clearance term $l_{\mathrm{reach}} + R_{\mathrm{goal}} + R_f$ takes over and reaches $18\,R_f$ at $N = 400$.

### Success rules

A trial succeeds at the first tick before the deadline where enough sheep are inside the goal:

- Strict rule: all $N$ sheep are inside the goal at the same tick.
- 99% rule: at least $\lceil 0.99\,N \rceil$ sheep are inside the goal at the same tick (all $N$ sheep below $N = 100$, allowing 1 straggler at $N = 100$ and 4 at $N = 400$).
- Flock-centre rule: the flock centre lies within the goal radius, used only in the [paper check](../methods/strombom_check.md).

### Deadlines in drive times

Because larger flocks are driven farther (206.8 m at $N = 400$ versus 80.6 m at $N = 25$), deadlines are scaled by the drive time $T_{\mathrm{drive}} = l / v_{\mathrm{sheep}}$, the time a sheep walking straight at $v_{\mathrm{sheep}} = 1.0$ m/s needs to cover the drive distance $l$. The study tests deadlines of 12, 6 and 3 drive times, rounded up to whole 1 s ticks from the unrounded drive distance (Table 2):

**Table 2: Calibrated radii, drive distances and deadlines at the five main flock sizes.**

| $N$ | $R_f$ (m) | $l$ (m) and $T_{\mathrm{drive}}$ (s) | 12x (s) | 6x (s) | 3x (s) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 25 | 6.20 | 80.6 | 968 | 484 | 242 |
| 50 | 7.60 | 98.8 | 1186 | 593 | 297 |
| 100 | 9.08 | 118.1 | 1417 | 709 | 355 |
| 200 | 10.47 | 139.8 | 1678 | 839 | 420 |
| 400 | 11.40 | 206.8 | 2482 | 1241 | 621 |

## 2. Start layouts and dog starts

### Flock start layouts

A sheep farther than the [collect distance](../methods/strombom_multi.md#when-to-collect) $f(N) = 2\,N^{2/3}$ m from the flock centre is an outlier that must be collected before driving. Scaling the scattered layouts by $f(N)$ keeps the initial outlier fraction consistent across $N$ (Figure 2, Animation 1):

- `compact`: a Gaussian with $\sigma = 0.5\,R_f$, truncated at $3\sigma$, where all sheep start inside $f(N)$ so the dogs drive immediately.
- `wide`: a Gaussian with $\sigma = 0.5\,f(N)$, truncated at $3\sigma$, placing about 13% of the sheep beyond $f(N)$ at every $N$.
- `split`: $k = 3$ compact clusters ($k = 2$ when $N < 12$) centred on a circle of radius $f(N)$, each a Gaussian with $\sigma = 0.5\,R_f / \sqrt{k}$ so each cluster has the density of `compact`.
- `outlier_rich`: 80% of the sheep in a `compact` core and 20% on a ring between $1.1\,f(N)$ and $1.6\,f(N)$ from the centre.

![The four starting flock layouts at N = 200](../figures/fig7_layouts.png)

**Figure 2: The four start layouts ($N = 200$, $D = 4$, same scale).** Sheep outside the dashed collect circle are outliers that must be gathered first.

- Marks: blue dots are sheep, orange triangles dogs, the green circle the goal and the dashed circle the collect distance $f(N)$.
- Panels: one layout per panel, named in its title.

![Animation of one team on the four start layouts](../gifs/layouts.gif)

**Animation 1: The same team on the four start layouts ($N = 200$, $D = 4$, seed 0, 99% rule, 6 drive times).** On `compact` the dogs drive immediately; on the scattered layouts they collect first, and `split` takes longest (`dmin_f99_m6`).

- Marks: blue dots are sheep, orange triangles dogs and the green circle the goal; the bottom-left label shows elapsed time and sheep outside the goal.
- Panels: `compact`, `wide`, `split` and `outlier_rich`, finishing at 236, 278, 631 and 277 s.

### Dog starts

Dogs start behind the flock so they never spawn inside the sheep (Figure 3). The inner arc sits 30 m behind the farthest point any sheep of that layout can start, with dogs at least 5 m apart along the arc and any overflow placed on a concentric arc 5 m farther out. All study protocols use `arcs` (semicircles on the side away from the goal); the engine also implements `ring` (full circles omitting the goal cone) and `handler` (all dogs at a single point behind the flock).

![Dog start patterns](../figures/fig8_dog_starts.png)

**Figure 3: Dog start patterns.** Dogs start on semicircular arcs behind the flock, spilling onto a second arc once the first is full.

- Marks: blue dots are sheep, orange triangles dogs and the green circle the goal.
- Top: default `arcs` for $D = 1$ to 64 behind an $N = 100$ flock.
- Bottom: `arcs`, `ring` and `handler` at $N = 200$ with $D = 8$.

## 3. Adaptive sampling

Most [cells](../glossary.md#trials-and-experiments) decide well before the 200-seed cap, so the campaign adds 10-seed batches only to [open cells](../glossary.md#success-and-reliability) ([architecture](../codes/architecture.md#how-a-campaign-runs)). Figures 4 to 7 illustrate the four sampling rules on stored cells from `dmin_f99_m6` (99% rule, 6 drive times).

### Stopping early with the 99% Clopper-Pearson interval

After each batch of 10 seeds, HerdSim computes the exact two-sided 99% Clopper-Pearson confidence interval $[L, U]$ for the cell's success rate and compares it against $\theta = 0.90$ (Figure 4):

- Unreliable ($U < 0.90$): seeding stops, typically after 10 to 20 trials.
- Reliable ($L \ge 0.90$): seeding stops once reliability is decided; because $L \ge 0.90$ requires at least 51/51 successes and checks happen every 10 seeds, the earliest reliable decision is at 60/60 trials ($L = 0.915$).
- Undecided ($L < 0.90 \le U$): the cell receives another batch of 10 seeds, up to the cap of 200 (where a cell with 168 to 190 successes remains undecided).

![Sequential refinement and early stopping](../figures/fig_adaptive_1_refinement.png)

**Figure 4: Early stopping with the 99% Clopper-Pearson interval after each 10-seed batch.** A cell with zero successes stops at 10 seeds and one with 100% successes stops at 60; `wide`, $N = 400$, $D = 2$ stays near 0.93 and remains undecided at 200 seeds (187 of 200).

- Marks: red is the upper bound $U$ for zero successes, green the lower bound $L$ for all successes, blue the stored cell's rate and interval, and the dashed line $\theta = 0.90$.

### Midpoint densification

Protocols specify a coarse grid of team sizes, and the campaign automatically inserts the midpoint $\lfloor(D_1 + D_2)/2\rfloor$ between two neighbouring tested sizes $D_1$ and $D_2$ when their zones differ (or their reliability labels differ when `decide_finish_times` is off), the gap $D_2 - D_1$ is greater than 1 (`refine_min_gap`), and neither neighbour is [pruned](#pruning-above-saturation) or an undecided cell below 200 seeds (Figure 5).

![Adaptive grid densification](../figures/fig_adaptive_2_densification.png)

**Figure 5: Midpoint densification on `wide`, $N = 400$.** Because the zone changed between $D = 4$ (`improving`) and $D = 6$ (`saturated`), the campaign inserted $D = 5$.

- Marks: dots are initial protocol team sizes and the star is the midpoint added by the campaign, coloured by final zone.

### Pruning above saturation

When `decide_finish_times` is enabled, once [$D_{\mathrm{sat}}$](#frontier-values) is decided, a larger team is already zoned `saturated` (confirming saturation), and the curve is not still improving at the top of the grid, reliable cells above the confirming team (zoned `saturated` or finish-time `undecided`) where at least 90% of dogs on average have another dog within 2 m (`dog_overlap`) receive no more seeds and are marked `pruned` in `frontier_cells.csv` (Figure 6). Unreliable cells, cells undecided on reliability, and `crowded` cells slower than $D_{\mathrm{best}}$ are never pruned.

![Saturation and overlap pruning](../figures/fig_adaptive_3_pruning.png)

**Figure 6: Overlap pruning on `compact`, $N = 200$, 99% rule, 6 drive times.** Every team finishes in 232 to 235 s ($D_{\mathrm{sat}} = 1$, confirmed at $D = 2$); above $D = 2$, only $D = 24$ exceeds 0.90 overlap (0.91) and is pruned.

- Marks: blue is median finish time (left axis), orange is mean dog overlap (right axis), the dotted line is the 0.90 threshold, the shaded area marks teams above the confirming team, and the hollow square is the pruned cell.

*Data:* `results/dmin_f99_m6/`, drawn by `docs/generate_docs/make_result_figures.py`.

### Paired random streams

Cells at the same $(N, \text{layout})$ share paired seeds so team sizes compare directly (Figure 7). Seed index $i$ of every cell uses `master_seed + i` ($2026 + i$ by default), and each seed splits into separate random streams for initial placement, sheep noise and dog noise, so every team size $D$ faces the same initial flock and the same sheep noise until dog trajectories diverge.

![Deterministic paired comparisons](../figures/fig_adaptive_4_paired_seeds.png)

**Figure 7: Paired seeds on `wide`, $N = 400$, seeds 2026 to 2028, $D = 2$ to $4$.** Each seed produces the identical initial flock across every team size $D$ (seed 2028 fails at $D = 2$ and succeeds at $D = 3, 4$).

- Marks: blue dots are sheep and orange triangles dogs at tick 0; green borders indicate success and red borders failure.
- Panels: columns are seeds, rows are team sizes.

## 4. Flock and team sizes tested

### Flock size

All nine study runs test $N = 25, 50, 100, 200, 400$ (factors of 2). The 99% runs at 12 and 6 drive times add the intermediate $\sqrt{2}$ steps $N = 71, 141, 283, 566$ so points are evenly spaced on a log-log axis.

The upper limit $N = 566$ is set by the calibration edge, the smallest tested flock size where calibration fails its 5% drift or start-agreement limits ([calibration settings](../guides/settings.md#calibration-of-r_f)). Across both settings of `graze_repulsion`:

- With 3 seeds per start (used in the study runs): window drift is at most 1.9% up to $N = 566$ and 2.7-2.8% at $N = 600$, then jumps to 5.7-5.9% at $N = 630$, making $N = 630$ the 3-seed calibration edge.
- With 20 seeds per start: window drift is at most 0.52% up to $N = 400$, 1.4-1.7% at $566$, 2.2% at $600$, 3.4% at $630$ and 4.1-5.6% at $N = 660$ (where start-spacing spread also reaches 11-13%), making $N = 660$ the 20-seed calibration edge.

The study therefore stops at $N = 566 = 400\sqrt{2}$, the last $\sqrt{2}$ step below the calibration edge.

### Team size

All nine study protocols start with the grid $D \in \{1, 2, 3, 4, 6, 8, 12, 16, 24\}$ (two steps per doubling above $D = 2$, alternating $1.5\times$ and $1.33\times$), and [midpoint densification](#midpoint-densification) fills in intermediate team sizes wherever needed.

## 5. Frontier rules and zones

The frontier rules summarize each curve of cells into critical team sizes (Table 3) and cell zones (Table 5, Figure 8). The [report](../report/d_min_report.md) uses $D_{\min}$, its bracket or lower bound, and $D_{\min,\mathrm{stable}}$; the remaining values guide midpoint refinement and pruning when `decide_finish_times` is enabled and are saved in `frontier_groups.csv`.

![Behavioral zones and frontier classification](../figures/def_D_zones.png)

**Figure 8: Zones and frontier values on the example curve of Table 4.** Cell reliability and paired finish-time comparisons assign each team size to a [zone](#zones).

- Marks: bars are coloured by zone, and dotted vertical lines mark the frontier team sizes defined in Table 3.
- Top: zone label and reliability status per team size $D$.
- Bottom: median finish time across reliable team sizes.

### Frontier values

Finish-time comparisons apply only to working teams (reliable cells from $D_{\min}$ to $D_{\max}$). Two working teams are compared over the shared seeds where both succeeded (at least 5 shared seeds, 4000 bootstrap resamples); one team is judged faster or slower when the 99% bootstrap interval of their median finish-time difference lies entirely outside $\pm 5\%$ of the slower median (`time_margin`), the same when it lies entirely within $\pm 5\%$, and undecided otherwise. Table 3 defines the frontier values, and Table 4 illustrates them on an example curve:

**Table 3: Frontier values.**

| Value | Definition |
| :--- | :--- |
| $D_{\min}$ | Smallest reliable $D$. |
| $D_{\min,\mathrm{low}}$ | Smallest $D$ with $U \ge 0.90$ (lowest team not yet ruled unreliable), forming a bracket `D_min,low - D_min` when $D_{\min}$ sits above an undecided cell. |
| $D_{\mathrm{overcrowd}}$ | Smallest $D$ above $D_{\min}$ (or above $D_{\min,\mathrm{low}}$ if no $D$ is reliable) where both $D$ and the next tested team size are unreliable. |
| $D_{\max}$ | Largest reliable $D$ below $D_{\mathrm{overcrowd}}$ (or the largest reliable $D$ if $D_{\mathrm{overcrowd}}$ does not occur). |
| $D_{\mathrm{best}}$ | Smallest working $D$ judged "same" or "faster" than the working team with the lowest median finish time. |
| $D_{\mathrm{sat}}$ | Smallest working $D$ that no larger working team is judged "faster" than. |
| $D_{\mathrm{crowd}}$ | Smallest working $D$ above $D_{\mathrm{best}}$ judged "slower" than $D_{\mathrm{best}}$. |

**Table 4: Example curve ($D_{\min} = 2$, $D_{\mathrm{best}} = D_{\mathrm{sat}} = 4$, $D_{\mathrm{crowd}} = D_{\max} = 6$, $D_{\mathrm{overcrowd}} = 7$).**

| $D$ | Reliable | Median finish (s) | Verdict | Zone |
| :---: | :--- | :---: | :--- | :--- |
| 1 | No | - | - | `too_few` |
| 2 | Yes | 400 | Slower than 4 | `improving` |
| 3 | Yes | 300 | Slower than 4 | `improving` |
| 4 | Yes | 250 | Same as 5 | `saturated` |
| 5 | Yes | 245 | Fastest | `saturated` |
| 6 | Yes | 290 | Slower than 4 | `crowded` |
| 7 | No | - | - | `collapse` |
| 8 | No | - | - | `collapse` |

### Zones

Each cell on a curve is assigned one zone from Table 5:

**Table 5: Cell zones.**

| Zone | Condition |
| :--- | :--- |
| `too_few` | Unreliable, below $D_{\min}$ (or below $D_{\min,\mathrm{low}}$ if no cell is reliable) |
| `improving` | Reliable, below $D_{\mathrm{sat}}$ and not slower than $D_{\mathrm{best}}$ |
| `saturated` | Reliable, at or above $D_{\mathrm{sat}}$ and not slower than $D_{\mathrm{best}}$ |
| `crowded` | Reliable, above $D_{\mathrm{best}}$ and slower than $D_{\mathrm{best}}$ |
| `unreliable_dip` | Unreliable, isolated between $D_{\min}$ (or $D_{\min,\mathrm{low}}$) and $D_{\mathrm{overcrowd}}$ |
| `collapse` | Unreliable, at or above $D_{\mathrm{overcrowd}}$ |
| `recovered` | Reliable again above $D_{\mathrm{overcrowd}}$ |
| `undecided` | Undecided on reliability, or reliable above $D_{\mathrm{best}}$ with an undecided finish-time comparison |

### How failed trials end

Every failed trial is assigned a diagnostic `failure_mode` from its per-tick metrics (Table 6, evaluated in precedence order; rules 1 to 4 inspect the second half of the trial and rules 5 to 6 compare the two halves). All thresholds in Table 6 are HerdSim conventions, and the failure label `split` (flock fragmentation) is distinct from the `split` start layout:

**Table 6: Diagnostic failure labels in order of precedence.**

| Order | Label | Condition |
| :---: | :--- | :--- |
| 1 | `dogs_out_of_range` | Fewer than 10% of the outer half of the flock on average lies within $r_s$ of a dog, and fewer than 1 sheep on average is beyond $2.5\,R_f$ from the flock centre. |
| 2 | `flock_escaped` | Mean flock-centre distance to the goal exceeds the initial distance. |
| 3 | `split` | Largest connected component of sheep linked within 5 m holds less than 55% of the flock. |
| 4 | `scatter` | Flock RMS radius exceeds $2\,R_f$. |
| 5 | `oscillation` | Matches `stuck`, and the 200 s moving-average goal distance reverses direction at least 3 times by more than $R_{\mathrm{goal}}$. |
| 6 | `stuck` | Mean flock-centre distance to the goal changes by less than $R_{\mathrm{goal}}$ between the two halves of the trial. |
| 7 | `timeout` | Any failed trial not matching rules 1 to 6. |
