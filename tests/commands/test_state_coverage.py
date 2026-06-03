"""TC-COV-B1: state.py coverage tests — state_freshness, resume, edge cases."""

import yaml
import pytest
from pathlib import Path


class TestStateFreshness:
    """B1: state_freshness field handling."""

    def test_resume_with_freshness_fresh(self, tmp_path, monkeypatch, capsys):
        """--resume shows FRESH when git HEAD matches."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        stdd_yaml = change_dir / ".stdd.yaml"
        stdd_yaml.write_text(yaml.dump({
            "change_name": "test",
            "active_phase": 4,
            "resume_context": "testing",
            "last_action": "test action",
            "last_modified": "2026-06-03T10:00:00",
            "state_freshness": {
                "verified_at": "2026-06-03T10:00:00",
                "git_head": "",
            }
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import cmd_state
        import argparse
        args = argparse.Namespace(name="test", resume=True, set=None)

        cmd_state(args)
        captured = capsys.readouterr()
        assert "STDD Resume Context" in captured.out
        assert "FRESH" in captured.out

    def test_resume_with_v25_format(self, tmp_path, monkeypatch, capsys):
        """V2.5 format .stdd.yaml (no state_freshness) still works."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        stdd_yaml = change_dir / ".stdd.yaml"
        # V2.5 format: no active_phase, no state_freshness
        stdd_yaml.write_text(yaml.dump({
            "change_name": "test",
            "resume_context": "Phase 4 BUILD",
            "active_slice": 2,
            "last_action": "test",
            "last_modified": "2026-06-03T10:00:00",
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import cmd_state
        import argparse
        args = argparse.Namespace(name="test", resume=True, set=None)

        cmd_state(args)  # Should not crash
        captured = capsys.readouterr()
        assert "Phase: ?" in captured.out  # Missing active_phase defaults to ?

    def test_set_new_field(self, tmp_path, monkeypatch):
        """--set active_phase works."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        stdd_yaml = change_dir / ".stdd.yaml"
        stdd_yaml.write_text(yaml.dump({
            "resume_context": "old", "last_modified": "2026-01-01T00:00:00"
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import cmd_state
        import argparse
        args = argparse.Namespace(name="test", resume=False,
                                   set="active_phase=3")

        cmd_state(args)
        data = yaml.safe_load(stdd_yaml.read_text(encoding="utf-8"))
        assert data["active_phase"] in (3, "3")  # YAML may parse as int or str

    def test_set_unknown_field(self, tmp_path, monkeypatch):
        """--set with invalid field exits."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        (change_dir / ".stdd.yaml").write_text("resume_context: test\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import cmd_state
        import argparse
        args = argparse.Namespace(name="test", resume=False,
                                   set="invalid_field=value")

        with pytest.raises(SystemExit):
            cmd_state(args)


class TestStateDefault:
    """B1: Default display path."""

    def test_default_display(self, tmp_path, monkeypatch, capsys):
        """Default state display shows active_phase and resume_context."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        stdd_yaml = change_dir / ".stdd.yaml"
        stdd_yaml.write_text(yaml.dump({
            "active_phase": 5,
            "resume_context": "testing defaults",
            "active_slice": 3,
            "last_action": "verify done",
            "last_modified": "2026-06-03T10:00:00",
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import cmd_state
        import argparse
        args = argparse.Namespace(name="test", resume=False, set=None)

        cmd_state(args)
        captured = capsys.readouterr()
        assert "active_slice: 3" in captured.out
        assert "resume_context: testing defaults" in captured.out
