import logging
import sys
import io
from pathlib import Path
from typing import Optional, Dict, Any

_logger: Optional[logging.Logger] = None
STDD_SOURCE: Optional[Path] = None


def setup_logging(verbose: int = 0) -> None:
    global _logger
    _logger = logging.getLogger("stdd")
    if verbose == 0:
        _logger.setLevel(logging.WARNING)
    elif verbose == 1:
        _logger.setLevel(logging.INFO)
    else:
        _logger.setLevel(logging.DEBUG)
    if not _logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        _logger.addHandler(handler)


def get_logger() -> logging.Logger:
    global _logger
    if _logger is None:
        setup_logging(0)
    return _logger


def get_stdd_source() -> Path:
    global STDD_SOURCE
    if STDD_SOURCE is not None:
        return STDD_SOURCE
    p = Path(__file__).resolve().parent
    while True:
        if (p / "STDD.md").exists() and (p / "bin").is_dir():
            return p
        if p.parent == p:
            raise RuntimeError("Cannot find STDD source root (STDD.md not found)")
        p = p.parent


def read_config(project_root: Path) -> Dict[str, Any]:
    config: Dict[str, Any] = {}
    config_d = project_root / ".stdd" / "config.d"
    if config_d.is_dir():
        for cfg_file in sorted(config_d.glob("*.yaml")):
            import yaml
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    config.update(data)
                else:
                    get_logger().warning("config.d/%s 不是 dict 类型，已跳过", cfg_file.name)
        if config:
            get_logger().info("从 config.d/ 加载配置 (%d 个文件)", len(list(config_d.glob("*.yaml"))))
            legacy = project_root / ".stdd" / "config.yaml"
            if legacy.exists():
                get_logger().warning("检测到旧 config.yaml，建议删除（config.d/ 已生效）")
            return config
    legacy = project_root / ".stdd" / "config.yaml"
    if legacy.exists():
        import yaml
        with open(legacy, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        get_logger().info("从 config.yaml 加载配置（向后兼容）")
    return config


def fix_windows_encoding() -> None:
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ── Version utilities (V2.9) ──

def get_source_version() -> Optional[str]:
    """Read stdd_version from STDD source's config.d/project.yaml."""
    try:
        source = get_stdd_source()
        config = read_config(source)
        return config.get("stdd_version")
    except Exception:
        return None


def get_project_version(project_root: Path) -> Optional[str]:
    """Read version from .stdd/version.yaml (preferred) or fallback to project.yaml."""
    version_file = project_root / ".stdd" / "version.yaml"
    if version_file.exists():
        try:
            import yaml
            data = yaml.safe_load(version_file.read_text(encoding="utf-8"))
            if data and "stdd_version" in data:
                return data["stdd_version"]
        except Exception:
            pass
    # Fallback to legacy project.yaml
    config = read_config(project_root)
    return config.get("stdd_version")


def compare_versions(v1: str, v2: str) -> int:
    """Compare semantic version strings. Returns -1, 0, or 1.

    Supports '2.7', '2.8.0', 'v2.9' style formats.
    """
    def _parse(v: str) -> tuple:
        v = v.strip().lstrip("v").lstrip("V").strip("'").strip('"')
        parts = v.split(".")
        return tuple(int(x) for x in parts if x.isdigit())

    a = _parse(v1)
    b = _parse(v2)
    max_len = max(len(a), len(b))
    a = a + (0,) * (max_len - len(a))
    b = b + (0,) * (max_len - len(b))
    if a < b:
        return -1
    elif a > b:
        return 1
    return 0


def try_version_check(project_root: Path) -> None:
    """Check project vs source version, print notice if outdated.
    Never raises — any exception is silently ignored.
    """
    try:
        if not (project_root / ".stdd").is_dir():
            return

        # Check lock status
        version_file = project_root / ".stdd" / "version.yaml"
        if version_file.exists():
            import yaml
            data = yaml.safe_load(version_file.read_text(encoding="utf-8"))
            if data and data.get("locked", False):
                return  # Locked project — skip

        source_ver = get_source_version()
        proj_ver = get_project_version(project_root)

        if source_ver and proj_ver and compare_versions(proj_ver, source_ver) < 0:
            print(f"  [STDD] 有新版本可用: {source_ver} (当前: {proj_ver})")
            print("  [STDD] 运行 'stdd upgrade --check' 查看详情，"
                  "或 'stdd upgrade --lock' 锁定版本")
    except Exception:
        pass  # Never block execution
