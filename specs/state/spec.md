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


<!-- 合并自 2026-05-14-v2.0-architecture-upgrade -->
# Capability: STATE — 状态与配置管理

## MODIFIED Requirements

### Requirement: 配置拆分

STDD 配置 SHALL 从单文件 `config.yaml` 拆分为 `config.d/` 目录下 4 个职责单一的文件。CLI SHALL 优先读取 `config.d/`，fallback 到 `config.yaml`。

#### Scenario: 新项目使用 config.d/

- **GIVEN** 项目使用 V2.0 初始化
- **WHEN** STDD 读取配置
- **THEN** 系统 SHALL 从 `config.d/project.yaml` 等 4 个文件加载配置
- **AND** `config.yaml` SHALL NOT 必须存在

#### Scenario: 旧项目 config.yaml 向后兼容

- **GIVEN** 项目仅有 `config.yaml`（无 config.d/）
- **WHEN** STDD 读取配置
- **THEN** 系统 SHALL fallback 到 `config.yaml`
- **AND** 所有配置项 SHALL 正常可用

#### Scenario: config.d/ 优先于 config.yaml

- **GIVEN** 项目同时存在 config.d/ 和 config.yaml
- **WHEN** STDD 读取配置
- **THEN** 系统 SHALL 以 config.d/ 为准
- **AND** 系统 SHALL 输出提示建议删除旧 config.yaml

### Requirement: 长程模式中途退出

用户在 Phase 3-5 长程执行期间 SHALL 可通过输入"切换普通模式"降级为普通交互模式。

#### Scenario: Phase 4 中途退出长程模式

- **GIVEN** 当前处于长程模式，Phase 4 自动执行中
- **WHEN** 用户输入"切换普通模式"
- **THEN** 系统 SHALL 更新 .stdd.yaml 中 `long_range.mode: normal`
- **AND** 当前正在执行的切片完成后 SHALL 暂停等待用户确认
- **AND** 后续切片 SHALL 按普通模式交互

### Requirement: _find_change_dir 透明化

`_find_change_dir` 返回选中目录时 SHALL 输出提示信息说明选中了哪个 change。

#### Scenario: 模糊匹配时提示选中结果

- **GIVEN** changes/ 下有 2026-05-14-my-feature 和 2026-05-13-other-fix
- **WHEN** 用户执行 `stdd status my-feature`
- **THEN** 系统 SHALL 输出"📋 匹配到 change: 2026-05-14-my-feature"
- **AND** 系统 SHALL 显示该 change 的状态信息
---
## V2.9 变更: 2026-06-05-stdd-v2.9-core
- 详见 archive/2026-06-05-stdd-v2.9-core/
