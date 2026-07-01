"""测试 cmd_install 命令。"""
import argparse
import pytest
from pathlib import Path

from stdd.cli.commands.install import cmd_install


def test_install_unsupported_platform(temp_project: Path, monkeypatch):
    """不支持的平台被拒绝。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="unknown", dry_run=False, verbose=0)
    with pytest.raises(SystemExit):
        cmd_install(args)


def test_install_claude_code(temp_project: Path, monkeypatch):
    """安装到 Claude Code。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="claude-code", dry_run=False, verbose=0)
    cmd_install(args)
    # 检查目标目录
    target = temp_project / ".claude" / "skills"
    assert target.exists()
    skills = list(target.iterdir())
    assert len(skills) >= 1


def test_install_cursor(temp_project: Path, monkeypatch):
    """安装到 Cursor（单文件模式）。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="cursor", dry_run=False, verbose=0)
    cmd_install(args)
    target = temp_project / ".cursor" / "rules" / "stdd.md"
    assert target.exists()


def test_install_trae(temp_project: Path, monkeypatch):
    """安装到 Trae。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="trae", dry_run=False, verbose=0)
    cmd_install(args)
    target = temp_project / ".trae" / "skills"
    assert target.exists()


def test_install_dry_run(temp_project: Path, monkeypatch, capsys):
    """--dry-run 预览但不安装文件。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="claude-code", dry_run=True, verbose=0)
    cmd_install(args)
    captured = capsys.readouterr()
    assert "[DRY-RUN]" in captured.out
    # 未创建 skills 目录
    target = temp_project / ".claude" / "skills"
    assert not target.exists()


def test_install_opencode(temp_project: Path, monkeypatch):
    """安装到 OpenCode。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="opencode", dry_run=False, verbose=0)
    cmd_install(args)
    target = temp_project / ".opencode" / "skills"
    assert target.exists()
    skills = list(target.iterdir())
    assert len(skills) >= 1
    # 每个 skill 应该是子目录，包含 SKILL.md
    for skill_dir in skills:
        assert skill_dir.is_dir()
        assert (skill_dir / "SKILL.md").exists()


def test_install_workbuddy(temp_project: Path, monkeypatch):
    """安装到 WorkBuddy。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="workbuddy", dry_run=False, verbose=0)
    # WorkBuddy 安装到 HOME 目录，需要 mock
    from unittest.mock import patch
    with patch('pathlib.Path.home', return_value=temp_project):
        cmd_install(args)
    target = temp_project / ".workbuddy" / "skills"
    assert target.exists()


# ── V2.9.5: skill-version-check-upgrade tests ──

def test_skill_meta_has_upgrade_entry():
    """TC-PSI-001: SKILL_META 包含 upgrade 条目且字段完整。"""
    from stdd.cli.commands.install import SKILL_META
    assert "upgrade" in SKILL_META
    meta = SKILL_META["upgrade"]
    assert meta["name"] == "stdd-upgrade"
    assert "description" in meta
    assert "keywords" in meta
    assert "stdd-upgrade" in meta["keywords"]


def test_install_frontmatter_has_stdd_version(temp_project: Path, monkeypatch):
    """TC-PSI-002: 安装生成的 SKILL.md frontmatter 包含 stdd_version 字段。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="claude-code", dry_run=False, verbose=0)
    cmd_install(args)
    # Read one generated SKILL.md and check frontmatter
    skill_dir = temp_project / ".claude" / "skills" / "stdd-understand"
    assert skill_dir.is_dir()
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists()
    content = skill_file.read_text(encoding="utf-8")
    assert "stdd_version:" in content
    # The version should be a valid semver-like string
    import re
    match = re.search(r'stdd_version:\s*"([\d.]+)"', content)
    assert match is not None, f"stdd_version not found in frontmatter:\n{content[:300]}"
    version = match.group(1)
    parts = version.split(".")
    assert len(parts) >= 2, f"Invalid version format: {version}"


# ── V2.10: platform-codex tests ──

def test_codex_in_platform_map():
    """TC-CODEX-001: platform_map 包含 codex 条目且配置完整。"""
    from stdd.cli.commands.install import cmd_install
    # Access platform_map via the function's closure
    import inspect
    source = inspect.getsource(cmd_install)
    assert '"codex"' in source or "'codex'" in source, \
        "platform_map should contain 'codex' key"

    # Direct import check
    import stdd.cli.commands.install as install_mod
    # Re-read the module source to check platform_map
    import ast
    tree = ast.parse(inspect.getsource(install_mod))
    platform_map_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key in node.keys:
                if isinstance(key, ast.Constant) and key.value == "codex":
                    platform_map_found = True
                    break
    assert platform_map_found, "platform_map should contain 'codex' key"


def test_install_codex_creates_structure(temp_project: Path, monkeypatch):
    """TC-CODEX-002: stdd install codex 创建 .codex/skills/ 目录结构。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="codex", dry_run=False, verbose=0)
    cmd_install(args)
    target = temp_project / ".codex" / "skills"
    assert target.exists(), f".codex/skills/ not created at {target}"
    skills = list(target.iterdir())
    assert len(skills) >= 1, "Should have at least 1 skill directory"
    # Each skill should be a subdirectory with SKILL.md
    for skill_dir in skills:
        assert skill_dir.is_dir(), f"{skill_dir} should be a directory"
        skill_file = skill_dir / "SKILL.md"
        assert skill_file.exists(), f"{skill_file} should exist"


def test_codex_frontmatter_format(temp_project: Path, monkeypatch):
    """TC-CODEX-003: Codex skill frontmatter 格式与 claude-code 一致。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="codex", dry_run=False, verbose=0)
    cmd_install(args)
    skill_dir = temp_project / ".codex" / "skills" / "stdd-understand"
    assert skill_dir.is_dir()
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.exists()
    content = skill_file.read_text(encoding="utf-8")
    # Should have YAML frontmatter with name, description, stdd_version
    assert "name: stdd-understand" in content
    assert "description:" in content
    assert "stdd_version:" in content
    import re
    match = re.search(r'stdd_version:\s*"([\d.]+)"', content)
    assert match is not None, f"stdd_version not found in frontmatter:\n{content[:300]}"


def test_install_codex_dry_run(temp_project: Path, monkeypatch, capsys):
    """TC-CODEX-004: codex --dry-run 预览但不创建文件。"""
    monkeypatch.chdir(temp_project)
    args = argparse.Namespace(platform="codex", dry_run=True, verbose=0)
    cmd_install(args)
    captured = capsys.readouterr()
    assert "[DRY-RUN]" in captured.out
    assert "OpenAI Codex CLI" in captured.out or "codex" in captured.out.lower()
    target = temp_project / ".codex" / "skills"
    assert not target.exists(), "dry-run should not create files"


def test_all_platforms_include_upgrade_skill(temp_project: Path, monkeypatch, capsys):
    """TC-PSI-003: 所有平台的 dry-run install 输出中包含 upgrade 技能。"""
    platforms = ["claude-code", "opencode", "trae", "workbuddy", "codex"]
    for platform in platforms:
        monkeypatch.chdir(temp_project)
        args = argparse.Namespace(platform=platform, dry_run=True, verbose=0)
        if platform == "workbuddy":
            from unittest.mock import patch
            with patch('pathlib.Path.home', return_value=temp_project):
                cmd_install(args)
        else:
            cmd_install(args)
        captured = capsys.readouterr()
        output = captured.out
        # upgrade skill should appear in the dry-run output
        assert "stdd-upgrade" in output or "upgrade" in output, \
            f"Platform {platform}: upgrade skill not found in dry-run output:\n{output}"
