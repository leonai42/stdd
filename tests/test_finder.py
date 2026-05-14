"""测试 _find_change_dir / find_change_dir 函数。"""
import pytest
from pathlib import Path
from datetime import date

from stdd.cli.finder import find_change_dir


def test_exact_match(sample_change: Path):
    """精确匹配 change 目录名。"""
    result = find_change_dir(sample_change.name, sample_change.parent.parent)
    assert result is not None
    assert result.name == sample_change.name


def test_fuzzy_match(sample_change: Path):
    """模糊匹配（省略日期前缀）。"""
    # 提取名称中日期之后的部分
    name_part = sample_change.name.split("-", 3)[-1] if sample_change.name[0].isdigit() else sample_change.name
    result = find_change_dir(name_part, sample_change.parent.parent)
    assert result is not None
    assert result.name == sample_change.name


def test_no_match(temp_project: Path):
    """无匹配时返回 None。"""
    result = find_change_dir("nonexistent-feature", temp_project)
    assert result is None


def test_no_name_returns_latest(sample_change: Path):
    """不传名称返回最近修改的 change（唯一的那个）。"""
    result = find_change_dir(None, sample_change.parent.parent)
    assert result is not None
    assert result.name == sample_change.name


def test_empty_changes_dir(temp_project: Path):
    """changes/ 目录存在但为空时返回 None。"""
    result = find_change_dir(None, temp_project)
    assert result is None


def test_no_changes_dir(tmp_path: Path):
    """没有 changes/ 目录时返回 None。"""
    result = find_change_dir(None, tmp_path)
    assert result is None


def test_directory_without_state_file(temp_project: Path):
    """目录存在但无 .stdd.yaml 时不应匹配。"""
    d = temp_project / "changes" / "2026-01-01-no-state"
    d.mkdir(parents=True)
    result = find_change_dir("no-state", temp_project)
    assert result is None


def test_exact_match_no_state_file(temp_project: Path):
    """精确匹配但无 .stdd.yaml 返回 None。"""
    # 创建无状态文件的目录
    d = temp_project / "changes" / "2026-01-01-no-state"
    d.mkdir(parents=True)
    result = find_change_dir("2026-01-01-no-state", temp_project)
    assert result is None
