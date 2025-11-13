# Created by claude-sonnet-4-5 | 2025-11-13_1
"""
Verification script for CLI integration test results.
Checks file content, timestamps, and backup creation.
"""
import os
from pathlib import Path

def verify_cli_test():
    """Verify the results of the CLI integration test."""
    print("=== CLI Integration Test Verification ===\n")
    
    # File paths
    file_a = Path("test_integration/project_a/.roo/file.txt")
    file_b = Path("test_integration/project_b/.roo/file.txt")
    backup_dir = Path("test_integration/project_b/.roo")
    
    # Check files exist
    if not file_a.exists():
        print("❌ FAIL: Source file does not exist")
        return False
    if not file_b.exists():
        print("❌ FAIL: Destination file does not exist")
        return False
    
    print("✓ Both files exist")
    
    # Check content matches
    content_a = file_a.read_text()
    content_b = file_b.read_text()
    
    print(f"\nSource content: {content_a[:50]}...")
    print(f"Dest content: {content_b[:50]}...")
    
    if content_a == content_b:
        print("✓ File contents match")
    else:
        print("❌ FAIL: File contents do not match")
        return False
    
    # Check backup file was created (.bak extension)
    backup_files = list(backup_dir.glob("*.bak"))
    if backup_files:
        print(f"✓ Backup file created: {backup_files[0].name}")
        backup_content = backup_files[0].read_text()
        print(f"  Backup content: {backup_content[:50]}...")
    else:
        print("❌ FAIL: No backup file found")
        return False
    
    # Check timestamps
    mtime_a = os.path.getmtime(file_a)
    mtime_b = os.path.getmtime(file_b)
    
    print(f"\nTimestamps:")
    print(f"  Source: {mtime_a}")
    print(f"  Dest: {mtime_b}")
    
    if mtime_b >= mtime_a - 1:  # Allow 1 second tolerance
        print("✓ Destination timestamp updated correctly")
    else:
        print("⚠ Warning: Destination timestamp may not be updated")
    
    print("\n=== CLI Integration Test: PASSED ===")
    return True

if __name__ == "__main__":
    verify_cli_test()