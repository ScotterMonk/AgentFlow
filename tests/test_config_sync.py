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
    assert cfg.get("include_roo_only") is True
    assert isinstance(cfg.get("ignore_patterns"), list)
    assert "node_modules" in cfg.get("ignore_patterns")

def test_save_and_load_config(tmp_path):
    cfg_file = tmp_path / "config.txt"
    # Create a config with various types
    config_in = {
        "window_width": 900,
        "window_height": 700,
        "include_roo_only": False,
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
    assert loaded["include_roo_only"] is False
    assert loaded["preserve_mtime"] is False
    assert loaded["dry_run"] is True
    assert loaded["backup_mode"] == "none"
    assert loaded["custom_value"] == "hello"
    # ignore_patterns should be a list and contain items we set
    assert isinstance(loaded["ignore_patterns"], list)
    assert "build" in loaded["ignore_patterns"]