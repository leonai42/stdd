# Capability: gate-interaction

## MODIFIED Requirements

### Requirement: Gate 确认消息 SHALL 包含自动审查结果

每个 Phase 的 confirmation gate 消息 SHALL 展示该阶段已执行的 review 的结果，帮助用户做出更好的确认决策。

#### Scenario: Gate 1 展示 proposal review 结果

- **GIVEN** Phase 1 Step 3.5 提案审查已完成（完整性/清晰度/范围）
- **WHEN** 系统展示 Gate 1 确认消息
- **THEN** 消息 SHALL 包含「🔍 自动审查结果」段落
- **AND** SHALL 列出审查维度（完整性/清晰度/范围）
- **AND** SHALL 列出发现问题数和已自动修复数
- **AND** SHALL 给出审查结论（全部通过/有修复项/有未解决问题）

#### Scenario: Gate 2 展示 design+specs review 结果

- **GIVEN** Phase 2 Step 4.5 设计审查已完成（需求覆盖/Scenario完备性/TC-ID一致性/文档一致性）
- **WHEN** 系统展示 Gate 2 确认消息
- **THEN** 消息 SHALL 包含「🔍 自动审查结果」段落
- **AND** SHALL 列出 4 项审查维度
- **AND** SHALL 列出发现问题数和已自动修复数
- **AND** SHALL 给出审查结论

#### Scenario: Gate 3 展示多路并行 review 结果和步骤确认

- **GIVEN** Phase 5 Step 0 三路并行审查已完成（代码质量/测试配置/文档Skills）
- **WHEN** 系统展示 Gate 3 确认消息
- **THEN** 消息 SHALL 包含三路审查结果，含 C/H/M/L 各级问题统计
- **AND** SHALL 包含自动修复的 C/H 问题数量
- **AND** SHALL 包含 6 步强制步骤完成确认表（Step 0-5 各步标记 ✅/❌）
