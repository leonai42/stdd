"""STDD index CLI — project-level index management (V2.7)."""

import sys
import yaml
from pathlib import Path


def cmd_index_update(args):
    """Scan project and generate/update project-index.yaml."""
    project_root = Path.cwd()
    index_file = project_root / "project-index.yaml"

    index = {
        "project": {
            "name": project_root.name,
            "language": _detect_language(project_root),
            "stdd_version": "2.7",
        },
        "changes": _scan_changes(project_root),
        "capabilities": _scan_capabilities(project_root),
        "module_index": _scan_modules(project_root),
    }

    index_file.write_text(
        yaml.dump(index, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    changes_count = len(index.get("changes", {}))
    caps_count = len(index.get("capabilities", {}))
    print(f"  project-index.yaml updated: {changes_count} changes, {caps_count} capabilities")


def _detect_language(project_root: Path) -> str:
    """Detect primary language from file extensions."""
    if list(project_root.glob("*.py")) or (project_root / "stdd").exists():
        return "python"
    if list(project_root.glob("*.go")):
        return "go"
    if list(project_root.glob("*.java")):
        return "java"
    if list(project_root.glob("*.rs")):
        return "rust"
    if list(project_root.glob("*.ts")):
        return "typescript"
    return "unknown"


def _scan_changes(project_root: Path) -> dict:
    """Scan changes/ directory."""
    changes = {}
    changes_dir = project_root / "changes"
    if not changes_dir.exists():
        return changes

    for change_dir in sorted(changes_dir.iterdir()):
        if not change_dir.is_dir():
            continue
        stdd_yaml = change_dir / ".stdd.yaml"
        phase = "unknown"
        if stdd_yaml.exists():
            try:
                state = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8")) or {}
                phase = state.get("active_phase", "unknown")
            except Exception:
                pass
        changes[change_dir.name] = {
            "status": "completed" if phase == 6 else "in_progress",
            "phase": phase,
        }
    return changes


def _scan_capabilities(project_root: Path) -> dict:
    """Scan specs/ directory for capabilities."""
    caps = {}
    specs_dir = project_root / "specs"
    if not specs_dir.exists():
        return caps

    for spec_dir in specs_dir.iterdir():
        if not spec_dir.is_dir():
            continue
        spec_file = spec_dir / "spec.md"
        if spec_file.exists():
            caps[spec_dir.name] = {"specs": f"specs/{spec_dir.name}/spec.md"}
    return caps


def _scan_modules(project_root: Path) -> dict:
    """Scan source directories for modules."""
    modules = {}
    for src_dir_name in ["stdd", "app", "src", "bin"]:
        src_dir = project_root / src_dir_name
        if not src_dir.exists():
            continue
        for py_file in src_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            rel_path = str(py_file.relative_to(project_root))
            modules[rel_path] = {"capabilities": []}
    return modules


def cmd_index_show(args):
    """Show capability info from project index."""
    project_root = Path.cwd()
    index_file = project_root / "project-index.yaml"

    if not index_file.exists():
        print("  project-index.yaml not found. Run 'stdd index update' first.")
        sys.exit(1)

    index = yaml.safe_load(index_file.read_text(encoding="utf-8"))

    if hasattr(args, "capability") and args.capability:
        cap = index.get("capabilities", {}).get(args.capability)
        if cap:
            print(f"\n  Capability: {args.capability}")
            print(f"  Specs: {cap.get('specs', 'N/A')}")
        else:
            print(f"  Capability '{args.capability}' not found")
    else:
        print(f"\n  Project: {index['project']['name']}")
        print(f"  Language: {index['project']['language']}")
        print(f"  Changes: {len(index.get('changes', {}))}")
        print(f"  Capabilities: {len(index.get('capabilities', {}))}")
        print(f"  Modules: {len(index.get('module_index', {}))}")
        print()


def cmd_index_trace(args):
    """Trace a file to its associated capabilities and changes."""
    project_root = Path.cwd()
    index_file = project_root / "project-index.yaml"

    if not index_file.exists():
        print("  project-index.yaml not found. Run 'stdd index update' first.")
        sys.exit(1)

    index = yaml.safe_load(index_file.read_text(encoding="utf-8"))
    module_info = index.get("module_index", {}).get(args.file)

    if module_info:
        print(f"\n  File: {args.file}")
        print(f"  Capabilities: {', '.join(module_info.get('capabilities', ['none']))}")
        if module_info.get("symbols"):
            print(f"  Symbols: {', '.join(module_info['symbols'])}")
        print()
    else:
        print(f"  File '{args.file}' not found in module index")


def _dispatch(args):
    """Route to appropriate index subcommand."""
    action = getattr(args, "action", "show")
    if action == "update":
        cmd_index_update(args)
    elif action == "show":
        cmd_index_show(args)
    elif action == "trace":
        cmd_index_trace(args)
    else:
        print(f"  Unknown index action: {action}")
        sys.exit(1)
