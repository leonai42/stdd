"""Tests for V2.9 experience commands: extract, review, share, search."""
import pytest
import argparse
import json
import yaml
from pathlib import Path


class TestExperienceExtract:
    """TC-EXT: stdd experience extract."""

    def test_extract_no_changes_dir(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="extract", dry_run=False, verbose=0)
        cmd_experience(args)

    def test_extract_no_test_report(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        (temp_project / "changes" / "2026-06-01-test").mkdir(parents=True)
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="extract", dry_run=False, verbose=0)
        cmd_experience(args)

    def test_extract_with_test_report(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        change_dir = temp_project / "changes" / "2026-06-12-test-extract"
        change_dir.mkdir(parents=True)
        test_report = change_dir / "test-report.md"
        test_report.write_text("""# Test Report

## 12 Failure Mode Checks

| Category | Status | Description |
|----------|--------|-------------|
| cascading_errors | FAIL | Exception silently swallowed in process_data() |
| hallucination | PASS | No hallucination detected |
| scope_creep | WARNING | Minor scope expansion |

## Test Summary
| Test | Status |
|------|--------|
| test_process | PASS |
| test_api | FAIL (flaky) |
""", encoding="utf-8")
        (temp_project / ".stdd" / "experiences").mkdir(parents=True, exist_ok=True)
        config_dir = temp_project / ".stdd" / "config.d"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "experience.yaml").write_text("experience:\n  dir: .stdd/experiences\n", encoding="utf-8")
        (config_dir / "project.yaml").write_text("project:\n  name: test\n  language: python\n", encoding="utf-8")

        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="extract", dry_run=False, verbose=0)
        cmd_experience(args)
        exp_dir = temp_project / ".stdd" / "experiences"
        drafts = list(exp_dir.glob("EXP-*.md"))
        assert len(drafts) >= 1, f"Expected >=1 draft, got {len(drafts)}"
        assert "discovered" in drafts[0].read_text(encoding="utf-8")

    def test_extract_low_value_filtered(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        change_dir = temp_project / "changes" / "2026-06-12-test-filter"
        change_dir.mkdir(parents=True)
        (change_dir / "test-report.md").write_text("""# Report
| Category | Status | Description |
|----------|--------|-------------|
| context_loss | PASS | OK |
| tool_misuse | PASS | OK |
""", encoding="utf-8")
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True, exist_ok=True)
        config_dir = temp_project / ".stdd" / "config.d"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "experience.yaml").write_text("experience:\n  dir: .stdd/experiences\n", encoding="utf-8")
        (config_dir / "project.yaml").write_text("project:\n  name: test\n  language: python\n", encoding="utf-8")

        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="extract", dry_run=False, verbose=0)
        cmd_experience(args)
        drafts = list(exp_dir.glob("EXP-*.md"))
        assert len(drafts) == 0, f"Expected 0 drafts, got {len(drafts)}"


class TestExperienceReview:
    """TC-REV: stdd experience review."""

    def _make_draft(self, exp_dir, eid, lifecycle="discovered"):
        fm = {"experience_id": eid, "category": "cascading_errors",
              "pattern": "Test pattern", "root_cause": "Test root cause",
              "detection_trigger": "", "fix_template": "", "language": "python",
              "tags": ["test"], "occurrences": 2, "severity": "high",
              "confidence": 0.7, "source_change": "test", "source_file": "",
              "lifecycle_state": lifecycle, "first_seen": "2026-06-12",
              "last_seen": "2026-06-12", "provenance": "ci-detected",
              "provenance_weight": 0.85, "community_votes_useful": 0,
              "community_votes_unuseful": 0, "adoption_count": 0,
              "project_type": "python"}
        body = f"# Test\n\nBody for {eid}."
        fm_yaml = yaml.dump(fm, allow_unicode=True, default_flow_style=False)
        (exp_dir / f"{eid}.md").write_text(f"---\n{fm_yaml}---\n\n{body}", encoding="utf-8")

    def test_review_empty(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="review", dry_run=False, verbose=0)
        cmd_experience(args)

    def test_review_no_drafts(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        (temp_project / ".stdd" / "experiences").mkdir(parents=True)
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="review", dry_run=False, verbose=0)
        cmd_experience(args)

    def test_review_quit(self, temp_project, monkeypatch, capsys):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_draft(exp_dir, "EXP-2026-0101")
        self._make_draft(exp_dir, "EXP-2026-0102")
        self._make_draft(exp_dir, "EXP-2026-0103", lifecycle="deposited")

        import builtins
        oi = builtins.input
        builtins.input = lambda _="": "Q"
        try:
            from stdd.cli.commands.experience import cmd_experience
            args = argparse.Namespace(subcommand="review", dry_run=False, verbose=0)
            cmd_experience(args)
        finally:
            builtins.input = oi
        captured = capsys.readouterr()
        assert "EXP-2026-0101" in captured.out
        # Q on first draft exits immediately, so 0102 may not be shown
        assert "EXP-2026-0103" not in captured.out  # deposited, never shown
        assert "preserved" in captured.out.lower()

    def test_review_local_only(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_draft(exp_dir, "EXP-2026-0201")
        import builtins
        oi = builtins.input
        builtins.input = lambda _="": "L"
        try:
            from stdd.cli.commands.experience import cmd_experience
            args = argparse.Namespace(subcommand="review", dry_run=False, verbose=0)
            cmd_experience(args)
        finally:
            builtins.input = oi
        content = (exp_dir / "EXP-2026-0201.md").read_text(encoding="utf-8")
        assert "deposited" in content

    def test_review_delete(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_draft(exp_dir, "EXP-2026-0301")
        import builtins
        oi = builtins.input
        builtins.input = lambda _="": "D"
        try:
            from stdd.cli.commands.experience import cmd_experience
            args = argparse.Namespace(subcommand="review", dry_run=False, verbose=0)
            cmd_experience(args)
        finally:
            builtins.input = oi
        assert not (exp_dir / "EXP-2026-0301.md").exists()


class TestExperienceShare:
    """TC-SHA: stdd experience share."""

    def _make_exp(self, exp_dir, eid, include_path=False):
        root_cause = "Test root cause"
        if include_path:
            root_cause += " in /home/user/project/src/main.py"
        fm = {"experience_id": eid, "category": "cascading_errors",
              "pattern": "Test pattern for sharing", "root_cause": root_cause,
              "detection_trigger": "", "fix_template": "", "language": "python",
              "tags": ["test"], "occurrences": 3, "severity": "high",
              "confidence": 0.8, "source_change": "test", "source_file": "",
              "lifecycle_state": "deposited", "first_seen": "2026-06-12",
              "last_seen": "2026-06-12", "provenance": "ci-detected",
              "provenance_weight": 0.85, "community_votes_useful": 0,
              "community_votes_unuseful": 0, "adoption_count": 0,
              "project_type": "python"}
        body = f"# Share Test\n\nBody for {eid}."
        fm_yaml = yaml.dump(fm, allow_unicode=True, default_flow_style=False)
        (exp_dir / f"{eid}.md").write_text(f"---\n{fm_yaml}---\n\n{body}", encoding="utf-8")

    def test_share_not_found(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        (temp_project / ".stdd" / "experiences").mkdir(parents=True)
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="share", experience_id="EXP-NOTFOUND",
                                  dry_run=False, verbose=0)
        with pytest.raises(SystemExit):
            cmd_experience(args)

    def test_share_sanitize(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_exp(exp_dir, "EXP-2026-0500", include_path=True)
        import shutil, requests
        ow, op = shutil.which, requests.post
        shutil.which = lambda x: None
        captured = []

        class MR:
            def json(self):
                return {"success": True}

        def mp(url, **kw):
            captured.append(kw.get("json", {}).get("content", ""))
            return MR()

        requests.post = mp
        try:
            from stdd.cli.commands.experience import cmd_experience
            args = argparse.Namespace(subcommand="share", experience_id="EXP-2026-0500",
                                      dry_run=False, verbose=0)
            cmd_experience(args)
            if captured:
                assert "<project>/<module>" in captured[0]
        finally:
            shutil.which, requests.post = ow, op

    def test_share_api_success(self, temp_project, monkeypatch):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_exp(exp_dir, "EXP-2026-0600")
        import shutil, requests
        ow, op = shutil.which, requests.post
        shutil.which = lambda x: None

        class MR:
            def json(self):
                return {"success": True, "experience_id": "EXP-2026-0600"}

        requests.post = lambda url, **kw: MR()
        try:
            from stdd.cli.commands.experience import cmd_experience
            args = argparse.Namespace(subcommand="share", experience_id="EXP-2026-0600",
                                      dry_run=False, verbose=0)
            cmd_experience(args)
            content = (exp_dir / "EXP-2026-0600.md").read_text(encoding="utf-8")
            assert "shared" in content
        finally:
            shutil.which, requests.post = ow, op


class TestExperienceSearch:
    """TC-SEA: stdd experience search."""

    def _make_exp(self, exp_dir, eid, category="cascading_errors",
                  pattern="Database connection timeout", root_cause="Connection pool exhausted",
                  language="python"):
        fm = {"experience_id": eid, "category": category, "pattern": pattern,
              "root_cause": root_cause, "detection_trigger": "", "fix_template": "",
              "language": language, "tags": [category], "occurrences": 3,
              "severity": "high", "confidence": 0.8, "source_change": "test",
              "source_file": "", "lifecycle_state": "deposited",
              "first_seen": "2026-06-12", "last_seen": "2026-06-12",
              "provenance": "ci-detected", "provenance_weight": 0.85,
              "community_votes_useful": 0, "community_votes_unuseful": 0,
              "adoption_count": 0, "project_type": "python"}
        body = f"# {pattern}\n\nRoot cause: {root_cause}."
        fm_yaml = yaml.dump(fm, allow_unicode=True, default_flow_style=False)
        (exp_dir / f"{eid}.md").write_text(f"---\n{fm_yaml}---\n\n{body}", encoding="utf-8")

    def test_search_empty(self, temp_project, monkeypatch, capsys):
        monkeypatch.chdir(temp_project)
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="search", keyword="test",
                                  category=None, language=None, severity=None,
                                  format="table", dry_run=False, verbose=0)
        cmd_experience(args)
        assert "empty" in capsys.readouterr().out.lower()

    def test_search_keyword(self, temp_project, monkeypatch, capsys):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_exp(exp_dir, "EXP-2026-1001", pattern="Database connection timeout",
                      root_cause="Connection pool exhausted")
        self._make_exp(exp_dir, "EXP-2026-1002", pattern="API rate limiting bug",
                      root_cause="No rate limiter configured")
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="search", keyword="connection",
                                  category=None, language=None, severity=None,
                                  format="table", dry_run=False, verbose=0)
        cmd_experience(args)
        captured = capsys.readouterr().out
        assert "EXP-2026-1001" in captured
        assert "EXP-2026-1002" not in captured

    def test_search_with_filters(self, temp_project, monkeypatch, capsys):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_exp(exp_dir, "EXP-2026-2001", category="cascading_errors",
                      pattern="Timeout in db", language="python")
        self._make_exp(exp_dir, "EXP-2026-2002", category="hallucination",
                      pattern="Timeout hallucination", language="python")
        self._make_exp(exp_dir, "EXP-2026-2003", category="cascading_errors",
                      pattern="Timeout api", language="go")
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="search", keyword="timeout",
                                  category="cascading_errors", language="python",
                                  severity=None, format="table", dry_run=False, verbose=0)
        cmd_experience(args)
        captured = capsys.readouterr().out
        assert "EXP-2026-2001" in captured
        assert "EXP-2026-2002" not in captured
        assert "EXP-2026-2003" not in captured

    def test_search_no_results(self, temp_project, monkeypatch, capsys):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_exp(exp_dir, "EXP-2026-3001", pattern="Test pattern")
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="search", keyword="xyznotfound",
                                  category=None, language=None, severity=None,
                                  format="table", dry_run=False, verbose=0)
        cmd_experience(args)
        captured = capsys.readouterr().out
        assert "No results" in captured or "not found" in captured.lower() or "empty" in captured.lower()

    def test_search_json_format(self, temp_project, monkeypatch, capsys):
        monkeypatch.chdir(temp_project)
        exp_dir = temp_project / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        self._make_exp(exp_dir, "EXP-2026-4001", pattern="Test json output")
        from stdd.cli.commands.experience import cmd_experience
        args = argparse.Namespace(subcommand="search", keyword="json",
                                  category=None, language=None, severity=None,
                                  format="json", dry_run=False, verbose=0)
        cmd_experience(args)
        output = json.loads(capsys.readouterr().out.strip())
        assert isinstance(output, list)
        assert output[0]["experience_id"] == "EXP-2026-4001"
        assert "relevance_score" in output[0]
