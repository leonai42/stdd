"""TC-CSUM-001~004: Code structure summary tests (V2.8)."""

import pytest
from pathlib import Path


class TestStructureDelta:
    """TC-CSUM-001"""

    def test_delta_creates_file(self, tmp_path, monkeypatch):
        """structure delta generates code-structure-delta.md."""
        change_dir = tmp_path / "changes" / "test-change"
        change_dir.mkdir(parents=True)
        (change_dir / "app.py").write_text("print('hello')", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="delta", target="test-change")

        _dispatch(args)

        delta_file = change_dir / "code-structure-delta.md"
        assert delta_file.exists()
        content = delta_file.read_text(encoding="utf-8")
        assert "test-change" in content
        assert "置信度: 0.70" in content

    def test_delta_nonexistent_change(self, tmp_path, monkeypatch):
        """delta for non-existent change exits with error."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="delta", target="no-such-change")

        with pytest.raises(SystemExit):
            _dispatch(args)


class TestStructureMerge:
    """TC-CSUM-002"""

    def test_merge_creates_index(self, tmp_path, monkeypatch):
        """merge creates .stdd/code-structure/index.md."""
        change_dir = tmp_path / "changes" / "test-change"
        change_dir.mkdir(parents=True)
        (change_dir / "app.py").write_text("print('hello')", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.structure import _dispatch
        import argparse

        # First generate delta
        _dispatch(argparse.Namespace(action="delta", target="test-change"))
        # Then merge
        _dispatch(argparse.Namespace(action="merge", target="test-change"))

        index_file = tmp_path / ".stdd" / "code-structure" / "index.md"
        assert index_file.exists()
        yaml_file = tmp_path / ".stdd" / "code-structure" / ".structure-index.yaml"
        assert yaml_file.exists()
        deltas_dir = tmp_path / ".stdd" / "code-structure" / "deltas"
        assert list(deltas_dir.glob("*.md"))


class TestStructureShow:
    """TC-CSUM-003"""

    def test_show_before_merge(self, tmp_path, monkeypatch, capsys):
        """show without index gives helpful message."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="show", target=None)

        _dispatch(args)
        captured = capsys.readouterr()
        assert "No structure index" in captured.out

    def test_show_after_merge(self, tmp_path, monkeypatch, capsys):
        """show after merge displays modules."""
        change_dir = tmp_path / "changes" / "test-change"
        change_dir.mkdir(parents=True)
        (change_dir / "app.py").write_text("print('hello')", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.structure import _dispatch
        import argparse
        _dispatch(argparse.Namespace(action="delta", target="test-change"))
        _dispatch(argparse.Namespace(action="merge", target="test-change"))

        _dispatch(argparse.Namespace(action="show", target=None))
        captured = capsys.readouterr()
        assert "Total modules" in captured.out


class TestStructureGraph:
    """TC-CSUM-004"""

    def test_graph_without_index(self, tmp_path, monkeypatch, capsys):
        """graph without index gives helpful message."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="graph", target=None)

        _dispatch(args)
        captured = capsys.readouterr()
        assert "No structure index" in captured.out

    def test_graph_with_index(self, tmp_path, monkeypatch, capsys):
        """graph after merge displays structure."""
        change_dir = tmp_path / "changes" / "test-change"
        change_dir.mkdir(parents=True)
        (change_dir / "app.py").write_text("print('hello')", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.structure import _dispatch
        import argparse
        _dispatch(argparse.Namespace(action="delta", target="test-change"))
        _dispatch(argparse.Namespace(action="merge", target="test-change"))

        _dispatch(argparse.Namespace(action="graph", target=None))
        captured = capsys.readouterr()
        assert "Code Structure Graph" in captured.out


class TestStructureRebuild:
    """Rebuild from deltas."""

    def test_rebuild_empty(self, tmp_path, monkeypatch, capsys):
        """rebuild with no deltas."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="rebuild", target=None)

        _dispatch(args)
        captured = capsys.readouterr()
        assert "No deltas" in captured.out


class TestStructureDispatch:
    """Dispatch routing."""

    def test_dispatch_unknown_action(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.structure import _dispatch
        import argparse
        args = argparse.Namespace(action="unknown", target=None)
        with pytest.raises(SystemExit):
            _dispatch(args)
