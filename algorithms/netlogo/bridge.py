"""Helpers for locating NetLogo installs and model files."""

from __future__ import annotations

import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _looks_like_netlogo_home(path: Path) -> bool:
    """True if path contains a NetLogo application jar."""
    if not path.is_dir():
        return False
    app = path / "lib" / "app"
    if not app.is_dir():
        return False
    return any(app.glob("netlogo*.jar")) or (app / "NetLogo.jar").is_file()


def find_netlogo_home() -> str | None:
    """Locate a NetLogo install.

    Order: NETLOGO_HOME, then common user/system directories.
    """
    env = os.environ.get("NETLOGO_HOME", "").strip()
    if env:
        candidate = Path(env).expanduser()
        if _looks_like_netlogo_home(candidate):
            return str(candidate.resolve())

    home = Path.home()
    search_roots = [
        home / ".local" / "share",
        home,
        Path("/opt"),
        Path("/usr/local/share"),
        Path("/usr/share"),
    ]
    for root in search_roots:
        if not root.is_dir():
            continue
        try:
            children = sorted(root.iterdir(), key=lambda p: p.name, reverse=True)
        except OSError:
            continue
        for child in children:
            name = child.name.lower()
            if "netlogo" not in name:
                continue
            if _looks_like_netlogo_home(child):
                return str(child.resolve())
    return None


def find_netlogo_gui_launcher(netlogo_home: str | Path | None = None) -> Path | None:
    """Return the desktop NetLogo executable for opening models in a GUI window."""
    home = Path(netlogo_home) if netlogo_home else None
    if home is None:
        detected = find_netlogo_home()
        if not detected:
            return None
        home = Path(detected)
    if not home.is_dir():
        return None

    candidates = [
        home / "NetLogo",
        home / "bin" / "NetLogo",
        home / "netlogo-gui.sh",
        home / "NetLogo.exe",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def resolve_model_path(model_file: str) -> Path:
    """Resolve a model path relative to the repo root, then the process cwd."""
    path = Path(model_file).expanduser()
    if path.is_absolute():
        return path
    repo_candidate = _REPO_ROOT / path
    if repo_candidate.is_file():
        return repo_candidate.resolve()
    cwd_candidate = Path.cwd() / path
    if cwd_candidate.is_file():
        return cwd_candidate.resolve()
    return repo_candidate.resolve()
