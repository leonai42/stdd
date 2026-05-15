# Capability: mode-selection

## MODIFIED Requirements

### Requirement: Gate 2 后模式选择 SHALL 为强制步骤

在 Phase 2 文档确认锁定后、Phase 3 启动前，系统 SHALL 强制展示执行模式选择，不可依据配置自动跳过。

#### Scenario: 模式选择不可跳过

- **GIVEN** Phase 2 文档已确认锁定，`.stdd.yaml` 中 `phases.spec.status == "completed"`
- **WHEN** 系统准备进入 Phase 3
- **THEN** 系统 SHALL 使用 AskUserQuestion 展示模式选择
- **AND** SHALL NOT 根据 `long_range.recommended` 配置自动跳过询问
- **AND** `recommended` 配置值 SHALL 仅影响推荐选项的标注方式（如标记为 `[推荐]`）

#### Scenario: 用户选择长程模式

- **GIVEN** 模式选择已展示，含「全自动长程模式」和「普通交互模式」两个选项
- **WHEN** 用户选择「全自动长程模式」
- **THEN** 系统 SHALL 进入 Step 7a 一次性预授权流程
- **AND** SHALL 展示预授权清单并等待确认

#### Scenario: 用户选择普通模式

- **GIVEN** 模式选择已展示
- **WHEN** 用户选择「普通交互模式」
- **THEN** 系统 SHALL 更新 `.stdd.yaml` 中 `long_range.mode = "normal"`
- **AND** SHALL 直接进入 Phase 3
- **AND** SHALL NOT 展示预授权清单
