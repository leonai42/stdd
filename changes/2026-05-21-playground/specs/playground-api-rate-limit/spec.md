# Capability: 场景一 — API 限流 (playground-api-rate-limit)

## ADDED Requirements

### Requirement: 场景数据内容

系统 SHALL 在 `playground/api-rate-limit/data.js` 中提供场景一的完整结构化数据，覆盖 6 个 Phase。

#### Scenario: Phase 1 UNDERSTAND 内容

- **GIVEN** stepper.js 渲染 Phase 1
- **WHEN** 读取 data.js 中 Phase 1 数据
- **THEN** SHALL 显示用户输入：`/stdd-understand 我们需要为 API 增加速率限制功能`
- **AND** SHALL 展示 proposal.md 结构化内容（Why / What Changes / Capabilities / Success Criteria 各标注关键字段）
- **AND** SHALL 展示 Gate 1 交互区：3 项 Success Criteria 勾选（① 单IP每分钟≤100次 ② 超限返回429+提示 ③ 白名单不限流）

#### Scenario: Phase 2 SPEC 内容

- **GIVEN** stepper.js 渲染 Phase 2
- **WHEN** 读取 data.js 中 Phase 2 数据
- **THEN** SHALL 展示 design.md 关键决策（算法选型令牌桶、存储 Redis、中间件位置）
- **AND** SHALL 展示至少 3 个 Scenario（正常放行/超限拒绝/令牌恢复）的 GIVEN/WHEN/THEN
- **AND** SHALL 展示 test-plan.md 覆盖矩阵表格（TC-RATE-001 ~ TC-RATE-006）
- **AND** SHALL 展示 Gate 2：「确认设计基线」按钮

#### Scenario: Phase 3-4 SLICE + BUILD 内容

- **GIVEN** stepper.js 渲染 Phase 3-4
- **WHEN** 读取 data.js 中对应数据
- **THEN** SHALL 展示切片拆分动画（S1:认证中间件→S2:限流核心→S3:白名单管理）
- **AND** SHALL 展示 RED→GREEN→REFACTOR 动画（先展示测试代码失败，再展示实现后通过）
- **AND** SHALL 展示 pending-adjustments 记录示例

#### Scenario: Phase 5 VERIFY 内容

- **GIVEN** stepper.js 渲染 Phase 5
- **WHEN** 读取 data.js 中 Phase 5 数据
- **THEN** SHALL 展示测试结果（22 passed, Coverage 94%）
- **AND** SHALL 展示 11 类失败模式逐条检查动画
- **AND** SHALL 展示 Gate 3：「确认交付」按钮

#### Scenario: Phase 6 DELIVER 内容

- **GIVEN** stepper.js 渲染 Phase 6
- **WHEN** 读取 data.js 中 Phase 6 数据
- **THEN** SHALL 展示 `stdd trace TC-RATE-002` 追溯链
- **AND** SHALL 展示 git commit + tag + archive 完成状态
