"""Tests for stdd batch CLI (V2.9)."""
import pytest
import argparse
import yaml
from pathlib import Path


def _make_args(action="status", description="", strategy="monthly", force=False):
    return argparse.Namespace(
        command="batch", action=action, description=description,
        strategy=strategy, force=force, dry_run=False, verbose=0,
    )


def _setup_batch_env(tmp_path: Path, strategy="monthly"):
    """Create minimal STDD project with lite.yaml config."""
    (tmp_path / ".stdd" / "config.d").mkdir(parents=True)
    (tmp_path / ".stdd" / "config.d" / "lite.yaml").write_text(
        yaml.dump({"batch": {"strategy": strategy, "max_items": 20, "auto_close": True}},
                  allow_unicode=True),
        encoding="utf-8",
    )
    (tmp_path / "changes" / "_batch").mkdir(parents=True)


class TestBatchCreate:
    """TC-BATCH-001,002"""

    def test_create_first_batch(self, tmp_path, monkeypatch):
        """TC-BATCH-001: First lightweight change creates a new batch directory."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import _create_batch
        batch_dir = _create_batch(tmp_path)

        assert batch_dir.exists()
        assert batch_dir.name.startswith("2026-")
        assert (batch_dir / "items").is_dir()
        assert (batch_dir / ".stdd.yaml").exists()

        data = yaml.safe_load((batch_dir / ".stdd.yaml").read_text(encoding="utf-8"))
        assert data["batch_type"] == "monthly"
        assert data["closed_at"] is None

    def test_create_second_batch_different_name(self, tmp_path, monkeypatch):
        """TC-BATCH-006: Closed batch + new change = different dir name."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import _create_batch, _close_batch

        b1 = _create_batch(tmp_path)
        _close_batch(b1)
        b2 = _create_batch(tmp_path)

        assert b1.name != b2.name


class TestBatchClose:
    """TC-BATCH-005"""

    def test_close_batch_generates_summary(self, tmp_path, monkeypatch):
        """TC-BATCH-005: Manual close generates archive-summary.md."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import _create_batch, _close_batch

        batch_dir = _create_batch(tmp_path)
        _close_batch(batch_dir)

        summary = batch_dir / "archive-summary.md"
        assert summary.exists()

        data = yaml.safe_load((batch_dir / ".stdd.yaml").read_text(encoding="utf-8"))
        assert data["closed_at"] is not None


class TestBatchStatus:
    """TC-BATCH-008"""

    def test_status_shows_open_batch(self, tmp_path, monkeypatch, capsys):
        """TC-BATCH-008: status shows current open batch info."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import _create_batch, cmd_batch

        _create_batch(tmp_path)
        cmd_batch(_make_args("status"))
        captured = capsys.readouterr()

        assert "批次" in captured.out or "batch" in captured.out.lower()


class TestBatchList:
    """TC-BATCH-009"""

    def test_list_shows_batches(self, tmp_path, monkeypatch, capsys):
        """TC-BATCH-009: list shows all batches."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import _create_batch, _close_batch, cmd_batch

        b1 = _create_batch(tmp_path)
        _close_batch(b1)
        _create_batch(tmp_path)

        cmd_batch(_make_args("list"))
        captured = capsys.readouterr()

        assert "进行中" in captured.out
        assert "已闭合" in captured.out


class TestBatchNoBatch:
    """Edge cases."""

    def test_status_no_batch(self, tmp_path, monkeypatch, capsys):
        """No batch exists yet."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import cmd_batch
        cmd_batch(_make_args("status"))
        captured = capsys.readouterr()

        assert "无" in captured.out or "打开" not in captured.out

    def test_close_no_batch(self, tmp_path, monkeypatch, capsys):
        """Close when no batch exists."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import cmd_batch
        cmd_batch(_make_args("close"))
        captured = capsys.readouterr()
        assert "无打开的批次" in captured.out

    def test_open_validates_micro_scope(self, tmp_path, monkeypatch, capsys):
        """Open batch with micro-fix description should succeed."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import cmd_batch
        cmd_batch(_make_args("open", "修复一个typo"))
        captured = capsys.readouterr()
        assert "批次已打开" in captured.out

    def test_open_rejects_large_scope(self, tmp_path, monkeypatch, capsys):
        """Open batch with large change description should be rejected."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import cmd_batch
        cmd_batch(_make_args("open", "重写系统架构API"))
        captured = capsys.readouterr()
        assert "batch 不适合大型变更" in captured.out

    def test_add_item_to_open_batch(self, tmp_path, monkeypatch, capsys):
        """Add item to open batch."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import cmd_batch
        cmd_batch(_make_args("open", "修bug"))
        cmd_batch(_make_args("add", "fix: typo"))
        captured = capsys.readouterr()
        assert "[1/5]" in captured.out

    def test_archive_moves_batch(self, tmp_path, monkeypatch):
        """Archive should move closed batch to archive/."""
        _setup_batch_env(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.batch import cmd_batch
        cmd_batch(_make_args("open", "测试归档"))
        cmd_batch(_make_args("close", force=True))
        cmd_batch(_make_args("archive"))

        # After archive, batch should be in archive/
        archive_dir = tmp_path / "archive"
        assert archive_dir.exists()
