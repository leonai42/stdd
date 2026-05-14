# STDD 故障排除指南

## 1. Windows GBK 终端 Unicode 乱码

**症状**：Windows 终端执行 `stdd` 命令时，Unicode 字符（emoji、中文）显示为乱码。

**原因**：Windows 默认终端编码为 GBK，不支持 UTF-8 字符。

**解决方案**：
1. 确保 `bin/stdd` 文件开头有 UTF-8 编码修复代码（V1.2.1+ 已内置）
2. 使用 Windows Terminal 替代 cmd.exe
3. 执行 `chcp 65001` 临时切换为 UTF-8 代码页

---

## 2. PYTHONPATH 路径问题

**症状**：`python bin/stdd` 报 `ModuleNotFoundError: No module named 'stdd'`。

**原因**：Python 无法找到 `stdd` 包。

**解决方案**：
1. 确保在 STDD 项目根目录执行命令
2. 检查 `bin/stdd` 是否包含 `sys.path.insert(0, ...)` 语句
3. 或设置环境变量：`set PYTHONPATH=.` (Windows) / `export PYTHONPATH=.` (Unix)

---

## 3. PyYAML 安装失败

**症状**：执行 `stdd validate` 时报 `ModuleNotFoundError: No module named 'yaml'`。

**原因**：PyYAML 未安装或安装到错误的 Python 版本。

**解决方案**：
```bash
pip install pyyaml
# 或指定 Python 版本
python3.10 -m pip install pyyaml
```
对于 Windows，可能需要先安装 Microsoft Visual C++ Build Tools。

---

## 4. pytest 安装失败

**症状**：运行 `pytest tests/` 时提示找不到命令。

**原因**：pytest 未安装或不在 PATH 中。

**解决方案**：
```bash
pip install pytest pytest-cov
python -m pytest tests/ -v
```

---

## 5. change 目录冲突

**症状**：`stdd new` 或 `stdd rollback` 报告"已存在"或"冲突"。

**原因**：目标目录已存在同名 change。

**解决方案**：
1. 检查 `changes/` 和 `archive/` 目录
2. 使用不同的 change 名称
3. 若需恢复，先删除或重命名冲突目录后重试

---

## 7. Skill 安装后不生效

**症状**：`stdd install claude-code` 后 `/stdd-understand` 无响应。

**原因**：Skill 文件未正确写入目标目录或 frontmatter 格式不匹配。

**解决方案**：
1. 检查 `.claude/skills/` 目录是否有对应的 `stdd-*/SKILL.md` 文件
2. 确保 SKILL.md 有正确的 YAML frontmatter（`---` 包裹的 name/description）
3. 重启 Claude Code 会话使 Skills 重新加载
4. 执行 `stdd install claude-code` 重新安装

---

## 8. archive 合并冲突

**症状**：`stdd archive` 输出"冲突警告: 以下 Requirement 已存在"。

**原因**：待合并的 spec 中包含与 `specs/` 中同名的 Requirement。

**解决方案**：
1. 查看冲突报告中的 Requirement 名称
2. 决定是否合并（系统将继续追加）或修改 spec 中的 Requirement 名称
3. 如果是要替换旧 Requirement，手动编辑 `specs/` 中的目标文件
