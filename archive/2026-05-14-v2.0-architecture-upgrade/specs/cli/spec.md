# Capability: CLI — 命令行工具架构升级

## MODIFIED Requirements

### Requirement: CLI 模块化拆分

系统 SHALL 将 `bin/stdd` 拆分为入口文件 + `stdd/cli/` 包结构，每个子命令独立模块。

#### Scenario: bin/stdd 入口保持兼容

- **GIVEN** 用户或脚本调用 `python bin/stdd <command>`
- **WHEN** 执行任意命令
- **THEN** 系统 SHALL 行为与拆分前完全一致
- **AND** `bin/stdd --help` SHALL 输出相同的帮助信息

#### Scenario: 子命令模块可独立导入测试

- **GIVEN** 开发者在 Python 中 `from stdd.cli.commands.init import cmd_init`
- **WHEN** 调用 `cmd_init(args)`
- **THEN** 系统 SHALL 正常执行 init 逻辑
- **AND** 函数签名 SHALL 包含完整类型注解

### Requirement: --dry-run 全局选项

系统 SHALL 接受 `--dry-run` 全局选项，预览操作但不修改文件系统。

#### Scenario: dry-run 模式预览 archive 操作

- **GIVEN** change 目录存在且已完成
- **WHEN** 用户执行 `stdd --dry-run archive my-change --yes`
- **THEN** 系统 SHALL 输出将执行的步骤（合并 specs、移动目录）
- **AND** 文件系统 SHALL NOT 发生变化

#### Scenario: dry-run 模式预览 init 操作

- **GIVEN** 项目未初始化 STDD
- **WHEN** 用户执行 `stdd --dry-run init`
- **THEN** 系统 SHALL 列出将创建的文件和目录
- **AND** 文件系统 SHALL NOT 发生变化

### Requirement: --verbose 分级日志

系统 SHALL 使用 Python logging 模块替代 print()，支持 `-v` (INFO) 和 `-vv` (DEBUG) 选项。

#### Scenario: 默认输出简洁

- **GIVEN** 用户执行 `stdd status`
- **WHEN** 不带 -v 选项
- **THEN** 系统 SHALL 仅输出最终结果（当前行为）

#### Scenario: -v 输出详细信息

- **GIVEN** 用户执行 `stdd -v validate`
- **WHEN** 带 -v 选项
- **THEN** 系统 SHALL 输出检查步骤的详细日志（如"检查必需文件..."）

### Requirement: rollback 命令

系统 SHALL 提供 `stdd rollback <name>` 命令，从 archive 恢复已归档的 change。

#### Scenario: 成功恢复已归档的 change

- **GIVEN** archive/2026-05-14-my-feature/ 存在
- **AND** changes/ 下无同名目录
- **WHEN** 用户执行 `stdd rollback my-feature`
- **THEN** 系统 SHALL 将目录移回 changes/2026-05-14-my-feature/
- **AND** 系统 SHALL 更新 .stdd.yaml 状态为 active

#### Scenario: 目标已存在时拒绝恢复

- **GIVEN** archive/2026-05-14-my-feature/ 存在
- **AND** changes/2026-05-14-my-feature/ 已存在
- **WHEN** 用户执行 `stdd rollback my-feature`
- **THEN** 系统 SHALL 报告冲突错误
- **AND** 系统 SHALL 以非零退出码退出

### Requirement: diff 命令

系统 SHALL 提供 `stdd diff <name>` 命令，显示 spec Scenario ↔ TC 案例 ↔ 测试函数 ↔ 源码的覆盖对比。

#### Scenario: diff 显示覆盖差异表

- **GIVEN** change 目录包含 test-plan.md 且源码中存在 TC-ID 引用
- **WHEN** 用户执行 `stdd diff my-change`
- **THEN** 系统 SHALL 输出四列对照表（Scenario | TC-ID | 测试函数 | 源码）
- **AND** 未覆盖项 SHALL 标注为 ❌

#### Scenario: diff 处理无 test-plan 的 change

- **GIVEN** change 目录不包含 test-plan.md
- **WHEN** 用户执行 `stdd diff my-change`
- **THEN** 系统 SHALL 报告"无 test-plan.md"
- **AND** 系统 SHALL 以非零退出码退出
