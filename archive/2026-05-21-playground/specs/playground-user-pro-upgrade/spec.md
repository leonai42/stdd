# Capability: 场景二 — 用户购买升级Pro (playground-user-pro-upgrade)

## ADDED Requirements

### Requirement: 场景数据内容

系统 SHALL 在 `playground/user-pro-upgrade/data.js` 中提供场景二的完整结构化数据，覆盖 6 个 Phase，重点展示多 capability 协作（order/payment/membership/privilege）。

#### Scenario: Phase 1 UNDERSTAND 内容

- **GIVEN** stepper.js 渲染 Phase 1
- **WHEN** 读取 data.js 中 Phase 1 数据
- **THEN** SHALL 显示需求描述（用户购买 Pro 服务，支付后升级会员，到期降级）
- **AND** SHALL 展示 proposal.md 结构化内容（含业务流程梳理：下单→支付→回调→开通→到期降级）
- **AND** SHALL 展示支付安全约束（幂等性、回调验签）和业务指标（支付成功率≥99%）
- **AND** SHALL 展示 Gate 1：Success Criteria 勾选

#### Scenario: Phase 2 SPEC 内容

- **GIVEN** stepper.js 渲染 Phase 2
- **WHEN** 读取 data.js 中 Phase 2 数据
- **THEN** SHALL 展示 4 个 capability 协作图（order/payment/membership/privilege）
- **AND** SHALL 展示跨 capability 的 GIVEN 依赖（"GIVEN 用户已完成支付 WHEN 回调到达 THEN 开通Pro"）
- **AND** SHALL 展示契约定义（payment→membership 回调字段规范）
- **AND** SHALL 展示 test-plan.md 覆盖矩阵（~24 TC）
- **AND** SHALL 展示 Gate 2：「确认设计基线」

#### Scenario: Phase 3-4 SLICE + BUILD 内容

- **GIVEN** stepper.js 渲染 Phase 3-4
- **WHEN** 读取 data.js 中对应数据
- **THEN** SHALL 展示 5 个切片依赖图（order→payment→membership 串行，privilege 可并行）
- **AND** SHALL 展示 TDD 演示（重点：支付网关 Mock、幂等性测试）
- **AND** SHALL 展示 pending-adjustments（支付超时从 30s→15s）

#### Scenario: Phase 5 VERIFY 内容

- **GIVEN** stepper.js 渲染 Phase 5
- **WHEN** 读取 data.js 中 Phase 5 数据
- **THEN** SHALL 展示覆盖矩阵（~24-28 TC）+ 11 类失败检查
- **AND** SHALL 重点展示 (k) 契约断层检查（payment↔membership 回调字段一致性）
- **AND** SHALL 展示 Gate 3

#### Scenario: Phase 6 DELIVER 内容

- **GIVEN** stepper.js 渲染 Phase 6
- **WHEN** 读取 data.js 中 Phase 6 数据
- **THEN** SHALL 展示跨 capability 追溯链（用户点击购买→order→payment→membership→privilege 完整链路）
- **AND** SHALL 展示 `stdd trace` 输出
