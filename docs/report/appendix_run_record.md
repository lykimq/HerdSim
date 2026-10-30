# Run record, claims and reproducibility

Appendix of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

## Appendix A: Protocol run record

The study holds 439,120 trials in 41 protocols. A protocol is one experiment plan, and a trial is one run of one cell with one seed ([glossary](../glossary.md#trials-and-experiments)). The trials fall into three groups:

- First study: 162,420 trials in 23 protocols, the [main runs](../glossary.md#trials-and-experiments), the [sensitivity runs](../glossary.md#trials-and-experiments), `dmin_fat`, `dmin_f99_fat` and `dmin_kubo` (Table 1).
- Drive-task follow-up: 236,420 trials, 195,330 in 16 new drive-task protocols and 41,090 added to the three 99% main grids when they were resumed (Table 2).
- Gather-task follow-up: 40,280 trials in the two protocols of the Lama and di Bernardo model (Table 2).

The follow-up runs are the 18 protocols added after the first study, 16 on the drive task and 2 on the gather task, together with the resumed 99% main grids. The first two groups together are the 398,840 trials of the 39 drive-task protocols.

Table 1 gives the trials and cells each first-study folder holds now, as its `results/<protocol>/status.json` records them, with one exception: the three 99% main grids, `dmin_f99_m12`, `dmin_f99_m6` and `dmin_f99_m3`. Table 1 shows them at their first queue pass, the line `results/queue_log.jsonl` records for each. They were later resumed with finish-time seeds and, at 12 and 6 [drive times](../glossary.md#the-drive-task), four more flock sizes. Table 2 gives their current counts and the trials added.

Fourteen other first-study folders also grew in later [sittings](../glossary.md#trials-and-experiments), so Table 1 shows more trials and cells for them than the queue log does: `dmin_m6`, `dmin_m3`, `dmin_fat`, `dmin_f99_fat`, `dmin_s_base`, `dmin_s_matched`, `dmin_s_handler`, `dmin_s_ring`, `dmin_s_goal`, `dmin_s_gap`, `dmin_f99_s_matched`, `dmin_f99_s_handler`, `dmin_f99_s_goal` and `dmin_f99_s_gap`. For example, the log records 11,625 trials on 180 cells for `dmin_m6`, and the folder now holds 13,470 on 191. Their trials are counted in Table 1 and nowhere else.

The hours in Table 1 are those of the run the queue log records and leave out the later sittings.
"Open at 200 seeds" counts the cells still undecided at the [seed cap](../glossary.md#trials-and-experiments) of 200, on reliability or, in a sitting that decides finish times, on a finish-time comparison ([open cell](../glossary.md#success-and-reliability)). Apart from the three first-pass rows, each row gives the count that the folder's last sitting wrote, with that sitting's settings. [Pruned cells](../experiments/task_design.md#pruning-above-saturation) and cells with an error are never counted open. "Decided" is the cells minus those open at 200 seeds, so it also counts the pruned cells: 4 in each main-grid row and in `dmin_f99_fat`, and 5 in `dmin_fat`. Two of the 5 in `dmin_fat` are still undecided on reliability, compact $N = 200$ at $D = 12$ with 140 seeds and at $D = 24$ with 110.

In `dmin_m12` this changes the count. Its first pass decided finish times, and the queue log records 36 open cells. A sitting on 2026-10-22 added no trials and rewrote `status.json` under the folder's frozen protocol file, which does not set `decide_finish_times`. It counted only the 4 cells still undecided on reliability, and Table 1 gives that count. Counted the first pass's way, the row would be 147 decided and 36 open, and the totals 2198 decided and 204 open.

**Table 1: Run record of the first-study protocols.**

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

Table 2 lists the follow-up runs of three kinds: the resumed 99% main grids, the 16 drive-task follow-up protocols and the two gather-task protocols. The drive-task runs use the [99% rule](../glossary.md#success-and-reliability) unless the row says otherwise, and the hours are at 20 workers.
The hours come from different records, row by row:

- Resumed grids: the trials were added over several sittings, and the current `status.json` gives the hours of the last one only (2.365, 1.573 and 0.017 h, 3.955 h in total). The status files kept in git history add a sitting on 2026-10-22 for `dmin_f99_m6` (1850 trials, 0.28 h) and one for `dmin_f99_m3` (470 trials, 0.05 h). With them the sittings account for every added trial and took 4.285 h in the recorded sittings, and sittings never committed to git may add more.
- `dmin_f99_big_cap`: it has no line in the queue log, so its row comes from its `status.json` (5.475 h). No stored record gives the hours of its 100 trials at $N = 3200$. The folder's span from creation to its last status update is 7.6 h, and that span also includes calibration and any idle time.
- Every other row: the hours are those of the queue log. `status.json` can differ in the third decimal, for example 0.284 h against the log's 0.285 h for `dmin_f99_c1.6`, and 0.171 h against 0.175 h for `dmin_f99_kubo`.

**Table 2: Run record of the follow-up runs.**

| Protocol | Trials | Cells | Open at 200 seeds | Errors | Hours |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`, resumed (current counts; added trials in parentheses) | 31,590 / 31,920 / 11,740 (+20,490 / +19,530 / +1070) | 349 / 354 / 185 | 53 / 58 / 10 | 0 | 4.285 in the recorded sittings, and sittings never committed to git may add more |
| `dmin_f99_indep` | 12,990 | 181 | 18 | 0 | 0.30 |
| `dmin_f99_kubo` | 3260 | 38 | 6 | 0 | 0.18 |
| `dmin_f99_hold` | 14,280 | 280 | 18 | 0 | 0.74 |
| `dmin_f99_hold_spacing` (rerun with the hard spacing rule: a dog already within 2 m of another walks straight away from the dogs crowding it at the dog speed, and a dog whose step would end within 2 m of another does not step) | 13,930 | 283 | 19 | 0 | 0.70 |
| `dmin_f99_hold_goal` (holding, goal 1.9, 2.5, 3.0 $R_f$, $N \le 100$) | 21,800 | 326 | 30 | 0 | 0.36 |
| `dmin_f99_hold_share` (holding, goal 1.9 to 2.5 $R_f$ x share 90, 95, 99%) | 50,170 | 746 | 57 | 0 | 0.91 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10,800 / 10,830 / 10,780 | 180 each | 1 / 0 / 0 | 0 | 0.31 / 0.29 / 0.41 |
| `dmin_f99_k05` | 11,630 | 149 | 14 | 0 | 2.29 |
| `dmin_f99_view_range` | 21,040 | 293 | 27 | 0 | 0.53 |
| `dmin_f99_view_comm` | 6890 | 102 | 3 | 0 | 0.20 |
| `dmin_f99_big` | 2230 | 84 | 1 | 0 | 3.12 |
| `dmin_f99_big_dense`, `_loose` | 1320 / 830 | 15 / 14 | 2 / 1 | 0 | 0.73 / 0.26 |
| `dmin_f99_big_cap` | 2550 (+100 at $N = 3200$, not counted) | 45 | 3 | 0 | 5.5 |
| `lama_r50` (gather task, sensing radius 10) | 17,660 | 500 | 23 | 0 | 6.53 |
| `lama_r50_inf` (gather task, infinite sensing) | 22,620 | 500 | 1 | 0 | 6.47 |

Across the 41 protocols the folders now hold 6,845 cells, and 499 of them are open at 200 seeds. These totals follow from the two tables once the three 99% main grids are counted only once, at their current counts in Table 2. Tables 1 and 2 add up to 7,386 cells and 517 open, and the first-pass rows of those grids in Table 1 hold 541 cells and 18 open. The 499 uses each folder's last-sitting count, so `dmin_m12` adds 4.

The diagnostic tools [replayed](../glossary.md#trials-and-experiments) 1172 stored trials: 164 pressure replays, 768 `split` replays and 240 holding-walk replays. 596 of them ran the trial unchanged: the 164 pressure replays, the 192 base `split` replays and the 240 holding-walk replays. Each unchanged replay is checked against its stored success and tick count, and the tools stop on a mismatch; all three wrote every row. The other 576 `split` replays ran changed versions of the team rule (192 each with the collecting dogs spread over the clusters, with the shorter stop distance, and with both), so they have no stored trial to match. Before `lama_r50`, two validation passes of the Lama model ran 8200 trials in scratch folders that were not kept. The second pass fixed the order in which herders and targets are moved ([section 6](d_min_report.md#6-limitations), item 12).

## Appendix B: Claims and evidence

Table 3 lists each claim with the evidence behind it and its limits. The [glossary](../glossary.md) defines the terms it uses: the [layouts](../glossary.md#start-layouts-and-dog-starts) `compact`, `wide`, `split` and `outlier_rich`, the [strict and 99% rules](../glossary.md#success-and-reliability), and [$D_{\min}$ and its brackets](../glossary.md#team-sizes).

**Table 3: Claims and evidence.**

| # | Claim | Kind | Evidence | Limits |
| :---: | :--- | :--- | :--- | :--- |
| 1 | A compact flock needs one dog ($D_{\min} = 1$) up to $N = 1131$. | Measured | The team rule in the main grids `dmin_m12`, `dmin_m6`, `dmin_m3` and `dmin_f99_m3` up to $N = 400$, and `dmin_f99_m12` and `dmin_f99_m6` up to $N = 566$; `dmin_f99_big_cap` at 800 and 1131. | Team rule on the drive task only: with FAT, `dmin_f99_fat` has no reliable team on compact $N = 400$ (lower bound [12]), and the holding runs have none on compact $N = 25$ and 50. Above 1056 only with the capped drive point. |
| 2 | Up to $N = 50$ one dog is enough on every layout and deadline. | Measured | All $N \le 50$ cells of the 23 base protocols decided at $D = 1$. | The reason given in [section 3.1](part1_growth.md#31-rq1-how-does-d_min-grow-with-n) has not been tested. |
| 3 | On scattered flocks $D_{\min}$ grows with slope 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich` at 12 drive times, and 0.38-0.61 and 0.40-0.58 at 6 (99% rule). | Measured | Slope ranges over the brackets of nine flock sizes ($N = 25$-566), `dmin_f99_m12`, `dmin_f99_m6`. | Only up to the calibration edge; `split` is left out. |
| 4 | Under the strict rule large teams fail on the last sheep. | Measured | 97% of strict failures with $D \ge 6$ had 99% of the flock in (`dmin_s_base`); with slower dogs (`dmin_s_dogspeed`) strict $D_{\min}$ on `outlier_rich` $N = 400$ goes from none to 6. | Applies to the strict rule with an open goal. |
| 5 | On `split` $N = 200$ at 6 drive times, collecting dogs crowd one cluster and many stand still. | Measured in replays | `split_diagnostic` replays, 99% rule: spreading the collecting dogs over the outliers halves the median finish time at $D = 4$ (631 s to 317.5 s); a shorter stop distance makes the drive 21-24% faster at $D = 8$ and 16 (678.5 s to 536 s, 724 s to 550.5 s). The medians are over successful replays only; at $D = 4$, 11 of 12 base and 10 of 12 spread replays succeeded. | 12 seeds per cell. At $N = 100$ the medians move by at most 10 s. At 3 drive times neither change makes `split` reliable. |
| 6 | Weaker cohesion makes $D_{\min}$ grow faster on `wide`, toward 0.5. | Measured | 99% rule, 12 drive times, `wide`: `dmin_f99_k05` slope 0.40-0.70, `dmin_f99_c*` 0.20. On `outlier_rich` `dmin_f99_k05` gives 0.30, the same as with Strömbom's cohesion. | One weaker level only ($n = 0.5N$). `dmin_f99_k05` is fitted on four sizes ($N = 50$-400) and `dmin_f99_c*` on five (25-400). Its first start failed calibration at $N = 25$ (radius still changing); no stored run tests weaker levels. |
| 7 | Above $N \approx 1056$ Strömbom's drive point is beyond the sheep's reaction distance. | Derived and measured | $2\sqrt{N} > 65$; uncapped, 0 of 10 trials succeed at $N = 1131$ for every $D$; capped, compact succeeds at 800, 1131 and 1600, and in 42 of 42 trials at 3200 (teams of 3 to 12 dogs). | Assumes the reaction distance $r_s = 65$ m. The 3200 result is partial: the 42 trials are among the 100 $N = 3200$ trials of a run stopped early, which are not counted in the totals. |
| 8 | Dogs kept 2 m apart make extra dogs harmful on `outlier_rich` $N = 400$. | Measured | `dmin_f99_hold_spacing`: 186 of 200 at $D = 6$, 54 of 70 at 9, 5 of 10 at 16; every $D \ge 9$ unreliable. | Not seen on `wide` or `compact`. |
| 9 | On `wide` $N = 200$ a sensing range of 30 to 65 m costs about one dog, and at 65 m sharing with the whole team brings $D_{\min}$ back to its full-sight value; on `split` $N = 200$ a range of 30 to 65 m does better than full sight. | Measured | 99% rule, 6 drive times. `dmin_f99_view_range` on `wide` $N = 200$: $D_{\min}$ 2 with full sight, 3 at 30 and 65 m, 3-4 at 45 m, 2-3 at 100 m, and no reliable team at 15 m (lower bound [7]). `dmin_f99_view_comm`: 2 with sharing at 65 m. | Sharing tested at 65 m only. Sharing is instant and error-free in the model. |
| 10 | Near the threshold, an average of 0.99 accepts teams that fail in 9 of 30 runs. | Measured | `lama_r50`: at 144 targets 11 herders average 0.992 but succeed in 21 of 30 runs (99% interval 0.45-0.89); HerdSim's $D_{\min}$ is 17-25. | Targets without cohesion on a disc. |
| 11 | Holding small flocks fails with the default goal; a goal of about 16 to 19 m holds them with one dog. This may be because the flock walks while the dogs withdraw; we have not tested it. | Thresholds and walk measured; cause consistent, not tested | `dmin_f99_hold_goal`, `dmin_f99_hold_share`: one dog decided reliable on every layout from 18.6 m ($N = 25$) and 17.5 m ($N = 50$) at 99%, with brackets down to 15.5 and 16.0 m. `hold_walk` replays: the flock centre walks a median 17, 15 and 13 m at $N = 25$, 50, 100. | Goal levels in steps of $0.2 R_f$; tied to the withdrawal rule; the walk was not varied directly. |

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
| Raw data | 439,120 trial rows in `results/<protocol>/trials.csv`; `trials.jsonl` (in git as `trials.jsonl.gz`) holds the same rows plus the 100 uncounted $N = 3200$ trials of `dmin_f99_big_cap`. `dmin_pilot`, the one other protocol folder in `results/`, is not part of the study; `results/diagnostics/` holds the CSVs of the three replay tools. Two earlier runs were also left out and are kept only in git history, no longer in `results/`. They are the first ring run, which put a dog in the goal, and the first spacing run, which used a soft spacing rule. The first `dmin_f99_k05` start stopped at calibration and has no trials. |
| Running the study | `uv run cli/campaign.py run --protocol <id>` and `uv run cli/run_queue.py`. |
| Tables | `docs/generate_docs/make_docs.py` writes [results_tables.md](results_tables.md) from the result folders, with the same verbs as `cli/dmin_tables.py`. |
| Tests | `make test` runs the unit, invariant and regression tests; `make bench` runs the benchmark tests, six small campaigns end to end. |
| Replays | `services/replay.py`; of the 1172 diagnostic replays, the 596 unchanged ones reproduced the success and tick count of their stored trials. |
