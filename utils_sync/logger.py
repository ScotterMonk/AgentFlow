# Modified by gemini-flash-latest | 2025-11-13_01
"""
Thread-safe logging utility for file sync operations.

This module provides a simple, thread-safe logging system that writes to both
a rotating log file and a human-readable plan log file. It integrates with
the ProgressEvent system to track sync operations.

Usage:
    from utils_sync.logger import init_logger, log_info, log_error, log_event
    from utils_sync.progress_events import make_event, EventType
    
    # Initialize logger (typically done once at startup)
    init_logger()
    
    # Log simple messages
    log_info("Starting sync operation", folder="my_folder")
    log_error("Failed to copy file", file_path="test.txt")
    
    # Log progress events
    event = make_event(EventType.COPY, file_path="test.txt", message="Copied file")
    log_event(event)
"""
import datetime
import json
import logging
import logging.handlers
import os
import threading
from pathlib import Path
from typing import Optional, Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from utils_sync.progress_events import ProgressEvent, EventType

# Module-level state
_lock = threading.Lock()
_log_dir: Optional[Path] = None
_plan_log_path: Optional[Path] = None
_rolling_log_path: Optional[Path] = None
_logger: Optional[logging.Logger] = None
_initialized = False


# Modified by gemini-flash-latest | 2025-11-13_01
def init_logger(log_dir: Optional[str] = None, plan_log_path: Optional[str] = None) -> None:
    """
    Initialize the logging system with thread-safe rotating file handler.
    
    This function must be called before using any logging functions. It sets up
    a RotatingFileHandler with 1MB max size and 5 backup files, ensuring proper
    log rotation and thread safety.
    
    Args:
        log_dir: Directory for rolling log files (default: "logs" under project root)
        plan_log_path: Path to plan log file (default: .roo/docs/plans/plan_251113_file_sync_log.md)
    
    Raises:
        OSError: If directories cannot be created due to permissions or other OS errors
    
    Example:
        >>> init_logger()  # Use defaults
        >>> init_logger(log_dir="custom_logs", plan_log_path="my_plan.md")
    """
    global _log_dir, _plan_log_path, _rolling_log_path, _logger, _initialized
    
    with _lock:
        if _initialized:
            return
        
        # Determine project root (parent of utils_sync directory)
        project_root = Path(__file__).parent.parent
        
        # Set up log directory
        if log_dir is None:
            _log_dir = project_root / "logs"
        else:
            _log_dir = Path(log_dir)
        
        # Create log directory if it doesn't exist
        try:
            _log_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            # Log error to plan log if possible, otherwise raise
            error_msg = f"Failed to create log directory {_log_dir}: {e}"
            if plan_log_path:
                try:
                    _write_plan_log_entry(error_msg, Path(plan_log_path))
                except Exception:
                    pass
            raise OSError(error_msg) from e
        
        # Set up rolling log path (changed from file_sync.log to sync_utility.log)
        _rolling_log_path = _log_dir / "sync_utility.log"
        
        # Set up plan log path
        if plan_log_path is None:
            _plan_log_path = project_root / ".roo" / "docs" / "plans" / "plan_251113_file_sync_log.md"
        else:
            _plan_log_path = Path(plan_log_path)
        
        # Ensure plan log directory exists
        try:
            _plan_log_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            error_msg = f"Failed to create plan log directory {_plan_log_path.parent}: {e}"
            raise OSError(error_msg) from e
        
        # Set up Python logging with RotatingFileHandler
        _logger = logging.getLogger("sync_utility")
        _logger.setLevel(logging.INFO)
        
        # Create rotating file handler (1MB max, 5 backups)
        handler = logging.handlers.RotatingFileHandler(
            _rolling_log_path,
            maxBytes=1024 * 1024,  # 1 MB
            backupCount=5,
            encoding="utf-8"
        )
        
        # Set format: timestamp - level - module name - message
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        _logger.addHandler(handler)
        
        _initialized = True


# Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
def _ensure_initialized() -> None:
    """
    Ensure logger is initialized before use.
    
    Raises:
        RuntimeError: If logger has not been initialized via init_logger()
    """
    if not _initialized:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")


# Modified by gemini-flash-latest | 2025-11-13_01
def _write_json_log(level: str, message: str, meta: Dict[str, Any]) -> None:
    """
    Write a log entry using Python's logging system with metadata as JSON.
    
    Args:
        level: Log level (info, error, etc.)
        message: Log message
        meta: Additional metadata dictionary
    """
    _ensure_initialized()
    
    # Format message with JSON metadata
    log_message = f"{message} | {json.dumps(meta)}"
    
    # Use appropriate logging level
    if level == "error":
        _logger.error(log_message)
    elif level == "warning":
        _logger.warning(log_message)
    elif level == "event":
        _logger.info(log_message)
    else:
        _logger.info(log_message)


# Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
def _write_plan_log_entry(message: str, plan_log_path: Optional[Path] = None) -> None:
    """
    Write a human-readable entry to the plan log file.
    
    Format: "YYYY-mm-dd HH:MM:SS; <message>"
    
    Args:
        message: Message to log
        plan_log_path: Optional override for plan log path
    """
    if plan_log_path is None:
        _ensure_initialized()
        plan_log_path = _plan_log_path
    
    # Use UTC time formatted as local-style timestamp (matching existing log format)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp}; {message}\n"
    
    with _lock:
        try:
            with open(plan_log_path, "a", encoding="utf-8") as f:
                f.write(log_line)
        except OSError as e:
            # If we can't write to plan log, there's nowhere else to log
            # Just raise the error
            raise OSError(f"Failed to write to plan log {plan_log_path}: {e}") from e


# Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
def log_info(message: str, **meta) -> None:
    """
    Log an informational message.
    
    Writes a JSON entry to the rolling log with level "info".
    
    Args:
        message: The message to log
        **meta: Additional metadata as keyword arguments
    
    Example:
        >>> log_info("Processing file", file_path="test.txt", size=1024)
    """
    _write_json_log("info", message, meta)


# Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
def log_error(message: str, **meta) -> None:
    """
    Log an error message.
    
    Writes a JSON entry to the rolling log with level "error".
    
    Args:
        message: The error message to log
        **meta: Additional metadata as keyword arguments
    
    Example:
        >>> log_error("Failed to copy file", file_path="test.txt", error="Permission denied")
    """
    _write_json_log("error", message, meta)


# Created by anthropic/claude-sonnet-4.5 | 2025-11-13_01
def log_event(event: "ProgressEvent") -> None:
    """
    Log a ProgressEvent to both rolling log and plan log.
    
    Writes a compact JSON line to the rolling log and appends a human-readable
    line to the plan log for major events (SCAN_START, COPY, ERROR, COMPLETE).
    
    Args:
        event: ProgressEvent instance to log
    
    Example:
        >>> from utils_sync.progress_events import make_event, EventType
        >>> event = make_event(EventType.COPY, file_path="test.txt", message="Copied file")
        >>> log_event(event)
    """
    _ensure_initialized()
    
    # Import here to avoid circular dependency
    from utils_sync.progress_events import EventType
    
    # Build metadata from event
    meta = {
        "event_type": event.event_type.value,
        "folder": event.folder,
        "file_path": event.file_path,
        "timestamp": event.timestamp
    }
    
    # Write to rolling log
    _write_json_log("event", event.message, meta)
    
    # Write to plan log for major events
    major_events = {
        EventType.SCAN_START,
        EventType.COPY,
        EventType.ERROR,
        EventType.COMPLETE
    }
    
    if event.event_type in major_events:
        # Create human-readable summary
        if event.event_type == EventType.SCAN_START:
            summary = f"Scan started: {event.folder}"
        elif event.event_type == EventType.COPY:
            summary = f"Copied: {event.file_path}"
        elif event.event_type == EventType.ERROR:
            summary = f"Error: {event.message}"
        elif event.event_type == EventType.COMPLETE:
            summary = f"Complete: {event.message}"
        else:
            summary = event.message
        
        _write_plan_log_entry(summary)