import argparse
import sys
import shutil
from pathlib import Path


SKILL_META = {
    "understand": {
        "name": "stdd-understand",
        "description": "STDD Phase 1: 需求理解与确认 — 将模糊需求转化为清晰、可验证的变更提案（proposal.md）",
        "keywords": ["stdd-understand", "需求理解", "understand"],
    },
    "spec": {
        "name": "stdd-spec",
        "description": "STDD Phase 2: 规格设计 — 将 proposal 转化为可测试的 spec Scenario",
        "keywords": ["stdd-spec", "规格设计", "spec"],
    },
    "slice": {
        "name": "stdd-slice",
        "description": "STDD Phase 3: 切片规划 — 将 spec 拆分为可实现的开发切片",
        "keywords": ["stdd-slice", "切片规划", "slice"],
    },
    "build": {
        "name": "stdd-build",
        "description": "STDD Phase 4: TDD 实现 — 逐切片实现并通过测试",
        "keywords": ["stdd-build", "TDD实现", "build"],
    },
    "verify": {
        "name": "stdd-verify",
        "description": "STDD Phase 5: 质量验证 — 运行测试、覆盖率、lint 等质量检查",
        "keywords": ["stdd-verify", "质量验证", "verify"],
    },
    "deliver": {
        "name": "stdd-deliver",
        "description": "STDD Phase 6: 交付 — 归档 change、合并 specs、更新文档",
        "keywords": ["stdd-deliver", "交付", "deliver"],
    },
}


def _make_claude_code_frontmatter(meta: dict) -> str:
    return f"""---
name: {meta['name']}
description: "{meta['description']}"
---
"""


def _make_workbuddy_frontmatter(meta: dict) -> str:
    keywords = "\\n  - ".join(meta["keywords"])
    return f"""---
name: {meta['name']}
description: "{meta['description']}"
trigger_keywords:
  - {keywords}
---
"""


def _make_trae_frontmatter(meta: dict) -> str:
    return f"""---
name: {meta['name']}
description: "{meta['description']}"
---
"""


def cmd_install(args: argparse.Namespace) -> None:
    from ..utils import get_stdd_source, get_logger
    logger = get_logger()

    project_root = Path.cwd()
    stdd_source = get_stdd_source()
    platform = args.platform

    platform_map = {
        "claude-code": {
            "target_base": ".claude/skills",
            "description": "Claude Code",
            "frontmatter_fn": _make_claude_code_frontmatter,
            "is_dir_per_skill": True,
            "skill_filename": "SKILL.md",
        },
        "workbuddy": {
            "target_base": ".workbuddy/skills",
            "description": "WorkBuddy",
            "target_is_home": True,
            "home_subdir": ".workbuddy/skills",
            "frontmatter_fn": _make_workbuddy_frontmatter,
            "is_dir_per_skill": False,
            "skill_filename": None,
        },
        "trae": {
            "target_base": ".trae/skills",
            "description": "Trae",
            "frontmatter_fn": _make_trae_frontmatter,
            "is_dir_per_skill": False,
            "skill_filename": None,
        },
        "cursor": {
            "source": "STDD.md",
            "target_base": ".cursor/rules",
            "description": "Cursor",
            "single_file": True,
            "target_name": "stdd.md",
        },
    }

    if platform not in platform_map:
        print(f" 不支持的平台: {platform}")
        print(f"   支持的平台: {', '.join(platform_map.keys())}")
        sys.exit(1)

    cfg = platform_map[platform]

    if cfg.get("single_file"):
        source_file = stdd_source / cfg["source"]
        if not source_file.exists():
            print(f" 源文件不存在: {source_file}")
            sys.exit(1)
        target_dir = Path.home() / cfg["target_base"] if cfg.get("target_is_home") else project_root / cfg["target_base"]
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_dir / cfg.get("target_name", cfg["source"]))
        logger.info("已安装 STDD 到 %s", cfg["description"])
        print(f" 已安装 STDD 到 {cfg['description']}: {target_dir / cfg.get('target_name', cfg['source'])}")
    else:
        core_skills_dir = stdd_source / ".stdd" / "skills"
        if not core_skills_dir.exists():
            print(f" 核心 Skill 目录不存在: {core_skills_dir}")
            sys.exit(1)

        if cfg.get("target_is_home"):
            target_base = Path.home() / cfg["home_subdir"]
        else:
            target_base = project_root / cfg["target_base"]
        target_base.mkdir(parents=True, exist_ok=True)

        count = 0
        for skill_file in sorted(core_skills_dir.glob("*.md")):
            skill_content = skill_file.read_text(encoding="utf-8")
            skill_key = skill_file.stem  # understand, spec, slice, etc.

            meta = SKILL_META.get(skill_key, {
                "name": f"stdd-{skill_key}",
                "description": f"STDD {skill_key} phase",
                "keywords": [f"stdd-{skill_key}"],
            })

            frontmatter = cfg["frontmatter_fn"](meta)
            full_content = frontmatter + skill_content

            if cfg.get("is_dir_per_skill"):
                skill_dir = target_base / meta["name"]
                skill_dir.mkdir(parents=True, exist_ok=True)
                dest = skill_dir / cfg["skill_filename"]
            else:
                dest = target_base / f"{meta['name']}.md"

            dest.write_text(full_content, encoding="utf-8")
            count += 1

        logger.info("已安装 %d 个 STDD skills 到 %s", count, cfg["description"])
        print(f" 已安装 {count} 个 STDD skills 到 {cfg['description']}: {target_base}")

    print()
    print("  使用方式:")
    if platform == "claude-code":
        print("   /stdd-understand  <需求>    启动新变更")
        print("   /stdd-spec                  进入规格设计")
        print("   /stdd-continue              继续执行")
    elif platform == "workbuddy":
        print("   在对话框中输入: /reload stdd")
        print("   然后通过关键词触发 (如 'stdd-understand')")
    elif platform == "trae":
        print("   /stdd-understand  <需求>    启动新变更")
    elif platform == "cursor":
        print("   规则已安装到 .cursor/rules/stdd.md")
        print("   在 Cursor 中自动生效")
