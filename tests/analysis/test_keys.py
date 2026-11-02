"""Group, cell and trial key format: build and split must stay stable."""

from analysis import keys


def test_keys_keep_the_stored_format_and_split_back() -> None:
    group = keys.group_key("strombom_multi", "wide", 200)
    assert group == "strombom_multi|wide|N=200"

    cell = keys.cell_key(group, 4)
    trial = keys.trial_key(cell, 7)
    assert trial == "strombom_multi|wide|N=200|D=4|seed=7"
    assert keys.cell_of_trial(trial) == cell
    assert keys.group_of_cell(cell) == group

    assert keys.split_group(group) == {"method": "strombom_multi", "layout": "wide", "n": 200}
