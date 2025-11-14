# Dry run

## Summary
**Dry-run mode runs the full discovery/planning and logging pipeline but turns all actual copy/backup/timestamp operations into SKIP events.** It guarantees that *no* files on disk are modified, created, deleted, or backed up; you only see what *would* happen in a real run.

## Detail

1) What it does conceptually  
- It runs the *full planning phase* of the sync, but completely skips any file modifications.  
- In other words: it shows you what **would** be copied where, but it does **not** copy, overwrite, delete, or back up any files.

2) Where the flag comes from  
- The `dry_run` setting is part of the config handled by [`config_sync.load_config()`](utils_sync/config_sync.py:1).  
- The config is normalized so `dry_run` is always a boolean by [`config_sync.normalize_config()`](utils_sync/config_sync.py:120).  
- The GUI checkbox (“Dry run (preview changes only)”) in [`MainApplication`](main_gui.py:1) binds directly to this flag, and the CLI reads it from `config.txt` or environment/config defaults.

3) How it affects the core sync logic  
The core behavior is in the sync engine’s execution step, inside something like [`SyncCore.execute_actions()`](utils_sync/sync_core.py:190):

- The tool first computes a list of planned copy actions (newest-wins logic), regardless of `dry_run`.  
- When executing those actions:
  - If `dry_run` is `True`, for each planned copy it does:
    - Emit a progress event with type `[EventType.SKIP](utils_sync/progress_events.py:1)` and message `"Dry run, skipping copy"` (see snippet around `self._emit_event(..., EventType.SKIP, ...)` in `execute_actions`).  
    - `continue` to the next action, so no copy happens:
      - No temp file is created.  
      - No rename/atomic replace is performed.  
      - No timestamped backup file is written.  
      - No destination or source file content or mtime is changed.
  - If `dry_run` is `False`, it:
    - Honors `backup_mode` (e.g., `timestamped`) and creates backup files.  
    - Performs the atomic copy: temp file + rename.  
    - Emits success/error progress events as it actually modifies files.

So: **all disk-changing behavior in `execute_actions()` is skipped when `dry_run` is on; only events/logging happen.**

4) What still happens in dry-run mode  
Even with `dry_run=True`, the following still occur:

- Directory scanning and planning:
  - It walks your selected project roots.  
  - It enforces `.roo`-only behavior and `root_allowlist` as normal.  
  - It computes which files are newest and which copies *would* be performed.
- Ignore patterns:
  - `ignore_patterns` in config are still applied: ignored files/folders don’t appear in planned actions.
- Logging and events:
  - The logger (`[logger.log_event()](utils_sync/logger.py:200)`) still records plan and SKIP events.  
  - Progress events are emitted, so the GUI log / CLI output shows *exactly* which operations would have run.
- Exit codes:
  - The process still returns success/failure codes based on whether the run itself was error-free; dry-run doesn’t force a special exit code.

5) How the GUI reflects dry-run  
In the GUI (`[main_gui.py](main_gui.py:1)`):

- If `dry_run` is `True`:
  - A status label is updated via `MainApplication._update_dry_run_status()` to `"⚠ DRY RUN MODE: No files will be modified"` in red/bold.  
  - After sync completes, it shows a message box:  
    - `"Dry run completed successfully.\n\nNo files were modified."`
- If `dry_run` is `False`:
  - Before starting sync, `MainApplication._on_start_sync()` shows a confirmation dialog:
    - `"WARNING: This is NOT a dry run. Files will be modified.\n\nAre you sure you want to proceed?"`
  - On success, the completion message is just `"Synchronization completed successfully."`

6) How the CLI behaves in dry-run  
From the CLI (`[cli_sync.run_sync()](cli_sync.py:1)`):

- It loads the config (including `dry_run`).  
- Runs planning and `execute_actions()` exactly the same as the GUI.  
- When `dry_run=True`, the printed/logged events will show `SKIP` entries with messages like `"Dry run, skipping copy"` and you will see *no* new/changed files in the filesystem.

7) Tested guarantees  
The unit tests in `[tests/test_sync_core.py](tests/test_sync_core.py:90)` explicitly verify:

- With `config = {"ignore_patterns": [], "dry_run": True, "backup_mode": "timestamped"}`:
  - `execute_actions()` only emits `SKIP` events.  
  - The destination files remain unchanged (no copy, no backup created).  
- With identical config but `dry_run=False`:
  - Real copies happen and timestamped backups are created.
