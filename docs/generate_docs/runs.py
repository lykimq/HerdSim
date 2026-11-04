"""The study's runs that the tables and figures show, and the flock sizes they label."""

from __future__ import annotations

# Main grids by drive-time multiple of the deadline, strict and 99 percent rule.
STRICT_RUNS = {12: "dmin_m12", 6: "dmin_m6", 3: "dmin_m3"}
F99_RUNS = {12: "dmin_f99_m12", 6: "dmin_f99_m6", 3: "dmin_f99_m3"}
STRICT_MAIN = tuple(STRICT_RUNS.values())
F99_MAIN = tuple(F99_RUNS.values())
# Uncoordinated farthest-agent targeting (FAT) baseline at 6 drive times, strict and 99 percent.
FAT_RUNS = ("dmin_fat", "dmin_f99_fat")
# The 99 percent grids resumed with more flock sizes.
NINE_SIZE_RUNS = (F99_RUNS[12], F99_RUNS[6])
# Flock sizes of every main grid.
ORIGINAL_NS = (25, 50, 100, 200, 400)
