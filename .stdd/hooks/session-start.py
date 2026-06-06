#!/usr/bin/env python3
"""STDD SessionStart Hook — auto-load change state."""
from pathlib import Path
import yaml

def main():
    project_root = Path.cwd()
    changes_dir = project_root / "changes"
    if not changes_dir.exists():
        return
    for change_dir in sorted(changes_dir.iterdir()):
        if not change_dir.is_dir():
            continue
        stdd_yaml = change_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            state = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8")) or {}
            phase = state.get("active_phase", "?")
            name = state.get("change_name", change_dir.name)
            print(f"[STDD] Active change: {name} (Phase {phase})")
            pc = state.get("phase_context_file", "")
            if pc:
                print(f"[STDD] Phase context: {pc}")
            break

if __name__ == "__main__":
    main()
