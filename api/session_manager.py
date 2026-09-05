"""Manages concurrent simulation sessions for the web UI."""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from typing import Any

from core.simulation_runner import SimulationRunner


@dataclass
class SimulationSession:
    session_id: str
    runner: SimulationRunner
    status: str = "initialized"  # initialized | running | paused | completed | timeout
    speed: float = 1.0  # tick delay multiplier


class SessionManager:
    """Thread-safe manager for multiple concurrent simulation sessions."""

    def __init__(self):
        self._sessions: dict[str, SimulationSession] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    def create_session(self, runner: SimulationRunner) -> str:
        session_id = str(uuid.uuid4())[:8]
        self._sessions[session_id] = SimulationSession(
            session_id=session_id, runner=runner
        )
        self._locks[session_id] = asyncio.Lock()
        runner.initialize()
        return session_id

    def get_session(self, session_id: str) -> SimulationSession:
        if session_id not in self._sessions:
            raise KeyError(f"No session '{session_id}'")
        return self._sessions[session_id]

    def remove_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        self._locks.pop(session_id, None)

    def list_sessions(self) -> list[dict[str, Any]]:
        return [
            {"session_id": s.session_id, "status": s.status}
            for s in self._sessions.values()
        ]


session_manager = SessionManager()
