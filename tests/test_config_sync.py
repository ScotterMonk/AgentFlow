import os
from utils_sync import config_sync

# [Created-or-Modified] by [LLM model] | 2025-11-13_01

def test_load_config_defaults(tmp_path):
    # Point to a non-existent config file to force defaults
    cfg_path = tmp_path / "no_config.txt"
    assert not cfg_path.exists()
    cfg = config_sync.load_config(str(cfg_path))
    # Defaults present and typed
    assert isinstance(cfg, dict)
    assert cfg.get("window_width") == config_sync.DEFAULTS["window_width"]
    assert cfg.get("window_height") == config_sync.DEFAULTS["window_height"]
    assert isinstance(cfg.get("ignore_patterns"), list)
    assert "node_modules" in cfg.get("ignore_patterns")

def test_save_and_load_config(tmp_path):
    cfg_file = tmp_path / "config.txt"
    # Create a config with various types
    config_in = {
        "window_width": 900,
        "window_height": 700,
        "ignore_patterns": [".git", "build", "__pycache__"],
        "backup_mode": "none",
        "preserve_mtime": False,
        "dry_run": True,
        "custom_value": "hello"
    }
    # Save should return True and create the file
    ok = config_sync.save_config(config_in, path=str(cfg_file))
    assert ok is True
    assert cfg_file.exists()

    # Load and verify values are parsed and typed
    loaded = config_sync.load_config(str(cfg_file))
    assert loaded["window_width"] == 900
    assert loaded["window_height"] == 700
    assert loaded["preserve_mtime"] is False
    assert loaded["dry_run"] is True
    assert loaded["backup_mode"] == "none"
    assert loaded["custom_value"] == "hello"
    # ignore_patterns should be a list and contain items we set
    assert isinstance(loaded["ignore_patterns"], list)
    assert "build" in loaded["ignore_patterns"]

import pytest

# [Created-or-Modified] by tester | 2025-11-13_1
def test_root_allowlist_parsing(tmp_path):
    """
    Test that root_allowlist config is correctly parsed from config file.
    """
    # Test 1: Verify root_allowlist with explicit value
    cfg_file = tmp_path / "config_test1.txt"
    cfg_file.write_text("root_allowlist=.roomodes\n", encoding="utf-8")
    cfg = config_sync.load_config(str(cfg_file))
    assert isinstance(cfg["root_allowlist"], list)
    assert cfg["root_allowlist"] == [".roomodes"]
    
    # Test 2: Verify root_allowlist with multiple values
    cfg_file2 = tmp_path / "config_test2.txt"
    cfg_file2.write_text("root_allowlist=.roomodes,.gitignore,README.md\n", encoding="utf-8")
    cfg2 = config_sync.load_config(str(cfg_file2))
    assert isinstance(cfg2["root_allowlist"], list)
    assert ".roomodes" in cfg2["root_allowlist"]
    assert ".gitignore" in cfg2["root_allowlist"]
    assert "README.md" in cfg2["root_allowlist"]
    assert len(cfg2["root_allowlist"]) == 3
    
    # Test 3: Verify default behavior (empty list when not specified)
    cfg_file3 = tmp_path / "config_test3.txt"
    cfg_file3.write_text("window_width=800\n", encoding="utf-8")
    cfg3 = config_sync.load_config(str(cfg_file3))
    assert isinstance(cfg3["root_allowlist"], list)
    assert cfg3["root_allowlist"] == []


# [Created-or-Modified] by Claude Sonnet 4.5 | 2025-11-15_01
def test_folders_faves_parsing_list(tmp_path):
    """
    Test that folders_faves config is correctly parsed as a list from config file.
    """
    cfg_file = tmp_path / "config_faves_test1.txt"
    cfg_file.write_text("folders_faves=/one,/two,/three\n", encoding="utf-8")
    cfg = config_sync.load_config(str(cfg_file))
    assert isinstance(cfg["folders_faves"], list)
    assert cfg["folders_faves"] == ["/one", "/two", "/three"]

def test_folders_faves_missing_defaults_to_empty(tmp_path):
    """
    Test that folders_faves defaults to empty list when not specified in config.
    """
    cfg_file = tmp_path / "no_faves_config.txt"
    # Point to non-existent file to get defaults
    cfg = config_sync.load_config(str(cfg_file))
    assert isinstance(cfg.get("folders_faves"), list)
    assert cfg.get("folders_faves") == config_sync.DEFAULTS["folders_faves"]
    assert cfg.get("folders_faves") == []

def test_folders_faves_round_trip(tmp_path):
    """
    Test that folders_faves can be saved and loaded correctly (round-trip).
    """
    cfg_file = tmp_path / "config_roundtrip.txt"
    # Create config with folders_faves
    cfg_in = {
        "folders_faves": ["/a", "/b"],
        "ignore_patterns": [],
        "backup_mode": "none"
    }
    # Save config
    ok = config_sync.save_config(cfg_in, path=str(cfg_file))
    assert ok is True
    assert cfg_file.exists()
    # Reload and verify
    reloaded = config_sync.load_config(str(cfg_file))
    assert isinstance(reloaded["folders_faves"], list)
    assert reloaded["folders_faves"] == ["/a", "/b"]
def test_comma_space_parsing_for_lists(tmp_path):
    # [Created-or-Modified] by Claude Sonnet 4.5 | 2025-11-15_02
    """
    Config list values should parse correctly when values are separated by ', '.
    """
    cfg_file = tmp_path / "config_comma_space.txt"
    cfg_file.write_text(
        "ignore_patterns=.git, build, __pycache__\n"
        "root_allowlist=.roomodes, .gitignore, README.md\n"
        "folders_faves=/one, /two, /three\n",
        encoding="utf-8",
    )
    cfg = config_sync.load_config(str(cfg_file))
    assert isinstance(cfg["ignore_patterns"], list)
    assert isinstance(cfg["root_allowlist"], list)
    assert isinstance(cfg["folders_faves"], list)
    assert cfg["ignore_patterns"] == [".git", "build", "__pycache__"]
    assert cfg["root_allowlist"] == [".roomodes", ".gitignore", "README.md"]
    assert cfg["folders_faves"] == ["/one", "/two", "/three"]


def test_save_config_uses_comma_space_for_lists(tmp_path):
    # [Created-or-Modified] by Claude Sonnet 4.5 | 2025-11-15_02
    """
    save_config should serialize list values using ', ' between items.
    """
    cfg_file = tmp_path / "config_pretty_lists.txt"
    config_in = {
        "ignore_patterns": [".git", "build", "__pycache__"],
        "root_allowlist": [".roomodes", "README.md"],
        "folders_faves": ["/one", "/two"],
        "backup_mode": "none",
    }
    ok = config_sync.save_config(config_in, path=str(cfg_file))
    assert ok is True
    text = cfg_file.read_text(encoding="utf-8")
    assert "ignore_patterns=.git, build, __pycache__" in text
    assert "root_allowlist=.roomodes, README.md" in text
    assert "folders_faves=/one, /two" in text

