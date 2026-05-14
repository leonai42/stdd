"""diff 命令 — 显示 spec<->test<->code 覆盖差异表。"""
import argparse
import re
import sys
from pathlib import Path


def cmd_diff(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    logger = get_logger()

    project_root = Path.cwd()
    change_dir = find_change_dir(args.name, project_root)

    if change_dir is None:
        print(f" 找不到 change: {args.name or '(无)'}")
        sys.exit(1)

    test_plan = change_dir / "test-plan.md"
    if not test_plan.exists():
        print(f" 无 test-plan.md")
        print(f"   当前 change ({change_dir.name}) 不包含测试方案文件")
        sys.exit(1)

    content = test_plan.read_text(encoding="utf-8")

    # 解析 test-plan 提取所有 TC 案例
    tc_cases = []
    lines = content.split("\n")
    current_case = {}
    in_table = False

    for line in lines:
        # 检测案例块开始
        case_match = re.match(r"####\s+案例\s+[\d.]+\s*[—\-]\s*(.+)", line)
        if case_match:
            if current_case and "id" in current_case:
                tc_cases.append(current_case)
            current_case = {"title": case_match.group(1).strip()}
            in_table = True
            continue

        if in_table and current_case:
            id_match = re.search(r"\*\*ID\*\*\s*\|\s*(TC-[A-Z]+-\d{3})", line)
            if id_match:
                current_case["id"] = id_match.group(1)

            expected_match = re.search(r"\*\*预期结果\*\*\s*\|\s*([^|]+)", line)
            if expected_match:
                current_case["expected"] = expected_match.group(1).strip()

    if current_case and "id" in current_case:
        tc_cases.append(current_case)

    if not tc_cases:
        print(f" 未找到 TC 案例（无 TC-ID 条目）")
        sys.exit(1)

    # 搜索源码中的 TC-ID 引用
    tc_references = {}  # tc_id -> [(file, line_no)]
    source_dirs = [project_root / "tests", project_root / "stdd"]
    for src_dir in source_dirs:
        if src_dir.exists():
            for py_file in src_dir.rglob("*.py"):
                try:
                    fc = py_file.read_text(encoding="utf-8")
                    for tc in tc_cases:
                        tc_id = tc.get("id", "")
                        if tc_id and tc_id in fc:
                            if tc_id not in tc_references:
                                tc_references[tc_id] = []
                            for i, l in enumerate(fc.split("\n"), 1):
                                if tc_id in l:
                                    tc_references[tc_id].append((py_file, i))
                                    break
                except Exception:
                    logger.debug("无法解析文件 %s", py_file.name, exc_info=True)

    # 输出四列对照表
    print(f"\n  Spec->Test 覆盖差异: {change_dir.name}")
    print(f"{'Spec Scenario':<30} {'TC-ID':<18} {'测试函数':<22} {'源码'}")
    print("-" * 95)

    for tc in tc_cases:
        tc_id = tc.get("id", "?")
        title = tc.get("title", "?")[:28]
        refs = tc_references.get(tc_id, [])
        if refs:
            src_file = str(refs[0][0].relative_to(project_root))[:20]
            status = f"  {src_file}"
        else:
            status = "  未覆盖"

        # 查找测试函数
        test_func = ""
        tests_dir = project_root / "tests"
        if tests_dir.exists():
            for test_file in tests_dir.rglob("test_*.py"):
                try:
                    fc = test_file.read_text(encoding="utf-8")
                    if tc_id in fc:
                        # 找到引用的测试函数
                        for l in fc.split("\n"):
                            if tc_id in l:
                                # 向上找 def test_
                                lines_list = fc.split("\n")
                                for j in range(len(lines_list)):
                                    if tc_id in lines_list[j]:
                                        for k in range(j, max(j - 50, -1), -1):
                                            if lines_list[k].strip().startswith("def test_"):
                                                test_func = lines_list[k].strip().replace("def ", "").replace("(self):", "").replace("():", "()")
                                                break
                                        break
                        break
                except Exception:
                    logger.debug("无法解析文件 %s", py_file.name, exc_info=True)

        print(f"{title:<30} {tc_id:<18} {test_func:<22} {status}")

    covered = sum(1 for tc in tc_cases if tc.get("id", "") in tc_references)
    print(f"\n   覆盖率: {covered}/{len(tc_cases)} TC 案例有源码引用 ({100*covered//max(len(tc_cases),1)}%)")
