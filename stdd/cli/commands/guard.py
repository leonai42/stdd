"""STDD guard CLI — project-level enforcement gate (V2.9.2)."""

import sys
import argparse
from pathlib import Path


def _find_active_change(project_root: Path) -> Path:
    """Find the most recent .stdd.yaml with in_progress status in changes/."""
    changes_dir = project_root / "changes"
    if not changes_dir.is_dir():
        return None

    for change_dir in sorted(
        [d for d in changes_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    ):
        stdd_yaml = change_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            import yaml
            data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            if data and data.get("status") in ("active", "in_progress"):
                return change_dir
    return None


def cmd_guard_check(args: argparse.Namespace) -> int:
    """Check if currently in a valid STDD flow. Exit 0 if yes, 1 if no."""
    project_root = Path.cwd()

    # Check if enforce_stdd is enabled
    enforce = True  # Default: check is active
    config_file = project_root / ".stdd" / "config.d" / "project.yaml"
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        enforce = config.get("enforce_stdd", True)

    if not enforce:
        return 0  # Enforcement disabled — allow

    # Find active change
    active = _find_active_change(project_root)
    if active:
        # In a valid STDD flow
        if not getattr(args, "quiet", False):
            print(f"  [STDD Guard] Active change: {active.name}")
        return 0

    # Check for allow_bypass
    allow_bypass = False
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        allow_bypass = config.get("allow_bypass", False)

    strict = getattr(args, "strict", False)
    if allow_bypass and not strict:
        print("  [STDD Guard] No active change, but allow_bypass is enabled.")
        print("  [STDD Guard] Consider starting a change via /stdd-understand.")
        return 0

    # Block: no active change, enforce is on
    platform = getattr(args, "platform", "cli")
    if platform == "claude-code":
        print("  [STDD Guard] Uncontrolled code modification detected!")
        print("  [STDD Guard] This project requires all changes to go through STDD.")
        print("  [STDD Guard] Please start a change via: /stdd-understand <description>")
    else:
        print("  [STDD Guard] No active STDD change found.")
        print("  [STDD Guard] Run 'stdd new <name>' or use /stdd-understand to start.")
    return 1


def cmd_guard_status(args: argparse.Namespace) -> None:
    """Display current STDD guard status."""
    project_root = Path.cwd()
    active = _find_active_change(project_root)

    config_file = project_root / ".stdd" / "config.d" / "project.yaml"
    enforce = True
    allow_bypass = False
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        enforce = config.get("enforce_stdd", True)
        allow_bypass = config.get("allow_bypass", False)

    print(f"  STDD Guard Status:")
    print(f"    enforce_stdd:  {enforce}")
    print(f"    allow_bypass:  {allow_bypass}")
    if active:
        print(f"    active change: {active.name}")
    else:
        print(f"    active change: None (uncontrolled)")


def cmd_guard_init(args: argparse.Namespace) -> None:
    """Initialize guard hooks for the current project."""
    project_root = Path.cwd()
    platform = getattr(args, "platform", "claude-code")

    if platform == "claude-code":
        import json
        settings_file = project_root / ".claude" / "settings.local.json"

        if settings_file.exists():
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        else:
            settings = {"permissions": {"allow": []}}

        # Ensure hooks section exists
        if "hooks" not in settings:
            settings["hooks"] = {}

        # Add PreToolUse hook for guard
        if "PreToolUse" not in settings["hooks"]:
            settings["hooks"]["PreToolUse"] = []

        # Check if guard hook already exists
        guard_exists = False
        for hook in settings["hooks"]["PreToolUse"]:
            if "stdd guard" in str(hook.get("hooks", [])):
                guard_exists = True
                break

        if not guard_exists:
            settings["hooks"]["PreToolUse"].append({
                "matcher": "Edit|Write",
                "hooks": [{
                    "type": "command",
                    "command": "stdd guard --check --platform claude-code"
                }]
            })

        settings_file.parent.mkdir(parents=True, exist_ok=True)
        settings_file.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print("  [STDD Guard] Claude Code PreToolUse hook deployed.")
        print("  [STDD Guard] All Edit/Write operations will be checked.")
    else:
        print(f"  [STDD Guard] Platform '{platform}' not supported for auto-init.")
        print(f"  [STDD Guard] See docs for manual guard configuration.")


def cmd_guard(args: argparse.Namespace) -> None:
    """Entry point for guard command."""
    action = getattr(args, "action", "check")

    if action == "check":
        exit_code = cmd_guard_check(args)
        if exit_code != 0:
            sys.exit(exit_code)
    elif action == "status":
        cmd_guard_status(args)
    elif action == "init":
        cmd_guard_init(args)
    else:
        print(f"  Unknown guard action: {action}")
        sys.exit(1)
