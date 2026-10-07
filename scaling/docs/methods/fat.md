# FAT: farthest-agent targeting

## Published inspiration

FAT is inspired by the local-camera shepherding rule discussed by Tsunoda et al. (2018): act on the farthest agent in the herder's visible set without requiring global flock coordinates.

HerdSim does not implement that paper's complete camera model, positional-error treatment, sheep dynamics, navigation law, or experimental calibration. The published contribution is therefore inspiration for target selection, not a claim of full model reproduction.

Reference: Y. Tsunoda et al., "Analysis of local-camera-based shepherding navigation," Advanced Robotics 32(23), 2018. DOI: `10.1080/01691864.2018.1539410`.

![FAT farthest-from-dog targeting.](../../results/summary/figures/schematics/en/alg_fat.svg)

## Exact HerdSim implementation

The `fat` method bundle combines:

- `sheep_model=strombom`;
- `dog_controller=fat`;
- two dogs by default outside experiment overrides.

Sheep therefore use HerdSim's Strombom grazing, flocking, repulsion, and fixed-displacement update. The dog controller has no Collect/Drive switch and no flock-cohesion test.

For each active dog on each tick:

1. Read that dog's observation after observation-mode and sensing filters.
2. If no sheep are visible, leave the dog stationary.
3. Choose the observed sheep farthest from the dog itself.
4. Place a target `r_a` behind that sheep on the ray from the goal through the sheep.
5. Move toward that target at `shepherd_speed`, with Strombom angular noise.
6. Stop if any sheep in the dog's working view is closer than `shepherd_stop_multiple * r_a`.

Each dog makes this choice independently. FAT has no dog-dog repulsion, assignment negotiation, or explicit spacing. "Farthest" means farthest from the dog, which differs from Strombom Collect (farthest from the flock center) and Kubo (farthest from the goal).

Implementation evidence:

- [`../../../core/methods.py`](../../../core/methods.py)
- [`../../../plugins/dogs/fat.py`](../../../plugins/dogs/fat.py)
- [`../../../plugins/sheep/strombom.py`](../../../plugins/sheep/strombom.py)
- [`../../../methods/strombom/heuristics.py`](../../../methods/strombom/heuristics.py)
- [`../../../methods/strombom/config.py`](../../../methods/strombom/config.py)

## `scaling_v2` setup

FAT is a Phase 4 transfer method on the same task and grids as Kubo and the baseline.

- Size map: compact layout on the full size and dog grids.
- Structure map: four layouts at `N = {50, 100, 200}`.
- Observation mode: global.
- Communication: no coordination is added by the FAT controller.
- Deadline: `T0 = 10000`.
- Reliability threshold: `R >= 0.90`.
- Staging: 30 scout seeds, then 100 claim seeds in selected windows.

The global observation setting is important. Although the target-selection idea is motivated by local sensing, completed Phases 1, 2, and 4 gave each FAT dog the full flock view. Those results do not test the local-camera information limit. Observation-mode experiments were planned for Phase 5 but were not run.

Configuration evidence:

- [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml)
- [`../../configs/protocols/phase4_fat_size_claim.yaml`](../../configs/protocols/phase4_fat_size_claim.yaml)
- [`../../configs/protocols/phase4_fat_structure_claim.yaml`](../../configs/protocols/phase4_fat_structure_claim.yaml)

## Observed completed results

### Compact size map

- `D_min = 1` at `N = 5` and `N = 10`.
- For every tested `N >= 25`, no dog count through 35 reached `R >= 0.90`.
- The latter cells are hard failures: `D_min` and `D_max` are undefined, not zero and not 35.
- Best reliability by size for `N = 50` through 400 was about 0.40 to 0.53.
- About half of FAT size trials failed. The summary attributes about 39% of all trials to oscillation failures and 7% to stuck failures.

![Three-method compact reliability heatmaps.](../../results/phase4/guides/assets/figures/f1_reliability_heatmaps.png)

*R(N, D) surfaces on compact starts. FAT clears the threshold only at N = 5 and 10; from N = 25 upward no cell reaches 0.90.*

![Failure-mode comparison.](../../results/summary/figures/f6_failure_modes.png)

*FAT failures are mostly oscillation or stuck, unlike Kubo (timeout) and baseline (far fewer failures).*

### Starting structure

FAT did not reach 90% reliability in any structure cell at `N = 50, 100, 200`.

- Compact best `R`: 0.47, 0.40, 0.47 for `N = 50, 100, 200`.
- Split best `R`: 0.50, 0.47, 0.40.
- `outlier_rich` best `R`: 0.10, 0.00, 0.00.
- Wide best `R`: 0.00 at all three sizes.

![Reliability curves by starting layout.](../../results/summary/figures/f5_layout_reliability_curves.png)

*R against D at N = 200. FAT never reaches 0.90 on any tested layout.*

The completed summary also reports a strong negative association between FAT trial interference and success on the size merge, with Pearson `r` about `-0.87`. This is observational. It does not establish interference as the cause of failure.

![Directional interference by dog count.](../../results/summary/figures/f7_interference.png)

*Interference index against D. The negative association with FAT success is observational on the size merge, not a controlled causal test.*

Evidence:

- [`../../results/phase4/fat_size/claim/packages/a/frontier.csv`](../../results/phase4/fat_size/claim/packages/a/frontier.csv)
- [`../../results/phase4/fat_size/claim/merged_trials.csv`](../../results/phase4/fat_size/claim/merged_trials.csv)
- [`../../results/phase4/fat_structure/claim/merged_trials.csv`](../../results/phase4/fat_structure/claim/merged_trials.csv)
- [`../../results/phase4/package_d/structure/frontier_by_method_layout.csv`](../../results/phase4/package_d/structure/frontier_by_method_layout.csv)

## Limitations and non-claims

- This is a minimal HerdSim FAT controller on Strombom sheep, not the full Tsunoda et al. model.
- The completed results use global observations. They do not measure camera occlusion, bearing-only control, position error, or lost-track recovery.
- Hard failure means no tested count reached the study's 90% bar before `T0`. It does not prove FAT can never work at larger `D`, under another timeout, or on another task.
- Increasing dog count did not rescue larger flocks on this grid. That observation does not isolate a causal mechanism.
- The interference correlation is not a controlled causal test.
- FAT has no registered NetLogo twin. Registry: [`../../../integrations/netlogo/twins.json`](../../../integrations/netlogo/twins.json).
- Results do not establish field performance or reproduce the quantitative results of the 2018 paper.
