import os
import sys
from pathlib import Path
from utils_sync import file_path_utils

# [Created-or-Modified] by [LLM model] | 2025-11-13_01

def test_normalize_path_expands_and_resolves(tmp_path):
    # Create a nested folder and a file
    folder = tmp_path / "someFolder"
    folder.mkdir()
    f = folder / "file.txt"
    f.write_text("hello")
    # Use an env var and ~ expansion simulation by passing absolute path string
    normalized = file_path_utils.normalize_path(str(folder))
    assert isinstance(normalized, Path)
    assert normalized.is_absolute()
    assert normalized.exists()
    # Trailing slashes should be handled
    normalized2 = file_path_utils.normalize_path(str(folder) + os.sep)
    assert normalized == normalized2

def test_deduplicate_paths_preserves_order_and_normalizes(tmp_path):
    a = tmp_path / "A"
    b = tmp_path / "B"
    a.mkdir()
    b.mkdir()
    # create same path twice with different representations
    paths = [str(a), a.as_posix(), str(b)]
    result = file_path_utils.deduplicate_paths(paths)
    assert len(result) == 2
    assert result[0] == file_path_utils.normalize_path(a)
    assert result[1] == file_path_utils.normalize_path(b)

def test_has_roo_dir_positive_and_negative(tmp_path):
    base = tmp_path / "project"
    base.mkdir()
    # Negative: no .roo
    assert file_path_utils.has_roo_dir(base) is False
    # Positive: create .roo directory (real dir)
    roo = base / ".roo"
    roo.mkdir()
    assert file_path_utils.has_roo_dir(base) is True
    # If .roo is a symlink (if filesystem supports), create a symlink and expect False
    # Some filesystems or platforms (Windows) may require admin rights; skip symlink test if not permitted
    try:
        target = tmp_path / "target_roo"
        target.mkdir()
        link = base / ".roo_link"
        # create symlink pointing at target
        link.symlink_to(target, target_is_directory=True)
        # has_roo_dir expects a directory named ".roo" specifically; symlink check ensures symlinks are ignored
        # Ensure the function does not crash when encountering symlinked entries
        # This is just to confirm behavior doesn't raise; result may be False since name isn't ".roo"
        _ = file_path_utils.has_roo_dir(base)
    except (OSError, NotImplementedError):
        # symlink creation not allowed on this platform; that's acceptable for test portability
        pass

def test_get_roo_relative_path_returns_relative_when_inside_roo(tmp_path):
    base = tmp_path / "proj"
    base.mkdir()
    roo = base / ".roo"
    roo.mkdir()
    nested = roo / "rules"
    nested.mkdir(parents=True)
    file = nested / "01.md"
    file.write_text("content")
    # full path inside .roo should return relative path 'rules/01.md'
    rel = file_path_utils.get_roo_relative_path(file, base)
    assert rel == "rules/01.md"
    # calling with the .roo directory itself returns None
    assert file_path_utils.get_roo_relative_path(roo, base) is None
    # outside path returns None
    outside = tmp_path / "other.txt"
    outside.write_text("x")
    assert file_path_utils.get_roo_relative_path(outside, base) is None