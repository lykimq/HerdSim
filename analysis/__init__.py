"""Reading finished results and deciding what they say. Nothing here runs the model.

    uv run cli/dmin_tables.py --help                  # the tables, one verb each
    uv run cli/dmin_report.py --help                  # D_min at a tighter deadline

The modules:

    frontier           the decision rules: reliable or not, faster or not, D_min, D_sat, zones;
                       the adaptive run uses them to choose where seeds go
    keys               the text keys of groups, cells and trials, built and split in one place
    results            reading a results folder and the run log, printing a table as Markdown
    dmin               D_min at a tighter deadline or a share of the flock, from one run
    dmin_tables        summary tables of finished runs (cli/dmin_tables.py prints them)
    growth_fits        which shape D_min(N) follows: growing without limit, or levelling off
    herdability        the gather task read the paper's way (N*) beside HerdSim's D_min
    pressure           how long the sheep spend near a dog, measured during a replay
    dispersion_burden  the start spread times N, and how failed drives failed
"""
