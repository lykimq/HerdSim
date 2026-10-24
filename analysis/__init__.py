"""Reading finished results and deciding what they say. Nothing here runs the model.

frontier     the decision rules: reliable or not, faster or not, D_min, D_sat, zones; the
             adaptive run uses them to choose where seeds go
results      reading a results folder, and printing a table as Markdown
dmin         D_min at a tighter deadline, read from the trials of one run
dmin_tables  the tables behind the report (cli/dmin_tables.py prints them)
growth_fits  which shape D_min(N) follows: growing without limit, or levelling off
pressure     how long the sheep spend near a dog, measured during a replay
"""
