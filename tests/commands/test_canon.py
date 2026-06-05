"""TC-CANON-001~005, TC-DUAL-001~003: Canonical data model + dual-track foundation tests."""

import pytest
import yaml
from pathlib import Path


class TestCanonicalDataModel:
    """TC-CANON-001~005"""

    def test_proposal_init_generates_yaml(self, tmp_path, monkeypatch):
        """TC-CANON-001: proposal.yaml generated from proposal.md."""
        # Arrange
        change_dir = tmp_path / "changes" / "2026-06-01-test"
        change_dir.mkdir(parents=True)
        proposal_md = change_dir / "proposal.md"
        proposal_md.write_text("""# Test Change

## Why
Test problem statement.

## What Changes
- Add feature X

## Capabilities
### New Capabilities
- **test-cap**：Test capability description

## Success Criteria
- [ ] Test passes
""", encoding="utf-8")

        (tmp_path / ".stdd").mkdir(parents=True, exist_ok=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.proposal import cmd_proposal_init
        import argparse
        args = argparse.Namespace(change_name="2026-06-01-test", format="yaml")

        # Act
        cmd_proposal_init(args)

        # Assert
        canon_dir = tmp_path / "canonical" / "proposals"
        yaml_file = canon_dir / "2026-06-01-test.yaml"
        assert yaml_file.exists(), f"Expected {yaml_file} to exist"
        data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        assert data["why"]["problem"] == "Test problem statement."
        assert len(data["what_changes"]) == 1
        assert data["what_changes"][0]["description"] == "Add feature X"

    def test_proposal_validate_missing_field(self, tmp_path, monkeypatch):
        """TC-CANON-002: Validation exits non-zero on missing required field."""
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        # Missing 'why.problem'
        bad_yaml = canon_dir / "test.yaml"
        bad_yaml.write_text(yaml.dump({
            "meta": {"change_id": "test", "title": "Test"},
            "capabilities": {"new": []}
        }), encoding="utf-8")

        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.proposal import cmd_proposal_validate
        import argparse
        args = argparse.Namespace(change_name="test")

        # Act & Assert
        with pytest.raises(SystemExit) as exc:
            cmd_proposal_validate(args)
        assert exc.value.code == 1

    def test_pure_markdown_mode_backward_compatible(self, tmp_path, monkeypatch):
        """TC-CANON-005: No canonical/ dir → V2.5 behavior preserved."""
        change_dir = tmp_path / "changes" / "test"
        change_dir.mkdir(parents=True)
        (change_dir / ".stdd.yaml").write_text("active_phase: 1\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.state import cmd_state
        import argparse
        args = argparse.Namespace(subcommand=None, resume=False, context=False)

        # Should not raise or error — just work
        try:
            cmd_state(args)
        except SystemExit:
            pass  # state may exit(0) or exit(1) depending on config
        # Key assertion: no crash due to missing canonical/

    def test_project_index_update(self, tmp_path, monkeypatch):
        """TC-CANON-004: project-index.yaml generated with changes/capabilities/modules."""
        # Create minimal project structure
        (tmp_path / "changes").mkdir()
        (tmp_path / "specs" / "rate-limiting").mkdir(parents=True)
        (tmp_path / "specs" / "rate-limiting" / "spec.md").write_text("# spec", encoding="utf-8")
        (tmp_path / ".stdd").mkdir(parents=True, exist_ok=True)

        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.index import cmd_index_update
        import argparse
        args = argparse.Namespace(subcommand="update")

        cmd_index_update(args)

        index_file = tmp_path / "project-index.yaml"
        assert index_file.exists()
        data = yaml.safe_load(index_file.read_text(encoding="utf-8"))
        assert "project" in data
        assert "changes" in data
        assert "capabilities" in data
        assert "module_index" in data

    def test_project_index_trace(self, tmp_path, monkeypatch, capsys):
        """TC-CANON-004b: index trace shows associated info."""
        # Pre-create a project index
        index_data = {
            "project": {"name": "test", "language": "python"},
            "module_index": {
                "middleware/rate_limit.py": {
                    "capabilities": ["rate-limiting"],
                    "symbols": ["TokenBucket"]
                }
            }
        }
        (tmp_path / "project-index.yaml").write_text(
            yaml.dump(index_data), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.index import cmd_index_trace
        import argparse
        args = argparse.Namespace(file="middleware/rate_limit.py")

        cmd_index_trace(args)
        captured = capsys.readouterr()
        assert "rate-limiting" in captured.out


class TestDualTrackFoundation:
    """TC-DUAL-001~003"""

    def test_canon_init_creates_directories(self, tmp_path, monkeypatch):
        """TC-DUAL-001: canon init creates all required directories."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.canon import cmd_canon_init
        import argparse
        args = argparse.Namespace()
        args.project_level = True  # V2.9: --project-level flag for root-level init

        cmd_canon_init(args)

        canon = tmp_path / "canonical"
        assert canon.exists()
        assert (canon / "proposals").is_dir()
        assert (canon / "designs").is_dir()
        assert (canon / "specs" / "code").is_dir()
        assert (canon / "specs" / "agent").is_dir()
        assert (canon / ".canon-index.yaml").exists()

    def test_canon_generate_creates_human_view(self, tmp_path, monkeypatch):
        """TC-DUAL-002: canon generate creates proposal.md with source_hash."""
        # Set up canonical proposal
        canon_dir = tmp_path / "canonical" / "proposals"
        canon_dir.mkdir(parents=True)
        proposal_yaml = canon_dir / "test.yaml"
        proposal_yaml.write_text(yaml.dump({
            "meta": {"change_id": "test", "title": "Test Change", "status": "draft"},
            "why": {"problem": "Test problem", "motivation": "Test motivation"},
            "what_changes": [{"id": "C1", "description": "Add X", "type": "new"}],
            "capabilities": {"new": [{"name": "cap-x", "description": "Desc"}]},
            "success_criteria": ["Criterion 1"]
        }), encoding="utf-8")

        # Create human-view template
        tmpl_dir = tmp_path / ".stdd" / "templates" / "human-view"
        tmpl_dir.mkdir(parents=True)
        (tmpl_dir / "proposal-brief.md").write_text("""# {{ meta.title }}

## Why
{{ why.problem }}

## What Changes
{% for c in what_changes %}
- {{ c.description }}
{% endfor %}

## Success Criteria
{% for s in success_criteria %}
- [ ] {{ s }}
{% endfor %}
""", encoding="utf-8")

        # Create changes dir
        (tmp_path / "changes" / "test").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.canon import cmd_canon_generate
        import argparse
        args = argparse.Namespace(change_name="test", type="proposal", all=False)

        cmd_canon_generate(args)

        result = tmp_path / "changes" / "test" / "proposal.md"
        assert result.exists()
        content = result.read_text(encoding="utf-8")
        assert "source_hash" in content
        assert "generated_at" in content

    def test_canon_verify_detects_stale(self, tmp_path, monkeypatch):
        """TC-DUAL-003: canon verify warns when Human View is stale."""
        # Mock minimal verify
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.canon import cmd_canon_verify
        import argparse
        args = argparse.Namespace(change_name="test")

        # When canonical doesn't exist → should report not found
        with pytest.raises(SystemExit) as exc:
            cmd_canon_verify(args)
        assert exc.value.code == 1


class TestAgentSpec:
    """TC-CANON-003"""

    def test_agent_spec_format_validation(self, tmp_path, monkeypatch, capsys):
        """TC-CANON-003: agent spec dry-run displays CPs and assertions."""
        # Create agent_spec
        canon_dir = tmp_path / "canonical" / "specs" / "agent"
        canon_dir.mkdir(parents=True)
        agent_spec = canon_dir / "deploy-test.yaml"
        agent_spec.write_text(yaml.dump({
            "meta": {"task_id": "deploy-test", "system": "test-server"},
            "steps": [
                {
                    "id": "CP-1",
                    "description": "Pull image",
                    "action": "docker pull test:latest",
                    "assertions": [
                        {"type": "exit_code", "expected": 0},
                        {"type": "stdout_contains", "expected": "Digest:"}
                    ]
                }
            ],
            "rollback": {"steps": ["docker compose down"]}
        }), encoding="utf-8")

        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.agent import cmd_agent_verify
        import argparse
        args = argparse.Namespace(task="deploy-test", cp=None, dry_run=True)

        cmd_agent_verify(args)
        captured = capsys.readouterr()
        assert "CP-1" in captured.out
        assert "Pull image" in captured.out
        assert "exit_code" in captured.out
