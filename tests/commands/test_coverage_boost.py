"""V2.8 coverage boost tests: B3 index, B4 experience, B5 ci, B6 proposal, B8 agent, B9 trace."""

import yaml
import json
import pytest
from pathlib import Path


# ── B3: index.py 50%→75% ──

class TestIndexCoverage:
    def test_trace_file_not_found(self, tmp_path, monkeypatch, capsys):
        """Trace a file not in project-index."""
        index_data = {"project": {"name": "test"}, "module_index": {}}
        (tmp_path / "project-index.yaml").write_text(yaml.dump(index_data), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.index import cmd_index_trace
        import argparse
        args = argparse.Namespace(file="nonexistent.py")
        cmd_index_trace(args)
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_show_no_index(self, tmp_path, monkeypatch):
        """Show with no project-index exits."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.index import cmd_index_show
        import argparse
        args = argparse.Namespace(capability=None)
        with pytest.raises(SystemExit):
            cmd_index_show(args)

    def test_show_capability_not_found(self, tmp_path, monkeypatch, capsys):
        """Show capability that doesn't exist."""
        (tmp_path / "project-index.yaml").write_text(yaml.dump({
            "project": {"name": "test", "language": "python"},
            "capabilities": {}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.index import cmd_index_show
        import argparse
        args = argparse.Namespace(capability="no-such")
        cmd_index_show(args)
        captured = capsys.readouterr()
        assert "not found" in captured.out


# ── B4: experience.py 72%→80% ──

class TestExperienceCoverage:
    def test_list_filter_by_provenance(self, tmp_path, monkeypatch):
        """Filter experiences by provenance."""
        exp_dir = _setup_exp_dir(tmp_path)
        # Create experiences with different provenance
        for i, prov in enumerate(["ci-detected", "ai-inferred", "ci-detected"]):
            from stdd.cli.commands.experience import cmd_experience
            import argparse
            args = argparse.Namespace(
                subcommand="add", category="cascading_errors",
                pattern=f"test prov {i}", language="python",
                severity="medium", body="", tags="test", root_cause="",
                detection_trigger="", fix_template="", source_change=None,
                provenance=prov, project_type=None, format="table",
                all=False, lifecycle=None
            )
            cmd_experience(args)

        # Filter by provenance
        from stdd.cli.commands.experience import cmd_experience
        import argparse
        args = argparse.Namespace(
            subcommand="list", format="json", category=None,
            language=None, lifecycle=None, severity=None,
            provenance="ci-detected", all=False
        )
        import sys, io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert len(data) == 2
        assert all(e["provenance"] == "ci-detected" for e in data)

    def test_export_sanitize_patterns(self, tmp_path, monkeypatch):
        """Export sanitizes IP and paths."""
        exp_dir = _setup_exp_dir(tmp_path)
        from stdd.cli.commands.experience import cmd_experience
        import argparse
        # Create experience with sensitive data
        args = argparse.Namespace(
            subcommand="add", category="cascading_errors",
            pattern="test with 192.168.1.1 in /home/user/file.py",
            language="python", severity="high", body="Server at db.internal.com failed",
            tags="test", root_cause="", detection_trigger="", fix_template="",
            source_change="manual", provenance=None, project_type=None
        )
        cmd_experience(args)

        # Export
        import sys, io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        args = argparse.Namespace(
            subcommand="export", format="json", output=None,
            no_sanitize=False, publish=False, experience_id=None
        )
        cmd_experience(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert len(data) == 1
        pattern = data[0]["frontmatter"]["pattern"]
        assert "192.168" not in pattern
        assert "/home/user" not in pattern
        assert "db.internal.com" not in data[0]["body"]

    def test_add_with_provenance(self, tmp_path, monkeypatch):
        """Adding experience includes provenance field."""
        exp_dir = _setup_exp_dir(tmp_path)
        from stdd.cli.commands.experience import cmd_experience
        import argparse
        args = argparse.Namespace(
            subcommand="add", category="cascading_errors",
            pattern="test", language="python", severity="high",
            body="", tags="test", root_cause="", detection_trigger="",
            fix_template="", source_change="manual",
            provenance="human-reported", project_type=None
        )
        cmd_experience(args)

        exp_file = sorted(exp_dir.glob("EXP-*.md"))[-1]
        content = exp_file.read_text(encoding="utf-8")
        assert "provenance: human-reported" in content
        assert "provenance_weight: 0.95" in content


# ── B5: ci.py 73%→82% ──

class TestCICoverage:
    def test_check_anchoring_critical(self, tmp_path, monkeypatch):
        """Anchoring check for critical change."""
        change_dir = tmp_path / "changes" / "test-crit"
        change_dir.mkdir(parents=True)
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        (canon_dir / "test-crit.yaml").write_text(yaml.dump({
            "critical": {"is_critical": True, "risk_assessment": {"safety_critical": True}},
            "anchoring": {"level": "L1"}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import check_anchoring_missing
        status, msg = check_anchoring_missing(change_dir, tmp_path)
        assert status == "FAIL"

    def test_check_anchoring_non_critical(self, tmp_path, monkeypatch):
        """Anchoring check passes for non-critical change."""
        change_dir = tmp_path / "changes" / "test-noncrit"
        change_dir.mkdir(parents=True)
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        (canon_dir / "test-noncrit.yaml").write_text(yaml.dump({
            "critical": {"is_critical": False},
            "anchoring": {"level": "L1"}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import check_anchoring_missing
        status, msg = check_anchoring_missing(change_dir, tmp_path)
        assert status == "PASS"

    def test_check_slice_completion(self, tmp_path, monkeypatch):
        """Slice completion check with evidence."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        (change_dir / ".stdd.yaml").write_text(yaml.dump({
            "phase4": {"slices_completed": {
                "1": {"status": "done", "tc_coverage": "4/4", "new_tests": 4,
                      "verified_at": "2026-06-03T10:00:00"}
            }}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.ci import check_slice_completion
        status, msg = check_slice_completion(change_dir, tmp_path)
        assert status == "PASS"


# ── B6: proposal.py 76%→85% ──

class TestProposalCoverage:
    def test_validate_missing_capabilities(self, tmp_path, monkeypatch):
        """Validate with missing capabilities field."""
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        (canon_dir / "test.yaml").write_text(yaml.dump({
            "meta": {"change_id": "test"}
            # Missing 'why' and 'capabilities'
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.proposal import cmd_proposal_validate
        import argparse
        args = argparse.Namespace(change_name="test")
        with pytest.raises(SystemExit) as exc:
            cmd_proposal_validate(args)
        assert exc.value.code == 1

    def test_show_nonexistent(self, tmp_path, monkeypatch):
        """Show proposal that doesn't exist exits with error."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.proposal import cmd_proposal_show
        import argparse
        args = argparse.Namespace(change_name="no-such")
        with pytest.raises(SystemExit):
            cmd_proposal_show(args)


# ── B8: agent.py 35%→55% ──

class TestAgentCoverage:
    def test_verify_spec_not_found(self, tmp_path, monkeypatch):
        """Agent verify with missing spec."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.agent import cmd_agent_verify
        import argparse
        args = argparse.Namespace(task="no-such", cp=None, dry_run=True)
        with pytest.raises(SystemExit):
            cmd_agent_verify(args)

    def test_dispatch_unknown_action(self, tmp_path, monkeypatch):
        """Agent dispatch unknown action."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.agent import _dispatch
        import argparse
        args = argparse.Namespace(action="unknown", task=None)
        with pytest.raises(SystemExit):
            _dispatch(args)


# ── B9: trace.py 73%→85% ──

class TestTraceCoverage:
    def test_trace_without_changes_dir(self, tmp_path, monkeypatch):
        """Trace when no changes directory exists."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.trace import cmd_trace
        import argparse
        args = argparse.Namespace(tc_id="TC-TEST-001", name=None)
        try:
            cmd_trace(args)
        except SystemExit:
            pass  # Expected behavior


# ── Helpers ──

def _setup_exp_dir(tmp_path: Path) -> Path:
    """Setup minimal experience directory."""
    exp_dir = tmp_path / ".stdd" / "experiences"
    exp_dir.mkdir(parents=True)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.chdir(tmp_path)
    return exp_dir
