"""测试 cmd_install 命令。"""
import argparse
import pytest
from pathlib import Path

from stdd.cli.commands.install import cmd_install


def test_install_unsupported_platform(temp_project: Path, monkeypatch):
    """不支持的平台被拒绝。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="unknown", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_install(args)


def test_install_claude_code(temp_project: Path, monkeypatch):
    """安装到 Claude Code。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="claude-code", dry_run=False, verbose=0)
    cmd_install(args)
    # 检查目标目录
    target = temp_project / ".claude" / "skills"
    assert target.exists()
    skills = list(target.iterdir())
    assert len(skills) >= 1


def test_install_cursor(temp_project: Path, monkeypatch):
    """安装到 Cursor（单文件模式）。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="cursor", dry_run=False, verbose=0)
    cmd_install(args)
    target = temp_project / ".cursor" / "rules" / "stdd.md"
    assert target.exists()


def test_install_trae(temp_project: Path, monkeypatch):
    """安装到 Trae。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="trae", dry_run=False, verbose=0)
    cmd_install(args)
    target = temp_project / ".trae" / "skills"
    assert target.exists()


def test_install_dry_run(temp_project: Path, monkeypatch, capsys):
    """--dry-run 预览但不安装文件。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="claude-code", dry_run=True, verbose=0)
    cmd_install(args)
    captured = capsys.readouterr()
    assert "[DRY-RUN]" in captured.out
    # 未创建 skills 目录
    target = temp_project / ".claude" / "skills"
    assert not target.exists()


def test_install_workbuddy(temp_project: Path, monkeypatch):
    """安装到 WorkBuddy。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="workbuddy", dry_run=False, verbose=0)
    # WorkBuddy 安装到 HOME 目录，需要 mock
    from unittest.mock import patch
    with patch('pathlib.Path.home', return_value=temp_project):
        cmd_install(args)
    target = temp_project / ".workbuddy" / "skills"
    assert target.exists()
