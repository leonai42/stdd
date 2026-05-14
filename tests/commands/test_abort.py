"""测试 cmd_abort 命令。"""
import argparse
import pytest
import yaml
from pathlib import Path

from stdd.cli.commands.abort import cmd_abort


def test_abort_with_yes(sample_change: Path, monkeypatch):
    """--yes 确认后成功放弃变更。"""
    monkeypatch.chdir(sample_change.parent.parent)
    args = argparse.Namespace(name=None, yes=True, dry_run=False, verbose=0)
    cmd_abort(args)

    # change 已移至 archive/aborted/
    aborted = sample_change.parent.parent / "archive" / "aborted" / sample_change.name
    assert aborted.exists()
    assert not sample_change.exists()

    # 状态已更新
    with open(aborted / ".stdd.yaml", "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)
    assert state["status"] == "aborted"


def test_abort_nonexistent_change(temp_project: Path, monkeypatch):
    """不存在的 change 报告错误。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(name="nonexistent", yes=True, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_abort(args)


def test_abort_duplicate_dest(sample_change: Path, monkeypatch):
    """archive/aborted/ 下已存在同名的处理。"""
    monkeypatch.chdir(sample_change.parent.parent)

    # 先创建一个同名的 aborted 目录
    aborted_dir = sample_change.parent.parent / "archive" / "aborted"
    aborted_dir.mkdir(parents=True, exist_ok=True)
    (aborted_dir / sample_change.name).mkdir(parents=True, exist_ok=True)

    args = argparse.Namespace(name=None, yes=True, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_abort(args)

    # 原始 change 仍存在
    assert sample_change.exists()


def test_abort_dry_run(sample_change: Path, monkeypatch):
    """--dry-run 预览但不移动文件。"""
    monkeypatch.chdir(sample_change.parent.parent)
    args = argparse.Namespace(name=None, yes=True, dry_run=True, verbose=0)
    cmd_abort(args)
    # 文件系统未变化
    assert sample_change.exists()
    aborted = sample_change.parent.parent / "archive" / "aborted" / sample_change.name
    assert not aborted.exists()
