"""API router for managing simulation sessions."""

from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from api.session_manager import session_manager
from core.experiment_config import resolve_experiment_config
from core.presets import get_preset
from core.simulation_runner import SimulationRunner
from metrics.registry import metric_registry
from scenarios.registry import scenario_registry

router = APIRouter()


class CreateSessionRequest(BaseModel):
    algorithm_id: Optional[str] = None
    instrument: Optional[str] = None
    scenario_id: str = "drive_to_goal"
    preset: str = Field(default="paper", pattern="^(paper|scenario|custom)$")
    num_sheep: Optional[int] = Field(default=None, ge=1, le=200)
    num_shepherds: Optional[int] = Field(default=None, ge=0, le=10)
    seed: Optional[int] = 42
    algorithm_params: Optional[dict[str, Any]] = None
    world_overrides: Optional[dict[str, Any]] = None
    sheep_model: Optional[str] = None
    dog_controller: Optional[str] = None
    obs_mode: Optional[str] = None


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
    instrument = req.instrument or req.algorithm_id or "strombom"
    try:
        get_preset(instrument)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        scenario = scenario_registry.get(req.scenario_id)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    params = dict(req.algorithm_params or {})
    if req.obs_mode:
        params["obs_mode"] = req.obs_mode

    try:
        config = resolve_experiment_config(
            scenario=scenario,
            instrument=instrument,
            preset=req.preset,
            num_sheep=req.num_sheep,
            num_shepherds=req.num_shepherds,
            algorithm_params=params or None,
            world_overrides=req.world_overrides,
            sheep_model=req.sheep_model,
            dog_controller=req.dog_controller,
        )
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    runner = SimulationRunner(
        scenario=scenario,
        metrics=metric_registry.get_all(),
        config=config,
        seed=req.seed if req.seed is not None else 42,
        instrument=instrument,
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
        "algorithm_id": instrument,
        "instrument": instrument,
        "sheep_model": config.get("sheep_model"),
        "dog_controller": config.get("dog_controller"),
        "obs_mode": config.get("obs_mode"),
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
    return session_manager.list_sessions()


@router.get("/{session_id}")
def get_session_status(session_id: str):
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
    session_manager.remove_session(session_id)
    return {"status": "deleted", "session_id": session_id}
