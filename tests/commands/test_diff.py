"""测试 cmd_diff 命令。"""
import argparse
import pytest
from pathlib import Path

from stdd.cli.commands.diff import cmd_diff


def test_diff_with_test_plan(sample_change_with_specs: Path, monkeypatch):
    """有 test-plan 的 change 可以正常 diff。"""
    monkeypatch.chdir(sample_change_with_specs.parent.parent)
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    cmd_diff(args)  # 不应崩溃


def test_diff_no_test_plan(sample_change: Path, monkeypatch):
    """无 test-plan 时报告错误。"""
    monkeypatch.chdir(sample_change.parent.parent)
    # 删除 test-plan
    tp = sample_change / "test-plan.md"
    if tp.exists():
        tp.unlink()
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_diff(args)


def test_diff_nonexistent_change(temp_project: Path, monkeypatch):
    """不存在的 change 报告错误。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(name="nonexistent", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_diff(args)


def test_diff_with_tc_references(sample_change: Path, monkeypatch):
    """TC-ID 在源码中有引用时显示覆盖状态。"""
    monkeypatch.chdir(sample_change.parent.parent)

    # 创建含 TC-ID 的 test-plan
    tp = """# Test Plan
#### 案例 1 — 测试入口兼容性
| **ID** | TC-CLI-101 |
| **预期结果** | 输出与拆分前一致；退出码 0 |

#### 案例 2 — 未覆盖案例
| **ID** | TC-NONE-999 |
| **预期结果** | 无对应源码 |
"""
    (sample_change / "test-plan.md").write_text(tp, encoding="utf-8")

    # 在源码中引用 TC-CLI-101
    test_dir = sample_change.parent.parent / "tests"
    test_dir.mkdir(exist_ok=True)
    (test_dir / "test_example.py").write_text(
        "# TC-CLI-101: 测试入口兼容性\ndef test_stdd_entry():\n    pass\n",
        encoding="utf-8"
    )

    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    cmd_diff(args)  # 应正常完成


def test_diff_empty_test_plan(sample_change: Path, monkeypatch):
    """test-plan 没有 TC-ID 时报错。"""
    monkeypatch.chdir(sample_change.parent.parent)
    (sample_change / "test-plan.md").write_text("# Empty Plan\nNo TC cases here", encoding="utf-8")
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_diff(args)
