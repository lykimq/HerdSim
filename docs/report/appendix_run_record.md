# Run record, claims and reproducibility

Appendix of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## Appendix A: Protocol run record

The study holds 439,120 trials in 41 protocols: 162,420 in the 23 protocols of the first study (Table 1), 236,420 in the 16 follow-up protocols and the resumed 99% main grids, and 40,280 in the two protocols of the Lama and di Bernardo model (Table 2).

Table 1 lists the first pass of each first-study protocol, as `results/queue_log.jsonl` records it. Only the three 99% main grids changed later: they were resumed with finish-time seeds and, at 12 and 6 drive times, four more flock sizes; Table 2 gives their current counts. "Open at 200 seeds" counts the cells still undecided at the cap, on reliability or, in runs that decide finish times, on a finish-time comparison.

**Table 1: Run record of the first-study protocols, first pass.**

| Protocol | Trials | Cells | Decided | Open at 200 seeds | Errors | Hours |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17,220 | 183 | 179 | 4 | 0 | 1.24 |
| `dmin_m6` | 13,470 | 191 | 170 | 21 | 0 | 0.28 |
| `dmin_m3` | 9530 | 183 | 178 | 5 | 0 | 0.17 |
| `dmin_f99_m12` | 11,100 | 180 | 178 | 2 | 0 | 0.41 |
| `dmin_f99_m6` | 12,390 | 180 | 171 | 9 | 0 | 0.49 |
| `dmin_f99_m3` | 10,670 | 181 | 174 | 7 | 0 | 0.27 |
| `dmin_fat` | 8660 | 181 | 179 | 2 | 0 | 0.22 |
| `dmin_f99_fat` | 8670 | 184 | 183 | 1 | 0 | 0.23 |
| `dmin_kubo` | 1080 | 18 | 18 | 0 | 0 | 0.08 |
| Sensitivity protocols (14 runs) | 69,630 | 921 | 800 | 121 | 0 | 3.27 |
| Total | 162,420 | 2402 | 2230 | 172 | 0 | about 6.7 |

Table 2 lists the follow-up runs (99% rule; hours at 20 workers):

**Table 2: Run record of the follow-up protocols.**

| Protocol | Trials | Cells | Open at 200 seeds | Errors | Hours |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`, resumed (current counts; added trials in parentheses) | 31,590 / 31,920 / 11,740 (+20,490 / +19,530 / +1070) | 349 / 354 / 185 | 53 / 58 / 10 | 0 | 4.0 |
| `dmin_f99_indep` | 12,990 | 181 | 18 | 0 | 0.30 |
| `dmin_f99_kubo` | 3260 | 38 | 6 | 0 | 0.18 |
| `dmin_f99_hold` | 14,280 | 280 | 18 | 0 | 0.74 |
| `dmin_f99_hold_spacing` (rerun with the hard spacing rule: a dog whose step would end within 2 m of another does not step) | 13,930 | 283 | 19 | 0 | 0.70 |
| `dmin_f99_hold_goal` (holding, goal 1.9, 2.5, 3.0 $R_f$, $N \le 100$) | 21,800 | 326 | 30 | 0 | 0.36 |
| `dmin_f99_hold_share` (holding, goal 1.9 to 2.5 $R_f$ x share 90, 95, 99%) | 50,170 | 746 | 57 | 0 | 0.91 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10,800 / 10,830 / 10,780 | 180 each | 1 / 0 / 0 | 0 | 0.31 / 0.29 / 0.41 |
| `dmin_f99_k05` | 11,630 | 149 | 14 | 0 | 2.29 |
| `dmin_f99_view_range` | 21,040 | 293 | 27 | 0 | 0.53 |
| `dmin_f99_view_comm` | 6890 | 102 | 3 | 0 | 0.20 |
| `dmin_f99_big` | 2230 | 84 | 1 | 0 | 3.12 |
| `dmin_f99_big_dense`, `_loose` | 1320 / 830 | 15 / 14 | 2 / 1 | 0 | 0.73 / 0.26 |
| `dmin_f99_big_cap` | 2550 (+100 at $N = 3200$, not counted) | 45 | 3 | 0 | 5.5 (7.6 with $N = 3200$) |
| `lama_r50` (gather task, sensing radius 10) | 17,660 | 500 | 23 | 0 | 6.53 |
| `lama_r50_inf` (gather task, infinite sensing) | 22,620 | 500 | 1 | 0 | 6.47 |

Diagnostic replays: 164 pressure replays, 768 `split` replays and 240 holding-walk replays, every unchanged replay identical to its stored trial. Two validation passes of the Lama model (8200 trials, scratch folders not kept) came before `lama_r50`; the second fixed the order in which herders and targets are moved ([section 6](d_min_report.md#6-limitations), item 12).

## Appendix B: Claims and evidence

Table 3 lists each claim with the evidence behind it and its limits.

**Table 3: Claims and evidence.**

| # | Claim | Kind | Evidence | Limits |
| :---: | :--- | :--- | :--- | :--- |
| 1 | A compact flock needs one dog ($D_{\min} = 1$) up to $N = 1131$. | Measured | `dmin_m12`, `dmin_m6`, `dmin_m3`, `dmin_f99_*` up to $N = 566$; `dmin_f99_big_cap` at 800 and 1131. | Above 1056 only with the capped drive point. |
| 2 | Up to $N = 50$ one dog is enough on every layout and deadline. | Measured | All $N \le 50$ cells of the 23 base protocols decided at $D = 1$. | The reason given in [section 3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n) has not been tested. |
| 3 | On scattered flocks $D_{\min}$ grows with slope 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich` at 12 drive times, and 0.38-0.61 and 0.40-0.58 at 6 (99% rule). | Measured | Slope ranges over the brackets of nine flock sizes ($N = 25$-566), `dmin_f99_m12`, `dmin_f99_m6`. | Only up to the calibration edge; `split` is left out. |
| 4 | Under the strict rule large teams fail on the last sheep. | Measured | 97% of strict failures with $D \ge 6$ had 99% of the flock in (`dmin_s_base`); with slower dogs (`dmin_s_dogspeed`) strict $D_{\min}$ on `outlier_rich` $N = 400$ goes from none to 6. | Applies to the strict rule with an open goal. |
| 5 | On `split`, collecting dogs crowd one cluster and many stand still. | Measured in replays | `split_diagnostic` replays: spreading the outliers halves the finish time at $D = 4$; a shorter stop distance makes the drive 21-24% faster at $D = 8$, 16. | 12 seeds per cell; neither change fixes 3 drive times. |
| 6 | Weaker cohesion makes $D_{\min}$ grow faster, toward 0.5. | Measured | `dmin_f99_k05` slope 0.40-0.70 on `wide`; `dmin_f99_c*` 0.20. | One weaker level only; weaker flocks do not calibrate. |
| 7 | Above $N \approx 1056$ Strömbom's drive point is beyond the sheep's reaction distance. | Derived and measured | $2\sqrt{N} > 65$; uncapped, 0 of 10 trials succeed at $N = 1131$ for every $D$; capped, compact succeeds at 800, 1131, 1600 and 42 of 42 at 3200. | Assumes the reaction distance $r_s = 65$ m. |
| 8 | Dogs kept 2 m apart make extra dogs harmful on `outlier_rich` $N = 400$. | Measured | `dmin_f99_hold_spacing`: 186 of 200 at $D = 6$, 54 of 70 at 9, 5 of 10 at 16; every $D \ge 9$ unreliable. | Not seen on `wide` or `compact`. |
| 9 | On `wide` $N = 200$ a local view costs about one dog and sharing with the whole team brings $D_{\min}$ back to its full-sight value; on `split` $N = 200$ a local view of 30 to 65 m does better than full sight. | Measured | `dmin_f99_view_range`, `dmin_f99_view_comm`. | Sharing is instant and error-free in the model. |
| 10 | Near the threshold, an average of 0.99 accepts teams that fail in 9 of 30 runs. | Measured | `lama_r50`: at 144 targets 11 herders average 0.992 but succeed in 21 of 30 runs (99% interval 0.45-0.89); HerdSim's $D_{\min}$ is 17-25. | Targets without cohesion on a disc. |
| 11 | Holding small flocks fails with the default goal; a goal of about 16 to 19 m holds them with one dog. The flock's walk while the dogs withdraw may be the cause. | Thresholds and walk measured; cause consistent, not tested | `dmin_f99_hold_goal`, `dmin_f99_hold_share`: one dog decided reliable on every layout from 18.6 m ($N = 25$) and 17.5 m ($N = 50$) at 99%, with brackets down to 15.5 and 16.0 m. `hold_walk` replays: the flock centre walks a median 17, 15 and 13 m at $N = 25$, 50, 100. | Goal levels in steps of $0.2 R_f$; tied to the withdrawal rule; the walk was not varied directly. |

## Appendix C: Reproducibility

Table 4 lists what is needed to run the study again.

**Table 4: Reproducibility items.**

| Item | Where |
| :--- | :--- |
| Code | Repository `HerdSim`, branch `scaling-cli-d-min-max`. |
| Environment | `uv`, Python 3.11 or later; versions locked in `pyproject.toml` and `uv.lock`. |
| Start layouts | `sim/core/world/layouts.py` (`compact`, `wide`, `split`, `outlier_rich`). |
| Random streams | Cells with the same seed start from the same flock ([paired random streams](../experiments/task_design.md#paired-random-streams)). |
| Hardware | Linux workstation, 20 workers (`--workers 20`). |
| Raw data | 439,120 trial rows in `results/<protocol>/trials.csv`; `trials.jsonl` (in git as `trials.jsonl.gz`) holds the same rows plus the 100 uncounted $N = 3200$ trials of `dmin_f99_big_cap`. One other folder in `results/` is not part of the study: `dmin_pilot`. Two earlier runs were also left out and are no longer in `results/`, only in git history: the first ring run, which put a dog in the goal, and the first spacing run, with a soft spacing rule. |
| Running the study | `uv run cli/campaign.py run --protocol <id>` and `uv run cli/run_queue.py`. |
| Tables | `cli/dmin_tables.py` builds [results_tables.md](results_tables.md) from the result folders. |
| Tests | `make test` runs the unit, invariant and regression tests; `make bench` runs the benchmark tests, six small campaigns end to end. |
| Replays | `services/replay.py`; 1172 diagnostic replays reproduced their stored trials exactly. |
