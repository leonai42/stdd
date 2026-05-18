# STDD 故障排除指南 / Troubleshooting Guide

## 1. Windows GBK 终端 Unicode 乱码 / Windows GBK Terminal Unicode Garbled

**症状 / Symptom**：Windows 终端执行 `stdd` 命令时，Unicode 字符（emoji、中文）显示为乱码。
When running `stdd` commands in Windows terminal, Unicode characters (emoji, Chinese) appear garbled.

**原因 / Cause**：Windows 默认终端编码为 GBK，不支持 UTF-8 字符。
Windows default terminal encoding is GBK, which doesn't support UTF-8.

**解决方案 / Solution**：
1. 确保 `bin/stdd` 文件开头有 UTF-8 编码修复代码（V1.2.1+ 已内置）/ Ensure `bin/stdd` has UTF-8 fix at the top (built-in since V1.2.1)
2. 使用 Windows Terminal 替代 cmd.exe / Use Windows Terminal instead of cmd.exe
3. 执行 `chcp 65001` 临时切换为 UTF-8 代码页 / Run `chcp 65001` to temporarily switch to UTF-8

---

## 2. PYTHONPATH 路径问题 / PYTHONPATH Issue

**症状 / Symptom**：`python bin/stdd` 报 `ModuleNotFoundError: No module named 'stdd'`。

**原因 / Cause**：Python 无法找到 `stdd` 包。Python cannot find the `stdd` package.

**解决方案 / Solution**：
1. 确保在 STDD 项目根目录执行命令 / Run commands from the STDD project root
2. 检查 `bin/stdd` 是否包含 `sys.path.insert(0, ...)` 语句 / Check `bin/stdd` for `sys.path.insert(0, ...)`
3. 或设置环境变量 / Or set environment variable:
   - Windows: `set PYTHONPATH=.`
   - Unix: `export PYTHONPATH=.`

---

## 3. PyYAML 安装失败 / PyYAML Installation Failure

**症状 / Symptom**：执行 `stdd validate` 时报 `ModuleNotFoundError: No module named 'yaml'`。

**原因 / Cause**：PyYAML 未安装或安装到错误的 Python 版本。
PyYAML is not installed or installed for the wrong Python version.

**解决方案 / Solution**：
```bash
pip install pyyaml
# 或指定 Python 版本 / Or specify Python version
python3.10 -m pip install pyyaml
```
对于 Windows，可能需要先安装 Microsoft Visual C++ Build Tools。
On Windows, you may need to install Microsoft Visual C++ Build Tools first.

---

## 4. pytest 安装失败 / pytest Installation Failure

**症状 / Symptom**：运行 `pytest tests/` 时提示找不到命令。
`pytest` command not found when running tests.

**原因 / Cause**：pytest 未安装或不在 PATH 中。pytest not installed or not in PATH.

**解决方案 / Solution**：
```bash
pip install pytest pytest-cov
python -m pytest tests/ -v
```

---

## 5. change 目录冲突 / Change Directory Conflict

**症状 / Symptom**：`stdd new` 或 `stdd rollback` 报告"已存在"或"冲突"。
`stdd new` or `stdd rollback` reports "already exists" or "conflict".

**原因 / Cause**：目标目录已存在同名 change。
A change with the same name already exists in the target directory.

**解决方案 / Solution**：
1. 检查 `changes/` 和 `archive/` 目录 / Check `changes/` and `archive/` directories
2. 使用不同的 change 名称 / Use a different change name
3. 若需恢复，先删除或重命名冲突目录后重试 / Delete or rename the conflicting directory first

---

## 6. Skill 安装后不生效 / Skill Not Working After Install

**症状 / Symptom**：`stdd install claude-code` 后 `/stdd-understand` 无响应。
`/stdd-understand` has no response after `stdd install claude-code`.

**原因 / Cause**：Skill 文件未正确写入目标目录或 frontmatter 格式不匹配。
Skill file not correctly written or frontmatter format doesn't match.

**解决方案 / Solution**：
1. 检查 `.claude/skills/` 目录是否有对应的 `stdd-*/SKILL.md` 文件 / Check for `stdd-*/SKILL.md` files
2. 确保 SKILL.md 有正确的 YAML frontmatter（`---` 包裹的 name/description）/ Ensure valid YAML frontmatter
3. 重启 Claude Code 会话使 Skills 重新加载 / Restart Claude Code session to reload skills
4. 执行 `stdd install claude-code` 重新安装 / Re-run `stdd install claude-code`

---

## 7. archive 合并冲突 / Archive Merge Conflict

**症状 / Symptom**：`stdd archive` 输出"冲突警告: 以下 Requirement 已存在"。
`stdd archive` outputs "Conflict warning: the following Requirements already exist".

**原因 / Cause**：待合并的 spec 中包含与 `specs/` 中同名的 Requirement。
The spec being merged contains Requirements with the same name as those in `specs/`.

**解决方案 / Solution**：
1. 查看冲突报告中的 Requirement 名称 / Review conflicting Requirement names
2. 决定是否合并（系统将继续追加）或修改 spec 中的 Requirement 名称 / Decide whether to merge (system will append) or rename Requirements
3. 如果是要替换旧 Requirement，手动编辑 `specs/` 中的目标文件 / To replace old Requirements, manually edit the target file in `specs/`
