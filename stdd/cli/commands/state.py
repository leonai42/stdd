"""stdd state — Read/write resume context fields in .stdd.yaml (V2.5)."""

import argparse
import sys
from pathlib import Path
from datetime import datetime

import yaml


RESUME_FIELDS = ["resume_context", "active_slice", "last_action", "last_modified",
                  "active_phase", "phase_context_file"]


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
        state_file = change_dir / ".stdd.yaml"
        data = yaml.safe_load(state_file.read_text(encoding="utf-8")) or {}

        print(f"\n  ══════════════════════════════════════")
        print(f"    STDD Resume Context")
        print(f"  ══════════════════════════════════════")
        print(f"\n  Change: {change_dir.name}")
        print(f"  Phase: {data.get('active_phase', '?')}")
        print(f"  Slice: {data.get('active_slice', 'N/A')}")
        print(f"  Last Action: {data.get('last_action', 'unknown')}")
        print(f"  Last Modified: {data.get('last_modified', 'unknown')}")

        # Phase context file pointer
        pc_file = data.get("phase_context_file", "")
        if pc_file:
            print(f"\n  📄 Phase Context: {pc_file}")
            print(f"  💡 建议: 先读取 phase-context.md 了解完整背景")

        # State freshness check (V2.7)
        freshness = data.get("state_freshness", {})
        if freshness:
            verified_at = freshness.get("verified_at", "unknown")
            saved_head = freshness.get("git_head", "")

            # Check git HEAD
            import subprocess
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--short", "HEAD"],
                    capture_output=True, text=True, cwd=project_root
                )
                current_head = result.stdout.strip()
            except Exception:
                current_head = ""

            if saved_head and current_head and saved_head != current_head:
                print(f"\n  🟡 State Freshness: STALE")
                print(f"     Git HEAD 已变更: saved={saved_head}, current={current_head}")
                print(f"     建议: 检查变更是否影响当前 change 的产出物")
            else:
                print(f"\n  🟢 State Freshness: FRESH — {verified_at}")

        print()
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
