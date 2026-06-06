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
    p_new.add_argument("--task-type", dest="task_type", default="code",
                       choices=["code", "documentation", "configuration", "data-migration", "dependency-upgrade"],
                       help="任务类型 (默认: code)")

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
    p_ci_check = ci_subs.add_parser("check-failures", help="确定性失败模式检查（全量聚合）", parents=[parent])
    p_ci_check.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")
    p_ci_scope = ci_subs.add_parser("check-scope", help="范围蔓延检查 (b)", parents=[parent])
    p_ci_scope.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")
    p_ci_cov = ci_subs.add_parser("check-coverage", help="覆盖真空检查 (j)", parents=[parent])
    p_ci_cov.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")
    p_ci_ctr = ci_subs.add_parser("check-contracts", help="契约断层检查 (k)", parents=[parent])
    p_ci_ctr.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")

    # state (V2.5 新增)
    p_state = subparsers.add_parser("state", help="查看/恢复跨 Session 状态", parents=[parent])
    p_state.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")
    p_state.add_argument("--resume", action="store_true", help="显示恢复上下文")
    p_state.add_argument("--compact", "-c", action="store_true", help="紧凑单行输出（跨平台，省 token）")
    p_state.add_argument("--set", help="设置恢复字段（格式：KEY=VALUE）")

    # gate (V2.5 新增)
    p_gate = subparsers.add_parser("gate", help="Gate 确认管理", parents=[parent])
    gate_subs = p_gate.add_subparsers(dest="subcommand", help="子命令")
    p_gate_approve = gate_subs.add_parser("approve", help="确认 Gate", parents=[parent])
    p_gate_approve.add_argument("name", nargs="?", help="change 目录名（默认使用最近的）")
    p_gate_approve.add_argument("--gate", type=int, required=True, choices=[1, 2, 3], help="Gate 编号 (1/2/3)")

    # experience (V2.4 新增)
    p_exp = subparsers.add_parser("experience", help="管理项目级 AI 经验库", parents=[parent])
    exp_subs = p_exp.add_subparsers(dest="subcommand", help="子命令")
    p_exp_list = exp_subs.add_parser("list", help="列出经验", parents=[parent])
    p_exp_list.add_argument("--category", help="按失败模式过滤")
    p_exp_list.add_argument("--language", help="按语言过滤")
    p_exp_list.add_argument("--lifecycle", help="按生命周期过滤")
    p_exp_list.add_argument("--severity", help="按严重程度过滤")
    p_exp_list.add_argument("--format", choices=["table", "json", "yaml"], default="table", help="输出格式")
    p_exp_list.add_argument("--all", action="store_true", help="显示所有经验（含 retired）")
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
    p_exp_add.add_argument("--project-type", help="项目类型（python/go/static_site/docs/config 等）")
    p_exp_stats = exp_subs.add_parser("stats", help="经验库统计", parents=[parent])
    p_exp_stats.add_argument("--format", choices=["table", "json"], default="table", help="输出格式")
    p_exp_export = exp_subs.add_parser("export", help="导出经验", parents=[parent])
    p_exp_export.add_argument("--output", "-o", help="输出文件路径")
    p_exp_export.add_argument("--format", choices=["json", "yaml"], default="json", help="导出格式")
    p_exp_export.add_argument("--no-sanitize", action="store_true", help="不脱敏")
    p_exp_export.add_argument("--publish", action="store_true", help="发布到社区（脱敏 + 打包 tar.gz + lifecycle→shared）")
    p_exp_pull = exp_subs.add_parser("pull", help="从社区拉取经验包", parents=[parent])
    p_exp_pull.add_argument("pack_name", help="经验包名称")
    p_exp_pull.add_argument("--source", help="社区源 URL")
    p_exp_verify = exp_subs.add_parser("verify", help="验证经验（discovered → verified）", parents=[parent])
    p_exp_verify.add_argument("experience_id", help="经验 ID（如 EXP-2026-0001）")
    p_exp_deposit = exp_subs.add_parser("deposit", help="沉淀经验（verified → deposited）", parents=[parent])
    p_exp_deposit.add_argument("experience_id", help="经验 ID（如 EXP-2026-0001）")
    p_exp_retire = exp_subs.add_parser("retire", help="废弃经验（任意状态 → retired）", parents=[parent])
    p_exp_retire.add_argument("experience_id", help="经验 ID（如 EXP-2026-0001）")
    p_exp_retire.add_argument("--reason", help="废弃原因")
    # curate subcommand under experience
    p_curate = exp_subs.add_parser("curate", help="官方维护者整理工具", parents=[parent])
    curate_subs = p_curate.add_subparsers(dest="curate_subcommand", help="子命令")
    curate_subs.add_parser("pull", help="拉取全量经验包到 inbox", parents=[parent])
    curate_subs.add_parser("deduplicate", help="自动去重合并", parents=[parent])
    curate_subs.add_parser("review", help="逐条审核经验", parents=[parent])
    p_curate_pack = curate_subs.add_parser("pack", help="打包官方经验包", parents=[parent])
    p_curate_pack.add_argument("language", help="目标语言（如 python）")

    # V2.7: proposal — Canonical proposal management
    p_proposal = subparsers.add_parser("proposal", help="管理 Canonical proposal (V2.7)", parents=[parent])
    p_proposal.add_argument("action", choices=["init", "validate", "show"], help="操作")
    p_proposal.add_argument("change_name", nargs="?", help="change 名称")

    # V2.7: canon — Dual-track document management
    p_canon = subparsers.add_parser("canon", help="双轨制文档管理 (V2.7)", parents=[parent])
    canon_subs = p_canon.add_subparsers(dest="subcommand", help="子命令")
    p_canon_init = canon_subs.add_parser("init", help="初始化 canonical/ 目录", parents=[parent])
    p_canon_init.add_argument("--change", help="change 名称 (默认: 最近的 change)")
    p_canon_init.add_argument("--project-level", action="store_true", help="在项目根目录创建 (默认: changes/<change>/canonical/)")
    p_canon_gen = canon_subs.add_parser("generate", help="从 Canonical 生成 Human View", parents=[parent])
    p_canon_gen.add_argument("change_name", nargs="?", help="change 名称")
    p_canon_gen.add_argument("--type", choices=["proposal", "design", "spec"], default="proposal")
    p_canon_gen.add_argument("--all", action="store_true", help="生成所有 change 的 Human View")
    p_canon_verify = canon_subs.add_parser("verify", help="验证双轨一致性", parents=[parent])
    p_canon_verify.add_argument("change_name", help="change 名称")

    # V2.7: index — Project-level index management
    p_index = subparsers.add_parser("index", help="项目索引管理 (V2.7)", parents=[parent])
    p_index.add_argument("action", choices=["update", "show", "trace"], help="操作")
    p_index.add_argument("target", nargs="?", help="capability 名称 (show) 或 file 路径 (trace)")

    # V2.7: agent — Agent verification pipeline
    p_agent = subparsers.add_parser("agent", help="Agent 行为验证 (V2.7)", parents=[parent])
    p_agent.add_argument("action", choices=["verify"], help="操作")
    p_agent.add_argument("task", nargs="?", help="任务 ID (对应 agent_spec.yaml)")
    p_agent.add_argument("--cp", help="仅执行指定检查点")
    # --dry-run 由父解析器提供，agent 直接使用 args.dry_run

    # V2.7: hooks — Lifecycle hooks management
    p_hooks = subparsers.add_parser("hooks", help="生命周期 Hooks 管理 (V2.7)", parents=[parent])
    p_hooks.add_argument("action", choices=["install", "status", "uninstall"], help="操作")
    p_hooks.add_argument("--force", action="store_true", help="覆盖已有配置")

    # V2.7: structure — Code structure summary management
    p_structure = subparsers.add_parser("structure", help="代码结构摘要管理 (V2.7)", parents=[parent])
    p_structure.add_argument("action", choices=["delta", "merge", "rebuild", "show", "graph"], help="操作")
    p_structure.add_argument("target", nargs="?", help="change 名称 (delta/merge) / module 名称 (show)")

    # V2.7: skill — Skill management
    p_skill = subparsers.add_parser("skill", help="Skill 管理 (V2.7)", parents=[parent])
    p_skill.add_argument("action", choices=["create"], help="操作")
    p_skill.add_argument("name", nargs="?", help="Skill 名称")
    p_skill.add_argument("--type", choices=["language", "workflow", "tools"], default="language")

    # V2.8: fix — Plankton multi-level auto-fix
    p_fix = subparsers.add_parser("fix", help="多级自动修复 (V2.8)", parents=[parent])
    p_fix.add_argument("--level", type=int, choices=[1, 2, 3], default=1, help="修复级别 (1=静默 2=建议 3=报告)")
    # --dry-run inherited from parent parser

    # V2.9: upgrade — version upgrade management
    p_upgrade = subparsers.add_parser("upgrade", help="升级 STDD 版本 (V2.9)", parents=[parent])
    p_upgrade.add_argument("--check", action="store_true", help="仅检查版本差异，不执行升级")
    p_upgrade.add_argument("--all", action="store_true", help="对所有已注册项目执行操作")
    p_upgrade.add_argument("--lock", action="store_true", help="锁定当前项目在当前版本")
    p_upgrade.add_argument("--unlock", action="store_true", help="解锁当前项目")
    p_upgrade.add_argument("--yes", "-y", action="store_true", help="跳过确认提示")

    # V2.9: batch — lightweight change batch management
    p_batch = subparsers.add_parser("batch", help="轻量变更批次管理 (V2.9)", parents=[parent])
    p_batch.add_argument("action", nargs="?", choices=["open", "add", "close", "archive", "list", "status"],
                         default="status", help="操作 (默认: status)")
    p_batch.add_argument("description", nargs="?", default="",
                         help="批次描述 (open/add 时使用)")
    p_batch.add_argument("--force", action="store_true",
                         help="强制闭合 (跳过近空批次保护)")
    p_batch.add_argument("--strategy", choices=["monthly", "weekly", "count_based"],
                         default="monthly", help="批次策略 (默认: monthly)")

    # V2.9.3: guard — intelligent enforcement gate
    p_guard = subparsers.add_parser("guard", help="项目级智能门禁 (V2.9.3)", parents=[parent])
    p_guard.add_argument("action", nargs="?", choices=["check", "status", "init", "disable", "enable"],
                         default="check", help="操作 (默认: check)")
    p_guard.add_argument("--check", dest="action", action="store_const", const="check",
                         help="等价于 'check' 位置参数 — 兼容 hook 命令")
    p_guard.add_argument("--platform", default="claude-code",
                         help="目标平台 (默认: claude-code)")
    p_guard.add_argument("--strict", action="store_true",
                         help="严格模式：allow_bypass 也阻止")
    p_guard.add_argument("--quiet", "-q", action="store_true",
                         help="静默模式")

    # V2.9.4: phase — advance and check change phase
    p_phase = subparsers.add_parser("phase", help="变更阶段管理 (V2.9.4)", parents=[parent])
    p_phase.add_argument("phase_action", nargs="?", choices=["status", "advance", "set"],
                         default="status", help="操作 (默认: status)")
    p_phase.add_argument("name", nargs="?", help="change 目录名（默认: 最近的）")
    p_phase.add_argument("target_phase", nargs="?", help="目标阶段 (set 时使用)")

    # V2.7: experience list — add provenance filter
    p_exp_list.add_argument("--provenance", help="按来源过滤 (ci-detected / ai-inferred / human-reported / community-imported)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    setup_logging(args.verbose)

    # V2.9: Startup version check (non-blocking, skip for upgrade command itself)
    if args.command != "upgrade":
        from .utils import try_version_check
        try_version_check(Path.cwd())

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
        "state": "stdd.cli.commands.state.cmd_state",
        "gate": "stdd.cli.commands.gate.cmd_gate",
        # V2.7 new commands
        "proposal": "stdd.cli.commands.proposal._dispatch",
        "canon": "stdd.cli.commands.canon._dispatch",
        "index": "stdd.cli.commands.index._dispatch",
        "agent": "stdd.cli.commands.agent._dispatch",
        "hooks": "stdd.cli.commands.hooks._dispatch",
        "structure": "stdd.cli.commands.structure._dispatch",
        "skill": "stdd.cli.commands.skill._dispatch",
        # V2.8 new commands
        "fix": "stdd.cli.commands.fix._dispatch",
        # V2.9 new commands
        "upgrade": "stdd.cli.commands.upgrade.cmd_upgrade",
        "batch": "stdd.cli.commands.batch.cmd_batch",
        # V2.9.3+ new commands
        "guard": "stdd.cli.commands.guard.cmd_guard",
        "phase": "stdd.cli.commands.phase.cmd_phase",
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
