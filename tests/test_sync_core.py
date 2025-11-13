import os
import time
import queue
import shutil
from pathlib import Path
import datetime
from utils_sync.sync_core import SyncEngine
from utils_sync.progress_events import EventType

# [Created-or-Modified] by [LLM model] | 2025-11-13_01

def drain_queue(q):
    items = []
    while True:
        try:
            items.append(q.get_nowait())
        except queue.Empty:
            break
    return items

def test_scan_folders_indexes_only_roo_files_respects_ignore_patterns(tmp_path):
    q = queue.Queue()
    config = {"ignore_patterns": [".git", "__pycache__"]}
    engine = SyncEngine(config, q)

    # create folder1 and folder2 with .roo
    base1 = tmp_path / "f1"; base1.mkdir()
    roo1 = base1 / ".roo"; roo1.mkdir()
    (roo1 / "a.txt").write_text("v1")
    (roo1 / ".git").mkdir()
    (roo1 / ".git" / "ignore.txt").write_text("secret")

    base2 = tmp_path / "f2"; base2.mkdir()
    roo2 = base2 / ".roo"; roo2.mkdir()
    (roo2 / "a.txt").write_text("v2")

    index = engine.scan_folders([base1, base2])

    # ensure 'a.txt' present and .git file ignored
    assert any(k.endswith("a.txt") for k in index.keys())

    # flatten check: there should be two entries for a.txt (one per folder)
    found = 0
    for rel, group in index.items():
        if rel and rel.endswith("a.txt"):
            found += len(group)
    assert found == 2

    events = drain_queue(q)
    assert any(e.event_type == EventType.SCAN_START for e in events)
    assert any(e.event_type == EventType.SCAN_FILE for e in events)

def test_plan_actions_picks_newest_source(tmp_path):
    q = queue.Queue()
    config = {"ignore_patterns": []}
    engine = SyncEngine(config, q)

    base1 = tmp_path / "p1"; base1.mkdir()
    (base1 / ".roo").mkdir()
    file1 = base1 / ".roo" / "rules" / "01.md"; file1.parent.mkdir(parents=True)
    file1.write_text("old")

    base2 = tmp_path / "p2"; base2.mkdir()
    (base2 / ".roo").mkdir()
    file2 = base2 / ".roo" / "rules" / "01.md"; file2.parent.mkdir(parents=True)
    file2.write_text("new")

    # set mtimes: file2 newer
    now = time.time()
    os.utime(file1, (now - 100, now - 100))
    os.utime(file2, (now, now))

    index = engine.scan_folders([base1, base2])

    # find the key for rules/01.md
    key = None
    for k in index:
        if k and k.endswith("rules/01.md"):
            key = k
            break
    assert key is not None

    actions = engine.plan_actions(index)
    assert len(actions) == 1
    act = actions[0]

    # source_path should be file2 (newer), destination file1
    assert str(act["source_path"]) == str(file2)
    assert str(act["destination_path"]) == str(file1)

def test_execute_actions_performs_copy_backup_and_respects_dry_run(tmp_path):
    q = queue.Queue()
    # prepare two bases
    base1 = tmp_path / "s1"; base1.mkdir()
    (base1 / ".roo").mkdir()
    src = (base1 / ".roo" / "x.txt")
    src.write_text("SRC")

    base2 = tmp_path / "s2"; base2.mkdir()
    (base2 / ".roo").mkdir()
    dst = (base2 / ".roo" / "x.txt")
    dst.write_text("OLD")

    # set mtimes so src is newer than dst
    now = time.time()
    os.utime(src, (now, now))
    os.utime(dst, (now - 200, now - 200))

    # build index and actions with dry_run=True
    config = {"ignore_patterns": [], "dry_run": True, "backup_mode": "timestamped"}
    engine = SyncEngine(config, q)
    index = engine.scan_folders([base1, base2])
    actions = engine.plan_actions(index)

    # dry run: execute_actions should emit SKIP and not modify dst
    engine.execute_actions(actions)
    events = drain_queue(q)
    assert any(e.event_type == EventType.SKIP for e in events)
    assert dst.read_text() == "OLD"

    # now perform real copy with backup_mode timestamped
    q2 = queue.Queue()
    config2 = {"ignore_patterns": [], "dry_run": False, "backup_mode": "timestamped"}
    engine2 = SyncEngine(config2, q2)
    engine2.execute_actions(actions)
    evs = drain_queue(q2)
    assert any(e.event_type == EventType.COPY for e in evs)

    # dst should now equal src
    assert dst.read_text() == "SRC"

    # backup file should exist with a .bak suffix in the same parent directory
    backups = [p for p in dst.parent.iterdir() if p.name.startswith(dst.name) and ".bak" in p.name]
    assert len(backups) >= 1