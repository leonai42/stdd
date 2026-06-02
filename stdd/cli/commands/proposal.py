"""STDD proposal.yaml CLI — canonical proposal management (V2.7)."""

import sys
import yaml
from pathlib import Path
from datetime import datetime


def cmd_proposal_init(args):
    """Generate canonical/proposals/<change-id>.yaml from proposal.md."""
    change_dir = Path.cwd() / "changes" / args.change_name
    proposal_md = change_dir / "proposal.md"
    if not proposal_md.exists():
        print(f"proposal.md not found in changes/{args.change_name}/")
        sys.exit(1)

    canon_dir = Path.cwd() / "canonical" / "proposals"
    canon_dir.mkdir(parents=True, exist_ok=True)

    content = proposal_md.read_text(encoding="utf-8")
    data = _parse_proposal_md(content, args.change_name)

    yaml_file = canon_dir / f"{args.change_name}.yaml"
    yaml_file.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")
    print(f"  Generated canonical/proposals/{args.change_name}.yaml")


def _parse_proposal_md(content: str, change_id: str) -> dict:
    """Parse proposal.md into structured canonical YAML."""
    sections = _extract_sections(content)

    data = {
        "meta": {
            "change_id": change_id,
            "title": sections.get("title", change_id),
            "created": datetime.now().isoformat(),
            "status": "draft",
        },
        "why": {
            "problem": sections.get("why", ""),
            "motivation": "",
        },
        "what_changes": _parse_bullets(sections.get("what_changes", "")),
        "capabilities": {
            "new": _parse_named_items(sections.get("new_capabilities", "")),
            "modified": _parse_named_items(sections.get("modified_capabilities", "")),
        },
        "constraints": _parse_bullet_strings(sections.get("constraints", "")),
        "stakeholders": _parse_bullet_strings(sections.get("stakeholders", "")),
        "risk_areas": _parse_bullet_strings(sections.get("risk_areas", "")),
        "non_goals": _parse_bullet_strings(sections.get("non_goals", "")),
        "critical": {"is_critical": False},
        "anchoring": {"level": "L1"},
        "success_criteria": _parse_checkboxes(sections.get("success_criteria", "")),
    }
    return data


def _extract_sections(content: str) -> dict:
    """Simple section extractor — splits by ## headings."""
    sections = {}
    current_heading = None
    current_content = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_heading:
                sections[current_heading] = "\n".join(current_content).strip()
            current_heading = line[3:].strip().lower().replace(" ", "_")
            current_content = []
        elif current_heading:
            current_content.append(line)

    if current_heading:
        sections[current_heading] = "\n".join(current_content).strip()

    # Extract title from first line
    for line in content.split("\n"):
        if line.startswith("# ") and not line.startswith("## "):
            sections["title"] = line[2:].strip()
            break

    return sections


def _parse_bullets(text: str) -> list:
    """Parse bullet list items into structured dicts."""
    items = []
    idx = 0
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            idx += 1
            desc = stripped[2:].strip()
            # Strip ** markers
            desc = desc.replace("**", "")
            items.append({"id": f"C{idx}", "description": desc, "type": "new"})
    return items


def _parse_named_items(text: str) -> list:
    """Parse **name**：description format."""
    items = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- **"):
            # Extract name between ** **
            end_name = stripped.find("**", 4)
            if end_name > 0:
                name = stripped[4:end_name]
                desc_start = stripped.find("：", end_name)
                if desc_start < 0:
                    desc_start = stripped.find(":", end_name)
                desc = stripped[desc_start + 1:].strip() if desc_start > 0 else ""
                items.append({"name": name, "description": desc})
    return items


def _parse_bullet_strings(text: str) -> list:
    """Parse bullet list into string list."""
    items = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def _parse_checkboxes(text: str) -> list:
    """Parse checkbox list."""
    items = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            items.append(stripped[5:].strip())
        elif stripped.startswith("- [x]") or stripped.startswith("- [X]"):
            items.append(stripped[5:].strip())
    return items


def cmd_proposal_validate(args):
    """Validate proposal.yaml field completeness."""
    canon_dir = Path.cwd() / "canonical" / "proposals"
    yaml_file = canon_dir / f"{args.change_name}.yaml"

    if not yaml_file.exists():
        print(f"  canonical/proposals/{args.change_name}.yaml not found")
        sys.exit(1)

    data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))

    errors = []
    # Check required top-level fields
    for field in ["meta", "why", "capabilities"]:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")

    if "why" in data:
        if not data["why"].get("problem"):
            errors.append("Missing required field: why.problem")

    if "meta" in data:
        if not data["meta"].get("change_id"):
            errors.append("Missing required field: meta.change_id")

    if errors:
        for e in errors:
            print(f"  Error: {e}")
        sys.exit(1)

    print(f"  proposal.yaml validation passed")


def _dispatch(args):
    """Route to appropriate subcommand."""
    if args.action == "init":
        cmd_proposal_init(args)
    elif args.action == "validate":
        cmd_proposal_validate(args)
    elif args.action == "show":
        cmd_proposal_show(args)
    else:
        print(f"  Unknown proposal action: {args.action}")
        sys.exit(1)
