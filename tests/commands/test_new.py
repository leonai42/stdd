"""测试 cmd_new 命令。"""
import argparse
import pytest
import sys
from pathlib import Path

from stdd.cli.commands.new import cmd_new


def test_new_valid_name(temp_project: Path, monkeypatch):
    """有效的 change 名称创建成功。"""
    monkeypatch.chdir(temp_project)
    # 需要 templates 目录
    (temp_project / ".stdd" / "templates").mkdir(parents=True, exist_ok=True)
    for t in ["proposal", "design", "test-plan"]:
        (temp_project / ".stdd" / "templates" / f"{t}.md").write_text(f"# {t}", encoding="utf-8")

    args = argparse.Namespace(name="my-feature", dry_run=False, verbose=0)
    cmd_new(args)

    changes = list((temp_project / "changes").iterdir())
    assert len(changes) == 1
    assert changes[0].name.endswith("my-feature")
    assert (changes[0] / ".stdd.yaml").exists()
    assert (changes[0] / "proposal.md").exists()


def test_new_invalid_name_special_chars(temp_project: Path, monkeypatch):
    """包含特殊字符的名称被拒绝。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(name="bad name!", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_new(args)


def test_new_duplicate_name(sample_change: Path, monkeypatch):
    """重复名称被拒绝。"""
    monkeypatch.chdir(sample_change.parent.parent)
    name_part = sample_change.name.split("-", 3)[-1]
    args = argparse.Namespace(name=name_part, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_new(args)


def test_new_version_field(sample_change: Path):
    """.stdd.yaml 包含 version: 2.0 字段。"""
    import yaml
    state_file = sample_change / ".stdd.yaml"
    with open(state_file, "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)
    assert state["version"] == "2.0"
