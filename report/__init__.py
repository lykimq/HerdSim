"""Writing the results of analysis/ as the tables and text the docs show. Nothing here decides a
value: D_min, D_sat, brackets, slopes and fits come from analysis/, and these modules only choose
how they read.

    uv run cli/dmin_tables.py --help                  # print the tables, one verb each
    uv run python docs/make_docs.py                   # write the generated pages

The modules:

    text      how one value is written: '2-4', '[5]', 'none on grid', the success rule, the
              label of a factor level, and a table as Markdown
    tables    the tables of cli/dmin_tables.py whose cells are text: D_min and D_sat by layout
              and N, their growth, cost beyond D_sat, upper end, runs side by side
    overview  every run in one view per success rule (docs/report/summary_results.md)

This layer sits above analysis/ and the campaign layer (it reads protocols for the overview);
neither imports it.
"""
