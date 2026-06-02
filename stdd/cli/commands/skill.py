"""STDD skill CLI — skill management (V2.7)."""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {name}
description: {description}
origin: STDD
version: 1.0.0
category: {category}
language: {language}
related_skills: []
---

# {title}

## 何时激活
<!-- 描述在什么条件下此 Skill 会被自动激活 -->

## 核心规范
<!-- 核心的编码规范或工作流指导 -->

## 反模式
<!-- 常见的错误模式及避免方法 -->

## 相关 STDD 经验
<!-- 与此 Skill 相关的经验库条目（如有） -->
"""


def cmd_skill_create(args):
    """Create a new STDD Skill from template."""
    project_root = Path.cwd()
    name = args.name
    skill_type = getattr(args, "type", "language")

    type_dir_map = {
        "language": "languages",
        "workflow": "workflow",
        "tools": "tools",
    }
    category_dir = type_dir_map.get(skill_type, "languages")

    skill_dir = project_root / ".stdd" / "skills" / category_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        print(f"  Skill already exists: .stdd/skills/{category_dir}/{name}/SKILL.md")
        sys.exit(1)

    content = SKILL_TEMPLATE.format(
        name=name,
        description=f"Auto-generated {skill_type} skill: {name}",
        category=skill_type,
        language="python",
        title=name.replace("-", " ").title(),
    )
    skill_md.write_text(content, encoding="utf-8")
    print(f"  Created .stdd/skills/{category_dir}/{name}/SKILL.md")
    print(f"  Next: edit the SKILL.md to fill in the actual content")


def _dispatch(args):
    """Route to appropriate skill subcommand."""
    if args.action == "create":
        cmd_skill_create(args)
    else:
        print(f"  Unknown skill action: {args.action}")
        sys.exit(1)
