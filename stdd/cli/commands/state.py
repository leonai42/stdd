"""stdd state — Read/write resume context fields in .stdd.yaml (V2.5)."""

import argparse
import sys
from pathlib import Path
from datetime import datetime

import yaml


RESUME_FIELDS = ["resume_context", "active_slice", "last_action", "last_modified"]


def _find_change_dir(name: str | None, project_root: Path) -> Path | None:
    """Find change directory by name (most recent if None)."""
    changes_dir = project_root / "changes"
    if not changes_dir.exists():
        return None
    if name:
        return changes_dir / name
    # Find most recently modified
    dirs = sorted(changes_dir.iterdir(), key=lambda d: d.stat().st_mtime, reverse=True)
    return dirs[0] if dirs else None


def read_resume_context(change_dir: Path) -> dict:
    """Read resume fields from .stdd.yaml with backward compatibility.

    Returns dict with resume_context, active_slice, last_action, last_modified.
    Values are None for missing fields (V2.4 compatibility).
    """
    state_file = change_dir / ".stdd.yaml"
    if not state_file.exists():
        return {k: None for k in RESUME_FIELDS}

    data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}
    result = {}
    for k in RESUME_FIELDS:
        result[k] = data.get(k)
    return result


def write_resume_context(change_dir: Path, **kwargs) -> None:
    """Write resume fields to .stdd.yaml. Only writes specified keys.

    Usage: write_resume_context(change_dir, resume_context="...", active_slice=2)
    """
    state_file = change_dir / ".stdd.yaml"
    if not state_file.exists():
        print(f"  .stdd.yaml not found in {change_dir}")
        return

    data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}
    for k in RESUME_FIELDS:
        if k in kwargs:
            data[k] = kwargs[k]
    data["last_modified"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    state_file.write_text(
        yaml.dump(data, allow_unicode=True, default_flow_style=False),
        encoding="utf-8"
    )


def cmd_state(args: argparse.Namespace) -> None:
    """CLI entry: stdd state <change-name> [--resume] [--set KEY=VALUE]."""
    project_root = Path.cwd()
    change_dir = _find_change_dir(getattr(args, "name", None), project_root)

    if change_dir is None:
        print("  No change found.")
        sys.exit(1)

    if getattr(args, "resume", False):
        ctx = read_resume_context(change_dir)
        print(f"  Resume context for {change_dir.name}:")
        for k in RESUME_FIELDS:
            print(f"    {k}: {ctx[k]}")
        return

    set_kv = getattr(args, "set", None)
    if set_kv:
        if "=" not in set_kv:
            print("  Usage: --set KEY=VALUE")
            sys.exit(1)
        key, value = set_kv.split("=", 1)
        if key not in RESUME_FIELDS:
            print(f"  Unknown field: {key}. Valid: {', '.join(RESUME_FIELDS)}")
            sys.exit(1)
        write_resume_context(change_dir, **{key: value})
        print(f"  Set {key}={value} for {change_dir.name}")
        return

    # Default: show full state
    state_file = change_dir / ".stdd.yaml"
    if not state_file.exists():
        print(f"  .stdd.yaml not found in {change_dir}")
        sys.exit(1)
    data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}
    print(f"  State for {change_dir.name}:")
    print(f"    current_phase: {data.get('current_phase', 'unknown')}")
    print(f"    status: {data.get('status', 'unknown')}")
    ctx = {k: data.get(k) for k in RESUME_FIELDS}
    print(f"    resume_context: {ctx.get('resume_context')}")
    print(f"    active_slice: {ctx.get('active_slice')}")
    print(f"    last_action: {ctx.get('last_action')}")
    print(f"    last_modified: {ctx.get('last_modified')}")
