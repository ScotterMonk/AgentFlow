# Plan: AgentFlow File Sync Utility

short plan name: 251113_file_sync
log file: .roo/docs/plans/plan_251113_file_sync_log.md
user query file: .roo/docs/plans/plan_20251113132519_251113_file_sync_user.md
autonomy level: High (rare direction)
testing type: Run py scripts in terminal and pytest

## Overview
Build a standalone Python GUI utility to synchronize files across multiple project directories by comparing modification timestamps and copying newer versions to older locations.
Note: While this utility lives in (and is part of) the AgentFlow project, the goal is about syncing the .roo/ part of AgentFlow with the .roo/ part of other completely separate projects in completely separate locations on the same network.

## Core Objective
Create a modular, user-friendly file sync tool that allows users to:
- Select multiple project folders via GUI
- Automatically identify matching files across folders
- Copy newest versions to all other locations
- Show real-time progress during sync operations

Scope and matching rules:
- Default scope: only the `.roo/` subtree of each selected folder is included
- File identity: relative path under `.roo/` is the key (example: `.roo/rules/01-general.md`)
- Newest wins: source is the file with the latest modification time; ties result in no copy unless content differs
- Exclusions: ignore `.git`, `__pycache__`, `.venv`, `.idea`, `.vscode`, `node_modules`, `*.pyc` by default (configurable)
- Safety: skip symlinks; preserve permissions/mtime where practical; create backups when overwriting targets

## Key Entities
- `config.txt`: Window dimensions and application settings (also ignore patterns, scope flags, backup mode)
- `sync_file.py`: Main tkinter GUI entry point
- `utils_sync/`: Utilities folder for modular components
    - `config_sync.py`: Configuration file handling (load/save/validate)
    - `file_sync_core.py`: File inventory, comparison, and sync engine
    - `file_sync_scanner.py`: Recursive directory scanner (scoped to `.roo/` by default)
    - `file_path_utils.py`: Path normalization and `.roo/`-relative matching helpers
    - `progress_events.py`: Progress event model for thread-safe GUI updates
- Tests:
    - `tests/test_file_sync_core.py`: Unit tests for comparison/copy decisions
    - `tests/test_scanner.py`: Scanner and ignore pattern behavior
    - Note: tests use temporary directories to avoid touching real files

## Constraints
- Build in project root: d:/Dropbox/Projects/AgentFlow
- GUI window: 800x480 (configurable)
- Use tkinter (Python standard library)
- Keep modules under 400 lines
- Use most recent modification date as source of truth; optional hash check as tiebreaker for equal mtimes
- Handle file name collisions safely: atomic replace via temp file + replace; timestamped `.bak` backup when enabled
- Default sync scope: only `.roo/` subtree; other paths require explicit opt-in in config
- Default ignore patterns: `.git`, `__pycache__`, `.venv`, `.idea`, `.vscode`, `node_modules`, `*.pyc` (configurable)
- Robustness: skip symlinks; gracefully handle permission/IO errors and continue; per-folder error reporting

## High Level Phases

### Phase 01: Core Infrastructure & Configuration
Create foundational utilities for configuration management, path handling, and logging.

Task 01: Create default config file with schema
Mode hint: /task-simple
Action: Create `config.txt` in project root with default values:
```
window_width=800
window_height=480
include_roo_only=true
ignore_patterns=.git,__pycache__,.venv,.idea,.vscode,node_modules,*.pyc
backup_mode=timestamped
preserve_mtime=true
dry_run=false
```
Acceptance: File created with all required fields; simple key=value format for easy parsing.

Task 02: Create utils_sync directory structure
Mode hint: /task-simple
Action: Create `utils_sync/` directory at project root and add `__init__.py`.
Acceptance: Directory exists; `__init__.py` created (can be empty for now).

Task 03: Create logs directory
Mode hint: /task-simple
Action: Create `logs/` directory at project root with `.gitignore` containing `*` and `!.gitignore` to track directory but not log files.
Acceptance: Directory created; `.gitignore` prevents logs from being committed.

Task 04: Implement config_sync.py - load function
Mode hint: /code-monkey
Action: Create `utils_sync/config_sync.py` with `load_config(path)` function that parses `config.txt` and returns a dict; handle missing file by returning defaults; validate types (bool parsing, int conversion, list splitting).
```python
def load_config(config_path="config.txt"):
    # Parse key=value lines
    # Convert types: true/false -> bool, numbers -> int, comma-separated -> list
    # Return dict with defaults if file missing or keys absent
```
Acceptance: Returns dict; handles missing file gracefully; type conversions work; ignore_patterns is list.

Task 05: Implement config_sync.py - save function
Mode hint: /code-monkey
Action: Add `save_config(config_dict, path)` function to write config dict back to file; format lists as comma-separated; bools as lowercase true/false.
Acceptance: Writes valid config.txt; load/save round-trip preserves values.

Task 06: Implement file_path_utils.py - normalization
Mode hint: /code-monkey
Action: Create `utils_sync/file_path_utils.py` with functions:
- `normalize_path(path)` -> absolute, resolved, canonical Path object
- `deduplicate_paths(paths)` -> list of unique normalized paths
```python
from pathlib import Path
def normalize_path(p):
    return Path(p).resolve()
def deduplicate_paths(paths):
    return list(set(normalize_path(p) for p in paths))
```
Acceptance: Handles relative paths, resolves symlinks, removes duplicates.

Task 07: Implement file_path_utils.py - .roo/ detection
Mode hint: /code-monkey
Action: Add function `has_roo_dir(folder_path)` that returns True if `.roo/` exists under the given folder.
Acceptance: Returns bool; works for paths with/without trailing slash.

Task 08: Implement file_path_utils.py - relative path helper
Mode hint: /code-monkey
Action: Add function `get_roo_relative_path(full_path, base_folder)` that returns the path relative to `<base_folder>/.roo/` if it's under `.roo/`, else None.
```python
# Example: get_roo_relative_path("/proj/.roo/rules/01.md", "/proj") -> "rules/01.md"
```
Acceptance: Returns relative path string or None; handles edge cases (file not under .roo/).

Task 09: Create progress_events.py - event model
Mode hint: /code-monkey
Action: Create `utils_sync/progress_events.py` with a `ProgressEvent` dataclass or simple class:
```python
from dataclasses import dataclass
from enum import Enum
class EventType(Enum):
    SCAN_START = "scan_start"
    SCAN_FILE = "scan_file"
    COPY = "copy"
    SKIP = "skip"
    ERROR = "error"
    COMPLETE = "complete"

@dataclass
class ProgressEvent:
    event_type: EventType
    folder: str = ""
    file_path: str = ""
    message: str = ""
```
Acceptance: Class defined; can be instantiated; contains event_type, folder, file_path, message fields.

Task 10: Implement logging utility
Mode hint: /code-monkey
Action: Create `utils_sync/logging_sync.py` with function `setup_logger(log_dir="logs")` that:
- Creates timestamped log filename: `file_sync_YYYYMMDD_HHMMSS.log`
- Configures Python logging to write to file and console
- Returns logger instance
Acceptance: Creates log file; logger writes messages; timestamp format correct.

### Phase 02: File Synchronization Engine
Build the core synchronization logic and progress reporting.

Task 11: Implement file_sync_scanner.py - base scanner
Mode hint: /code-monkey
Action: Create `utils_sync/file_sync_scanner.py` with function `scan_folder(folder_path, include_roo_only, ignore_patterns)` that traverses folder (only .roo/ subtree if include_roo_only=True); applies ignore patterns using glob matching; returns dict of roo_relative_path to FileMeta; skips symlinks.
Acceptance: Returns dict; respects include_roo_only flag; ignore patterns work; skips symlinks.

Task 12: Implement FileMeta data structure
Mode hint: /code-monkey
Action: Add FileMeta data class to file_sync_scanner.py with fields: full_path, mtime, size.
Acceptance: Can be instantiated; fields accessible; hashable/comparable.

Task 13: Implement file_sync_core.py - build inventory
Mode hint: /code-monkey
Action: Create `utils_sync/file_sync_core.py` with function `build_inventory(folders, config)` that calls scan_folder for each folder; builds master inventory dict mapping rel_path to list of FileMeta from different folders; logs progress; emits SCAN events to queue.
Acceptance: Aggregates multiple folders; event queue populated; returns correct structure.

Task 14: Implement file_sync_core.py - comparison logic
Mode hint: /code-monkey
Action: Add function `select_source_file(file_meta_list)` that finds FileMeta with newest mtime; on tie, compares size; returns the selected FileMeta (source).
Acceptance: Correctly identifies newest; handles ties; returns FileMeta object.

Task 15: Implement file_sync_core.py - copy decision
Mode hint: /code-monkey
Action: Add function `should_copy(source_meta, target_meta)` that returns True if target is None or target.mtime is less than source.mtime.
Acceptance: Returns bool; handles None target; compares mtime correctly.

Task 16: Implement file_sync_core.py - safe copy with backup
Mode hint: /code
Action: Add function `safe_copy_file(source_path, target_path, backup_mode, preserve_mtime)` that creates timestamped backup if needed; copies to temp file; atomically renames; preserves mtime; handles errors gracefully and returns bool.
Acceptance: Creates backup; atomic replace; preserves mtime; handles errors.

Task 17: Implement file_sync_core.py - sync orchestration
Mode hint: /code
Action: Add function `sync_files(inventory, config, logger, event_queue)` that for each rel_path selects source; decides if copy needed; calls safe_copy_file; emits COPY/SKIP/ERROR events; logs operations; continues on errors; returns summary dict.
Acceptance: Orchestrates sync; emits events; returns summary; handles errors.

Task 18: Add dry-run support
Mode hint: /code-monkey
Action: Modify sync_files to check config dry_run flag; if True, log intention but skip actual copy; still emit events.
Acceptance: Dry run logs actions without modifying files; events still emitted.

### Phase 03: GUI Application
Implement the tkinter-based user interface with folder management and sync controls.

Task 19: Create sync_file.py - main window setup
Mode hint: /front-end
Action: Create `sync_file.py` with main tkinter window; load config; set window size from config; add title "AgentFlow File Sync" and description label "Use this utility to sync up all your AgentFlow files across as many projects as you want. Most recent 'date modified' will be used as source."
Acceptance: Window opens; correct size; title and description displayed.

Task 20: Add Browse button and folder selection
Mode hint: /front-end
Action: Add "Browse" button that opens tkinter.filedialog.askdirectory; on selection, add folder to internal list and update display.
Acceptance: Dialog opens; folder added to list on selection; duplicate folders prevented.

Task 21: Create scrollable folder list with remove buttons
Mode hint: /front-end
Action: Add scrollable frame/canvas containing rows; each row shows folder path and "X" button; clicking "X" removes folder from list and updates display.
Acceptance: Scrollable list works; folders displayed; remove button functions.

Task 22: Add status column to folder rows
Mode hint: /front-end
Action: Modify folder rows to include status label (initially empty); this will show progress messages during sync.
Acceptance: Status column visible; can be updated programmatically.

Task 23: Add Sync button at bottom
Mode hint: /front-end
Action: Add "Sync" button at bottom of window (sticky position); initially enabled only if 2+ folders selected.
Acceptance: Button positioned at bottom; enabled/disabled based on folder count.

Task 24: Implement background sync thread
Mode hint: /code
Action: Create function `run_sync_thread(folders, config, event_queue)` that runs sync in separate thread; calls build_inventory and sync_files from utils_sync; emits events to queue.
Acceptance: Runs in background thread; doesn't block GUI; completes successfully.

Task 25: Implement event queue processing
Mode hint: /code
Action: Add function `process_event_queue()` that checks event_queue (Queue.Queue); updates appropriate folder row status based on ProgressEvent; schedules itself to run again via after() if sync active.
Acceptance: Updates GUI from queue; thread-safe; runs periodically during sync.

Task 26: Wire Sync button to background thread
Mode hint: /front-end
Action: Connect Sync button click to start background thread; disable controls during sync; call process_event_queue to begin updates; re-enable controls on COMPLETE event.
Acceptance: Sync runs; GUI remains responsive; controls disabled/re-enabled correctly.

Task 27: Add completion summary dialog
Mode hint: /front-end
Action: On sync completion, show tkinter.messagebox with summary: files copied, skipped, errors from sync return value.
Acceptance: Dialog displays correct counts; appears after sync finishes.

### Phase 04: Testing & Validation
Comprehensive testing of sync logic and GUI behavior.

Task 28: Create tests directory structure
Mode hint: /task-simple
Action: Create `tests/` directory at project root; add `__init__.py` and `conftest.py` for pytest fixtures.
Acceptance: Directory created; pytest can discover tests.

Task 29: Create test fixtures for temp directories
Mode hint: /tester
Action: Add pytest fixture in `conftest.py` that creates temporary directory with .roo/ structure; yields path; cleans up after test.
Acceptance: Fixture creates temp dirs; cleanup works; can be reused across tests.

Task 30: Write tests for file_sync_scanner
Mode hint: /tester
Action: Create `tests/test_scanner.py` with tests for scan_folder: honors include_roo_only; applies ignore patterns; skips symlinks; returns correct structure; handles missing .roo/ folder.
Acceptance: All scanner tests pass; covers edge cases.

Task 31: Write tests for file comparison logic
Mode hint: /tester
Action: Create `tests/test_file_sync_core.py` with tests for select_source_file and should_copy: newest mtime selected; ties handled; None target handled; comparison logic correct.
Acceptance: Comparison tests pass; edge cases covered.

Task 32: Write tests for safe copy operations
Mode hint: /tester
Action: Add tests to test_file_sync_core.py for safe_copy_file: backup created when enabled; atomic replace works; mtime preserved; errors handled gracefully.
Acceptance: Copy safety tests pass; backups verified; no partial writes.

Task 33: Create integration test for full sync
Mode hint: /tester
Action: Add integration test that creates multiple temp folders with .roo/ structures; runs full sync; verifies newest files copied to all locations; checks backups; validates summary counts.
Acceptance: Integration test passes; verifies end-to-end sync behavior.

Task 34: Test dry-run mode
Mode hint: /tester
Action: Add test that enables dry_run config; runs sync; verifies no files actually copied but events emitted and logged.
Acceptance: Dry run test passes; no files modified; events correct.

Task 35: Manual GUI testing checklist
Mode hint: /tester
Action: Run sync_file.py manually and verify: window opens at correct size; Browse adds folders; X removes folders; scrolling works; Sync button enables/disables; progress shows during sync; summary appears; .roo/ detection works.
Acceptance: Manual test checklist completed; all UI behaviors confirmed.

Task 36: Create README documentation
Mode hint: /docs-writer
Action: Create `README_file_sync.md` documenting: purpose; usage instructions; config.txt fields and defaults; safety features; testing notes.
Acceptance: Documentation complete; covers all key aspects; examples provided.