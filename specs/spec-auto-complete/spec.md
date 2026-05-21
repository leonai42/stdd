# Capability: Spec 自动补全 (spec-auto-complete)

## ADDED Requirements

### Requirement: Proposal 结构化提取

系统 SHALL 提供 `stdd extract-proposal` CLI 命令，从 proposal.md 中提取结构化的 capabilities / what_changes / success_criteria 数据。

#### Scenario: 提取完整 proposal

- **GIVEN** 一个 change 目录中包含完整的 proposal.md（含 Why / What Changes / Capabilities / Success Criteria / Impact）
- **WHEN** 执行 `stdd extract-proposal <change-name> --format json`
- **THEN** 系统 SHALL 输出包含 `title`, `capabilities`, `what_changes`, `success_criteria`, `impact` 字段的有效 JSON
- **AND** capabilities SHALL 区分 `new` 和 `modified` 两类
- **AND** impact SHALL 包含 `code`, `config`, `infrastructure` 子字段

#### Scenario: 自动选择最新 change

- **GIVEN** 不指定 change 名称
- **WHEN** 执行 `stdd extract-proposal --format yaml`
- **THEN** 系统 SHALL 自动选择 `changes/` 下最近修改的 change 目录

#### Scenario: proposal.md 缺失处理

- **GIVEN** 指定的 change 目录中没有 proposal.md
- **WHEN** 执行 `stdd extract-proposal <change>`
- **THEN** 系统 SHALL 输出错误信息 "proposal.md 不存在" 并返回退出码 1

### Requirement: Phase 2 Spec 自动生成

Phase 2 SPEC 技能 SHALL 从 proposal 结构化字段自动生成 spec 草稿，并标注置信度标签。

#### Scenario: 从 Capabilities 字段生成 spec 文件

- **GIVEN** proposal.md 的 Capabilities > New 包含 "rate-limiting" 和 "whitelist-management"
- **WHEN** AI 执行 spec.md 增强后的 Step 2
- **THEN** AI SHALL 为每个 capability 自动生成 `specs/<capability-name>/spec.md` 草稿
- **AND** 每个生成的 Requirement SHALL 标注置信度来源（proposal 字段名）

#### Scenario: 从 Success Criteria 生成 THEN 子句

- **GIVEN** proposal.md 的 Success Criteria 包含 "单 IP 每分钟不超过 100 次请求"
- **WHEN** AI 自动生成 spec
- **THEN** 该 Success Criteria SHALL 映射为某个 Scenario 的 THEN 子句
- **AND** THEN 子句 SHALL 使用 SHALL 关键字
- **AND** 置信度 SHALL 标记为 ✓（高，来源：Success Criteria #1）

#### Scenario: 低置信度标注

- **GIVEN** proposal.md 中没有明确描述某个 Scenario 的 AND 条件
- **WHEN** AI 推断补充了 AND 条件
- **THEN** 该 AND 条件 SHALL 标记为 ⚠（低置信度，来源：AI 推断）
- **AND** Gate 2 时 SHALL 提示用户审核所有 ⚠ 项

#### Scenario: 用户审核模式

- **GIVEN** AI 已生成带置信度标签的 spec 草稿
- **WHEN** 向用户展示 Gate 2 确认
- **THEN** 系统 SHALL 显示 "✓ 高置信度：N 项，⚠ 需确认：M 项"
- **AND** 用户 SHALL 逐条审核或批量确认 ✓ 项
- **AND** 对 ⚠ 项 SHALL 提供修改或补充的交互入口

### Requirement: Spec 草稿模板

系统 SHALL 提供 `spec-draft.md` 模板用于 AI 生成带置信度标注的 spec 草稿。

#### Scenario: 模板包含置信度字段

- **GIVEN** AI 读取 `.stdd/templates/spec-draft.md`
- **WHEN** 生成 spec 草稿
- **THEN** 模板 SHALL 在每个 Requirement 和 Scenario 旁包含置信度标记位
- **AND** SHALL 要求 AI 记录每个 ✓ 的来源字段

## MODIFIED Requirements

### Requirement: proposal.md 模板增强

原 proposal.md 模板 SHALL 增加结构化提取标记，使 `extract-proposal` 能精确解析。

#### Scenario: 标记注释不影响人工阅读

- **GIVEN** proposal.md 模板增加了 `<!-- __CAP_NEW__ -->` 等标记
- **WHEN** 用户或 AI 阅读 proposal.md
- **THEN** Markdown 渲染 SHALL 隐藏这些注释（标准 HTML 注释行为）
- **AND** AI 在填写 proposal 时 SHALL 保留标记结构
