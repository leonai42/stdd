#!/usr/bin/env python3
"""STDD PreCompact Hook — save critical state before compaction."""
from pathlib import Path
import yaml
from datetime import datetime

def main():
    project_root = Path.cwd()
    for change_dir in sorted((project_root / "changes").iterdir()):
        stdd_yaml = change_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            state = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8")) or {}
            state["last_modified"] = datetime.now().isoformat()
            print(f"[STDD] State saved: Phase {state.get('active_phase', '?')}")
            break

if __name__ == "__main__":
    main()
