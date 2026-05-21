"""Tests for stdd dependency-graph CLI command."""
import pytest
import argparse
import json


def _make_args(**kwargs):
    ns = argparse.Namespace(
        command="dependency-graph",
        dry_run=False,
        verbose=0,
    )
    for k, v in kwargs.items():
        setattr(ns, k, v)
    return ns


def _setup_change(tmp_path, specs: dict[str, str] = None):
    """Create a minimal change directory with specs files.

    specs: dict of filename -> content for files in specs/<capability>/spec.md
    """
    change_dir = tmp_path / "changes" / "2026-01-01-test-feature"
    change_dir.mkdir(parents=True)

    (change_dir / ".stdd.yaml").write_text("change_id: test\n", encoding="utf-8")

    if specs:
        for cap_name, content in specs.items():
            cap_dir = change_dir / "specs" / cap_name
            cap_dir.mkdir(parents=True)
            (cap_dir / "spec.md").write_text(content, encoding="utf-8")

    (tmp_path / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".stdd" / "config.d" / "project.yaml").write_text("""
paths:
  changes_dir: changes
  archive_dir: archive
project:
  language: python
stdd_version: '2.0'
""", encoding="utf-8")
    (tmp_path / "archive").mkdir(exist_ok=True)

    return change_dir


SIMPLE_SPEC = """\
# Simple Capability

## Scenario: Basic Flow
**GIVEN** the system is running
**WHEN** user sends a request
**THEN** the system SHALL respond with 200

#### Scenario: Happy Path
**GIVEN** valid input data
**WHEN** the endpoint is called
**THEN** the response SHALL contain the expected data
"""

DEPENDENT_SPEC = """\
# Dependent Capability

## Scenario: Depends on TaskQueue
**GIVEN** the task-queue is initialized and running
**WHEN** a new task is submitted
**THEN** the task SHALL be processed within 5 seconds

#### Scenario: Falls back to Cache
**GIVEN** the cache-layer is available
**WHEN** task result is requested
**THEN** the cached result SHALL be returned
"""

INDEPENDENT_SPEC = """\
# Independent Capability

## Scenario: Standalone Check
**GIVEN** the config file exists
**WHEN** the application starts
**THEN** it SHALL load all configuration values
"""

CYCLIC_SPEC_A = """\
# Cyclic A

## Scenario: A needs B
**GIVEN** cyclic-b is running
**WHEN** A is activated
**THEN** it SHALL coordinate with B
"""

CYCLIC_SPEC_B = """\
# Cyclic B

## Scenario: B needs A
**GIVEN** cyclic-a is running
**WHEN** B is activated
**THEN** it SHALL coordinate with A
"""


class TestDependencyGraph:
    """TC-SLI-001 ~ TC-SLI-005"""

    def test_build_graph_with_dependencies(self, tmp_path, monkeypatch):
        """TC-SLI-001: Build graph with GIVEN dependencies between capabilities."""
        specs = {
            "task-queue": SIMPLE_SPEC,
            "async-processor": DEPENDENT_SPEC,
            "config-loader": INDEPENDENT_SPEC,
        }
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_dependency_graph(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        assert len(data["nodes"]) == 3
        assert len(data["edges"]) >= 1  # async-processor -> task-queue

        # Verify node structure
        node_ids = {n["id"] for n in data["nodes"]}
        assert "task-queue" in node_ids
        assert "async-processor" in node_ids
        assert "config-loader" in node_ids

        # config-loader has no incoming deps -> zero_dependency
        assert "config-loader" in data["zero_dependency"]

    def test_format_json_valid(self, tmp_path, monkeypatch):
        """--format json outputs valid JSON structure."""
        specs = {"task-queue": SIMPLE_SPEC}
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_dependency_graph(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        assert "nodes" in data
        assert "edges" in data
        assert "zero_dependency" in data
        assert "cycles" in data
        assert len(data["nodes"]) == 1
        assert data["zero_dependency"] == ["task-queue"]

    def test_format_dot_valid(self, tmp_path, monkeypatch):
        """--format dot outputs valid Graphviz DOT format."""
        specs = {"task-queue": SIMPLE_SPEC, "cache-layer": INDEPENDENT_SPEC}
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="dot")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_dependency_graph(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        assert output.startswith("digraph STDD {")
        assert "rankdir=LR" in output
        assert '"task-queue"' in output
        assert '"cache-layer"' in output
        assert "}" in output

    def test_format_text_human_readable(self, tmp_path, monkeypatch):
        """--format text outputs human-readable report."""
        specs = {"task-queue": SIMPLE_SPEC, "async-processor": DEPENDENT_SPEC}
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        args = _make_args(name="2026-01-01-test-feature", format="text")
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_dependency_graph(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        assert "Nodes:" in output
        assert "Edges:" in output

    def test_cycle_detection_exits_error(self, tmp_path, monkeypatch):
        """TC-SLI-002: Cycle detection exits with code 1."""
        specs = {
            "cyclic-a": CYCLIC_SPEC_A,
            "cyclic-b": CYCLIC_SPEC_B,
        }
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        args = _make_args(name="2026-01-01-test-feature", format="json")
        with pytest.raises(SystemExit) as exc_info:
            cmd_dependency_graph(args)
        assert exc_info.value.code == 1

    def test_no_edges_when_independent(self, tmp_path, monkeypatch):
        """Graph with no cross-references has zero edges."""
        specs = {
            "feature-a": SIMPLE_SPEC,
            "feature-b": INDEPENDENT_SPEC,
        }
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_dependency_graph(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        assert len(data["edges"]) == 0
        assert len(data["zero_dependency"]) == 2

    def test_missing_specs_dir_exits_error(self, tmp_path, monkeypatch):
        """Missing specs/ directory exits with code 1."""
        change_dir = tmp_path / "changes" / "2026-01-01-test-feature"
        change_dir.mkdir(parents=True)
        (tmp_path / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".stdd" / "config.d" / "project.yaml").write_text("""
paths:
  changes_dir: changes
  archive_dir: archive
project:
  language: python
stdd_version: '2.0'
""", encoding="utf-8")
        (tmp_path / "archive").mkdir(exist_ok=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        args = _make_args(name="2026-01-01-test-feature", format="json")
        with pytest.raises(SystemExit) as exc_info:
            cmd_dependency_graph(args)
        assert exc_info.value.code == 1

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

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        args = _make_args(name="nonexistent-change", format="json")
        with pytest.raises(SystemExit) as exc_info:
            cmd_dependency_graph(args)
        assert exc_info.value.code == 1

    def test_zero_dependency_nodes(self, tmp_path, monkeypatch):
        """TC-SLI-003: Zero-dependency nodes are correctly identified."""
        specs = {
            "base-module": SIMPLE_SPEC,
            "dependent-a": """\
# Dependent A
## Scenario: Needs base
**GIVEN** base-module is ready
**WHEN** A starts
**THEN** it SHALL connect to base-module
""",
            "dependent-b": """\
# Dependent B
## Scenario: Needs base
**GIVEN** base-module is ready
**WHEN** B starts
**THEN** it SHALL connect to base-module
""",
        }
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        import sys
        from io import StringIO
        args = _make_args(name="2026-01-01-test-feature", format="json")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_dependency_graph(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        data = json.loads(output)
        # dependent-a and dependent-b depend ON base-module, so they have no incoming edges
        assert set(data["zero_dependency"]) == {"dependent-a", "dependent-b"}

    def test_default_format_is_text(self, tmp_path, monkeypatch):
        """Default output format is text when --format not specified."""
        specs = {"module-a": SIMPLE_SPEC}
        _setup_change(tmp_path, specs)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.dependency_graph import cmd_dependency_graph

        args = _make_args(name="2026-01-01-test-feature")
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            cmd_dependency_graph(args)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout

        assert "Nodes:" in output
