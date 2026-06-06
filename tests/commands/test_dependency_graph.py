"""Tests for stdd dependency-graph CLI."""
import json, argparse
from stdd.cli.commands.dependency_graph import cmd_dependency_graph

class TestDependencyGraph:
    def test_text_format(self, tmp_path, capsys):
        d = tmp_path / "changes" / "2026-06-06-test"
        specs = d / "specs" / "auth"
        specs.mkdir(parents=True)
        (specs / "spec.md").write_text("# Capability: auth\n## Requirement: login\n### Scenario: success\n- **GIVEN** valid credentials\n- **WHEN** login\n- **THEN** SHALL return token\n", encoding="utf-8")
        (d / ".stdd.yaml").write_text("status: active\n", encoding="utf-8")
        ns = argparse.Namespace(name="2026-06-06-test", format="text", verbose=0, dry_run=False)
        cmd_dependency_graph(ns)
        out = capsys.readouterr().out
        assert "auth" in out

    def test_json_format(self, tmp_path, capsys):
        d = tmp_path / "changes" / "2026-06-06-test2"
        specs = d / "specs" / "api"
        specs.mkdir(parents=True)
        (specs / "spec.md").write_text("# Capability: api\n## Requirement: r1\n### Scenario: s1\n- **GIVEN** data\n- **WHEN** call\n- **THEN** SHALL return\n", encoding="utf-8")
        (d / ".stdd.yaml").write_text("status: active\n", encoding="utf-8")
        ns = argparse.Namespace(name="2026-06-06-test2", format="json", verbose=0, dry_run=False)
        cmd_dependency_graph(ns)
        data = json.loads(capsys.readouterr().out)
        assert "nodes" in data or "capabilities" in data
