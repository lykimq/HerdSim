"""The packages import only downward: cli -> services, analysis -> sim.

sim is the model and knows nothing of campaigns. analysis reads finished results and runs no
simulation. services runs things (protocols, campaigns, calibration, replays) and may use the
analysis that decides cells. cli tools are entry points; none imports another, so removing one
breaks nothing else.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

FORBIDDEN = {
    "sim": {"services", "analysis", "cli"},
    "analysis": {"sim", "services", "cli"},
    "services": {"cli"},
    "cli": {"cli"},
}


def imported_packages(path: Path) -> set[str]:
    """Top-level names of the absolute imports in a file."""
    names = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return names


@pytest.mark.parametrize("package", sorted(FORBIDDEN))
def test_package_imports_only_downward(package: str):
    wrong = {
        str(path.relative_to(REPO)): sorted(imported_packages(path) & FORBIDDEN[package])
        for path in sorted((REPO / package).rglob("*.py"))
    }
    assert not {k: v for k, v in wrong.items() if v}
