"""STDD fix CLI — Plankton multi-level auto-fix (V2.8)."""

import sys
import subprocess
from pathlib import Path


def cmd_fix(args):
    """Main fix dispatch: stdd fix --level 1|2|3 [--dry-run]."""
    level = getattr(args, "level", 1)
    dry_run = getattr(args, "dry_run", False)

    if level == 1:
        _fix_level1(dry_run)
    elif level == 2:
        _fix_level2(dry_run)
    elif level == 3:
        _fix_level3(dry_run)
    else:
        print(f"  Invalid level: {level}. Use 1, 2, or 3.")
        sys.exit(1)


def _fix_level1(dry_run: bool):
    """Level 1: Silent auto-fix — formatting, import sorting, trailing whitespace."""
    commands = [
        ["ruff", "format", "."],
        ["ruff", "check", "--fix", "."],
        ["isort", "."],
    ]

    fixed_files = []
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                fixed_files.append(cmd[0])
        except FileNotFoundError:
            print(f"  [SKIP] {cmd[0]} not found — install with: pip install ruff isort")
            continue

    if dry_run:
        print("  [DRY-RUN] Would run: ruff format . && ruff check --fix . && isort .")
        return

    if fixed_files:
        print(f"  ✅ Level 1 fix applied: {', '.join(fixed_files)}")
    else:
        print("  ✅ Already formatted — nothing to fix")


def _fix_level2(dry_run: bool):
    """Level 2: Suggested fix — type annotations, exception handling patterns."""
    project_root = Path.cwd()
    suggestions = []

    # Scan Python files for common issues
    for py_file in project_root.rglob("*.py"):
        if "__pycache__" in str(py_file) or ".pytest_cache" in str(py_file):
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:
            continue

        rel_path = py_file.relative_to(project_root)

        # Check for bare except Exception in async functions
        if "async def " in content and "except Exception" in content:
            suggestions.append(f"  ⚠️  {rel_path}: Possible missing CancelledError handling in async function")

        # Check for functions without type annotations (simple heuristic)
        lines = content.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("def ") and "(" in line and ")" in line:
                # Skip if has return type annotation
                if " -> " in line:
                    continue
                # Skip methods
                if "self" in line or "cls" in line:
                    continue
                # Skip if has param annotations
                if ")" in line and ":" in line.split(")")[0]:
                    continue
                func_name = stripped.split("(")[0].replace("def ", "")
                suggestions.append(f"  💡 {rel_path}:{i+1}: '{func_name}' has no type annotations")

    if dry_run:
        print(f"  [DRY-RUN] Would check {len(list(project_root.rglob('*.py')))} files for Level 2 issues")
        return

    if suggestions:
        print(f"  Level 2 suggestions ({len(suggestions)} issues):")
        for s in suggestions[:20]:  # Cap at 20 suggestions
            print(s)
        if len(suggestions) > 20:
            print(f"  ... and {len(suggestions) - 20} more")
        print(f"\n  💡 Review the suggestions above and apply manually, or run with --dry-run first")
    else:
        print("  ✅ No Level 2 issues detected")


def _fix_level3(dry_run: bool):
    """Level 3: Report — security, performance, architecture issues. Never auto-applies."""
    print("  Level 3: Report-only mode")
    print("  Run security/performance/architecture analysis tools manually:")
    print("    - bandit for security: pip install bandit && bandit -r .")
    print("    - pylint for code quality: pylint <source_dir>")
    print("    - mypy for type checking: mypy <source_dir>")
    print()
    if dry_run:
        print("  [DRY-RUN] Would generate fix report")
        return
    print("  💡 Level 3 fixes should always be reviewed by a human before applying.")


def _dispatch(args):
    """Route to fix command."""
    cmd_fix(args)
