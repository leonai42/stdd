"""STDD structure CLI — code structure summary management (V2.8)."""

import sys
import yaml
import hashlib
from pathlib import Path
from datetime import datetime


def _get_structure_dir(project_root: Path) -> Path:
    return project_root / ".stdd" / "code-structure"


def _ensure_structure_dir(project_root: Path):
    d = _get_structure_dir(project_root)
    d.mkdir(parents=True, exist_ok=True)
    (d / "deltas").mkdir(exist_ok=True)
    index_file = d / "index.md"
    if not index_file.exists():
        index_file.write_text("# 项目代码结构索引\n\n> 自动生成 | STDD V2.8\n\n", encoding="utf-8")
    yaml_file = d / ".structure-index.yaml"
    if not yaml_file.exists():
        yaml_file.write_text(yaml.dump({"meta": {"last_updated": "", "total_changes": 0, "modules": {}}},
                                       allow_unicode=True, default_flow_style=False), encoding="utf-8")


def cmd_structure_delta(args):
    """Generate code-structure-delta.md for a change."""
    project_root = Path.cwd()
    change_name = args.target
    change_dir = project_root / "changes" / change_name
    if not change_dir.exists():
        print(f"  changes/{change_name}/ not found")
        sys.exit(1)

    delta_file = change_dir / "code-structure-delta.md"
    # Generate basic delta by scanning change directory
    git_head = _get_git_head(project_root)
    lines = [
        f"# Code Structure Delta — {change_name}",
        f"> 生成时间: {datetime.now().isoformat()} | Git commit: {git_head}",
        f"> 置信度: 0.70 (AI-generated — 以源代码为准)",
        "",
        "## 变更文件",
        "",
    ]
    # List all files in change directory (excluding .stdd.yaml and .md files)
    for f in sorted(change_dir.rglob("*")):
        if f.is_file() and f.suffix not in (".md", ".yaml", ".yml"):
            rel = f.relative_to(change_dir)
            lines.append(f"- `{rel}`")
        elif f.is_file() and f.suffix == ".py":
            rel = f.relative_to(change_dir)
            lines.append(f"- `{rel}` (Python)")

    delta_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Generated {delta_file}")


def cmd_structure_merge(args):
    """Merge delta into .stdd/code-structure/index.md."""
    project_root = Path.cwd()
    _ensure_structure_dir(project_root)
    change_name = args.target
    delta_file = project_root / "changes" / change_name / "code-structure-delta.md"

    if not delta_file.exists():
        print(f"  Delta not found for {change_name}. Run 'stdd structure delta {change_name}' first.")
        sys.exit(1)

    # Copy delta to deltas/ archive
    deltas_dir = _get_structure_dir(project_root) / "deltas"
    import shutil
    shutil.copy(delta_file, deltas_dir / f"{change_name}.md")

    # Update index
    index_file = _get_structure_dir(project_root) / "index.md"
    yaml_file = _get_structure_dir(project_root) / ".structure-index.yaml"

    # Update YAML index
    index_data = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or {}
    index_data["meta"]["last_updated"] = datetime.now().isoformat()
    index_data["meta"]["total_changes"] = index_data["meta"].get("total_changes", 0) + 1

    # Extract module info from delta
    delta_content = delta_file.read_text(encoding="utf-8")
    modules = index_data.setdefault("modules", {})
    for line in delta_content.split("\n"):
        if line.startswith("- `") and line.endswith("`"):
            mod_path = line.strip("- `").rstrip("`")
            if mod_path not in modules:
                modules[mod_path] = {"changes": [change_name]}
            else:
                modules[mod_path]["changes"].append(change_name)

    yaml_file.write_text(yaml.dump(index_data, allow_unicode=True, default_flow_style=False), encoding="utf-8")

    # Append to index.md
    git_head = _get_git_head(project_root)
    with open(index_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {change_name} ({datetime.now().strftime('%Y-%m-%d')})\n")
        f.write(f"> Git commit: {git_head}\n\n")
        f.write(delta_content)
        f.write("\n---\n")

    print(f"  Merged {change_name} into .stdd/code-structure/index.md")


def cmd_structure_rebuild(args):
    """Rebuild entire code structure index from deltas."""
    project_root = Path.cwd()
    deltas_dir = _get_structure_dir(project_root) / "deltas"
    if not deltas_dir.exists() or not list(deltas_dir.glob("*.md")):
        print("  No deltas to rebuild from.")
        return

    # Reset index
    index_file = _get_structure_dir(project_root) / "index.md"
    index_file.write_text("# 项目代码结构索引\n\n> 重建 | STDD V2.8\n\n", encoding="utf-8")

    yaml_file = _get_structure_dir(project_root) / ".structure-index.yaml"
    yaml_file.write_text(yaml.dump({"meta": {"last_updated": datetime.now().isoformat(),
                                              "total_changes": 0, "modules": {}}},
                                   allow_unicode=True, default_flow_style=False), encoding="utf-8")

    # Re-merge all deltas
    for delta_file in sorted(deltas_dir.glob("*.md")):
        change_name = delta_file.stem
        delta_content = delta_file.read_text(encoding="utf-8")
        with open(index_file, "a", encoding="utf-8") as f:
            f.write(f"\n## {change_name}\n")
            f.write(delta_content)
            f.write("\n---\n")

    print(f"  Index rebuilt from {len(list(deltas_dir.glob('*.md')))} deltas")


def cmd_structure_show(args):
    """Show module structure from index."""
    project_root = Path.cwd()
    yaml_file = _get_structure_dir(project_root) / ".structure-index.yaml"
    if not yaml_file.exists():
        print("  No structure index found. Run 'stdd structure merge <change>' first.")
        return

    index_data = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or {}
    modules = index_data.get("modules", {})

    if args.target:
        mod_info = modules.get(args.target)
        if mod_info:
            print(f"\n  Module: {args.target}")
            print(f"  Changes: {', '.join(mod_info.get('changes', []))}")
        else:
            print(f"  Module '{args.target}' not found in index")
    else:
        print(f"\n  Code Structure Index")
        print(f"  Total changes: {index_data['meta'].get('total_changes', 0)}")
        print(f"  Total modules: {len(modules)}")
        print(f"  Last updated: {index_data['meta'].get('last_updated', 'unknown')}")
        if modules:
            print(f"\n  Modules:")
            for mod_path, info in sorted(modules.items()):
                print(f"    {mod_path} ({len(info.get('changes', []))} changes)")
        print()


def cmd_structure_graph(args):
    """Output ASCII dependency graph from index."""
    project_root = Path.cwd()
    yaml_file = _get_structure_dir(project_root) / ".structure-index.yaml"
    if not yaml_file.exists():
        print("  No structure index found.")
        return

    index_data = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or {}
    modules = index_data.get("modules", {})

    print("\n  Code Structure Graph")
    print("  " + "─" * 30)
    for mod_path in sorted(modules.keys()):
        depth = mod_path.count("/")
        indent = "  " * (depth + 1)
        print(f"{indent}├── {mod_path.split('/')[-1]}")
    print()


def _get_git_head(project_root: Path) -> str:
    import subprocess
    try:
        result = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True, cwd=project_root)
        return result.stdout.strip()
    except Exception:
        return "unknown"


def _dispatch(args):
    """Route to appropriate structure subcommand."""
    action_map = {
        "delta": cmd_structure_delta,
        "merge": cmd_structure_merge,
        "rebuild": cmd_structure_rebuild,
        "show": cmd_structure_show,
        "graph": cmd_structure_graph,
    }
    func = action_map.get(args.action)
    if func:
        func(args)
    else:
        print(f"  Unknown structure action: {args.action}")
        sys.exit(1)
