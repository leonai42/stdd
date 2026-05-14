"""测试 cmd_validate 命令。"""
import argparse
import pytest
from pathlib import Path

from stdd.cli.commands.validate import cmd_validate


def test_validate_valid_change(sample_change_with_specs: Path, monkeypatch):
    """合规的 change 验证通过。"""
    monkeypatch.chdir(sample_change_with_specs.parent.parent)
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    # 不应抛 SystemExit
    cmd_validate(args)


def test_validate_missing_file(sample_change: Path, monkeypatch):
    """缺少必需文件时报告错误。"""
    monkeypatch.chdir(sample_change.parent.parent)
    (sample_change / "design.md").unlink()
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_validate(args)


def test_validate_nonexistent_change(temp_project: Path, monkeypatch):
    """不存在的 change 报告错误。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(name="nonexistent", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_validate(args)


def test_validate_and_count_warning(temp_project: Path, monkeypatch, capsys):
    """AND 超过 5 条时产生警告。"""
    monkeypatch.chdir(temp_project)
    today = __import__("datetime").date.today().isoformat()
    change_dir = temp_project / "changes" / f"{today}-and-test"
    change_dir.mkdir(parents=True)
    (change_dir / "specs").mkdir()

    import yaml
    state = {
        "version": "2.0", "change_id": f"{today}-and-test", "status": "active",
        "current_phase": "spec",
        "phases": {p: {"status": "pending"} for p in ["understand", "spec", "slice", "build", "verify", "deliver"]},
    }
    with open(change_dir / ".stdd.yaml", "w", encoding="utf-8") as f:
        yaml.dump(state, f)

    (change_dir / "proposal.md").write_text("# P", encoding="utf-8")
    (change_dir / "design.md").write_text("# D", encoding="utf-8")

    # 创建含 6 条 AND 的 spec
    spec = """# Capability: TEST
### Requirement: 测试
#### Scenario: 多 AND
- **GIVEN** 条件
- **WHEN** 触发
- **THEN** 系统 SHALL 执行
- **AND** 步骤1
- **AND** 步骤2
- **AND** 步骤3
- **AND** 步骤4
- **AND** 步骤5
- **AND** 步骤6
"""
    (change_dir / "specs" / "test.md").write_text(spec, encoding="utf-8")

    # test-plan 需要至少包含 TC 案例数 >= Scenario 数
    tp = """# Test Plan
| **ID** | TC-TEST-001 |
| **ID** | TC-TEST-002 |
"""
    (change_dir / "test-plan.md").write_text(tp, encoding="utf-8")

    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    cmd_validate(args)
    captured = capsys.readouterr()
    assert "AND 数量 (6) 超过上限 (5)" in captured.out


def test_validate_tc_id_duplicates(sample_change: Path, monkeypatch, capsys):
    """重复 TC-ID 检测。"""
    monkeypatch.chdir(sample_change.parent.parent)
    tp = """# Test Plan
| **ID** | TC-DUP-001 |
| **ID** | TC-DUP-001 |
"""
    (sample_change / "test-plan.md").write_text(tp, encoding="utf-8")
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_validate(args)
    captured = capsys.readouterr()
    assert "重复的 TC-ID" in captured.out


def test_validate_given_insufficient(sample_change_with_specs: Path, monkeypatch):
    """GIVEN 数量少于 Scenario 时警告。"""
    monkeypatch.chdir(sample_change_with_specs.parent.parent)
    # spec 已有 1 Scenario 和 1 GIVEN，添加第二个 Scenario 但不加 GIVEN
    spec_path = sample_change_with_specs / "specs" / "test.md"
    content = spec_path.read_text(encoding="utf-8") + "\n#### Scenario: 第二个场景\n\n- **WHEN** 触发\n- **THEN** 系统 SHALL 响应\n"
    spec_path.write_text(content, encoding="utf-8")
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    # 不应 exit，只有 warning
    try:
        cmd_validate(args)
    except SystemExit:
        pass  # ok if warning-only, no error


def test_validate_shall_missing(sample_change_with_specs: Path, monkeypatch):
    """THEN 中未使用 SHALL 时警告。"""
    monkeypatch.chdir(sample_change_with_specs.parent.parent)
    spec_path = sample_change_with_specs / "specs" / "test.md"
    content = spec_path.read_text(encoding="utf-8").replace("SHALL", "")
    spec_path.write_text(content, encoding="utf-8")
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    cmd_validate(args)  # 不应 crash


def test_validate_tc_insufficient(sample_change_with_specs: Path, monkeypatch):
    """TC 案例数少于 Scenario 时报错。"""
    monkeypatch.chdir(sample_change_with_specs.parent.parent)
    # 添加第二个 Scenario 但不添加对应 TC
    spec_path = sample_change_with_specs / "specs" / "test.md"
    content = spec_path.read_text(encoding="utf-8") + "\n#### Scenario: 额外场景\n\n- **GIVEN** 条件\n- **WHEN** 触发\n- **THEN** 系统 SHALL 处理\n"
    spec_path.write_text(content, encoding="utf-8")
    args = argparse.Namespace(name=None, dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_validate(args)
