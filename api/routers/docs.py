"""Serve curated documentation markdown for the Guide tab."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter()

_DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs"

# Whitelist served by Guide; titles come from list_docs().
DOC_SLUGS: dict[str, Path] = {
    "user_guide": _DOCS_ROOT / "user_guide.md",
    "research/algorithms": _DOCS_ROOT / "research" / "algorithms" / "README.md",
    "research/algorithms/strombom_2014": _DOCS_ROOT / "research" / "algorithms" / "strombom_2014.md",
    "research/algorithms/strombom_multi": _DOCS_ROOT / "research" / "algorithms" / "strombom_multi.md",
    "research/algorithms/strombom_noise": _DOCS_ROOT / "research" / "algorithms" / "strombom_noise.md",
    "research/algorithms/v_formation": _DOCS_ROOT / "research" / "algorithms" / "v_formation.md",
    "research/algorithms/heterogeneous": _DOCS_ROOT / "research" / "algorithms" / "heterogeneous.md",
    "research/algorithms/obstacle_aware": _DOCS_ROOT / "research" / "algorithms" / "obstacle_aware.md",
    "research/algorithms/kubo_2022": _DOCS_ROOT / "research" / "algorithms" / "kubo_2022.md",
    "research/algorithms/flocking_dog_2024": _DOCS_ROOT / "research" / "algorithms" / "flocking_dog_2024.md",
    "research/algorithms/fat": _DOCS_ROOT / "research" / "algorithms" / "fat.md",
    "research/algorithms/communication_free": _DOCS_ROOT / "research" / "algorithms" / "communication_free.md",
    "research/algorithms/adaptive": _DOCS_ROOT / "research" / "algorithms" / "adaptive.md",
    "research/scenarios": _DOCS_ROOT / "research" / "scenarios.md",
    "research/metrics": _DOCS_ROOT / "research" / "metrics.md",
    "research/environment": _DOCS_ROOT / "research" / "environment.md",
    "research/netlogo": _DOCS_ROOT / "research" / "netlogo.md",
    "research/comparison_framework": _DOCS_ROOT / "research" / "comparison_framework.md",
    "architecture": _DOCS_ROOT / "architecture.md",
}


@router.get("")
async def list_docs():
    """List Guide-visible documentation slugs."""
    title_map = {
        "user_guide": "User Guide",
        "research/algorithms": "Instruments",
        "research/algorithms/strombom_2014": "Strombom 2014",
        "research/algorithms/strombom_multi": "Strombom Multi-Dog",
        "research/algorithms/strombom_noise": "Strombom Noise",
        "research/algorithms/v_formation": "V-Formation",
        "research/algorithms/heterogeneous": "Heterogeneous",
        "research/algorithms/obstacle_aware": "Obstacle-Aware",
        "research/algorithms/kubo_2022": "Kubo 2022",
        "research/algorithms/flocking_dog_2024": "Flocking Dog",
        "research/algorithms/fat": "FAT",
        "research/algorithms/communication_free": "Communication-Free",
        "research/algorithms/adaptive": "Adaptive",
        "research/scenarios": "Scenarios",
        "research/metrics": "Metrics",
        "research/environment": "Environment",
        "research/netlogo": "NetLogo",
        "research/comparison_framework": "Comparison Framework",
        "architecture": "Architecture",
    }
    items = []
    for slug, path in DOC_SLUGS.items():
        items.append(
            {
                "slug": slug,
                "exists": path.is_file(),
                "title": title_map.get(slug, slug.split("/")[-1]),
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
