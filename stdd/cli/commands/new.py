import argparse
import sys
import re
import shutil
from datetime import date
from pathlib import Path

import yaml


def cmd_new(args: argparse.Namespace) -> None:
    from ..utils import get_logger
    logger = get_logger()

    project_root = Path.cwd()
    change_name = args.name

    if not re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9_.]{1,49}\Z", change_name):
        print(f" 无效的 change 名称: {change_name}")
        print(f"   名称必须以字母或数字开头，可包含连字符(-)、下划线(_)、点(.)")
        print(f"   长度 2-50 字符，不能包含空格或特殊字符")
        print(f"   示例: fix-login-bug, feature_rate_limit, v1.2.1")
        sys.exit(1)

    today = date.today().isoformat()
    dir_name = f"{today}-{change_name}"
    change_dir = project_root / "changes" / dir_name

    if change_dir.exists():
        print(f" Change 目录已存在: changes/{dir_name}")
        sys.exit(1)

    dry_run = getattr(args, "dry_run", False)
    if dry_run:
        print(" [DRY-RUN] 将执行以下操作:")
        print(f"   创建 change 目录: changes/{dir_name}")
        print(f"   创建 specs 子目录: changes/{dir_name}/specs")
        print(f"   复制模板: proposal.md, design.md, test-plan.md")
        print(f"   创建状态文件: changes/{dir_name}/.stdd.yaml")
        print(f"   状态版本: 2.0, 状态: active")
        print(" [DRY-RUN] 文件系统未发生变化")
        return

    (change_dir / "specs").mkdir(parents=True)

    templates_dir = project_root / ".stdd" / "templates"
    for tmpl_name in ["proposal", "design", "test-plan"]:
        tmpl = templates_dir / f"{tmpl_name}.md"
        if tmpl.exists():
            shutil.copy2(tmpl, change_dir / f"{tmpl_name}.md")

    state = {
        "version": "2.0",
        "change_id": dir_name,
        "status": "active",
        "current_phase": "understand",
        "mode": "standard",           # V2.9: standard | lightweight | thorough
        "task_type": getattr(args, "task_type", "code") or "code",  # V2.9.4: from --task-type
        "complexity_score": None,     # V2.9: set by Phase 1 Step 3.5
        "score_confidence": None,     # V2.9: preliminary | confirmed
        "phases": {
            "understand": {"status": "pending"},
            "spec": {"status": "pending"},
            "slice": {"status": "pending"},
            "build": {"status": "pending"},
            "verify": {"status": "pending"},
            "deliver": {"status": "pending"},
        },
        "design_adjustments": {"count": 0},
        "traceability": {"spec_scenarios": 0, "tc_cases": 0, "test_functions": 0},
    }
    with open(change_dir / ".stdd.yaml", "w", encoding="utf-8") as f:
        yaml.dump(state, f, allow_unicode=True, default_flow_style=False)

    logger.info("Change 创建完成: changes/%s", dir_name)
    print(f" Change 创建完成: changes/{dir_name}")
    print(f"   模板已就绪: proposal.md, design.md, test-plan.md")
    print(f"   状态文件: .stdd.yaml")

    # V2.8: Two-Instance Kickoff
    if getattr(args, "parallel", False):
        _setup_parallel_worktrees(project_root, dir_name)

    print()
    print("  下一步:")
    print(f"   /stdd-understand  开始需求理解阶段")


def _setup_parallel_worktrees(project_root: Path, change_name: str):
    """V2.8: Create parallel worktrees for Two-Instance Kickoff."""
    import subprocess
    base = project_root / ".claude" / "worktrees"
    base.mkdir(parents=True, exist_ok=True)

    print(f"\n  🔀 Two-Instance Kickoff 模式")
    print(f"  {'─' * 40}")

    for suffix, role, desc in [
        ("-explore", "Explorer", "需求探索 → proposal.md"),
        ("-research", "Researcher", "技术调研 → research.md"),
    ]:
        wt_path = base / f"{change_name}{suffix}"
        if not wt_path.exists():
            result = subprocess.run(
                ["git", "worktree", "add", str(wt_path)],
                capture_output=True, text=True, cwd=project_root
            )
            if result.returncode == 0:
                print(f"  ✅ {role}: {wt_path}")
                print(f"     职责: {desc}")
            else:
                print(f"  ⚠️ {role}: 创建失败 — {result.stderr.strip()}")
        else:
            print(f"  ⚠️ {role}: worktree 已存在 — {wt_path}")

    print()
    print(f"  启动双 Agent (在两个终端中分别执行):")
    print(f"    Terminal 1 (Explorer):  cd {base}/{change_name}-explore  && claude")
    print(f"    Terminal 2 (Researcher): cd {base}/{change_name}-research && claude")
    print(f"  Gate 1 前合并双 Agent 结果到 changes/{change_name}/")
