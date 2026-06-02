# Capability: 智能切片推荐 (smart-slice)

## ADDED Requirements

### Requirement: 依赖图构建 CLI

系统 SHALL 提供 `stdd dependency-graph` CLI 命令，从 specs 中构建 capability 间的依赖关系图。

#### Scenario: 构建无环依赖图

- **GIVEN** specs 目录中有 3 个 capability：auth, rate-limit, whitelist
- **AND** rate-limit 的 spec 中有一个 Scenario 的 GIVEN 包含 "用户已登录"（auth 的输出）
- **WHEN** 执行 `stdd dependency-graph <change> --format json`
- **THEN** 系统 SHALL 输出包含 3 个 nodes 和 1 个 edge 的 JSON
- **AND** edge SHALL 标注 from=rate-limit, to=auth, reason="Scenario: xxx GIVEN 用户已登录"

#### Scenario: 识别零依赖节点

- **GIVEN** auth 的 Scenarios 中所有 GIVEN 都不引用其他 capability
- **WHEN** 执行 `stdd dependency-graph --format text`
- **THEN** 系统 SHALL 在 zero_dependency 列表中包含 auth
- **AND** 文本输出 SHALL 清晰显示可并行开发的节点

#### Scenario: 循环依赖警告

- **GIVEN** capability A 的 spec 引用 B，B 的 spec 又引用 A
- **WHEN** 执行 `stdd dependency-graph`
- **THEN** 系统 SHALL 输出警告 "检测到循环依赖：A ↔ B"
- **AND** SHALL 在依赖图中标记循环边

#### Scenario: DOT 格式输出

- **GIVEN** 标准依赖图数据
- **WHEN** 执行 `stdd dependency-graph --format dot`
- **THEN** 系统 SHALL 输出有效的 DOT 格式文本
- **AND** 零依赖节点 SHALL 被标记为绿色

### Requirement: Phase 3 五步切片分析

Phase 3 SLICE 技能 SHALL 升级为五步智能分析流程。

#### Scenario: 风险评分

- **GIVEN** 切片 S1 依赖 3 个其他 capability，涉及 auth 核心模块，spec 包含 12 个 GIVEN/WHEN/THEN 子句
- **WHEN** AI 执行 slice.md 增强后的 Step 2b
- **THEN** AI SHALL 标记 S1 为高风险（跨依赖数 ≥ 3 + 触碰核心模块 + 复杂度 > 10）
- **AND** SHALL 在 slices.md 的 Risk 列显示 🟡 Med 或 🔴 High

#### Scenario: 工作量预估

- **GIVEN** 切片 A 覆盖 2 个 Scenario（预计 3 个 TC），切片 B 覆盖 8 个 Scenario（预计 12 个 TC）
- **WHEN** AI 执行 Step 2c
- **THEN** AI SHALL 将切片 A 分类为 S（Small，预估 1-2h）
- **AND** SHALL 建议将切片 B 拆分为 2 个 M（Medium）切片以提高可管理性

#### Scenario: 智能分组

- **GIVEN** 切片 X 和 Y 都是低风险、零依赖、同属 middleware 模块
- **WHEN** AI 执行 Step 2d
- **THEN** AI SHALL 建议将 X 和 Y 合并为一个切片
- **AND** SHALL 在理由列中说明合并原因

#### Scenario: 高风险切片隔离

- **GIVEN** 切片 Z 涉及支付核心模块，依赖 4 个其他 capability，spec 复杂
- **WHEN** AI 执行 Step 2d
- **THEN** AI SHALL 将 Z 标记为独立切片（不与其他合并）
- **AND** SHALL 在理由列中说明隔离原因（"高风险，失败不应影响其他切片"）

#### Scenario: 并行化建议

- **GIVEN** 拓扑排序显示切片 A→C→E 和 B→D→F 两条独立链
- **WHEN** AI 执行 Step 2e
- **THEN** AI SHALL 标注 A 和 B 属于并行组 1
- **AND** 标注 C 和 D 属于并行组 2
- **AND** 标注 E 和 F 属于并行组 3

## MODIFIED Requirements

### Requirement: slices.md 模板增强

原 slices.md 模板 SHALL 增加风险等级、预估工时、并行组和理由列。

#### Scenario: 增强模板字段

- **GIVEN** AI 读取增强后的 `.stdd/templates/slices.md`
- **WHEN** 生成切片计划
- **THEN** 模板 SHALL 包含列：`# | Priority | Risk | Est. Effort | Parallel Group | TC Coverage | Implementation | Dependency | Rationale`
- **AND** Risk 列 SHALL 使用 🟢 Low / 🟡 Med / 🔴 High 色标
- **AND** Est. Effort SHALL 使用 S/M/L 分类 + 预估小时数
- **AND** Parallel Group SHALL 标注可并行执行的切片组号
