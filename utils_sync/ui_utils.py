# [Modified] by Claude Sonnet 4.5 | 2025-11-13_02
"""
UI utility components for the file sync application.
Provides reusable tkinter widgets and UI helpers.
"""
import tkinter as tk
from tkinter import ttk

class FolderItem:
    """A UI component representing a single folder in the folder list."""
    # [Modified] by Claude Sonnet 4.5 | 2025-11-13_02
    
    def __init__(self, parent, folder_path: str, remove_callback):
        """Initialize a folder item widget.
        
        Args:
            parent: The parent tkinter widget
            folder_path: The full path to the folder
            remove_callback: Callback function to call when remove button is clicked
        """
        # Create main frame for this folder item
        self.frame = ttk.Frame(parent, relief=tk.FLAT, borderwidth=0)
        
        # Store folder path
        self.folder_path = folder_path
        
        # Create label showing the folder path
        self.label = ttk.Label(
            self.frame,
            text=folder_path,
            anchor=tk.W
        )
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5), pady=2)
        
        # Create progress bar
        self.progress_bar = ttk.Progressbar(
            self.frame,
            mode="determinate",
            length=100
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 5), pady=2)
        self.progress_bar["value"] = 0
        
        # Create status label
        self.status_label = ttk.Label(
            self.frame,
            text="",
            anchor=tk.W,
            width=15
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 5), pady=2)
        
        # Create remove button
        self.remove_button = ttk.Button(
            self.frame,
            text="X",
            width=3,
            command=lambda: remove_callback(folder_path)
        )
        self.remove_button.pack(side=tk.RIGHT, padx=(0, 5), pady=2)
    
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
    
    def reset_status(self):
        """Reset the status label and progress bar to initial states."""
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_02
        self.status_label.config(text="", foreground="black")
        self.progress_bar["value"] = 0