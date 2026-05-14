# STDD 扩展开发指南

STDD 设计为可扩展框架，支持新增平台适配、开发语言规范和失败模式检查。

## 一、新增平台适配

STDD 使用 Skill + frontmatter 模式支持多 AI 编程平台。

### 步骤

1. **在 `stdd/cli/commands/install.py` 中添加平台配置**：

```python
platform_map["new-platform"] = {
    "target_base": ".new-platform/skills",
    "description": "New Platform",
    "frontmatter_fn": _make_new_platform_frontmatter,
    "is_dir_per_skill": False,  # 或 True（取决于平台要求）
}
```

2. **定义 frontmatter 生成函数**：

```python
def _make_new_platform_frontmatter(meta: dict) -> str:
    return f"""---
name: {meta['name']}
description: "{meta['description']}"
# 平台特有的 frontmatter 字段
---
"""
```

3. **在 `SKILL_META` 中添加 keyword 配置**（如平台需要特定触发词）

4. **在 `stdd/cli/commands/install.py` 中完成平台配置**（如有平台特有安装逻辑）

### 现有平台参考
- **Claude Code**：directory-per-skill 格式（`skill-name/SKILL.md`）
- **WorkBuddy**：`trigger_keywords` YAML frontmatter + home 目录安装
- **Trae**：flat `.trae/skills/` 目录结构
- **Cursor**：单文件 `.cursor/rules/stdd.md`

---

## 二、新增开发语言规范

STDD 通过 `.stdd/standards/<language>.md` 提供语言特定的开发规范。

### 步骤

1. **创建规范文件**：`.stdd/standards/<language>.md`

2. **规范文件应包含**：
   - 代码风格（命名规范、缩进、行宽）
   - 测试框架和约定（pytest/unittest/jest 等）
   - Lint 工具和配置（ruff/eslint/golangci-lint）
   - 类型注解要求
   - 文件组织约定
   - 常见反模式和最佳实践

3. **在 `config.d/quality.yaml` 中配置语言特定的质量命令**：

```yaml
quality:
  test: "pytest tests/ -v"       # Python
  # test: "go test ./..."        # Go
  # test: "npm test"             # JavaScript
  lint: "ruff check app/ tests/" # Python
  # lint: "golangci-lint run"    # Go
```

4. **参考 `standards/python.md`** 了解完整格式

---

## 三、新增自定义失败模式检查

STDD Phase 5 包含 11 类故障模式检查。可通过 Python 代码扩展。

### 步骤

1. **在 `stdd/cli/commands/validate.py` 中添加检查函数**：

```python
def _check_custom_failure(specs_dir: Path, test_plan: Path) -> list:
    """检查自定义失败模式。"""
    warnings = []
    # 实现检查逻辑
    # ...
    return warnings
```

2. **在 `cmd_validate` 中调用新函数**

3. **更新核心 Skill `verify.md`**，在质量检查清单中增加新项

4. **更新模板 `test-report.md`**（如需在报告中体现新检查）

### 现有 11 类故障模式

| # | 类别 | 检查位置 |
|---|------|----------|
| a | 缺失必需文件 | validate.py |
| b | .stdd.yaml 无效 Phase | validate.py |
| c | Spec 格式不完整（GIVEN/WHEN/THEN） | validate.py |
| d | TC-ID 重复 | validate.py |
| e | TC 案例数不足 | validate.py |
| f | THEN 未使用 SHALL | validate.py |
| g | AND 数量超限（>5） | validate.py |
| h | archive 合并冲突 | archive.py |
| i | 测试执行失败 | pytest |
| j | 覆盖率不足 | pytest-cov |
| k | 设计偏差未记录 | verify.md Skill |

---

## 四、新增 CLI 命令

### 步骤

1. **创建命令模块**：`stdd/cli/commands/<command>.py`

```python
import argparse

def cmd_<command>(args: argparse.Namespace) -> None:
    from ..finder import find_change_dir
    from ..utils import get_logger
    logger = get_logger()
    # 命令逻辑
```

2. **在 `stdd/cli/__init__.py` 中注册**：
   - 添加 subparser：`p_cmd = subparsers.add_parser("cmd", ...)`
   - 在 `commands` dict 中添加映射

3. **编写测试**：`tests/commands/test_<command>.py`

4. **更新文档**（README.md, AGENTS.md 等）
