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
from utils_sync import config_sync, file_path_utils
from utils_sync.sync_core import SyncEngine
from utils_sync.sync_worker import SyncWorker
from utils_sync.progress_events import ProgressEvent, EventType
from utils_sync.ui_utils import FolderItem

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
        
        # Set up main window
        self.root.title("Agentflow File Sync")
        window_width = self.config.get("window_width", 800)
        window_height = self.config.get("window_height", 600)
        self.root.geometry(f"{window_width}x{window_height}")
        
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
        
        # Store status label references
        self.dry_run_label = None
        self.ignore_patterns_label = None
        
        # Create UI widgets
        self._create_widgets()
        
        # Update status displays
        self._update_dry_run_status()
        self._update_ignore_patterns_display()
        
        # Start periodic event processing
        self._process_events()
    
    def _create_widgets(self):
        """Create and layout all UI widgets."""
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_01
        
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
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
        title_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)
        
        # Description label
        desc_label = ttk.Label(
            main_frame,
            text="Synchronize files across multiple folders with intelligent conflict resolution."
        )
        desc_label.grid(row=1, column=0, pady=(0, 5), sticky=tk.W)
        
        # Dry run status label
        self.dry_run_label = ttk.Label(main_frame, text="")
        self.dry_run_label.grid(row=2, column=0, pady=(0, 2), sticky=tk.W)
        
        # Ignore patterns label
        self.ignore_patterns_label = ttk.Label(main_frame, text="")
        self.ignore_patterns_label.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)
        
        # Folder list frame
        folder_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
        folder_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        folder_frame.columnconfigure(0, weight=1)
        folder_frame.rowconfigure(0, weight=1)
        
        # Create scrollable frame for folder list
        self.folder_list_frame = ttk.Frame(folder_frame)
        self.folder_list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Bottom button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        # Browse button
        self.browse_button = ttk.Button(
            button_frame,
            text="Browse...",
            command=self._open_folder_dialog
        )
        self.browse_button.grid(row=0, column=0, padx=(0, 5))
        
        # Sync button
        self.sync_button = ttk.Button(
            button_frame,
            text="Sync",
            command=self._start_sync
        )
        self.sync_button.grid(row=0, column=1, padx=(0, 5))
        
        # Settings button
        self.settings_button = ttk.Button(
            button_frame,
            text="Settings",
            command=self._open_settings_window
        )
        self.settings_button.grid(row=0, column=2)
    
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
        # [Modified] by Claude Sonnet 4.5 | 2025-11-13_02
        
        # Destroy all existing widgets in the folder list frame
        for widget in self.folder_list_frame.winfo_children():
            widget.destroy()
        
        # Clear folder widgets dictionary
        self.folder_widgets = {}
        
        # Create a FolderItem for each selected folder
        for folder_path in self.selected_folders:
            folder_item = FolderItem(
                self.folder_list_frame,
                folder_path,
                self._remove_folder
            )
            folder_item.frame.pack(fill=tk.X, padx=2, pady=2)
            
            # Store widget reference in dictionary
            self.folder_widgets[folder_path] = folder_item
    
    def _start_sync(self):
        """Start the sync process in a background thread."""
        # [Modified] by Claude Sonnet 4.5 | 2025-11-13_04
        
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
        
        # Pre-sync confirmation for real runs
        if not self.config.get("dry_run", False):
            confirm = messagebox.askyesno(
                "Confirm Sync",
                "WARNING: This is NOT a dry run. Files will be modified.\n\nAre you sure you want to proceed?"
            )
            if not confirm:
                return
        
        # Set syncing state
        self.is_syncing = True
        
        # Disable buttons
        self.sync_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        
        # Reset status of all folder widgets
        for widget in self.folder_widgets.values():
            widget.reset_status()
        
        # Create and start sync worker
        worker = SyncWorker(self.selected_folders, self.event_queue)
        worker.start()
    
    def _process_events(self):
        """Process events from the event queue periodically."""
        # [Modified] by Claude Sonnet 4.5 | 2025-11-13_02
        
        # Process all events currently in the queue
        while not self.event_queue.empty():
            try:
                event = self.event_queue.get_nowait()
                
                # Get the widget for this folder path
                widget = self.folder_widgets.get(event.folder_path)
                
                # Handle different event types
                if event.event_type == EventType.SCAN_START:
                    if widget:
                        widget.update_status("Scanning...", "blue")
                
                elif event.event_type == EventType.SCAN_FILE:
                    if widget and event.total > 0:
                        widget.update_progress(event.current, event.total)
                
                elif event.event_type == EventType.SCAN_COMPLETE:
                    if widget:
                        widget.update_status("Scan complete", "green")
                        widget.update_progress(100, 100)
                
                elif event.event_type == EventType.COPY_START:
                    # Update all widgets to show syncing status
                    for w in self.folder_widgets.values():
                        w.update_status("Syncing...", "orange")
                
                elif event.event_type == EventType.COPY_PROGRESS:
                    if widget and event.total > 0:
                        widget.update_progress(event.current, event.total)
                
                elif event.event_type == EventType.SKIP:
                    if widget:
                        widget.update_status("Up to date", "gray")
                
                elif event.event_type == EventType.COPY_COMPLETE:
                    if widget:
                        widget.update_status("Sync complete", "green")
                
                elif event.event_type == EventType.ERROR:
                    if widget:
                        widget.update_status(f"Error: {event.message}", "red")
                
                elif event.event_type == EventType.ALL_COMPLETE:
                    # Re-enable buttons
                    self.is_syncing = False
                    self.sync_button.config(state=tk.NORMAL)
                    self.browse_button.config(state=tk.NORMAL)
                    
                    # Show completion message
                    if self.config.get("dry_run", False):
                        messagebox.showinfo(
                            "Sync Complete",
                            "Dry run completed successfully.\n\nNo files were modified."
                        )
                    else:
                        messagebox.showinfo(
                            "Sync Complete",
                            "Synchronization completed successfully."
                        )
                
            except queue.Empty:
                break
        
        # Schedule next check (100ms from now)
        self.root.after(100, self._process_events)
    
    def _open_settings_window(self):
        """Open the settings configuration window."""
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_03
        
        # Create modal window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
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
            text="(comma-separated)",
            font=("TkDefaultFont", 8)
        ).pack(anchor=tk.W)
        
        current_patterns = self.config.get("ignore_patterns", [])
        patterns_str = ", ".join(current_patterns) if current_patterns else ""
        ignore_entry = ttk.Entry(ignore_frame, width=40)
        ignore_entry.insert(0, patterns_str)
        ignore_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(15, 0))
        
        # Cancel button
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=settings_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=lambda: self._save_settings(
                settings_window,
                backup_var.get(),
                preserve_var.get(),
                dryrun_var.get(),
                ignore_entry.get()
            )
        )
        save_button.pack(side=tk.LEFT, padx=5)
    
    def _save_settings(self, window, backup_mode, preserve_mtime, dry_run, ignore_patterns_str):
        """Save settings to config and persist to file.
        
        Args:
            window: The settings window to close
            backup_mode: The backup mode setting
            preserve_mtime: Whether to preserve modification times
            dry_run: Whether to run in dry-run mode
            ignore_patterns_str: Comma-separated ignore patterns
        """
        # [Modified] by Claude Sonnet 4.5 | 2025-11-13_04
        
        # Parse ignore patterns
        patterns = [p.strip() for p in ignore_patterns_str.split(",") if p.strip()]
        
        # Update config
        self.config["backup_mode"] = backup_mode
        self.config["preserve_mtime"] = preserve_mtime
        self.config["dry_run"] = dry_run
        self.config["ignore_patterns"] = patterns
        
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
    
    def _update_ignore_patterns_display(self):
        """Update the ignore patterns display label based on current config."""
        # [Modified] by Claude Sonnet 4.5 | 2025-11-13_05

        if self.ignore_patterns_label:
            self.ignore_patterns_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()