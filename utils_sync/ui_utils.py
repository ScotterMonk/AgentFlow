# [Modified] by Claude Sonnet 4.5 | 2025-11-13_02
"""
UI utility components for the file sync application.
Provides reusable tkinter widgets and UI helpers.
"""
import tkinter as tk
from tkinter import ttk

class FolderItem:
    """A UI component representing a single folder in the folder list."""
    # [Modified] by openai/gpt-5.1 | 2025-11-14_02
    
    def __init__(self, parent, folder_path: str, remove_callback, overwrite_remove_callback=None,
                 toggle_favorite_callback=None, is_favorite: bool = False):
        """Initialize a folder item widget.
        
        Args:
            parent: The parent tkinter widget
            folder_path: The full path to the folder
            remove_callback: Callback function to call when remove button is clicked
            overwrite_remove_callback: Callback when an individual planned overwrite is removed
            toggle_favorite_callback: Callback when favorite star is toggled (receives folder_path, is_favorite)
            is_favorite: Whether this folder is currently marked as favorite
        """
        # [Modified] by openai/gpt-5-mini | 2025-11-15_01
        # Create main frame for this folder item
        self.frame = ttk.Frame(parent, relief=tk.FLAT, borderwidth=0)
        
        # Create a top row container for the main controls
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X)
        
        # Store folder path, callbacks, and favorite state
        self.folder_path = folder_path
        self.overwrite_remove_callback = overwrite_remove_callback
        self._toggle_favorite_callback = toggle_favorite_callback
        self.is_favorite = is_favorite
        
        # Create favorite toggle button
        # [Created] by openai/gpt-5-mini | 2025-11-15_01
        self.favorite_button = ttk.Button(
            top_frame,
            text="★" if self.is_favorite else "☆",
            width=3,
            command=self._on_favorite_toggle
        )
        self.favorite_button.pack(side=tk.LEFT, padx=(5, 2), pady=2)
        
        # Create label showing the folder path
        self.label = ttk.Label(
            top_frame,
            text=folder_path,
            anchor=tk.W
        )
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 5), pady=2)
        
        # Create progress bar
        self.progress_bar = ttk.Progressbar(
            top_frame,
            mode="determinate",
            length=100
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 5), pady=2)
        self.progress_bar["value"] = 0
        
        # Create status label
        self.status_label = ttk.Label(
            top_frame,
            text="",
            anchor=tk.W,
            width=15
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 5), pady=2)
        
        # Create remove button for the entire folder
        self.remove_button = ttk.Button(
            top_frame,
            text="X",
            width=3,
            command=lambda: remove_callback(folder_path)
        )
        self.remove_button.pack(side=tk.RIGHT, padx=(0, 5), pady=2)
        
        # Container for planned overwrite rows (shown under the main row)
        self.preview_frame = ttk.Frame(self.frame)
        self.preview_frame.pack(fill=tk.X, padx=(20, 5), pady=(0, 2))
        # Map relative file paths to the label widgets for their preview rows
        self._preview_rows = {}
    
    def update_status(self, text: str, color: str = "black"):
        """Update the status label text and color.
        
        Args:
            text: The status text to display
            color: The text color (default: "black")
        """
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_02
        self.status_label.config(text=text, foreground=color)
    
    def update_progress(self, current: int, total: int):
        """Update the progress bar value.
        
        Args:
            current: Current progress value
            total: Total value for completion
        """
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_02
        if total > 0:
            percentage = (current / total) * 100
            self.progress_bar["value"] = percentage
        else:
            self.progress_bar["value"] = 0
    
    def update_preview(self, items):
        """Update the planned overwrite preview UI for this folder item.
        
        Each item in `items` should be a dict with:
            - relative: Relative file path within the sync scope
            - timestamp: Human-readable last modified timestamp string
            - action: The underlying planned action object
        """
        # [Modified] by openai/gpt-5.1 | 2025-11-14_02
        # [Modified] by openai/gpt-5.1 | 2025-11-16_01
        
        # Clear any existing rows and label mapping
        for child in self.preview_frame.winfo_children():
            child.destroy()
        
        # Reset preview mapping so executed rows can be marked later
        self._preview_rows = {}
        
        if not items:
            return
        
        # Sort so that:
        # - Root-level files (no "/") appear first
        # - Then entries are grouped by their first path segment so "rules" comes before "rules-architect"
        # - Within each group, paths are sorted lexicographically, giving patterns like:
        #   "root" → "root/rules" → "root/rules-architect" → "root/rules-ask"
        def _sort_key(item):
            rel = item.get("relative", "") or ""
            rel_str = str(rel)
            
            # Root-level: no "/" in path
            if "/" not in rel_str:
                return (0, rel_str.lower())
            
            # Nested: group by first segment so "rules/..." sorts before "rules-architect/..."
            first_segment = rel_str.split("/", 1)[0]
            return (1, first_segment.lower(), rel_str.lower())
        
        sorted_items = sorted(items, key=_sort_key)
        
        for item in sorted_items:
            row_frame = ttk.Frame(self.preview_frame)
            row_frame.pack(fill=tk.X, pady=(0, 1))
            
            text = f"- {item.get('relative', '')}  {item.get('timestamp', '')}"
            label = ttk.Label(
                row_frame,
                text=text,
                anchor=tk.W,
                justify=tk.LEFT,
                font=("TkDefaultFont", 8),
                foreground="gray"
            )
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Track label widget by relative path for later updates (e.g., marking as replaced)
            rel_key = str(item.get("relative", "") or "")
            self._preview_rows[rel_key] = label
            
            # Per-file "X" button to remove this planned overwrite from the queue
            if self.overwrite_remove_callback is not None and "action" in item:
                remove_button = ttk.Button(
                    row_frame,
                    text="X",
                    width=2,
                    command=lambda action=item["action"]: self.overwrite_remove_callback(action)
                )
                remove_button.pack(side=tk.RIGHT, padx=(5, 0))
    
    def reset_status(self):
        """Reset the status label, progress bar, and preview area to initial states."""
        # [Modified] by openai/gpt-5.1 | 2025-11-14_02
        self.status_label.config(text="", foreground="black")
        self.progress_bar["value"] = 0
        for child in self.preview_frame.winfo_children():
            child.destroy()
        # Reset preview label mapping as well
        self._preview_rows = {}
    
    def mark_preview_replaced(self, relative_path: str) -> None:
        """Mark a single preview row as replaced for the given relative path."""
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-11-16_01
        if not relative_path:
            return
        key = str(relative_path)
        label = getattr(self, "_preview_rows", {}).get(key)
        if label is None:
            return
        # Prefix with a checkmark once and change color to green to indicate replacement
        current_text = label.cget("text")
        if not current_text.startswith("✓ "):
            label.config(text=f"✓ {current_text}", foreground="green")
    
    def _on_favorite_toggle(self):
        """Handle favorite button toggle.
        
        Flips the favorite state, updates the button text, and calls the callback if provided.
        """
        # [Created] by openai/gpt-5-mini | 2025-11-15_01
        self.is_favorite = not self.is_favorite
        self.favorite_button.config(text="★" if self.is_favorite else "☆")
        
        if self._toggle_favorite_callback is not None:
            self._toggle_favorite_callback(self.folder_path, self.is_favorite)