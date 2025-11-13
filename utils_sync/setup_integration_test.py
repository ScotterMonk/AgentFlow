# Created by claude-sonnet-4-5 | 2025-11-13_1
"""
Setup script for integration testing of the file sync utility.
Creates test directories and files with controlled timestamps.
"""
import os
import time
from pathlib import Path

def setup_integration_test():
    """Create test environment for integration testing."""
    # Create root test directory
    test_root = Path("test_integration")
    test_root.mkdir(exist_ok=True)
    
    # Create project directories
    project_a = test_root / "project_a"
    project_b = test_root / "project_b"
    
    project_a.mkdir(exist_ok=True)
    project_b.mkdir(exist_ok=True)
    
    # Create .roo subdirectories
    roo_a = project_a / ".roo"
    roo_b = project_b / ".roo"
    
    roo_a.mkdir(exist_ok=True)
    roo_b.mkdir(exist_ok=True)
    
    # Create test file in project_a (source - newer)
    file_a = roo_a / "file.txt"
    file_a.write_text("Content from project_a - This is the newer version")
    
    # Wait a moment to ensure timestamp difference
    time.sleep(0.1)
    
    # Create test file in project_b (destination - older)
    file_b = roo_b / "file.txt"
    file_b.write_text("Content from project_b - This is the older version")
    
    # Explicitly set older mtime for project_b file
    old_time = time.time() - 3600  # 1 hour ago
    os.utime(file_b, (old_time, old_time))
    
    # Verify setup
    print("Integration test environment created:")
    print(f"  {project_a} - Created")
    print(f"  {project_b} - Created")
    print(f"  {file_a} - Created (newer)")
    print(f"  {file_b} - Created (older)")
    print(f"\nFile timestamps:")
    print(f"  project_a file mtime: {os.path.getmtime(file_a)}")
    print(f"  project_b file mtime: {os.path.getmtime(file_b)}")
    print(f"\nReady for integration testing!")

if __name__ == "__main__":
    setup_integration_test()