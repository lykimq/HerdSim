# Kubo force-based herding

## Published inspiration

Kubo et al. (2022) model sheep and multiple dogs through continuous force sums rather than a discrete Collect/Drive switch. Sheep combine neighbor repulsion, velocity alignment, cohesion, and dog repulsion. Each dog targets an in-range sheep farthest from the goal, while target repulsion, goal repulsion, and dog-dog repulsion shape its motion. Dog-dog repulsion can spread the team behind the flock.

Reference: M. Kubo, M. Tashiro, H. Sato, et al., "Herd guidance by multiple sheepdog agents with repulsive force," Artificial Life and Robotics 27, 416-427, 2022. DOI: `10.1007/s10015-021-00726-7`.

## Exact HerdSim implementation

The `kubo` method bundle combines:

- `sheep_model=kubo`;
- `dog_controller=kubo_forces`;
- default counts of 40 sheep and 4 dogs outside experiment overrides.

It does not use Strombom sheep and has no Collect/Drive state.

### Sheep force step

For each sheep, HerdSim finds sheep and dogs within `radius = 60`. It computes:

- mean inverse-square sheep repulsion;
- mean unit velocity of moving neighbors;
- mean unit attraction toward neighboring sheep;
- mean inverse-cube repulsion from dogs.

The weighted velocity uses `K_s1..K_s4 = 10, 0.5, 2, 5000`. Its magnitude is clamped to `sheep_speed_max = 5`, and position advances by `dt * velocity` with `dt = 0.05`.

### Dog force step

For each active dog with a nonempty observation:

1. Build the observation-limited local state.
2. Keep sheep inside `radius`.
3. Select the in-range sheep farthest from the goal.
4. Combine attraction to that target, inverse-cube repulsion from it, repulsion from the goal, and inverse-cube repulsion from other in-range dogs.
5. Weight the terms with `K_f1..K_f4 = 10, 200, 8, 3000`.
6. Clamp speed to `dog_speed_max = 10` and advance by `dt * velocity`.

If the observation contains no sheep, the controller leaves that dog stationary for the tick. Sheep update before dogs in the simulation step. HerdSim also applies its scenario goal, bounded arena behavior, per-agent response and cohesion factors, and observation pipeline around these forces.

Implementation evidence:

- [`../../../core/methods.py`](../../../core/methods.py)
- [`../../../methods/kubo/config.py`](../../../methods/kubo/config.py)
- [`../../../methods/kubo/forces.py`](../../../methods/kubo/forces.py)
- [`../../../plugins/sheep/kubo.py`](../../../plugins/sheep/kubo.py)
- [`../../../plugins/dogs/kubo_forces.py`](../../../plugins/dogs/kubo_forces.py)

## `scaling_v2` setup

Kubo is a Phase 4 transfer method, compared with the `strombom_multi` baseline without changing the shared task geometry.

- Size map: compact layout on the full `N` and `D` grids.
- Structure map: four layouts at `N = {50, 100, 200}`.
- Observation mode: global.
- Deadline: `T0 = 10000`.
- Reliability threshold: `R >= 0.90`.
- Staging: 30 scout seeds, then 100 claim seeds in selected windows.
- Additional precision: `outlier_rich`, `N = 200`, `D` in `{1, 2, 3, 4, 6, 10, 15, 20, 25}` was raised to 200 seeds. `D = 35` remained at 30 scout seeds.

The experiment overrides the preset counts with each tested `(N, D)` cell. It does not retune Kubo's force gains for each flock size or layout.

Configuration evidence:

- [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml)
- [`../../configs/protocols/phase4_kubo_size_claim.yaml`](../../configs/protocols/phase4_kubo_size_claim.yaml)
- [`../../configs/protocols/phase4_kubo_structure_claim.yaml`](../../configs/protocols/phase4_kubo_structure_claim.yaml)

## Observed completed results

### Compact size map

- `D_min = 3` at `N = 5`.
- `D_min = 1` at every tested size from `N = 10` through 400.
- `D_max = 35` is the grid ceiling in every size cell.
- No overcrowding was observed.
- Overall success in the Kubo size merge was 0.991, and all recorded failures were timeouts.

Kubo therefore shared the baseline compact frontier for `N >= 25`, but not every small-flock result.

### Starting structure

- Compact and split: `D_min = 1` at `N = 50, 100, 200`.
- `outlier_rich`: `D_min = 1` at `N = 50, 100`.
- `outlier_rich`, `N = 200`: point estimate `D_min = 20`.
- Wide: hard failure at all three sizes. The best reliability over tested dog counts was about 0.47 to 0.54, below 0.90.

For `outlier_rich`, `N = 200`, the 200-seed cells gave `R = 0.935` at `D = 20` and `R = 0.910` at `D = 25`. The bootstrap interval for `D_min` was `[2, 20]` because several lower dog counts lay near the threshold. The point estimate should always be reported with that wide interval.

Evidence:

- [`../../results/phase4/kubo_size/claim/packages/a/frontier.csv`](../../results/phase4/kubo_size/claim/packages/a/frontier.csv)
- [`../../results/phase4/kubo_structure/claim/packages/b/frontier_by_layout.csv`](../../results/phase4/kubo_structure/claim/packages/b/frontier_by_layout.csv)
- [`../../results/phase4/kubo_structure/claim/merged_dmin_bootstrap.csv`](../../results/phase4/kubo_structure/claim/merged_dmin_bootstrap.csv)
- [`../../results/phase4/kubo_structure/claim/outlier_rich_n200_window.json`](../../results/phase4/kubo_structure/claim/outlier_rich_n200_window.json)
- [`../../results/phase4/package_d/structure/frontier_by_method_layout.csv`](../../results/phase4/package_d/structure/frontier_by_method_layout.csv)

## Relevant existing figures

- [Three-method compact reliability heatmaps](../../results/phase4/guides/assets/figures/f1_reliability_heatmaps.png)
- [Reliability curves by starting layout](../../results/phase4/guides/assets/figures/f5_layout_reliability_curves.png)
- [Failure-mode comparison](../../results/phase4/guides/assets/figures/f6_failure_modes.png)
- [Kubo `outlier_rich`, `N = 200`](../../results/phase4/guides/assets/figures/f9_kubo_outlier_rich_n200.png)

## Limitations and non-claims

- Shared compact `D_min` does not imply full transfer. Kubo failed the 90% criterion on every wide cell and shifted sharply at `outlier_rich`, `N = 200`.
- The `[2, 20]` bootstrap interval makes the `D_min = 20` boundary uncertain on its lower side.
- Hard failure on wide means no tested `D <= 35` reached the reliability threshold. It is not evidence that more dogs always make Kubo worse.
- Kubo ticks are not physically comparable with Strombom-family ticks because Kubo uses `dt` integration.
- HerdSim's bounded arena, spawn geometry, goal disk, and experiment counts are study choices, not claims about the paper's exact setup.
- A Kubo NetLogo twin is registered, but the completed scaling report does not provide a quantitative parity result. Registry: [`../../../integrations/netlogo/twins.json`](../../../integrations/netlogo/twins.json).
- The results do not reproduce the paper's numerical tables and do not establish performance outside this simulated task.
