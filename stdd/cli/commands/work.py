"""STDD work CLI — track related work during a change (V2.9.4).

Related work captures bugfixes, tests, experiences, and other
incidental work produced during a change's lifecycle.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import yaml


def _find_change(project_root: Path, name: str = None) -> Path:
    """Find change dir by name (most recent if None)."""
    changes_dir = project_root / "changes"
    if not changes_dir.is_dir():
        return None
    if name:
        return changes_dir / name
    candidates = sorted(
        [d for d in changes_dir.iterdir() if d.is_dir() and d.name != "_batch" and (d / ".stdd.yaml").exists()],
        key=lambda d: d.stat().st_mtime, reverse=True,
    )
    return candidates[0] if candidates else None


def cmd_work(args: argparse.Namespace) -> None:
    """Track related work for a change."""
    project_root = Path.cwd()
    action = getattr(args, "work_action", "list")
    change_name = getattr(args, "name", None)

    change_dir = _find_change(project_root, change_name)
    if change_dir is None:
        print("  No change found.")
        sys.exit(1)

    stdd_yaml = change_dir / ".stdd.yaml"
    if not stdd_yaml.exists():
        print(f"  .stdd.yaml not found in {change_dir.name}")
        sys.exit(1)

    data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
    works = data.get("related_work", [])

    if action == "add":
        work_type = getattr(args, "work_type", "other") or "other"
        description = getattr(args, "description", "")
        if not description:
            print("  Usage: stdd work add --type bugfix \"描述\"")
            sys.exit(1)
        commit = getattr(args, "commit_hash", "") or ""

        works.append({
            "type": work_type,
            "description": description,
            "commit": commit,
            "added_at": datetime.now().isoformat(),
        })
        data["related_work"] = works
        stdd_yaml.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")
        print(f"  ✅ [{len(works)}] {work_type}: {description}")
        return

    # list
    if works:
        print(f"  Related work ({len(works)}):")
        for i, w in enumerate(works, 1):
            commit_str = f" ({w.get('commit', '')})" if w.get('commit') else ""
            print(f"    {i}. [{w.get('type', '?')}] {w.get('description', '?')}{commit_str}")
    else:
        print(f"  暂无关联工作记录。")
        print(f"  用 'stdd work add --type bugfix \"描述\"' 记录附带工作。")
