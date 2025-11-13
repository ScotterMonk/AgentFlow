# Created by openai/gpt-5-mini | 2025-11-13_01
"""
Progress event types and data structures for file sync operations.

This module provides event types and a dataclass for tracking progress
during file synchronization operations. Events are emitted at key stages
to enable logging, UI updates, and monitoring.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import datetime


class EventType(Enum):
    """Event types for file sync progress tracking."""
    SCAN_START = "scan_start"
    SCAN_FILE = "scan_file"
    COPY = "copy"
    SKIP = "skip"
    ERROR = "error"
    COMPLETE = "complete"


@dataclass
class ProgressEvent:
    """
    Represents a single progress event during file sync.
    
    Attributes:
        event_type: Type of event (from EventType enum)
        folder: Folder path related to the event
        file_path: File path related to the event
        message: Human-readable message describing the event
        timestamp: ISO8601 UTC timestamp when event was created
    """
    event_type: EventType
    folder: str = ""
    file_path: str = ""
    message: str = ""
    timestamp: Optional[str] = None


def make_event(
    event_type: EventType,
    folder: str = "",
    file_path: str = "",
    message: str = ""
) -> ProgressEvent:
    """
    Create a ProgressEvent with automatic timestamp.
    
    Args:
        event_type: Type of event (from EventType enum)
        folder: Folder path related to the event (default: "")
        file_path: File path related to the event (default: "")
        message: Human-readable message describing the event (default: "")
    
    Returns:
        ProgressEvent with ISO8601 UTC timestamp
    
    Example:
        >>> event = make_event(EventType.COPY, file_path="test.txt", message="Copied file")
        >>> event.event_type
        <EventType.COPY: 'copy'>
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    return ProgressEvent(
        event_type=event_type,
        folder=folder,
        file_path=file_path,
        message=message,
        timestamp=timestamp
    )