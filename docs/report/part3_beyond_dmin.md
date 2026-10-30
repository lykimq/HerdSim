# Enough dogs and too many dogs

Part 3 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.7 RQ7: Beyond D_min: enough dogs, cost, and pressure on the flock

Past a team size $D_{\mathrm{sat}}$, more dogs stop making the drive faster, and each extra dog adds dog time ($D$ times the finish time) for little speed. On three of the four replayed curves, the time each sheep flees falls up to $D_{\mathrm{sat}}$ and hardly grows beyond it, although on `wide` $N = 400$ more sheep flee at once. Under the 99% rule, extra dogs almost never make the task fail. Most results here come from the 99% runs (item 4 also cites two strict-rule cases); the flight times come from 164 replayed trials, each of which reproduced its stored trial exactly.

### 1. When more dogs stop helping (D_sat)
$D_{\mathrm{sat}}$ is the smallest [working team](../glossary.md#team-sizes) that no larger working team beats on finish time by more than 5%, at 99% confidence; an undecided comparison leaves it as a range ([how teams are compared](../experiments/task_design.md#frontier-values)).
- Compact flocks up to $N = 566$ and the other layouts at $N \le 50$: $D_{\mathrm{sat}} = 1$ (except `outlier_rich` $N = 50$, bracketed at 1-24). One dog already keeps the flock walking at 1 m/s.
- Scattered flocks at 6 drive times: $D_{\mathrm{sat}}$ is 2 to 7 where decided at $N = 100$ to 400; on `wide`, after the finish-time top-up runs ([section 3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)), it is 1, 1, 1, 2, 3, 3, 4, 5 from $N = 25$ to 400. Some `outlier_rich` and `wide` curves still have a bracket ([D_sat table](results_tables.md#d_sat-dmin_f99_m6-d_sat-1)), and `split` has none from $N = 200$.
- $D_{\mathrm{sat}}$ is the same at 12 and 6 drive times on every curve with a $D_{\min}$ at both (`outlier_rich` $N = 566$ gives overlapping brackets, 8-24 at 12 and 8-12 at 6). At 3 drive times on `wide`, $D_{\min}$ rises to $D_{\mathrm{sat}}$ at $N = 100$ and 200 (2 and 3 dogs), and at 400 its bracket, 5-6, includes $D_{\mathrm{sat}} = 6$; it does not on `outlier_rich` or `split` at $N = 100$ ([section 3.3](part1_growth.md#33-rq3-how-does-the-deadline-change-d_min)).

### 2. What dogs beyond D_sat cost
In all 189 reliable cells above a decided $D_{\mathrm{sat}}$ at 6 drive times, the finish time is 0.96 to 1.01 times the $D_{\mathrm{sat}}$ time, while dog time grows with $D / D_{\mathrm{sat}}$ (Figure 1, Table 1). On a compact flock of 50, 24 dogs take the same 154 s as one dog, for 24 times the dog time. The dogs are moving for nearly all of it: at $N = 400$ (6 drive times, 99% rule) the median dog moves at 1.44-1.50 m/s on `compact`, `wide` and `outlier_rich`, close to its top speed of 1.5 m/s, and at 1.20-1.40 m/s on `split`, where up to 20% of the dogs stand still.

**Table 1: Finish time and dog time at twice $D_{\mathrm{sat}}$ and at $D = 24$, relative to the $D_{\mathrm{sat}}$ cell (6 drive times; on `outlier_rich` $N = 400$ relative to the cell at 6, the low end of the bracket).**

| Layout, $N$ | $D_{\mathrm{sat}}$ | At $2 D_{\mathrm{sat}}$: finish time / dog time | At $D = 24$: finish time / dog time |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0.97 / 1.94 | 0.96 / 7.70 |
| `wide`, $N = 400$ | 5 | 0.97 / 2.32 (at $D = 12$) | 0.96 / 4.61 |
| `outlier_rich`, $N = 100$ | 3 | 0.99 / 1.98 | 0.98 / 7.85 |
| `outlier_rich`, $N = 400$ | 6-24 | 0.96 / 1.91 | 0.94 / 3.74 |
| `split`, $N = 100$ | 4 | 0.99 / 1.98 | 0.99 / 5.91 |

Over the 10 scattered curves at $N \ge 100$ with a decided $D_{\mathrm{sat}}$ (`wide` $N = 100$ to 400, `outlier_rich` 100 to 200, `split` 100 and 141), 24 dogs take 0.96 to 1.00 times the $D_{\mathrm{sat}}$ finish time for 3.31 (`split` $N = 141$) to 11.94 (`wide` $N = 100$) times the dog time. A dog beyond $D_{\mathrm{sat}}$ adds its full dog time and saves almost no finish time.  
*Data:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) and [results_tables.md: D_sat, dmin_f99_m6](results_tables.md#d_sat-dmin_f99_m6-d_sat-1).

### 3. Pressure on the sheep
A sheep flees while a dog is within 65 m ($r_s$). On three of the four replayed curves, each sheep flees for less time as the team grows to $D_{\mathrm{sat}}$ and hardly longer beyond it (Figure 2, Animation 1). This may be because the flock is gathered sooner; we have not tested it. On `wide` $N = 400$ the median flight time per sheep falls from 485 s at $D = 3$ to 359 s at $D = 6$ and stays there (361 s at $D = 12$), while the median share of the flock fleeing at a given moment rises from 68% to 84% between $D = 3$ and 12. The replays took $D_{\mathrm{sat}} = 6$ there, its value before the finish-time top-up; it is now 5. On `wide` $N = 100$ only $D = 1$ and 2 were replayed (186 s and 190 s), so no replayed team lies beyond its current $D_{\mathrm{sat}}$ of 2. At every replayed team size a sheep spends less than 1.3 s (median; at most 1.25 s) within 6 m (the dog's stop distance $3 r_a$, with $r_a = 2$ m; [glossary](../glossary.md#sheep-models-and-dog-rules)) of a dog.

### 4. Extra dogs almost never make the task fail
Under the 99% rule, on the five original flock sizes and up to 24 dogs, no curve that reaches a reliable team becomes unreliable again at larger teams. The three 99% main runs have one dip, at a size of the denser grid, and the strict rule has one collapse and one dip, both on `split` $N = 100$. The 99% runs also label `collapse` on four curves with no reliable team: `split` $N = 200$, 283 and 400 at 6 drive times and `outlier_rich` $N = 400$ at 3:
- Under the 99% rule on the denser grid, `split` $N = 141$ at 6 drive times (`dmin_f99_m6`): 4 dogs are decided unreliable (88 of 110, success 0.80) between a reliable 3 and a reliable 7.
- Under the strict rule, `split` $N = 100$ at 3 drive times: one dog is reliable (60 of 60) and 2 to 4 dogs are not (5 of 10, 5 of 10, 97 of 120). Two unreliable sizes in a row make this an onset of failure ($D_{\mathrm{overcrowd}} = 2$, [item 5](#5-the-upper-end-of-the-curves-d_max-d_crowd-and-d_overcrowd)), labelled `collapse`, with the teams from 5 dogs up `recovered` ([zones](../experiments/task_design.md#zones)). At 6 drive times 3 dogs are decided unreliable (36 of 50) between a reliable 1 and a reliable 5 (`unreliable_dip`).

At 12 drive times, extra dogs slow the drive while it still succeeds on `split` at $N = 71$, 200, 283, 400 and 566 and on `outlier_rich` at $N = 566$ (the curves with a $D_{\mathrm{crowd}}$). At $N = 71$ only $D = 2$ is slower (209 s against 186 s) and the time from 90% to 99% of the flock is 4-5 s for every team; from $N = 200$ on `split`, and on `outlier_rich` $N = 566$ from 12 dogs, the flock arrives in two parts ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)). On `split` $N = 400$ at 12 drive times the median finish time is 950-1040 s for $D \ge 9$ against 839 s at $D = 5$. At 12 drive times, after 90% of the flock is in, the next 9% takes a median of 294-465 s ($N = 200$), 342-492 s ($N = 283$), 316-519 s ($N = 400$) and 480-694 s ($N = 566$) on `split` with teams from 3 dogs up (from 2 at $N = 283$, from 4 at $N = 566$), and 465 to 578 s on `outlier_rich` $N = 566$ with teams from 12 dogs up. On `outlier_rich` $N = 283$ only 5 and 8 dogs show the gap (380 and 330 s); the other teams take 8 to 12 s. On that curve at 6 drive times, for $D = 5$ to 12, the finish times fall in a fast and a slow group (at $D = 5$ the quartiles are 367 and 799 s), so a median describes it poorly and its $D_{\mathrm{sat}}$ stays a bracket (5-24).

On `outlier_rich` $N = 566$, 16 and 24 dogs succeed in 130 of 130 and 100 of 100 trials at 12 drive times. They fail some trials at 6 drive times (limit 1520 s). Of these, 8 of 12 at $D = 16$ and 7 of 11 at $D = 24$ use seeds also run at 12 drive times, and all 15 finished there, in 1521 to 1951 s. The $D_{\max}$ of 12 at 6 drive times may be set by these late arrivals; we have not tested it.

### 5. The upper end of the curves: D_max, D_crowd and D_overcrowd
Four values bound a curve from above ([frontier values](../experiments/task_design.md#frontier-values)). $D_{\mathrm{overcrowd}}$ is the first team from which two tested sizes in a row are unreliable, looked for above $D_{\min}$, or, on a curve with no reliable team, above $D_{\min,\mathrm{low}}$, the smallest team not yet decided unreliable. $D_{\max}$ is the largest reliable team below $D_{\mathrm{overcrowd}}$ (or the largest reliable team when there is none); the reliable teams below $D_{\mathrm{overcrowd}}$ are the working teams. $D_{\mathrm{best}}$ is the smallest working team as fast as the fastest one, within 5%, and $D_{\mathrm{crowd}}$ the first working team above $D_{\mathrm{best}}$ that is more than 5% slower than it.

In the three 99% main runs:
- $D_{\max}$ is almost always the top of the grid: 84 of the 85 curves with a $D_{\min}$ are still reliable at 24 dogs and have no $D_{\mathrm{overcrowd}}$, so $D_{\max}$ is only a lower bound. The exception, `outlier_rich` $N = 566$ at 6 drive times, has 16 and 24 dogs undecided (188 of 200 = 0.94 and 189 of 200 = 0.945), so $D_{\max} = 12$.
- $D_{\mathrm{crowd}}$ appears on 6 curves at 12 drive times, `split` at $N = 71$, 200, 283, 400 and 566 (from 2 to 14 dogs) and `outlier_rich` $N = 566$ (15 dogs): the slower drives of item 4.
- $D_{\mathrm{overcrowd}}$ appears on 4 curves on which no team is decided reliable: `split` $N = 200$, 283 and 400 at 6 drive times (from 4, 15 and 10 dogs) and `outlier_rich` $N = 400$ at 3 (from 7). The larger teams there stay near but mostly below $\theta$.

More dogs do make the task fail in a few follow-up settings: with whole-team sharing at a range of 65 m on `split` $N = 200$ (reliable with 3 dogs, decided unreliable at 4, 6, 8, 9, 13, 14 and 16; [section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it)), near the smallest goal that holds a flock of 25, and with dogs kept 2 m apart in the holding task ([section 3.10](#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)).

*Data:* [results_tables.md: the upper end of the curves](results_tables.md#the-upper-end-of-the-curves-d_max-d_crowd-and-d_overcrowd) (`uv run cli/dmin_tables.py upper ...`); success rates per cell in each folder's `frontier_cells.csv`.

![Cost of dogs beyond D_sat](../figures/fig33_effort.png)

**Figure 1: Cost of dogs beyond $D_{\mathrm{sat}}$ (6 drive times, 99% rule).** On the curves with a decided $D_{\mathrm{sat}}$, dogs beyond it make the drive about 4% faster at most, while the dog time grows in proportion to the team.

- Marks: each line is one curve (one layout and $N$, coloured by layout) with a decided $D_{\mathrm{sat}}$, and each point is one reliable team from $D_{\mathrm{sat}}$ up, 27 lines and 189 cells above their $D_{\mathrm{sat}}$. The horizontal axis is $D / D_{\mathrm{sat}}$ (log scale), so every line starts at 1 and $x = 2$ means twice the team needed; on `wide` $N = 400$ ($D_{\mathrm{sat}} = 5$), $D = 24$ sits at 4.8.
- Left: median finish time divided by that of the $D_{\mathrm{sat}}$ cell, so 0.97 means 3% faster. Every curve stays within about 0.96 to 1.01 (the largest ratio is 1.012), a narrow range that the axis stretches. Points below 1 do not contradict $D_{\mathrm{sat}}$: a larger team counts as faster only when it saves more than 5% of the time with 99% confidence, judged by resampling the paired finish times of shared seeds (a paired bootstrap), and none does.
- Right: dog time ($D$ times the finish time) divided by that of the $D_{\mathrm{sat}}$ cell. The curves follow the diagonal $y = x$, so twice the dogs cost twice the dog time.

*Data:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1).

![Pressure on the flock](../figures/fig34_pressure.png)

**Figure 2: How long the sheep flee, against team size (6 drive times, 99% rule).** Larger teams make more sheep flee at once (on `outlier_rich` $N = 100$ the share stays at 0.88-0.91). On three of the four curves the time each sheep flees falls up to $D_{\mathrm{sat}}$ and hardly grows beyond it; on `wide` $N = 100$ the two replayed teams give 186 s and 190 s.

- Marks: medians over successful trials for $N = 100$ (circles, dotted) and $N = 400$ (squares, solid); blue is `wide`, green `outlier_rich`. Each curve has points only at the replayed team sizes $D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ and $2 D_{\mathrm{sat}}$, as they stood before the finish-time top-up ($D_{\mathrm{sat}} = 6$ on `wide` $N = 400$ then, 5 now; on `wide` $N = 100$ it was 1 (open) then and is 2 now, and $2 D_{\mathrm{sat}}$ was 2 then and is 4 now).
- Left: seconds each sheep spends with a dog within 65 m. From $D_{\min}$ to $D_{\mathrm{sat}}$ it falls; beyond $D_{\mathrm{sat}}$ it hardly grows.
- Right: share of the flock fleeing, averaged over each trial.

At $N = 400$ one dog succeeded in none of its 10 trials and $D = 2$ was not replayed, so those curves start at 3.  
*Data:* [results_tables.md: Pressure, dmin_f99_m6](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

![Animation of the sheep fleeing from 3 dogs and from 12 dogs](../gifs/flock_pressure.gif)

**Animation 1: The flock under 3 and 12 dogs, replayed (`wide`, $N = 400$, seed 0, 99% rule, 6 drive times).** With 12 dogs more of the flock flees at once, but the drive is shorter, as in Figure 2. Both start from the same flock, and each replay reproduces its stored trial.

- Marks: filled dots are sheep within $r_s = 65$ m of a dog, which flee; hollow dots graze.
- Left: 3 dogs. At 148 s, 129 of the 400 sheep flee, and the flock is in at 727 s.
- Right: 12 dogs. At 148 s, 395 flee, and the flock is in at 431 s.

## 3.10 RQ10: When do more dogs hurt? Holding the flock, and dogs that take up room

In the open drive under the 99% rule, extra [point dogs](../glossary.md#sheep-models-and-dog-rules) (dogs with no size, as in all the main runs) never lost a reliable team at the five original flock sizes of the three 99% main runs; the one dip in those runs is on the denser grid ([section 3.7](#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock), item 4). Extra dogs do hurt in the holding task, where the flock must stay in the goal while the dogs withdraw: with dogs kept 2 m apart on `outlier_rich` $N = 400$ (result 2), and with a goal just too small for a flock of 25 (result 3). With 99% of the flock held, no team holds a flock of 50 or fewer in the default goal (result 1).

The protocols change the end of the task or the room each dog takes. `dmin_f99_hold` runs the [holding task](../experiments/task_design.md#the-holding-task): a trial succeeds once 99% of the flock has stayed in the goal for one drive time while each dog withdraws to $r_s + r_a = 67$ m beyond the farthest sheep on its bearing from the flock centre. `dmin_f99_hold_spacing` keeps the [dogs 2 m apart](../experiments/task_design.md#crowding-with-dogs-that-take-up-room), so the arc behind the flock has room for about $D_{\mathrm{cap}} = 7, 9, 10, 11, 12$ dogs at $N = 25$ to 400 (the arc length divided by the 2 m spacing). `dmin_f99_hold_goal` and `dmin_f99_hold_share` hold flocks of 25, 50 and 100 with the goal radius raised from $1.9 R_f$ to 2.1, 2.3 and $2.5 R_f$, crossed with the share that must stay in (99%, 95%, 90%), and to $3.0 R_f$ at 99%, on the seeds of `dmin_f99_hold`.

### Results

1. With 99% held, holding works on $N \ge 100$ on `wide` and `compact`, with the same $D_{\min}$ as the open drive or one more (1, 2 and 3 dogs on `wide` at $N = 100$, 200, 400). On `split` no team is decided reliable from $N = 200$ (at 200 two dogs succeed in 171 of 200, undecided, 99% interval 0.78-0.91; at 400 every team is decided unreliable). On $N \le 50$ no team holds the flock, and most failed trials end with no sheep in the goal (423 of 560 at $N = 25$, 301 of 444 at $N = 50$). The flock enters at the near edge of the goal and its centre keeps walking while the dogs withdraw, a median 17 m at $N = 25$, 15 m at $N = 50$ and 13 m at $N = 100$ (`cli/diagnostics/hold_walk.py`, all 240 stored trials replayed at a goal of $3.0 R_f$; the dogs cleared in 239 and never in the other). The default goal is 11.8 m at $N = 25$ and 14.4 m at $N = 50$, and below $N = 100$ the 99% share is every sheep, so the first sheep across the far edge ends the hold. This points to the goal size against the walk as the cause; the walk itself was not varied.

2. With dogs kept 2 m apart, extra dogs make holding fail on `outlier_rich` $N = 400$ (Figure 3). Teams of 3 to 6 succeed in 0.925-0.94 of trials (undecided), and from $D = 9$ every team up to 24 is decided unreliable: 54 of 70 at $D = 9$ (99% interval 0.62-0.89), 13 of 20 at $D = 12$ (0.34-0.89), 5 of 10 at $D = 16$ (0.13-0.87). This may be because the arc holds only about 12 spaced dogs, so near that number they push each other off their places and cannot leave the arc to catch a breakaway sheep; we have not tested it, and it does not explain why failures start at 9 dogs. On `compact` $N = 400$ every spaced team from 1 to 24 is reliable, and on `wide` $N = 400$ 3 dogs and every team from 6 to 24 are reliable (4 and 5 undecided, 190 of 200 each). On `split` $N = 200$ success falls from 0.85 at $D = 2$ (170 of 200, undecided) to 0-0.10 from 6 dogs up (10 trials per cell). Whether extra dogs hurt depends on the layout as well as on the room each dog takes.

![Holding with point dogs and with dogs 2 m apart](../figures/fig36_spacing.png)

**Figure 3: Holding at $N = 400$, point dogs against dogs kept 2 m apart.** On `wide` success holds up to 24 spaced dogs; on `outlier_rich` it falls from $D = 9$.

- Marks: success against $D$ (log scale), dotted grey for point dogs and solid blue for dogs 2 m apart. The orange band marks 10 to 12 dogs, the arc capacity $D_{\mathrm{cap}}$ of the larger flocks; the dashed line is $\theta = 0.90$, and hollow markers are cells with fewer than 30 trials.
- Panels: `wide` (left) and `outlier_rich` (right).

*Data:* [results_tables.md: D_min, dmin_f99_hold](results_tables.md#d_min-dmin_f99_hold) and [results_tables.md: D_min, dmin_f99_hold_spacing](results_tables.md#d_min-dmin_f99_hold_spacing).

3. A larger goal or a smaller share held lets one dog hold a small flock (Table 2, Figure 4). With 99% held one dog needs about 16 to 19 m; with 95% or 90% held, 13.0 to 14.4 m is enough at $N = 25$ and 50. With 99% held, the three ranges overlap in metres (15.5-18.6, 16.0-17.5 and at most 17.3 m), while in flock radii their lower ends fall from 2.5 to 2.1 to at most 1.9 $R_f$. The walk gives smaller values: a flock that enters with its last sheep at the near edge and walks $w$ keeps every sheep in only if the goal radius exceeds about $w/2$ plus the distance of its farthest sheep from the centre, which gives 14.3 and 15.7 m at $N = 25$ and 50 (medians over the replays), below the observed ranges, and 17.2 m at $N = 100$, where the observed threshold is only an upper bound (at most 17.3 m). This is consistent with the walk being the cause; the walk itself was not varied.

   Just short of the threshold some larger teams fail. At $N = 25$, 90% held, $2.1 R_f$, one dog is reliable on `split` and `outlier_rich`, while on every layout teams from 3 to 7 dogs upward are decided unreliable (success down to 0.50). At $N = 50$, 99% held, $2.1 R_f$, no team is decided reliable and 4 dogs are decided unreliable on `wide` and `outlier_rich` (159 of 190 and 97 of 120). In the walk replays at $N = 25$ (goal $3.0 R_f$, 99% held, 20 replays per team size from 5 seeds on each of the 4 layouts, no interval computed) the median walk is 17.5-17.8 m with 2, 4 or 8 dogs and 16.6 m with one. A longer walk may be why larger teams fail just short of the threshold; we have not tested it, and the walk was measured at another goal and share.

**Table 2: Smallest goal tested from which one dog is decided reliable on every layout except `outlier_rich` $N = 100$ (holding for one drive time, 6 drive times; "<=" where the default $1.9 R_f$, the smallest goal tested, already holds).**

| Share that must stay in | $N = 25$ | $N = 50$ | $N = 100$ |
| :--- | :---: | :---: | :---: |
| 99% (out: none below $N = 100$, one at 100) | $2.5$-$3.0 R_f$ = 15.5-18.6 m | $2.1$-$2.3 R_f$ = 16.0-17.5 m | <= $1.9 R_f$ = 17.3 m (`outlier_rich` 3) |
| 95% (out: one of 25, two of 50, five of 100) | $2.3 R_f$ = 14.3 m | <= $1.9 R_f$ = 14.4 m | <= $1.9 R_f$ = 17.3 m (`outlier_rich` 2) |
| 90% (out: two of 25, five of 50, ten of 100) | $2.1$-$2.3 R_f$ = 13.0-14.3 m | <= $1.9 R_f$ = 14.4 m | <= $1.9 R_f$ = 17.3 m (`outlier_rich` 2) |

A range means one dog is still undecided at the smaller goal on some layout. At $N = 100$ the value in parentheses is the team `outlier_rich` needs at the default goal; with 99% held it needs 3 at the default goal and 2 with any larger goal, and with a smaller share it needs 2. No goal tested makes one dog reliable there. Every other layout needs one dog at the goal given. Trials shared by the three holding protocols reproduce each other exactly.  
*Data:* [results_tables.md: dmin_f99_hold_goal](results_tables.md#dmin_f99_hold_goal-dmin_f99_hold--dmin_f99_hold_goal), [results_tables.md: dmin_f99_hold_share](results_tables.md#dmin_f99_hold_share-dmin_f99_hold--dmin_f99_hold_share) and [results_tables.md: walk while the dogs withdraw](results_tables.md#walk-while-the-dogs-withdraw-dmin_f99_hold_goal-at-30-r_f-replay-of-5-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

![Holding a small flock: success against the goal radius](../figures/fig40_hold_goal.png)

**Figure 4: Holding success against the goal radius in metres, for each share that must stay in.** With 99% held, the curves of $N = 25$ and 50 rise between about 13 and 17.5 m, and $N = 100$ is already above $\theta$ at its default 17.3 m; letting one or two sheep out moves the rise of the small flocks to smaller goals.

- Marks: each point is the mean success rate over the 20 cells of one flock size and goal (4 layouts x $D = 1, 2, 4, 8, 24$, each cell counted once, without the midpoints the adaptive run added). The bar is the range over those cells, and its low end near the threshold is the larger teams; at $N = 100$ the low end is `outlier_rich` with one dog. Blue is $N = 25$, orange $N = 50$, green $N = 100$; ringed points are the default goal of $1.9 R_f$, and the dashed line is $\theta = 0.90$.
- Panels: 90%, 95% and 99% of the flock must stay in the goal for one drive time, from left to right.

*Data:* `results/dmin_f99_hold_share` and `results/dmin_f99_hold_goal` (the $3.0 R_f$ points).

Animation 1 in [task design](../experiments/task_design.md#the-holding-task) replays one dog holding a flock of 25 in a goal of $1.9 R_f$, where the flock walks out, and of $3.0 R_f$, where it is held.
