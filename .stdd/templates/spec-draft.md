# Spec Draft: <能力名称>

> **自动生成草稿** — 由 `stdd extract-proposal` 提取 proposal 结构化数据后，AI 自动生成。
> 用户角色：审阅和修正，而非从零编写。

## 置信度说明

每个 Requirement 和 Scenario 标注置信度标签：

- **✓ 高置信度**：直接从 proposal.md 的明确字段提取（如 Capabilities 章节中的名称和描述）
- **⚠ 低置信度**：AI 根据 proposal 上下文推断生成，需要用户确认或修正

---

## <ADDED|MODIFIED> Requirements

### Requirement: <需求名称> <!-- confidence: high|medium|low -->

<一句话描述：系统 SHALL 做什么>

**证据来源**：proposal.md `Capabilities > <New|Modified> > **<名称>**：<描述>`

#### Scenario: <场景名称> <!-- confidence: high|medium|low -->

- **GIVEN** <前置条件>
- **WHEN** <触发动作>
- **THEN** 系统 SHALL <预期结果>
- **AND** <附加条件或结果>

**证据来源**：<proposal.md 中哪段文本支撑此 Scenario>

---

<!--
置信度判断规则：
- high：Scenario 的所有要素 (GIVEN/WHEN/THEN) 均可从 proposal.md 或 design.md 直接找到
- medium：部分要素需 AI 从上下文推断
- low：Scenario 几乎完全由 AI 推断，proposal 只提供了能力名称

AND 用法说明：
- 一个 Scenario 至少包含 GIVEN/WHEN/THEN 各 1 条
- 可通过 AND 扩展多条件，最多 5 条 AND
-->
