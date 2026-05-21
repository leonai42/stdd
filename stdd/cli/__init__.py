"""STDD CLI — Spec+Test Driven Development 命令行工具"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _init_parent_parser() -> argparse.ArgumentParser:
    """创建父解析器，包含 --dry-run 和 --verbose 全局选项。"""
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--dry-run", action="store_true", help="预览操作，不实际修改文件系统")
    parent.add_argument("-v", "--verbose", action="count", default=0, help="详细输出（-v INFO, -vv DEBUG）")
    return parent


def main() -> None:
    from .utils import setup_logging, fix_windows_encoding

    fix_windows_encoding()

    # 初始化 STDD_SOURCE（bin/stdd 所在的项目根目录）
    from .utils import STDD_SOURCE as _src
    if _src is None:
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

    # extract-proposal (V2.4 新增)
    p_extract = subparsers.add_parser("extract-proposal", help="从 proposal.md 提取结构化数据", parents=[parent])
    p_extract.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")
    p_extract.add_argument("--format", choices=["json", "yaml"], default="json", help="输出格式")

    # dependency-graph (V2.4 新增)
    p_dep = subparsers.add_parser("dependency-graph", help="构建 spec 依赖图", parents=[parent])
    p_dep.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")
    p_dep.add_argument("--format", choices=["json", "dot", "text"], default="text", help="输出格式")

    # ci (V2.4 新增)
    p_ci = subparsers.add_parser("ci", help="CI/CD 集成管理", parents=[parent])
    ci_subs = p_ci.add_subparsers(dest="subcommand", help="子命令")
    ci_subs.add_parser("init", help="生成所有 CI 配置文件", parents=[parent])
    p_ci_gen = ci_subs.add_parser("generate", help="生成单个 CI 配置文件", parents=[parent])
    p_ci_gen.add_argument("target", choices=["workflow", "pre-commit", "pr-template"], help="生成目标")
    p_ci_check = ci_subs.add_parser("check-failures", help="确定性失败模式检查", parents=[parent])
    p_ci_check.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")

    # experience (V2.4 新增)
    p_exp = subparsers.add_parser("experience", help="管理项目级 AI 经验库", parents=[parent])
    exp_subs = p_exp.add_subparsers(dest="subcommand", help="子命令")
    p_exp_list = exp_subs.add_parser("list", help="列出经验", parents=[parent])
    p_exp_list.add_argument("--category", help="按失败模式过滤")
    p_exp_list.add_argument("--language", help="按语言过滤")
    p_exp_list.add_argument("--lifecycle", help="按生命周期过滤")
    p_exp_list.add_argument("--severity", help="按严重程度过滤")
    p_exp_list.add_argument("--format", choices=["table", "json", "yaml"], default="table", help="输出格式")
    p_exp_add = exp_subs.add_parser("add", help="添加经验条目", parents=[parent])
    p_exp_add.add_argument("--category", required=True, help="失败模式类别")
    p_exp_add.add_argument("--pattern", required=True, help="错误模式描述")
    p_exp_add.add_argument("--root-cause", help="根本原因")
    p_exp_add.add_argument("--detection-trigger", help="检测信号")
    p_exp_add.add_argument("--fix-template", help="修复模板")
    p_exp_add.add_argument("--language", help="编程语言")
    p_exp_add.add_argument("--severity", choices=["critical", "high", "medium", "low"], default="medium")
    p_exp_add.add_argument("--tags", help="逗号分隔的标签")
    p_exp_add.add_argument("--source-change", help="来源 change")
    p_exp_add.add_argument("--body", help="Markdown body 内容")
    p_exp_stats = exp_subs.add_parser("stats", help="经验库统计", parents=[parent])
    p_exp_stats.add_argument("--format", choices=["table", "json"], default="table", help="输出格式")
    p_exp_export = exp_subs.add_parser("export", help="导出经验", parents=[parent])
    p_exp_export.add_argument("--output", "-o", help="输出文件路径")
    p_exp_export.add_argument("--format", choices=["json", "yaml"], default="json", help="导出格式")
    p_exp_export.add_argument("--no-sanitize", action="store_true", help="不脱敏")
    p_exp_pull = exp_subs.add_parser("pull", help="从社区拉取经验包", parents=[parent])
    p_exp_pull.add_argument("pack_name", help="经验包名称")
    p_exp_pull.add_argument("--source", help="社区源 URL")

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
        "extract-proposal": "stdd.cli.commands.extract_proposal.cmd_extract_proposal",
        "dependency-graph": "stdd.cli.commands.dependency_graph.cmd_dependency_graph",
        "ci": "stdd.cli.commands.ci.cmd_ci",
        "experience": "stdd.cli.commands.experience.cmd_experience",
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
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
