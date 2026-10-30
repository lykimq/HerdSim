# Why trials fail: the `split` layout and how failed trials end

Part 5 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 4. A closer look: the `split` layout and per-tick measures

### 4.1 Why more dogs do not help on `split`
A [`split`](../glossary.md#start-layouts-and-dog-starts) flock starts as three separate clusters. From $N = 200$ sheep, adding dogs beyond about 4 to 5 does not raise success on it, and at 6 [drive times](../glossary.md#the-drive-task) no team is reliable at $N = 200$ or 400 under either [success rule](../glossary.md#success-and-reliability).

At 6 drive times under the 99% rule, every tested team of $D \ge 4$ dogs succeeds in 0.60-0.90 of trials at $N = 200$ and 0.70-0.92 at $N = 400$. Under the strict rule they reach 0.50-0.76 at $N = 200$ and 0.10-0.50 at $N = 400$, where every cell has 10 trials (1 to 5 of 10). The two runs test different teams: the strict run tests 4, 6, 8, 12, 16 and 24 dogs, and the 99% run adds 7, 10 and 11 at $N = 200$, and 5, 9, 10, 14, 15 and 18-20 at $N = 400$. Figure 1 shows the 6 drive-time curves; it does not plot the 3 drive-time runs. At 3 drive times success falls to at most 1 of 10 trials for 99%-rule teams of 6 or more dogs at $N = 200$ and 8 or more at $N = 400$, and for every strict-rule team at both sizes (`uv run cli/dmin_tables.py curve dmin_f99_m3 --layout split --n 200`, and the same verb on `dmin_m3` and $N = 400$).

From $N = 200$ up, in the successful trials of most teams from 3 dogs up, the flock arrives in two parts. At $N = 100$ no team shows it: the median time from 90% to 99% is 4-5 s for every $D$. At 6 drive times on `split` $N = 200$ (99% rule), going from 90% to 99% of the flock in the goal takes a median 7 s with one or two dogs. With 3 dogs, and with teams from 6 up, it takes 249 to 418 s, or 43% to 60% of the median finish time, though 6 and 24 dogs have only 13 and 12 successes. 4 dogs are the exception, at 22 s over 38 successes. The values for $N = 283$ to 566 are in the [single-trial tables](results_tables.md#single-trials-and-curves-across-folders).

Other dog rules do better on `split` $N = 200$ (6 drive times, 99% rule), where the [team rule](../glossary.md#sheep-models-and-dog-rules) succeeds in 0.60-0.95 of trials and has no reliable team (`dmin_f99_m6`). Independent shepherds, each running Strömbom's single-dog rule on its own, are reliable from 3 dogs ([section 3.9](part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters)). Dogs that see only 30 to 65 m and do not share succeed in all 60 trials of every team from 3 to 16 dogs, against 0.80-0.93 for the full-sight control of their own run, `dmin_f99_view_range` ([section 3.12](part4_coordination.md#312-rq12-what-a-dog-sees-and-sharing-it)). The two runs repeat the same setup and disagree for a single dog (169 of 200 trials in one, 183 of 200 in the other), so each variant is compared with the control of its own run. Independent shepherds lack only the team layer, which assigns dogs to outliers and sets the arc they drive from. This may help them on `split` because of the first cause below; we have not tested it.

Replays of stored trials at $N = 200$ (`cli/diagnostics/split_diagnostic.py`, 12 stored seeds per cell, 99% rule), each with one change to the team rule, point to two possible causes. At 6 drive times the median finish of the successful seeds fell with each change at the team sizes given below, except that spreading the collecting dogs slowed it at $D = 2$ (365 s to 393.5 s). A median over successful seeds only can fall when fewer seeds succeed: at $D = 4$ both changes lowered the success from 11 of 12 seeds to 10 of 12.

1. All collecting dogs may go to one cluster ($D = 4$): the team rule sends its dogs to the $D$ outliers farthest from the flock centre (an outlier is a sheep farther than the collect distance $f(N) = r_a N^{2/3}$, with $r_a = 2$ m), whatever cluster they are in. They can all lie in one cluster while another drifts. With the dogs taking the farthest outliers that were at least $f(N)$ apart, the median finish of the successful seeds at $D = 4$ and 6 drive times fell from 631 s (11 of 12 seeds succeeded) to 317.5 s (10 of 12); the two sets of successful seeds differ.
2. Many dogs stand still, which the stop rule may cause ($D \ge 4$): Strömbom's dog stops while any sheep is within $3 r_a = 6$ m ([stop rule](../glossary.md#sheep-models-and-dog-rules)). At $N = 200$ (99% rule, 6 drive times) and $D \ge 4$, the median share of dogs with zero commanded speed is about 1% on `wide`, 3% to 4% on `outlier_rich` and about 25% on `split` (Figure 2). This share does not say where those dogs stand or which rule stopped them. With the stop distance cut to $r_a = 2$ m, the median finish of the successful seeds was 21-24% faster at $D = 8$ and 16. It was also faster at $D = 2$ (365 s to 332 s) and at $D = 4$ (631 s to 476 s, with 10 of 12 seeds succeeding against 11 of 12).

At 3 drive times neither change made `split` reliable: at 4, 8 and 16 dogs no version succeeded in more than 7 of 12 seeds, and with that few successes the 99% interval rules out reliability.

![Split curves and metric diagnoses](../figures/fig23_split_curves.png)

**Figure 1: Success against team size on `split` at $N = 100$, 200 and 400 and on `wide` at $N = 400$ (strict and 99% rules, 6 drive times).** On `wide` $N = 400$ every team from 3 dogs is reliable under the 99% rule, while under the strict rule the best cell reaches 182 of 200 (0.91) and none is reliable. On `split` at $N = 200$ and 400 no team is reliable under either rule; some 99% cells reach 0.90-0.95 (2 dogs at $N = 200$: 190 of 200) but stay undecided. At $N = 100$ every team is reliable under the 99% rule; under the strict rule 3 dogs are unreliable (36 of 50), 2 and 4 dogs are undecided (179 and 177 of 200) and the other teams are reliable.

- Marks: blue circles are the strict rule and orange squares the 99% rule, each with its 99% Clopper-Pearson interval, against $D$ on a log scale. The dotted line is $\theta = 0.90$.
- Panels: `split` at $N = 100$, 200 and 400, and `wide` at $N = 400$ for comparison.

*Data:* `results/dmin_m6` and `results/dmin_f99_m6`; values in [results_tables.md: dmin_m6](results_tables.md#dmin_m6) and [results_tables.md: dmin_f99_m6](results_tables.md#dmin_f99_m6).

![Animation of two seeds of one split cell](../gifs/split.gif)

**Animation 1: Two seeds of one `split` cell, replayed ($N = 200$, 16 dogs, 99% rule, 6 drive times).** The same team succeeds on one start and fails on another. Each replay reproduces its stored trial.

- Left: seed 4 brings the clusters together and succeeds at 283 s.
- Right: seed 8 brings 196 of the 200 sheep into the goal, then drives the flock back out and runs out of time with its centre 139 m from the goal.

At 6 drive times on `split` $N = 200$, independent shepherds are reliable and two replayed changes to the team rule made the drive faster at most team sizes, but neither showed a reliable team. With 12 seeds per cell, 12 of 12 successes at $D = 8$ and 16 leaves the cell undecided (the lower end of the 99% interval is 0.64). The cause of the limit is not established; the two replayed changes point to the assignment and to dogs held still.

### 4.2 Per-tick measures
Two measures are recorded at every tick, one step of the simulation. At 6 drive times, cells whose flock stays spread out succeed less often. At $N = 200$ (99% rule, 6 drive times), in teams of 16 many dogs stand within 2 m of another dog.

The flock spread is the RMS distance of the sheep to their centroid, averaged over the trial. Over the [cells](../glossary.md#trials-and-experiments) with at least 20 seeds, the rank correlation (Spearman) between a cell's mean spread and its success rate at 6 drive times is $-0.76$ under the strict rule (167 cells) and $-0.71$ under the 99% rule (337 cells; Figure 2). At 12 drive times under the 99% rule it is $-0.17$ (339 cells). Because the spread is a whole-trial average, this does not tell whether a spread flock leads to failure or a failing trial keeps the flock spread.

Dog bunching is the share of a trial's dogs that have another dog within 2 m, averaged over the trial, with the median taken over trials. At $N = 200$, $D = 16$ (99% rule, 6 drive times) it is 0.55 on `wide`, 0.45 on `outlier_rich` and 0.59 on `split` with the team rule. With [FAT](../glossary.md#sheep-models-and-dog-rules), where every dog goes behind the sheep farthest from the goal, it is 0.74, 0.78 and 0.90 on the same layouts (10 trials each). With 2 FAT dogs on `wide` and `outlier_rich` at $N = 200$ and 400 the median is 0.00-0.005 (10 trials each), so the bunching FAT's rule leads one to expect does not show there.

![Per-trial metrics](../figures/fig27_metrics.png)

**Figure 2: Per-tick measures at 6 drive times (left: strict and 99% rules; middle and right: $N = 200$, 99% rule).** Cells whose flock stays more spread out succeed less often, and on `split` about a quarter of the dogs stand still at $D \ge 4$.

- Left: mean flock spread over the trial (RMS distance to the centroid) against the success rate, one point per cell with at least 20 seeds, coloured by layout, circles for the strict rule and squares for the 99% rule. The rank correlation is $-0.76$ strict and $-0.71$ at 99%.
- Middle: median share of dogs standing still (commanded speed zero) against $D$ at $N = 200$ (99% rule) for `wide`, `split` and `outlier_rich`.
- Right: median share of dogs with another dog within 2 m against $D$, for the same cells.

*Data:* `results/dmin_m6` and `results/dmin_f99_m6`; no `dmin_tables.py` verb prints the correlations or the overlap shares; they come from the trial reader of `docs/generate_docs/make_result_figures.py` and the stored per-trial columns.

### 4.3 How failed trials end, and the start spread

In each of the six main protocols, 70.6% to 90.6% of the failed drive trials end with the flock centre far from the goal (Table 1). At $N = 400$ the start spread separates compact from scattered starts, but it does not order the scattered layouts (Table 2); at small $N$ some scattered layouts also reach 100% success.

A failed trial ended near the goal when the flock centre ended within two goal radii of the goal centre (our choice; no other cutoff was tried), and far otherwise. The rule uses only where the centre ended: it does not tell whether the flock reached the goal earlier, or whether more time would have saved the trial.

**Table 1: Failed drive trials by where the flock ended.**

| Protocol | Rule | Failed trials | Far from goal | Near goal | Share far |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `dmin_m12` | strict, 12x | 235 | 180 | 55 | 76.6% |
| `dmin_m6` | strict, 6x | 889 | 639 | 250 | 71.9% |
| `dmin_m3` | strict, 3x | 710 | 571 | 139 | 80.4% |
| `dmin_f99_m12` | 99%, 12x | 235 | 213 | 22 | 90.6% |
| `dmin_f99_m6` | 99%, 6x | 1511 | 1067 | 444 | 70.6% |
| `dmin_f99_m3` | 99%, 3x | 584 | 457 | 127 | 78.3% |

*Data:* the command below, on the six main protocols.

```bash
uv run cli/dmin_tables.py dispersion
```

The failure labels are heuristic patterns read from each trial's history and named after what they look for, such as `flock_escaped` (over the second half of the trial the flock centre was on average farther from the goal than at the start), `stuck` (the mean distance of the flock centre from the goal changed by less than one goal radius between the two halves of the trial) and `scatter` (the flock stayed spread out). A failed trial that matches no pattern is a plain timeout. At 6 drive times under the 99% rule 1049 of the 1511 failures match no pattern and are plain timeouts. At 12 drive times under the 99% rule 182 of the 235 failures match a pattern, most often `flock_escaped` (105 of 235; `uv run cli/dmin_tables.py labels dmin_f99_m6 dmin_f99_m12`).

$S_0$ is the flock's start spread, its RMS radius at the start, and $S_0 \times N$, the start radius times the number of sheep, is HerdSim's own rough measure of how much gathering a layout asks for: it grows with both how far out the sheep start and how many there are. At $N = 400$ it is 8 to 13 times larger on the scattered layouts than on `compact`; this includes an over-estimate of the `compact` start spread of up to 26%, explained under Table 2. Under the strict rule at 6 drive times, success pooled over every team size is 100% on `compact` at every $N$. The scattered layouts also reach 100% at $N = 25$ and, on `wide`, at $N = 50$; at $N = 50$ it is 99.8% on `outlier_rich` and 99.3% on `split`. At $N = 400$ it is 84% on `wide`, 55% on `outlier_rich` and 21% on `split` (Table 2). `outlier_rich` has a smaller product than `wide` and a lower success rate. This may be because how the outliers are placed matters as well as how far out they start; we have not tested it.

**Table 2: Start spread, its product with $N$, and success rate (strict rule, `dmin_m6`, 6 drive times).**

| Layout | $N$ | Start spread $S_0$ (m) | $S_0 \times N$ (m) | Success rate (all $D$) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 25 | 4.8 | 119 | 100.0% |
| `compact` | 100 | 6.7 | 665 | 100.0% |
| `compact` | 400 | 8.3 | 3316 | 100.0% |
| `wide` | 400 | 74.8 | 29,931 | 83.8% |
| `outlier_rich` | 400 | 66.2 | 26,496 | 55.3% |
| `split` | 400 | 108.8 | 43,507 | 21.1% |

*Data:* `uv run cli/dmin_tables.py dispersion` on `dmin_m6`; $S_0$ is the mean of `max_extent`, the flock's largest RMS radius in a trial, which the code takes as the start. On `compact` it is up to 26% larger than the start. The success rate pools every tested team, including $D = 1$, so it depends on the grid.
