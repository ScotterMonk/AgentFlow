# [Created] by Claude Sonnet 4.5 | 2025-11-13_01
"""
Background worker thread for running file synchronization operations.

This module provides the SyncWorker class which runs the SyncEngine
in a separate thread to avoid blocking the main application thread.
"""
import threading
from pathlib import Path
from typing import List
from .sync_core import SyncEngine
from .progress_events import EventType

class SyncWorker(threading.Thread):
    """
    Background worker thread that orchestrates the sync process.
    
    This class inherits from threading.Thread and runs the complete
    scan-plan-execute sequence of the SyncEngine in the background.
    All progress and errors are communicated via the SyncEngine's
    event queue.
    """
    # [Created] by Claude Sonnet 4.5 | 2025-11-13_01
    
    def __init__(self, sync_engine: SyncEngine, folders: List[Path], actions=None):
        """
        Initialize the SyncWorker.
        
        Args:
            sync_engine: Pre-configured SyncEngine instance
            folders: List of folder paths to synchronize
            actions: Optional precomputed list of planned actions to execute.
                     If provided, the worker will skip scan/plan and only execute.
        """
        # [Modified] by openai/gpt-5.1 | 2025-11-14_01
        super().__init__()
        self.sync_engine = sync_engine
        self.folders = folders
        self.actions = actions
        # Set as daemon thread so it doesn't prevent app shutdown
        self.daemon = True
    
    def run(self):
        """
        Execute the sync process in the background thread.
        
        Depending on initialization, this either:
        1) Runs full scan → plan → execute using the SyncEngine, or
        2) Executes a precomputed list of actions directly.
        
        All progress is communicated via the SyncEngine's event queue.
        Any exceptions are caught and emitted as ERROR events.
        """
        # [Modified] by openai/gpt-5.1 | 2025-11-14_01
        try:
            # When no actions are precomputed, run full scan/plan/execute
            if self.actions is None:
                file_index = self.sync_engine.scan_folders(self.folders)
                actions = self.sync_engine.plan_actions(file_index)
            else:
                actions = self.actions
            
            # Execute the planned actions
            self.sync_engine.execute_actions(actions)
            
        except Exception as e:
            # Emit error event if anything goes wrong
            error_msg = f"Sync worker error: {str(e)}"
            self.sync_engine._emit_event(EventType.ERROR, message=error_msg)