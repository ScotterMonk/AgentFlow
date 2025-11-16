# Config Refactoring Plan

Plan: 251116_config_refactor
Log: `.roo/docs/plans/plan_251116_config_refactor_log.md`
User Query: `.roo/docs/plans/plan_20251116_config_refactor_user.md`

## Overview
Refactor config.txt and related code to remove obsolete parameters `include_roo_only` and `include_roomodes`, consolidating behavior into `root_allowlist` and `ignore_patterns`.

## Analysis Summary
Current state:
- `include_roo_only` is defined in DEFAULTS but NOT used in actual sync logic
- `include_roomodes` has an xfail test but was NEVER implemented in actual code
- `root_allowlist` and `ignore_patterns` already support both "," and ", " separation
- `save_config` already writes using ", " (comma-space) format by default
- config.txt has duplicate `root_allowlist` lines (line 4 and line 10)

## Tasks

- Task 01: Remove `include_roo_only` from utils_sync/config_sync.py DEFAULTS dict (line 13)
    Mode hint: /task-simple
    Action: Delete line 13 which contains `"include_roo_only": True,`

- Task 02: Remove `include_roo_only` from load_config parsing logic in utils_sync/config_sync.py
    Mode hint: /task-simple
    Action: Remove `include_roo_only` from the boolean keys tuple on line 106
    Change from: `elif key in ("include_roo_only", "preserve_mtime", "dry_run"):`
    Change to: `elif key in ("preserve_mtime", "dry_run"):`

- Task 03: Remove `include_roo_only` from boolean validation in utils_sync/config_sync.py
    Mode hint: /task-simple
    Action: Remove `include_roo_only` from the validation loop on line 136
    Change from: `for b in ("include_roo_only", "preserve_mtime", "dry_run"):`
    Change to: `for b in ("preserve_mtime", "dry_run"):`

- Task 04: Update config.txt to remove obsolete parameters
    Mode hint: /task-simple
    Action: Remove lines 3, 5, and 10 from config.txt:
    - Line 3: `include_roo_only=true`
    - Line 5: `include_roomodes=true`
    - Line 10: `root_allowlist=` (duplicate empty line)
    Keep line 4: `root_allowlist=.roomodes`

- Task 05: Remove xfail test for `include_roomodes` from tests/test_config_sync.py
    Mode hint: /task-simple
    Action: Delete the entire test function `test_include_roomodes_behavior` (lines 81-98) which is marked with @pytest.mark.xfail

- Task 06: Update agents.md Configuration section
    Mode hint: /task-simple
    Action: In agents.md, remove the line `- include_roo_only: Must be true (project requirement)` from the Configuration section (around line 36)

- Task 07: Update README-file-sync.md to remove obsolete parameter references
    Mode hint: /code-monkey
    Action: Search README-file-sync.md for any references to `include_roo_only` or `include_roomodes` and remove/update them
    Note: Based on search results, there's a comment block around lines 93-100 that mentions these obsolete parameters

- Task 08: Run pytest to verify all tests pass
    Mode hint: /tester
    Action: Execute `pytest tests/` and verify all tests pass after the changes
    Expected: All tests should pass since we're only removing unused code

## Expected Outcome
After completion:
- Simplified configuration with only `root_allowlist` and `ignore_patterns`
- No obsolete parameters in code, tests, or documentation  
- Both params support "," and ", " separation (already working)
- Config writes with ", " format (already working)
- All tests passing

## Files to Modify
- utils_sync/config_sync.py
- config.txt
- tests/test_config_sync.py
- agents.md
- README-file-sync.md