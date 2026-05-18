# STDD 扩展开发指南 / Extension Development Guide

> STDD 设计为可扩展框架，支持新增平台适配、开发语言规范和失败模式检查。
> STDD is designed as an extensible framework, supporting new platform adapters, language standards, and failure mode checks.

---

## 一、新增平台适配 / Adding a Platform Adapter

STDD 使用 Skill + frontmatter 模式支持多 AI 编程平台。
STDD supports multiple AI coding platforms through the Skill + frontmatter pattern.

### 步骤 / Steps

1. **在 `stdd/cli/commands/install.py` 中添加平台配置**：
   Add platform config in `stdd/cli/commands/install.py`:

```python
platform_map["new-platform"] = {
    "target_base": ".new-platform/skills",
    "description": "New Platform",
    "frontmatter_fn": _make_new_platform_frontmatter,
    "is_dir_per_skill": False,  # 或 True（取决于平台要求）/ or True (platform-dependent)
}
```

2. **定义 frontmatter 生成函数** / Define frontmatter generation function:

```python
def _make_new_platform_frontmatter(meta: dict) -> str:
    return f"""---
name: {meta['name']}
description: "{meta['description']}"
# 平台特有的 frontmatter 字段 / Platform-specific frontmatter fields
---
"""
```

3. **在 `SKILL_META` 中添加 keyword 配置**（如平台需要特定触发词）
   Add keyword config in `SKILL_META` if the platform needs specific trigger words.

4. **完成平台特有安装逻辑** / Complete platform-specific install logic.

### 现有平台参考 / Existing Platform Reference

| 平台 / Platform | 格式 / Format | 特点 / Characteristic |
|----------------|--------------|----------------------|
| **Claude Code** | directory-per-skill（`skill-name/SKILL.md`） | YAML frontmatter, `/` slash commands |
| **WorkBuddy** | `trigger_keywords` YAML frontmatter + home 目录 | Keyword matching trigger |
| **Trae** | flat `.trae/skills/` 目录结构 | `/` slash commands |
| **Cursor** | 单文件 `.cursor/rules/stdd.md` | Project rules auto-load |
| **Copilot** | 单文件 `.github/copilot-instructions.md` | Instructions auto-load |
| **Aider** | 单文件 `.aider.conf.yml` | Config-based |

---

## 二、新增开发语言规范 / Adding a Language Standard

STDD 通过 `.stdd/standards/<language>.md` 提供语言特定的开发规范。
STDD provides language-specific development standards via `.stdd/standards/<language>.md`.

### 步骤 / Steps

1. **创建规范文件** / Create standard file: `.stdd/standards/<language>.md`

2. **规范文件应包含** / The standard file should cover:
   - 代码风格（命名规范、缩进、行宽）/ Code style (naming, indentation, line width)
   - 测试框架和约定（pytest/unittest/jest 等）/ Test framework & conventions
   - Lint 工具和配置（ruff/eslint/golangci-lint）/ Lint tools & config
   - 类型注解要求 / Type annotation requirements
   - 文件组织约定 / File organization conventions
   - 常见反模式和最佳实践 / Common anti-patterns & best practices

3. **在 `config.d/quality.yaml` 中配置语言特定的质量命令**：
   Configure language-specific quality commands in `config.d/quality.yaml`:

```yaml
quality:
  test: "pytest tests/ -v"       # Python
  # test: "go test ./..."        # Go
  # test: "npm test"             # JavaScript
  lint: "ruff check app/ tests/" # Python
  # lint: "golangci-lint run"    # Go
```

4. **参考 `standards/python.md`** 了解完整格式。
   See `standards/python.md` for complete format reference.

---

## 三、新增自定义失败模式检查 / Adding a Failure Mode Check

STDD Phase 5 包含 11 类故障模式检查。可通过 Python 代码扩展。
STDD Phase 5 includes 11 failure mode checks, extensible via Python code.

### 步骤 / Steps

1. **在 `stdd/cli/commands/validate.py` 中添加检查函数**：
   Add check function in `stdd/cli/commands/validate.py`:

```python
def _check_custom_failure(specs_dir: Path, test_plan: Path) -> list:
    """检查自定义失败模式 / Check custom failure mode."""
    warnings = []
    # 实现检查逻辑 / Implement check logic
    # ...
    return warnings
```

2. **在 `cmd_validate` 中调用新函数** / Call the new function in `cmd_validate`.

3. **更新核心 Skill `verify.md`**，在质量检查清单中增加新项。
   Update core Skill `verify.md` to add the new check item.

4. **更新模板 `test-report.md`**（如需在报告中体现新检查）。
   Update template `test-report.md` if the new check should appear in reports.

### 现有 11 类故障模式 / Existing 11 Failure Modes

| # | 类别 / Category | 检查位置 / Check Location |
|---|----------------|--------------------------|
| a | 缺失必需文件 / Missing required files | validate.py |
| b | .stdd.yaml 无效 Phase / Invalid phase in .stdd.yaml | validate.py |
| c | Spec 格式不完整（GIVEN/WHEN/THEN）/ Incomplete spec format | validate.py |
| d | TC-ID 重复 / Duplicate TC-ID | validate.py |
| e | TC 案例数不足 / Insufficient TC cases | validate.py |
| f | THEN 未使用 SHALL / THEN missing SHALL | validate.py |
| g | AND 数量超限（>5）/ Excessive AND clauses | validate.py |
| h | archive 合并冲突 / Archive merge conflict | archive.py |
| i | 测试执行失败 / Test execution failure | pytest |
| j | 覆盖率不足 / Insufficient coverage | pytest-cov |
| k | 设计偏差未记录 / Undocumented design deviations | verify.md Skill |

---

## 四、新增 CLI 命令 / Adding a CLI Command

### 步骤 / Steps

1. **创建命令模块** / Create command module: `stdd/cli/commands/<command>.py`

```python
import argparse

def cmd_<command>(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    logger = get_logger()
    # 命令逻辑 / Command logic
```

2. **在 `stdd/cli/__init__.py` 中注册** / Register in `stdd/cli/__init__.py`:
   - 添加 subparser / Add subparser: `p_cmd = subparsers.add_parser("cmd", ...)`
   - 在 `commands` dict 中添加映射 / Add mapping in `commands` dict

3. **编写测试** / Write tests: `tests/commands/test_<command>.py`

4. **更新文档**（README.md, AGENTS.md 等）/ Update documentation.

---

## 五、目录结构总览 / Directory Overview

```
stdd/cli/
├── __init__.py          # CLI 入口调度 / Entry point dispatcher
├── commands/            # 子命令模块 / Subcommand modules
│   ├── init.py
│   ├── install.py
│   ├── new_cmd.py
│   ├── validate.py
│   ├── status.py
│   ├── archive.py
│   ├── trace.py
│   ├── diff.py
│   ├── rollback.py
│   └── abort.py
├── finder.py            # change 目录查找 / Change directory finder
├── utils.py             # 工具函数 / Utility functions
└── ...

tests/
├── commands/
│   ├── test_init.py
│   ├── test_install.py
│   └── ...
└── ...
```
