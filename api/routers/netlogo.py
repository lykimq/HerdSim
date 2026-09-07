"""API for NetLogo model discovery, uploads, and desktop launch."""

from __future__ import annotations

import json
import logging
import re
import subprocess
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from algorithms.netlogo.bridge import (
    find_netlogo_gui_launcher,
    find_netlogo_home,
    resolve_model_path,
)

router = APIRouter()
logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MODELS_ROOT = _REPO_ROOT / "netlogo" / "models"
_UPLOADS_ROOT = _MODELS_ROOT / "uploads"
_MAX_UPLOAD_BYTES = 5 * 1024 * 1024
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}\.nlogo$")


def _ensure_dirs() -> None:
    _MODELS_ROOT.mkdir(parents=True, exist_ok=True)
    _UPLOADS_ROOT.mkdir(parents=True, exist_ok=True)


def _rel_model_path(path: Path) -> str:
    return path.resolve().relative_to(_REPO_ROOT.resolve()).as_posix()


def _model_entry(path: Path, source: str) -> dict:
    return {
        "id": _rel_model_path(path),
        "name": path.name,
        "path": _rel_model_path(path),
        "source": source,
        "size_bytes": path.stat().st_size,
    }


def _list_nlogo(directory: Path, source: str) -> list[dict]:
    if not directory.is_dir():
        return []
    entries = []
    for path in sorted(directory.glob("*.nlogo")):
        if path.is_file():
            entries.append(_model_entry(path, source))
    return entries


def _resolve_allowed_model(model_file: str) -> Path:
    """Resolve a model path and require it to live under netlogo/models/."""
    path = resolve_model_path(model_file).resolve()
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Model not found: {model_file}")
    if path.suffix.lower() != ".nlogo":
        raise HTTPException(status_code=400, detail="Only .nlogo files can be opened.")
    try:
        path.relative_to(_MODELS_ROOT.resolve())
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Model must be under netlogo/models/ (bundled or uploads).",
        ) from exc
    return path


class OpenDesktopRequest(BaseModel):
    model_file: str = Field(..., min_length=1)
    netlogo_home: str | None = None


_TWINS_PATH = _REPO_ROOT / "netlogo" / "twins.json"


def _load_twins() -> list[dict]:
    if not _TWINS_PATH.is_file():
        return []
    with _TWINS_PATH.open(encoding="utf-8") as fh:
        raw = json.load(fh)
    if not isinstance(raw, list):
        return []
    twins = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        algorithm_id = str(item.get("algorithm_id", "")).strip()
        model_file = str(item.get("model_file", "")).strip()
        if not algorithm_id or not model_file:
            continue
        path = resolve_model_path(model_file)
        if not path.is_file():
            continue
        twins.append(
            {
                "algorithm_id": algorithm_id,
                "name": str(item.get("name") or algorithm_id),
                "model_file": _rel_model_path(path),
                "description": str(item.get("description") or ""),
                "size_bytes": path.stat().st_size,
            }
        )
    return twins


@router.get("/twins")
def list_twins():
    """List HerdSim algorithms that have a NetLogo twin model."""
    return {"twins": _load_twins()}


@router.get("/status")
def netlogo_status():
    """Report whether a NetLogo install / GUI launcher can be auto-detected."""
    home = find_netlogo_home()
    launcher = find_netlogo_gui_launcher(home)
    return {
        "netlogo_home": home,
        "detected": home is not None,
        "gui_available": launcher is not None,
        "gui_launcher": str(launcher) if launcher else None,
        "models_dir": _rel_model_path(_MODELS_ROOT)
        if _MODELS_ROOT.is_dir()
        else "netlogo/models",
        "twins_count": len(_load_twins()),
    }


@router.get("/models")
def list_models():
    """List bundled example models and user uploads."""
    _ensure_dirs()
    bundled = _list_nlogo(_MODELS_ROOT, "bundled")
    uploads = _list_nlogo(_UPLOADS_ROOT, "upload")
    return {"models": bundled + uploads}


@router.post("/upload")
async def upload_model(file: UploadFile = File(...)):
    """Save an uploaded .nlogo into netlogo/models/uploads/."""
    _ensure_dirs()
    filename = Path(file.filename or "").name
    if not _SAFE_NAME.match(filename):
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid filename. Use a simple .nlogo name "
                "(letters, numbers, ., _, -)."
            ),
        )

    dest = _UPLOADS_ROOT / filename
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(raw) > _MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large (max {_MAX_UPLOAD_BYTES // (1024 * 1024)} MB).",
        )

    dest.write_bytes(raw)
    return {"model": _model_entry(dest, "upload")}


@router.post("/open")
def open_in_desktop(req: OpenDesktopRequest):
    """Launch the selected model in the local NetLogo desktop GUI."""
    model_path = _resolve_allowed_model(req.model_file)

    home = (req.netlogo_home or "").strip() or find_netlogo_home()
    if not home:
        raise HTTPException(
            status_code=400,
            detail=(
                "NetLogo desktop install not found. Install NetLogo 6.x or set "
                "netlogo_home / NETLOGO_HOME."
            ),
        )

    launcher = find_netlogo_gui_launcher(home)
    if launcher is None:
        raise HTTPException(
            status_code=400,
            detail=f"No NetLogo GUI launcher found under {home}.",
        )

    try:
        subprocess.Popen(  # noqa: S603 - launcher path validated from install tree
            [str(launcher), str(model_path)],
            cwd=str(Path(home)),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError as exc:
        logger.exception("Failed to launch NetLogo GUI")
        raise HTTPException(
            status_code=500,
            detail=f"Could not launch NetLogo: {exc}",
        ) from exc

    return {
        "opened": True,
        "model_file": _rel_model_path(model_path),
        "launcher": str(launcher),
        "netlogo_home": str(Path(home).resolve()),
    }
