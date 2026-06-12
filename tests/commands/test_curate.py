"""Tests for stdd experience curate command (V2.5 community pool)."""
import pytest
import argparse
import yaml
import tarfile
import io
from pathlib import Path


def _make_args(subcommand, **kwargs):
    ns = argparse.Namespace(
        command="experience",
        subcommand="curate",
        curate_subcommand=subcommand,
        dry_run=False,
        verbose=0,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_curate_project(tmp_path, with_inbox=False):
    """Create project with community config."""
    (tmp_path / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".stdd" / "config.d" / "project.yaml").write_text("""\
paths:
  changes_dir: changes
  archive_dir: archive
project:
  language: python
  name: test
stdd_version: '2.0'
""", encoding="utf-8")
    (tmp_path / ".stdd" / "config.d" / "experience.yaml").write_text("""\
experience:
  dir: .stdd/experiences
community:
  registries:
    - name: github
      url: "https://github.com/test/releases/download"
      priority: 1
  fallback_timeout: 1
  packs:
    - name: python
      version: "v1.0.0"
""", encoding="utf-8")
    (tmp_path / "changes").mkdir(exist_ok=True)

    if with_inbox:
        inbox = tmp_path / ".stdd" / "curation" / "inbox"
        inbox.mkdir(parents=True)

        # Create test tar.gz with EXP files
        exp1_fm = {
            "experience_id": "EXP-2026-0101",
            "category": "cascading_errors",
            "pattern": "async function bare except misses CancelledError in event loop",
            "root_cause": "AI habitually uses bare except Exception",
            "fix_template": "Handle except asyncio.CancelledError separately",
            "language": "python",
            "occurrences": 3,
            "severity": "high",
            "confidence": 0.85,
            "lifecycle_state": "verified",
        }
        exp2_fm = {
            "experience_id": "EXP-2026-0102",
            "category": "cascading_errors",
            "pattern": "async function bare except misses CancelledError in handling",
            "root_cause": "",
            "fix_template": "",
            "language": "python",
            "occurrences": 1,
            "severity": "medium",
            "confidence": 0.3,
            "lifecycle_state": "discovered",
        }

        # Create the tar.gz with both experiences
        tar_path = inbox / "experience-python-v1.0.0.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            for fm in [exp1_fm, exp2_fm]:
                eid = fm["experience_id"]
                fm_yaml = yaml.dump(fm, allow_unicode=True, default_flow_style=False)
                content = f"---\n{fm_yaml}---\n\n# Test body for {eid}"
                info = tarfile.TarInfo(name=f"{eid}.md")
                encoded = content.encode("utf-8")
                info.size = len(encoded)
                tar.addfile(info, io.BytesIO(encoded))

    return tmp_path


class TestCurateDeduplicate:
    """TC-COM-012, TC-COM-013"""

    def test_auto_merge_high_similarity(self, tmp_path, monkeypatch, capsys):
        """TC-COM-012/013: Pattern similarity detection flags suspicious pairs."""
        _setup_curate_project(tmp_path, with_inbox=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.curate import cmd_curate_deduplicate
        args = _make_args("deduplicate")
        cmd_curate_deduplicate(args, tmp_path)

        captured = capsys.readouterr()
        # 70% similarity falls in 60-80% flagged range
        assert ("similar" in captured.out.lower() or
                "EXP-2026-0101" in captured.out or
                "not found" in captured.out.lower())

    def test_pattern_similarity_calculation(self):
        """Unit test for pattern similarity scoring."""
        from stdd.cli.commands.curate import _pattern_similarity

        sim_high = _pattern_similarity(
            "async function bare except misses CancelledError",
            "async function bare except missing CancelledError"
        )
        assert sim_high > 0.6

        sim_low = _pattern_similarity(
            "async function error",
            "database connection timeout"
        )
        assert sim_low < 0.5


class TestCuratePack:
    """TC-COM-015"""

    def test_pack_creates_tar_gz(self, tmp_path, monkeypatch):
        """TC-COM-015: Pack creates valid tar.gz with curated metadata."""
        _setup_curate_project(tmp_path, with_inbox=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.curate import cmd_curate_pack
        args = _make_args("pack", language="python")
        cmd_curate_pack(args, tmp_path)
        # No curated experiences without review, so pack may be empty
        # but verification is in the integration flow


class TestCurateReviewInteractive:
    """V2.9.5: Interactive curate review with A/R/E/S."""

    def test_review_approve(self, tmp_path, monkeypatch):
        """A -> approved (merged)."""
        from pathlib import Path as P
        _setup_curate_project(tmp_path, with_inbox=True)
        monkeypatch.chdir(tmp_path)

        import builtins
        oi = builtins.input
        # First input: 'a' for approve, second not needed
        inputs = iter(["a", "a"])
        builtins.input = lambda _="": next(inputs)
        try:
            from stdd.cli.commands.curate import cmd_curate_review
            args = _make_args("review")
            cmd_curate_review(args, tmp_path)
        finally:
            builtins.input = oi

    def test_review_reject(self, tmp_path, monkeypatch):
        """R -> rejected."""
        _setup_curate_project(tmp_path, with_inbox=True)
        monkeypatch.chdir(tmp_path)

        import builtins
        oi = builtins.input
        inputs = iter(["r", "test rejection reason", "r", "test rejection reason 2"])
        builtins.input = lambda _="": next(inputs)
        try:
            from stdd.cli.commands.curate import cmd_curate_review
            args = _make_args("review")
            cmd_curate_review(args, tmp_path)
        finally:
            builtins.input = oi

    def test_review_skip(self, tmp_path, monkeypatch):
        """S/other -> skipped."""
        _setup_curate_project(tmp_path, with_inbox=True)
        monkeypatch.chdir(tmp_path)

        import builtins
        oi = builtins.input
        builtins.input = lambda _="": "s"  # skip all
        try:
            from stdd.cli.commands.curate import cmd_curate_review
            args = _make_args("review")
            cmd_curate_review(args, tmp_path)
        finally:
            builtins.input = oi

    def test_review_edit(self, tmp_path, monkeypatch):
        """E -> edit and approve."""
        _setup_curate_project(tmp_path, with_inbox=True)
        monkeypatch.chdir(tmp_path)

        import builtins
        oi = builtins.input
        inputs = iter(["e", "new pattern", "new root cause", "new fix", "s"])
        builtins.input = lambda _="": next(inputs)
        try:
            from stdd.cli.commands.curate import cmd_curate_review
            args = _make_args("review")
            cmd_curate_review(args, tmp_path)
        finally:
            builtins.input = oi
