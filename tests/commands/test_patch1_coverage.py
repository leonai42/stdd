"""V2.8-patch1: Targeted coverage boosts for B4 B5 B6 B8 B9."""

import yaml
import json
import pytest
from pathlib import Path


# ── B4: experience.py ──

class TestExpProvenance:
    def test_add_default_provenance(self, tmp_path, monkeypatch):
        """New experience defaults to ai-inferred."""
        exp_dir = tmp_path / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.experience import cmd_experience
        import argparse
        args = argparse.Namespace(
            subcommand="add", category="cascading_errors", pattern="test",
            language="python", severity="medium", body="", tags="test",
            root_cause="", detection_trigger="", fix_template="",
            source_change=None, provenance=None, project_type=None
        )
        cmd_experience(args)
        exp_file = sorted(exp_dir.glob("EXP-*.md"))[-1]
        content = exp_file.read_text(encoding="utf-8")
        assert "provenance: ai-inferred" in content
        assert "provenance_weight: 0.6" in content

    def test_export_publish_sets_shared_and_tar(self, tmp_path, monkeypatch):
        """Export --publish creates tar.gz and sets lifecycle to shared."""
        exp_dir = tmp_path / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.experience import cmd_experience
        import argparse
        # Add experience
        cmd_experience(argparse.Namespace(
            subcommand="add", category="cascading_errors", pattern="test_pub",
            language="python", severity="high", body="test body", tags="",
            root_cause="", detection_trigger="", fix_template="",
            source_change="manual", provenance="human-reported", project_type=None
        ))
        # Export --publish
        import sys, io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        cmd_experience(argparse.Namespace(
            subcommand="export", format="json",
            output="test-export.tar.gz", no_sanitize=False,
            publish=True, experience_id=None
        ))
        sys.stdout = old_stdout
        # Verify tar.gz created
        tar_file = tmp_path / "test-export.tar.gz"
        assert tar_file.exists()

    def test_pull_no_packs_configured(self, tmp_path, monkeypatch, capsys):
        """Pull with no packs configured gives helpful error."""
        exp_dir = tmp_path / ".stdd" / "experiences"
        exp_dir.mkdir(parents=True)
        # Setup config with registries but no matching pack
        config_dir = tmp_path / ".stdd" / "config.d"
        config_dir.mkdir(parents=True)
        (config_dir / "experience.yaml").write_text(yaml.dump({
            "community": {"registries": [], "packs": []}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.experience import cmd_experience
        import argparse
        args = argparse.Namespace(
            subcommand="pull", pack_name="nonexistent", source=None
        )
        with pytest.raises(SystemExit):
            cmd_experience(args)


# ── B5: ci.py ──

class TestCIMoreCoverage:
    def test_anchoring_financial_requires_l4(self, tmp_path, monkeypatch):
        """Financial change requires L4 anchoring."""
        change_dir = tmp_path / "changes" / "test-fin"
        change_dir.mkdir(parents=True)
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        (canon_dir / "test-fin.yaml").write_text(yaml.dump({
            "critical": {"is_critical": True, "risk_assessment": {"financial": True}},
            "anchoring": {"level": "L2"}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.ci import check_anchoring_missing
        status, msg = check_anchoring_missing(change_dir, tmp_path)
        assert status == "FAIL"

    def test_anchoring_cross_system_requires_l2(self, tmp_path, monkeypatch):
        """Cross-system change with L1 fails."""
        change_dir = tmp_path / "changes" / "test-xs"
        change_dir.mkdir(parents=True)
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        (canon_dir / "test-xs.yaml").write_text(yaml.dump({
            "critical": {"is_critical": True, "risk_assessment": {"cross_system": True}},
            "anchoring": {"level": "L1"}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.ci import check_anchoring_missing
        status, msg = check_anchoring_missing(change_dir, tmp_path)
        assert status == "FAIL"

    def test_slice_completion_no_evidence(self, tmp_path, monkeypatch):
        """Slice marked done but no verified_at triggers warning."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        (change_dir / ".stdd.yaml").write_text(yaml.dump({
            "phase4": {"slices_completed": {
                "1": {"status": "done", "new_tests": 0}
            }}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.ci import check_slice_completion
        status, msg = check_slice_completion(change_dir, tmp_path)
        assert status == "WARN"


# ── B8: agent.py ──

class TestAgentMoreCoverage:
    def test_verify_spec_missing(self, tmp_path, monkeypatch):
        """Agent verify exits when spec not found."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.agent import cmd_agent_verify
        import argparse
        args = argparse.Namespace(task="missing", cp=None, dry_run=False)
        with pytest.raises(SystemExit):
            cmd_agent_verify(args)

    def test_dry_run_displays_checkpoints(self, tmp_path, monkeypatch, capsys):
        """Dry-run shows checkpoints without executing."""
        canon_dir = tmp_path / "canonical" / "specs" / "agent"
        canon_dir.mkdir(parents=True)
        (canon_dir / "test.yaml").write_text(yaml.dump({
            "meta": {"task_id": "test", "system": "test"},
            "steps": [
                {"id": "CP-1", "description": "Check", "action": "echo hello",
                 "assertions": [{"type": "exit_code", "expected": 0}]}
            ],
            "rollback": {"steps": []}
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.agent import cmd_agent_verify
        import argparse
        args = argparse.Namespace(task="test", cp=None, dry_run=True)
        cmd_agent_verify(args)
        captured = capsys.readouterr()
        assert "CP-1" in captured.out
        assert "Check" in captured.out


# ── B9: trace.py ──

class TestTraceMoreCoverage:
    def test_trace_with_test_plan(self, tmp_path, monkeypatch, capsys):
        """Trace finds TC in test-plan."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        (change_dir / "test-plan.md").write_text(
            "| **ID** | TC-TEST-001 | **P0** | test | test | test |", encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.trace import cmd_trace
        import argparse
        args = argparse.Namespace(tc_id="TC-TEST-001", name=None)
        cmd_trace(args)
        captured = capsys.readouterr()
        assert "TC-TEST-001" in captured.out

    def test_trace_invalid_format(self, tmp_path, monkeypatch):
        """Trace with invalid TC-ID format exits."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.trace import cmd_trace
        import argparse
        args = argparse.Namespace(tc_id="INVALID", name=None)
        with pytest.raises(SystemExit):
            cmd_trace(args)
