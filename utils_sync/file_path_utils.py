# [Created-or-Modified] by [LLM model] | 2025-11-13_01
"""
utils_sync.file_path_utils

Utilities for normalizing file system paths and deduplicating path lists.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Union, Iterable, List, Optional


# Basic utilities for path handling used by file-sync tasks.


def normalize_path(p: Union[str, Path]) -> Path:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """Return an absolute, canonical Path.

    - Expands environment variables and ~.
    - Resolves symlinks where possible without failing on missing files.
    - Returns a pathlib.Path that is absolute.

    Raises:
        ValueError: For invalid input types or empty strings.
    """
    if p is None:
        raise ValueError("p must not be None")
    if isinstance(p, Path):
        s = str(p)
    elif isinstance(p, str):
        s = p
    else:
        raise ValueError("p must be a str or pathlib.Path")
    s = s.strip()
    if not s:
        raise ValueError("p must not be empty")
    # Expand env vars and user (~)
    expanded = os.path.expandvars(os.path.expanduser(s))
    # Try to resolve symlinks safely; strict=False avoids raising on missing targets.
    try:
        resolved = Path(expanded).resolve(strict=False)
    except Exception:
        # Fallback to absolute path if resolve fails for any reason.
        resolved = Path(os.path.abspath(expanded))
    return resolved


def deduplicate_paths(paths: Iterable[Union[str, Path]]) -> List[Path]:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """Normalize and deduplicate an iterable of paths, preserving insertion order.

    Returns a list of resolved Path objects (first occurrence kept).
    """
    if paths is None:
        raise ValueError("paths must not be None")
    seen = set()
    out: List[Path] = []
    for item in paths:
        np = normalize_path(item)
        key = str(np)
        if key not in seen:
            seen.add(key)
            out.append(np)
    return out


def ensure_folder(path: Union[str, Path]) -> Path:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """Ensure a folder exists at the given path; create it if necessary.

    Returns the normalized Path to the folder.
    """
    if path is None:
        raise ValueError("path must not be None")
    p = normalize_path(path)
    # If path exists and is a file, raise.
    if p.exists() and not p.is_dir():
        raise ValueError(f"Path exists and is not a directory: {p}")
    # Create directory if missing.
    p.mkdir(parents=True, exist_ok=True)
    return p

def has_roo_dir(folder_path: Union[str, Path]) -> bool:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """
    Return True if a `.roo` directory exists directly under the provided folder_path.

    - Accepts str or Path.
    - Normalizes path using normalize_path().
    - Returns False if folder_path doesn't exist or is not a directory.
    - Treats a symlinked `.roo` as absent (symlinks are ignored).
    """
    if folder_path is None:
        raise ValueError("folder_path must not be None")
    # normalize_path will raise ValueError for empty/invalid inputs.
    base = normalize_path(folder_path)
    # If base doesn't exist or is not a directory, no .roo can be present.
    if not base.exists() or not base.is_dir():
        return False
    candidate = base / ".roo"
    # Treat symlinked `.roo` as absent: require it be a real directory and not a symlink.
    return candidate.exists() and candidate.is_dir() and not candidate.is_symlink()


# [Created-or-Modified] by [LLM model] | 2025-11-13_01
def get_roo_relative_path(full_path: Union[str, Path], base_folder: Union[str, Path]) -> Optional[str]:
    """
    If `full_path` is inside `<base_folder>/.roo/`, return the path relative to that `.roo/` directory
    as a POSIX-style string (no leading slash), e.g. "rules/01.md".
    If not under `<base_folder>/.roo/`, return None.

    Behavior:
    - Accepts strings or pathlib.Path.
    - Uses normalize_path() to resolve inputs.
    - Ensures `.roo` must be a normal directory (not a symlink) under base_folder.
    - Handles case where full_path equals the `.roo` directory or is the directory itself (return None).
    - Returns None for invalid inputs (or raise ValueError for clearly invalid inputs like empty strings).
    """
    if full_path is None:
        raise ValueError("full_path must not be None")
    if base_folder is None:
        raise ValueError("base_folder must not be None")

    # Normalize inputs using existing utility
    fp = normalize_path(full_path)
    base = normalize_path(base_folder)

    roo_dir = base / ".roo"

    # Require .roo to exist as a real directory and not be a symlink.
    if not roo_dir.exists() or not roo_dir.is_dir() or roo_dir.is_symlink():
        return None

    # If the provided path equals the .roo directory itself, return None.
    if fp == roo_dir:
        return None

    # If full path is inside roo_dir, compute relative path.
    try:
        rel = fp.relative_to(roo_dir)
    except Exception:
        return None

    # Return as POSIX-style string with no leading slash.
    return rel.as_posix()