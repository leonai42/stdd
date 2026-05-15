# Capability: verify-completeness

## MODIFIED Requirements

### Requirement: Verify 阶段 SHALL 执行全部 6 个强制步骤

Phase 5 Verify 阶段的所有 6 个步骤均为强制步骤。系统 SHALL 在进入 Gate 3 之前完成所有步骤，SHALL NOT 跳过任何一步。

#### Scenario: 6 个强制步骤全部执行后才能进入 Gate 3

- **GIVEN** 系统进入 Phase 5 Verify
- **WHEN** 系统开始执行质量验证
- **THEN** 系统 SHALL 依次执行 Step 0（三路并行技术评审）
- **AND** SHALL 执行 Step 1（全量质量检查：pytest + coverage + lint）
- **AND** SHALL 执行 Step 2（Diff 审查：逐文件检查所有变更）
- **AND** SHALL 执行 Step 3（十一类失败模式检查 a-k 共 11 项）
- **AND** SHALL 执行 Step 4（汇总设计调整，生成 design-adjustments.md）
- **AND** SHALL 执行 Step 5（生成 test-report.md）
- **AND** SHALL NOT 在任何步骤未完成时展示 Gate 3 确认消息

#### Scenario: Gate 3 展示步骤完成确认表

- **GIVEN** Verify 阶段 6 个强制步骤全部已完成
- **WHEN** 系统展示 Gate 3 确认消息
- **THEN** 消息 SHALL 包含「📋 步骤完成确认」表格
- **AND** 已完成的步骤 SHALL 标记为 ✅
- **AND** 无需执行的步骤（如设计调整不存在时）SHALL 标记为 N/A
