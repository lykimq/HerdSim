# Command-Line Reference

Every tool lives in [`cli/`](../../cli/) and is run from the repository root with `uv run`; `--help` prints the same information as the tables below. This page lists every verb and flag. For the order in which to use them, read [`cli/README.md`](../../cli/README.md). Terms such as cell, curve, bracket, the zones and $D_{\min}$ are defined in the [glossary](../glossary.md).

## `cli/campaign.py`: one protocol

```bash
uv run cli/campaign.py <verb> --protocol <id or path> [--output <folder>] [--workers <n>]
```

Table 1 lists the verbs and Table 2 the flags:

**Table 1: Verbs of `campaign.py`.**

| Verb | Does | Writes |
| :--- | :--- | :--- |
| `plan` | Prints the grid, the number of cells, the cost of the first round, and whether the results folder is new, resumes or is refused. | nothing |
| `calibrate` | Measures the settled flock radius $R_f(N)$ per method and flock size and prints it; refuses a size that does not settle. Says there is nothing to calibrate for the gather task. | nothing |
| `run` | Calibrates (or reuses the folder's saved radii), then runs rounds of trials until every cell is decided, every open cell is at the seed cap, or the time budget is spent. | `results/<protocol_id>/` |
| `status` | Prints how far a run has got, whether it is running now, and why it stopped. | nothing |
| `refresh` | Decides every cell again from the stored trials, after a change to the decision rules in `analysis/frontier.py`. Runs no trial and adds no dog count. | rewrites `trials.csv`, `frontier_cells.csv` and `frontier_groups.csv` |

**Table 2: Flags of `campaign.py`.**

| Flag | Default | Meaning |
| :--- | :--- | :--- |
| `--protocol` | required | A protocol id under `protocols/configs/protocols/`, or a path to a YAML file. |
| `--output` | the protocol's `output` | The results folder. |
| `--workers` | the number of CPUs | Worker processes, each running one trial at a time. |

## `cli/run_queue.py`: the study

```bash
uv run cli/run_queue.py [--list] [--workers <n>] [--only <id> ...]
```

Runs the 41 protocols of the study in the order they ran, as listed in `protocols/configs/study_queue.yaml`, each as `campaign.py run` would. A folder where every cell is decided is skipped, one that stopped for any other reason is resumed, and a protocol that raises is logged while the queue moves on. Each protocol appends one line to `results/queue_log.jsonl`. Table 3 lists the flags:

**Table 3: Flags of `run_queue.py`.**

| Flag | Default | Meaning |
| :--- | :--- | :--- |
| `--list` | off | Print the queue and the state of each folder, then exit. |
| `--workers` | 20 | Worker processes per protocol. |
| `--only` | the whole queue | Protocol ids to run, in the order given; ids outside the queue are refused. |

## `cli/dmin_tables.py`: tables from finished runs

```bash
uv run cli/dmin_tables.py <verb> <folder> [<folder> ...] [flags]
```

A folder is a protocol id under `results/` or a path. Every verb prints Markdown. Nothing here runs a simulation. An entry such as `2-3` is a range (3 is reliable, 2 still undecided), `[5]` a lower bound with no reliable team yet, and `none on grid` a curve where every tested team is unreliable. Table 4 lists the verbs:

**Table 4: Verbs of `dmin_tables.py`.**

| Verb | Flags | Prints |
| :--- | :--- | :--- |
| `record` | none, takes no folder | Every run in `results/queue_log.jsonl`: when it finished, trials, cells, open cells, errors, hours. |
| `dispersion` | none, takes no folder | The start spread times $N$ per layout (`dmin_m6`), and where the failed drives of the main runs ended: near the goal or never there. |
| `dmin` | | $D_{\min}$ by layout and flock size, one table per folder. |
| `growth` | | The range of log-log slopes of $D_{\min}$ against $N$ that the brackets allow, and whether layout or $N$ moves it more. |
| `fits` | | A power law against a curve that levels off, fitted to $D_{\min}(N)$ per layout, and the range each shape allows at larger $N$. |
| `dsat` | | $D_{\mathrm{sat}}$ by layout and flock size, and its growth. |
| `effort` | | Finish time, dog time and dog path beyond $D_{\mathrm{sat}}$, relative to the $D_{\mathrm{sat}}$ cell. |
| `zones` | | Cells where more dogs did worse (crowded, dip, collapse, recovered). |
| `upper` | | The upper end of every curve: how often $D_{\max}$ is only the grid top, and the curves with $D_{\max}$ below it, a $D_{\mathrm{crowd}}$ or a $D_{\mathrm{overcrowd}}$. |
| `tail` | `--layout`, `--n` | Per $D$, over successful trials: the median time from 90 to 99 percent of the flock in the goal, the share of trials where it exceeds a minute, and the median finish. |
| `endings` | `--min-d` | How failed trials ended: with no sheep in the goal, or after 99 percent had been in; and the time from 99 percent in to the finish in successes. |
| `spread` | `--layout`, `--n` | Quartiles of the finish time per $D$, to spot finish times in two groups. |
| `nested` | (two folders) | Whether the shorter of two deadlines only cuts the longer one's trials short. |
| `curve` | `--layout`, `--n` | One curve cell by cell across folders: successes out of trials, reliability, median finish. |
| `labels` | | Failed trials per layout by the failure label the task gives them (for example a plain timeout, `stuck`, `flock_escaped`). |
| `pace` | `--layout`, `--n` | Per $D$, over successful trials: the median dog speed (path over finish time) and the median share of dogs standing still. |
| `dips` | | Cells above $D_{\min}$ that are not reliable. |
| `arrival` | `--pct {90,95,99}` | $D_{\min}$ if success had meant that share of the flock in the goal, beside the run's own rule. |
| `compare` | `--base <folder>` | Each variant folder beside the base, curve by curve. |
| `methods` | `--pct {90,95,99}` | $D_{\min}$, $D_{\mathrm{sat}}$, $D_{\mathrm{crowd}}$ and $D_{\max}$ per curve across folders; `--pct` relabels a strict run so every row uses one rule. |
| `overview` | | Every folder in one view: what each protocol changes from the canonical settings, then one row per method, layout and variant with $D_{\min}$, $D_{\mathrm{sat}}$, $D_{\max}$ and $D_{\mathrm{overcrowd}}$ per $N$, in tables split by success rule ([summary_results.md](../report/summary_results.md)). |
| `herdability` | `--above <N>` | The gather task read the paper's way (mean share in the goal at least 0.99, and at 0.90 and 0.95) beside $D_{\min}$, with the growth exponent of both above `--above` targets. |
| `extent` | `--layout <name>` | The flock's measured size against the radius its task was sized from, per cell. |

## `cli/dmin_report.py`: a finished run at a tighter deadline

```bash
uv run cli/dmin_report.py --protocol <id> --folder <results folder> --multiples <m> [<m> ...]
```

The dogs do not know the deadline, so a trial runs the same under any of them, and one that finished inside a tighter deadline would have succeeded under it too. The tool relabels each stored trial by whether it finished inside each deadline (a multiple of the drive time) and prints $D_{\min}$, $D_{\min,\mathrm{low}}$ and $D_{\max}$ per curve. The deadlines must not be looser than the one the run used.

## `cli/diagnostics/`: replays and checks

The three replay tools run stored trials again. An unchanged replay must reproduce its stored outcome and length, or the tool stops. Each writes their rows to `--out` as CSV and print a per-cell summary.

### `pressure_replay.py`

```bash
uv run cli/diagnostics/pressure_replay.py <folder> --out <csv> [--layouts ...] [--n ...] [--seeds <k>] [--workers <n>]
```

Replays the cells at $D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ and the smallest tested $D$ at or above $2 D_{\mathrm{sat}}$, taken from the folder's current frontier, and measures how long each sheep spends fleeing a dog and how much of the flock flees at once. Table 5 lists the flags:

**Table 5: Flags of `pressure_replay.py`.**

| Flag | Default |
| :--- | :--- |
| `--layouts` | `wide outlier_rich` |
| `--n` | `100 400` |
| `--seeds` | 12 |
| `--workers` | 20 |
| `--out` | required |

### `split_diagnostic.py`

```bash
uv run cli/diagnostics/split_diagnostic.py --out <csv> [--seeds <k>] [--workers <n>]
```

Replays `split` at $N = 100$ and 200, $D = 2, 4, 8, 16$, at 6 and 3 drive times, in four versions of the team rule: as run, with the dog stop distance cut from $3 r_a$ to $r_a$, with collecting dogs taking outliers at least $f(N)$ apart, and both. Defaults: 12 seeds, 8 workers.

### `hold_walk.py`

```bash
uv run cli/diagnostics/hold_walk.py --out <csv> [--goal <multiple>] [--layouts ...] [--n ...] [--d ...] [--seeds <k>] [--workers <n>]
```

Replays `dmin_f99_hold_goal` at one goal level and measures, from the first tick with the share inside to the first tick no dog is within $r_s$, the walk of the flock centre, its duration and the distance of the farthest sheep from the centre. The summary adds the goal radius that walk calls for, $w/2$ plus that distance (medians per $N$ and per $N$ and $D$). Table 6 lists the flags:

**Table 6: Flags of `hold_walk.py`.**

| Flag | Default |
| :--- | :--- |
| `--goal` | 3.0 |
| `--layouts` | all four |
| `--n` | `25 50 100` |
| `--d` | `1 2 4 8` |
| `--seeds` | 5 |
| `--workers` | 20 |
| `--out` | required |

### `gradient_validation.py`

```bash
uv run cli/diagnostics/gradient_validation.py [--seeds <k>]
```

Replays nothing. Draws start flocks and prints, per layout, flock size and neighbour count, the angle between the true direction to the flock centre and the direction a sheep would get from its nearest neighbours. Default: 10 flocks per layout and size.
