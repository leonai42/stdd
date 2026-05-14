"""测试 utils 模块（logging, config, encoding）。"""
import pytest
import logging
from pathlib import Path

from stdd.cli.utils import (
    setup_logging,
    get_logger,
    get_stdd_source,
    read_config,
    fix_windows_encoding,
)


def test_setup_logging_default():
    """默认日志级别为 WARNING。"""
    setup_logging(0)
    logger = get_logger()
    assert logger.level == logging.WARNING


def test_setup_logging_info():
    """-v 一次为 INFO 级别。"""
    setup_logging(1)
    logger = get_logger()
    assert logger.level == logging.INFO


def test_setup_logging_debug():
    """-vv 为 DEBUG 级别。"""
    setup_logging(2)
    logger = get_logger()
    assert logger.level == logging.DEBUG


def test_get_stdd_source():
    """能找到 STDD 项目根目录（存在 STDD.md）。"""
    source = get_stdd_source()
    assert source.exists()
    assert (source / "STDD.md").exists()
    assert (source / "bin" / "stdd").exists()


def test_read_config_from_config_d():
    """从 config.d/ 读取配置。"""
    config = read_config(Path.cwd())
    assert "project" in config
    assert "stdd_version" in config
    assert "gates" in config
    assert "long_range" in config


def test_read_config_legacy_fallback(tmp_path: Path):
    """config.d/ 不存在时 fallback 到 config.yaml。"""
    import yaml
    (tmp_path / ".stdd").mkdir()
    legacy = {"project": {"name": "test"}, "stdd_version": "1.0"}
    with open(tmp_path / ".stdd" / "config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(legacy, f)
    config = read_config(tmp_path)
    assert config["project"]["name"] == "test"
    assert config["stdd_version"] == "1.0"


def test_read_config_non_dict_yaml(temp_project: Path, monkeypatch):
    """config.d/ 中非 dict 文件被跳过并警告。"""
    from stdd.cli.utils import read_config, setup_logging
    setup_logging(0)
    (temp_project / ".stdd" / "config.d").mkdir(parents=True, exist_ok=True)
    # 创建一个包含 YAML 列表的配置文件
    (temp_project / ".stdd" / "config.d" / "list.yaml").write_text("- item1\n- item2\n", encoding="utf-8")
    # 同时创建一个有效的 dict 配置
    (temp_project / ".stdd" / "config.d" / "valid.yaml").write_text("key: value\n", encoding="utf-8")

    config = read_config(temp_project)
    # 有效配置应该被加载
    assert config.get("key") == "value"
    # 列表文件被跳过
    assert "item1" not in config


def test_fix_windows_encoding():
    """编码修复函数可正常调用。"""
    fix_windows_encoding()  # 不应抛出异常
