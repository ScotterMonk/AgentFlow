Recommendation: keep .roo-only safety and add a root-level “allowlist” gate for .roomodes

Goal
- Preserve the current safety boundary (only scan .roo subtree), but also include one specific sibling file that lives next to .roo: .roomodes.

Minimal, safe design
- Keep the existing hard requirement: a folder is eligible only if it has a real (non-symlink) .roo directory. No change to validation or scope baseline.
- Add an explicit, opt-in allowlist for root-level files to include in the scan. Default is empty; recommend shipping with .roomodes as the only default entry (can be toggled off).

Concrete plan
1) Config
- Add a new setting in config.txt:
  - root_allowlist=.roomodes
  - Default: empty list (safest). Your curated default can set it to .roomodes.
- Also acceptable UI alternatives:
  - include_roomodes=true (single-purpose switch for this one file)
  - Both can co-exist; if include_roomodes=true, treat it as implicitly adding .roomodes to the root_allowlist.

2) Scan behavior (append-only to the current index)
- After the regular .roo scan completes for each folder, attempt to include allowlisted root files.
- For each folder in the sync set:
  - Ensure the folder passed the existing .roo gate (no changes here).
  - For each entry in root_allowlist:
    - Resolve path = <folder> / <entry>
    - Include only if:
      - path.exists() and path.is_file()
      - Not a symlink (path.is_symlink() is false)
    - Add it to the file index with a stable, synthetic relative key equal to the file name (e.g., ".roomodes"). This prevents any overlap with real .roo keys (which are always like "rules/…", "docs/…", etc.).
- Result: actions/planning/execution all continue to operate on real Path objects; only the map key (relative_path) is the synthetic label ".roomodes", which is safe and unique.

3) Safety rails (keep blast radius tiny)
- Do not broaden scanning beyond the exact allowlist; never traverse more of the project root.
- Keep the existing .roo presence requirement (folders without .roo are rejected before any root-level inclusion).
- Disallow symlinks and non-regular files for allowlisted items.
- Respect ignore_patterns by name if you want a belt-and-suspenders option (not strictly necessary for a single fixed name like ".roomodes").
- Optional: enforce a small size cap (e.g., 256 KB) for allowlisted root files to avoid accidental large syncs.

4) User experience defaults
- Default to safe: root_allowlist empty; include_roomodes=false.
- Document the option in README-file-sync so users explicitly opt in.
- Surface a small UI toggle in the Settings dialog: “Include root-level .roomodes” (mapped to include_roomodes or root_allowlist).

5) Where this fits in the code
- Update index-building at end of [SyncEngine.scan_folders()](utils_sync/sync_core.py:48).
- Add/read config keys in [utils_sync/config_sync.py](utils_sync/config_sync.py).
- Document the new setting(s) in [README-file-sync.md](README-file-sync.md).

Notes on compatibility
- No changes needed to planning or execution flows; they work with the real destination paths from the index.
- Event messages will naturally show “.roomodes” for file_path, which is clear and consistent.

Mermaid overview
flowchart TD
  A[Validate folder has real .roo] -->|pass| B[Scan .roo subtree]
  A -->|fail| X[Skip folder]
  B --> C[Append allowlisted root files e.g. .roomodes]
  C --> D[Plan actions (mtime newest-wins)]
  D --> E[Execute (atomic copy, backups, dry-run)]

This approach keeps the strict .roo boundary by default, introduces zero traversal outside .roo unless explicitly allowlisted, and limits additions to a tiny, known-safe set—starting with .roomodes only.