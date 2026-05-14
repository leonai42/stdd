"""STDD CLI — Spec+Test Driven Development 命令行工具"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional


def _init_parent_parser() -> argparse.ArgumentParser:
    """创建父解析器，包含 --dry-run 和 --verbose 全局选项。"""
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--dry-run", action="store_true", help="预览操作，不实际修改文件系统")
    parent.add_argument("-v", "--verbose", action="count", default=0, help="详细输出（-v INFO, -vv DEBUG）")
    return parent


def main() -> None:
    from .utils import setup_logging, fix_windows_encoding, get_stdd_source
    from pathlib import Path

    fix_windows_encoding()

    # 初始化 STDD_SOURCE（bin/stdd 所在的项目根目录）
    from .utils import STDD_SOURCE as _src
    if _src is None:
        import os
        # 从 sys.argv[0] 推断
        bin_path = Path(sys.argv[0]).resolve()
        if bin_path.parent.name == "bin" and (bin_path.parent.parent / "STDD.md").exists():
            from . import utils
            utils.STDD_SOURCE = bin_path.parent.parent

    parent = _init_parent_parser()

    parser = argparse.ArgumentParser(
        description="STDD CLI — Spec+Test Driven Development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parent],
        epilog="""
示例:
  stdd init                    初始化 STDD 到当前项目
  stdd new fix-login-bug       创建新 change
  stdd validate                验证当前 change
  stdd status                  查看当前 change 状态
  stdd archive v1.5-stable     归档已完成的 change
  stdd trace TC-CASUAL-001     追溯 spec<->test<->code 链
  stdd install claude-code     安装到 Claude Code
  stdd rollback my-feature     从 archive 恢复 change
  stdd diff my-feature         显示 spec<->test 覆盖差异
  stdd abort experiment        放弃变更
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化 STDD 到当前项目", parents=[parent])
    p_init.add_argument("--force", "-f", action="store_true", help="覆盖已存在的文件")

    # new
    p_new = subparsers.add_parser("new", help="创建新的 change 目录骨架", parents=[parent])
    p_new.add_argument("name", help="change 名称（如 fix-login-bug）")

    # validate
    p_validate = subparsers.add_parser("validate", help="验证 change 结构", parents=[parent])
    p_validate.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")

    # status
    p_status = subparsers.add_parser("status", help="显示 artifact 完成状态", parents=[parent])
    p_status.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")

    # archive
    p_archive = subparsers.add_parser("archive", help="归档已完成的 change", parents=[parent])
    p_archive.add_argument("name", help="change 目录名")
    p_archive.add_argument("--yes", "-y", action="store_true", help="跳过确认")
    p_archive.add_argument("--skip-specs", action="store_true", help="不合并 specs")

    # trace
    p_trace = subparsers.add_parser("trace", help="查看 spec<->test<->code 追溯链", parents=[parent])
    p_trace.add_argument("tc_id", help="TC-ID（如 TC-CASUAL-001）")

    # install
    p_install = subparsers.add_parser("install", help="安装 STDD 到指定平台", parents=[parent])
    p_install.add_argument("platform", help="目标平台 (claude-code, workbuddy, trae, cursor)")

    # rollback (V2.0 新增)
    p_rollback = subparsers.add_parser("rollback", help="从 archive 恢复已归档的 change", parents=[parent])
    p_rollback.add_argument("name", help="change 名称（支持模糊匹配）")

    # diff (V2.0 新增)
    p_diff = subparsers.add_parser("diff", help="显示 spec<->test<->code 覆盖差异", parents=[parent])
    p_diff.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")

    # abort (V2.0 新增)
    p_abort = subparsers.add_parser("abort", help="放弃变更并归档到 archive/aborted/", parents=[parent])
    p_abort.add_argument("name", help="change 名称")
    p_abort.add_argument("--yes", "-y", action="store_true", help="跳过确认")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    setup_logging(args.verbose)

    # 将 dry_run 附加到 args 供各命令使用
    commands = {
        "init": "stdd.cli.commands.init.cmd_init",
        "new": "stdd.cli.commands.new.cmd_new",
        "validate": "stdd.cli.commands.validate.cmd_validate",
        "status": "stdd.cli.commands.status.cmd_status",
        "archive": "stdd.cli.commands.archive.cmd_archive",
        "trace": "stdd.cli.commands.trace.cmd_trace",
        "install": "stdd.cli.commands.install.cmd_install",
        "rollback": "stdd.cli.commands.rollback.cmd_rollback",
        "diff": "stdd.cli.commands.diff.cmd_diff",
        "abort": "stdd.cli.commands.abort.cmd_abort",
    }

    if args.command in commands:
        import importlib
        mod_path, func_name = commands[args.command].rsplit(".", 1)
        mod = importlib.import_module(mod_path)
        func = getattr(mod, func_name)
    else:
        print(f" 未知命令: {args.command}")
        sys.exit(1)

    try:
        func(args)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
