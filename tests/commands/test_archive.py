"""测试 cmd_archive 命令。"""
import argparse
import pytest
import yaml
from pathlib import Path

from stdd.cli.commands.archive import cmd_archive


def test_archive_completed_change(sample_change: Path, monkeypatch):
    """归档已完成的 change。"""
    monkeypatch.chdir(sample_change.parent.parent)

    # 标记为 verify 完成
    state_file = sample_change / ".stdd.yaml"
    with open(state_file, "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)
    state["phases"]["verify"]["status"] = "completed"
    with open(state_file, "w", encoding="utf-8") as f:
        yaml.dump(state, f)

    args = argparse.Namespace(name=None, yes=True, skip_specs=False, dry_run=False, verbose=0)
    cmd_archive(args)

    assert not sample_change.exists()
    archived = sample_change.parent.parent / "archive" / sample_change.name
    assert archived.exists()


def test_archive_dry_run(sample_change: Path, monkeypatch):
    """--dry-run 预览但不执行。"""
    monkeypatch.chdir(sample_change.parent.parent)

    state_file = sample_change / ".stdd.yaml"
    with open(state_file, "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)
    state["phases"]["verify"]["status"] = "completed"
    with open(state_file, "w", encoding="utf-8") as f:
        yaml.dump(state, f)

    args = argparse.Namespace(name=None, yes=True, skip_specs=False, dry_run=True, verbose=0)
    cmd_archive(args)

    # 文件系统不应变化
    assert sample_change.exists()
    assert not (sample_change.parent.parent / "archive" / sample_change.name).exists()


def test_archive_nonexistent_change(temp_project: Path, monkeypatch):
    """归档不存在的 change 报告错误。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(name="nonexistent", yes=True, skip_specs=False, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_archive(args)


def test_archive_with_specs_merge(sample_change_with_specs: Path, monkeypatch):
    """归档时合并 specs 到主 specs/。"""
    monkeypatch.chdir(sample_change_with_specs.parent.parent)

    state_file = sample_change_with_specs / ".stdd.yaml"
    with open(state_file, "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)
    state["phases"]["verify"]["status"] = "completed"
    with open(state_file, "w", encoding="utf-8") as f:
        yaml.dump(state, f)

    args = argparse.Namespace(name=None, yes=True, skip_specs=False, dry_run=False, verbose=0)
    cmd_archive(args)

    main_specs = sample_change_with_specs.parent.parent / "specs"
    assert (main_specs / "test.md").exists()
