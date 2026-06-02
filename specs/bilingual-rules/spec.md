# Spec: 关键规则双语注入

> 对应板块 D（D4）| 1 个 New Capability
> bilingual-rules

## ADDED Requirements

### Requirement: 强制性约束双语表达 <!-- confidence: high -->

STDD 的 10 条强制性约束 SHALL 在 STDD.md、AGENTS.md 和各阶段 skill 中以中英双语重复表达。

**证据来源**：proposal.md `Capabilities > New > bilingual-rules`

#### Scenario: STDD.md 中的双语规则表 <!-- confidence: high -->

- **GIVEN** STDD V2.7 已安装
- **WHEN** AI 读取 STDD.md
- **THEN** 文件 SHALL 包含 "⚠️ 强制性约束 / MANDATORY CONSTRAINTS" 章节
- **AND** 章节 SHALL 为中英对照表格式（# | 中文 | English）
- **AND** 覆盖 10 条规则：Gate 确认不可跳过 / 设计偏离必须记录 / RED→GREEN→REFACTOR 顺序 / 失败模式全量检查 / Gate 2 前不可实现 / 先读模板再生成 / 覆盖率诊断不可跳过 / change 目录外不可修改 / 经验不可删除 / 新 session 必须先读 phase-context

#### Scenario: AGENTS.md 中的双语 subagent 约束 <!-- confidence: medium -->

- **GIVEN** STDD V2.7 已安装
- **WHEN** AI 读取 AGENTS.md
- **THEN** 每个 subagent 定义的约束段 SHALL 包含中英双语的关键约束
- **AND** 双语约束 SHALL 放在 agent 定义的开头，确保最先被模型读取

#### Scenario: 阶段 skill 中的双语检查项 <!-- confidence: medium -->

- **GIVEN** Phase 4 BUILD 开始
- **WHEN** AI 读取 build.md skill
- **THEN** skill 文件的 "关键规则" 段 SHALL 包含中英双语的强制性约束
- **AND** 约束 SHALL 包含：RED→GREEN→REFACTOR 顺序（中英）、不可跳过模板读取（中英）、文件大小约束（中英）

#### Scenario: 双语规则同步维护 <!-- confidence: medium -->

- **GIVEN** 需要修改一条强制性规则
- **WHEN** 开发者更新规则
- **THEN** 中文和 English 版本 SHALL 在同一位置相邻更新
- **AND** 单向更新一个语言版本 SHALL 被视为 bug

#### Scenario: 非强制性规则保持单语言 <!-- confidence: high -->

- **GIVEN** skill 文件中的指导性内容（如 "建议使用 async/await 模式"）
- **WHEN** AI 读取 skill
- **THEN** 这些内容 SHALL 保持当前语言（中文），不做双语
- **AND** 双语仅覆盖 10 条强制性约束
