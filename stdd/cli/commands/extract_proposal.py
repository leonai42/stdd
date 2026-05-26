"""stdd extract-proposal — Extract structured data from proposal.md."""
import argparse
import sys
import re
import json
from pathlib import Path

import yaml


def _parse_section(content: str, heading: str) -> list[str]:
    """Extract bullet list items from a markdown section."""
    # Find the target heading and the next heading of same or higher level
    heading_pattern = rf"^##\s+{re.escape(heading)}\s*$"
    next_section_pattern = r"^##\s+"
    lines = content.split("\n")
    start = None
    for i, line in enumerate(lines):
        if start is None and re.match(heading_pattern, line):
            start = i + 1
        elif start is not None and re.match(next_section_pattern, line):
            end = i
            break
    else:
        end = len(lines) if start is not None else 0

    if start is None:
        return []

    section = "\n".join(lines[start:end])
    items = re.findall(r"^[ \t]*(?:-|\*)\s+(.+)", section, re.MULTILINE)
    return [item.strip() for item in items]


def _parse_capabilities(content: str) -> dict:
    """Parse New and Modified capabilities from proposal.md."""
    result = {"new": [], "modified": []}

    # Look for Capabilities section with subsections
    cap_section = re.search(r"##\s+Capabilities\s*\n(.*?)(?=\n##\s+|\Z)", content, re.DOTALL)
    if not cap_section:
        return result

    section = cap_section.group(1)

    # Parse New Capabilities
    new_match = re.search(r"###\s+New\s+Capabilities?\s*\n(.*?)(?=###|\Z)", section, re.DOTALL)
    if new_match:
        new_items = re.findall(r"- \*\*(.+?)\*\*：(.+)", new_match.group(1))
        for name, desc in new_items:
            result["new"].append({"name": name.strip(), "description": desc.strip()})

    # Parse Modified Capabilities
    mod_match = re.search(r"###\s+Modified\s+Capabilities?\s*\n(.*?)(?=###|\Z)", section, re.DOTALL)
    if mod_match:
        mod_items = re.findall(r"- \*\*(.+?)\*\*：(.+)", mod_match.group(1))
        for name, desc in mod_items:
            result["modified"].append({"name": name.strip(), "description": desc.strip()})

    return result


def _parse_impact(content: str) -> dict:
    """Parse Impact section from proposal.md."""
    result = {"code": [], "config": [], "infrastructure": []}
    impact = re.search(r"##\s+Impact\s*\n(.*?)(?=\n##\s+|\Z)", content, re.DOTALL)
    if not impact:
        return result

    section = impact.group(1)
    # Parse bold-labeled sub-items: **代码层面**：\n- item
    for label, key in [("代码层面", "code"), ("配置层面", "config"), ("基础设施", "infrastructure")]:
        sub = re.search(rf"\*\*{label}\*\*[：:]\s*\n((?:(?:-|\*)\s+.+\n?)+)", section)
        if sub:
            items = re.findall(r"(?:-|\*)\s+(.+)", sub.group(1))
            result[key] = [i.strip() for i in items]

    return result


def _parse_risk_areas(content: str) -> list[dict]:
    """Parse Risk Areas section with structured capability mapping.

    Expected format:
    ## Risk Areas
    - capability: <name> — <risk description>
    """
    items = _parse_section(content, "Risk Areas")
    result = []
    for item in items:
        # Try "capability: <name> — <risk>" format
        m = re.match(r"capability:\s*(\S+)\s*[—\-]\s*(.+)", item)
        if m:
            result.append({"capability": m.group(1), "risk": m.group(2)})
        elif item.startswith("capability:"):
            parts = item.split(":", 1)
            cap_name = parts[1].strip().split("—")[0].strip() if "—" in parts[1] else parts[1].strip().split("-")[0].strip()
            risk = parts[1].split("—", 1)[-1].strip() if "—" in parts[1] else parts[1].split("-", 1)[-1].strip()
            result.append({"capability": cap_name, "risk": risk})
        else:
            result.append({"capability": "", "risk": item})
    return result


def cmd_extract_proposal(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    get_logger()

    project_root = Path.cwd()
    change_dir = find_change_dir(args.name, project_root)
    if change_dir is None:
        print(f" 找不到 change: {args.name or '(无)'}")
        sys.exit(1)

    proposal_path = change_dir / "proposal.md"
    if not proposal_path.exists():
        print(f" 错误: proposal.md 不存在 ({change_dir})")
        sys.exit(1)

    content = proposal_path.read_text(encoding="utf-8")

    # Extract title from first heading
    title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else change_dir.name

    result = {
        "title": title,
        "capabilities": _parse_capabilities(content),
        "what_changes": _parse_section(content, "What Changes"),
        "success_criteria": _parse_section(content, "Success Criteria"),
        "impact": _parse_impact(content),
        # V2.5 new fields — backward compatible (empty if not present)
        "constraints": _parse_section(content, "Constraints"),
        "stakeholders": _parse_section(content, "Stakeholders"),
        "risk_areas": _parse_risk_areas(content),
        "non_goals": _parse_section(content, "NonGoals"),
    }

    fmt = getattr(args, "format", "json") or "json"
    if fmt == "yaml":
        print(yaml.dump(result, allow_unicode=True, default_flow_style=False))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
