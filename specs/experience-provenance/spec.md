# Spec: 经验溯源 + 扩展类别

> 对应板块 D（D2）+ 板块 A（A8）| 2 个 New Capabilities + 1 个 Modified Capability
> experience-provenance / experience-new-categories / experience-model

## ADDED Requirements

### Requirement: 经验 Provenance 字段 <!-- confidence: high -->

STDD 经验条目 SHALL 新增 provenance 字段，记录经验的来源和对应基础权重。

**证据来源**：proposal.md `Capabilities > New > experience-provenance`

#### Scenario: 新经验自动标记 provenance <!-- confidence: high -->

- **GIVEN** Phase 5 VERIFY 中 CI 自动检测到新的失败模式
- **WHEN** AI 创建新的经验条目
- **THEN** 经验 YAML frontmatter SHALL 包含 `provenance: ci-detected` 和 `provenance_weight: 0.85`
- **AND** 通过 `stdd experience add` 手动添加的经验 SHALL 默认标记为 `provenance: ai-inferred`（weight: 0.60）

#### Scenario: 按 provenance 过滤 <!-- confidence: high -->

- **GIVEN** 经验库中有 3 条 ci-detected 和 5 条 ai-inferred 经验
- **WHEN** 执行 `stdd experience list --provenance ci-detected`
- **THEN** 系统 SHALL 仅列出 provenance 为 ci-detected 的 3 条经验

#### Scenario: 自动升级 provenance <!-- confidence: medium -->

- **GIVEN** 一条 provenance=ai-inferred 的经验 occurrences 达到 3
- **WHEN** Phase 5 VERIFY 中的 auto_promote 规则触发
- **THEN** 系统 SHALL 将该经验的 provenance 升级为 ci-detected
- **AND** confidence SHALL 提升至 max(当前值, 0.85)

#### Scenario: 旧经验向后兼容 <!-- confidence: high -->

- **GIVEN** V2.5 的经验条目缺少 provenance 字段
- **WHEN** V2.7 CLI 读取该经验
- **THEN** 系统 SHALL 默认将其 provenance 设为 ai-inferred（weight: 0.60）
- **AND** 不修改原始文件（仅在内存中补充默认值）

---

### Requirement: 经验库新增类别 <!-- confidence: high -->

STDD 经验库 SHALL 新增 agent_cp_failure 和 spec_ambiguity 两个经验类别。

**证据来源**：proposal.md `Capabilities > New > experience-new-categories`

#### Scenario: Agent CP 失败经验记录 <!-- confidence: medium -->

- **GIVEN** `stdd agent verify deploy-staging` 中 CP-2 断言失败
- **WHEN** AI 识别这是一个可复现的失败模式
- **THEN** AI SHALL 创建 category=agent_cp_failure 的经验条目
- **AND** 经验 SHALL 包含失败的 CP 描述、实际输出 vs 预期输出、根因分析

#### Scenario: Spec 歧义经验记录 <!-- confidence: medium -->

- **GIVEN** pass@1=40% 但 pass@3=90%（说明 spec 有歧义但不够精确）
- **WHEN** Phase 5 VERIFY 分析 pass@k 报告
- **THEN** AI SHALL 创建 category=spec_ambiguity 的经验条目
- **AND** 经验 SHALL 标记导致歧义的具体 Scenario 和模糊表述
