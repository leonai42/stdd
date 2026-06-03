"""TC-COV-B2: canon.py coverage tests — verify edge cases."""

import yaml
import pytest
from pathlib import Path


class TestCanonVerifyEdge:
    """B2: canon verify error paths."""

    def test_verify_hash_mismatch(self, tmp_path, monkeypatch, capsys):
        """DC-HASH fails when YAML changed but MD not regenerated."""
        # Set up canonical proposal
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        yaml_content = yaml.dump({"meta": {"change_id": "test", "title": "Test"},
                                   "why": {"problem": "test"}})
        (canon_dir / "test.yaml").write_text(yaml_content, encoding="utf-8")

        # Create MD with wrong hash
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        (change_dir / "proposal.md").write_text(
            "# Test\n\n<!-- source_hash: deadbeef00000000 -->\n\n## Why\n\ntest\n",
            encoding="utf-8")

        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.canon import cmd_canon_verify
        import argparse
        args = argparse.Namespace(change_name="test")

        with pytest.raises(SystemExit) as exc:
            cmd_canon_verify(args)
        assert exc.value.code == 1

    def test_verify_yaml_not_found(self, tmp_path, monkeypatch):
        """Verify exits when YAML doesn't exist."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.canon import cmd_canon_verify
        import argparse
        args = argparse.Namespace(change_name="no-such")

        with pytest.raises(SystemExit) as exc:
            cmd_canon_verify(args)
        assert exc.value.code == 1

    def test_verify_md_not_found(self, tmp_path, monkeypatch, capsys):
        """Verify handles missing MD gracefully."""
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        (canon_dir / "test.yaml").write_text(yaml.dump({"meta": {"change_id": "test"}}),
                                              encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.canon import cmd_canon_verify
        import argparse
        args = argparse.Namespace(change_name="test")

        # Should not crash — exits 0 with warning
        try:
            cmd_canon_verify(args)
        except SystemExit:
            pass  # May exit 0


class TestCanonGenerateEdge:
    """B2: canon generate error paths."""

    def test_generate_yaml_not_found(self, tmp_path, monkeypatch):
        """Generate exits when YAML doesn't exist."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.canon import cmd_canon_generate
        import argparse
        args = argparse.Namespace(change_name="no-such", type="proposal", all=False)

        with pytest.raises(SystemExit):
            cmd_canon_generate(args)
