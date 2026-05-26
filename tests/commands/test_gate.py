"""Tests for stdd gate CLI command (V2.5 gate-file-confirm)."""
import pytest
import argparse
import yaml


def _make_args(subcommand="approve", **kwargs):
    ns = argparse.Namespace(
        command="gate",
        subcommand=subcommand,
        dry_run=False,
        verbose=0,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_gate_project(tmp_path, gates_confirmed=None):
    """Create project with change directory and .stdd.yaml."""
    (tmp_path / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".stdd" / "config.d" / "gates.yaml").write_text("""\
gates:
  phase1_understand:
    required: true
  phase2_spec:
    required: true
  phase5_verify:
    required: true
confirmation:
  channels:
    - dialog
    - file_token
    - cli
""", encoding="utf-8")
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
    change_dir = tmp_path / "changes" / "2026-01-01-gate-test"
    change_dir.mkdir(parents=True)

    phases = {
        "understand": {"status": "pending"},
        "spec": {"status": "pending"},
        "slice": {"status": "pending"},
        "build": {"status": "pending"},
        "verify": {"status": "pending"},
        "deliver": {"status": "pending"},
    }

    if gates_confirmed:
        for g in gates_confirmed:
            label, key = {1: ("understand", "understand"), 2: ("spec", "spec"), 3: ("verify", "verify")}[g]
            phases[key]["status"] = "completed"
            phases[key]["confirmed_at"] = "2026-01-01T10:00:00"

    state = {
        "change_id": "2026-01-01-gate-test",
        "current_phase": "spec",
        "status": "active",
        "version": "2.0",
        "phases": phases,
        "traceability": {"spec_scenarios": 3, "tc_cases": 3, "test_functions": 0},
    }
    (change_dir / ".stdd.yaml").write_text(
        yaml.dump(state, allow_unicode=True, default_flow_style=False),
        encoding="utf-8"
    )

    return change_dir


class TestGateConfirm:
    """TC-GF-001 ~ 007: Gate file-token and CLI confirmation."""

    def test_cli_approve_gate1(self, tmp_path, monkeypatch, capsys):
        """TC-GF-001: CLI approve Gate 1 writes confirmed_at."""
        change_dir = _setup_gate_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.gate import cmd_gate

        args = _make_args("approve", name="2026-01-01-gate-test", gate=1)
        cmd_gate(args)
        captured = capsys.readouterr()
        assert "Gate 1 confirmed" in captured.out

        data = yaml.safe_load((change_dir / ".stdd.yaml").read_text(encoding="utf-8"))
        assert data["phases"]["understand"]["confirmed_at"] is not None
        assert data["phases"]["understand"]["status"] == "completed"

    def test_idempotent_reconfirm(self, tmp_path, monkeypatch, capsys):
        """TC-GF-002: Re-confirming an already confirmed gate is idempotent."""
        change_dir = _setup_gate_project(tmp_path, gates_confirmed=[1])
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.gate import cmd_gate

        args = _make_args("approve", name="2026-01-01-gate-test", gate=1)
        cmd_gate(args)
        captured = capsys.readouterr()
        assert "already confirmed" in captured.out

        # confirmed_at should not change
        data = yaml.safe_load((change_dir / ".stdd.yaml").read_text(encoding="utf-8"))
        assert data["phases"]["understand"]["confirmed_at"] == "2026-01-01T10:00:00"

    def test_gate_order_validation(self, tmp_path, monkeypatch):
        """TC-GF-003: Cannot confirm Gate 2 before Gate 1."""
        _setup_gate_project(tmp_path)  # No gates confirmed
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.gate import cmd_gate

        args = _make_args("approve", name="2026-01-01-gate-test", gate=2)
        with pytest.raises(SystemExit) as exc_info:
            cmd_gate(args)
        assert exc_info.value.code == 1

    def test_invalid_gate_number(self, tmp_path, monkeypatch):
        """TC-GF-004: Invalid gate number returns error."""
        _setup_gate_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.gate import cmd_gate

        args = _make_args("approve", name="2026-01-01-gate-test", gate=4)
        with pytest.raises(SystemExit) as exc_info:
            cmd_gate(args)
        assert exc_info.value.code == 1

    def test_file_token_confirmation(self, tmp_path, monkeypatch, capsys):
        """TC-GF-005: GATE<N>_APPROVED file is recognized as confirmation."""
        change_dir = _setup_gate_project(tmp_path, gates_confirmed=[1])
        # Create file token for Gate 2
        (change_dir / "GATE2_APPROVED").touch()
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.gate import cmd_gate

        args = _make_args("approve", name="2026-01-01-gate-test", gate=2)
        cmd_gate(args)
        captured = capsys.readouterr()
        assert "Gate 2 confirmed" in captured.out

        data = yaml.safe_load((change_dir / ".stdd.yaml").read_text(encoding="utf-8"))
        assert data["phases"]["spec"]["confirmed_at"] is not None

    def test_file_token_and_cli_equivalent(self, tmp_path, monkeypatch, capsys):
        """TC-GF-006: File token + CLI approve are equivalent."""
        change_dir = _setup_gate_project(tmp_path, gates_confirmed=[1])
        (change_dir / "GATE2_APPROVED").touch()
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.gate import cmd_gate

        # First call: confirm via file token
        args = _make_args("approve", name="2026-01-01-gate-test", gate=2)
        cmd_gate(args)

        # Second call: should say already confirmed
        args2 = _make_args("approve", name="2026-01-01-gate-test", gate=2)
        cmd_gate(args2)
        captured = capsys.readouterr()
        assert "already confirmed" in captured.out

    def test_configurable_channels(self, tmp_path, monkeypatch):
        """TC-GF-007: gates.yaml channels config is readable."""
        _setup_gate_project(tmp_path)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.gate import _read_gates_config
        config = _read_gates_config(tmp_path)
        assert "confirmation" in config
        assert "channels" in config["confirmation"]
        assert "file_token" in config["confirmation"]["channels"]
        assert "cli" in config["confirmation"]["channels"]
