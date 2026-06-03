"""TC-CSUM-001~003: Code structure summary tests (V2.7)."""

import pytest
from pathlib import Path


class TestStructureCLI:
    """TC-CSUM-001~003 — structure CLI smoke tests."""

    def test_dispatch_delta(self, tmp_path, monkeypatch, capsys):
        """structure delta command is wired and doesn't crash."""
        change_dir = tmp_path / "changes" / "test-change"
        change_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="delta", target="test-change")

        _dispatch(args)
        captured = capsys.readouterr()
        assert "TODO" in captured.out

    def test_dispatch_merge(self, tmp_path, monkeypatch, capsys):
        """structure merge command is wired and doesn't crash."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="merge", target="test-change")

        _dispatch(args)
        captured = capsys.readouterr()
        assert "TODO" in captured.out

    def test_dispatch_rebuild(self, tmp_path, monkeypatch, capsys):
        """structure rebuild command is wired and doesn't crash."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="rebuild", target=None)

        _dispatch(args)
        captured = capsys.readouterr()
        assert "TODO" in captured.out

    def test_dispatch_show(self, tmp_path, monkeypatch, capsys):
        """structure show command is wired and doesn't crash."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="show", target="middleware")

        _dispatch(args)
        captured = capsys.readouterr()
        assert "TODO" in captured.out

    def test_dispatch_graph(self, tmp_path, monkeypatch, capsys):
        """structure graph command is wired and doesn't crash."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="graph", target=None)

        _dispatch(args)
        captured = capsys.readouterr()
        assert "TODO" in captured.out

    def test_dispatch_unknown_action(self, tmp_path, monkeypatch):
        """Dispatch exits on unknown action."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="unknown", target=None)

        with pytest.raises(SystemExit):
            _dispatch(args)
