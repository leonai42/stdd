"""rollback 命令 — 从 archive 恢复已归档的 change。"""
import argparse
import sys
import shutil
from pathlib import Path

import yaml


def cmd_rollback(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    logger = get_logger()

    project_root = Path.cwd()
    name = args.name

    archive_dir = project_root / "archive"
    if not archive_dir.exists():
        print(f" archive/ 目录不存在")
        sys.exit(1)

    # 在 archive 中查找匹配的目录
    target = None
    for d in sorted(archive_dir.iterdir(), reverse=True):
        if d.is_dir() and d.name.endswith(name) and (d / ".stdd.yaml").exists():
            target = d
            break

    if target is None:
        # 精确匹配
        exact = archive_dir / name
        if exact.exists() and exact.is_dir():
            target = exact

    if target is None:
        print(f" 在 archive 中找不到 change: {name}")
        sys.exit(1)

    # 检查 changes/ 下是否已有同名目录
    changes_dir = project_root / "changes"
    conflict_dir = changes_dir / target.name
    if conflict_dir.exists():
        print(f" 冲突: changes/{target.name} 已存在")
        print(f"   无法恢复，目标路径已被占用")
        sys.exit(1)

    logger.info("恢复 %s -> changes/%s", target.name, target.name)

    # 更新状态
    state_file = target / ".stdd.yaml"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f)
        state["status"] = "active"
        state["current_phase"] = "understand"
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(state, f, allow_unicode=True, default_flow_style=False)

    # 移动到 changes/
    shutil.move(str(target), str(conflict_dir))

    print(f" 已恢复: changes/{target.name}")
    print(f"   状态已更新为 active")
    print(f"   使用 /stdd-continue 或 stdd status {target.name} 查看")
