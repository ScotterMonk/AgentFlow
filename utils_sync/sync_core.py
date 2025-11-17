# [Modified] by anthropic/claude-sonnet-4.5 | 2025-11-13_01
"""
Core sync engine for file synchronization operations.

This module provides the SyncEngine class which orchestrates the file sync
process through three main phases: scanning folders, planning actions, and
executing those actions. Progress events are emitted throughout for monitoring.
"""
import datetime
import os
import queue
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any

from . import file_path_utils
from .progress_events import EventType, ProgressEvent


class SyncEngine:
    # Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
    """
    Orchestrates file synchronization operations.
    
    The sync engine manages the complete sync workflow:
    1. Scan folders to build a file index
    2. Plan copy/delete actions based on the index
    3. Execute planned actions while emitting progress events
    
    Attributes:
        config: Configuration dictionary containing sync settings
        event_queue: Thread-safe queue for emitting ProgressEvent instances
    """
    
    def __init__(self, config: Dict[str, Any], event_queue: queue.Queue):
        # Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
        """
        Initialize the sync engine.
        
        Args:
            config: Configuration dictionary with sync settings
            event_queue: Thread-safe queue for emitting ProgressEvent instances
        """
        self.config = config
        self.event_queue = event_queue
    
    def scan_folders(self, folders: List[Path]) -> Dict[str, List[Dict[str, Any]]]:
        # [Modified] by google/gemini-2.5-pro | 2025-11-13_02
        """
        Scan folders to build a file index.
        
        Recursively scans the .roo/ subdirectory within each provided folder,
        collecting file metadata and building an index keyed by relative paths.
        
        Args:
            folders: List of folder paths to scan
        
        Returns:
            Dictionary mapping relative paths (within .roo) to lists of file metadata dicts.
            Each file dict contains: path, mtime, size, base_folder
        """
        # Emit scan start event
        self._emit_event(EventType.SCAN_START, message="Starting folder scan")
        
        # Initialize file index - maps relative paths to list of file metadata
        file_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Get ignore patterns from config
        raw_ignore_patterns = self.config.get("ignore_patterns", [])
        # Normalize patterns so entries like ".roo/docs" or ".roo\docs" behave as
        # "docs" relative to the .roo/ directory. This allows users to copy/paste
        # subpaths directly from their editor while still matching our internal
        # .roo-scoped relative paths.
        ignore_patterns = []
        for pattern in raw_ignore_patterns:
            if not pattern:
                continue
            norm = str(pattern).replace("\\", "/")
            if norm.startswith(".roo/"):
                norm = norm[len(".roo/"):]
            ignore_patterns.append(norm)
        
        # Scan each folder
        for folder in folders:
            # Validate folder contains .roo directory
            if not file_path_utils.has_roo_dir(folder):
                self._emit_event(
                    EventType.ERROR,
                    folder=str(folder),
                    message=f"Folder does not contain .roo directory: {folder}"
                )
                continue
            
            # Define scan root as .roo subdirectory
            scan_root = folder.joinpath(".roo")
            
            # Recursively scan all files in .roo directory
            for item_path in scan_root.rglob("*"):
                # Check if any part of relative path matches ignore patterns
                relative_parts = item_path.relative_to(scan_root).parts
                if any(pattern in relative_parts for pattern in ignore_patterns):
                    continue
                
                # Process only files (skip directories)
                if item_path.is_file():
                    # Get file stats
                    stats = item_path.stat()
                    mtime = stats.st_mtime
                    size = stats.st_size
                    
                    # Get relative path within .roo scope
                    relative_path = file_path_utils.get_roo_relative_path(item_path, folder)
                    
                    # Emit scan file event
                    self._emit_event(
                        EventType.SCAN_FILE,
                        folder=str(folder),
                        file_path=str(relative_path),
                        message=f"Scanning: {relative_path}"
                    )
                    
                    # Add file metadata to index
                    file_index[relative_path].append({
                        "path": item_path,
                        "mtime": mtime,
                        "size": size,
                        "base_folder": folder
                    })
            
            # After scanning .roo, attempt to include root-level allowlisted files
            root_allowlist = self.config.get("root_allowlist", [])
            for allowlist_entry in root_allowlist:
                candidate_path = folder / allowlist_entry
                # Include only if: exists, is_file, not symlink
                if (candidate_path.exists() and
                    candidate_path.is_file() and
                    not candidate_path.is_symlink()):
                    stats = candidate_path.stat()
                    # Use synthetic relative key = filename only
                    synthetic_key = allowlist_entry
                    self._emit_event(
                        EventType.SCAN_FILE,
                        folder=str(folder),
                        file_path=synthetic_key,
                        message=f"Scanning allowlisted root file: {synthetic_key}"
                    )
                    file_index[synthetic_key].append({
                        "path": candidate_path,
                        "mtime": stats.st_mtime,
                        "size": stats.st_size,
                        "base_folder": folder
                    })
        
        return file_index
    
    def plan_actions(self, file_index: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        # [Modified] by openai/gpt-5.1 | 2025-11-16_01
        """
        Plan copy actions based on file index.
        
        Compares files across folders and creates copy actions for files that need
        to be synchronized. Uses modification time (mtime) to determine the source
        file (most recently modified) and identifies destinations that need updating.
        
        In addition to updating existing peers, this method will also plan copy
        actions for folders that are missing a given file (including root-level
        allowlisted files such as ".roomodes") so that new files are created
        where needed.
        
        Args:
            file_index: File index from scan_folders(), mapping relative paths to
                        lists of file metadata dictionaries.
        
        Returns:
            List of action dictionaries. Each action contains:
            - action: 'copy'
            - source_path: Path object of the source file
            - destination_path: Path object of the destination file
            - relative_path: Relative path within .roo directory or synthetic key
            - source_mtime: Modification time of source file
            - destination_mtime: Modification time of destination file (or None
              when the destination did not previously exist)
        """
        actions: List[Dict[str, Any]] = []
        
        # Collect all base folders that participated in the scan. This lets us
        # create actions for folders that are missing a given file entirely.
        all_base_folders = set()
        for group in file_index.values():
            for meta in group:
                base_folder = meta.get("base_folder")
                if base_folder is not None:
                    all_base_folders.add(base_folder)
        
        # Iterate through each file group in the index
        for relative_path, file_group in file_index.items():
            # Skip if only one file exists and there are no other folders to sync to
            if len(file_group) <= 1 and len(all_base_folders) <= 1:
                continue
            
            # Find the file with the maximum mtime (most recently modified)
            source_file = max(file_group, key=lambda f: f["mtime"])
            
            # Get all other files as potential destinations (existing peers)
            destination_files = [f for f in file_group if f is not source_file]
            
            # Track which base folders already have this file
            present_base_folders = {
                f["base_folder"] for f in file_group if "base_folder" in f
            }
            # Folders that were scanned but do not yet have this file
            missing_base_folders = all_base_folders - present_base_folders
            
            # Create copy actions for existing destinations that need updating
            for dest_file in destination_files:
                # Only create action if source is newer than destination
                if source_file["mtime"] > dest_file["mtime"]:
                    action = {
                        "action": "copy",
                        "source_path": source_file["path"],
                        "destination_path": dest_file["path"],
                        "relative_path": relative_path,
                        "source_mtime": source_file["mtime"],
                        "destination_mtime": dest_file["mtime"],
                    }
                    actions.append(action)
            
            # Create copy actions for folders that are missing this file entirely.
            # This applies both to .roo-relative paths and root-level allowlisted
            # files (which use a synthetic key such as ".roomodes").
            for base_folder in missing_base_folders:
                # Determine destination path:
                # - If the relative path contains a '/', treat it as under .roo/.
                # - Otherwise, treat it as a root-level allowlisted file.
                rel_str = str(relative_path)
                if "/" in rel_str:
                    destination_path = base_folder / ".roo" / Path(rel_str)
                else:
                    destination_path = base_folder / rel_str
                
                action = {
                    "action": "copy",
                    "source_path": source_file["path"],
                    "destination_path": destination_path,
                    "relative_path": relative_path,
                    "source_mtime": source_file["mtime"],
                    # Destination did not previously exist in the index
                    "destination_mtime": None,
                }
                actions.append(action)
        
        return actions
    
    def execute_actions(self, actions: List[Dict[str, Any]]) -> None:
        # [Modified] by anthropic/claude-sonnet-4.5 | 2025-11-13_01
        """
        Execute planned copy actions with safe atomic operations.
        
        Performs file copy operations with the following features:
        - Respects dry_run mode (skips actual copying)
        - Creates timestamped backups when backup_mode is enabled
        - Uses atomic copy operations (temp file + rename)
        - Emits progress events for monitoring
        - Handles errors gracefully
        
        Args:
            actions: List of action dictionaries from plan_actions()
        """
        # Get configuration settings
        dry_run = self.config.get("dry_run", False)
        backup_mode = self.config.get("backup_mode", "none")
        
        # Execute each action
        for action in actions:
            if action["action"] == "copy":
                source_path = action["source_path"]
                destination_path = action["destination_path"]
                relative_path = action["relative_path"]
                
                # Skip if dry run mode
                if dry_run:
                    self._emit_event(
                        EventType.SKIP,
                        file_path=str(relative_path),
                        message="Dry run, skipping copy"
                    )
                    continue
                
                # Perform file copy with error handling
                try:
                    # Create timestamped backup if needed
                    if backup_mode == "timestamped" and destination_path.exists():
                        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                        backup_path = Path(str(destination_path) + f"_{timestamp}.bak")
                        os.rename(destination_path, backup_path)
                    
                    # Ensure parent directory exists
                    destination_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Atomic copy: copy to temp file, then rename
                    temp_path = destination_path.parent / f".tmp_{destination_path.name}"
                    shutil.copy2(source_path, temp_path)
                    os.replace(temp_path, destination_path)
                    
                    # Emit success event
                    self._emit_event(
                        EventType.COPY,
                        file_path=str(relative_path),
                        message=f"Copied: {source_path} -> {destination_path}"
                    )
                    
                except Exception as e:
                    # Emit error event and continue
                    self._emit_event(
                        EventType.ERROR,
                        file_path=str(relative_path),
                        message=f"Error copying file: {str(e)}"
                    )
                    continue
        
        # Emit completion event
        self._emit_event(EventType.COMPLETE, message="Sync complete")
    
    def _emit_event(self, event_type: EventType, **kwargs) -> None:
        # Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
        """
        Create and emit a progress event.
        
        Helper method to create ProgressEvent instances and put them on the queue.
        
        Args:
            event_type: Type of event from EventType enum
            **kwargs: Additional event parameters (folder, file_path, message)
        """
        event = ProgressEvent(
            event_type=event_type,
            folder=kwargs.get("folder", ""),
            file_path=kwargs.get("file_path", ""),
            message=kwargs.get("message", "")
        )
        self.event_queue.put(event)