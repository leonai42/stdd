# Spec: 结构化数据模型（Canonical Data Model）

> 对应板块 E（E1/E2/E4）| 3 个 New Capabilities
> canonical-proposal / canonical-agent-spec / canonical-project-index

## ADDED Requirements

### Requirement: proposal.yaml 格式定义 <!-- confidence: high -->

STDD SHALL 支持 proposal.yaml 作为变更提案的 Canonical（结构化 YAML）表达，与现有 proposal.md（Human View）并存。

**证据来源**：proposal.md `Capabilities > New > canonical-proposal`

#### Scenario: 从 proposal.md 生成 proposal.yaml <!-- confidence: high -->

- **GIVEN** 用户已完成 Phase 1 且 proposal.md 经 Gate 1 确认
- **WHEN** 执行 `stdd proposal init`
- **THEN** 系统 SHALL 生成 `canonical/proposals/<change-id>.yaml`，包含 proposal.md 的结构化映射（why / what_changes / capabilities / constraints / risk_areas / success_criteria / anchoring）
- **AND** 生成的 YAML 中每个字段 SHALL 对应 proposal.md 模板中的 `STDD-MARKER` 标记

#### Scenario: 校验 proposal.yaml 完整性 <!-- confidence: high -->

- **GIVEN** 存在 `canonical/proposals/<change-id>.yaml`
- **WHEN** 执行 `stdd proposal validate`
- **THEN** 系统 SHALL 检查必填字段（meta.change_id / why.problem / capabilities）是否存在
- **AND** 缺失必填字段时 SHALL 输出错误信息并以非零状态码退出

#### Scenario: 纯 Markdown 模式向后兼容 <!-- confidence: high -->

- **GIVEN** 项目未创建 `canonical/` 目录
- **WHEN** 执行任何 STDD 命令
- **THEN** 系统 SHALL 行为与 V2.5 完全一致，不要求 canonical/ 目录存在

---

### Requirement: agent_spec.yaml 格式定义 <!-- confidence: high -->

STDD SHALL 支持 agent_spec.yaml 作为 Agent 操作验证规格的 Canonical 表达，定义检查点（CP）和断言。

**证据来源**：proposal.md `Capabilities > New > canonical-agent-spec`

#### Scenario: 定义单系统 Agent 验证规格 <!-- confidence: high -->

- **GIVEN** 开发者需要验证 "部署到 staging" 这个 Agent 操作
- **WHEN** 创建 `canonical/specs/agent/deploy-staging.yaml`，定义 CP-1（拉镜像）和 CP-2（重启容器）及对应断言
- **THEN** 该文件 SHALL 包含 meta（task_id / system / preconditions）、steps（id / description / action / assertions）、rollback 三个顶层字段
- **AND** 每个 assertion SHALL 包含 type（exit_code / stdout_contains / http_status）和 expected 字段

#### Scenario: agent_spec 与 code_spec 格式区分 <!-- confidence: medium -->

- **GIVEN** 开发者查看 `canonical/specs/` 目录
- **WHEN** 浏览 code/ 和 agent/ 子目录
- **THEN** code/ 下 SHALL 存放代码行为 spec（GIVEN/WHEN/THEN 格式，对应函数/API 验证）
- **AND** agent/ 下 SHALL 存放 Agent 操作 spec（CP 检查点 + assertions 格式，对应操作过程验证）

---

### Requirement: project-index.yaml 格式定义 <!-- confidence: high -->

STDD SHALL 支持 project-index.yaml 作为项目级结构化索引，记录所有 changes、specs、capabilities 及模块映射关系。

**证据来源**：proposal.md `Capabilities > New > canonical-project-index`

#### Scenario: 扫描项目生成索引 <!-- confidence: high -->

- **GIVEN** 项目已有 3 个 changes 和 5 个 capabilities
- **WHEN** 执行 `stdd index update`
- **THEN** 系统 SHALL 生成 `project-index.yaml`，包含 changes 列表（状态+关联capabilities+模块）、capabilities 索引（关联specs+模块+changes）、module_index（模块→capability 映射）
- **AND** 索引中的每个 capability SHALL 关联到至少 1 个 change 和 1 个 spec 文件

#### Scenario: 追溯文件关联 <!-- confidence: high -->

- **GIVEN** project-index.yaml 已就绪
- **WHEN** 执行 `stdd index trace middleware/rate_limit.py`
- **THEN** 系统 SHALL 输出该文件关联的 capabilities、changes、specs
- **AND** 输出格式 SHALL 为人类可读的层级缩进
