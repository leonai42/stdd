"""STDD upgrade CLI — version upgrade management (V2.9)."""

import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path


def _read_version_yaml(project_root: Path) -> dict:
    """Read .stdd/version.yaml, return empty dict if not found."""
    version_file = project_root / ".stdd" / "version.yaml"
    if version_file.exists():
        import yaml
        data = yaml.safe_load(version_file.read_text(encoding="utf-8"))
        return data or {}
    return {}


def _write_version_yaml(project_root: Path, data: dict) -> None:
    """Write .stdd/version.yaml."""
    import yaml
    version_file = project_root / ".stdd" / "version.yaml"
    version_file.write_text(
        yaml.dump(data, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )


def _registry_path() -> Path:
    """Get path to global projects registry."""
    return Path.home() / ".stdd" / "projects.yaml"


def _read_registry() -> dict:
    """Read global projects registry, create if not found."""
    import yaml
    rp = _registry_path()
    if rp.exists():
        data = yaml.safe_load(rp.read_text(encoding="utf-8"))
        return data or {"registry_version": "1.0", "projects": []}
    return {"registry_version": "1.0", "projects": []}


def _write_registry(data: dict) -> None:
    """Write global projects registry."""
    import yaml
    rp = _registry_path()
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(
        yaml.dump(data, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )


def _register_project(project_root: Path, version: str, locked: bool = False) -> None:
    """Add/update project entry in global registry."""
    data = _read_registry()
    proj_path = str(project_root.resolve())
    now = datetime.now().strftime("%Y-%m-%d")

    for proj in data.get("projects", []):
        if proj.get("path") == proj_path:
            proj["version"] = version
            proj["locked"] = locked
            proj["last_seen"] = now
            _write_registry(data)
            return

    data.setdefault("projects", []).append({
        "path": proj_path,
        "version": version,
        "locked": locked,
        "last_seen": now,
        "name": project_root.name,
    })
    _write_registry(data)


def _backup_project_files(project_root: Path, old_version: str) -> Path:
    """Backup current STDD files before upgrade. Returns backup dir path."""
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    backup_dir = project_root / ".stdd" / "backup" / f"{old_version}-{ts}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    dirs_to_backup = [".stdd/skills", ".stdd/templates", ".stdd/standards", ".stdd/config.d", ".stdd/experiences", "canonical"]
    for d in dirs_to_backup:
        src = project_root / d
        if src.is_dir():
            dst = backup_dir / d
            dst.mkdir(parents=True, exist_ok=True)
            for f in src.rglob("*"):
                if f.is_file():
                    rel = f.relative_to(src)
                    target = dst / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, target)

    version_file = project_root / ".stdd" / "version.yaml"
    if version_file.exists():
        shutil.copy2(version_file, backup_dir / "version.yaml")

    return backup_dir


def _merge_project_yaml(project_root: Path, stdd_source: Path) -> None:
    """Merge source project.yaml into project, preserving identity keys."""
    import yaml
    preserve_keys = {"project", "paths"}

    src_file = stdd_source / ".stdd" / "config.d" / "project.yaml"
    dst_file = project_root / ".stdd" / "config.d" / "project.yaml"

    if not src_file.exists():
        return

    src_data = yaml.safe_load(src_file.read_text(encoding="utf-8")) or {}
    dst_data = {}
    if dst_file.exists():
        dst_data = yaml.safe_load(dst_file.read_text(encoding="utf-8")) or {}

    # Start with source, preserve project-specific keys
    merged = dict(src_data)
    for key in preserve_keys:
        if key in dst_data:
            merged[key] = dst_data[key]

    merged["stdd_version"] = src_data.get("stdd_version", merged.get("stdd_version"))

    dst_file.write_text(
        yaml.dump(merged, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )


def _detect_installed_platforms(project_root: Path) -> list:
    """Detect which platforms are installed in the project."""
    platforms = []
    if (project_root / ".claude" / "skills").is_dir():
        platforms.append("claude-code")
    if (project_root / ".workbuddy" / "skills").is_dir():
        platforms.append("workbuddy")
    if (project_root / ".trae" / "skills").is_dir():
        platforms.append("trae")
    if (project_root / ".cursor" / "rules" / "stdd.md").exists():
        platforms.append("cursor")
    if (project_root / ".opencode" / "skills").is_dir():
        platforms.append("opencode")
    return platforms


def _reinstall_platforms(project_root: Path, stdd_source: Path, platforms: list, dry_run: bool = False) -> None:
    """Reinstall STDD skills for detected platforms."""
    if not platforms:
        return

    from ..commands.install import cmd_install

    for platform in platforms:
        if dry_run:
            print(f"   [DRY-RUN] 重新安装平台: {platform}")
            continue
        print(f"   重新安装平台: {platform}")
        ns = argparse.Namespace(
            command="install", platform=platform, dry_run=False, verbose=0
        )
        old_cwd = os.getcwd()
        try:
            os.chdir(str(project_root))
            cmd_install(ns)
        finally:
            os.chdir(old_cwd)


def _cmd_check_current(args: argparse.Namespace) -> None:
    """Check version gap for current project."""
    from ..utils import get_source_version, get_project_version, compare_versions
    project_root = Path.cwd()

    source_ver = get_source_version()
    proj_ver = get_project_version(project_root)

    if not source_ver:
        print("  无法检测 STDD 源版本")
        return

    if not proj_ver:
        proj_ver = "未知"
    version_data = _read_version_yaml(project_root)
    locked = version_data.get("locked", False)

    print(f"  STDD 源版本:  {source_ver}")
    print(f"  项目版本:    {proj_ver}")
    if locked:
        print("  状态:        🔒 已锁定")

    if proj_ver == "未知":
        print("  ⚠️ 无法确定项目版本，建议执行 stdd upgrade")
    elif compare_versions(proj_ver, source_ver) < 0:
        print("  ⚠️ 有新版本可用。运行 'stdd upgrade' 升级")
    else:
        print("  ✅ 已是最新版本")


def _cmd_upgrade_current(args: argparse.Namespace) -> None:
    """Upgrade current project."""
    from ..utils import get_source_version, get_project_version, compare_versions, get_stdd_source
    project_root = Path.cwd()
    dry_run = getattr(args, "dry_run", False)
    skip_confirm = getattr(args, "yes", False)

    source_ver = get_source_version()
    proj_ver = get_project_version(project_root)
    stdd_source = get_stdd_source()

    if not source_ver:
        print("  无法检测 STDD 源版本，请从 STDD 仓库运行")
        return

    if not proj_ver:
        proj_ver = "0.0.0"

    # Check lock
    version_data = _read_version_yaml(project_root)
    if version_data.get("locked", False):
        print(f"  项目已锁定在版本 {proj_ver}。使用 'stdd upgrade --unlock' 解锁后再升级。")
        return

    if compare_versions(proj_ver, source_ver) >= 0:
        print(f"  项目已是最新版本 ({proj_ver})，无需升级")
        return

    if dry_run:
        print("  [DRY-RUN] 升级计划:")
        print(f"    当前版本: {proj_ver} → 目标版本: {source_ver}")
        from ..commands.init import FILES_TO_COPY
        backup_dir = project_root / ".stdd" / "backup" / f"{proj_ver}-<timestamp>"
        print(f"    备份目录: {backup_dir}")
        print(f"    将同步 {len(FILES_TO_COPY)} 个文件")
        platforms = _detect_installed_platforms(project_root)
        print(f"    检测到平台: {platforms or '无'}")
        print("  [DRY-RUN] 文件系统未发生变化")
        return

    # Confirm
    if not skip_confirm:
        print(f"  当前版本: {proj_ver} → 目标版本: {source_ver}")
        resp = input("  确认升级? [y/N] ").strip().lower()
        if resp not in ("y", "yes"):
            print("  已取消")
            return

    # Backup
    print(f"  备份到 {_backup_project_files(project_root, proj_ver)}")

    # Sync files
    from ..commands.init import FILES_TO_COPY, DIRS
    for d in DIRS:
        (project_root / d).mkdir(parents=True, exist_ok=True)

    copied = 0
    for f in FILES_TO_COPY:
        src = stdd_source / f
        dst = project_root / f
        if src.exists():
            if f in (".stdd/config.d/project.yaml",):
                _merge_project_yaml(project_root, stdd_source)
            else:
                shutil.copy2(src, dst)
            copied += 1

    # Reinstall platforms
    platforms = _detect_installed_platforms(project_root)
    _reinstall_platforms(project_root, stdd_source, platforms)

    # Write version
    now = datetime.now().isoformat()
    installed_at = version_data.get("installed_at", now)
    _write_version_yaml(project_root, {
        "stdd_version": source_ver,
        "locked": False,
        "installed_at": installed_at,
        "upgraded_at": now,
        "source_path": str(stdd_source.resolve()),
    })

    # Update registry
    _register_project(project_root, source_ver)

    print(f"  ✅ 升级完成: {proj_ver} → {source_ver} ({copied} 个文件)")


def _cmd_check_all(args: argparse.Namespace) -> None:
    """Show version matrix for all registered projects."""
    from ..utils import get_source_version, compare_versions
    source_ver = get_source_version() or "未知"

    data = _read_registry()
    projects = data.get("projects", [])

    if not projects:
        print("  注册表中无项目。在各项目中运行 'stdd upgrade' 以注册。")
        return

    print(f"  STDD 最新版本: {source_ver}")
    print()
    print(f"  {'项目':<25} {'当前版本':<10} {'状态':<10}")
    print(f"  {'-'*25} {'-'*10} {'-'*10}")

    for proj in projects:
        proj_path = Path(proj["path"])
        status = ""
        if not proj_path.exists():
            status = "[已删除]"
        elif proj.get("locked", False):
            status = "🔒 锁定"
        elif compare_versions(proj.get("version", "0"), source_ver) < 0:
            status = "⚠️ 可升级"
        else:
            status = "✅ 最新"
        print(f"  {proj['name']:<25} {proj.get('version', '?'):<10} {status:<10}")


def _cmd_upgrade_all(args: argparse.Namespace) -> None:
    """Upgrade all registered non-locked projects."""
    from ..utils import get_source_version, compare_versions
    source_ver = get_source_version()
    if not source_ver:
        print("  无法检测 STDD 源版本")
        return

    data = _read_registry()
    projects = data.get("projects", [])
    skip_confirm = getattr(args, "yes", False)

    upgraded = 0
    for proj in projects:
        proj_path = Path(proj["path"])
        if not proj_path.exists():
            print(f"  ⏭️ {proj['name']}: 路径不存在，跳过")
            continue
        if proj.get("locked", False):
            print(f"  🔒 {proj['name']}: 已锁定，跳过")
            continue
        if compare_versions(proj.get("version", "0"), source_ver) >= 0:
            continue

        print(f"\n  ⬆️ {proj['name']} ({proj['version']} → {source_ver})")
        # Simulate args for per-project upgrade
        sub_args = argparse.Namespace(
            command="upgrade", check=False, all=False,
            lock=False, unlock=False,
            dry_run=False, verbose=0,
            yes=skip_confirm,
        )
        old_cwd = os.getcwd()
        try:
            os.chdir(str(proj_path))
            _cmd_upgrade_current(sub_args)
        finally:
            os.chdir(old_cwd)
        upgraded += 1

    print(f"\n  ✅ 升级完成: {upgraded} 个项目")


def _cmd_lock_project(args: argparse.Namespace) -> None:
    """Lock current project at current version."""
    from ..utils import get_project_version
    project_root = Path.cwd()
    proj_ver = get_project_version(project_root) or "0.0.0"

    data = _read_version_yaml(project_root)
    now = datetime.now().isoformat()
    data["stdd_version"] = proj_ver
    data["locked"] = True
    if "installed_at" not in data:
        data["installed_at"] = now
    _write_version_yaml(project_root, data)
    _register_project(project_root, proj_ver, locked=True)
    print(f"  🔒 项目已锁定在版本 {proj_ver}")


def _cmd_unlock_project(args: argparse.Namespace) -> None:
    """Unlock current project."""
    from ..utils import get_project_version
    project_root = Path.cwd()
    proj_ver = get_project_version(project_root) or "0.0.0"

    data = _read_version_yaml(project_root)
    data["locked"] = False
    _write_version_yaml(project_root, data)
    _register_project(project_root, proj_ver, locked=False)
    print(f"  🔓 项目已解锁 (版本 {proj_ver})")


def cmd_upgrade(args: argparse.Namespace) -> None:
    """Dispatch upgrade command based on flags."""
    if args.lock:
        _cmd_lock_project(args)
    elif args.unlock:
        _cmd_unlock_project(args)
    elif args.check and args.all:
        _cmd_check_all(args)
    elif args.check:
        _cmd_check_current(args)
    elif args.all:
        _cmd_upgrade_all(args)
    else:
        _cmd_upgrade_current(args)
