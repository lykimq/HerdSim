"""The key format is stored in every results folder, so it must not change."""

from analysis import keys


def test_keys_keep_the_stored_format_and_split_back():
    group = keys.group_key("strombom_multi", "wide", [("dog_start_gap", 15), ("x", "a")], 200)
    assert group == "strombom_multi|wide|dog_start_gap=15.0|x=a|N=200"
    cell = keys.cell_key(group, 4)
    trial = keys.trial_key(cell, 7)
    assert trial == "strombom_multi|wide|dog_start_gap=15.0|x=a|N=200|D=4|seed=7"
    assert keys.cell_of_trial(trial) == cell
    assert keys.group_of_cell(cell) == group
    parts = keys.split_group(group)
    assert parts == {
        "method": "strombom_multi",
        "layout": "wide",
        "factors": "dog_start_gap=15.0|x=a",
        "n": 200,
    }
    assert keys.join_group(**parts) == group
    assert keys.join_group("m", "wide", "", 25) == "m|wide|N=25"
