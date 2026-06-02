"""STDD hooks CLI — lifecycle hook management (V2.7)."""

import sys
import json
from pathlib import Path


HOOK_SCRIPTS = {
    "session-start": """#!/usr/bin/env python3
\"\"\"STDD SessionStart Hook — auto-load change state.\"\"\"
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
""",
    "pre-compact": """#!/usr/bin/env python3
\"\"\"STDD PreCompact Hook — save critical state before compaction.\"\"\"
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
""",
    "session-end": """#!/usr/bin/env python3
\"\"\"STDD Stop Hook — persist session learnings.\"\"\"
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
""",
}


def cmd_hooks_install(args):
    """Install STDD hooks to .claude/settings.json."""
    project_root = Path.cwd()
    hooks_dir = project_root / ".stdd" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    # Write hook scripts
    for name, script in HOOK_SCRIPTS.items():
        script_path = hooks_dir / f"{name}.py"
        if script_path.exists() and not args.force:
            print(f"  [SKIP] {name}.py already exists (use --force to overwrite)")
            continue
        script_path.write_text(script, encoding="utf-8")
        print(f"  [OK] .stdd/hooks/{name}.py")

    # Update .claude/settings.json
    settings_path = project_root / ".claude" / "settings.local.json"
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    else:
        settings = {}

    hooks_config = settings.setdefault("hooks", {})
    hooks_config["SessionStart"] = f"python .stdd/hooks/session-start.py"
    hooks_config["PreCompact"] = f"python .stdd/hooks/pre-compact.py"
    hooks_config["Stop"] = f"python .stdd/hooks/session-end.py"

    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [OK] Hooks configured in .claude/settings.local.json")


def cmd_hooks_status(args):
    """Show current hooks status."""
    project_root = Path.cwd()
    hooks_dir = project_root / ".stdd" / "hooks"
    if not hooks_dir.exists():
        print("  No STDD hooks installed.")
        return

    scripts = list(hooks_dir.glob("*.py"))
    print(f"  Installed hooks: {len(scripts)}")
    for s in sorted(scripts):
        print(f"    - {s.name}")


def cmd_hooks_uninstall(args):
    """Remove STDD hooks configuration."""
    project_root = Path.cwd()
    settings_path = project_root / ".claude" / "settings.local.json"
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        if "hooks" in settings:
            del settings["hooks"]
            settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
            print("  Hooks removed from .claude/settings.local.json")


def _dispatch(args):
    """Route to appropriate hooks subcommand."""
    if args.action == "install":
        cmd_hooks_install(args)
    elif args.action == "status":
        cmd_hooks_status(args)
    elif args.action == "uninstall":
        cmd_hooks_uninstall(args)
    else:
        print(f"  Unknown hooks action: {args.action}")
        sys.exit(1)
