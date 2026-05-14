import argparse
import sys
import shutil
from pathlib import Path


def cmd_init(args: argparse.Namespace) -> None:
    project_root = Path.cwd()

    from ..utils import get_stdd_source, get_logger
    logger = get_logger()
    stdd_source = get_stdd_source()

    dirs = [
        ".stdd/skills",
        ".stdd/templates",
        ".stdd/standards",
        ".stdd/config.d",
        ".stdd/platforms/claude-code/skills",
        ".stdd/platforms/workbuddy/skills",
        ".stdd/platforms/trae/skills",
        "changes",
        "specs",
        "archive",
    ]
    for d in dirs:
        (project_root / d).mkdir(parents=True, exist_ok=True)

    files_to_copy = [
        ".stdd/config.d/project.yaml",
        ".stdd/config.d/gates.yaml",
        ".stdd/config.d/long_range.yaml",
        ".stdd/config.d/quality.yaml",
        ".stdd/skills/understand.md",
        ".stdd/skills/spec.md",
        ".stdd/skills/slice.md",
        ".stdd/skills/build.md",
        ".stdd/skills/verify.md",
        ".stdd/skills/deliver.md",
        ".stdd/templates/proposal.md",
        ".stdd/templates/design.md",
        ".stdd/templates/spec.md",
        ".stdd/templates/test-plan.md",
        ".stdd/templates/tasks.md",
        ".stdd/templates/slices.md",
        ".stdd/templates/design-adjustments.md",
        ".stdd/templates/test-report.md",
        ".stdd/standards/python.md",
        "STDD.md",
        "AGENTS.md",
    ]
    force = getattr(args, "force", False)
    copied = 0
    skipped = 0
    for f in files_to_copy:
        src = stdd_source / f
        dst = project_root / f
        if src.exists():
            if force or not dst.exists():
                shutil.copy2(src, dst)
                copied += 1
            else:
                skipped += 1

    for platform in ["claude-code", "workbuddy", "trae"]:
        platform_skills = stdd_source / ".stdd" / "platforms" / platform / "skills"
        if platform_skills.exists():
            for skill_file in platform_skills.iterdir():
                dst = project_root / ".stdd" / "platforms" / platform / "skills" / skill_file.name
                if force or not dst.exists():
                    shutil.copy2(skill_file, dst)
                    copied += 1
                else:
                    skipped += 1

    logger.info("STDD 初始化完成，已复制 %d 个文件", copied)
    print("STDD 初始化完成")
    print(f"   项目根目录: {project_root}")
    print(f"   已创建 .stdd/ 目录、changes/、specs/、archive/")
    if force and skipped > 0:
        print(f"   已复制 {copied} 个文件, 跳过 {skipped} 个已存在文件（使用 --force 覆盖）")
    print()
    print("  开始使用:")
    print("   /stdd-understand  <需求描述>    启动新变更的需求理解阶段")
    print("   /stdd-spec                      进入规格设计阶段")
    print("   /stdd-continue                  继续执行当前变更")
