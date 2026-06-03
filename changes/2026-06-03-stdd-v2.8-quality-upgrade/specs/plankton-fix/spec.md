# Spec: Plankton 多级自动修复

## ADDED Requirements

### Requirement: Level 1 静默修复

#### Scenario: 修复格式化和 import 排序
- **GIVEN** 项目代码存在格式问题（尾随空格、import 未排序）
- **WHEN** 执行 `stdd fix --level 1`
- **THEN** 系统 SHALL 执行 `ruff format .` + `ruff check --fix .` + `isort .`
- **AND** 输出修复的文件列表

#### Scenario: 仅在有变更时修复
- **GIVEN** 代码已格式化，无格式问题
- **WHEN** 执行 `stdd fix --level 1`
- **THEN** 系统 SHALL 输出 "Already formatted — nothing to fix"

---

### Requirement: Level 2 建议修复

#### Scenario: 检测类型注解缺失
- **GIVEN** 代码中存在无类型注解的函数
- **WHEN** 执行 `stdd fix --level 2 --dry-run`
- **THEN** 系统 SHALL 列出缺失类型注解的函数
- **AND** 生成建议的 diff（不自动应用）

#### Scenario: 检测异常处理不完整
- **GIVEN** async 函数中使用裸 `except Exception`
- **WHEN** 执行 `stdd fix --level 2`
- **THEN** 系统 SHALL 检测并警告 "Possible missing CancelledError handling"
- **AND** 提示用户确认后应用修复

---

### Requirement: Level 3 报告修复

#### Scenario: 生成安全/性能报告不自动应用
- **GIVEN** 代码中存在潜在安全问题
- **WHEN** 执行 `stdd fix --level 3`
- **THEN** 系统 SHALL 生成修复建议报告
- **AND** SHALL NOT 自动修改任何代码
