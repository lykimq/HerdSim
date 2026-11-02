# Protocols

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: the protocol files in `protocols/configs/` and the study queue.

The 6 protocols of the study, in queue order: what each tests, its grid, and the settings it changes from `protocols/configs/canonical.yaml`. The results of protocol `<id>` are in `results/<id>`; its numbers are in the [result tables](../report/results_tables.md), its trials and hours in the [run record](../report/d_min_report.md#5-run-record). Terms are in the [glossary](../glossary.md), the methods in [Strombom sheep](../methods/strombom_sheep.md) and [team rule](../methods/strombom_multi.md) and each setting in [settings](settings.md).

The rule is the share of the flock that must be in the goal (strict: every sheep). The deadline is a multiple of the drive time. The research questions RQ1 to RQ3 are in the [report](../report/d_min_report.md#1-the-question). As for the task, all protocols run the `drive_to_goal` task.

## Protocols

### `dmin_m12`

D_min against N on four start layouts, strict rule, 12 drive times.

| Field | Value |
| :--- | :--- |
| Run | `strombom_multi`, strict rule, 12 drive times |
| Layouts | compact, wide, split, outlier_rich |
| Flock sizes N | 25, 50, 100, 200, 400 |
| Team sizes D | 1-4, 6, 8, 12, 16, 24 |

### `dmin_m6`

D_min against N on four start layouts, strict rule, 6 drive times.

| Field | Value |
| :--- | :--- |
| Run | `strombom_multi`, strict rule, 6 drive times |
| Layouts | compact, wide, split, outlier_rich |
| Flock sizes N | 25, 50, 100, 200, 400 |
| Team sizes D | 1-4, 6, 8, 12, 16, 24 |

### `dmin_m3`

D_min against N on four start layouts, strict rule, 3 drive times.

| Field | Value |
| :--- | :--- |
| Run | `strombom_multi`, strict rule, 3 drive times |
| Layouts | compact, wide, split, outlier_rich |
| Flock sizes N | 25, 50, 100, 200, 400 |
| Team sizes D | 1-4, 6, 8, 12, 16, 24 |

### `dmin_f99_m6`

D_min against N on four start layouts, 99 percent rule, 6 drive times, nine sizes.

| Field | Value |
| :--- | :--- |
| Run | `strombom_multi`, 99 percent rule, 6 drive times |
| Layouts | compact, wide, split, outlier_rich |
| Flock sizes N | 25, 50, 71, 100, 141, 200, 283, 400, 566 |
| Team sizes D | 1-4, 6, 8, 12, 16, 24 |
| Changed from canonical | decide_finish_times = true |

### `dmin_f99_m3`

D_min against N on four start layouts, 99 percent rule, 3 drive times.

| Field | Value |
| :--- | :--- |
| Run | `strombom_multi`, 99 percent rule, 3 drive times |
| Layouts | compact, wide, split, outlier_rich |
| Flock sizes N | 25, 50, 100, 200, 400 |
| Team sizes D | 1-4, 6, 8, 12, 16, 24 |
| Changed from canonical | decide_finish_times = true |

### `dmin_f99_m12`

D_min against N on four start layouts, 99 percent rule, 12 drive times, nine sizes.

| Field | Value |
| :--- | :--- |
| Run | `strombom_multi`, 99 percent rule, 12 drive times |
| Layouts | compact, wide, split, outlier_rich |
| Flock sizes N | 25, 50, 71, 100, 141, 200, 283, 400, 566 |
| Team sizes D | 1-4, 6, 8, 12, 16, 24 |
| Changed from canonical | decide_finish_times = true |

## Methods

A method is a sheep model paired with a dog controller ([Strombom sheep](../methods/strombom_sheep.md) and [team rule](../methods/strombom_multi.md)).

`strombom_multi` pairs the sheep model `strombom` with the dog controller `collect_drive_multi`.
