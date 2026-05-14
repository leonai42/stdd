"""测试 cmd_status 命令。"""
import argparse
import pytest
from pathlib import Path

from stdd.cli.commands.status import cmd_status


def test_status_valid_change(sample_change: Path, monkeypatch):
    """正常显示 change 状态。"""
    monkeypatch.chdir(sample_change.parent.parent)
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    cmd_status(args)  # 不应抛异常


def test_status_with_name(sample_change: Path, monkeypatch):
    """按名称显示状态。"""
    monkeypatch.chdir(sample_change.parent.parent)
    name_part = sample_change.name.split("-", 3)[-1]
    args = argparse.Namespace(name=name_part, dry_run=False, verbose=0)
    cmd_status(args)


def test_status_nonexistent_change(temp_project: Path, monkeypatch):
    """不存在的 change 报告错误。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(name="nonexistent", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_status(args)


def test_status_missing_state_file(temp_project: Path, monkeypatch):
    """缺少 .stdd.yaml 时报告错误。"""
    monkeypatch.chdir(temp_project)
    d = temp_project / "changes" / "2026-01-01-no-state"
    d.mkdir(parents=True)
    args = argparse.Namespace(name="2026-01-01-no-state", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_status(args)
