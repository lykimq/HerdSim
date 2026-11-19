# Uncoordinated greedy baseline: `fat`

Farthest-agent targeting, or FAT, tests whether coordination between dogs is needed at all ([report, section 2.4](../report/d_min_report.md#24-rq4-do-uncoordinated-fat-dogs-reach-a-finite-d_min)). It is the simplest of the three dog rules; [independent.md](independent.md#comparison-with-strombom_multi-and-fat) compares all three.

Every FAT dog aims at the same point: $r_a = 2$ m behind the sheep farthest from the goal, on the side away from the goal. Strombom's rule instead picks the sheep farthest from the flock centre. FAT has no collect or drive switch, no assignment of dogs to sheep and no driving arc. The dogs move with [Strombom's step, noise and stop rule](strombom_multi.md#dog-speed-step-and-stop-rule). Nothing keeps them apart, so they bunch behind one sheep (Figure 1).

![Strömbom and FAT targets, and four FAT dogs bunching](../figures/fig4_fat.png)

**Figure 1: Bunching in FAT (`wide`, $N = 100$).** Every FAT dog picks the same sheep, so the dogs bunch behind it.

- Marks: blue dots are sheep and orange triangles are dogs; the orange circle marks the chosen sheep, the cross the dog's target, and the green arrow the direction to the goal.
- Left: Strombom's one-dog rule, behind the sheep farthest from the flock centre $\mathrm{GCM}$.
- Middle: FAT with one dog, behind the sheep farthest from the goal.
- Right: FAT with 4 dogs, bunched on the same sheep.

## Target

At each tick, with sheep positions $\mathbf{x}_1, \dots, \mathbf{x}_N$ and goal centre $\mathbf{g}$, FAT picks the sheep $i^*$ farthest from the goal:

$$
i^* = \arg\max_{i \in \{1, \dots, N\}} \lVert \mathbf{x}_i - \mathbf{g} \rVert
$$

The target is $r_a$ behind that sheep, on the line from the goal through it:

$$
P_{\mathrm{FAT}} = \mathbf{x}_{i^\ast} + r_a \frac{\mathbf{x}_{i^\ast} - \mathbf{g}}{\lVert \mathbf{x}_{i^\ast} - \mathbf{g} \rVert}
$$

Every dog $d = 1, \dots, D$ gets this same target $\mathbf{T}_d = P_{\mathrm{FAT}}$. Everything else is the same as for `strombom_multi`: the sheep model and its weights ([strombom_sheep.md](strombom_sheep.md)), and the dog speed $v_{\mathrm{dog}} = 1.5$ m/s, noise $e = 0.3$ and stop distance $3\,r_a = 6$ m.

At 6 drive times, no FAT team up to 24 dogs (the largest team tested) is reliable on `wide`, `split` or `outlier_rich` from $N = 200$, under either success rule. The report gives the results and the dog overlap measured in these runs ([section 2.4](../report/d_min_report.md#24-rq4-do-uncoordinated-fat-dogs-reach-a-finite-d_min)).

## Shared calibration (`calibrate_as: strombom_multi`)

The protocol [`dmin_fat.yaml`](../../protocols/configs/protocols/dmin_fat.yaml) sets `calibrate_as: strombom_multi`, and [`dmin_f99_fat.yaml`](../../protocols/configs/protocols/dmin_f99_fat.yaml) inherits it. Calibration therefore measures the settled flock radius $R_f(N)$ with one `strombom_multi` dog, not one FAT dog. FAT and `strombom_multi` then run on the same $R_f(N)$, start flocks, goal radius, drive distance, seeds and 6-drive-time deadline. An animation of the three dog rules on one start flock is in [independent.md](independent.md#shared-calibration-calibrate_as-strombom_multi).

## References

1. Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719, [10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719).
2. Nalepka, P., Kallen, R. W., Chemero, A., Saltzman, E., & Richardson, M. J. (2017). *Herd those sheep: Emergent multiagent coordination and behavioral-mode switching*. Psychological Science, 28(5), 630-650, [10.1177/0956797617692107](https://doi.org/10.1177/0956797617692107).
3. Auletta, F., Fiore, D., Richardson, M. J., & di Bernardo, M. (2022). *Herding stochastic autonomous agents via local control rules and online target selection strategies*. Autonomous Robots, 46, 469-481, [10.1007/s10514-021-10033-6](https://doi.org/10.1007/s10514-021-10033-6).
