"""Serve curated documentation markdown for the Guide tab."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter()

_GUIDE_ROOT = Path(__file__).resolve().parents[2] / "docs" / "guide"

# Whitelist served by Guide. Order and groups drive the left nav.
_DOC_ENTRIES: list[tuple[str, Path, str, str]] = [
    # slug, path, title, nav group
    ("overview", _GUIDE_ROOT / "overview.md", "Overview", "Start here"),
    ("simulate", _GUIDE_ROOT / "simulate.md", "Simulate", "How to use"),
    (
        "guide/compare",
        _GUIDE_ROOT / "compare.md",
        "Compare",
        "How to use",
    ),
    ("experiments", _GUIDE_ROOT / "experiments.md", "Experiments", "How to use"),
    ("guide/netlogo", _GUIDE_ROOT / "netlogo.md", "NetLogo", "How to use"),
    (
        "guide/methods",
        _GUIDE_ROOT / "methods" / "README.md",
        "Methods",
        "Reference",
    ),
    (
        "guide/methods/strombom_2014",
        _GUIDE_ROOT / "methods" / "strombom_2014.md",
        "Strombom 2014",
        "Reference",
    ),
    (
        "guide/methods/strombom_multi",
        _GUIDE_ROOT / "methods" / "strombom_multi.md",
        "Strombom Multi-Dog",
        "Reference",
    ),
    (
        "guide/methods/strombom_noise",
        _GUIDE_ROOT / "methods" / "strombom_noise.md",
        "Strombom Noise",
        "Reference",
    ),
    (
        "guide/methods/v_formation",
        _GUIDE_ROOT / "methods" / "v_formation.md",
        "V-Formation",
        "Reference",
    ),
    (
        "guide/methods/heterogeneous",
        _GUIDE_ROOT / "methods" / "heterogeneous.md",
        "Heterogeneous",
        "Reference",
    ),
    (
        "guide/methods/obstacle_aware",
        _GUIDE_ROOT / "methods" / "obstacle_aware.md",
        "Obstacle-Aware",
        "Reference",
    ),
    (
        "guide/methods/kubo_2022",
        _GUIDE_ROOT / "methods" / "kubo_2022.md",
        "Kubo 2022",
        "Reference",
    ),
    (
        "guide/methods/flocking_dog_2024",
        _GUIDE_ROOT / "methods" / "flocking_dog_2024.md",
        "Flocking Dog",
        "Reference",
    ),
    (
        "guide/methods/fat",
        _GUIDE_ROOT / "methods" / "fat.md",
        "FAT",
        "Reference",
    ),
    (
        "guide/methods/communication_free",
        _GUIDE_ROOT / "methods" / "communication_free.md",
        "Communication-Free",
        "Reference",
    ),
    (
        "guide/methods/adaptive",
        _GUIDE_ROOT / "methods" / "adaptive.md",
        "Adaptive",
        "Reference",
    ),
    (
        "guide/scenarios",
        _GUIDE_ROOT / "scenarios.md",
        "Scenarios",
        "Reference",
    ),
    ("guide/metrics", _GUIDE_ROOT / "metrics.md", "Metrics", "Reference"),
    (
        "guide/environment",
        _GUIDE_ROOT / "environment.md",
        "Environment",
        "Reference",
    ),
]

DOC_SLUGS: dict[str, Path] = {slug: path for slug, path, _title, _group in _DOC_ENTRIES}


@router.get("")
async def list_docs():
    """List Guide-visible documentation slugs in nav order."""
    items = []
    for slug, path, title, group in _DOC_ENTRIES:
        items.append(
            {
                "slug": slug,
                "exists": path.is_file(),
                "title": title,
                "group": group,
            }
        )
    return {"docs": items}


@router.get("/{slug:path}")
async def get_doc(slug: str):
    """Return markdown for a whitelisted slug."""
    path = DOC_SLUGS.get(slug)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Unknown doc slug '{slug}'")
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Doc file missing for '{slug}'")
    return PlainTextResponse(
        path.read_text(encoding="utf-8"), media_type="text/markdown; charset=utf-8"
    )
