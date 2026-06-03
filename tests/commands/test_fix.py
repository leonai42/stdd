"""TC-FIX-001~003: Plankton auto-fix tests (V2.8)."""

import pytest
from pathlib import Path


class TestFixLevel1:
    """TC-FIX-001"""

    def test_fix_level1_dry_run(self, tmp_path, monkeypatch, capsys):
        """L1 dry-run prints preview without modifying files."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.fix import cmd_fix
        import argparse
        args = argparse.Namespace(level=1, dry_run=True)

        cmd_fix(args)
        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out

    def test_fix_level1_no_changes(self, tmp_path, monkeypatch, capsys):
        """L1 on already clean code reports nothing to fix."""
        # Create a clean Python file
        (tmp_path / "test.py").write_text("def hello():\n    return 'world'\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.fix import cmd_fix
        import argparse
        args = argparse.Namespace(level=1, dry_run=False)

        cmd_fix(args)
        captured = capsys.readouterr()
        assert "Already formatted" in captured.out or "fix applied" in captured.out

    def test_fix_invalid_level(self, tmp_path, monkeypatch):
        """Invalid level exits with error."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.fix import cmd_fix
        import argparse
        args = argparse.Namespace(level=99, dry_run=False)

        with pytest.raises(SystemExit):
            cmd_fix(args)


class TestFixLevel2:
    """TC-FIX-002"""

    def test_fix_level2_dry_run(self, tmp_path, monkeypatch, capsys):
        """L2 dry-run doesn't modify files."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.fix import cmd_fix
        import argparse
        args = argparse.Namespace(level=2, dry_run=True)

        cmd_fix(args)
        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out

    def test_fix_level2_no_issues(self, tmp_path, monkeypatch, capsys):
        """L2 on clean code reports no issues."""
        (tmp_path / "clean.py").write_text(
            "def greet(name: str) -> str:\n    return f'Hello {name}'\n",
            encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.fix import cmd_fix
        import argparse
        args = argparse.Namespace(level=2, dry_run=False)

        cmd_fix(args)
        captured = capsys.readouterr()
        assert "No Level 2 issues" in captured.out


class TestFixLevel3:
    """TC-FIX-003"""

    def test_fix_level3_report_only(self, tmp_path, monkeypatch, capsys):
        """L3 generates report without modifying code."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.fix import cmd_fix
        import argparse
        args = argparse.Namespace(level=3, dry_run=False)

        cmd_fix(args)
        captured = capsys.readouterr()
        assert "Report-only" in captured.out
        assert "bandit" in captured.out


class TestFixDispatch:
    """Test dispatch routing."""

    def test_dispatch_routes_to_fix(self, tmp_path, monkeypatch, capsys):
        """_dispatch calls cmd_fix correctly."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.fix import _dispatch
        import argparse
        args = argparse.Namespace(level=1, dry_run=True)

        _dispatch(args)
        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
