Error: Parse error on line 4:
...fig_sync.load_config()]    end    sub
-----------------------^
Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', '-)', 'STADIUMEND', 'SUBROUTINEEND', 'PIPE', 'CYLINDEREND', 'DIAMOND_STOP', 'TAGEND', 'TRAPEND', 'INVTRAPEND', 'UNICODE_TEXT', 'TEXT', 'TAGSTART', got 'PS'

```mermaid
flowchart TD
    subgraph Config
        C1[config.txt<br/>folders_faves=/proj/a,/proj/b]
        C2[config_sync.load_config()]
    end

    subgraph GUI
        A1[MainApp.__init__]
        A2[favorite_folders list]
        A3[_update_folder_list_ui]
        A4[FolderItem rows]
        A5[_set_folder_favorite]
        A6[_load_favorite_folders]
        A7[_save_favorites_to_config]
    end

    C1 --> C2 --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4

    A4 -- click star --> A5
    A5 --> A2
    A5 --> A7
    A7 --> C1

    A2 -- user clicks Load Favorites --> A6
    A6 --> A3

```

Here is a concrete interface and behavior plan for favorites, wired to your new `folders_faves` config key.

1) Concept and data model

- `folders_faves` in `config.txt`:
  - Format: comma-separated absolute folder paths, like:
    - `folders_faves=/proj/one,/proj/two`
  - Stored as a list of strings in the in-memory config.
- Favorites are strictly absolute folder paths, same normalization as current selection.
- On startup:
  - The config loader parses `folders_faves` into a list.
  - The GUI loads this into an in-memory `favorite_folders` list on the `MainApp` instance (no automatic selection).

2) Config parsing and persistence

Goal: treat `folders_faves` similar to `ignore_patterns` and `root_allowlist`.

Plan:

- In `utils_sync/config_sync.py`:
  - Extend the parser to treat `folders_faves` as a comma-separated list.
    - Similar to `ignore_patterns` / `root_allowlist`.
    - If key missing or empty, default to `[]`.
  - In defaults:
    - Either keep it implicit (only present when set), or add `folders_faves: []` to `DEFAULTS` for clarity.
- Save behavior:
  - `config_sync.save_config()` should:
    - Round-trip `folders_faves` as a comma-separated list line, e.g.:
      - `folders_faves=/a/b/c,/x/y/z`
    - Order is not important; you can preserve the current order in memory.

This is enough for non-UI usage (e.g., CLI wanting to reuse favorites later if you decide to).

3) MainApp state and lifecycle

Within `main_gui.py`:

- New state on `MainApp`:
  - `self.favorite_folders: list[str]`:
    - Initialized in `__init__` right after `self.config = config_sync.load_config()`:
      - Read `self.config.get("folders_faves", [])`.
      - Optionally normalize each path through `file_path_utils.normalize_path()` so favorites are normalized on load.
- A small helper to sync memory -> config -> disk:
  - `self._save_favorites_to_config()`:
    - Updates `self.config["folders_faves"] = list(self.favorite_folders)`.
    - Calls `config_sync.save_config(self.config)`.
    - Does not touch other settings.

This keeps favorites persistence clearly separated from the Settings dialog save (which already manages backup_mode / dry_run etc).

4) UI changes – buttons and placement

Layout: use the existing bottom `button_frame` in `MainApp._create_widgets()` (`main_gui.py:150+`).

New buttons:

- Add a "Load Favorites" button:
  - Sits near Browse / Scan / Execute / Settings:
    - For example:
      - Col 0: Browse...
      - Col 1: Scan
      - Col 2: Execute
      - Col 3: Load Favorites
      - Col 4: Settings
  - Behavior:
    - Calls a new `self._load_favorite_folders()` method.
- Optional: add an "Add Current to Favorites" button:
  - If you want, to quickly persist the current selection:
    - "Save Favorites" or "Update Favorites".
    - Calls `self._save_current_selection_as_favorites()`.

5) UI changes – per-folder favorite toggle

The current folder row widget comes from the FolderItem class in `utils_sync/ui_utils.py`.

Plan:

- In `utils_sync/ui_utils.py`:
  - Add a small "favorite toggle" UI element to each folder row:
    - Example: a button with text "☆" (not favorite) / "★" (favorite), or a checkbox with label "Fav".
    - The star text avoids images and keeps dependencies light.
  - The FolderItem constructor should accept:
    - The folder path (already there).
    - A new callback `toggle_favorite_callback(folder_path: str)` (or similar).
    - Optionally a boolean `is_favorite` to set initial state (for rendering).
  - FolderItem should:
    - Expose an internal variable `self.is_favorite` to track state.
    - When the user clicks the star button:
      - Flip `self.is_favorite`.
      - Update its text/visual (☆ vs ★).
      - Invoke the callback with the folder path and new state (or just path, leaving lookup to the parent).

- In `MainApp._update_folder_list_ui()` (`main_gui.py:224+`):
  - When creating each FolderItem:
    - Determine if folder_path is in `self.favorite_folders`.
    - Pass that boolean to the FolderItem constructor.
    - Provide a callback that updates `favorite_folders` and persists to config.

6) Behavior details

6.1) Marking / unmarking favorites

New methods on `MainApp` (described at a high level):

- `_set_folder_favorite(folder_path: str, is_favorite: bool) -> None`:
  - Normalize `folder_path` the same way as when it's added to `selected_folders`.
  - If `is_favorite` is true:
    - Add to `self.favorite_folders` if not already present.
  - If `is_favorite` is false:
    - Remove from `self.favorite_folders` if present.
  - Call `_save_favorites_to_config()` to persist.
- The `toggle_favorite_callback` passed into FolderItem calls `_set_folder_favorite()` with the path and new state.

Edge cases:

- If a selected folder is removed (`_remove_folder`), you probably:
  - Leave it as favorite: a user might want it as a favorite even when not currently selected.
  - So `_remove_folder` should not touch favorites.

6.2) Loading favorites

`_load_favorite_folders()` should:

- Start from the stored `self.favorite_folders`.
- For each favorite path:
  - Normalize it via `file_path_utils.normalize_path()`.
  - Check it still exists and has `.roo`:
    - If missing or has no `.roo`, skip.
    - Optionally accumulate skipped favorites; at the end, you can show a message like:
      - "Some favorites are invalid and were skipped: ..." (nice-to-have).
  - If not already in `self.selected_folders`, append.
- After processing all favorites:
  - Call `self._update_folder_list_ui()`.
- If, after loading, there are fewer than 2 valid folders:
  - No immediate error; the existing Scan/Execute logic already checks for `< 2` and shows an error when user tries to scan.

Idempotence:

- If user clicks "Load Favorites" multiple times, your logic should avoid duplicates by checking membership before appending.

6.3) Saving current selection as favorites (optional enhancement)

If you include a "Save Favorites" button:

- `_save_current_selection_as_favorites()`:
  - Set `self.favorite_folders = list(self.selected_folders)`.
  - Call `_save_favorites_to_config()`.
  - Optionally show a small messagebox:
    - "Favorites saved from current selection."

This gives a power-user path: select a new set of project roots, then persist them all as the new favorite set.

7) Interaction with CLI and non-GUI

Current CLI entrypoint `cli_sync.py` probably doesn't touch `folders_faves`.

- Minimal plan:
  - For now, keep favorites purely as a GUI-only convenience:
    - CLI behavior unchanged.
- Future extension (if desired):
  - Add CLI flag like `--use-favorites` to load `folders_faves` from config as the folder set when no explicit folders are passed.
  - This would reuse the same parsing in `config_sync.load_config()`.

8) UX considerations / microcopy

- Button labels:
  - "Load Favorites" (clear intent).
  - Optional "Save Favorites" or "Update Favorites" (if added).
- Star toggle:
  - Use "☆" / "★" and keep them monochrome; no need for colors unless you want them.
- Feedback:
  - For toggling favorites:
    - Given it's low-risk, you probably don't need messageboxes.
    - Visual feedback from the icon flip is enough.
  - For "Load Favorites":
    - If no favorites configured, show:
      - "No favorite folders are configured in config.txt."
    - If some favorites were skipped because they are invalid:
      - Optionally display one message listing them (or just print to stdout).

9) Testing strategy

Config-level tests:

- In `tests/test_config_sync.py`:
  - Add tests:
    - `test_folders_faves_parsing_list`:
      - Config line: `folders_faves=/one,/two`.
      - Assert `cfg["folders_faves"] == ["/one", "/two"]`.
    - `test_folders_faves_missing_defaults_to_empty`:
      - No line: `folders_faves=...`.
      - Assert `cfg["folders_faves"] == []` (or not present if you prefer, but be consistent).
- Optional: test round-tripping via `save_config()`:
  - Create a config dict in memory with `folders_faves`.
  - Save to temp file.
  - Reload and assert equivalence.

UI-level:

- You likely do not have Tkinter tests currently; so:
  - Rely on manual validation for:
    - Star toggle.
    - Load Favorites button.
  - Keep the logic simple and side-effect-light to make Tkinter debugging easy.

10) High-level flow diagram

```mermaid
flowchart TD
    subgraph Config
        C1[config.txt<br/>folders_faves=/proj/a,/proj/b]
        C2[config_sync.load_config()]
    end

    subgraph GUI
        A1[MainApp.__init__]
        A2[favorite_folders list]
        A3[_update_folder_list_ui]
        A4[FolderItem rows]
        A5[_set_folder_favorite]
        A6[_load_favorite_folders]
        A7[_save_favorites_to_config]
    end

    C1 --> C2 --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4

    A4 -- click star --> A5
    A5 --> A2
    A5 --> A7
    A7 --> C1

    A2 -- user clicks Load Favorites --> A6
    A6 --> A3
```

This plan keeps favorites self-contained:

- Config key `folders_faves` holds paths.
- The GUI exposes lightweight controls:
  - Per-folder toggle.
  - One-click "Load Favorites".
  - Optional "Save Favorites".
- Sync behavior remains unchanged; favorites only affect how `selected_folders` is populated.