"""Tests for stdd guard CLI — intelligent enforcement gate (V2.9.3)."""

import pytest
import yaml
from pathlib import Path

from stdd.cli.commands.guard import (
    _find_active_change,
    _find_open_batch,
    _classify_description,
    _SCOPE_MICRO,
    _SCOPE_SMALL,
    _SCOPE_MEDIUM,
    _SCOPE_LARGE,
)


class TestFindActiveChange:
    """Test _find_active_change with both 'phase' and 'current_phase' keys."""

    def test_finds_change_with_current_phase(self, tmp_path):
        """REQ: 应识别使用 current_phase 字段的 change（new.py 的标准格式）。"""
        changes_dir = tmp_path / "changes"
        change_dir = changes_dir / "2026-06-06-test-fix"
        change_dir.mkdir(parents=True)
        (change_dir / ".stdd.yaml").write_text(yaml.dump({
            "status": "active",
            "current_phase": "build",
        }), encoding="utf-8")

        found, phase = _find_active_change(tmp_path)
        assert found is not None
        assert found.name == "2026-06-06-test-fix"
        assert phase == "build"

    def test_finds_change_with_legacy_phase(self, tmp_path):
        """向后兼容：也识别使用 phase 字段的旧格式 change。"""
        changes_dir = tmp_path / "changes"
        change_dir = changes_dir / "2026-06-05-old-format"
        change_dir.mkdir(parents=True)
        (change_dir / ".stdd.yaml").write_text(yaml.dump({
            "status": "active",
            "phase": "verify",
        }), encoding="utf-8")

        found, phase = _find_active_change(tmp_path)
        assert found is not None
        assert phase == "verify"

    def test_skips_batch_directory(self, tmp_path):
        """REQ: _batch 目录不应被识别为 active change。"""
        changes_dir = tmp_path / "changes"
        batch_dir = changes_dir / "_batch" / "2026-06-06"
        batch_dir.mkdir(parents=True)
        (batch_dir / ".stdd.yaml").write_text(yaml.dump({
            "mode": "batch",
            "batch_id": "2026-06-06",
            "closed_at": None,
        }), encoding="utf-8")

        found, phase = _find_active_change(tmp_path)
        assert found is None

    def test_returns_none_when_no_changes(self, tmp_path):
        """无 changes 目录时返回 None。"""
        found, phase = _find_active_change(tmp_path)
        assert found is None

    def test_current_phase_has_priority_over_legacy_phase(self, tmp_path):
        """current_phase 优先于 phase。"""
        changes_dir = tmp_path / "changes"
        change_dir = changes_dir / "2026-06-06-both"
        change_dir.mkdir(parents=True)
        (change_dir / ".stdd.yaml").write_text(yaml.dump({
            "status": "active",
            "current_phase": "build",
            "phase": "understand",
        }), encoding="utf-8")

        _, phase = _find_active_change(tmp_path)
        assert phase == "build"  # current_phase wins


class TestFindOpenBatch:
    """Test _find_open_batch. Returns (batch_dir, batch_data) tuple."""

    def test_finds_open_batch(self, tmp_path):
        batches_dir = tmp_path / "changes" / "_batch" / "2026-06-06"
        batches_dir.mkdir(parents=True)
        (batches_dir / ".stdd.yaml").write_text(yaml.dump({
            "mode": "batch",
            "batch_id": "2026-06-06",
            "closed_at": None,
        }), encoding="utf-8")

        batch_dir, batch_data = _find_open_batch(tmp_path)
        assert batch_dir is not None
        assert batch_dir.name == "2026-06-06"

    def test_skips_closed_batch(self, tmp_path):
        batches_dir = tmp_path / "changes" / "_batch" / "2026-06-05"
        batches_dir.mkdir(parents=True)
        (batches_dir / ".stdd.yaml").write_text(yaml.dump({
            "mode": "batch",
            "batch_id": "2026-06-05",
            "closed_at": "2026-06-05T12:00:00",
        }), encoding="utf-8")

        batch_dir, batch_data = _find_open_batch(tmp_path)
        assert batch_dir is None

    def test_returns_none_when_no_batches(self, tmp_path):
        batch_dir, batch_data = _find_open_batch(tmp_path)
        assert batch_dir is None


class TestClassifyDescription:
    """Test _classify_description scope classifier."""

    def test_micro_fix(self):
        assert _classify_description("修复一个typo") == _SCOPE_MICRO
        assert _classify_description("fix a bug") == _SCOPE_MICRO
        assert _classify_description("改个变量名") == _SCOPE_MICRO

    def test_small_change(self):
        assert _classify_description("优化日志输出格式") == _SCOPE_SMALL
        assert _classify_description("调整UI界面显示") == _SCOPE_SMALL

    def test_medium_change(self):
        assert _classify_description("重构交易模块数据处理") == _SCOPE_MEDIUM

    def test_large_change(self):
        assert _classify_description("新增交易风控API接口模块") == _SCOPE_LARGE
        assert _classify_description("重写K线分析架构引擎") == _SCOPE_LARGE

    def test_english_keywords(self):
        # "rewrite"=10 + "architecture"=10 + "system"=10 = 30 → LARGE
        assert _classify_description("rewrite the system architecture") == _SCOPE_LARGE
        # "fix"=1 + "typo"=1 = 2 → MICRO
        assert _classify_description("fix typo in readme") == _SCOPE_MICRO
        # "improve"=2 + "UI"=2 = 4 → SMALL
        assert _classify_description("improve UI") == _SCOPE_SMALL
