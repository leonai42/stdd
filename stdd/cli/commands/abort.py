"""abort 命令 — 放弃变更并归档到 archive/aborted/。"""
import argparse
import sys
import shutil
from pathlib import Path

import yaml


def cmd_abort(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    logger = get_logger()

    project_root = Path.cwd()
    change_dir = find_change_dir(args.name, project_root)

    if change_dir is None:
        print(f" 找不到 change: {args.name}")
        sys.exit(1)

    if not args.yes:
        print(f" 确认放弃变更: {change_dir.name}?")
        print(f"   此操作将把 change 移至 archive/aborted/")
        resp = input("输入 y 确认: ")
        if resp.lower() != "y":
            print("已取消")
            sys.exit(0)

    dry_run = getattr(args, "dry_run", False)
    if dry_run:
        print(" [DRY-RUN] 将执行以下操作:")
        print(f"   放弃变更: changes/{change_dir.name}")
        print(f"   移至: archive/aborted/{change_dir.name}")
        print(f"   更新状态: status=aborted")
        print(" [DRY-RUN] 文件系统未发生变化")
        return

    # 确保 archive/aborted/ 目录存在
    aborted_dir = project_root / "archive" / "aborted"
    aborted_dir.mkdir(parents=True, exist_ok=True)

    dest = aborted_dir / change_dir.name
    if dest.exists():
        print(f" archive/aborted/{change_dir.name} 已存在")
        print(f"   请手动处理冲突后重试")
        sys.exit(1)

    # 更新状态
    state_file = change_dir / ".stdd.yaml"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f)
        state["status"] = "aborted"
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(state, f, allow_unicode=True, default_flow_style=False)

    # 移动到 archive/aborted/
    shutil.move(str(change_dir), str(dest))

    logger.info("变更已放弃: %s", change_dir.name)
    print(f" 已放弃变更: archive/aborted/{change_dir.name}")
    print(f"   状态已更新为 aborted")
