import argparse
import sys
import re
from pathlib import Path


def cmd_trace(args: argparse.Namespace) -> None:
    from ..utils import get_logger
    logger = get_logger()

    project_root = Path.cwd()
    tc_id = args.tc_id.upper()

    if not tc_id.startswith("TC-"):
        print(f" 无效的 TC-ID 格式: {tc_id}")
        print(f"   期望格式: TC-<CAPABILITY>-<NNN> (如 TC-CASUAL-001)")
        sys.exit(1)

    print(f"\n  追溯链: {tc_id}")
    print("=" * 60)

    found_in_test_plan = False

    def _search_test_plans(base_dir: Path, label: str):
        nonlocal found_in_test_plan
        if not base_dir.exists():
            return False
        for d in sorted(base_dir.iterdir(), reverse=True):
            test_plan = d / "test-plan.md"
            if test_plan.exists():
                content = test_plan.read_text(encoding="utf-8")
                if tc_id in content:
                    found_in_test_plan = True

                    # 逐行分段解析（不依赖 DOTALL 正则）
                    lines = content.split("\n")
                    case_title = ""
                    expected_result = ""
                    in_target_case = False
                    in_expected = False

                    for line in lines:
                        if line.startswith("####") and "案例" in line:
                            in_target_case = False
                            in_expected = False
                        if tc_id in line:
                            in_target_case = True
                            # 案例标题在同一行或上一行
                            title_match = re.search(r"####\s+案例\s+[\d.]+\s*[—\-]\s*(.+)", line)
                            if not title_match:
                                # 尝试从上一行或当前块开头提取
                                pass
                            else:
                                case_title = title_match.group(1).strip()
                            continue
                        if in_target_case:
                            # 提取案例标题（如果在 TC-ID 行之前出现）
                            title_match = re.search(r"####\s+案例\s+[\d.]+\s*[—\-]\s*(.+)", line)
                            if title_match:
                                case_title = title_match.group(1).strip()
                            # 提取预期结果
                            if "**预期结果**" in line:
                                in_expected = True
                                result_match = re.search(r"\*\*预期结果\*\*\s*\|\s*([^|]+)", line)
                                if result_match:
                                    expected_result = result_match.group(1).strip()
                                continue
                            if in_expected and line.strip().startswith("|"):
                                # 表格续行
                                pass
                            elif in_expected and line.strip() and not line.strip().startswith("|"):
                                in_expected = False
                            # 遇到下一个案例块则停止
                            if line.startswith("####") and "案例" in line and tc_id not in line:
                                break

                    print(f"  Test Plan ({label}): {d.name}/test-plan.md")
                    if case_title:
                        print(f"   案例标题: {case_title}")
                    else:
                        print(f"   状态: 已引用 (未能解析标题)")
                    if expected_result:
                        print(f"   预期结果: {expected_result[:80]}...")
                    else:
                        print(f"   状态: 已引用")

        return found_in_test_plan

    changes_dir = project_root / "changes"
    _search_test_plans(changes_dir, "changes")
    specs_dir = project_root / "specs"
    _search_test_plans(specs_dir, "specs")

    print()
    tests_dir = project_root / "tests"
    if tests_dir.exists():
        for test_file in tests_dir.rglob("test_*.py"):
            content = test_file.read_text(encoding="utf-8")
            if tc_id in content:
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if tc_id in line:
                        func_line = ""
                        for j in range(i, max(i - 50, -1), -1):
                            if lines[j].strip().startswith("def test_"):
                                func_line = lines[j].strip()
                                break
                        print(f"   测试: {test_file.relative_to(project_root)}")
                        if func_line:
                            print(f"   函数: {func_line}")
                        print(f"   行号: {i + 1}")
                        break

    if not found_in_test_plan:
        print("   未在 test-plan.md 中找到此 TC-ID")
