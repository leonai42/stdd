"""STDD guard CLI — project-level enforcement gate (V2.9.2)."""

import sys
import argparse
from pathlib import Path


# V2.9.2: Phases where code editing is permitted
_EDITABLE_PHASES = {"build", "verify"}


def _find_active_change(project_root: Path) -> tuple:
    """Find the most recent active change. Returns (change_dir, phase) or (None, None)."""
    changes_dir = project_root / "changes"
    if not changes_dir.is_dir():
        return None, None

    for change_dir in sorted(
        [d for d in changes_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    ):
        stdd_yaml = change_dir / ".stdd.yaml"
        if stdd_yaml.exists():
            import yaml
            data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
            if data:
                status = data.get("status", "")
                phase = data.get("phase", "")
                # Active: understand/spec/slice/build/verify in_progress or pending
                if status in ("active", "in_progress", "pending") or phase in (
                    "understand", "spec", "slice", "build", "verify"
                ):
                    return change_dir, phase
    return None, None


def cmd_guard_check(args: argparse.Namespace) -> int:
    """Check if currently in a valid STDD flow. Exit 0 if yes, 1 if no."""
    project_root = Path.cwd()

    # Check if enforce_stdd is enabled
    enforce = True
    config_file = project_root / ".stdd" / "config.d" / "project.yaml"
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        enforce = config.get("enforce_stdd", True)

    if not enforce:
        return 0  # Enforcement disabled

    # Find active change and check phase
    active_dir, phase = _find_active_change(project_root)

    if active_dir and phase in _EDITABLE_PHASES:
        # Phase 4 (build) or Phase 5 (verify) — editing is expected
        if not getattr(args, "quiet", False):
            print(f"  [STDD Guard] Active: {active_dir.name} (phase: {phase}) — allowed")
        return 0

    # Block with specific reason
    platform = getattr(args, "platform", "cli")
    if active_dir:
        reason = f"当前 Phase '{phase}' 不允许代码修改。只有 Phase 4 (build) 和 Phase 5 (verify) 允许编辑。"
    else:
        reason = "无 active change。请通过 /stdd-understand 启动变更流程。"

    # Check for allow_bypass
    allow_bypass = False
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        allow_bypass = config.get("allow_bypass", False)

    strict = getattr(args, "strict", False)
    if allow_bypass and not strict:
        print(f"  [STDD Guard] {reason}")
        print("  [STDD Guard] allow_bypass is enabled — allowing anyway.")
        return 0

    # Block
    if platform == "claude-code":
        print("  [STDD Guard] ⛔ Code modification blocked!")
        print(f"  [STDD Guard] {reason}")
    else:
        print(f"  [STDD Guard] {reason}")
    return 1


def cmd_guard_status(args: argparse.Namespace) -> None:
    """Display current STDD guard status."""
    project_root = Path.cwd()
    active_dir, phase = _find_active_change(project_root)

    config_file = project_root / ".stdd" / "config.d" / "project.yaml"
    enforce = True
    allow_bypass = False
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        enforce = config.get("enforce_stdd", True)
        allow_bypass = config.get("allow_bypass", False)

    editable = phase in _EDITABLE_PHASES if phase else False
    print("  STDD Guard Status:")
    print(f"    enforce_stdd:  {enforce}")
    print(f"    allow_bypass:  {allow_bypass}")
    print(f"    editable phases: {sorted(_EDITABLE_PHASES)}")
    if active_dir:
        status = "✅ 可编辑" if editable else "🔒 只读"
        print(f"    active change: {active_dir.name} (phase: {phase}) — {status}")
    else:
        print("    active change: None — 🔒 只读")


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


def cmd_guard_disable(args: argparse.Namespace) -> None:
    """Temporarily remove the guard hook (reversible with 'enable')."""
    project_root = Path.cwd()
    import json
    settings_file = project_root / ".claude" / "settings.local.json"

    if not settings_file.exists():
        print("  [STDD Guard] No settings.local.json found. Nothing to disable.")
        return

    settings = json.loads(settings_file.read_text(encoding="utf-8"))
    hooks = settings.get("hooks", {}).get("PreToolUse", [])

    removed = False
    new_hooks = []
    for hook in hooks:
        if "stdd guard" in str(hook.get("hooks", [])):
            removed = True
        else:
            new_hooks.append(hook)

    if removed:
        settings["hooks"]["PreToolUse"] = new_hooks
        if not new_hooks:
            del settings["hooks"]["PreToolUse"]
            if not settings["hooks"]:
                del settings["hooks"]
        settings_file.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print("  [STDD Guard] Hook disabled. Run 'stdd guard enable' to re-enable.")
    else:
        print("  [STDD Guard] No guard hook found. Already disabled.")


def cmd_guard_enable(args: argparse.Namespace) -> None:
    """Re-enable the guard hook after disable."""
    # Reuse init logic
    cmd_guard_init(args)


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
    elif action == "disable":
        cmd_guard_disable(args)
    elif action == "enable":
        cmd_guard_enable(args)
    else:
        print(f"  Unknown guard action: {action}")
        sys.exit(1)
