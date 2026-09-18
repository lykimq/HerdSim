# Campaign YAML checklist (copy into every new configs/budget/campaigns/*.yaml)
#
# Before adding a campaign:
# 1. Point protocol: at configs/budget/canonical_grid.yaml (or a dated fork).
# 2. For EVERY override (N, D, layouts, seeds, instruments, max ticks, factors),
#    write a one-line WHY comment. "Faster" alone is not enough -- say what
#    scientific or engineering question the subset still answers.
# 3. Set grade: SMOKE | SCOUT | CLAIM and do not cite below that grade.
# 4. Set output: results/budget/phase{k}/{slug}/ matching campaign_id.
# 5. List packages: that this run is meant to feed (A-G).
# 6. Log the campaign in docs/research/budget/progress_tracker.md after it runs.
# 7. If you change a frozen Section 8 default, bump protocol_id / document an
#    exception in the tracker; do not silently diverge.
#
# Template:
#
# campaign_id: phaseK_short_name
# phase: K
# grade: SMOKE
# output: results/budget/phaseK/short_name
# protocol: configs/budget/canonical_grid.yaml
# instruments: [...]   # why these methods
# layouts: [...]       # why these X0
# flock_sizes: [...]   # why this N subset vs full freeze
# shepherd_counts: [...]
# seeds: N
# seed_mode: scout|claim
# store_timeseries: true|false
# packages: [A]
