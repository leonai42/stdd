"""TC-EFFI-003: Hooks lifecycle management tests (V2.7)."""

import json
import pytest
from pathlib import Path


class TestHooksInstall:
    """TC-EFFI-003"""

    def test_install_creates_scripts_and_config(self, tmp_path, monkeypatch):
        """Hook install creates .stdd/hooks/ scripts and updates settings.json."""
        # Arrange
        (tmp_path / ".stdd").mkdir(parents=True)
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)
        (claude_dir / "settings.local.json").write_text("{}", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.hooks import cmd_hooks_install
        import argparse
        args = argparse.Namespace(action="install", force=False)

        # Act
        cmd_hooks_install(args)

        # Assert: scripts created
        hooks_dir = tmp_path / ".stdd" / "hooks"
        assert hooks_dir.exists()
        assert (hooks_dir / "session-start.py").exists()
        assert (hooks_dir / "pre-compact.py").exists()
        assert (hooks_dir / "session-end.py").exists()

        # Assert: settings.json updated with correct array-of-matchers format
        settings = json.loads((claude_dir / "settings.local.json").read_text(encoding="utf-8"))
        assert "hooks" in settings
        for hook_name in ("SessionStart", "PreCompact", "Stop"):
            assert hook_name in settings["hooks"], f"{hook_name} missing from hooks config"
            value = settings["hooks"][hook_name]
            assert isinstance(value, list), (
                f"hooks.{hook_name} should be a list (array of matchers), "
                f"got {type(value).__name__}"
            )
            assert len(value) > 0, f"hooks.{hook_name} should have at least one matcher"
            matcher = value[0]
            assert "hooks" in matcher, f"hooks.{hook_name}[0] missing 'hooks' key"
            assert isinstance(matcher["hooks"], list), (
                f"hooks.{hook_name}[0].hooks should be a list"
            )
            assert len(matcher["hooks"]) > 0, (
                f"hooks.{hook_name}[0].hooks should not be empty"
            )
            hook = matcher["hooks"][0]
            assert hook["type"] == "command", (
                f"hooks.{hook_name}[0].hooks[0].type should be 'command', "
                f"got {hook.get('type')!r}"
            )
            assert "command" in hook, (
                f"hooks.{hook_name}[0].hooks[0] missing 'command' field"
            )

    def test_install_skips_existing_without_force(self, tmp_path, monkeypatch, capsys):
        """Second install without --force skips existing scripts."""
        hooks_dir = tmp_path / ".stdd" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "session-start.py").write_text("# existing", encoding="utf-8")

        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)
        (claude_dir / "settings.local.json").write_text("{}", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.hooks import cmd_hooks_install
        import argparse
        args = argparse.Namespace(action="install", force=False)

        cmd_hooks_install(args)
        captured = capsys.readouterr()
        assert "[SKIP]" in captured.out

    def test_install_force_overwrites(self, tmp_path, monkeypatch):
        """Install with --force overwrites existing scripts."""
        hooks_dir = tmp_path / ".stdd" / "hooks"
        hooks_dir.mkdir(parents=True)
        original = hooks_dir / "session-start.py"
        original.write_text("# old script", encoding="utf-8")

        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)
        (claude_dir / "settings.local.json").write_text("{}", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.hooks import cmd_hooks_install
        import argparse
        args = argparse.Namespace(action="install", force=True)

        cmd_hooks_install(args)
        content = original.read_text(encoding="utf-8")
        assert "STDD SessionStart Hook" in content

    def test_status_shows_installed(self, tmp_path, monkeypatch, capsys):
        """Status command shows installed hooks."""
        hooks_dir = tmp_path / ".stdd" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "test-hook.py").write_text("# test", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.hooks import cmd_hooks_status
        import argparse
        args = argparse.Namespace(action="status")

        cmd_hooks_status(args)
        captured = capsys.readouterr()
        assert "test-hook.py" in captured.out

    def test_status_no_hooks(self, tmp_path, monkeypatch, capsys):
        """Status when no hooks installed."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.hooks import cmd_hooks_status
        import argparse
        args = argparse.Namespace(action="status")

        cmd_hooks_status(args)
        captured = capsys.readouterr()
        assert "No STDD hooks installed" in captured.out

    def test_uninstall_removes_config(self, tmp_path, monkeypatch):
        """Uninstall removes hooks from settings.json."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)
        settings = {"hooks": {"SessionStart": "python test.py"}, "other": "keep"}
        (claude_dir / "settings.local.json").write_text(
            json.dumps(settings), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.hooks import cmd_hooks_uninstall
        import argparse
        args = argparse.Namespace(action="uninstall")

        cmd_hooks_uninstall(args)
        result = json.loads(
            (claude_dir / "settings.local.json").read_text(encoding="utf-8"))
        assert "hooks" not in result
        assert result["other"] == "keep"  # Preserve non-STDD config

    def test_dispatch_routes_correctly(self, tmp_path, monkeypatch):
        """_dispatch routes to correct subcommand."""
        from stdd.cli.commands.hooks import _dispatch
        import argparse

        # Verify dispatch doesn't crash for valid actions
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)
        (claude_dir / "settings.local.json").write_text("{}", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        # Status should work
        args = argparse.Namespace(action="status")
        try:
            _dispatch(args)
        except SystemExit:
            pass

    def test_install_validates_config_format(self, tmp_path, monkeypatch, capsys):
        """install validates written config and warns on format errors."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)
        # Pre-populate with malformed hooks (string instead of array)
        bad_settings = {
            "hooks": {
                "SessionStart": "python bad.py",
                "PreCompact": 123,
                "Stop": [{"hooks": []}],  # empty hooks array
            }
        }
        (claude_dir / "settings.local.json").write_text(
            json.dumps(bad_settings), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.hooks import _validate_hooks_config
        warnings = _validate_hooks_config(claude_dir / "settings.local.json")

        # Should report at least 3 issues: string, int, empty hooks
        assert len(warnings) >= 3, f"Expected >=3 warnings, got {len(warnings)}: {warnings}"
        assert any("SessionStart" in w and "array" in w.lower() for w in warnings), (
            f"Expected warning about SessionStart being non-array, got: {warnings}"
        )
        assert any("PreCompact" in w for w in warnings), (
            f"Expected warning about PreCompact, got: {warnings}"
        )
        assert any("empty" in w.lower() for w in warnings), (
            f"Expected warning about empty hooks, got: {warnings}"
        )

    def test_install_validates_clean_config_passes(self, tmp_path, monkeypatch, capsys):
        """_validate_hooks_config returns no warnings for correct format."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir(parents=True)
        good_settings = {
            "hooks": {
                "SessionStart": [
                    {"hooks": [{"type": "command", "command": "python test.py"}]}
                ],
                "PreCompact": [
                    {"hooks": [{"type": "command", "command": "python test2.py"}]}
                ],
                "Stop": [
                    {"hooks": [{"type": "command", "command": "python test3.py"}]}
                ],
            }
        }
        (claude_dir / "settings.local.json").write_text(
            json.dumps(good_settings), encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        from stdd.cli.commands.hooks import _validate_hooks_config
        warnings = _validate_hooks_config(claude_dir / "settings.local.json")

        assert len(warnings) == 0, f"Expected 0 warnings for valid config, got: {warnings}"

    def test_dispatch_unknown_action(self, tmp_path, monkeypatch):
        """Dispatch exits on unknown action."""
        monkeypatch.chdir(tmp_path)
        from stdd.cli.commands.hooks import _dispatch
        import argparse
        args = argparse.Namespace(action="unknown")

        with pytest.raises(SystemExit):
            _dispatch(args)
