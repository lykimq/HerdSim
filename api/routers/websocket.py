"""WebSocket endpoint for real-time simulation streaming and control."""

from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.session_manager import session_manager

router = APIRouter()


def _heading_from_velocity(velocities) -> list[float]:
    import numpy as np

    norms = np.linalg.norm(velocities, axis=1)
    headings = np.zeros(len(velocities), dtype=float)
    moving = norms > 1e-10
    headings[moving] = np.arctan2(velocities[moving, 1], velocities[moving, 0])
    return headings.tolist()


def _frame_payload(runner, status: str, frame_type: str = "tick") -> dict:
    state = runner.state
    if state is None:
        return {"type": frame_type, "status": status, "tick": 0}

    world = state.world
    goal = world.goal
    return {
        "type": frame_type,
        "tick": state.tick,
        "sheep_positions": state.sheep_positions.tolist(),
        "shepherd_positions": state.shepherd_positions.tolist(),
        "sheep_headings": _heading_from_velocity(state.sheep_velocities),
        "shepherd_headings": _heading_from_velocity(state.shepherd_velocities),
        "metrics": runner.recorder.latest() if frame_type == "tick" else {},
        "status": status,
        "seed": runner.seed,
        "world": {
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
        },
    }


@router.websocket("/ws/simulation/{session_id}")
async def simulation_websocket(websocket: WebSocket, session_id: str):
    """Streaming websocket connection for controlling and viewing simulation."""
    await websocket.accept()

    try:
        session = session_manager.get_session(session_id)
    except KeyError:
        await websocket.send_json({"error": f"Session '{session_id}' not found"})
        await websocket.close()
        return

    runner = session.runner
    running = False

    # Send the initialized frame immediately so the UI can render agents.
    await websocket.send_json(_frame_payload(runner, session.status, frame_type="reset"))

    async def run_loop():
        nonlocal running
        while running:
            state, metrics_data, status = runner.step()
            payload = _frame_payload(runner, status, frame_type="tick")
            payload["metrics"] = metrics_data
            await websocket.send_json(payload)

            if status != "running":
                session.status = status
                await websocket.send_json(
                    {
                        "type": "terminated",
                        "status": status,
                        "summary": runner.recorder.get_summary(),
                    }
                )
                running = False
                break

            await asyncio.sleep(0.03 / max(session.speed, 0.1))

    loop_task = None

    try:
        while True:
            text = await websocket.receive_text()
            cmd = json.loads(text)
            action = cmd.get("action")

            if action in ("start", "play"):
                if not running:
                    running = True
                    session.status = "running"
                    loop_task = asyncio.create_task(run_loop())
            elif action == "pause":
                running = False
                session.status = "paused"
                if loop_task:
                    loop_task.cancel()
                    loop_task = None
            elif action == "step":
                # Manual step is not continuous play: stop the run loop and
                # report paused so the UI can keep stepping without Pause.
                running = False
                if loop_task:
                    loop_task.cancel()
                    loop_task = None
                state, metrics_data, status = runner.step()
                if status == "running":
                    session.status = "paused"
                    frame_status = "paused"
                else:
                    session.status = status
                    frame_status = status
                payload = _frame_payload(runner, frame_status, frame_type="tick")
                payload["metrics"] = metrics_data
                await websocket.send_json(payload)
                if status != "running":
                    await websocket.send_json(
                        {
                            "type": "terminated",
                            "status": status,
                            "summary": runner.recorder.get_summary(),
                        }
                    )
            elif action == "reset":
                running = False
                if loop_task:
                    loop_task.cancel()
                    loop_task = None
                runner.initialize()
                session.status = "initialized"
                await websocket.send_json(
                    _frame_payload(runner, session.status, frame_type="reset")
                )
            elif action == "set_speed":
                speed = float(cmd.get("speed", 1.0))
                session.speed = max(0.1, min(10.0, speed))
    except WebSocketDisconnect:
        running = False
        if loop_task:
            loop_task.cancel()
