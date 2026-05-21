"""Tests for stdd experience CLI commands."""
import pytest
import argparse
import json
import yaml
from pathlib import Path


def _make_args(subcommand, **kwargs):
    """Helper to build argparse.Namespace for experience commands."""
    ns = argparse.Namespace(
        command="experience",
        subcommand=subcommand,
        dry_run=False,
        verbose=0,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_experiences_dir(project_root: Path) -> Path:
    """Create .stdd/experiences directory and config files in a temp project."""
    (project_root / ".stdd" / "experiences").mkdir(parents=True, exist_ok=True)
    (project_root / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)

    exp_config = project_root / ".stdd" / "config.d" / "experience.yaml"
    exp_config.write_text("""
experience:
  dir: .stdd/experiences
  auto_record:
    enabled: true
    min_confidence: 0.5
  auto_load:
    enabled: true
    max_experiences: 10
    match:
      by_language: true
      by_category: true
      by_tags: true
  lifecycle:
    verified_threshold: 3
    settled_threshold: 10
    retire_after_days: 730
  export:
    sanitize_paths: true
    sanitize_ips: true
    sanitize_domains: true
  index:
    auto_generate: true
""", encoding="utf-8")

    proj_config = project_root / ".stdd" / "config.d" / "project.yaml"
    proj_config.write_text("""
paths:
  archive_dir: archive
  changes_dir: changes
  experiences_dir: .stdd/experiences
  platforms_dir: .stdd/platforms
  skills_dir: .stdd/skills
  specs_dir: specs
  standards_dir: .stdd/standards
  templates_dir: .stdd/templates
project:
  language: python
  name: stdd
  python_version: '3.10'
  source_dir: app
stdd_version: '2.0'
""", encoding="utf-8")

    (project_root / "changes").mkdir(exist_ok=True)
    (project_root / "specs").mkdir(exist_ok=True)
    (project_root / "archive").mkdir(exist_ok=True)
    return project_root / ".stdd" / "experiences"


class TestExperienceAdd:
    """TC-EXP-001, TC-EXP-002, TC-EXP-003, TC-EXP-007"""

    def test_add_creates_file_and_updates_index(self, tmp_path, monkeypatch):
        """TC-EXP-001: Creating an experience entry writes file with correct frontmatter."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        args = _make_args("add",
                          category="cascading_errors",
                          pattern="async function bare except misses CancelledError",
                          language="python",
                          severity="high",
                          tags="async,error-handling",
                          root_cause="AI habitually uses bare except Exception",
                          detection_trigger="async timeout test unstable",
                          fix_template="Handle except asyncio.CancelledError separately",
                          body="",
                          source_change=None)
        cmd_experience(args)

        # Verify file was created
        exp_files = list(exp_dir.glob("EXP-*.md"))
        assert len(exp_files) == 1
        assert exp_files[0].name.startswith("EXP-2026-")

        # Verify frontmatter
        content = exp_files[0].read_text(encoding="utf-8")
        parts = content.split("---", 2)
        assert len(parts) >= 3
        fm = yaml.safe_load(parts[1])
        assert fm["category"] == "cascading_errors"
        assert fm["pattern"] == "async function bare except misses CancelledError"
        assert fm["language"] == "python"
        assert fm["severity"] == "high"
        assert fm["tags"] == ["async", "error-handling"]
        assert fm["occurrences"] == 1
        assert fm["lifecycle_state"] == "discovered"

        # Verify index was updated
        index_path = exp_dir / ".experience-index.yaml"
        assert index_path.exists()
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        assert index["total"] == 1
        assert exp_files[0].stem in index["by_category"]["cascading_errors"]
        assert exp_files[0].stem in index["by_language"]["python"]

    def test_add_auto_id_increment(self, tmp_path, monkeypatch):
        """TC-EXP-002: Adding multiple entries auto-increments IDs."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        for i in range(3):
            args = _make_args("add",
                              category="scope_creep",
                              pattern=f"test pattern {i + 1}",
                              language="python",
                              severity="medium",
                              tags="",
                              root_cause="",
                              detection_trigger="",
                              fix_template="",
                              body="",
                              source_change=None)
            cmd_experience(args)

        exp_files = sorted(exp_dir.glob("EXP-*.md"))
        assert len(exp_files) == 3
        # IDs should be sequential
        nums = [int(f.stem.split("-")[-1]) for f in exp_files]
        assert nums == [nums[0], nums[0] + 1, nums[0] + 2]

        # Index should reflect 3 entries
        index = yaml.safe_load((exp_dir / ".experience-index.yaml").read_text(encoding="utf-8"))
        assert index["total"] == 3
        assert index["last_id"] == nums[-1]

    def test_add_invalid_category_rejected(self, tmp_path, monkeypatch, capsys):
        """TC-EXP-007: Invalid categories are rejected with helpful message."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        args = _make_args("add",
                          category="invalid_category_name",
                          pattern="test",
                          language="python",
                          severity="medium",
                          tags="",
                          root_cause="",
                          detection_trigger="",
                          fix_template="",
                          body="",
                          source_change=None)
        with pytest.raises(SystemExit) as exc_info:
            cmd_experience(args)
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "无效的 category" in captured.out
        assert "cascading_errors" in captured.out


class TestExperienceList:
    """TC-EXP-005, TC-EXP-006"""

    def test_list_filter_by_language(self, tmp_path, monkeypatch):
        """TC-EXP-005: List filters correctly by language."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        # Add python experience
        cmd_experience(_make_args("add", category="cascading_errors", pattern="python err",
                                   language="python", severity="high", tags="", body="",
                                   root_cause="", detection_trigger="", fix_template="", source_change=None))
        # Add go experience
        cmd_experience(_make_args("add", category="contract_gap", pattern="go err",
                                   language="go", severity="high", tags="", body="",
                                   root_cause="", detection_trigger="", fix_template="", source_change=None))

        # List by python
        args = _make_args("list", category=None, language="python",
                          lifecycle=None, severity=None, format="json")
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert len(data) == 1
        assert data[0]["language"] == "python"

    def test_list_format_json(self, tmp_path, monkeypatch):
        """TC-EXP-006: JSON output is valid and complete."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="high", tags="test",
                                   body="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        import sys
        from io import StringIO
        args = _make_args("list", category=None, language=None,
                          lifecycle=None, severity=None, format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert isinstance(data, list)
        assert len(data) == 1
        assert "experience_id" in data[0]
        assert "category" in data[0]
        assert "pattern" in data[0]


class TestExperienceStats:
    """TC-EXP-008"""

    def test_stats_shows_distribution(self, tmp_path, monkeypatch, capsys):
        """TC-EXP-008: Stats shows correct distribution by category."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        # Add experiences in 2 categories
        cmd_experience(_make_args("add", category="cascading_errors", pattern="err1",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        cmd_experience(_make_args("add", category="cascading_errors", pattern="err2",
                                   language="python", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        cmd_experience(_make_args("add", category="scope_creep", pattern="err3",
                                   language="go", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        args = _make_args("stats", format="table")
        cmd_experience(args)
        captured = capsys.readouterr()
        assert "3" in captured.out
        assert "级联错误" in captured.out

    def test_stats_format_json(self, tmp_path, monkeypatch):
        """Stats JSON output is valid."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="err",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        import sys
        from io import StringIO
        args = _make_args("stats", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert isinstance(data, dict)
        assert "total" in data


class TestExperienceExport:
    """TC-EXP-009, TC-EXP-010"""

    def test_export_sanitizes_content(self, tmp_path, monkeypatch):
        """TC-EXP-009: Export sanitizes paths, IPs, and domains."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        # Add experience with sensitive content
        cmd_experience(_make_args("add",
                                   category="cascading_errors",
                                   pattern="Error in /home/user/project/app/main.py with IP 192.168.1.1 at api.internal.com",
                                   language="python",
                                   severity="high",
                                   body="Path: /var/log/app/error.log, connect to 10.0.0.1 at db.internal.com",
                                   tags="",
                                   root_cause="config at /etc/app/config.yaml",
                                   detection_trigger="",
                                   fix_template="edit /home/user/project/app/main.py",
                                   source_change=None))

        import sys
        from io import StringIO
        args = _make_args("export", format="json", output=None, no_sanitize=False)
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        fm = data[0]["frontmatter"]
        body = data[0]["body"]

        # Check sanitization in frontmatter text fields
        assert "/home/user/project/app/main.py" not in str(fm)
        assert "192.168.1.1" not in str(fm)
        assert "api.internal.com" not in str(fm)
        assert "<project>/<module>" in str(fm) or "<ip-address>" in str(fm) or "<domain>" in str(fm)

        # Check sanitization in body
        if body:
            assert "/var/log" not in body
            assert "10.0.0.1" not in body

    def test_export_no_sanitize_preserves_content(self, tmp_path, monkeypatch):
        """TC-EXP-010: --no-sanitize preserves original content."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add",
                                   category="scope_creep",
                                   pattern="Changed /home/user/app/main.py",
                                   language="python",
                                   severity="medium",
                                   body="",
                                   tags="",
                                   root_cause="",
                                   detection_trigger="",
                                   fix_template="",
                                   source_change=None))

        import sys
        from io import StringIO
        args = _make_args("export", format="json", output=None, no_sanitize=True)
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        fm = data[0]["frontmatter"]
        assert "/home/user/app/main.py" in fm["pattern"]

    def test_export_to_file(self, tmp_path, monkeypatch):
        """Export writes to output file when --output is specified."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        out_file = tmp_path / "exported.json"
        args = _make_args("export", format="json", output=str(out_file), no_sanitize=True)
        cmd_experience(args)

        assert out_file.exists()
        data = json.loads(out_file.read_text(encoding="utf-8"))
        assert len(data) == 1


class TestExperiencePull:
    """TC-EXP-011"""

    def test_pull_shows_placeholder(self, tmp_path, monkeypatch, capsys):
        """TC-EXP-011: Pull command shows V2.5 placeholder message."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        args = _make_args("pull", pack_name="python-pack", source=None)
        cmd_experience(args)

        captured = capsys.readouterr()
        assert "V2.5" in captured.out


class TestIndexRebuild:
    """TC-EXP-004"""

    def test_index_rebuilt_when_deleted(self, tmp_path, monkeypatch):
        """TC-EXP-004: Index is rebuilt from EXP files when index is deleted."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        # Add experiences
        cmd_experience(_make_args("add", category="cascading_errors", pattern="err1",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        cmd_experience(_make_args("add", category="scope_creep", pattern="err2",
                                   language="python", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        # Delete index
        index_path = exp_dir / ".experience-index.yaml"
        index_path.unlink()
        assert not index_path.exists()

        # List should rebuild index
        import sys
        from io import StringIO
        args = _make_args("list", category=None, language=None,
                          lifecycle=None, severity=None, format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        sys.stdout = old_stdout

        # Index should be rebuilt
        assert index_path.exists()
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        assert index["total"] == 2


class TestCategoryValidation:
    """Tests for category validation edge cases."""

    def test_all_valid_categories_accepted(self, tmp_path, monkeypatch):
        """All 11 valid categories should be accepted."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience, VALID_CATEGORIES

        for cat in VALID_CATEGORIES:
            args = _make_args("add", category=cat, pattern=f"test {cat}",
                               language="python", severity="medium", body="",
                               tags="", root_cause="", detection_trigger="", fix_template="", source_change=None)
            cmd_experience(args)

        assert len(list(exp_dir.glob("EXP-*.md"))) == 11
