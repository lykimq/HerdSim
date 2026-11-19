# Independent paper shepherds: `independent`

This baseline tests what a team gets from Strombom's one-dog rule alone, with no team layer on top ([report, section 2.5](../report/d_min_report.md#25-rq5-what-does-the-team-layer-add-over-independent-shepherds)). It sits between the uncoordinated baseline [`fat`](fat.md) and the team rule [`strombom_multi`](strombom_multi.md).

Every dog runs Strombom's one-dog rule on the whole flock, as described in [strombom_multi.md](strombom_multi.md):

- Collect: if any sheep is farther than $f(N) = r_a N^{2/3}$ from the flock centre $\mathrm{GCM}$, the dog aims at the collect point $P_c$, $r_a = 2$ m behind the sheep farthest from $\mathrm{GCM}$.
- Drive: otherwise it aims at the drive point $P_d$, $r_a\sqrt{N}$ behind $\mathrm{GCM}$ on the side away from the goal.

The dog's step, noise and stop rule are the same as in `strombom_multi`. What is missing is the team layer: there is no Hungarian assignment of dogs to separate outliers and no arc of driving slots. Every dog sees the same flock and computes the same target, so all $D$ dogs aim at the same point at every tick (Figure 1, Animation 1).

![Team rule and independent dogs collecting and driving](../figures/fig_independent.png)

**Figure 1: The team rule against `independent` ($N = 100$, $D = 4$).** Without a team layer, every dog aims at the same point, both when collecting and when driving.

- Marks: blue dots are sheep, orange triangles are dogs, the plus sign is the $\mathrm{GCM}$, and crosses are target points; arrows are dashed for `independent`.
- Left: the team rule `strombom_multi`, where 4 dogs collect 4 different outliers at once through the Hungarian assignment.
- Middle: `independent` collecting, where all 4 dogs chase the same outlier and no dog goes to the other outliers.
- Right: `independent` driving, where all dogs head for the single point $P_d$ instead of spreading along the driving arc (dotted green line).

## Comparison with `strombom_multi` and `fat`

Table 1 lists what each of the three dog rules has. Each row adds one layer to the row above it, so comparing neighbouring rows shows what that layer adds.

**Table 1: The three dog rules.**

| Rule | Collect or drive switch | Outlier assignment | Driving formation |
| :--- | :--- | :--- | :--- |
| `fat` ([fat.md](fat.md)) | None: always pushes the sheep farthest from the goal | None: all dogs aim behind the same sheep | None: all dogs aim at the same point |
| `independent` | Yes: collects while any sheep is beyond $f(N)$ | None: all dogs chase the outlier farthest from $\mathrm{GCM}$ | None: all dogs aim at $P_d$ |
| `strombom_multi` ([strombom_multi.md](strombom_multi.md)) | Yes: collects while any sheep is beyond $f(N)$ | Hungarian assignment of the $D$ farthest outliers | Arc of $D$ slots as wide as the flock |

At 6 drive times under the 99% rule, `independent` has a reliable team on every layout up to $N = 200$, and no reliable team up to 24 dogs (the largest team tested) on `wide`, `split` and `outlier_rich` at $N = 400$. The results and a possible cause are in the [report, section 2.5](../report/d_min_report.md#25-rq5-what-does-the-team-layer-add-over-independent-shepherds).

## Shared calibration (`calibrate_as: strombom_multi`)

The protocol [`dmin_f99_indep.yaml`](../../protocols/configs/protocols/dmin_f99_indep.yaml) sets `calibrate_as: strombom_multi`. With one dog, `independent` and `strombom_multi` are the same rule, and the calibration uses one dog. Both rules therefore run on the same [task lengths](../experiments/task_design.md#sizing-by-the-calibrated-flock-radius) (calibrated flock radius $R_f(N)$, goal radius, drive distance), start flocks and deadline. The FAT protocols do the same ([fat.md](fat.md#shared-calibration-calibrate_as-strombom_multi)).

Animation 1 shows the three dog rules on the same start flock.

![Animation of three dog rules on one start flock](../gifs/controllers.gif)

**Animation 1: Three dog rules on the same start flock (`wide`, $N = 400$, $D = 4$, seed 0, 99% rule, 6 drive times).** Only the team rule brings the flock in; both baselines fail when time is up.

- Marks: blue dots are sheep, orange triangles are dogs, and the green circle is the goal; the bottom-left text gives the time and the number of sheep outside the goal.
- Left: the team rule gives each dog its own outlier while collecting, then drives from an arc, and succeeds at 569 s (`dmin_f99_m6`).
- Middle: the `independent` dogs all chase the same outlier, crowd together and fail at the 1241 s deadline with no sheep in the goal (`dmin_f99_indep`).
- Right: every `fat` dog aims behind the sheep farthest from the goal, and the team fails at 1241 s (`dmin_f99_fat`).

## References

1. Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719, [10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719).
