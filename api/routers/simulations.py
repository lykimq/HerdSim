"""API router for managing simulation sessions."""

from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from algorithms.registry import algorithm_registry
from api.session_manager import session_manager
from core.experiment_config import resolve_experiment_config
from core.simulation_runner import SimulationRunner
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry

router = APIRouter()


class CreateSessionRequest(BaseModel):
    algorithm_id: str = "strombom"
    scenario_id: str = "drive_to_goal"
    preset: str = Field(default="paper", pattern="^(paper|scenario|custom)$")
    num_sheep: Optional[int] = Field(default=None, ge=1, le=200)
    num_shepherds: Optional[int] = Field(default=None, ge=1, le=10)
    seed: Optional[int] = 42
    algorithm_params: Optional[dict[str, Any]] = None
    world_overrides: Optional[dict[str, Any]] = None


def _world_payload(runner: SimulationRunner) -> dict[str, Any]:
    state = runner.state
    if state is None:
        return {}
    world = state.world
    goal = world.goal
    return {
        "width": world.width,
        "height": world.height,
        "goal_center": goal.center.tolist() if goal is not None else None,
        "goal_radius": goal.radius if goal is not None else None,
        "obstacles": [
            {
                "min_corner": obs.min_corner.tolist(),
                "max_corner": obs.max_corner.tolist(),
            }
            for obs in world.obstacles
        ],
    }


@router.post("")
@router.post("/")
def create_session(req: CreateSessionRequest):
    """Create and initialize a new simulation session."""
    try:
        algorithm = algorithm_registry.get(req.algorithm_id)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        scenario = scenario_registry.get(req.scenario_id)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        config = resolve_experiment_config(
            algorithm,
            scenario,
            preset=req.preset,
            num_sheep=req.num_sheep,
            num_shepherds=req.num_shepherds,
            algorithm_params=req.algorithm_params,
            world_overrides=req.world_overrides,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    runner = SimulationRunner(
        algorithm=algorithm,
        scenario=scenario,
        metrics=metric_registry.get_all(),
        config=config,
        seed=req.seed if req.seed is not None else 42,
    )

    session_id = session_manager.create_session(runner)
    state = runner.state
    return {
        "session_id": session_id,
        "status": "initialized",
        "preset": req.preset,
        "num_sheep": config["n_sheep"],
        "num_shepherds": config["n_shepherds"],
        "seed": runner.seed,
        "algorithm_id": req.algorithm_id,
        "scenario_id": req.scenario_id,
        "config": config,
        "world": _world_payload(runner),
        "sheep_positions": state.sheep_positions.tolist() if state else [],
        "shepherd_positions": state.shepherd_positions.tolist() if state else [],
        "tick": state.tick if state else 0,
    }


@router.get("")
@router.get("/")
def list_sessions():
    """List all active simulation sessions."""
    return session_manager.list_sessions()


@router.get("/{session_id}")
def get_session_status(session_id: str):
    """Get status and current state of a session."""
    try:
        session = session_manager.get_session(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    state = session.runner.state
    return {
        "session_id": session.session_id,
        "status": session.status,
        "tick": state.tick if state else 0,
        "seed": session.runner.seed,
        "world": _world_payload(session.runner),
    }


@router.delete("/{session_id}")
def delete_session(session_id: str):
    """Terminate and remove a session."""
    session_manager.remove_session(session_id)
    return {"status": "deleted", "session_id": session_id}
