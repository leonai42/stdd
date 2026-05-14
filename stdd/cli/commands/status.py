import argparse
import sys
from pathlib import Path

import yaml


def cmd_status(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir

    project_root = Path.cwd()

    change_dir = find_change_dir(args.name, project_root)
    if change_dir is None:
        print(f" 找不到 change: {args.name or '(无)'}")
        sys.exit(1)

    state_file = change_dir / ".stdd.yaml"
    if not state_file.exists():
        print(" 缺少 .stdd.yaml 状态文件")
        sys.exit(1)

    with open(state_file, "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)

    print(f"\n  Change: {state.get('change_id', change_dir.name)}")
    print(f"   状态: {state.get('status', 'unknown')}")
    print(f"   当前阶段: {state.get('current_phase', 'unknown')}")
    long_range = state.get("long_range", {})
    mode = long_range.get("mode", None)
    if mode == "full_auto":
        print(f"   执行模式:   全自动长程模式")
    elif mode == "normal" or mode is None:
        print(f"   执行模式:   普通交互模式（默认）")
    else:
        print(f"   执行模式: {mode}")
    print()

    phase_order = ["understand", "spec", "slice", "build", "verify", "deliver"]
    phase_names = {
        "understand": "Phase 1: UNDERSTAND (需求理解)",
        "spec": "Phase 2: SPEC (规格设计)",
        "slice": "Phase 3: SLICE (切片规划)",
        "build": "Phase 4: BUILD (TDD实现)",
        "verify": "Phase 5: VERIFY (质量验证)",
        "deliver": "Phase 6: DELIVER (交付)",
    }
    status_icons = {
        "pending": "  ",
        "in_progress": "  ",
        "completed": "  ",
    }

    for phase in phase_order:
        phase_info = state.get("phases", {}).get(phase, {})
        phase_status = phase_info.get("status", "pending")
        icon = status_icons.get(phase_status, " ?")
        name = phase_names.get(phase, phase)
        confirmed = phase_info.get("confirmed_at", "")
        confirm_str = f" (确认于 {confirmed})" if confirmed else ""
        print(f"   {icon}  {name}: {phase_status}{confirm_str}")

    print(f"\n  文件状态:")
    expected_files = [
        "proposal.md", "design.md", "test-plan.md",
        "tasks.md", "test-report.md", "design-adjustments.md"
    ]
    for f in expected_files:
        exists = (change_dir / f).exists()
        icon = "  " if exists else "  "
        print(f"   {icon}  {f}")

    specs_dir = change_dir / "specs"
    if specs_dir.exists():
        spec_files = list(specs_dir.rglob("*.md"))
        print(f"     Spec 文件: {len(spec_files)} 个")
        for sf in spec_files:
            print(f"      - {sf.relative_to(change_dir)}")
