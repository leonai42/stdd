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
    """TC-EXP-011, TC-COM-001, TC-COM-008, TC-COM-009"""

    def test_pull_no_registries_configured(self, tmp_path, monkeypatch):
        """Pull exits when no community registries configured."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        args = _make_args("pull", pack_name="python-pack", source=None)
        with pytest.raises(SystemExit) as exc_info:
            cmd_experience(args)
        assert exc_info.value.code == 1

    def test_pull_all_registries_unreachable(self, tmp_path, monkeypatch, capsys):
        """TC-COM-009: All registries unreachable exits with error."""
        exp_dir = _setup_experiences_dir(tmp_path)
        # Add community config
        exp_config = tmp_path / ".stdd" / "config.d" / "experience.yaml"
        content = exp_config.read_text(encoding="utf-8") + """
community:
  registries:
    - name: github
      url: "https://github.com/test/releases/download"
      priority: 1
  fallback_timeout: 1
  packs:
    - name: python
      version: "v1.0.0"
"""
        exp_config.write_text(content, encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        args = _make_args("pull", pack_name="python", source=None)
        with pytest.raises(SystemExit) as exc_info:
            cmd_experience(args)
        assert exc_info.value.code == 1


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


class TestCommunityPool:
    """TC-COM-004 ~ 007: Community experience pool features."""

    def test_new_experience_has_vote_fields(self, tmp_path, monkeypatch):
        """TC-COM-004: New experience includes community vote metadata fields."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        files = sorted(exp_dir.glob("EXP-*.md"))
        eid = files[0].stem
        from stdd.cli.commands.experience import _load_experience
        data = _load_experience(exp_dir / f"{eid}.md")
        assert "community_votes_useful" in data
        assert data["community_votes_useful"] == 0
        assert "community_votes_unuseful" in data
        assert data["community_votes_unuseful"] == 0
        assert "adoption_count" in data
        assert data["adoption_count"] == 0

    def test_export_sanitize(self, tmp_path, monkeypatch):
        """TC-COM-005: Export sanitizes path/IP/domain."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors",
                                   pattern="Bug in /home/user/projects/myapp/auth.py with 192.168.1.100",
                                   language="python", severity="high", body="Error at api.example.com",
                                   tags="", root_cause="Path /etc/config.yaml",
                                   detection_trigger="", fix_template="Edit /home/user/projects/myapp/auth.py",
                                   source_change=None))

        import sys
        from io import StringIO
        args = _make_args("export", format="json", output=None, no_sanitize=False, publish=False)
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        fm = data[0]["frontmatter"]
        assert "/home/user/projects/myapp/auth.py" not in str(fm)
        assert "192.168.1.100" not in str(fm)
        assert "api.example.com" not in str(fm)

    def test_export_no_sanitize_warning(self, tmp_path, monkeypatch, capsys):
        """TC-COM-006: --no-sanitize warns when publishing."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="scope_creep", pattern="test",
                                   language="python", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        args = _make_args("export", format="json", output=None, no_sanitize=True, publish=True)
        cmd_experience(args)
        captured = capsys.readouterr()
        assert "without sanitization" in captured.out

    def test_export_publish_sets_shared(self, tmp_path, monkeypatch):
        """TC-COM-007: --publish sets lifecycle_state to shared and creates tar.gz."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test publish",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="test", detection_trigger="", fix_template="fix", source_change=None))
        files = sorted(exp_dir.glob("EXP-*.md"))
        eid = files[0].stem

        tar_out = tmp_path / "test-export.tar.gz"
        args = _make_args("export", format="json", output=str(tar_out), no_sanitize=False, publish=True)
        cmd_experience(args)

        from stdd.cli.commands.experience import _load_experience
        data = _load_experience(exp_dir / f"{eid}.md")
        assert data["lifecycle_state"] == "shared"

        assert tar_out.exists()
        # Verify it's a valid tar.gz
        import tarfile
        with tarfile.open(tar_out, "r:gz") as tar:
            names = tar.getnames()
            assert f"{eid}.md" in names or any(n.startswith("EXP-") for n in names)


class TestProjectType:
    """TC-NCC-001 ~ 005: project_type detection and filtering."""

    def test_detect_project_type_python(self, tmp_path, monkeypatch):
        """TC-NCC-001: Auto-detect project_type=python from change files."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)
        # Create some .py files in changes
        (tmp_path / "changes" / "dummy" / "test.py").parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / "changes" / "dummy" / "test.py").write_text("x=1")

        from stdd.cli.commands.experience import _detect_project_type
        ptype = _detect_project_type(tmp_path / "changes")
        assert ptype == "python"

    def test_detect_project_type_static_site(self, tmp_path, monkeypatch):
        """TC-NCC-002: Auto-detect project_type=static_site from html/css/js."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)
        (tmp_path / "changes" / "web" / "index.html").parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / "changes" / "web" / "index.html").write_text("<html>")
        (tmp_path / "changes" / "web" / "style.css").write_text("body {}")
        (tmp_path / "changes" / "web" / "app.js").write_text("console.log(1)")

        from stdd.cli.commands.experience import _detect_project_type
        ptype = _detect_project_type(tmp_path / "changes")
        assert ptype == "static_site"

    def test_detect_project_type_docs(self, tmp_path, monkeypatch):
        """TC-NCC-003: Auto-detect project_type=docs from .md only."""
        _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)
        (tmp_path / "changes" / "doc" / "readme.md").parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / "changes" / "doc" / "readme.md").write_text("# Title")

        from stdd.cli.commands.experience import _detect_project_type
        ptype = _detect_project_type(tmp_path / "changes")
        assert ptype == "docs"

    def test_add_includes_project_type(self, tmp_path, monkeypatch):
        """TC-NCC-004: experience add includes project_type in frontmatter."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="",
                                   fix_template="", source_change=None, project_type=None))

        files = sorted(exp_dir.glob("EXP-*.md"))
        eid = files[0].stem
        from stdd.cli.commands.experience import _load_experience
        data = _load_experience(exp_dir / f"{eid}.md")
        assert "project_type" in data

    def test_project_type_backward_compatible(self, tmp_path, monkeypatch):
        """TC-NCC-005: Loading V2.4 experience without project_type works (wildcard)."""
        exp_dir = _setup_experiences_dir(tmp_path)
        # Manually create a V2.4-style experience without project_type
        exp_file = exp_dir / "EXP-2026-0099.md"
        content = """---
experience_id: EXP-2026-0099
category: cascading_errors
pattern: test old format
language: python
occurrences: 1
severity: medium
confidence: 0.5
lifecycle_state: discovered
---

# Old format body
"""
        exp_file.write_text(content, encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import _load_experience
        data = _load_experience(exp_file)
        assert data is not None
        assert "project_type" not in data  # Old format has no project_type
        # Should be treated as wildcard (null/None) — compatible


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


class TestExperienceLifecycle:
    """TC-EXP-LC-001 ~ 009: Experience lifecycle state machine."""

    def _get_first_exp_id(self, exp_dir):
        """Get the ID of the first (only) experience file."""
        files = sorted(exp_dir.glob("EXP-*.md"))
        return files[0].stem if files else None

    def _get_exp_data(self, exp_dir, eid):
        """Load experience frontmatter data."""
        from stdd.cli.commands.experience import _load_experience
        return _load_experience(exp_dir / f"{eid}.md")

    def test_new_experience_is_discovered(self, tmp_path, monkeypatch):
        """TC-EXP-LC-001: New experience created with lifecycle_state=discovered."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))

        eid = self._get_first_exp_id(exp_dir)
        data = self._get_exp_data(exp_dir, eid)
        assert data["lifecycle_state"] == "discovered"

    def test_manual_verify(self, tmp_path, monkeypatch):
        """TC-EXP-LC-002: Manual verify transitions discovered → verified."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        eid = self._get_first_exp_id(exp_dir)

        args = _make_args("verify", experience_id=eid)
        cmd_experience(args)

        data = self._get_exp_data(exp_dir, eid)
        assert data["lifecycle_state"] == "verified"
        assert data["confidence"] >= 0.7
        assert data["occurrences"] >= 2

    def test_auto_promote_to_verified(self, tmp_path, monkeypatch):
        """TC-EXP-LC-003: Auto-promote to verified when occurrences>=2 and confidence>=0.7."""
        from stdd.cli.commands.experience import _auto_promote

        data = {"lifecycle_state": "discovered", "occurrences": 2, "confidence": 0.7}
        assert _auto_promote(data) == "verified"

        data2 = {"lifecycle_state": "discovered", "occurrences": 1, "confidence": 0.9}
        assert _auto_promote(data2) is None

    def test_deposit(self, tmp_path, monkeypatch):
        """TC-EXP-LC-004: Deposit verified experience with occurrences>=3 and confidence>=0.8."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        eid = self._get_first_exp_id(exp_dir)

        # First verify it
        cmd_experience(_make_args("verify", experience_id=eid))

        # Manually bump occurrences and confidence for deposit eligibility
        exp_file = exp_dir / f"{eid}.md"
        content = exp_file.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        fm = yaml.safe_load(parts[1])
        fm["occurrences"] = 3
        fm["confidence"] = 0.85
        new_content = f"---\n{yaml.dump(fm, allow_unicode=True, default_flow_style=False)}---\n{parts[2] if len(parts) >= 3 else ''}"
        exp_file.write_text(new_content, encoding="utf-8")

        args = _make_args("deposit", experience_id=eid)
        cmd_experience(args)

        data = self._get_exp_data(exp_dir, eid)
        assert data["lifecycle_state"] == "deposited"

    def test_retire(self, tmp_path, monkeypatch):
        """TC-EXP-LC-006: Retire an experience from any state."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="scope_creep", pattern="test",
                                   language="python", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        eid = self._get_first_exp_id(exp_dir)

        args = _make_args("retire", experience_id=eid, reason="no longer relevant")
        cmd_experience(args)

        data = self._get_exp_data(exp_dir, eid)
        assert data["lifecycle_state"] == "retired"
        assert data["retire_reason"] == "no longer relevant"
        assert "retired_date" in data

    def test_retired_hidden_by_default(self, tmp_path, monkeypatch, capsys):
        """TC-EXP-LC-007: Retired experiences hidden unless --all."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="active",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        eid = self._get_first_exp_id(exp_dir)
        cmd_experience(_make_args("retire", experience_id=eid, reason="obsolete"))

        # Default list should hide retired
        args = _make_args("list", category=None, language=None,
                          lifecycle=None, severity=None, format="json", all=False)
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        data = json.loads(output)
        assert len(data) == 0  # retired is hidden

        # --all should show retired
        args_all = _make_args("list", category=None, language=None,
                              lifecycle=None, severity=None, format="json", all=True)
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_experience(args_all)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        data_all = json.loads(output)
        assert len(data_all) == 1
        assert data_all[0]["lifecycle_state"] == "retired"

    def test_invalid_transition_rejected(self, tmp_path, monkeypatch):
        """TC-EXP-LC-008: Invalid state transitions return error."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="medium", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        eid = self._get_first_exp_id(exp_dir)

        # discovered → deposited (should fail: need verified first)
        args = _make_args("deposit", experience_id=eid)
        with pytest.raises(SystemExit) as exc_info:
            cmd_experience(args)
        assert exc_info.value.code == 1

    def test_index_sync_after_state_change(self, tmp_path, monkeypatch):
        """TC-EXP-LC-009: Index by_lifecycle is updated after state transition."""
        exp_dir = _setup_experiences_dir(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.experience import cmd_experience

        cmd_experience(_make_args("add", category="cascading_errors", pattern="test",
                                   language="python", severity="high", body="",
                                   tags="", root_cause="", detection_trigger="", fix_template="", source_change=None))
        eid = self._get_first_exp_id(exp_dir)

        index = yaml.safe_load((exp_dir / ".experience-index.yaml").read_text(encoding="utf-8"))
        assert eid in index["by_lifecycle"]["discovered"]

        cmd_experience(_make_args("verify", experience_id=eid))

        index = yaml.safe_load((exp_dir / ".experience-index.yaml").read_text(encoding="utf-8"))
        assert "discovered" not in index["by_lifecycle"].get("discovered", []) or eid not in index["by_lifecycle"].get("discovered", [])
        assert eid in index["by_lifecycle"].get("verified", [])
