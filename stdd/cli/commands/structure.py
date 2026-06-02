"""STDD structure CLI — code structure summary management (V2.7)."""

import sys
import yaml
from pathlib import Path
from datetime import datetime


def cmd_structure_delta(args):
    """Generate code-structure-delta.md for a change."""
    change_dir = Path.cwd() / "changes" / args.target
    if not change_dir.exists():
        print(f"  changes/{args.target}/ not found")
        sys.exit(1)
    print(f"  [TODO] Generate delta for {args.target}")


def cmd_structure_merge(args):
    """Merge delta into .stdd/code-structure/index.md."""
    print(f"  [TODO] Merge delta for {args.target}")


def cmd_structure_rebuild(args):
    """Rebuild entire code structure index."""
    print("  [TODO] Rebuild index")


def cmd_structure_show(args):
    """Show module structure from index."""
    print(f"  [TODO] Show structure for {args.target}")


def cmd_structure_graph(args):
    """Output ASCII dependency graph."""
    print("  [TODO] Dependency graph")


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
