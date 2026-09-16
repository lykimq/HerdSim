"""Serve curated documentation markdown for the Guide tab."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter()

_DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs"

# Whitelist served by Guide. Order and groups drive the left nav.
_DOC_ENTRIES: list[tuple[str, Path, str, str]] = [
    # slug, path, title, nav group
    ("overview", _DOCS_ROOT / "overview.md", "Overview", "Start here"),
    (
        "research/comparison_framework",
        _DOCS_ROOT / "research" / "comparison_framework.md",
        "Compare",
        "How to use",
    ),
    ("experiments", _DOCS_ROOT / "experiments.md", "Experiments", "How to use"),
    ("research/netlogo", _DOCS_ROOT / "research" / "netlogo.md", "NetLogo", "How to use"),
    (
        "research/algorithms",
        _DOCS_ROOT / "research" / "algorithms" / "README.md",
        "Instruments",
        "Reference",
    ),
    (
        "research/algorithms/strombom_2014",
        _DOCS_ROOT / "research" / "algorithms" / "strombom_2014.md",
        "Strombom 2014",
        "Reference",
    ),
    (
        "research/algorithms/strombom_multi",
        _DOCS_ROOT / "research" / "algorithms" / "strombom_multi.md",
        "Strombom Multi-Dog",
        "Reference",
    ),
    (
        "research/algorithms/strombom_noise",
        _DOCS_ROOT / "research" / "algorithms" / "strombom_noise.md",
        "Strombom Noise",
        "Reference",
    ),
    (
        "research/algorithms/v_formation",
        _DOCS_ROOT / "research" / "algorithms" / "v_formation.md",
        "V-Formation",
        "Reference",
    ),
    (
        "research/algorithms/heterogeneous",
        _DOCS_ROOT / "research" / "algorithms" / "heterogeneous.md",
        "Heterogeneous",
        "Reference",
    ),
    (
        "research/algorithms/obstacle_aware",
        _DOCS_ROOT / "research" / "algorithms" / "obstacle_aware.md",
        "Obstacle-Aware",
        "Reference",
    ),
    (
        "research/algorithms/kubo_2022",
        _DOCS_ROOT / "research" / "algorithms" / "kubo_2022.md",
        "Kubo 2022",
        "Reference",
    ),
    (
        "research/algorithms/flocking_dog_2024",
        _DOCS_ROOT / "research" / "algorithms" / "flocking_dog_2024.md",
        "Flocking Dog",
        "Reference",
    ),
    (
        "research/algorithms/fat",
        _DOCS_ROOT / "research" / "algorithms" / "fat.md",
        "FAT",
        "Reference",
    ),
    (
        "research/algorithms/communication_free",
        _DOCS_ROOT / "research" / "algorithms" / "communication_free.md",
        "Communication-Free",
        "Reference",
    ),
    (
        "research/algorithms/adaptive",
        _DOCS_ROOT / "research" / "algorithms" / "adaptive.md",
        "Adaptive",
        "Reference",
    ),
    (
        "research/scenarios",
        _DOCS_ROOT / "research" / "scenarios.md",
        "Scenarios",
        "Reference",
    ),
    ("research/metrics", _DOCS_ROOT / "research" / "metrics.md", "Metrics", "Reference"),
    (
        "research/environment",
        _DOCS_ROOT / "research" / "environment.md",
        "Environment",
        "Reference",
    ),
    ("architecture", _DOCS_ROOT / "architecture.md", "Architecture", "For developers"),
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
    return PlainTextResponse(path.read_text(encoding="utf-8"), media_type="text/markdown; charset=utf-8")
