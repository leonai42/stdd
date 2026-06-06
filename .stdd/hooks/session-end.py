#!/usr/bin/env python3
"""STDD Stop Hook — persist session learnings."""
from pathlib import Path
import yaml

def main():
    project_root = Path.cwd()
    exp_dir = project_root / ".stdd" / "experiences"
    exp_count = len(list(exp_dir.glob("EXP-*.md"))) if exp_dir.exists() else 0
    if exp_count > 0:
        print(f"[STDD] Experience library: {exp_count} entries")
        print(f"[STDD] Tip: run 'stdd experience curate' to extract new patterns")

if __name__ == "__main__":
    main()
