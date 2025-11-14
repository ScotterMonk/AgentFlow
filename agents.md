# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Type
Python file synchronization utility for `.roo` directories across multiple project folders.

## Run Commands
GUI: `python main_gui.py`
CLI: `python cli_sync.py <folder1> <folder2> ...`
Tests: `pytest tests/`

## Critical Non-Standard Patterns

### LLM Attribution Comments
All functions/classes MUST include: `# [Created-or-Modified] by [LLM model] | yyyy-mm-dd_[iteration]`

### Naming Convention
Domain-suffix pattern: `{domain}_{specific}` not `{specific}_{domain}`
- Correct: `utils_sync/`, `sync_core.py`, `config_sync.py`
- Wrong: `sync_utils/`, `core_sync.py`, `sync_config.py`

### File Sync Behavior
- Scans `.roo/` subdirectories ONLY (not entire project folders)
- Uses mtime (modification time) to determine newest file as source
- Root-level files require explicit `root_allowlist` in config.txt
- Atomic copy: temp file + rename (not direct copy)
- Timestamped backups: `filename_YYYYMMDDTHHMMSSZ.bak` format

### Configuration
Settings in `config.txt` (NOT .ini, .json, or .yaml):
- `root_allowlist`: Comma-separated list of root files to sync (e.g., `.roomodes`)
- `backup_mode`: "timestamped" or "none"
- `preserve_mtime`: Must be true to maintain file timestamps
- `include_roo_only`: Must be true (project requirement)

### Testing
- Integration tests use `test_integration/` with project_a and project_b folders
- Tests verify .roo sync behavior, not general file sync
- pytest fixtures in tests/ create temporary .roo structures

## Documentation
See `.roo/rules/01-general.md` for comprehensive coding standards, workflow, and mode selection guidance.

## Misc
There is no database for this project. Ignore any references to a database.