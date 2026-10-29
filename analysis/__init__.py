"""Reading finished results and deciding what they say. Nothing here runs the model. The text
forms the docs use (a team size as '2-4' or '[5]', the success rule, factor labels, Markdown)
are written in report/, which reads these values; nothing here imports it.

    uv run cli/dmin_tables.py --help                  # the tables, one verb each
    uv run cli/dmin_report.py --help                  # D_min at a tighter deadline

The modules:

    frontier           the decision rules: reliable or not, faster or not, D_min, D_sat, zones;
                       the adaptive run uses them to choose where seeds go
    keys               the text keys of groups, cells and trials, built and split in one place
    results            reading a results folder and the run log
    curves             the D curves of a run as numbers: brackets of D_min and D_sat, growth
                       slopes and shape fits, cells where more dogs did worse
    dmin               D_min at a tighter deadline or a share of the flock, from one run
    growth_fits        which shape D_min(N) follows: growing without limit, or levelling off
    herdability        the gather task read the paper's way (N*)
    trial_measures     single trials: arrival tail, failed endings, finish spread, flock size
    pressure           how long the sheep spend near a dog, measured during a replay
    dispersion_burden  the start spread times N, and how failed drives failed
"""
