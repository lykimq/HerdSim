"""API router for scenario discovery."""

from fastapi import APIRouter

from scenarios.registry import scenario_registry

router = APIRouter()


@router.get("")
@router.get("/")
def list_scenarios():
    """List all available simulation scenarios."""
    return scenario_registry.list_all()
