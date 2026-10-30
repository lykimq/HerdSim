# Enough dogs and too many dogs

Part 3 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.7 RQ7: Beyond D_min: enough dogs, cost, and pressure on the flock

The smallest reliable team leaves three questions open. Do more dogs make the drive faster? What does each extra dog cost? Do more dogs put the sheep under more stress? We read the answers from the 99% runs. We also replayed 164 stored trials to measure how long each sheep spends fleeing, and every replay reproduced its stored trial exactly.

From the team size $D_{\mathrm{sat}}$ on, more dogs stop making the drive faster (item 1). Beyond it each dog adds dog time ($D$ times the finish time) but little speed (item 2). More dogs make more sheep flee at once, but the total time each sheep flees hardly grows (item 3). Under the 99% rule, extra dogs almost never make the task fail (items 4 and 5).

### 1. When more dogs stop helping (D_sat)
$D_{\mathrm{sat}}$ is the smallest [working team](../glossary.md#team-sizes) that no larger working team beats on finish time by more than 5%, at 99% confidence; when a comparison stays undecided, $D_{\mathrm{sat}}$ is shown as a range ([how teams are compared](../experiments/task_design.md#frontier-values)).
- Compact flocks and $N \le 50$: $D_{\mathrm{sat}} = 1$ (except `outlier_rich` $N = 50$, bracketed at 1-24). One dog already keeps the flock walking at 1 m/s.
- Scattered flocks at 6 drive times: $D_{\mathrm{sat}}$ is 2 to 7 where decided at $N = 100$ to 400 (`outlier_rich` $N = 100$: 3; `wide` $N = 400$: 5; `split` $N = 141$: 7). The top of the bracket is still open on `outlier_rich` $N = 283$ (5-24) and 400 (6-24) and on `wide` $N = 566$ (7-24); `outlier_rich` $N = 566$ is bracketed at 8-12, and `split` has no $D_{\mathrm{sat}}$ from $N = 200$.
- After the finish-time top-up runs ([section 3.8](part1_growth.md#38-rq8-growth-with-n-on-a-denser-grid-d_sat-and-the-shape-of-the-curve)), $D_{\mathrm{sat}}$ on `wide` is 1, 1, 1, 2, 3, 3, 4, 5 from $N = 25$ to 400.
- $D_{\mathrm{sat}}$ is the same at 12 and 6 drive times on every curve with a $D_{\min}$ at both. `outlier_rich` $N = 566$ gives overlapping brackets (8-24 at 12, 8-12 at 6), and `split` at $N \ge 200$ has no $D_{\min}$ and so no $D_{\mathrm{sat}}$ at 6 drive times. At 3 drive times on `wide`, $D_{\min}$ rises to $D_{\mathrm{sat}}$ at $N = 100$ and 200 (2 and 3 dogs), and at 400 its bracket, 5-6, includes $D_{\mathrm{sat}} = 6$. It does not on `outlier_rich` or `split` at $N = 100$ ([section 3.3](part1_growth.md#33-rq3-how-does-the-deadline-change-d_min)).

### 2. What dogs beyond D_sat cost
- In all 189 reliable cells above a decided $D_{\mathrm{sat}}$ at 6 drive times, the finish time is 0.96 to 1.01 times the $D_{\mathrm{sat}}$ time: at most 4% faster, sometimes 1% slower (Figure 1).
- Dog time grows with $D / D_{\mathrm{sat}}$. On a compact flock of 50, 24 dogs take the same 154 s as one dog, for 24 times the dog time. The dogs are moving for nearly all of it: at $N = 400$ (6 drive times, 99% rule) the median dog runs at 1.44-1.50 m/s on `compact`, `wide` and `outlier_rich`, close to its top speed of 1.5 m/s, and at 1.20-1.40 m/s on `split`, where up to 20% of the dogs stand still.

Table 1 compares twice $D_{\mathrm{sat}}$ and $D = 24$ with the $D_{\mathrm{sat}}$ cell on five scattered curves at 6 drive times. One of them, `outlier_rich` $N = 400$, has $D_{\mathrm{sat}}$ still bracketed at 6-24, and its ratios are taken against the cell at 6, the lower end:

**Table 1: Finish time and dog time at twice $D_{\mathrm{sat}}$ and at $D = 24$, relative to the $D_{\mathrm{sat}}$ cell.**

| Layout, $N$ | $D_{\mathrm{sat}}$ | At $2 D_{\mathrm{sat}}$: finish time / dog time | At $D = 24$: finish time / dog time |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0.97 / 1.94 | 0.96 / 7.70 |
| `wide`, $N = 400$ | 5 | 0.97 / 2.32 (at $D = 12$) | 0.96 / 4.61 |
| `outlier_rich`, $N = 100$ | 3 | 0.99 / 1.98 | 0.98 / 7.85 |
| `outlier_rich`, $N = 400$ | 6-24 | 0.96 / 1.91 | 0.94 / 3.74 |
| `split`, $N = 100$ | 4 | 0.99 / 1.98 | 0.99 / 5.91 |

In these five rows, 24 dogs drive 1% to 6% faster than $D_{\mathrm{sat}}$, for 3.7 to 7.9 times the dog time; the 6% is `outlier_rich` $N = 400$, whose $D_{\mathrm{sat}}$ is the bracket. Over the 10 scattered curves at $N \ge 100$ with a decided $D_{\mathrm{sat}}$ (`wide` $N = 100$ to 400, `outlier_rich` 100 to 200, `split` 100 and 141), 24 dogs take 0.96 to 1.00 times the $D_{\mathrm{sat}}$ finish time, for 3.31 (`split` $N = 141$) to 11.94 (`wide` $N = 100$) times the dog time.  
*Data:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) and [results_tables.md: D_sat, dmin_f99_m6](results_tables.md#d_sat-dmin_f99_m6-d_sat-1).

### 3. Pressure on the sheep
A sheep flees while a dog is within 65 m ($r_s$). The replays measure how long that lasts (Figure 2).
- Each sheep flees for less time as the team grows up to $D_{\mathrm{sat}}$ on three of the four curves: more dogs gather the flock sooner, so the drive is shorter. On `wide` $N = 400$ the median flight time per sheep falls from 485 s at $D = 3$ to 359 s at $D = 6$, and stays there (361 s at $D = 12$). The replay used $D = 6$ as $D_{\mathrm{sat}}$, its value before the finish-time top-up; it is now 5. On `wide` $N = 100$ only $D = 1$ and $D = 2$ were replayed, and the time rises from 186 s to 190 s. $D_{\mathrm{sat}}$ there was 1 (open) at replay time and is 2 now.
- More of the flock flees at once: on `wide` $N = 400$ the median share of the flock fleeing at a given moment rises from 68% at $D = 3$ to 84% at $D = 12$. Beyond $D_{\mathrm{sat}}$ (as it stood at replay time) the total time each sheep spends fleeing hardly grows: on `wide` $N = 400$ it goes from 359 to 361 s. On `wide` $N = 100$ no replayed team lies beyond the current $D_{\mathrm{sat}}$ of 2.
- Dogs stay off the sheep: the time a sheep spends within 6 m ($3 r_a$, the dog's stop distance) of a dog stays below 1.3 s per sheep (median; at most 1.25 s) at every replayed team size ($D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ and $2 D_{\mathrm{sat}}$ on the four replayed curves).

### 4. Extra dogs almost never make the task fail
Under the 99% rule, on the five original flock sizes and up to 24 dogs, no curve that reaches a reliable team becomes unreliable again at larger teams. The exceptions, and the cases where extra dogs only slow the drive:
- Dips: on the denser grid there is one. On `split` $N = 141$ at 6 drive times (`dmin_f99_m6`), 4 dogs are decided unreliable (88 of 110, success 0.80) between a reliable 3 and a reliable 7; 5 and 6 dogs are undecided. Under the strict rule `split` $N = 100$ loses its reliable one-dog team at two deadlines:
  - At 3 drive times one dog is reliable (60 of 60) and 2 to 4 dogs are not (5 of 10, 5 of 10, 97 of 120). Two unreliable sizes in a row make this an onset of failure ($D_{\mathrm{overcrowd}} = 2$, [item 5](#5-the-upper-end-of-the-curves-d_max-d_crowd-and-d_overcrowd)), so the tables label 2 to 4 dogs `collapse`, and the teams from 5 dogs up, reliable again, `recovered` ([zones](../experiments/task_design.md#zones)).
  - At 6 drive times 3 dogs are decided unreliable (36 of 50), between a reliable 1 and a reliable 5. This one is a dip (`unreliable_dip`).
- Slower drives: on `split` $N = 400$ at 12 drive times, the median finish time is 950-1040 s for $D \ge 9$ against 839 s at $D = 5$, though the task still succeeds.
- Where the time goes: the flock arrives in two parts ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)). At 12 drive times:
  - on `split` at $N = 200$ to 566, teams from 3 dogs up (from 2 at $N = 283$, from 4 at $N = 566$) bring 90% of the flock in and then take a median of 294-465 s ($N = 200$), 342-492 s ($N = 283$), 316-519 s ($N = 400$) and 480-694 s ($N = 566$) for the next 9%;
  - on `outlier_rich` $N = 566$ teams from 12 dogs up take 465 to 578 s;
  - on `outlier_rich` $N = 283$ only 5 and 8 dogs show the gap (380 and 330 s); the other teams take 8 to 12 s.
- The upper values of `outlier_rich` $N = 566$ ([item 5](#5-the-upper-end-of-the-curves-d_max-d_crowd-and-d_overcrowd)):
  - At 12 drive times 16 and 24 dogs succeed in 130 of 130 and 100 of 100 trials.
  - A shorter deadline only cuts the same trials short ([section 3.3](part1_growth.md#33-rq3-how-does-the-deadline-change-d_min)). Of the trials these teams fail at 6 drive times (limit 1520 s), 8 of 12 at $D = 16$ and 7 of 11 at $D = 24$ use seeds that were also run at 12 drive times, and all 15 finished there, in 1521 to 1951 s. The other 4 and 4 seeds were not run at 12 drive times.
  - The $D_{\max}$ of 12 at 6 drive times may be set by the late arrivals; we have not tested it.
  - The $D_{\mathrm{crowd}}$ of 15 at 12 drive times comes from the same slowing.
- Two groups of trials on `outlier_rich` $N = 283$ at 6 drive times:
  - At $D = 5$ the quartiles are 367 and 799 s, and the median, 725 s, lies in the slow group.
  - At 6 to 12 dogs the median lies in the fast group (357-375 s) and the upper quartile in the slow one (774-815 s).
  - A median therefore describes such teams poorly, and the $D_{\mathrm{sat}}$ of this curve stays a bracket from 5 (5-24).

### 5. The upper end of the curves: D_max, D_crowd and D_overcrowd
Four values bound a curve from above ([frontier values](../experiments/task_design.md#frontier-values)):
- $D_{\mathrm{overcrowd}}$: the first team from which two tested sizes in a row are unreliable. It is looked for above $D_{\min}$, or, on a curve with no reliable team, above $D_{\min,\mathrm{low}}$, the smallest team not yet decided unreliable.
- $D_{\max}$: the largest reliable team below $D_{\mathrm{overcrowd}}$, or the largest reliable team when the curve has no $D_{\mathrm{overcrowd}}$. The reliable teams below $D_{\mathrm{overcrowd}}$ are the working teams.
- $D_{\mathrm{best}}$: the smallest working team as fast as the fastest one, within 5%.
- $D_{\mathrm{crowd}}$: the first working team above $D_{\mathrm{best}}$ that is more than 5% slower than it.

In the three 99% main runs:
- $D_{\max}$ is almost always the top of the grid: 84 of the 85 curves with a $D_{\min}$ are still reliable at 24 dogs and have no $D_{\mathrm{overcrowd}}$, so no upper limit was found and $D_{\max}$ is only a lower bound. The one exception, `outlier_rich` $N = 566$ at 6 drive times, has no $D_{\mathrm{overcrowd}}$, and 16 and 24 dogs are still undecided (188 of 200 = 0.94 and 189 of 200 = 0.945), so its largest reliable team is 12 and $D_{\max} = 12$.
- $D_{\mathrm{crowd}}$ appears on 6 curves at 12 drive times: `split` at $N = 71$, 200, 283, 400 and 566 (from 2 to 14 dogs) and `outlier_rich` $N = 566$ (15 dogs). These teams still succeed but finish later than the fastest team, which is the slowing described in item 4.
- $D_{\mathrm{overcrowd}}$ appears on 4 curves on which no team is decided reliable: `split` $N = 200$, 283 and 400 at 6 drive times (from 4, 15 and 10 dogs) and `outlier_rich` $N = 400$ at 3 (from 7). On these curves the larger teams stay near but mostly below $\theta$ (`split` $N = 200$: 0.60-0.95; `split` $N = 283$ from 5 dogs: 0.70-0.925; `split` $N = 400$ from 5 dogs: 0.70-0.92; `outlier_rich` $N = 400$ from 5 dogs: 0.60-0.86). The onset is the first point where two tested sizes in a row are decided unreliable on a curve with no team decided reliable. Some of these curves have teams whose success rate is above $\theta$ but still undecided (`split` $N = 200$, $D = 2$: 0.95; $N = 283$, $D = 6$: 0.925; $N = 400$, $D = 5$: 0.92).

More dogs do make the task fail in a few follow-up settings.

- With whole-team sharing at a range of 65 m, `split` $N = 200$ is reliable with 3 dogs, decided unreliable at 4, 6, 8, 9, 13, 14 and 16 dogs, and undecided at 0.85 with 10 and 12 ([section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it)).
- Near the smallest goal that holds a flock of 25, larger teams fail ([section 3.10](#310-rq10-when-do-more-dogs-hurt-holding-the-flock-and-dogs-that-take-up-room)).
- With dogs kept 2 m apart in the holding task, larger teams fail on two curves, neither of which has a reliable team. On `outlier_rich` $N = 400$ teams of 3 to 8 reach 0.87-0.94 (200 trials each), and from 9 dogs up success is 0.50-0.77 (10 to 70 trials per cell), so $D_{\mathrm{overcrowd}} = 9$. On `split` $N = 200$ success falls from 0.85 at $D = 2$ (170 of 200, undecided) to 0-0.10 from 6 dogs up (10 trials per cell).

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
- Left: seconds each sheep spends with a dog within 65 m. From $D_{\min}$ to $D_{\mathrm{sat}}$ it falls, because the flock is gathered sooner; beyond $D_{\mathrm{sat}}$ it hardly grows.
- Right: share of the flock fleeing, averaged over each trial.

At $N = 400$ one dog succeeded in none of its 10 trials and $D = 2$ was not replayed, so those curves start at 3.  
*Data:* [results_tables.md: Pressure, dmin_f99_m6](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

![Animation of the sheep fleeing from 3 dogs and from 12 dogs](../gifs/flock_pressure.gif)

**Animation 1: The flock under 3 and 12 dogs, replayed (`wide`, $N = 400$, seed 0, 99% rule, 6 drive times).** With 12 dogs more of the flock flees at once, but the drive is shorter, as in Figure 2. Both start from the same flock, and each replay reproduces its stored trial.

- Marks: filled dots are sheep within $r_s = 65$ m of a dog, which flee; hollow dots graze.
- Left: 3 dogs. At 148 s, 129 of the 400 sheep flee, and the flock is in at 727 s.
- Right: 12 dogs. At 148 s, 395 flee, and the flock is in at 431 s.

## 3.10 RQ10: When do more dogs hurt? Holding the flock, and dogs that take up room

In the open drive under the 99% rule, extra [point dogs](../glossary.md#sheep-models-and-dog-rules) (dogs with no size, as in all the main runs) never lost a reliable team in the main runs, apart from one dip (4 dogs on `split` $N = 141$ at 6 drive times, [section 3.7](#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)). They do in a few follow-up settings ([section 3.7](#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock), item 5).

The clearest cases are in holding, where the flock must stay in the goal while the dogs withdraw. Extra dogs hurt with dogs kept 2 m apart on `outlier_rich` $N = 400$ (result 2), and with a goal just too small for a flock of 25 (result 3). With 99% of the flock held, holding a flock of 50 or fewer fails with the default goal whatever the team (result 1). This may be because the flock walks out of the goal while the dogs withdraw; we have not tested it.

Three sets of protocols change the end of the task or the room each dog takes:

- Holding (`dmin_f99_hold`): the [holding task](../experiments/task_design.md#the-holding-task); a trial succeeds only once 99% of the flock has stayed in the goal for one drive time while the dogs withdraw, each to a point $r_s + r_a = 67$ m beyond the farthest sheep on its bearing from the flock centre.
- Dogs that take up room (`dmin_f99_hold_spacing`): the same task with [dogs kept 2 m apart](../experiments/task_design.md#crowding-with-dogs-that-take-up-room). The arc of dogs behind the flock then has room for a limited number, about $D_{\mathrm{cap}} = 7, 9, 10, 11, 12$ at $N = 25$ to 400 (the arc length divided by the 2 m spacing).
- The goal that holds a small flock (`dmin_f99_hold_goal`, `dmin_f99_hold_share`): the holding task at $N = 25$, 50 and 100 with the goal radius raised from $1.9 R_f$ to 2.1, 2.3 and $2.5 R_f$, crossed with the share that must stay in (99%, 95%, 90%), and to $3.0 R_f$ at 99%, on the seeds of `dmin_f99_hold`.

### Results

1. With 99% held, holding fails on small flocks: on larger flocks ($N \ge 100$) holding works on `wide` and `compact`, with the same $D_{\min}$ as the open drive or one more (1, 2 and 3 dogs on `wide` at $N = 100$, 200, 400). On `split` no team is decided reliable from $N = 200$, even with point dogs. At $N = 200$ one dog succeeds in 98 of 120 trials (decided unreliable) and two in 171 of 200 (undecided, 99% interval 0.78-0.91), so $D_{\min}$ is at least 2; larger teams succeed in 10% to 75% (10 to 60 trials per cell). At $N = 400$ every team is decided unreliable and none passes 0.70; with dogs kept 2 m apart, `split` $N = 200$ falls to 0-10% from 6 dogs.

   On small flocks ($N \le 50$) no team holds the flock. Of the failed trials, 423 of 560 at $N = 25$ (76%) and 301 of 444 at $N = 50$ (68%) end with no sheep in the goal. The flock enters the goal at its near edge with the dogs behind it. While the dogs withdraw they stay within 65 m of some sheep for 26 to 29 s, and the flock keeps walking. Its centre moves a median 17 m at $N = 25$, 15 m at $N = 50$ and 13 m at $N = 100$. These medians come from `cli/diagnostics/hold_walk.py`, which replayed all 240 stored trials with a goal of $3.0 R_f$, large enough not to cut the walk short. 239 of them give a walk; in the remaining one (`outlier_rich` $N = 100$, one dog) the dogs never cleared.

   A goal of $1.9 R_f$ is 11.8 m at $N = 25$ and 14.4 m at $N = 50$, so the leading sheep cross the far edge. Below $N = 100$ the 99% share is every sheep, so the first sheep out ends the hold. The dogs then come back, drive the flock from the far side and push it farther out. This points to the goal size against that walk as the cause of the failure; the walk itself was not varied.

2. Dogs that take up room make extra dogs harmful on `outlier_rich` $N = 400$ (Figure 3):
   - With 3 to 6 dogs the success rate is 0.925-0.94, undecided.
   - From $D = 9$ on, every team up to 24 is decided unreliable: 54 of 70 at $D = 9$ (99% interval 0.62-0.89), 13 of 20 at $D = 12$ (0.34-0.89), 5 of 10 at $D = 16$ (0.13-0.87).
   - This may be because the arc behind a flock of 400 holds only about 12 dogs 2 m apart ($D_{\mathrm{cap}}$); near or above that number, dogs push each other off their places on the arc and cannot leave it to catch a sheep that breaks away. We have not tested this, and it does not explain why failures start at 9 dogs, below that number.
   - On `compact` $N = 400$ every spaced team from 1 to 24 dogs is reliable. On `wide` $N = 400$, 3 dogs and every team from 6 to 24 are reliable, and 4 and 5 dogs are undecided (190 of 200 each). This may be because the dogs that do not fit on the arc stay behind it without getting in the way; we have not tested it. Whether extra dogs hurt therefore depends on the layout as well as on the space each dog takes.

![Holding with point dogs and with dogs 2 m apart](../figures/fig36_spacing.png)

**Figure 3: Holding at $N = 400$, point dogs against dogs kept 2 m apart.** On `wide` success holds up to 24 spaced dogs; on `outlier_rich` it falls from $D = 9$.

- Marks: success against $D$ (log scale), dotted grey for point dogs and solid blue for dogs 2 m apart. The orange band marks 10 to 12 dogs, the arc capacity $D_{\mathrm{cap}}$ of the larger flocks; the dashed line is $\theta = 0.90$, and hollow markers are cells with fewer than 30 trials.
- Panels: `wide` (left) and `outlier_rich` (right).

*Data:* [results_tables.md: D_min, dmin_f99_hold](results_tables.md#d_min-dmin_f99_hold) and [results_tables.md: D_min, dmin_f99_hold_spacing](results_tables.md#d_min-dmin_f99_hold_spacing).

3. With 99% of the flock held, a goal of about 16 to 19 m holds a small flock with one dog, and with 95% or 90% held 13.0 to 14.4 m is enough at $N = 25$ and 50 (Figure 4). Table 2 gives, for each share, the smallest goal tested from which one dog is decided reliable on every layout; a range means one dog is still undecided at the smaller goal.
   - With 99% held, the threshold is $2.5$-$3.0 R_f$ (15.5-18.6 m) at $N = 25$ and $2.1$-$2.3 R_f$ (16.0-17.5 m) at $N = 50$. At $N = 100$ the default $1.9 R_f$ (17.3 m) already holds the flock with one dog on three layouts; it is an upper bound, since no smaller goal was tested. In metres the thresholds are close to each other, while in flock radii they fall from about 2.5 to 1.9.
   - The walk predicts this. A flock enters with its last sheep at the near edge and walks $w$. It keeps every sheep in only if the goal radius exceeds about $w/2$ plus the distance of its farthest sheep from the centre. This gives 14.3, 15.7 and 17.2 m at $N = 25$, 50 and 100 (medians over the replays), at or just below the thresholds observed. The agreement is consistent with the walk being the cause; the walk itself was not varied.
   - Letting sheep stay out lowers the goal needed: at $N = 25$ one sheep out (95%) lowers it by one step of the tested grid or more, from 15.5-18.6 m to 14.3 m, and a second (90%) by up to one more step, to 13.0-14.3 m. At $N = 50$ two sheep out (95%) are enough for the default goal of 14.4 m, at least 1.5 m below the 99% threshold.
   - Near the threshold some larger teams fail. Where a goal holds the flock with margin, one dog does and larger teams do as well. At a goal just short of that:
     - at $N = 25$, 90%, $2.1 R_f$, one dog is reliable on `split` and `outlier_rich`, while on every layout teams from 3 to 7 dogs upward are decided unreliable (success down to 0.50);
     - at $N = 50$, 99%, $2.1 R_f$, no team is decided reliable on any layout, and one dog is undecided everywhere (0.895-0.935, 200 trials each). On `wide` and `outlier_rich` 4 dogs are decided unreliable (159 of 190 and 97 of 120, labelled `unreliable_dip`), while 5 to 24 dogs stay undecided (`wide` 0.845-0.89, `outlier_rich` 0.855-0.875). On `wide`, 3 dogs (0.94) do slightly better than one (0.935).
   - In the walk replays at $N = 25$ (goal $3.0 R_f$, 99% held, 20 replays per team size from 5 seeds on each of the 4 layouts, no interval computed), the median walk during the withdrawal is 17.5-17.8 m with 2, 4 or 8 dogs and 16.6 m with one. A longer walk may be why larger teams fail at a goal just short of the threshold, such as $2.1 R_f$ with 90% held; we have not tested it, and the walk was measured at another goal and share.
   - At $N = 100$ only `outlier_rich` needs more than one dog: 3 at the default goal with 99% held, 2 with any larger goal or smaller share.
   - Where the three holding protocols share a cell, their shared trials reproduce each other exactly, with the same outcome and length. `dmin_f99_hold` shares 2410 trials with `dmin_f99_hold_share` and 3750 with `dmin_f99_hold_goal`, all at the default goal with 99% held. `dmin_f99_hold_goal` and `dmin_f99_hold_share` share 9830 trials (7420 at $2.5 R_f$ and 2410 at the default goal), all with 99% held. No generated table states these counts; they come from matching the stored `trials.csv` of the three folders on layout, $N$, $D$, seed, goal and share.

Table 2 lists the smallest goal tested from which one dog is decided reliable on every layout (holding for one drive time, 6 drive times; "<=" where the default $1.9 R_f$, the smallest goal tested, already holds):

**Table 2: Smallest goal tested from which one dog is decided reliable on every layout.**

| Share that must stay in | $N = 25$ | $N = 50$ | $N = 100$ |
| :--- | :---: | :---: | :---: |
| 99% (out: none below $N = 100$, one at 100) | $2.5$-$3.0 R_f$ = 15.5-18.6 m | $2.1$-$2.3 R_f$ = 16.0-17.5 m | <= $1.9 R_f$ = 17.3 m (`outlier_rich` 3) |
| 95% (out: one of 25, two of 50, five of 100) | $2.3 R_f$ = 14.3 m | <= $1.9 R_f$ = 14.4 m | <= $1.9 R_f$ = 17.3 m (`outlier_rich` 2) |
| 90% (out: two of 25, five of 50, ten of 100) | $2.1$-$2.3 R_f$ = 13.0-14.3 m | <= $1.9 R_f$ = 14.4 m | <= $1.9 R_f$ = 17.3 m (`outlier_rich` 2) |

At $N = 25$ and 99%, $2.5 R_f$ holds `compact` and `split` with one dog while `wide` (1-2) and `outlier_rich` (1-3) are still open; at $N = 25$ and 90%, $2.1 R_f$ holds `split` and `outlier_rich` with one dog while `compact` and `wide` are still bounds ([1]); at $N = 50$ and 99%, one dog at $2.1 R_f$ is undecided on every layout (success 0.895-0.935 over 200 seeds).  
*Data:* [results_tables.md: dmin_f99_hold_goal](results_tables.md#dmin_f99_hold_goal-dmin_f99_hold--dmin_f99_hold_goal), [results_tables.md: dmin_f99_hold_share](results_tables.md#dmin_f99_hold_share-dmin_f99_hold--dmin_f99_hold_share) and [results_tables.md: walk while the dogs withdraw](results_tables.md#walk-while-the-dogs-withdraw-dmin_f99_hold_goal-at-30-r_f-replay-of-5-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

![Holding a small flock: success against the goal radius](../figures/fig40_hold_goal.png)

**Figure 4: Holding success against the goal radius in metres, for each share that must stay in.** With 99% held, the curves of $N = 25$ and 50 rise between about 13 and 17.5 m, and $N = 100$ is already above $\theta$ at its default 17.3 m; letting one or two sheep out moves the rise of the small flocks to smaller goals.

- Marks: each point is the mean success rate over the 20 cells of one flock size and goal (4 layouts x $D = 1, 2, 4, 8, 24$, each cell counted once, without the midpoints the adaptive run added). The bar is the range over those cells, and its low end near the threshold is the larger teams; at $N = 100$ the low end is `outlier_rich` with one dog. Blue is $N = 25$, orange $N = 50$, green $N = 100$; ringed points are the default goal of $1.9 R_f$, and the dashed line is $\theta = 0.90$.
- Panels: 90%, 95% and 99% of the flock must stay in the goal for one drive time, from left to right.

*Data:* `results/dmin_f99_hold_share` and `results/dmin_f99_hold_goal` (the $3.0 R_f$ points).

Animation 1 in [task design](../experiments/task_design.md#the-holding-task) replays one dog holding a flock of 25 in a goal of $1.9 R_f$, where the flock walks out, and of $3.0 R_f$, where it is held.
