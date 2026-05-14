"""测试 cmd_trace 命令。"""
import argparse
import pytest
from pathlib import Path

from stdd.cli.commands.trace import cmd_trace


def test_trace_valid_tc_id(sample_change: Path, monkeypatch):
    """在 test-plan 中找到有效 TC-ID。"""
    monkeypatch.chdir(sample_change.parent.parent)
    tp = """# Test Plan
#### 案例 1 — 测试入口兼容性
| **ID** | TC-CLI-101 |
| **预期结果** | 输出与拆分前一致；退出码 0 |
"""
    (sample_change / "test-plan.md").write_text(tp, encoding="utf-8")
    args = argparse.Namespace(tc_id="TC-CLI-101", dry_run=False, verbose=0)
    cmd_trace(args)


def test_trace_invalid_format(sample_change: Path, monkeypatch):
    """无效 TC-ID 格式被拒绝。"""
    monkeypatch.chdir(sample_change.parent.parent)
    args = argparse.Namespace(tc_id="INVALID", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_trace(args)


def test_trace_not_found(sample_change: Path, monkeypatch):
    """TC-ID 在 test-plan 中不存在。"""
    monkeypatch.chdir(sample_change.parent.parent)
    (sample_change / "test-plan.md").write_text("# Test Plan\nNo TC here", encoding="utf-8")
    args = argparse.Namespace(tc_id="TC-NONE-999", dry_run=False, verbose=0)
    cmd_trace(args)  # 应正常执行，显示"未找到"


def test_trace_without_test_plan(sample_change: Path, monkeypatch):
    """无 test-plan.md 时的处理。"""
    monkeypatch.chdir(sample_change.parent.parent)
    if (sample_change / "test-plan.md").exists():
        (sample_change / "test-plan.md").unlink()
    args = argparse.Namespace(tc_id="TC-ANY-001", dry_run=False, verbose=0)
    cmd_trace(args)  # 不应崩溃
