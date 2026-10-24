"""Running things: everything between a protocol file and a results folder.

protocol     load and check a protocol YAML over the canonical defaults
cells        the grid: D curves, cells, trials and the run config of each
calibration  the flock radius R_f(N) every task is sized from
adaptive     the campaign: rounds of seeds until every cell is decided
runner, pool run a batch of trials in worker processes
store        the results folder: what is written, locked and resumed
replay       run stored trials of a finished folder again, checked against what was stored
"""
