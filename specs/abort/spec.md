# Capability: ABORT — 放弃变更

## NEW Requirements

### Requirement: /stdd-abort 命令

系统 SHALL 提供 `/stdd-abort` 命令（Skill 指令），允许用户放弃当前变更并清理 change 目录。

#### Scenario: 确认后放弃变更

- **GIVEN** 当前活跃 change 为 2026-05-14-experiment
- **AND** 用户输入 `/stdd-abort` 或"放弃当前变更"
- **WHEN** 系统确认后
- **THEN** 系统 SHALL 将 change 目录移动到 archive/aborted/
- **AND** 系统 SHALL 更新 .stdd.yaml 状态为 aborted
- **AND** 系统 SHALL 提示用户变更已放弃

#### Scenario: 用户取消放弃操作

- **GIVEN** 用户输入 `/stdd-abort`
- **WHEN** 系统要求确认，用户回复"取消"
- **THEN** 系统 SHALL 保留 change 目录不变
- **AND** 系统 SHALL 提示操作已取消

### Requirement: stdd abort CLI 命令

CLI SHALL 提供 `stdd abort <name>` 命令作为 abort 的 CLI 实现。

#### Scenario: CLI 执行 abort

- **GIVEN** change 目录 changes/2026-05-14-experiment/ 存在
- **WHEN** 用户执行 `stdd abort experiment --yes`
- **THEN** 系统 SHALL 将目录移动到 archive/aborted/
- **AND** 系统 SHALL 以零退出码退出
