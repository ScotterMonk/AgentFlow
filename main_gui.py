# [Modified] by Claude Sonnet 4.5 | 2025-11-13_03
"""
Agentflow File Sync - Main GUI Application
Provides a Tkinter-based interface for managing file synchronization.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import queue
from pathlib import Path
from functools import partial
import datetime
from utils_sync import config_sync, file_path_utils
from utils_sync.sync_core import SyncEngine
from utils_sync.sync_worker import SyncWorker
from utils_sync.progress_events import ProgressEvent, EventType
from utils_sync.ui_utils import FolderItem

# Global UI colors for dark mode
DARK_BG = "#000000"
DARK_BG_ALT = "#111111"
FG_PRIMARY = "#e0e0e0"

# Button colors for dark mode
BUTTON_BG = "#000000"
BUTTON_BG_HOVER = "#111111"
BUTTON_BORDER = "#00ff5f"
BUTTON_TEXT = FG_PRIMARY

class MainApp:
    """Main application window for Agentflow File Sync."""
    # [Created] by Claude Sonnet 4.5 | 2025-11-13_01
    
    def __init__(self, root: tk.Tk):
        """Initialize the main application window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        
        # Load configuration
        self.config = config_sync.load_config()
        
        # Initialize favorite folders from config, normalizing paths
        raw_faves = self.config.get("folders_faves", [])
        self.favorite_folders = [
            file_path_utils.normalize_path(p) for p in raw_faves
        ]
        
        # Set up main window
        self.root.title("Agentflow File Sync")
        window_width = self.config["window_width"]
        window_height = self.config["window_height"]
        self.root.geometry(f"{window_width}x{window_height}")
        # Apply base dark background to root window
        self.root.configure(bg=DARK_BG)
        
        # Create event queue for progress updates
        self.event_queue = queue.Queue()
        
        # Initialize sync engine
        self.sync_engine = SyncEngine(self.config, self.event_queue)
        
        # Initialize selected folders list
        self.selected_folders = []
        
        # Initialize sync state
        self.is_syncing = False
        
        # Initialize folder widgets dictionary
        self.folder_widgets = {}
        
        # Store button references
        self.browse_button = None
        self.sync_button = None
        self.confirm_button = None
        self.load_favorites_button = None
        
        # Store status label references
        self.dry_run_label = None
        self.ignore_patterns_label = None
        
        # Store planned actions for two-stage sync (preview then execute)
        self.planned_actions = []
        
        # Create UI widgets
        self._create_widgets()
        
        # Update status displays
        self._update_dry_run_status()
        self._update_ignore_patterns_display()
        
        # Start periodic event processing
        self._process_events()
    
    def _create_widgets(self):
        """Create and layout all UI widgets."""
        # [Modified] by openai/gpt-5.1 | 2025-12-04_02
        
        # Configure a basic dark theme for ttk widgets
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            # Fall back to current theme if clam is unavailable
            pass

        # Dark background for frames and labels
        style.configure("TFrame", background=DARK_BG)
        style.configure("TLabel", background=DARK_BG, foreground=FG_PRIMARY)

        # Base button style (fallback)
        style.configure(
            "TButton",
            background=BUTTON_BG,
            foreground=BUTTON_TEXT,
        )

        # Primary app button style: black background, green outline, hover highlight
        style.configure(
            "AF.TButton",
            background=BUTTON_BG,
            foreground=BUTTON_TEXT,
            bordercolor=BUTTON_BORDER,
            focusthickness=1,
            focuscolor=BUTTON_BORDER,
        )
        style.map(
            "AF.TButton",
            background=[("active", BUTTON_BG_HOVER)],
            bordercolor=[("active", BUTTON_BORDER)],
            foreground=[
                ("active", BUTTON_BORDER),
                ("disabled", "#555555"),
            ],
        )
 
        # Danger style (for destructive actions like Delete .bak)
        style.configure(
            "AFDanger.TButton",
            background=BUTTON_BG,
            foreground="#ff6666",
            bordercolor="#ff6666",
            focusthickness=1,
            focuscolor="#ff6666",
        )
        style.map(
            "AFDanger.TButton",
            background=[("active", BUTTON_BG_HOVER)],
            bordercolor=[("active", "#ff6666")],
            foreground=[
                ("active", BUTTON_BORDER),
                ("disabled", "#555555"),
            ],
        )
 
        # Compact button style for small icon buttons (used in folder rows)
        style.configure(
            "AFMini.TButton",
            background=BUTTON_BG,
            foreground=BUTTON_TEXT,
            bordercolor=BUTTON_BORDER,
            focusthickness=1,
            focuscolor=BUTTON_BORDER,
            padding=0,
        )
        style.map(
            "AFMini.TButton",
            background=[("active", BUTTON_BG_HOVER)],
            bordercolor=[("active", BUTTON_BORDER)],
        )

        # Progress bar style: dark, invisible trough with a glowing green bar
        # The trough matches the DARK_BG so idle (0%) bars visually disappear,
        # while the active portion uses the same neon green as primary actions.
        #
        # Progressbar internally prefixes the style with "Horizontal." for horizontal
        # bars, so a Progressbar with style="AF.Progressbar" will actually look for
        # the layout/style "Horizontal.AF.Progressbar". We clone the base horizontal
        # layout and then customize colors so Tk has a valid layout for this style.
        style.layout("Horizontal.AF.Progressbar", style.layout("Horizontal.TProgressbar"))
        style.configure(
            "Horizontal.AF.Progressbar",
            troughcolor=DARK_BG,
            background=BUTTON_BORDER,
            bordercolor=BUTTON_BORDER,
            lightcolor="#66ff99",
            darkcolor=BUTTON_BORDER,
            thickness=8,
        )

        # Scrollbar style: subtle dark theme: very dark grey trough, deep muted green thumb
        style.configure(
            "Vertical.TScrollbar",
            troughcolor="#151515",        # darker than DARK_BG_ALT but not pure black
            background="#0f3b24",        # deep, low-saturation green thumb
            bordercolor="#0f3b24",
            arrowcolor="#666666",        # neutral arrows so the thumb doesn't pop
        )
        style.map(
            "Vertical.TScrollbar",
            background=[("active", "#145232")],  # slightly lighter but still dark green on hover
        )
 
        # Ensure the root window background matches the dark theme
        self.root.configure(bg=DARK_BG)
        
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="3")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title label
        title_label = ttk.Label(
            main_frame,
            text="Agentflow File Sync",
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 2), sticky=tk.W)
        
        # Description label
        desc_label = ttk.Label(
            main_frame,
            text="Synchronize files across multiple folders with intelligent conflict resolution."
        )
        desc_label.grid(row=1, column=0, pady=(0, 0), sticky=tk.W)
        
        # Dry run status label
        self.dry_run_label = ttk.Label(main_frame, text="")
        self.dry_run_label.grid(row=2, column=0, pady=(0, 0), sticky=tk.W)
        
        # Ignore patterns label
        #self.ignore_patterns_label = ttk.Label(main_frame, text="")
        #self.ignore_patterns_label.grid(row=3, column=0, pady=(0, 0), sticky=tk.W)
        
        # Folder list frame
        folder_frame = tk.Frame(
            main_frame,
            relief=tk.SOLID,
            borderwidth=1,
            bg=DARK_BG,
        )
        folder_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(1, 7))
        folder_frame.columnconfigure(0, weight=1)
        folder_frame.rowconfigure(0, weight=1)

        # Create scrollable canvas + frame for folder list
        self.folder_canvas = tk.Canvas(
            folder_frame,
            borderwidth=1,
            highlightthickness=0,
            bg=DARK_BG,
        )
        self.folder_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        folder_scrollbar = ttk.Scrollbar(
            folder_frame,
            orient=tk.VERTICAL,
            command=self.folder_canvas.yview
        )
        folder_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.folder_canvas.configure(yscrollcommand=folder_scrollbar.set)

        # Inner frame that holds the per-folder widgets
        self.folder_list_frame = ttk.Frame(self.folder_canvas)
        self.folder_canvas.create_window((0, 0), window=self.folder_list_frame, anchor="nw")

        # Update scroll region whenever the inner frame size changes
        self.folder_list_frame.bind(
            "<Configure>",
            lambda e: self.folder_canvas.configure(scrollregion=self.folder_canvas.bbox("all"))
        )
        
        # Enable mouse wheel scrolling anywhere in the main window
        # Bind at the application level so scroll works even when child widgets have focus
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Bottom button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        # Browse button
        self.browse_button = ttk.Button(
            button_frame,
            text="Browse...",
            command=self._open_folder_dialog,
            style="AF.TButton",
        )
        self.browse_button.grid(row=0, column=0, padx=(0, 5))
        
        # Scan button (first stage: plan/preview, was "Preview")
        self.sync_button = ttk.Button(
            button_frame,
            text="Scan",
            command=self._start_sync,
            style="AF.TButton",
        )
        self.sync_button.grid(row=0, column=1, padx=(0, 5))
        
        # Execute button (second stage: execute planned actions, was "Confirm")
        self.confirm_button = ttk.Button(
            button_frame,
            text="Execute",
            state=tk.DISABLED,
            command=self._confirm_sync,
            style="AF.TButton",
        )
        self.confirm_button.grid(row=0, column=2, padx=(0, 5))
        
        # Load Favorites button
        self.load_favorites_button = ttk.Button(
            button_frame,
            text="Load Favorites",
            command=self._load_favorite_folders,
            style="AF.TButton",
        )
        self.load_favorites_button.grid(row=0, column=3, padx=(0, 5))
        
        # Save Favorites button
        self.save_favorites_button = ttk.Button(
            button_frame,
            text="Save Favorites",
            command=self._save_current_selection_as_favorites,
            style="AF.TButton",
        )
        self.save_favorites_button.grid(row=0, column=4, padx=(0, 5))
        
        # Delete .bak files button (disabled until at least one folder is selected)
        self.delete_bak_button = ttk.Button(
            button_frame,
            text="Delete .bak files",
            command=self._delete_bak_files,
            state=tk.DISABLED,
            style="AFDanger.TButton",
        )
        self.delete_bak_button.grid(row=0, column=5, padx=(0, 5))
        
        # Settings button
        self.settings_button = ttk.Button(
            button_frame,
            text="Settings",
            command=self._open_settings_window,
            style="AF.TButton",
        )
        self.settings_button.grid(row=0, column=6)
    
    def _open_folder_dialog(self):
        """Open folder selection dialog and add valid folder to list."""
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_01
        
        # Open folder selection dialog
        folder_path = filedialog.askdirectory(title="Select folder to sync")
        
        if folder_path:
            # Normalize the path
            normalized_path = file_path_utils.normalize_path(folder_path)
            
            # Validate folder has .roo directory
            if not file_path_utils.has_roo_dir(normalized_path):
                print(f"Error: Folder does not contain a .roo subdirectory: {normalized_path}")
                return
            
            # Check if folder is already in the list
            if normalized_path in self.selected_folders:
                print(f"Folder already selected: {normalized_path}")
                return
            
            # Add to selected folders and update UI
            self.selected_folders.append(normalized_path)
            self._update_folder_list_ui()
    
    def _remove_folder(self, folder_to_remove: str):
        """Remove a folder from the selected folders list.
        
        Args:
            folder_to_remove: The folder path to remove
        """
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_01
        
        if folder_to_remove in self.selected_folders:
            self.selected_folders.remove(folder_to_remove)
            self._update_folder_list_ui()
    
    def _update_folder_list_ui(self):
        """Update the folder list UI to reflect current selected folders."""
        # [Modified] by openai/gpt-5.1 | 2025-11-15_01
        
        # Destroy all existing widgets in the folder list frame
        for widget in self.folder_list_frame.winfo_children():
            widget.destroy()
        
        # Clear folder widgets dictionary
        self.folder_widgets = {}
        
        # Create a FolderItem for each selected folder
        for folder_path in self.selected_folders:
            # Determine initial favorite state, normalizing paths when possible
            try:
                normalized_path = file_path_utils.normalize_path(folder_path)
                is_fav = normalized_path in self.favorite_folders
            except Exception as exc:
                # Fail soft if normalization fails; fall back to raw path membership
                print(
                    f"Error normalizing selected folder path {folder_path!r} "
                    f"for favorites: {exc}"
                )
                is_fav = folder_path in self.favorite_folders
            
            folder_item = FolderItem(
                self.folder_list_frame,
                folder_path,
                self._remove_folder,
                self._remove_planned_action,
                toggle_favorite_callback=lambda p, fav, fp=folder_path: self._set_folder_favorite(fp, fav),
                is_favorite=is_fav,
            )
            folder_item.frame.pack(fill=tk.X, padx=2, pady=2)
            
            # Store widget reference in dictionary
            self.folder_widgets[folder_path] = folder_item
        
        # Always disable Delete .bak button when no folders are selected; enabling
        # is controlled by _update_bak_previews() based on visible .bak rows.
        if getattr(self, "delete_bak_button", None) is not None:
            if not self.selected_folders:
                self.delete_bak_button.config(state=tk.DISABLED)
    
    def _format_mtime(self, mtime: float) -> str:
        """Format a POSIX mtime value for display in the preview."""
        # [Created] by openai/gpt-5.1 | 2025-11-14_02
        try:
            dt = datetime.datetime.fromtimestamp(mtime)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return ""
    
    def _update_overwrite_previews(self) -> None:
        """Rebuild per-folder overwrite previews from the current planned actions."""
        # [Created] by openai/gpt-5.1 | 2025-11-14_02
    
        # Build per-folder list of planned overwrites, including timestamps and action refs
        overwrites_by_folder = {folder: [] for folder in self.selected_folders}
        for action in self.planned_actions:
            dest_path = action.get("destination_path")
            relative = str(action.get("relative_path", ""))
            dest_mtime = action.get("destination_mtime")
    
            # Pre-format timestamp once for display; use destination mtime snapshot from scan
            timestamp = self._format_mtime(dest_mtime) if dest_mtime is not None else ""
    
            if dest_path is None:
                continue
    
            for base in self.selected_folders:
                base_path = Path(base)
                try:
                    dest_path.relative_to(base_path)
                    overwrites_by_folder[base].append(
                        {
                            "relative": relative,
                            "timestamp": timestamp,
                            "action": action,
                        }
                    )
                    break
                except ValueError:
                    continue
    
        any_actions = False
        for folder_path, widget in self.folder_widgets.items():
            items = overwrites_by_folder.get(folder_path, [])
            # Update per-folder preview under the folder name
            if hasattr(widget, "update_preview"):
                widget.update_preview(items)
            # Track whether any actions are planned for enabling the Execute button
            if items:
                any_actions = True
            # Show a clear post-scan status for all folders
            widget.update_status("Scanned", "green")
    
        # Enable or disable Execute based on whether any actions remain
        if any_actions:
            if self.confirm_button:
                self.confirm_button.config(state=tk.NORMAL)
        else:
            if self.confirm_button:
                self.confirm_button.config(state=tk.DISABLED)
    
    def _update_bak_previews(self) -> None:
        """Refresh .bak backup file rows under each selected folder preview."""
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-12-04_02
        if not self.selected_folders or not self.folder_widgets:
            # No folders or widgets – ensure Delete .bak button is disabled.
            if getattr(self, "delete_bak_button", None) is not None:
                self.delete_bak_button.config(state=tk.DISABLED)
            return

        any_bak = False

        for folder_path, widget in self.folder_widgets.items():
            base_path = Path(folder_path)
            if not base_path.exists():
                # Folder no longer exists; clear any existing backup rows
                if hasattr(widget, "show_backup_files"):
                    widget.show_backup_files([])
                continue

            bak_relatives: list[str] = []
            try:
                for bak in base_path.rglob("*.bak"):
                    try:
                        rel = bak.relative_to(base_path)
                    except ValueError:
                        # Should not happen for descendants, but fail soft
                        continue
                    bak_relatives.append(str(rel))
            except OSError as exc:
                # Fail soft; log error and clear backups for this folder
                print(f"Error scanning for .bak files under {base_path!s}: {exc}")
                if hasattr(widget, "show_backup_files"):
                    widget.show_backup_files([])
                continue

            if bak_relatives:
                any_bak = True

            # Delegate to the folder widget to render (or clear) backup rows.
            # Passing an empty list will remove any previously displayed .bak rows.
            if hasattr(widget, "show_backup_files"):
                widget.show_backup_files(bak_relatives)

        # Enable Delete .bak files button only when at least one backup row is visible;
        # otherwise keep it disabled and its text grayed out.
        if getattr(self, "delete_bak_button", None) is not None:
            if any_bak:
                self.delete_bak_button.config(state=tk.NORMAL)
            else:
                self.delete_bak_button.config(state=tk.DISABLED)
    
    def _remove_planned_action(self, action_to_remove: dict) -> None:
        """Remove a single planned action from the queue and refresh previews."""
        # [Created] by openai/gpt-5.1 | 2025-11-14_02
        if not self.planned_actions:
            return
    
        # Remove by identity; callbacks receive the original action dict instance
        self.planned_actions = [
            a for a in self.planned_actions
            if a is not action_to_remove
        ]
    
        # Rebuild previews and update Execute button state
        self._update_overwrite_previews()
    
    def _start_sync(self):
        """Run planning phase and show per-folder preview before actual sync."""
        # [Modified] by openai/gpt-5.1 | 2025-11-14_02
        
        # Check if already syncing
        if self.is_syncing:
            return
        
        # Check if at least 2 folders are selected
        if len(self.selected_folders) < 2:
            messagebox.showerror(
                "Insufficient Folders",
                "Please select at least 2 folders to sync."
            )
            return
        
        # Set syncing state for planning phase
        self.is_syncing = True
        
        # Disable buttons during planning
        self.sync_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        if self.confirm_button:
            self.confirm_button.config(state=tk.DISABLED)
        
        # Reset status of all folder widgets and show planning state
        for widget in self.folder_widgets.values():
            widget.reset_status()
            widget.update_status("Planning...", "blue")
        
        try:
            # Run scan and plan synchronously to compute actions
            folder_paths = [Path(p) for p in self.selected_folders]
            file_index = self.sync_engine.scan_folders(folder_paths)
            actions = self.sync_engine.plan_actions(file_index)
        except Exception as e:
            messagebox.showerror(
                "Preview Failed",
                f"Error while planning sync:\n{e}"
            )
            self.is_syncing = False
            self.sync_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)
            return
        
        # Store planned actions for confirmation stage
        self.planned_actions = actions
        
        # Re-enable buttons after planning
        self.is_syncing = False
        self.browse_button.config(state=tk.NORMAL)
        self.sync_button.config(state=tk.NORMAL)
        
        # Build per-folder preview list of files that will be overwritten
        # including last-modified timestamps and per-file removal "X" controls.
        self._update_overwrite_previews()
        
        # Clear any queued scan events so they don't overwrite the preview status
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break
    
    def _confirm_sync(self):
        """Execute the planned sync actions after user confirmation."""
        # [Created] by openai/gpt-5.1 | 2025-11-14_01
        
        # Do not start if already syncing
        if self.is_syncing:
            return
        
        # Ensure we have planned actions
        if not self.planned_actions:
            messagebox.showinfo(
                "Nothing to Sync",
                "There are no planned actions to execute. Run Preview first."
            )
            return
        
        # Execute immediately without an extra confirmation dialog; UI already shows planned actions.
        
        # Set syncing state
        self.is_syncing = True
        
        # Disable buttons during execution
        self.sync_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        if self.confirm_button:
            self.confirm_button.config(state=tk.DISABLED)
        
        # Indicate execution phase has started without clearing the file preview lists
        for widget in self.folder_widgets.values():
            widget.update_status("Executing...", "orange")
        
        # Start background worker to execute planned actions
        folder_paths = [Path(p) for p in self.selected_folders]
        worker = SyncWorker(self.sync_engine, folder_paths, self.planned_actions)
        worker.start()
    
    def _process_events(self):
        """Process events from the event queue periodically."""
        # [Modified] by openai/gpt-5.1 | 2025-11-16_01
        
        # Process all events currently in the queue
        while not self.event_queue.empty():
            try:
                event = self.event_queue.get_nowait()
                
                # Handle different event types using the current ProgressEvent schema
                if event.event_type == EventType.SCAN_START:
                    # Global scan start – mark all folders as scanned
                    for widget in self.folder_widgets.values():
                        widget.update_status("Scanned", "green")
                
                elif event.event_type == EventType.SCAN_FILE:
                    # Per-folder scan notification when folder is available
                    folder_widget = self.folder_widgets.get(event.folder)
                    if folder_widget:
                        folder_widget.update_status("Scanned", "green")
                
                elif event.event_type == EventType.COPY:
                    # A file was copied; show generic syncing state
                    for widget in self.folder_widgets.values():
                        widget.update_status("Syncing...", "orange")
                
                elif event.event_type == EventType.SKIP:
                    # In dry-run, files are skipped; detailed per-file preview is handled
                    # in the planning stage, so we keep the UI unchanged here.
                    pass
                
                elif event.event_type == EventType.ERROR:
                    # Show a generic error state; detailed message goes to the log
                    for widget in self.folder_widgets.values():
                        widget.update_status("Error during sync", "red")
                
                elif event.event_type == EventType.COMPLETE:
                    # Re-enable buttons when the engine signals completion
                    self.is_syncing = False
                    self.sync_button.config(state=tk.NORMAL)
                    self.browse_button.config(state=tk.NORMAL)
                    
                    # Update folder statuses to a clear completed state
                    if self.config.get("dry_run", False):
                        for widget in self.folder_widgets.values():
                            widget.update_status("Dry run complete", "blue")
                    else:
                        for widget in self.folder_widgets.values():
                            widget.update_status("Completed", "green")
                    
                    # For real executions, update preview header and mark files as replaced
                    if not self.config.get("dry_run", False):
                        for widget in self.folder_widgets.values():
                            # Update header from "will be" to "are now"
                            if hasattr(widget, "update_preview_header_to_completed"):
                                widget.update_preview_header_to_completed()
                            
                            # Mark each file row with checkmark
                            preview_rows = getattr(widget, "_preview_rows", {})
                            for rel_key in list(preview_rows.keys()):
                                if hasattr(widget, "mark_preview_replaced"):
                                    widget.mark_preview_replaced(rel_key)
    
                        # Also show any .bak backup files that now exist on disk
                        self._update_bak_previews()
                    
                    # Completion status is communicated via folder status and preview updates.
                
            except queue.Empty:
                break
        
        # Schedule next check (100ms from now)
        self.root.after(100, self._process_events)
    
    def _open_settings_window(self):
        """Open the settings configuration window."""
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-11-16_01

        # Create modal window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("600x520")
        settings_window.transient(self.root)
        settings_window.grab_set()
        settings_window.configure(bg=DARK_BG)

        # Main frame with padding
        main_frame = ttk.Frame(settings_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Sync Configuration",
            font=("TkDefaultFont", 12, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Backup mode
        backup_frame = ttk.Frame(main_frame)
        backup_frame.pack(fill=tk.X, pady=5)
        ttk.Label(backup_frame, text="Backup Mode:").pack(side=tk.LEFT)
        backup_var = tk.StringVar(value=self.config.get("backup_mode", "timestamped"))
        backup_combo = ttk.Combobox(
            backup_frame,
            textvariable=backup_var,
            values=["timestamped", "none"],
            state="readonly",
            width=15
        )
        backup_combo.pack(side=tk.LEFT, padx=(10, 0))

        # Preserve mtime
        preserve_var = tk.BooleanVar(value=self.config.get("preserve_mtime", True))
        preserve_check = ttk.Checkbutton(
            main_frame,
            text="Preserve modification times",
            variable=preserve_var
        )
        preserve_check.pack(fill=tk.X, pady=5)

        # Dry run
        dryrun_var = tk.BooleanVar(value=self.config.get("dry_run", False))
        dryrun_check = ttk.Checkbutton(
            main_frame,
            text="Dry run (preview changes only)",
            variable=dryrun_var
        )
        dryrun_check.pack(fill=tk.X, pady=5)

        # Ignore patterns
        ignore_frame = ttk.Frame(main_frame)
        ignore_frame.pack(fill=tk.X, pady=5)
        ttk.Label(ignore_frame, text="Ignore Patterns:").pack(anchor=tk.W)
        ttk.Label(
            ignore_frame,
            text="(comma-separated; wraps automatically)",
            font=("TkDefaultFont", 8)
        ).pack(anchor=tk.W)

        current_patterns = self.config.get("ignore_patterns", [])
        patterns_str = ", ".join(current_patterns) if current_patterns else ""
        ignore_text = tk.Text(
            ignore_frame,
            height=5,
            wrap="word",
            bg=DARK_BG_ALT,
            fg=FG_PRIMARY,
            insertbackground=FG_PRIMARY,
        )
        ignore_text.insert("1.0", patterns_str)
        ignore_text.pack(fill=tk.X, pady=(5, 0))

        # Favorite folders from config (folders_faves)
        faves_frame = ttk.Frame(main_frame)
        faves_frame.pack(fill=tk.X, pady=5)
        ttk.Label(faves_frame, text="Favorite Folders (config.txt):").pack(anchor=tk.W)
        ttk.Label(
            faves_frame,
            text="(comma-separated folder paths; wraps automatically)",
            font=("TkDefaultFont", 8)
        ).pack(anchor=tk.W)

        current_faves = self.config.get("folders_faves", [])
        faves_str = ", ".join(current_faves) if current_faves else ""
        faves_text = tk.Text(
            faves_frame,
            height=8,
            wrap="word",
            bg=DARK_BG_ALT,
            fg=FG_PRIMARY,
            insertbackground=FG_PRIMARY,
        )
        faves_text.insert("1.0", faves_str)
        faves_text.pack(fill=tk.X, pady=(5, 0))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(15, 0))

        # Cancel button
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=settings_window.destroy,
            style="AF.TButton",
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Save button
        save_button = ttk.Button(
            button_frame,
            text="Save",
            style="AF.TButton",
            command=lambda: self._save_settings(
                settings_window,
                backup_var.get(),
                preserve_var.get(),
                dryrun_var.get(),
                ignore_text.get("1.0", "end"),
                faves_text.get("1.0", "end")
            )
        )
        save_button.pack(side=tk.LEFT, padx=5)
    
    def _save_settings(
        self,
        window,
        backup_mode,
        preserve_mtime,
        dry_run,
        ignore_patterns_str,
        folders_faves_str,
    ):
        """Save settings to config and persist to file.
        
        Args:
            window: The settings window to close
            backup_mode: The backup mode setting
            preserve_mtime: Whether to preserve modification times
            dry_run: Whether to run in dry-run mode
            ignore_patterns_str: Comma-separated ignore patterns
            folders_faves_str: Comma-separated favorite folder paths
        """
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-11-16_01

        # Parse ignore patterns
        patterns = [p.strip() for p in ignore_patterns_str.split(",") if p.strip()]

        # Parse favorite folders (folders_faves)
        raw_faves = [p.strip() for p in folders_faves_str.split(",") if p.strip()]
        normalized_faves = []
        for fav in raw_faves:
            try:
                normalized_faves.append(file_path_utils.normalize_path(fav))
            except Exception as exc:
                # Fail soft on bad paths; keep original string
                print(f"Error normalizing favorite folder from settings {fav!r}: {exc}")
                normalized_faves.append(fav)

        # Update config
        self.config["backup_mode"] = backup_mode
        self.config["preserve_mtime"] = preserve_mtime
        self.config["dry_run"] = dry_run
        self.config["ignore_patterns"] = patterns
        self.config["folders_faves"] = normalized_faves

        # Keep in-memory favorites in sync with config
        self.favorite_folders = list(normalized_faves)

        # Persist to file
        config_sync.save_config(self.config)

        # Update status displays
        self._update_dry_run_status()
        self._update_ignore_patterns_display()

        # Close window
        window.destroy()

        # Show confirmation
        messagebox.showinfo(
            "Settings Saved",
            "Configuration has been saved successfully."
        )
    
    def _set_folder_favorite(self, folder_path: str, is_favorite: bool) -> None:
        """Add or remove a folder from the favorites list and persist to config."""
        # [Created-or-Modified] by [LLM model] | 2025-11-15_01
        # Ignore missing or empty paths
        if not folder_path:
            return

        try:
            normalized = file_path_utils.normalize_path(folder_path)
        except Exception as exc:
            # Log and fail soft; GUI should not crash on bad path
            print(f"Error normalizing favorite folder path {folder_path!r}: {exc}")
            return

        changed = False

        if is_favorite:
            if normalized not in self.favorite_folders:
                self.favorite_folders.append(normalized)
                changed = True
        else:
            if normalized in self.favorite_folders:
                self.favorite_folders.remove(normalized)
                changed = True

        if changed:
            self._save_favorites_to_config()

    def _save_favorites_to_config(self) -> None:
        """Persist favorite folders to config."""
        # [Created] by openai/gpt-5.1 | 2025-11-15_01
        self.config["folders_faves"] = list(self.favorite_folders)
        config_sync.save_config(self.config)

    def _load_favorite_folders(self) -> None:
        """Load favorite folders into the selected folders list and update UI."""
        # [Modified] by openai/gpt-5.1 | 2025-11-15_02

        if not self.favorite_folders:
            messagebox.showinfo(
                "No Favorites",
                "No favorite folders are configured in config.txt."
            )
            return

        skipped: list[str] = []
        added_any = False

        for fav in self.favorite_folders:
            try:
                normalized = file_path_utils.normalize_path(fav)
            except Exception as exc:
                print(f"Error normalizing favorite folder {fav!r}: {exc}")
                skipped.append(str(fav))
                continue

            # Validate folder has a .roo directory
            if not file_path_utils.has_roo_dir(normalized):
                skipped.append(normalized)
                continue

            if normalized not in self.selected_folders:
                self.selected_folders.append(normalized)
                added_any = True

        if added_any:
            self._update_folder_list_ui()

        if skipped:
            msg_lines = ["Some favorites are invalid and were skipped:"] + skipped
            msg = "\n".join(msg_lines)
            print(msg)
            # Optional UX: inform the user once about skipped favorites
            messagebox.showinfo("Favorites Skipped", msg)

    def _save_current_selection_as_favorites(self) -> None:
        """Save the current selected_folders as the new favorites and persist."""
        # [Created-or-Modified] by [LLM model] | 2025-11-15_02
        favs: list[str] = []
        for p in self.selected_folders:
            try:
                favs.append(file_path_utils.normalize_path(p))
            except Exception as exc:
                print(f"Error normalizing selected folder for saving favorites {p!r}: {exc}")
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for p in favs:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        self.favorite_folders = unique
        self._save_favorites_to_config()
        messagebox.showinfo("Favorites Saved", "Favorites saved from current selection.")
        
    def _delete_bak_files(self) -> None:
        """Delete all .bak backup files in the listed folders."""
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-11-16_02
        if not self.selected_folders:
            messagebox.showinfo(
                "Delete .bak Files",
                "No folders are selected. Select folders before deleting backups."
            )
            return
        
        # Proceed immediately without an extra confirmation dialog to keep cleanup fast.
        deleted_count = 0
        errors: list[str] = []
        
        for folder in self.selected_folders:
            base_path = Path(folder)
            if not base_path.exists():
                continue
            
            # Collect all .bak files first to avoid generator iteration issues during deletion
            bak_files = list(base_path.rglob("*.bak"))
            
            # Delete all .bak files anywhere under this base folder
            for bak in bak_files:
                try:
                    bak.unlink()
                    deleted_count += 1
                except OSError as exc:
                    errors.append(f"{bak}: {exc}")
        
        if deleted_count == 0:
            messagebox.showinfo(
                "Delete .bak Files",
                "No .bak backup files were found to delete in the listed folders."
            )
        else:
            if errors:
                print("Some .bak files could not be deleted:\n" + "\n".join(errors))

        # After deletion, refresh only the .bak backup previews
        # so the executed/updated file list remains visible until the next Scan.
        self._update_bak_previews()

    def _rescan_after_bak_delete(self) -> None:
        """Re-scan folders to refresh planned file list after deleting backups."""
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-11-16_02
        if self.is_syncing:
            return
        if len(self.selected_folders) < 2:
            return
        try:
            folder_paths = [Path(p) for p in self.selected_folders]
            file_index = self.sync_engine.scan_folders(folder_paths)
            actions = self.sync_engine.plan_actions(file_index)
        except Exception as exc:
            # Fail soft; log error but keep GUI responsive
            print(f"Rescan after .bak delete failed: {exc}")
            return

        # Replace existing planned actions and previews with fresh scan results
        self.planned_actions = actions
        self._update_overwrite_previews()

        # Clear any queued scan events so they don't overwrite the preview status
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break

    def _update_dry_run_status(self):
        """Update the dry run status label based on current config."""
        # [Modified] by Claude Sonnet 4.5 | 2025-11-13_06

        if self.dry_run_label:
            if self.config.get("dry_run", False):
                self.dry_run_label.config(
                    text="⚠ DRY RUN MODE: No files will be modified",
                    foreground="red",
                    font=("TkDefaultFont", 9, "bold")
                )
            else:
                self.dry_run_label.config(text="")
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling for the folder canvas.
        
        Args:
            event: The mouse wheel event
        """
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-11-16_01
        # Only respond to events originating from the main window (not modal dialogs)
        if event.widget.winfo_toplevel() is not self.root:
            return
        self.folder_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _update_ignore_patterns_display(self):
        """Update the ignore patterns display label based on current config."""
        # [Modified] by Claude Sonnet 4.5 | 2025-11-13_05

        if self.ignore_patterns_label:
            self.ignore_patterns_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()