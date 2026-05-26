"""Tests for stdd extract-proposal CLI command."""
import pytest
import argparse
import json
import yaml


def _make_args(subcommand=None, **kwargs):
    ns = argparse.Namespace(
        command="extract-proposal",
        dry_run=False,
        verbose=0,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_change(tmp_path, proposal_content=None):
    """Create a minimal change directory with proposal.md."""
    change_dir = tmp_path / "changes" / "2026-01-01-test-feature"
    change_dir.mkdir(parents=True)

    (change_dir / ".stdd.yaml").write_text("change_id: test\n", encoding="utf-8")
    if proposal_content is not None:
        (change_dir / "proposal.md").write_text(proposal_content, encoding="utf-8")

    (tmp_path / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".stdd" / "config.d" / "project.yaml").write_text("""
paths:
  changes_dir: changes
  archive_dir: archive
project:
  language: python
  name: stdd
stdd_version: '2.0'
""", encoding="utf-8")
    (tmp_path / "archive").mkdir(exist_ok=True)

    return change_dir


SAMPLE_PROPOSAL = """\
# Test Feature Proposal

## What Changes

- Add async task queue
- Update API error handling
- Remove deprecated endpoints

## Capabilities

### New Capabilities

- **AsyncTaskQueue**：Asynchronous task processing with retry logic
- **HealthCheckAPI**：New health check endpoint for monitoring

### Modified Capabilities

- **ErrorHandler**：Enhanced error categorization with experience integration

## Success Criteria

- All tests pass
- Coverage > 80%
- No regression in existing APIs

## Impact

**代码层面**：
- app/task_queue.py (新增)
- app/error_handler.py (修改)
- app/health.py (新增)

**配置层面**：
- config/task_queue.yaml (新增)
- config/retry_policy.yaml (新增)

**基础设施**：
- Redis 队列 (新增)
- Worker 进程 (新增)
"""


MINIMAL_PROPOSAL = """\
# Minimal Feature

## What Changes

- One simple change

## Capabilities

## Success Criteria

## Impact
"""


class TestExtractProposal:
    """TC-SAC-001, TC-SAC-002, TC-SAC-003"""

    def test_extract_full_proposal_json(self, tmp_path, monkeypatch):
        """TC-SAC-001: Extract structured data from valid proposal.md as JSON."""
        _setup_change(tmp_path, SAMPLE_PROPOSAL)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_extract_proposal(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        assert data["title"] == "Test Feature Proposal"
        assert len(data["what_changes"]) == 3
        assert "Add async task queue" in data["what_changes"]
        assert len(data["capabilities"]["new"]) == 2
        assert data["capabilities"]["new"][0]["name"] == "AsyncTaskQueue"
        assert data["capabilities"]["new"][1]["name"] == "HealthCheckAPI"
        assert len(data["capabilities"]["modified"]) == 1
        assert data["capabilities"]["modified"][0]["name"] == "ErrorHandler"
        assert len(data["success_criteria"]) == 3
        assert "All tests pass" in data["success_criteria"]
        assert len(data["impact"]["code"]) == 3
        assert len(data["impact"]["config"]) == 2
        assert len(data["impact"]["infrastructure"]) == 2

    def test_extract_format_yaml(self, tmp_path, monkeypatch):
        """TC-SAC-002: --format yaml outputs valid YAML."""
        _setup_change(tmp_path, SAMPLE_PROPOSAL)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="yaml")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_extract_proposal(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = yaml.safe_load(output)
        assert data["title"] == "Test Feature Proposal"
        assert len(data["capabilities"]["new"]) == 2

    def test_missing_proposal_exits_error(self, tmp_path, monkeypatch):
        """TC-SAC-003: Missing proposal.md exits with code 1."""
        _setup_change(tmp_path, None)  # No proposal.md
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        args = _make_args(name="2026-01-01-test-feature", format="json")
        with pytest.raises(SystemExit) as exc_info:
            cmd_extract_proposal(args)
        assert exc_info.value.code == 1

    def test_minimal_proposal_no_sections(self, tmp_path, monkeypatch):
        """Proposal with minimal sections returns empty lists."""
        _setup_change(tmp_path, MINIMAL_PROPOSAL)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_extract_proposal(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        assert data["title"] == "Minimal Feature"
        assert data["what_changes"] == ["One simple change"]
        assert data["capabilities"]["new"] == []
        assert data["capabilities"]["modified"] == []
        assert data["success_criteria"] == []
        assert data["impact"]["code"] == []

    def test_missing_change_dir(self, tmp_path, monkeypatch):
        """Non-existent change dir exits with code 1."""
        (tmp_path / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".stdd" / "config.d" / "project.yaml").write_text("""
paths:
  changes_dir: changes
  archive_dir: archive
project:
  language: python
stdd_version: '2.0'
""", encoding="utf-8")
        (tmp_path / "changes").mkdir(exist_ok=True)
        (tmp_path / "archive").mkdir(exist_ok=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        args = _make_args(name="nonexistent-change", format="json")
        with pytest.raises(SystemExit) as exc_info:
            cmd_extract_proposal(args)
        assert exc_info.value.code == 1

    def test_default_format_is_json(self, tmp_path, monkeypatch):
        """Default output format is JSON when --format not specified."""
        _setup_change(tmp_path, SAMPLE_PROPOSAL)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_extract_proposal(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        assert data["title"] == "Test Feature Proposal"

    def test_impact_with_mixed_content(self, tmp_path, monkeypatch):
        """Impact section with only code changes, no config or infra."""
        proposal = """\
# Simple Feature
## What Changes
- One change
## Capabilities
## Success Criteria
## Impact
**代码层面**：
- app/main.py (修改)
"""
        _setup_change(tmp_path, proposal)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_extract_proposal(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        assert len(data["impact"]["code"]) == 1
        assert data["impact"]["config"] == []
        assert data["impact"]["infrastructure"] == []


class TestExtractProposalExtended:
    """TC-EPE-001 ~ 007: V2.5 extended fields."""

    PROPOSAL_WITH_NEW_FIELDS = """\
# Extended Feature Proposal

## What Changes
- Something

## Capabilities
### New Capabilities
- **TestCap**：Test description

## Success Criteria

## Impact

## Constraints
- Must work on Python 3.10+
- Max memory usage < 512MB

## Stakeholders
- Backend team
- Frontend team

## Risk Areas
- capability: TestCap — API breaking changes risk
- capability: TestCap — Performance degradation under load

## NonGoals
- Not supporting Python 3.9
- No WebSocket support in v1
"""

    def test_extract_constraints(self, tmp_path, monkeypatch):
        """TC-EPE-001: Extract Constraints field."""
        _setup_change(tmp_path, self.PROPOSAL_WITH_NEW_FIELDS)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_extract_proposal(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert "constraints" in data
        assert len(data["constraints"]) == 2
        assert "Python 3.10+" in data["constraints"][0]

    def test_extract_stakeholders(self, tmp_path, monkeypatch):
        """TC-EPE-002: Extract Stakeholders field."""
        _setup_change(tmp_path, self.PROPOSAL_WITH_NEW_FIELDS)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_extract_proposal(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert "stakeholders" in data
        assert "Backend team" in data["stakeholders"]
        assert "Frontend team" in data["stakeholders"]

    def test_extract_risk_areas_structured(self, tmp_path, monkeypatch):
        """TC-EPE-003: Extract RiskAreas with structured capability mapping."""
        _setup_change(tmp_path, self.PROPOSAL_WITH_NEW_FIELDS)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_extract_proposal(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert "risk_areas" in data
        assert len(data["risk_areas"]) == 2
        assert data["risk_areas"][0]["capability"] == "TestCap"
        assert "API breaking" in data["risk_areas"][0]["risk"]

    def test_extract_non_goals(self, tmp_path, monkeypatch):
        """TC-EPE-004: Extract NonGoals field."""
        _setup_change(tmp_path, self.PROPOSAL_WITH_NEW_FIELDS)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_extract_proposal(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert "non_goals" in data
        assert len(data["non_goals"]) == 2
        assert "Python 3.9" in data["non_goals"][0]

    def test_old_proposal_new_fields_empty(self, tmp_path, monkeypatch):
        """TC-EPE-005: V2.4 format proposal returns empty arrays for new fields."""
        _setup_change(tmp_path, SAMPLE_PROPOSAL)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_extract_proposal(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert data.get("constraints") == []
        assert data.get("stakeholders") == []
        assert data.get("risk_areas") == []
        assert data.get("non_goals") == []

    def test_old_fields_unchanged(self, tmp_path, monkeypatch):
        """TC-EPE-006: Old fields (what_changes, capabilities, etc.) unchanged."""
        _setup_change(tmp_path, SAMPLE_PROPOSAL)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.extract_proposal import cmd_extract_proposal

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        cmd_extract_proposal(args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        data = json.loads(output)
        assert len(data["what_changes"]) == 3
        assert len(data["capabilities"]["new"]) == 2
        assert len(data["success_criteria"]) == 3
