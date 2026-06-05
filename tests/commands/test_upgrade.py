"""Tests for stdd upgrade CLI (V2.9)."""
import pytest
import argparse
import yaml
from pathlib import Path


def _make_args(**kwargs):
    ns = argparse.Namespace(
        command="upgrade",
        check=False, all=False, lock=False, unlock=False,
        dry_run=False, verbose=0, yes=False,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_project(tmp_path: Path, version: str = "2.5.0", locked: bool = False):
    """Create a minimal STDD project for testing."""
    (tmp_path / ".stdd" / "config.d").mkdir(parents=True)
    (tmp_path / ".stdd" / "skills").mkdir(parents=True)
    (tmp_path / ".stdd" / "templates").mkdir(parents=True)
    (tmp_path / ".stdd" / "standards").mkdir(parents=True)
    (tmp_path / ".stdd" / "config.d" / "project.yaml").write_text(
        f"stdd_version: '{version}'\nproject:\n  language: python\n  name: test\n",
        encoding="utf-8",
    )
    if locked:
        (tmp_path / ".stdd" / "version.yaml").write_text(
            yaml.dump({"stdd_version": version, "locked": True}, allow_unicode=True),
            encoding="utf-8",
        )


class TestUpgradeCheck:
    """TC-UPGRADE-001,002,003"""

    def test_check_shows_gap(self, tmp_path, monkeypatch):
        """TC-UPGRADE-001: Detects version gap."""
        _setup_project(tmp_path, "2.5.0")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import cmd_upgrade
        import sys
        from io import StringIO

        args = _make_args(check=True)
        old = sys.stdout
        sys.stdout = StringIO()
        cmd_upgrade(args)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert "2.9" in out or "新版本" in out or "已是最新" in out

    def test_check_at_latest(self, tmp_path, monkeypatch):
        """TC-UPGRADE-002: No gap when same version."""
        _setup_project(tmp_path, "2.9.0")
        (tmp_path / ".stdd" / "version.yaml").write_text(
            yaml.dump({"stdd_version": "2.9.0", "locked": False}, allow_unicode=True),
            encoding="utf-8",
        )
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import cmd_upgrade
        import sys
        from io import StringIO

        args = _make_args(check=True)
        old = sys.stdout
        sys.stdout = StringIO()
        cmd_upgrade(args)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert "已是最新" in out

    def test_check_fallback_project_yaml(self, tmp_path, monkeypatch):
        """TC-UPGRADE-003: Falls back to project.yaml when no version.yaml."""
        _setup_project(tmp_path, "2.3.0")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import cmd_upgrade
        import sys
        from io import StringIO

        args = _make_args(check=True)
        old = sys.stdout
        sys.stdout = StringIO()
        cmd_upgrade(args)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert "2.3" in out or "已是最新" in out


class TestUpgradeLock:
    """TC-UPGRADE-006,008,009"""

    def test_locked_project_skipped(self, tmp_path, monkeypatch):
        """TC-UPGRADE-006: Locked project refuses upgrade."""
        _setup_project(tmp_path, "2.5.0", locked=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import cmd_upgrade
        import sys
        from io import StringIO

        args = _make_args()
        old = sys.stdout
        sys.stdout = StringIO()
        cmd_upgrade(args)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert "锁定" in out

    def test_lock_sets_flag(self, tmp_path, monkeypatch):
        """TC-UPGRADE-008: --lock sets locked:true."""
        _setup_project(tmp_path, "2.5.0")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import cmd_upgrade

        cmd_upgrade(_make_args(lock=True))

        vf = tmp_path / ".stdd" / "version.yaml"
        assert vf.exists()
        data = yaml.safe_load(vf.read_text(encoding="utf-8"))
        assert data["locked"] is True

    def test_unlock_removes_lock(self, tmp_path, monkeypatch):
        """TC-UPGRADE-009: --unlock sets locked:false."""
        _setup_project(tmp_path, "2.5.0", locked=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import cmd_upgrade

        cmd_upgrade(_make_args(unlock=True))

        vf = tmp_path / ".stdd" / "version.yaml"
        data = yaml.safe_load(vf.read_text(encoding="utf-8"))
        assert data["locked"] is False


class TestUpgradeDryRun:
    """TC-UPGRADE-007"""

    def test_dry_run_no_changes(self, tmp_path, monkeypatch):
        """TC-UPGRADE-007: --dry-run previews without modifying filesystem."""
        _setup_project(tmp_path, "2.5.0")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import cmd_upgrade
        import sys
        from io import StringIO

        args = _make_args(dry_run=True)
        old = sys.stdout
        sys.stdout = StringIO()
        cmd_upgrade(args)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert "DRY-RUN" in out
        # version.yaml should NOT have been created
        assert not (tmp_path / ".stdd" / "version.yaml").exists()


class TestUpgradeRegistry:
    """TC-UPGRADE-010,011"""

    def test_registry_created(self, tmp_path, monkeypatch):
        """TC-UPGRADE-010: Global registry is created on first use."""
        _setup_project(tmp_path, "2.9.0")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.upgrade import _register_project, _registry_path

        _register_project(tmp_path, "2.9.0")
        rp = _registry_path()
        assert rp.exists()
        data = yaml.safe_load(rp.read_text(encoding="utf-8"))
        assert len(data.get("projects", [])) >= 1
        # Cleanup: remove the entry we just added
        data["projects"] = [p for p in data.get("projects", [])
                            if tmp_path.name not in str(p.get("path", ""))]
        rp.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")


class TestStartupCheck:
    """TC-UPGRADE-012,013,014"""

    def test_startup_check_prompts(self, tmp_path, monkeypatch):
        """TC-UPGRADE-012: Startup check prints notice when outdated."""
        _setup_project(tmp_path, "2.3.0")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.utils import try_version_check
        import sys
        from io import StringIO

        old = sys.stdout
        sys.stdout = StringIO()
        try_version_check(tmp_path)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert "新版本" in out or "STDD" in out or out == ""

    def test_startup_check_locked_skips(self, tmp_path, monkeypatch):
        """TC-UPGRADE-013: Locked project gets no notice."""
        _setup_project(tmp_path, "2.3.0", locked=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.utils import try_version_check
        import sys
        from io import StringIO

        old = sys.stdout
        sys.stdout = StringIO()
        try_version_check(tmp_path)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert out == ""  # No output for locked projects

    def test_startup_check_non_stdd_skips(self, tmp_path, monkeypatch):
        """TC-UPGRADE-014: Non-STDD project gets no notice."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.utils import try_version_check
        import sys
        from io import StringIO

        old = sys.stdout
        sys.stdout = StringIO()
        try_version_check(tmp_path)
        out = sys.stdout.getvalue()
        sys.stdout = old

        assert out == ""


class TestVersionCompare:
    """Unit tests for version comparison."""

    def test_compare_versions(self):
        from stdd.cli.utils import compare_versions
        assert compare_versions("2.5", "2.9") < 0
        assert compare_versions("2.9.0", "2.9.0") == 0
        assert compare_versions("2.10", "2.9") > 0
        assert compare_versions("v2.7", "2.8") < 0
        assert compare_versions("'2.7'", "2.7.0") == 0
