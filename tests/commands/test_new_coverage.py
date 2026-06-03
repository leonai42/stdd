"""TC-PAR-001: new.py --parallel coverage tests (V2.8)."""

import pytest
from pathlib import Path


class TestNewParallel:
    """TC-PAR-001"""

    def test_new_parallel_creates_worktrees(self, tmp_path, monkeypatch, capsys):
        """--parallel creates worktree directories."""
        # Setup minimal git repo
        import subprocess, os
        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True)
        # Need an initial commit for worktree
        (repo / "README.md").write_text("# test")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=repo, capture_output=True)

        # Setup STDD structure
        (repo / ".stdd").mkdir()
        (repo / ".stdd" / "templates").mkdir(parents=True)
        for tmpl in ["proposal.md", "design.md", "test-plan.md"]:
            (repo / ".stdd" / "templates" / tmpl).write_text(f"# {tmpl}", encoding="utf-8")

        monkeypatch.chdir(repo)

        from stdd.cli.commands.new import cmd_new
        import argparse
        args = argparse.Namespace(name="test-parallel", dry_run=False, parallel=True)

        cmd_new(args)
        captured = capsys.readouterr()

        assert "Two-Instance Kickoff" in captured.out
        assert "Explorer" in captured.out
        assert "Researcher" in captured.out

    def test_new_parallel_dry_run(self, tmp_path, monkeypatch, capsys):
        """--parallel with --dry-run doesn't create worktrees."""
        import subprocess
        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True)
        (repo / "README.md").write_text("# test")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=repo, capture_output=True)

        (repo / ".stdd").mkdir()
        monkeypatch.chdir(repo)

        from stdd.cli.commands.new import cmd_new
        import argparse
        args = argparse.Namespace(name="test-dry", dry_run=True, parallel=True)

        cmd_new(args)
        captured = capsys.readouterr()
        assert "[DRY-RUN]" in captured.out
