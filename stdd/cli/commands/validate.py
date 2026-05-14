import argparse
import sys
import re
from pathlib import Path

import yaml


def cmd_validate(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    logger = get_logger()

    project_root = Path.cwd()

    change_dir = find_change_dir(args.name, project_root)
    if change_dir is None:
        print(f" 找不到 change: {args.name or '(无)'}")
        sys.exit(1)

    errors = []
    warnings = []

    required_files = ["proposal.md", "design.md", "test-plan.md", ".stdd.yaml"]
    for f in required_files:
        if not (change_dir / f).exists():
            errors.append(f"缺少必需文件: {f}")

    state_file = change_dir / ".stdd.yaml"
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f) or {}
        valid_phases = ["understand", "spec", "slice", "build", "verify", "deliver"]
        for phase in state.get("phases", {}):
            if phase not in valid_phases:
                errors.append(f".stdd.yaml: 无效的阶段: {phase}")

    specs_dir = change_dir / "specs"
    if specs_dir.exists():
        for spec_file in specs_dir.rglob("*.md"):
            content = spec_file.read_text(encoding="utf-8")
            scenarios = re.findall(r"####\s+Scenario:", content)
            given_count = len(re.findall(r"\*\*GIVEN\*\*", content))
            when_count = len(re.findall(r"\*\*WHEN\*\*", content))
            then_count = len(re.findall(r"\*\*THEN\*\*", content))

            if len(scenarios) == 0:
                warnings.append(f"{spec_file.name}: 未找到 Scenario")
            if given_count < len(scenarios):
                warnings.append(f"{spec_file.name}: GIVEN 数量 ({given_count}) 少于 Scenario 数量 ({len(scenarios)})")
            if when_count < len(scenarios):
                warnings.append(f"{spec_file.name}: WHEN 数量 ({when_count}) 少于 Scenario 数量 ({len(scenarios)})")
            if then_count < len(scenarios):
                errors.append(f"{spec_file.name}: THEN 数量 ({then_count}) 少于 Scenario 数量 ({len(scenarios)})")

            then_pattern = re.findall(r"\*\*THEN\*\*\s*(.+?)(?:\n|$)", content)
            for t in then_pattern:
                if "SHALL" not in t:
                    warnings.append(f"{spec_file.name}: THEN 中未使用 SHALL: {t[:50]}...")

            # AND 数量检查
            and_count = len(re.findall(r"\*\*AND\*\*", content))
            if and_count > 5:
                warnings.append(f"{spec_file.name}: AND 数量 ({and_count}) 超过上限 (5)")

    test_plan = change_dir / "test-plan.md"
    if test_plan.exists():
        content = test_plan.read_text(encoding="utf-8")
        tc_ids = re.findall(r"(TC-[A-Z]+-\d{3})", content)
        duplicates = [tc for tc in tc_ids if tc_ids.count(tc) > 1]
        if duplicates:
            errors.append(f"test-plan.md: 重复的 TC-ID: {set(duplicates)}")
        if tc_ids:
            logger.info("共找到 %d 个 TC-ID, %d 个唯一", len(tc_ids), len(set(tc_ids)))

    if specs_dir.exists() and test_plan.exists():
        spec_scenarios = []
        for spec_file in specs_dir.rglob("*.md"):
            content = spec_file.read_text(encoding="utf-8")
            spec_scenarios.extend(re.findall(r"####\s+Scenario:\s*(.+)", content))

        tc_cases = len(re.findall(r"\*\*ID\*\*\s*\|", test_plan.read_text(encoding="utf-8")))

        logger.info("Spec Scenarios: %d, TC Cases: %d", len(spec_scenarios), tc_cases)
        if tc_cases < len(spec_scenarios):
            errors.append(f"test-plan.md: TC 案例数 ({tc_cases}) 少于 Spec Scenario 数 ({len(spec_scenarios)})")

    print()
    if errors:
        print(f" 验证失败 ({len(errors)} 个错误):")
        for e in errors:
            print(f"   - {e}")
    if warnings:
        print(f"  警告 ({len(warnings)} 个):")
        for w in warnings:
            print(f"   - {w}")
    if not errors and not warnings:
        print(f" 验证通过")
    if errors:
        sys.exit(1)
