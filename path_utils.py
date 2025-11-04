"""Utility helpers for resolving project paths in a cross-platform way."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "config.ini"

# Allow overriding the base directory (e.g. when data is stored elsewhere)
_ENV_BASE = os.getenv("WEB_ANNOTATION_DATA_ROOT")
if _ENV_BASE:
    BASE_PATH = Path(_ENV_BASE).expanduser().resolve()
else:
    BASE_PATH = PROJECT_ROOT


def resolve_path(path_like: Union[str, Path]) -> Path:
    """Resolve a user/config supplied path to an absolute Path."""
    path = Path(path_like)
    if not path.is_absolute():
        path = BASE_PATH / path
    return path.resolve()


def ensure_directory(path_like: Union[str, Path]) -> Path:
    """Ensure the directory exists and return its absolute Path."""
    directory = resolve_path(path_like)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def as_config_path(path_like: Union[str, Path]) -> str:
    """
    Convert a filesystem path into a string suitable for storing in config.

    Preference is given to paths relative to BASE_PATH to keep config portable.
    """
    path = resolve_path(path_like)
    try:
        relative = path.relative_to(BASE_PATH)
        return relative.as_posix()
    except ValueError:
        return path.as_posix()


def static_root() -> Path:
    """Return the absolute path of the static assets directory."""
    return (BASE_PATH / "statics").resolve()


def static_path(relative: Union[str, Path]) -> Path:
    """Return absolute path inside the static assets directory."""
    return (static_root() / relative).resolve()
