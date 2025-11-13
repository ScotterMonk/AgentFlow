# Plan: Root-Level File Allowlist for File Sync

Plan Name: 251113_roomodes_allowlist
Log File: plan_251113_roomodes_allowlist_log.md
User Query File: plan_20251113_190141_251113_roomodes_allowlist_user.md
Autonomy Level: High
Testing Type: Use pytest

## Overview
Add opt-in support for syncing specific root-level files (like `.roomodes`) alongside `.roo` directory contents while maintaining strict safety boundaries.

## Goal
Enable selective inclusion of root-level files in sync operations through a configurable allowlist while preserving the existing `.roo`-only safety model as the default.

## Safety Principles
- Keep `.roo` presence requirement unchanged
- Default to empty allowlist (safest)
- Only include files explicitly listed in allowlist
- Reject symlinks and non-regular files
- Use synthetic relative paths to avoid collisions

## Architecture

flowchart TD
    A[Scan starts] --> B[Validate .roo exists]
    B -->|pass| C[Scan .roo subtree]
    B -->|fail| X[Skip folder]
    C --> D[Check root_allowlist config]
    D -->|empty| E[Complete scan]
    D -->|has entries| F[Attempt include allowlisted files]
    F --> G[Validate each: exists, is_file, not symlink]
    G --> H[Add to index with synthetic key]
    H --> E
    E --> I[Plan and execute actions]

## Tasks

Task 01: Add root_allowlist config support
Mode hint: /code-monkey
Action: Modify `utils_sync/config_sync.py` to add `root_allowlist` configuration key with default empty list.
Update DEFAULTS dict:
```python
DEFAULTS = {
    # ... existing keys ...
    "root_allowlist": [],  # comma-separated list of root-level files to sync
}
```
Update load_config to parse root_allowlist as comma-separated list (similar to ignore_patterns):
```python
elif key == "root_allowlist":
    parts: List[str] = [p.strip() for p in val.split(",") if p.strip()]
    config[key] = parts
```
Ensure save_config handles list properly (already supports lists).

Task 02: Add scan logic for allowlisted root files
Mode hint: /code
Action: Modify `utils_sync/sync_core.py` scan_folders method to include allowlisted root files after scanning `.roo` directory.
Add new logic at end of folder loop (after line 117, before return):
```python
# After scanning .roo, attempt to include root-level allowlisted files
root_allowlist = self.config.get("root_allowlist", [])
for allowlist_entry in root_allowlist:
    candidate_path = folder / allowlist_entry
    # Include only if: exists, is_file, not symlink
    if (candidate_path.exists() and 
        candidate_path.is_file() and 
        not candidate_path.is_symlink()):
        stats = candidate_path.stat()
        # Use synthetic relative key = filename only
        synthetic_key = allowlist_entry
        self._emit_event(
            EventType.SCAN_FILE,
            folder=str(folder),
            file_path=synthetic_key,
            message=f"Scanning allowlisted root file: {synthetic_key}"
        )
        file_index[synthetic_key].append({
            "path": candidate_path,
            "mtime": stats.st_mtime,
            "size": stats.st_size,
            "base_folder": folder
        })
```
Safety checks: path.exists(), path.is_file(), not path.is_symlink().

Task 03: Update default config.txt
Mode hint: /task-simple
Action: Add `root_allowlist` entry to `config.txt` with empty default and comment.
Add after line 7:
```
# comma-separated list of root-level files to sync (e.g., .roomodes)
root_allowlist=
```

Task 04: Update README-file-sync.md documentation
Mode hint: /task-simple
Action: Add documentation for root_allowlist feature in `README-file-sync.md`.
Add new section after "Configuration" section (around line 90):
```markdown
### Root-Level File Allowlist

By default, only files within the `.roo` directory are synced. You can optionally include specific root-level files (files that live next to `.roo` at the project root) by adding them to the `root_allowlist` configuration.

Example in config.txt:
```
root_allowlist=.roomodes
```

Multiple files:
```
root_allowlist=.roomodes,.gitignore
```

Safety guarantees:
- Files must exist and be regular files (not symlinks or directories)
- Files are referenced using synthetic relative paths (just the filename)
- The `.roo` directory requirement is unchanged
- Default is empty (no root files included)
```

Task 05: Update Configuration section in README
Mode hint: /task-simple
Action: Add root_allowlist to the configuration example in `README-file-sync.md` around line 80.
Add to config example:
```
# comma-separated list of root-level files to sync
root_allowlist=
```

Task 06: Update Behavior section in README
Mode hint: /task-simple
Action: Update the "Scope" bullet point in "Behavior and guarantees" section (around line 94) to mention root_allowlist option.
Change:
```markdown
- Scope: By default, only the `.roo` subtree of each folder is scanned and synced
```
To:
```markdown
- Scope: By default, only the `.roo` subtree of each folder is scanned and synced. Optionally, specific root-level files can be included via `root_allowlist` configuration
```

Task 07: Add pytest test for root_allowlist config loading
Mode hint: /tester
Action: Add test to `tests/test_config_sync.py` to verify root_allowlist is loaded correctly as a list.
Add new test function:
```python
def test_load_config_with_root_allowlist(tmp_path):
    cfg_file = tmp_path / "config.txt"
    cfg_file.write_text("root_allowlist=.roomodes,.gitignore\n")
    cfg = config_sync.load_config(str(cfg_file))
    assert isinstance(cfg["root_allowlist"], list)
    assert ".roomodes" in cfg["root_allowlist"]
    assert ".gitignore" in cfg["root_allowlist"]
    assert len(cfg["root_allowlist"]) == 2
```

Task 08: Add pytest test for scanning allowlisted root files
Mode hint: /tester
Action: Add test to `tests/test_sync_core.py` to verify allowlisted root files are included in scan.
Add new test function:
```python
def test_scan_folders_includes_root_allowlist_files(tmp_path):
    # Setup: create folder with .roo and root-level .roomodes file
    base = tmp_path / "project"
    base.mkdir()
    (base / ".roo").mkdir()
    (base / ".roo" / "rules" / "01.md").parent.mkdir(parents=True)
    (base / ".roo" / "rules" / "01.md").write_text("content")
    (base / ".roomodes").write_text("mode content")
    
    # Configure engine with root_allowlist
    q = queue.Queue()
    config = {"ignore_patterns": [], "root_allowlist": [".roomodes"]}
    engine = SyncEngine(config, q)
    
    # Scan and verify .roomodes is included with synthetic key
    index = engine.scan_folders([base])
    assert ".roomodes" in index
    assert len(index[".roomodes"]) == 1
    assert index[".roomodes"][0]["path"] == base / ".roomodes"
```

Task 09: Add pytest test for root_allowlist safety checks
Mode hint: /tester
Action: Add test to `tests/test_sync_core.py` to verify symlinks and non-files are rejected.
Add new test function:
```python
def test_scan_folders_rejects_symlinks_in_allowlist(tmp_path):
    # Setup
    base = tmp_path / "project"
    base.mkdir()
    (base / ".roo").mkdir()
    
    # Create a symlink (if platform supports it)
    try:
        target = tmp_path / "target.txt"
        target.write_text("target")
        symlink = base / ".roomodes"
        symlink.symlink_to(target)
        
        # Configure and scan
        q = queue.Queue()
        config = {"ignore_patterns": [], "root_allowlist": [".roomodes"]}
        engine = SyncEngine(config, q)
        index = engine.scan_folders([base])
        
        # Verify symlink was NOT included
        assert ".roomodes" not in index or len(index[".roomodes"]) == 0
    except (OSError, NotImplementedError):
        # Platform doesn't support symlinks, skip test
        pass
```