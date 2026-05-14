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
    if sys.stdout.encoding != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
