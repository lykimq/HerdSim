# Coordinated team architecture: `strombom_multi`

`strombom_multi` extends the single-dog collect-or-drive rule of [Strombom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719) to a team of $D$ dogs by assigning each dog its own target at every tick (Figure 1):

- Outlier: any sheep farther than the [collect distance](#when-to-collect) $f(N) = r_a N^{2/3}$ from the flock centre $\mathrm{GCM} = \frac{1}{N}\sum_k \mathbf{x}_k$.
- Collecting (when outliers exist): the $D$ farthest outliers each get one dog at their collect point $P_c$ ([Hungarian assignment](#assigning-outliers-hungarian-algorithm)), and any spare dogs drive the core of the flock.
- Driving (when all sheep lie within $f(N)$): all $D$ dogs spread across an arc of slots centred on the drive point $P_d$ behind the flock ([driving arc](#driving-and-its-limit-for-large-flocks)).
- Single-dog baseline: when $D = 1$, `strombom_multi` reduces identically to Strombom's single-dog rule.

![Collect and drive targets of the team rule with 1, 2, 4 and 8 dogs](../figures/fig3_team_rule.png)

**Figure 1: The team rule `strombom_multi` for $D = 1, 2, 4, 8$ dogs ($N = 200$).** Larger teams collect more outliers in parallel (top) and cover a wider arc behind the flock when driving (bottom).

- Legend: light blue dots are sheep inside $f(N)$ (dashed circle), dark-outlined dots are outliers, orange triangles are dogs, and orange arrows point to each dog's target (`x`).
- Top (`wide` start, collecting): the $D$ farthest outliers are matched to the $D$ dogs at collect points $P_c$.
- Bottom (`compact` start, driving): the $D$ dogs are matched in angular order to slots along the back arc through $P_d$.

## When to collect

At every tick, the team checks the maximum sheep distance from the global centre of mass $\mathrm{GCM}$ against Strombom's collect threshold:

$$
f(N) = r_a N^{2/3}
$$

- Mode switch: if any sheep exceeds $f(N)$ ($43.1$ m at $N = 100$ with $r_a = 2$ m), the team enters `collect` mode; once every sheep is within $f(N)$, the team enters `drive` mode.
- Scaling with $N$: because $f(N) \propto N^{2/3}$ grows faster than the packed flock radius ($\propto \sqrt{N}$), larger flocks tolerate a looser spread before triggering collection.

## Assigning outliers (Hungarian algorithm)

For each outlier $o$ among the $\min(D, n_{\mathrm{outliers}})$ sheep farthest from $\mathrm{GCM}$ (ties broken by sheep index), its collect point $P_c$ sits $r_a = 2$ m behind the outlier along the ray from $\mathrm{GCM}$ (Figure 2, Animation 1):

$$
P_c = \mathbf{x}_o + r_a \frac{\mathbf{x}_o - \mathrm{GCM}}{\lVert \mathbf{x}_o - \mathrm{GCM} \rVert}
$$

- Minimum-distance matching: dogs are paired with collect points by the Hungarian algorithm (`scipy.optimize.linear_sum_assignment` on the Euclidean distance matrix), which minimizes total travel distance and guarantees non-crossing paths in the plane.
- Recomputed every tick: assignments update at every step as sheep and dogs move.
- Spare dogs ($D > n_{\mathrm{outliers}}$): any unassigned dogs drive the core flock (the sheep currently inside $f(N)$) along its driving arc.

![Outliers, the collect point and the dog-to-collect-point assignment](../figures/fig_hungarian_matching.png)

**Figure 2: Outlier collection and Hungarian assignment ($N = 100$, $D = 4$).** Each of the $D$ farthest outliers defines a collect point $P_c$, and the Hungarian algorithm assigns dogs without crossing paths.

- Legend: light blue dots are sheep inside $f(N)$ (dashed circle), dark-outlined dots are outliers, `+` is the $\mathrm{GCM}$, `x` marks are collect points $P_c$, and orange triangles are dogs.
- Left: geometry of $P_c$ on the ray from $\mathrm{GCM}$ through outlier $o$ (offset drawn at $4\,r_a$ for visibility).
- Right: optimal Hungarian assignment (solid orange arrows) compared against a crossing assignment (red dashed lines).

![Animation of the team rule with each dog's target](../gifs/team_rule.gif)

**Animation 1: `strombom_multi` during a 4-dog trial (`outlier_rich`, $N = 200$, $D = 4$, seed 0, 99% rule, 6 drive times).** Dogs collect up to four outliers at a time while spare dogs drive the core, then form a driving arc once all sheep are inside $f(N)$, finishing at 277 s (`dmin_f99_m6`).

- Legend: `x` marks are each dog's true target ($r_a = 2$ m), orange lines connect each dog to its target, the dashed circle is $f(N)$, and the top-right label shows the active mode.

## Driving and its limit for large flocks

When all sheep lie within $f(N)$, the team drives the flock toward $\mathbf{x}_{\mathrm{goal}}$ around Strombom's drive point $P_d$, located $R_{\mathrm{arc}} = r_a\sqrt{N}$ behind $\mathrm{GCM}$ (Figure 3):

$$
P_d = \mathrm{GCM} + r_a \sqrt{N} \frac{\mathrm{GCM} - \mathbf{x}_{\mathrm{goal}}}{\lVert \mathrm{GCM} - \mathbf{x}_{\mathrm{goal}} \rVert}
$$

- Driving arc slots: for $D > 1$, $D$ evenly spaced slots are placed on a circular arc of radius $R_{\mathrm{arc}} = r_a\sqrt{N}$ centred at $\mathrm{GCM}$ with $P_d$ at the midpoint.
- Arc span: the arc spans $\pm \arcsin(\min(1,\, R_{\mathrm{flock}} / R_{\mathrm{arc}}))$ around $P_d$, where $R_{\mathrm{flock}} = \sqrt{2}\,\mathrm{RMS}(\mathbf{x}_k - \mathrm{GCM})$ is the flock's instantaneous radius at that tick, so the outer slots cover the left and right flanks of the flock.
- Angular matching: dogs and arc slots are sorted by signed angle around $\mathrm{GCM}$ (measured from $\mathrm{GCM} \to P_d$) and paired in order, preventing paths from crossing.
- Large-$N$ detection limit: because $R_{\mathrm{arc}} = 2\sqrt{N}$ grows faster than $R_{\mathrm{flock}}$, $R_{\mathrm{arc}}$ exceeds the sheep detection distance $r_s = 65$ m above $N = (65/2)^2 \approx 1056$. All flock sizes in the study ($N \le 566$) stay well below this limit.

![The drive point behind the flock and the arc of drive slots](../figures/fig_driving_arc.png)

**Figure 3: Drive point $P_d$ and driving arc slots ($N = 100$, $D = 4$).** A single dog drives from $P_d$; multiple dogs spread across an arc spanning the flock's width.

- Legend: blue dots are sheep, the shaded blue circle is $R_{\mathrm{flock}}$, `+` is the $\mathrm{GCM}$, `x` marks are $P_d$ or arc slots, the green curve is the driving arc, and orange triangles are dogs.
- Left: $P_d$ sits $r_a\sqrt{N} = 20$ m behind $\mathrm{GCM}$ on the line away from $\mathbf{x}_{\mathrm{goal}}$.
- Right: 4 arc slots spanning $\pm \arcsin(R_{\mathrm{flock}} / R_{\mathrm{arc}})$, paired with the 4 dogs in angular order.

## Dog speed, step and stop rule

Every dog has full knowledge of all sheep positions and updates its position at each tick ($\Delta t = 1$ s) after the sheep have moved:

- Stop rule: if any sheep is closer than $3\,r_a = 6$ m to a dog, that dog stands still ($\mathbf{v}_d = \mathbf{0}$) for that tick.
- Step with angular noise: otherwise, the dog adds a random unit vector $\boldsymbol{\epsilon}_d$ (weighted by $e = 0.3$, drawn from the dog RNG stream) to the unit vector toward its target $\mathbf{T}_d$ and moves at $v_{\mathrm{dog}} = 1.5$ m/s ($1.5\times$ the sheep speed):

$$
\mathbf{v}_d = v_{\mathrm{dog}} \frac{\widehat{\mathbf{T}_d - \mathbf{x}_d} + e\,\boldsymbol{\epsilon}_d}{\left\lVert \widehat{\mathbf{T}_d - \mathbf{x}_d} + e\,\boldsymbol{\epsilon}_d \right\rVert}
$$

## References

- Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
