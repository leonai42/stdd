"""Tests for stdd ci CLI command."""
import pytest
import argparse


def _make_args(subcommand, **kwargs):
    ns = argparse.Namespace(
        command="ci",
        subcommand=subcommand,
        dry_run=False,
        verbose=0,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_project(tmp_path):
    """Create project skeleton with config files for CI testing."""
    (tmp_path / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".stdd" / "config.d" / "quality.yaml").write_text("""
quality:
  lint: ruff check app/ tests/
  type_check: mypy app/
  min_coverage: 80
ci:
  github_actions:
    python_version: '3.12'
    test_command: pytest tests/ --cov=stdd --cov-report=xml --cov-report=term
    lint_command: ruff check stdd/ tests/
    typecheck_command: mypy stdd/
  pre_commit:
    enabled: true
""", encoding="utf-8")

    (tmp_path / ".stdd" / "config.d" / "project.yaml").write_text("""
paths:
  changes_dir: changes
  archive_dir: archive
project:
  language: python
  name: test-project
  python_version: '3.11'
stdd_version: '2.0'
""", encoding="utf-8")

    (tmp_path / "changes").mkdir(exist_ok=True)
    (tmp_path / "archive").mkdir(exist_ok=True)
    return tmp_path


class TestCiInit:
    """TC-CI-001, TC-CI-002"""

    def test_init_creates_all_three_files(self, tmp_path, monkeypatch):
        """TC-CI-001: ci init creates workflow + pre-commit + PR template."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("init")
        cmd_ci(args)

        workflow = tmp_path / ".github" / "workflows" / "stdd-quality.yml"
        assert workflow.exists()
        content = workflow.read_text(encoding="utf-8")
        assert "STDD Quality Gate" in content
        assert "actions/checkout@v4" in content
        assert "python-version: '3.12'" in content

        precommit = tmp_path / ".pre-commit-config.yaml"
        assert precommit.exists()
        precommit_content = precommit.read_text(encoding="utf-8")
        assert "STDD Pre-commit Hook" in precommit_content
        assert "stdd-validate" in precommit_content

        pr_template = tmp_path / ".github" / "stdd-pr-comment.md"
        assert pr_template.exists()
        pr_content = pr_template.read_text(encoding="utf-8")
        assert "STDD Quality Gate Results" in pr_content

    def test_init_dry_run_does_not_create_files(self, tmp_path, monkeypatch):
        """TC-CI-002: ci init --dry-run prints preview but creates no files."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("init", dry_run=True)
        cmd_ci(args)

        assert not (tmp_path / ".github").exists()
        assert not (tmp_path / ".pre-commit-config.yaml").exists()

    def test_init_uses_fallback_python_version(self, tmp_path, monkeypatch):
        """When ci config has no python_version, fallback to project config."""
        _setup_project(tmp_path)
        # Override quality.yaml without python_version in ci section
        (tmp_path / ".stdd" / "config.d" / "quality.yaml").write_text("""
quality:
  lint: ruff check app/
ci:
  github_actions:
    test_command: pytest tests/
    lint_command: ruff check app/
    typecheck_command: mypy app/
""", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("init")
        cmd_ci(args)

        workflow = tmp_path / ".github" / "workflows" / "stdd-quality.yml"
        content = workflow.read_text(encoding="utf-8")
        assert "python-version: '3.11'" in content  # From project config


class TestCiGenerate:
    """TC-CI-003, TC-CI-004, TC-CI-005"""

    def test_generate_workflow_only(self, tmp_path, monkeypatch):
        """TC-CI-003: ci generate workflow creates only the workflow file."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("generate", target="workflow")
        cmd_ci(args)

        assert (tmp_path / ".github" / "workflows" / "stdd-quality.yml").exists()
        assert not (tmp_path / ".pre-commit-config.yaml").exists()
        assert not (tmp_path / ".github" / "stdd-pr-comment.md").exists()

    def test_generate_precommit_only(self, tmp_path, monkeypatch):
        """TC-CI-004: ci generate pre-commit creates only pre-commit hook."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("generate", target="pre-commit")
        cmd_ci(args)

        assert (tmp_path / ".pre-commit-config.yaml").exists()
        assert not (tmp_path / ".github" / "workflows" / "stdd-quality.yml").exists()

    def test_generate_pr_template_only(self, tmp_path, monkeypatch):
        """TC-CI-005: ci generate pr-template creates only PR comment template."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("generate", target="pr-template")
        cmd_ci(args)

        assert (tmp_path / ".github" / "stdd-pr-comment.md").exists()
        assert not (tmp_path / ".github" / "workflows" / "stdd-quality.yml").exists()

    def test_generate_dry_run_prints_preview(self, tmp_path, monkeypatch, capsys):
        """ci generate --dry-run prints preview without creating files."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("generate", target="workflow", dry_run=True)
        cmd_ci(args)

        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert "STDD Quality Gate" in captured.out
        assert not (tmp_path / ".github").exists()

    def test_generate_unknown_target(self, tmp_path, monkeypatch):
        """ci generate with unknown target prints error message."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("generate", target="unknown-target")
        cmd_ci(args)  # Should not crash; prints error message

    def test_generate_precommit_appends_existing(self, tmp_path, monkeypatch):
        """Pre-commit generation appends to existing config without STDD hooks."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        existing = """\
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
"""
        (tmp_path / ".pre-commit-config.yaml").write_text(existing, encoding="utf-8")

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("generate", target="pre-commit")
        cmd_ci(args)

        content = (tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        assert "black" in content
        assert "STDD Pre-commit Hook" in content


class TestCiCheckFailures:
    """TC-CI-006, TC-CI-007, TC-CI-008"""

    def _setup_valid_change(self, tmp_path):
        """Create a valid change with all required files."""
        _setup_project(tmp_path)
        change_dir = tmp_path / "changes" / "2026-01-01-test-change"
        change_dir.mkdir(parents=True)

        (change_dir / "proposal.md").write_text("# Test\n", encoding="utf-8")
        (change_dir / "design.md").write_text("# Design\n", encoding="utf-8")
        (change_dir / ".stdd.yaml").write_text("change_id: test\n", encoding="utf-8")

        # Valid test-plan with unique TC-IDs
        (change_dir / "test-plan.md").write_text("""\
# Test Plan
| TC-ID | Description |
|-------|-------------|
| TC-EXP-001 | Test 1 |
| TC-EXP-002 | Test 2 |
| TC-EXP-003 | Test 3 |
""", encoding="utf-8")

        # Valid spec with SHALL keywords and reasonable AND count
        spec_dir = change_dir / "specs" / "test-capability"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("""\
# Test Capability

#### Scenario: Happy Path
**GIVEN** valid input
**WHEN** processed
**THEN** the system SHALL return success

#### Scenario: Error Case
**GIVEN** invalid input
**WHEN** processed
**THEN** the system SHALL return error
**AND** log the error
**AND** increment error counter
""", encoding="utf-8")

        return change_dir

    def test_check_failures_passes_valid_change(self, tmp_path, monkeypatch):
        """TC-CI-006: check-failures passes for valid change structure."""
        self._setup_valid_change(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("check-failures", name="2026-01-01-test-change")
        cmd_ci(args)  # Should not raise SystemExit

    def test_check_failures_detects_missing_files(self, tmp_path, monkeypatch):
        """TC-CI-007: check-failures detects missing required files."""
        _setup_project(tmp_path)
        change_dir = tmp_path / "changes" / "2026-01-01-test-change"
        change_dir.mkdir(parents=True)
        # Missing: proposal.md, design.md, test-plan.md, .stdd.yaml
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("check-failures", name="2026-01-01-test-change")
        with pytest.raises(SystemExit) as exc_info:
            cmd_ci(args)
        assert exc_info.value.code == 1

    def test_check_failures_detects_duplicate_tc_ids(self, tmp_path, monkeypatch):
        """TC-CI-008: check-failures detects duplicate TC-IDs."""
        _setup_project(tmp_path)
        change_dir = tmp_path / "changes" / "2026-01-01-test-change"
        change_dir.mkdir(parents=True)

        (change_dir / "proposal.md").write_text("# Test", encoding="utf-8")
        (change_dir / "design.md").write_text("# Design", encoding="utf-8")
        (change_dir / ".stdd.yaml").write_text("change_id: test", encoding="utf-8")
        (change_dir / "test-plan.md").write_text("""\
TC-CASUAL-001 TC-CASUAL-001 TC-CASUAL-002 TC-CASUAL-001
""", encoding="utf-8")

        spec_dir = change_dir / "specs" / "test-cap"
        spec_dir.mkdir(parents=True)
        (spec_dir / "spec.md").write_text("""\
#### Scenario: Test
**GIVEN** x
**WHEN** y
**THEN** the system SHALL do z
""", encoding="utf-8")

        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("check-failures", name="2026-01-01-test-change")
        with pytest.raises(SystemExit) as exc_info:
            cmd_ci(args)
        assert exc_info.value.code == 1

    def test_check_failures_missing_change(self, tmp_path, monkeypatch):
        """check-failures with non-existent change exits with code 1."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("check-failures", name="nonexistent")
        with pytest.raises(SystemExit) as exc_info:
            cmd_ci(args)
        assert exc_info.value.code == 1


class TestCiEdgeCases:
    """Additional edge case tests."""

    def test_unknown_subcommand(self, tmp_path, monkeypatch):
        """Unknown subcommand exits with code 1."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = _make_args("unknown-subcommand")
        with pytest.raises(SystemExit) as exc_info:
            cmd_ci(args)
        assert exc_info.value.code == 1

    def test_init_with_gen_alias(self, tmp_path, monkeypatch):
        """Subcommand 'gen' is alias for 'generate'."""
        _setup_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import cmd_ci

        args = argparse.Namespace(
            command="ci",
            subcommand="gen",
            target="workflow",
            dry_run=False,
            verbose=0,
        )
        cmd_ci(args)
        assert (tmp_path / ".github" / "workflows" / "stdd-quality.yml").exists()
