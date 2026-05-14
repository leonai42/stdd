"""测试 cmd_rollback 命令。"""
import argparse
import pytest
import yaml
from pathlib import Path

from stdd.cli.commands.rollback import cmd_rollback


def test_rollback_success(archived_change: Path, monkeypatch):
    """从 archive 成功恢复到 changes/。"""
    monkeypatch.chdir(archived_change.parent.parent)

    name_part = archived_change.name.split("-", 3)[-1]
    args = argparse.Namespace(name=name_part, dry_run=False, verbose=0)
    cmd_rollback(args)

    restored = archived_change.parent.parent / "changes" / archived_change.name
    assert restored.exists()
    assert not archived_change.exists()

    # 验证状态已更新为 active
    with open(restored / ".stdd.yaml", "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)
    assert state["status"] == "active"


def test_rollback_conflict(archived_change: Path, monkeypatch):
    """目标已存在时拒绝恢复。"""
    monkeypatch.chdir(archived_change.parent.parent)

    # 在 changes/ 下创建同名目录
    conflict_dir = archived_change.parent.parent / "changes" / archived_change.name
    conflict_dir.mkdir(parents=True)
    (conflict_dir / ".stdd.yaml").write_text("status: active", encoding="utf-8")

    name_part = archived_change.name.split("-", 3)[-1]
    args = argparse.Namespace(name=name_part, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_rollback(args)


def test_rollback_not_found(temp_project: Path, monkeypatch):
    """archive 中不存在时报错。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(name="nonexistent", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_rollback(args)


def test_rollback_dry_run(archived_change: Path, temp_project: Path, monkeypatch, capsys):
    """--dry-run 预览但不恢复。"""
    monkeypatch.chdir(temp_project)
    name_part = archived_change.name.split("-", 3)[-1]
    args = argparse.Namespace(name=name_part, dry_run=True, verbose=0)
    cmd_rollback(args)
    captured = capsys.readouterr()
    assert "[DRY-RUN]" in captured.out
    # 变更仍在 archive 中
    assert archived_change.exists()


def test_rollback_no_archive_dir(temp_project: Path, monkeypatch):
    """没有 archive/ 目录时报错。"""
    monkeypatch.chdir(temp_project)
    # 确保 archive 目录不存在
    archive = temp_project / "archive"
    if archive.exists():
        import shutil
        shutil.rmtree(archive)
    args = argparse.Namespace(name="anything", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_rollback(args)
