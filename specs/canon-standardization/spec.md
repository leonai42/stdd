# Spec: Canonical 标准化 + 验证管线

> 对应板块 A（A3/A4/A6）| 3 个 New Capabilities
> canonical-standardization / canon-verify-cli

## ADDED Requirements

### Requirement: Canonical Source 目录标准化 <!-- confidence: high -->

STDD SHALL 将 `canonical/` 定为 Canonical YAML 的标准目录，与 `changes/`（Human View）并行存在。

**证据来源**：proposal.md `Capabilities > New > canonical-standardization`

#### Scenario: 目录结构互不冲突 <!-- confidence: high -->

- **GIVEN** 项目同时存在 `canonical/` 和 `changes/` 目录
- **WHEN** AI 执行 Phase 1-6 流程
- **THEN** Canonical YAML SHALL 写入 `canonical/` 目录
- **AND** Human View MD SHALL 写入 `changes/` 目录
- **AND** 两个目录的文件 SHALL 通过 `.canon-index.yaml` 维护映射关系

---

### Requirement: specs/code/ 与 specs/agent/ 分目录 <!-- confidence: high -->

STDD SHALL 在 `canonical/specs/` 下区分代码行为验证（code/）和 Agent 操作验证（agent/）两个子目录。

**证据来源**：proposal.md `Capabilities > New > canonical-standardization`

#### Scenario: 代码 spec 写入 code/ 目录 <!-- confidence: high -->

- **GIVEN** change 涉及 Python 函数行为变更
- **WHEN** Phase 2 SPEC 生成 spec
- **THEN** Canonical spec SHALL 写入 `canonical/specs/code/<capability>.yaml`
- **AND** spec 格式 SHALL 为 GIVEN/WHEN/THEN 行为规格

#### Scenario: Agent spec 写入 agent/ 目录 <!-- confidence: high -->

- **GIVEN** change 涉及 Agent 操作验证（如部署脚本）
- **WHEN** Phase 2 SPEC 生成 agent_spec
- **THEN** Canonical spec SHALL 写入 `canonical/specs/agent/<task-id>.yaml`
- **AND** spec 格式 SHALL 为 CP 检查点 + assertions 验证规格

---

### Requirement: stdd canon verify CLI <!-- confidence: high -->

STDD SHALL 提供 `stdd canon verify` 命令，检查 Canonical YAML 与 Human View MD 之间的一致性。

**证据来源**：proposal.md `Capabilities > New > canon-verify-cli`

#### Scenario: 源哈希校验通过 <!-- confidence: high -->

- **GIVEN** Canonical YAML 和 Human View MD 内容一致（YAML 未被修改）
- **WHEN** 执行 `stdd canon verify <change-name>`
- **THEN** 系统 SHALL 计算 YAML 的 SHA256 并与 MD 头部的 `source_hash` 比对
- **AND** 一致时输出 "✅ DC-HASH 源哈希一致"

#### Scenario: 源哈希不匹配时阻断 <!-- confidence: high -->

- **GIVEN** Canonical YAML 已被修改但 Human View 未重新生成
- **WHEN** 执行 `stdd canon verify <change-name>`
- **THEN** 系统 SHALL 输出 "❌ DC-HASH 源哈希不一致" 并以非零状态码退出
- **AND** 提示用户执行 `stdd canon generate <change-name>` 重新生成 Human View

#### Scenario: 字段引用校验 <!-- confidence: high -->

- **GIVEN** Human View 模板引用了 Canonical 中不存在的字段
- **WHEN** 执行 `stdd canon verify <change-name>`
- **THEN** 系统 SHALL 输出 "❌ DC-FIELD 引用到不存在的字段: <field-path>"
- **AND** 以非零状态码退出

#### Scenario: 非阻断性警告 <!-- confidence: medium -->

- **GIVEN** Human View 的 generated_at 早于 Canonical 的 last_modified
- **WHEN** 执行 `stdd canon verify <change-name>`
- **THEN** 系统 SHALL 输出 "⚠️ DC-TIME Human View 可能过时"
- **AND** 不阻断流程（警告不导致非零退出码）
