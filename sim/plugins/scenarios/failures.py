"""Shared failure labels: ``NONE`` (success), ``TIMEOUT``, plus each task's own."""

from __future__ import annotations

from dataclasses import dataclass

NONE = "none"
TIMEOUT = "timeout"  # none of the task's rules matched


@dataclass(frozen=True)
class Failure:
    mode: str
    hints: tuple[str, ...]  # every rule that matched, the first in the task's priority is the mode
