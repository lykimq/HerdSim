# Coordination and what the dogs see

Part 4 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules) that define $D_{\min}$, its brackets and lower bounds, the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## 3.6 RQ6: Do dogs without a team rule reach a finite D_min?

FAT (farthest-agent targeting) is a baseline without coordination: every dog goes behind the sheep farthest from the goal. It is compared with the team rule `strombom_multi`, which switches each dog between collecting strays and driving the flock and has a team layer that assigns dogs to strays ([section 3.9](#39-rq9-which-part-of-the-team-rule-matters)).

Can dogs that do not coordinate do the job if there are enough of them? Not on large flocks: from $N = 200$ FAT has no reliable team on any scattered layout, and adding dogs does not help (item 1). Its dogs end up close together behind the same sheep (item 2).

1. FAT fails on large flocks.  
   FAT is reliable on small flocks ($N \le 100$) but has no reliable team at $N \ge 200$ on any scattered layout, and none on compact $N = 400$, where the team rule needs one dog. Adding dogs does not help (Figure 1).

2. Why.  
   Every dog sees every sheep and picks by the same rule, so all $D$ dogs chase the same sheep. They bunch together: at $N \ge 200$ the median share of dogs with another dog within 2 m, for teams of two or more, is 0.86 on `compact` and 0.79 on `split` (0.46 on `wide`, 0.30 on `outlier_rich`). A larger FAT team is a larger pack behind one sheep while the rest of the flock spreads out.  
   The independent shepherds of [section 3.9](#39-rq9-which-part-of-the-team-rule-matters) also have no team layer, but they keep Strömbom's collect/drive switch, and they reach a finite $D_{\min}$ up to $N = 200$. FAT may fail because it has neither the team layer nor the switch; no run gave FAT the switch alone.

Table 1 compares FAT with `strombom_multi` at 6 drive times (FAT strict / 99%, with `strombom_multi` in brackets):

**Table 1: FAT against `strombom_multi` at 6 drive times, strict / 99% rule.**

| Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

*Data:* [results_tables.md: FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); `strombom_multi` in [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT against the coordinated team rule](../figures/fig26_fat.png)

**Figure 1: Success against team size for `strombom_multi` and FAT at 6 drive times.** Beyond two dogs FAT never reaches $\theta$, while `strombom_multi` becomes reliable on `wide` and `outlier_rich`.

- Marks: blue is `strombom_multi`, orange FAT; solid lines are the strict rule, dashed the 99% rule, and the dotted line is $\theta = 0.90$. Each marker is one cell; hollow markers are cells with fewer than 30 trials, decided early and so less certain.
- Panels: `compact` $N = 400$, `wide` $N = 200$ and 400, `outlier_rich` $N = 200$, and `split` $N = 200$. FAT stays below about 0.55 on `wide` and `outlier_rich`, and below 0.9 on `compact` $N = 400$ and `split` $N = 200$.

*Data:* `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` and `dmin_f99_m6`.

Animation 7 in [models](../methods/models.md#independent-paper-shepherds-independent) replays the team rule, independent dogs and FAT on one start flock of 400; only the team rule brings it in.

## 3.9 RQ9: Which part of the team rule matters?

Which part of the team rule makes a team work: Strömbom's switch between collecting and driving, or the team layer that assigns dogs to strays? Each matters at a different size: the switch alone carries a team to $N = 200$, and the team layer is needed at $N = 400$ (items 1 and 2, Table 2). On `split` $N = 200$ the order reverses (item 2).

FAT ([section 3.6](#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min)) lacks two things the team rule has: (1) Strömbom's switch between collecting outliers and driving the flock, and (2) the team layer, which assigns dogs to outliers (Hungarian assignment) and spreads them on an arc behind the flock in angular order.

To separate the two, `dmin_f99_indep` runs a team of independent paper shepherds: each dog runs Strömbom's single-dog rule on the whole flock, with no assignment and no arc.

1. The switch alone is enough up to $N = 200$.  
   Independent shepherds are reliable on every scattered layout up to $N = 200$, where FAT fails: 2–3 dogs on `wide`, 3 on `outlier_rich`. This may be because switching to driving once the flock is gathered keeps it together, even when the dogs chase the same outlier; we have not tested it.

2. At $N = 400$ the team layer is needed.  
   Independent shepherds have no reliable team up to 24 dogs at $N = 400$. The team rule needs 2–3 dogs on `wide` and 3 on `outlier_rich`. This may be because, without assignment, the dogs keep going after the same sheep while other parts of a large flock spread; we have not tested it. On `split` $N = 200$ the order reverses: independent shepherds are reliable from 3 dogs, while the team rule has no reliable team ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)).

3. In the Kubo model more dogs keep helping, with diminishing returns.  
   With Kubo sheep (`dmin_f99_kubo`), one dog is enough on compact flocks of 25 to 100. Unlike Strömbom sheep, Kubo sheep walk faster under a stronger push (up to 5 m/s), so more dogs shorten the drive: at $N = 100$ the median finish time falls from 115 s with one dog to 29 s with ten, and to 25 s with 24. Ten dogs already give 95% of the gain of 24, but $D_{\mathrm{sat}}$ is still open: it is at least 16 or 17 dogs (16–24 at $N = 25$ and 100, 17–24 at 50).

Table 2 compares the three rules at 6 drive times (99% rule):

**Table 2: $D_{\min}$ of the team rule, independent shepherds and FAT at 6 drive times, 99% rule.**

| `strombom_multi` / `independent` / `fat` | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

*Data:* [results_tables.md: Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) and [results_tables.md: Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); Kubo finish times from `results/dmin_f99_kubo`.

## 3.12 RQ12: What a dog sees, and sharing it

Real dogs, robots and drones do not see the whole field. Here each dog sees only the sheep within a sensing range (15, 30, 45, 65 or 100 m), and dogs share what they see in one of three ways: not at all (`none`), with the dogs in range (`neighbour`), or with the whole team (`shared`).

How much does a limited view cost, and does sharing make up for it? On `wide` $N = 200$ a range of 30 to 65 m costs about one dog, and at 65 m sharing with the whole team brings $D_{\min}$ back to its full-sight value; at 15 m far more dogs are needed (items 1 to 3, Figure 2). On `split` $N = 200$ the result reverses (item 3).

1. A realistic range costs about one dog.  
   On `wide` $N = 200$, dogs that see everything need 2. With a range of 30 to 65 m they need 3 (3–4 at 45 m). On flocks of 100 or fewer a range of 30 m or more costs nothing (Figure 2).

2. At 15 m far more dogs are needed.  
   With a range of 15 m on `wide`, no team up to 16 is reliable at $N = 50$, and at $N = 100$ at least 6 dogs are needed. This may be because, once the range is shorter than the gaps between strays, the dogs lose sight of the outer sheep; we have not measured those gaps.

3. Sharing with the whole team wins the dog back.  
   At 65 m on `wide` $N = 200$, dogs that do not share need 3. Sharing with the whole team brings $D_{\min}$ back to 2, as with full sight. Sharing only with the dogs in range does not help (still 3): a dog far away has to learn about a stray it cannot see. On `split` $N = 200$ the order reverses: dogs that see everything have no reliable team ([1], a lower bound), while dogs that see 30 to 65 m and do not share succeed in 60 of 60 trials at every team from 3 to 16 dogs. Sharing with the whole team is reliable with 3 dogs but fails from 4 up ([section 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)). Why the full view hurts on `split` was not tested.

![D_min against sensing range, and sharing](../figures/fig37_view.png)

**Figure 2: $D_{\min}$ against sensing range, and the effect of sharing.** At 15 m `wide` needs at least 6 dogs at $N = 100$ and 7 at $N = 200$; on `wide`, sharing what each dog sees with the whole team matches full sight.

- Left: $D_{\min}$ against the range for `wide` (circles) and `split` (squares) at $N = 100$ (faded) and $N = 200$, with a bar for a bracket and a hollow triangle for a lower bound ([section 2.1](d_min_report.md#21-when-a-team-is-reliable)); each layout and $N$ is shifted sideways a little. The dashed line marks 65 m, the distance at which a sheep reacts.
- Right: success against $D$ on `wide` $N = 200$ at a range of 65 m, with no sharing (dotted blue), sharing with dogs in range (dashed blue), sharing with the whole team (solid blue) and full sight (solid black). Hollow markers are cells with fewer than 30 trials.

*Data:* [results_tables.md: Views: sensing range](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) and [results_tables.md: Views: sharing at range 65](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

![Animation of two dogs with a 65 m range, without and with sharing](../gifs/sight_sharing.gif)

**Animation 1: Two dogs that see 65 m, without and with sharing, replayed (`wide`, $N = 200$, $D = 2$, seed 0, 99% rule, 6 drive times).** Sharing what each dog sees turns a failed trial into a success. Without sharing this cell succeeds in 3 of 10 trials (99% interval 0.04–0.74); with sharing in 88 of 90 (0.90–1.00), which makes 2 dogs reliable. Each replay reproduces its stored trial (`dmin_f99_view_range`, `dmin_f99_view_comm`).

- Marks: dashed circles are each dog's sensing range; hollow dots are sheep that no dog sees.
- Left: without sharing each dog plans on its own view. The two dogs end up on either side of a long, thin flock, a few strays at its ends stay unseen, and the trial runs out of time at 817 s.
- Right: with sharing the team plans once on every sheep either dog sees, gathers the flock and brings it in at 275 s.
