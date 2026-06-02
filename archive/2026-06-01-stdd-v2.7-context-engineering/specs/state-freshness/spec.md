# Spec: 状态新鲜度校验

> 对应板块 D（D3）| 1 个 New Capability + 1 个 Modified Capability
> state-freshness / stdd-state

## ADDED Requirements

### Requirement: .stdd.yaml 状态新鲜度字段 <!-- confidence: high -->

`.stdd.yaml` SHALL 新增 state_freshness 字段块，记录状态确认时间、git HEAD 和关键文件哈希。

**证据来源**：proposal.md `Capabilities > New > state-freshness`

#### Scenario: Phase 切换时更新新鲜度 <!-- confidence: high -->

- **GIVEN** Phase 4 BUILD 完成，即将进入 Phase 5
- **WHEN** AI 更新 `.stdd.yaml` 的 active_phase
- **THEN** AI SHALL 同时更新 state_freshness：verified_at=当前时间、git_head=当前HEAD、key_files_hash=关键产出物的SHA256
- **AND** key_files_hash SHALL 至少包含 phase-context.md 和 test-report.md（如有）

#### Scenario: 状态新鲜度显示 <!-- confidence: high -->

- **GIVEN** `.stdd.yaml` 的 state_freshness.verified_at 为 2 小时前
- **WHEN** 执行 `stdd state --resume`
- **THEN** 输出 SHALL 显示 "🟢 状态: FRESH — 最近更新于 2 小时前"

#### Scenario: Git HEAD 变更时输出警告 <!-- confidence: high -->

- **GIVEN** state_freshness.git_head 为 a1b2c3d，当前 HEAD 为 f3e4d5c（+2 commits）
- **WHEN** 执行 `stdd state --resume`
- **THEN** 输出 SHALL 显示 "🟡 状态: STALE — Git HEAD 已变更（+2 commits）"
- **AND** 提示 "建议: 检查变更是否影响当前 change 的产出物"

#### Scenario: 超过 7 天未更新时警告 <!-- confidence: high -->

- **GIVEN** state_freshness.verified_at 为 10 天前
- **WHEN** 执行 `stdd state --resume`
- **THEN** 输出 SHALL 显示 "🔴 状态: STALE — 已 10 天未更新，建议重新验证"
- **AND** 提示执行 `stdd state --resume --force` 跳过警告

#### Scenario: 软检查不阻断 <!-- confidence: high -->

- **GIVEN** 状态为 STALE 但用户明确选择继续
- **WHEN** 执行 `stdd state --resume --force`
- **THEN** 系统 SHALL 跳过新鲜度警告，输出正常的恢复提示
