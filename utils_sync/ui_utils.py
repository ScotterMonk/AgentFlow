# [Modified] by Claude Sonnet 4.5 | 2025-11-13_02
"""
UI utility components for the file sync application.
Provides reusable tkinter widgets and UI helpers.
"""
import tkinter as tk
from tkinter import ttk

class FolderItem:
    """A UI component representing a single folder in the folder list."""
    # [Modified] by openai/gpt-5.1 | 2025-11-14_01
    
    def __init__(self, parent, folder_path: str, remove_callback):
        """Initialize a folder item widget.
        
        Args:
            parent: The parent tkinter widget
            folder_path: The full path to the folder
            remove_callback: Callback function to call when remove button is clicked
        """
        # Create main frame for this folder item
        self.frame = ttk.Frame(parent, relief=tk.FLAT, borderwidth=0)
        
        # Create a top row container for the main controls
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X)
        
        # Store folder path
        self.folder_path = folder_path
        
        # Create label showing the folder path
        self.label = ttk.Label(
            top_frame,
            text=folder_path,
            anchor=tk.W
        )
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5), pady=2)
        
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
        
        # Create remove button
        self.remove_button = ttk.Button(
            top_frame,
            text="X",
            width=3,
            command=lambda: remove_callback(folder_path)
        )
        self.remove_button.pack(side=tk.RIGHT, padx=(0, 5), pady=2)
        
        # Preview label for planned overwrites (shown under the main row)
        self.preview_label = ttk.Label(
            self.frame,
            text="",
            anchor=tk.W,
            justify=tk.LEFT,
            font=("TkDefaultFont", 8),
            foreground="gray"
        )
        self.preview_label.pack(fill=tk.X, padx=(20, 5), pady=(0, 2))
    
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
    
    def update_preview(self, lines):
        """Update the planned overwrite preview text for this folder item."""
        # [Created] by openai/gpt-5.1 | 2025-11-14_01
        if lines:
            text = "\n".join(f"- {line}" for line in lines)
        else:
            text = ""
        self.preview_label.config(text=text)
    
    def reset_status(self):
        """Reset the status label and progress bar to initial states."""
        # [Modified] by openai/gpt-5.1 | 2025-11-14_01
        self.status_label.config(text="", foreground="black")
        self.progress_bar["value"] = 0
        self.preview_label.config(text="")