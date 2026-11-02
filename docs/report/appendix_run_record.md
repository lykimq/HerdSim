# Run record, claims and reproducibility

Reference for the stored runs of the study: the fields of a run record, one record per protocol, one entry per claim, and what is needed to run the study again. Every entry is self-contained and uses the protocol ids that name the folders in `results/`.

## Contents

- [Appendix A: Protocol run record](#appendix-a-protocol-run-record)
- [Appendix B: Claims and evidence](#appendix-b-claims-and-evidence)
- [Appendix C: Reproducibility](#appendix-c-reproducibility)

## Appendix A: Protocol run record

### Fields

Table 1 defines the fields used in the records below.

**Table 1: Fields of a protocol record.**

| Field | Meaning |
| :--- | :--- |
| Protocol | Id of one experiment plan; its results are in `results/<id>/` |
| Trial | One simulation run of one cell with one seed |
| Cell | One setup (flock size, layout, deadline, rule) with the question "is a team of $D$ dogs reliable here?" |
| Decided | A cell that is not open, including pruned cells: cells above a confirmed $D_{\mathrm{sat}}$ that the campaign does not run |
| Open | A cell still undecided at the seed cap of 200, on reliability or, in a sitting that decides finish times, on a finish-time comparison |
| Errors | Trials that ended in a simulation error; cells with an error are never open |
| Sitting | One run of the campaign command on a results folder |
| Hours | Wall-clock hours at 20 workers, from the queue log `results/queue_log.jsonl`, one line per finished protocol run |

A record reads `Record: <trials> trials, <cells> cells (<decided> decided, <open> open), <errors> errors, <hours> h`; the follow-up records omit the decided count.

### Totals

Table 2 counts the protocols and trials of the study; none had a simulation error.

**Table 2: Protocols and trials of the study.**

| Part of the study | Protocols | Trials |
| :--- | :---: | :---: |
| First study (drive task) | 23 | 162,420 |
| Follow-up, drive task | 16 new, 3 resumed | 236,420 |
| Follow-up, gather task of Lama and di Bernardo (2024) | 2 | 40,280 |
| Total | 41 | 439,120 |

- The 3 resumed runs are first-study protocols, so the total is 23 + 16 + 2 = 41.
- Eleven first-study protocols use the 99% rule, under which a team is reliable when its success is shown at 99% confidence.
- The follow-up's drive-task trials are 195,330 in 16 new protocols (four of them on the holding task) and 41,090 added to the three 99% main runs when resumed. The 39 drive-task protocols hold 398,840.
- The drive task is a drive of the flock to a goal by the dogs; the holding task is to keep the flock inside the goal; the gather task is the one of Lama and di Bernardo (2024).

### First-study protocols

Each entry gives the record of one protocol, with its decided and open cells.

#### `dmin_m12`

- Record: 17,220 trials, 183 cells (179 decided, 4 open), 0 errors, 1.24 h

#### `dmin_m6`

- Record: 13,470 trials, 191 cells (170 decided, 21 open), 0 errors, 0.28 h

#### `dmin_m3`

- Record: 9530 trials, 183 cells (178 decided, 5 open), 0 errors, 0.17 h

#### `dmin_f99_m12`

- Record: 11,100 trials, 180 cells (178 decided, 2 open), 0 errors, 0.41 h
- Note: first pass; the resumed run is in the follow-up protocols

#### `dmin_f99_m6`

- Record: 12,390 trials, 180 cells (171 decided, 9 open), 0 errors, 0.49 h
- Note: first pass; the resumed run is in the follow-up protocols

#### `dmin_f99_m3`

- Record: 10,670 trials, 181 cells (174 decided, 7 open), 0 errors, 0.27 h
- Note: first pass; the resumed run is in the follow-up protocols

#### `dmin_fat`

- Record: 8660 trials, 181 cells (179 decided, 2 open), 0 errors, 0.22 h

#### `dmin_f99_fat`

- Record: 8670 trials, 184 cells (183 decided, 1 open), 0 errors, 0.23 h

#### `dmin_kubo`

- Record: 1080 trials, 18 cells (18 decided, 0 open), 0 errors, 0.08 h

#### Sensitivity protocols (14 runs)

- Record: 69,630 trials, 921 cells (800 decided, 121 open), 0 errors, 3.27 h

#### First-study total

- Record: 162,420 trials, 2402 cells (2230 decided, 172 open), 0 errors, about 6.7 h

Notes on the first-study records:

- Counts are each folder's current state, except the three 99% main runs (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`), shown at their first pass as the queue log records it; the follow-up records give them after the top-up, the resumed run that adds trials.
- Fourteen other first-study folders (`dmin_m6`, `dmin_m3`, `dmin_fat`, `dmin_f99_fat` and ten sensitivity runs) hold more trials than their last log line, added in later sittings and counted here only.
- Pruned cells in Decided: 4 in each main-run record and in `dmin_f99_fat`, 5 in `dmin_fat`.

### Follow-up protocols

Each entry gives the research question (RQ) the protocol answers, its setting where it differs from the base run, and its record. All use the 99% rule unless the entry says otherwise.

#### `dmin_f99_m12`, resumed

- Question: RQ4, RQ7, RQ8, finish times at nine sizes
- Record: 31,590 trials (20,490 added by the resumption), 349 cells (53 open), 0 errors, hours not recorded per sitting

#### `dmin_f99_m6`, resumed

- Question: RQ4, RQ7, RQ8, finish times at nine sizes
- Record: 31,920 trials (19,530 added by the resumption), 354 cells (58 open), 0 errors, hours not recorded per sitting

#### `dmin_f99_m3`, resumed

- Question: RQ4, RQ7, finish times
- Record: 11,740 trials (1070 added by the resumption), 185 cells (10 open), 0 errors, hours not recorded per sitting

#### `dmin_f99_indep`

- Question: RQ9, dogs without a team layer
- Record: 12,990 trials, 181 cells (18 open), 0 errors, 0.30 h

#### `dmin_f99_kubo`

- Question: RQ9, $D_{\mathrm{sat}}$ of Kubo's model
- Record: 3260 trials, 38 cells (6 open), 0 errors, 0.18 h

#### `dmin_f99_hold`

- Question: RQ10, holding while dogs withdraw
- Record: 14,280 trials, 280 cells (18 open), 0 errors, 0.74 h

#### `dmin_f99_hold_spacing`

- Question: RQ10, dogs that take up room
- Setting: rerun with the hard 2 m spacing rule
- Record: 13,930 trials, 283 cells (19 open), 0 errors, 0.70 h

#### `dmin_f99_hold_goal`

- Question: RQ10, holding small flocks
- Setting: goal 1.9, 2.5 and 3.0 $R_f$, $N \le 100$
- Record: 21,800 trials, 326 cells (30 open), 0 errors, 0.36 h

#### `dmin_f99_hold_share`

- Question: RQ10, holding small flocks
- Setting: goal 1.9 to 2.5 $R_f$ x share 90, 95 and 99%
- Record: 50,170 trials, 746 cells (57 open), 0 errors, 0.91 h

#### `dmin_f99_c1.3`

- Question: RQ11, stronger cohesion
- Record: 10,800 trials, 180 cells (1 open), 0 errors, 0.31 h

#### `dmin_f99_c1.6`

- Question: RQ11, stronger cohesion
- Record: 10,830 trials, 180 cells (0 open), 0 errors, 0.29 h

#### `dmin_f99_c2.0`

- Question: RQ11, stronger cohesion
- Record: 10,780 trials, 180 cells (0 open), 0 errors, 0.41 h

#### `dmin_f99_k05`

- Question: RQ11, weaker cohesion
- Record: 11,630 trials, 149 cells (14 open), 0 errors, 2.29 h

#### `dmin_f99_view_range`

- Question: RQ12, limited sight, no sharing
- Record: 21,040 trials, 293 cells (27 open), 0 errors, 0.53 h

#### `dmin_f99_view_comm`

- Question: RQ12, sharing what dogs see
- Record: 6890 trials, 102 cells (3 open), 0 errors, 0.20 h

#### `dmin_f99_big`

- Question: RQ13, above the calibration edge
- Record: 2230 trials, 84 cells (1 open), 0 errors, 3.12 h

#### `dmin_f99_big_dense`

- Question: RQ13, denser imposed flock
- Record: 1320 trials, 15 cells (2 open), 0 errors, 0.73 h

#### `dmin_f99_big_loose`

- Question: RQ13, looser imposed flock
- Record: 830 trials, 14 cells (1 open), 0 errors, 0.26 h

#### `dmin_f99_big_cap`

- Question: RQ13, drive point capped
- Record: 2550 trials, 45 cells (3 open), 0 errors, 5.5 h
- Note: 100 more trials at $N = 3200$ from a run stopped early are left out of the trials, every total and the hours (taken from `status.json`, as they are not in the log)

#### `lama_r50`

- Question: RQ14, Lama and di Bernardo (2024)
- Setting: gather task, sensing radius 10
- Record: 17,660 trials, 500 cells (23 open), 0 errors, 6.53 h

#### `lama_r50_inf`

- Question: RQ14, as `lama_r50`
- Setting: gather task, infinite sensing
- Record: 22,620 trials, 500 cells (1 open), 0 errors, 6.47 h

Notes on the follow-up records:

- $R_f$ is the flock radius calibrated under one driving dog; goals are given in multiples of it.
- The three resumed grids have no single log line, and their hours are not recorded per sitting; the sittings we could find add up to 4.285 h for the three, perhaps a little low.
- The 41 folders hold 6845 cells, 499 of them open. The first-study and follow-up records sum to 7386 and 517 because they also count the first-pass records of the three 99% main runs (541 cells, 18 open).

### Runs outside the study

- `dmin_pilot`: a one-batch pilot.
- The first `ring` dog-start and spacing runs, kept only in git history.
- Two validation passes of the Lama model before `lama_r50`: 8200 trials in scratch folders, not kept. The second fixed the order in which herders and targets move.

## Appendix B: Claims and evidence

Every claim rests on protocol runs except claim 5, which rests on replays, and claim 7, a formula checked against runs. Each entry gives the claim, the runs behind it and its limits.

### Claim 1

- Claim: a compact flock needs one dog ($D_{\min} = 1$) up to $N = 1131$.
- Runs: team rule on `compact` in `dmin_m12`, `dmin_m6`, `dmin_m3` and `dmin_f99_m3` up to $N = 400$, `dmin_f99_m12` and `dmin_f99_m6` up to 566, and `dmin_f99_big_cap` at 800 and 1131.
- Limits: drive task and team rule only. FAT has no reliable team on compact $N = 400$ (`dmin_f99_fat`, lower bound 12), and the holding runs have none on compact $N = 25$ and 50. Above 1056 it holds only with the capped drive point (claim 7).

### Claim 2

- Claim: up to $N = 50$ one dog is enough on every layout and deadline.
- Runs: every $N \le 50$ cell of the 23 first-study protocols is decided at $D = 1$.
- Limits: the reason for it is untested.

### Claim 3

- Claim: on scattered flocks $D_{\min}$ grows with log-log slope 0.27-0.38 on `wide` and 0.28-0.38 on `outlier_rich` at 12 drive times, and 0.38-0.61 and 0.40-0.58 at 6 (99% rule).
- Runs: slopes over the brackets of nine sizes ($N = 25$-566) in `dmin_f99_m12` and `dmin_f99_m6`.
- Limits: valid up to about $N = 600$, where the flock stops settling to one size. `split` is left out.

### Claim 4

- Claim: under the strict rule large teams fail on the last sheep.
- Runs: the strict failures with $D \ge 6$ in the sensitivity base run `dmin_s_base` (`wide` and `outlier_rich`, $N = 100$-400, 6 drive times). With slower dogs (`dmin_s_dogspeed`) strict $D_{\min}$ on `outlier_rich` $N = 400$ goes from none to 6.
- Limits: strict rule with an open goal.

### Claim 5

- Claim: on `split` $N = 200$ at 6 drive times, two changes to the team rule speed up the drive but make no team reliable; the cause of the slowdown is open.
- Runs: `split_diagnostic` replays of stored trials with a changed team rule, 99% rule, 12 seeds per cell; medians over the successful replays only.
- Limits: at $N = 100$ the medians move by at most 10 s. At 3 drive times the replays rule out reliability only at $N = 200$ with 4, 8 and 16 dogs.

### Claim 6

- Claim: weaker cohesion makes $D_{\min}$ grow faster on `wide`, toward 0.5.
- Runs: `dmin_f99_k05` and `dmin_f99_c*`, 99% rule, 12 drive times.
- Limits: one weaker level only ($n = 0.5N$ neighbours), fitted on four sizes ($N = 50$-400) against five (25-400) for `dmin_f99_c*`. At $N = 25$ the weaker level's $R_f$ still changed by 62% between the 90 s windows that calibration compares; weaker settings ($n = 0.25N$ and below, $c = 0.8$ and 0.9) never settled to one flock size, so those checks are not stored. No stored run tests weaker levels.

### Claim 7

- Claim: above $N \approx 1056$ Strömbom's drive point is beyond the sheep's reaction distance.
- Runs: uncapped, 0 of 10 trials succeed at $N = 1131$ for every $D$. Capped (`dmin_f99_big_cap`), `compact` succeeds at 800, 1131 and 1600, and in 42 of 42 trials at 3200 (teams of 3 to 12 dogs).
- Limits: assumes the reaction distance $r_s = 65$ m. The 3200 result is partial, from the 100 uncounted $N = 3200$ trials of a run stopped early.

### Claim 8

- Claim: dogs kept 2 m apart make extra dogs harmful on `outlier_rich` $N = 400$.
- Runs: `dmin_f99_hold_spacing` succeeds in 186 of 200 trials at $D = 6$, 54 of 70 at 9 and 5 of 10 at 16; every $D \ge 9$ is unreliable.
- Limits: not seen on `wide` or `compact`.

### Claim 9

- Claim: at $N = 200$ a sensing range of 30 to 65 m costs `wide` one or two dogs, which whole-team sharing at 65 m wins back, and does better than full sight on `split`.
- Runs: `dmin_f99_view_range` and `dmin_f99_view_comm`, `wide` and `split` $N = 200$, 99% rule, 6 drive times.
- Limits: sharing was tested at 65 m only, and is instant and error-free in the model.

### Claim 10

- Claim: near the threshold, an average success of 0.99 accepts teams that fail in 9 of 30 runs.
- Runs: `lama_r50`, sensing radius 10, 144 targets and 11 herders (average share 0.992).
- Limits: targets without cohesion on a disc.

### Claim 11

- Claim: holding small flocks fails with the default goal; a goal of about 16 to 19 m holds them with one dog.
- Runs: `dmin_f99_hold_goal` and `dmin_f99_hold_share`: one dog decided reliable on every layout from 18.6 m ($N = 25$) and 17.5 m ($N = 50$) at 99%, with brackets down to 15.5 and 16.0 m. In the `hold_walk` replays the flock centre walks a median 17, 15 and 13 m at $N = 25$, 50 and 100 while the dogs withdraw.
- Limits: goal levels in steps of $0.2 R_f$, tied to the withdrawal rule. The walk was never varied directly, so whether it causes the failures is open.

## Appendix C: Reproducibility

Table 3 lists what is needed to run the study again.

**Table 3: Reproducibility items.**

| Item | Where |
| :--- | :--- |
| Code | Repository `HerdSim`, branch `scaling-cli-d-min-max` at the time of writing; the result folders record no commit |
| Environment | `uv`, Python 3.11 or later; versions locked in `pyproject.toml` and `uv.lock`; one BLAS thread per process; the CPU is not recorded |
| Start layouts | `sim/core/world/layouts.py` (`compact`, `wide`, `split`, `outlier_rich`) |
| Random streams | Cells with the same seed start from the same flock |
| Hardware | Linux workstation, 20 workers (`--workers 20`) |
| Raw data | 439,120 trial rows in `results/<protocol>/trials.csv`; `trials.jsonl` (in git as `trials.jsonl.gz`) holds the same rows plus the 100 uncounted $N = 3200$ trials of `dmin_f99_big_cap`; `results/diagnostics/` holds the CSVs of the three replay tools |
| Running the study | `uv run cli/campaign.py run --protocol <id>` and `uv run cli/run_queue.py` |
| Tables | `docs/generate_docs/make_docs.py` writes `docs/report/results_tables.md` from the result folders, with the same verbs as `cli/dmin_tables.py` |
| Tests | `make test` runs the unit, invariant and regression tests; `make bench` runs the benchmark tests, six small campaigns end to end |
| Replays | `services/replay.py`; results below |

### Replay check

The diagnostic tools ran 1172 replays, each rerunning a stored trial from its settings and seed.

- Unchanged replays: 596 (164 pressure, 192 base `split` and 240 holding-walk). 590 had a stored trial to compare with, and all gave its success and tick count on the same machine with one BLAS thread per process.
- Unchanged replays with nothing to compare: 6 base `split` replays at 3 drive times ($N = 200$, $D = 4$, 8 and 16, seeds 10 and 11), which `dmin_f99_m3` does not store.
- Changed-rule replays: 576, the same 192 `split` seeds for each of three changes (collecting dogs spread over the clusters, a shorter stop distance, both), with no stored result to compare with.
