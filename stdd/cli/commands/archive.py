import argparse
import re
import sys
import shutil
from pathlib import Path

import yaml


def cmd_archive(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    logger = get_logger()

    project_root = Path.cwd()
    change_dir = find_change_dir(args.name, project_root)

    if change_dir is None:
        print(f" 找不到 change: {args.name}")
        sys.exit(1)

    dry_run = getattr(args, "dry_run", False)

    state_file = change_dir / ".stdd.yaml"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f) or {}
        if state.get("phases", {}).get("verify", {}).get("status") != "completed":
            print("   Phase 5 (VERIFY) 尚未完成，确认要归档吗？")
            if not args.yes:
                resp = input("输入 y 继续: ")
                if resp.lower() != "y":
                    print("已取消")
                    sys.exit(0)

    archive_dir = project_root / "archive" / change_dir.name
    if archive_dir.exists():
        print(f" 归档目录已存在: archive/{change_dir.name}")
        sys.exit(1)

    if dry_run:
        print(f"[dry-run] 将移动 {change_dir.name} -> archive/{change_dir.name}")
        print(f"[dry-run] 将合并 specs 到 specs/")
        print(f"[dry-run] 将更新 .stdd.yaml status=archived")
        return

    # 合并 specs（在移动前，失败时源不受影响）
    archive_specs = change_dir / "specs"
    main_specs = project_root / "specs"
    if archive_specs.exists() and not args.skip_specs:
        for spec_file in archive_specs.rglob("*.md"):
            rel_path = spec_file.relative_to(archive_specs)
            dest = main_specs / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)

            if dest.exists():
                existing = dest.read_text(encoding="utf-8")
                new_content = spec_file.read_text(encoding="utf-8")

                # 冲突检测：同名 Requirement
                existing_reqs = set(re.findall(r"###\s+Requirement:\s*(.+)", existing))
                new_reqs = set(re.findall(r"###\s+Requirement:\s*(.+)", new_content))
                conflicts = existing_reqs & new_reqs
                if conflicts:
                    logger.warning("检测到重复 Requirement: %s", conflicts)
                    print(f"    冲突警告: 以下 Requirement 已存在于 {rel_path}:")
                    for c in conflicts:
                        print(f"      - {c}")
                    print(f"    将追加合并（可能产生重复内容）...")

                merge_note = f"\n\n<!-- 合并自 {change_dir.name} -->\n"
                combined = existing + merge_note + new_content
                dest.write_text(combined, encoding="utf-8")
                logger.info("合并: %s", rel_path)
            else:
                shutil.copy2(spec_file, dest)
                logger.info("新增: %s", rel_path)

    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f) or {}
        state["status"] = "archived"
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(state, f, allow_unicode=True, default_flow_style=False)

    shutil.move(str(change_dir), str(archive_dir))

    print(f" 归档完成: archive/{change_dir.name}")
    if not args.skip_specs:
        print(f" Specs 已合并到 specs/")
