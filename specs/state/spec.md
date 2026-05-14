# Capability: STATE — 变更状态文件

## MODIFIED Requirements

### Requirement: .stdd.yaml 包含 version 字段

系统 SHALL 在新建 change 时生成的 `.stdd.yaml` 中包含 `version` 字段，标记状态文件格式版本。

#### Scenario: 新建 change 生成带 version 的状态文件

- **GIVEN** 用户执行 `stdd new my-feature`
- **WHEN** 系统生成 `.stdd.yaml`
- **THEN** 生成的文件 SHALL 包含 `version: "1.2"`

#### Scenario: 读取旧格式状态文件（无 version 字段）

- **GIVEN** 已存在的 `.stdd.yaml` 不包含 `version` 字段
- **WHEN** CLI 读取该文件
- **THEN** 系统 SHALL 默认视为 version `"1.0"`
- **AND** 系统 SHALL NOT 报错或警告

#### Scenario: status 命令显示 version 信息

- **GIVEN** .stdd.yaml 包含 `version: "1.2"`
- **WHEN** 用户执行 `stdd status`
- **THEN** 系统 SHALL 在状态信息中显示版本号
