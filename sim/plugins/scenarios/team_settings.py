"""Settings of the dog team that every task passes through to the controllers.

Dog spacing, the local view and its sharing, the holding step and the drive cap are read
by the dog controllers, not by any task. Each task carries them from the protocol into the
run config the same way, so they live here once. ``TEAM`` gives each its type and its off
value, the value at which the paper's dog runs; the setup keys, the neutral values of the
physics hash and the dog that calibration uses are all read from it. ``check`` refuses the
combinations no controller can honour.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

# name: (type, off value)
TEAM: dict[str, tuple[type, Any]] = {
    "dog_spacing": (float, 0.0),
    "sensing_range": (float, 0.0),
    "communication": (str, "none"),
    "hold_withdraw": (bool, False),
    "drive_offset_cap": (float, 0.0),
}
KEYS = tuple(TEAM)
OFF = {name: off for name, (_, off) in TEAM.items()}

# What dogs share when they see only part of the flock (collect_drive_multi).
COMMUNICATION = ("none", "neighbour", "shared")


def setup(settings: Mapping[str, Any]) -> dict[str, Any]:
    """The team settings of a protocol, typed, as setup keys."""
    return {name: kind(settings[name]) for name, (kind, _) in TEAM.items()}


def check(config: dict[str, Any]) -> None:
    """Team settings of a built run config against the controller that runs it."""
    controller = config["dog_controller"]
    if float(config["dog_spacing"]) < 0.0:
        raise ValueError("dog_spacing must not be negative")
    if config["hold_withdraw"] and controller != "collect_drive_multi":
        raise ValueError("hold_withdraw is a step of the collect_drive_multi team rule only")
    if float(config["dog_spacing"]) > 0.0 and controller in ("kubo_forces", "lama_herders"):
        raise ValueError(f"dog_spacing is not for {controller}, whose dogs keep apart on their own")
    if config["communication"] not in COMMUNICATION:
        raise ValueError(f"communication {config['communication']!r} not in {COMMUNICATION}")
    if float(config["sensing_range"]) > 0.0:
        if controller != "collect_drive_multi":
            raise ValueError("sensing_range is a setting of the collect_drive_multi team rule only")
        if config["hold_withdraw"]:
            raise ValueError("hold_withdraw judges the goal from the true flock; not with sensing")
