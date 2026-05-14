# Capability: METHOD — 方法论增强

## MODIFIED Requirements

### Requirement: VERIFY 并行 Review

VERIFY 阶段 SHALL 在执行质量检查前先进行多路并行技术评审。

#### Scenario: 三路并行审查

- **GIVEN** Phase 4 BUILD 已完成
- **WHEN** 进入 Phase 5 VERIFY
- **THEN** 系统 SHALL 启动 3 个并行审查代理（代码质量 + 测试/配置 + 文档/Skills）
- **AND** 汇总发现并按严重性分类

#### Scenario: Review-Fix 迭代循环

- **GIVEN** 首轮 Review 发现 C/H 级问题
- **WHEN** 自动修复后重新 Review
- **THEN** 系统 SHALL 迭代直到 C=0、H≤3、M≤10
- **AND** 最多执行可配置的 N 轮迭代

#### Scenario: Review 结果汇总到 test-report

- **GIVEN** Review 迭代完成
- **WHEN** 生成 test-report.md
- **THEN** 报告 SHALL 包含 Review 发现的问题、修复状态、最终得分

### Requirement: Phase 1 提案审查

Phase 1 UNDERSTAND SHALL 在用户确认前自动审查 proposal.md。

#### Scenario: proposal 完整性审查

- **GIVEN** proposal.md 已起草
- **WHEN** 进入 Step 3.5
- **THEN** 系统 SHALL 检查：Why 清晰、What Changes 具体、Success Criteria 可验证
- **AND** 自动修复发现的问题

### Requirement: Phase 2 设计审查

Phase 2 SPEC SHALL 在用户确认前自动审查 design.md 和 specs。

#### Scenario: design/specs 一致性审查

- **GIVEN** design.md + specs 已生成
- **WHEN** 进入 Step 4.5
- **THEN** 系统 SHALL 检查：需求覆盖完整、Scenario 格式正确、TC-ID 一致性
- **AND** 自动修复发现的问题

### Requirement: Review 阈值配置

`quality.yaml` SHALL 包含 Review 迭代的阈值配置。

#### Scenario: 配置可读

- **GIVEN** quality.yaml
- **WHEN** 读取 review 配置
- **THEN** SHALL 包含 max_rounds、severity_thresholds
