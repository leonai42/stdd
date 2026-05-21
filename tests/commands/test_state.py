"""Tests for stdd state CLI command (V2.5 session-resume)."""
import pytest
import argparse
import yaml
from datetime import datetime


def _make_args(subcommand=None, **kwargs):
    ns = argparse.Namespace(
        command="state",
        dry_run=False,
        verbose=0,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_state_project(tmp_path, with_state=True):
    """Create project with a change directory and .stdd.yaml."""
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
    (tmp_path / "changes").mkdir(exist_ok=True)
    change_dir = tmp_path / "changes" / "2026-01-01-state-test"
    change_dir.mkdir(parents=True)

    if with_state:
        state = {
            "change_id": "2026-01-01-state-test",
            "current_phase": "build",
            "status": "active",
            "version": "2.0",
            "phases": {
                "understand": {"status": "completed", "confirmed_at": "2026-01-01"},
                "spec": {"status": "completed", "confirmed_at": "2026-01-01"},
                "slice": {"status": "completed"},
                "build": {"status": "in_progress"},
                "verify": {"status": "pending"},
                "deliver": {"status": "pending"},
            },
            "traceability": {"spec_scenarios": 5, "tc_cases": 5, "test_functions": 0},
        }
        (change_dir / ".stdd.yaml").write_text(
            yaml.dump(state, allow_unicode=True, default_flow_style=False),
            encoding="utf-8"
        )

    return change_dir


class TestSessionResume:
    """TC-SR-001 ~ 004: Session resume context read/write."""

    def test_write_resume_context(self, tmp_path, monkeypatch):
        """TC-SR-001: Write 4 resume fields to .stdd.yaml."""
        change_dir = _setup_state_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import write_resume_context

        write_resume_context(change_dir,
                             resume_context="slice-2-halfway",
                             active_slice="2",
                             last_action="implemented cmd_verify")

        data = yaml.safe_load((change_dir / ".stdd.yaml").read_text(encoding="utf-8"))
        assert data["resume_context"] == "slice-2-halfway"
        assert data["active_slice"] == "2"
        assert data["last_action"] == "implemented cmd_verify"
        assert "last_modified" in data

    def test_backward_compatibility(self, tmp_path, monkeypatch):
        """TC-SR-002: Read V2.4 format .stdd.yaml returns None for new fields."""
        change_dir = _setup_state_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import read_resume_context

        ctx = read_resume_context(change_dir)
        assert ctx["resume_context"] is None
        assert ctx["active_slice"] is None
        assert ctx["last_action"] is None
        assert ctx["last_modified"] is None

    def test_phase_switch_auto_update(self, tmp_path, monkeypatch):
        """TC-SR-003: Phase switch updates resume_context."""
        change_dir = _setup_state_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import write_resume_context, read_resume_context

        write_resume_context(change_dir, resume_context="build-phase-started")
        ctx = read_resume_context(change_dir)
        assert ctx["resume_context"] == "build-phase-started"

        write_resume_context(change_dir, resume_context="verify-phase-started", active_slice="3")
        ctx = read_resume_context(change_dir)
        assert ctx["resume_context"] == "verify-phase-started"
        assert ctx["active_slice"] == "3"

    def test_read_resume_context_parsing(self, tmp_path, monkeypatch):
        """TC-SR-004: Read resume context parsing is correct."""
        change_dir = _setup_state_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import write_resume_context, read_resume_context

        write_resume_context(change_dir,
                             resume_context="chunk-3-of-5",
                             active_slice="C",
                             last_action="wrote tests for curate dedup")

        ctx = read_resume_context(change_dir)
        assert ctx["resume_context"] == "chunk-3-of-5"
        assert ctx["active_slice"] == "C"
        assert ctx["last_action"] == "wrote tests for curate dedup"
