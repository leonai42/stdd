"""TC-SKIL-001, TC-SKIL-002: Skill management tests (V2.7)."""

import pytest
from pathlib import Path


class TestSkillCreate:
    """TC-SKIL-001, TC-SKIL-002"""

    def test_create_language_skill(self, tmp_path, monkeypatch):
        """TC-SKIL-001: skill create generates SKILL.md with correct structure."""
        # Arrange
        (tmp_path / ".stdd" / "skills" / "languages").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.skill import cmd_skill_create
        import argparse
        args = argparse.Namespace(action="create", name="test-patterns", type="language")

        # Act
        cmd_skill_create(args)

        # Assert
        skill_file = tmp_path / ".stdd" / "skills" / "languages" / "test-patterns" / "SKILL.md"
        assert skill_file.exists()
        content = skill_file.read_text(encoding="utf-8")
        assert "name: test-patterns" in content
        assert "origin: STDD" in content
        assert "category: language" in content
        assert "## 何时激活" in content
        assert "## 核心规范" in content
        assert "## 反模式" in content

    def test_create_workflow_skill(self, tmp_path, monkeypatch):
        """Skill create with type=workflow goes to correct directory."""
        (tmp_path / ".stdd" / "skills" / "workflow").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.skill import cmd_skill_create
        import argparse
        args = argparse.Namespace(action="create", name="my-workflow", type="workflow")

        cmd_skill_create(args)

        skill_file = tmp_path / ".stdd" / "skills" / "workflow" / "my-workflow" / "SKILL.md"
        assert skill_file.exists()
        content = skill_file.read_text(encoding="utf-8")
        assert "category: workflow" in content

    def test_create_tools_skill(self, tmp_path, monkeypatch):
        """Skill create with type=tools goes to correct directory."""
        (tmp_path / ".stdd" / "skills" / "tools").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.skill import cmd_skill_create
        import argparse
        args = argparse.Namespace(action="create", name="docker-build", type="tools")

        cmd_skill_create(args)

        skill_file = tmp_path / ".stdd" / "skills" / "tools" / "docker-build" / "SKILL.md"
        assert skill_file.exists()
        content = skill_file.read_text(encoding="utf-8")
        assert "category: tools" in content

    def test_duplicate_skill_exits(self, tmp_path, monkeypatch):
        """Creating duplicate skill exits with error."""
        skill_dir = tmp_path / ".stdd" / "skills" / "languages" / "existing"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# existing", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.skill import cmd_skill_create
        import argparse
        args = argparse.Namespace(action="create", name="existing", type="language")

        with pytest.raises(SystemExit) as exc:
            cmd_skill_create(args)
        assert exc.value.code == 1

    def test_dispatch_routes_create(self, tmp_path, monkeypatch):
        """_dispatch routes to create correctly."""
        (tmp_path / ".stdd" / "skills" / "languages").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.skill import _dispatch
        import argparse
        args = argparse.Namespace(action="create", name="dispatch-test", type="language")

        _dispatch(args)
        skill_file = tmp_path / ".stdd" / "skills" / "languages" / "dispatch-test" / "SKILL.md"
        assert skill_file.exists()

    def test_dispatch_unknown_action(self, tmp_path, monkeypatch):
        """Dispatch exits on unknown action."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.skill import _dispatch
        import argparse
        args = argparse.Namespace(action="unknown", name="test")

        with pytest.raises(SystemExit):
            _dispatch(args)
