import argparse
import queue
import sys
from pathlib import Path

# [Created] by LLM model | 2025-11-13_01
"""
CLI wrapper for headless operation of the sync engine.

Usage:
    python cli_sync.py folder1 folder2 [folder3 ...]

This script:
- Loads configuration via load_config()
- Validates provided folders contain a .roo directory
- Creates a SyncEngine with a Queue for events
- Runs a synchronous sync via engine.run_sync(folders)
- Prints basic progress events from the event queue to stdout
"""

from utils_sync.sync_core import SyncEngine
from utils_sync.config_sync import load_config
from utils_sync.file_path_utils import has_roo_dir
from utils_sync.progress_events import EventType, ProgressEvent

def _print_event(event: ProgressEvent) -> None:
    """Print a concise, human-readable representation of a ProgressEvent."""
    et = event.event_type
    if et == EventType.SCAN_START:
        print(f"[SCAN_START] {event.folder} - {event.message}")
    elif et == EventType.SCAN_FILE:
        print(f"[SCAN_FILE] {event.folder}: {event.file_path}")
    elif et == EventType.COPY:
        print(f"[COPY] {event.file_path} - {event.message}")
    elif et == EventType.SKIP:
        print(f"[SKIP] {event.file_path} - {event.message}")
    elif et == EventType.ERROR:
        print(f"[ERROR] {event.message}")
    elif et == EventType.COMPLETE:
        print(f"[COMPLETE] {event.message}")
    else:
        # Generic fallback
        print(f"[{et}] {event.message}")

def run_cli_sync(folders):
    # [Created-or-Modified] by LLM model | 2025-11-13_01
    """
    Run a synchronous CLI-based sync operation.

    Args:
        folders: iterable of folder paths (str or Path)
    """
    # Normalize folder paths to Path objects
    folders = [Path(f) for f in folders]

    # Load configuration
    config = load_config()

    # Validate number of folders
    if len(folders) < 2:
        print("Error: At least two folders must be provided for sync.", file=sys.stderr)
        sys.exit(1)

    # Validate each folder contains a .roo directory
    invalid = [str(f) for f in folders if not has_roo_dir(f)]
    if invalid:
        for bad in invalid:
            print(f"Error: Folder does not contain a .roo subdirectory: {bad}", file=sys.stderr)
        sys.exit(1)

    # Create event queue and engine
    event_queue = queue.Queue()
    engine = SyncEngine(config, event_queue)

    # Run synchronous sync operation
    try:
        engine.run_sync(folders)
    except AttributeError:
        # In case SyncEngine exposes only scan/plan/execute, try the sequence
        try:
            file_index = engine.scan_folders(folders)
            actions = engine.plan_actions(file_index)
            engine.execute_actions(actions)
        except Exception as e:
            print(f"Sync failed: {e}", file=sys.stderr)
            sys.exit(2)
    except Exception as e:
        print(f"Sync failed: {e}", file=sys.stderr)
        sys.exit(2)

    # After run_sync completes, drain and print remaining events
    while not event_queue.empty():
        event = event_queue.get()
        try:
            _print_event(event)
        except Exception:
            # Best-effort printing
            print(f"[EVENT] {getattr(event, 'message', repr(event))}")

def _parse_args():
    p = argparse.ArgumentParser(
        description="Headless CLI wrapper for the AgentFlow sync engine."
    )
    p.add_argument(
        "folders",
        nargs="+",
        help="Folders to synchronize (must contain a .roo subdirectory)"
    )
    return p.parse_args()

if __name__ == "__main__":
    args = _parse_args()
    run_cli_sync(args.folders)