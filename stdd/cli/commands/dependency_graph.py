"""stdd dependency-graph — Build dependency graph from spec GIVEN clauses."""
import argparse
import sys
import re
import json
from pathlib import Path
from collections import defaultdict


def _extract_capability_name(spec_dir_name: str) -> str:
    """Convert spec directory name to a readable label."""
    return spec_dir_name.replace("-", " ").title()


def _parse_given_clauses(content: str) -> list[str]:
    """Extract all GIVEN clause text from a spec file."""
    givens = []
    for match in re.finditer(r"\*\*GIVEN\*\*\s*(.+?)(?:\n|$)", content):
        givens.append(match.group(1).strip())
    return givens


def _parse_scenario_names(content: str) -> list[str]:
    """Extract all Scenario names from a spec file."""
    return re.findall(r"####\s+Scenario:\s*(.+)", content)


def _build_graph(specs_dir: Path) -> dict:
    """Build a dependency graph from all spec files in specs_dir."""
    nodes = []
    edges = []
    capability_names = set()
    capability_data = {}

    if not specs_dir.exists():
        return {"nodes": [], "edges": [], "zero_dependency": []}

    # First pass: collect all capability names and their data
    for spec_file in sorted(specs_dir.rglob("*.md")):
        # Determine capability name from parent directory
        cap_dir = spec_file.parent
        cap_name = cap_dir.name if cap_dir != specs_dir else spec_file.stem
        cap_label = _extract_capability_name(cap_name)
        capability_names.add(cap_name)

        content = spec_file.read_text(encoding="utf-8")
        scenarios = _parse_scenario_names(content)
        givens = _parse_given_clauses(content)

        capability_data[cap_name] = {
            "label": cap_label,
            "scenarios": scenarios,
            "givens": givens,
        }

    # Second pass: build edges by checking GIVEN references
    in_degree = defaultdict(int)

    for cap_name, data in capability_data.items():
        nodes.append({"id": cap_name, "label": data["label"]})

        for given_text in data["givens"]:
            for other_cap in capability_names:
                if other_cap == cap_name:
                    continue
                # Check if GIVEN text contains the other capability name
                # Use exact word-boundary matching on capability name parts
                cap_parts = other_cap.replace("-", " ")
                if _contains_word(given_text.lower(), other_cap.lower()) or \
                   _contains_word(given_text.lower(), cap_parts.lower()):
                    edges.append({
                        "from": cap_name,
                        "to": other_cap,
                        "reason": f"GIVEN: {given_text[:60]}",
                    })
                    in_degree[other_cap] += 1

    # Determine zero-dependency nodes
    zero_dep = [n["id"] for n in nodes if in_degree[n["id"]] == 0]

    # Detect cycles
    cycles = _detect_cycles(nodes, edges) if edges else []

    return {
        "nodes": nodes,
        "edges": edges,
        "zero_dependency": zero_dep,
        "cycles": cycles,
    }


def _contains_word(text: str, word: str) -> bool:
    """Check if word appears as a whole word/phrase in text using word boundaries."""
    return bool(re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text))


def _detect_cycles(nodes: list, edges: list) -> list[list[str]]:
    """Detect cycles in the dependency graph using DFS."""
    adj = defaultdict(list)
    for edge in edges:
        adj[edge["from"]].append(edge["to"])

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n["id"]: WHITE for n in nodes}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for neighbor in adj.get(node, []):
            if color.get(neighbor) == GRAY:
                # Found cycle
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color.get(neighbor) == WHITE:
                dfs(neighbor, path)
        path.pop()
        color[node] = BLACK

    for node in nodes:
        if color[node["id"]] == WHITE:
            dfs(node["id"], [])

    return cycles


def _format_json(graph: dict) -> str:
    return json.dumps(graph, ensure_ascii=False, indent=2)


def _format_dot(graph: dict) -> str:
    lines = ["digraph STDD {", '  rankdir=LR;', '  node [shape=box, style=rounded];']
    for node in graph["nodes"]:
        color = "lightgreen" if node["id"] in graph.get("zero_dependency", []) else "lightblue"
        lines.append(f'  "{node["id"]}" [label="{node["label"]}", style=filled, fillcolor={color}];')
    for edge in graph["edges"]:
        lines.append(f'  "{edge["from"]}" -> "{edge["to"]}" [label="{edge["reason"][:30]}"];')
    lines.append("}")
    return "\n".join(lines)


def _format_text(graph: dict) -> str:
    lines = []
    lines.append(f"\n  Nodes: {len(graph['nodes'])}, Edges: {len(graph['edges'])}")
    if graph.get("cycles"):
        lines.append(f"  ⚠ 检测到 {len(graph['cycles'])} 个循环依赖:")
        for cycle in graph["cycles"]:
            lines.append(f"    {' ↔ '.join(cycle)}")
    if graph.get("zero_dependency"):
        lines.append("\n  零依赖节点（可并行）:")
        for nid in graph["zero_dependency"]:
            node = next((n for n in graph["nodes"] if n["id"] == nid), None)
            label = node["label"] if node else nid
            lines.append(f"    - {label} ({nid})")
    if graph["edges"]:
        lines.append("\n  依赖关系:")
        for edge in graph["edges"]:
            lines.append(f"    {edge['from']} → {edge['to']}  ({edge['reason'][:50]}...)")
    lines.append("")
    return "\n".join(lines)


def cmd_dependency_graph(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    get_logger()

    project_root = Path.cwd()
    change_dir = find_change_dir(args.name, project_root)
    if change_dir is None:
        print(f" 找不到 change: {args.name or '(无)'}")
        sys.exit(1)

    specs_dir = change_dir / "specs"
    if not specs_dir.exists():
        print(f" 错误: specs 目录不存在，无法构建依赖图 ({change_dir})")
        sys.exit(1)

    graph = _build_graph(specs_dir)

    fmt = getattr(args, "format", None) or "text"
    if fmt == "json":
        print(_format_json(graph))
    elif fmt == "dot":
        print(_format_dot(graph))
    else:
        print(_format_text(graph))

    if graph.get("cycles"):
        print(f"\n  ⚠ 检测到 {len(graph['cycles'])} 个循环依赖，请检查并修复。")
        sys.exit(1)
