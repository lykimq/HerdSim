"""The failure label of a trial, shared by every task's rules.

A task reads a finished trial's metric history and names why it failed
(``Scenario.classify_failure``). ``NONE`` is the label of a success and ``TIMEOUT`` the label of
a failure no rule explains; each task adds its own labels in its rules module.
"""

from __future__ import annotations

from dataclasses import dataclass

NONE = "none"
TIMEOUT = "timeout"  # none of the task's rules matched


@dataclass(frozen=True)
class Failure:
    mode: str
    hints: tuple[str, ...]  # every rule that matched, the first in the task's priority is the mode
