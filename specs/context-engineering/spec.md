# Spec: 上下文工程（Context Engineering）

> 对应板块 B（B1/B2/B3）| 3 个 New Capabilities + 1 个 Modified Capability
> phase-context / context-budget-check / session-resume

## ADDED Requirements

### Requirement: phase-context.md 阶段交接摘要 <!-- confidence: high -->

STDD SHALL 支持 phase-context.md 作为阶段间结构化交接摘要，每个 phase 结束时 AI 撰写对应章节。

**证据来源**：proposal.md `Capabilities > New > phase-context`

#### Scenario: Phase 完成时 AI 撰写摘要 <!-- confidence: high -->

- **GIVEN** Phase 1 UNDERSTAND 已完成且 Gate 1 已确认
- **WHEN** AI 检测到 phase 切换（active_phase: 1 → 2）
- **THEN** AI SHALL 在 phase-context.md 中追加 "Phase 1: UNDERSTAND" 章节
- **AND** 章节 SHALL 包含关键决策、用户关注点、被否决的方向、产出物清单、完整上下文文件清单

#### Scenario: 新 session Agent 恢复上下文 <!-- confidence: high -->

- **GIVEN** 上一个 session 已完成 Phase 4 BUILD，phase-context.md 包含 Phase 1-4 所有章节
- **WHEN** 新 session Agent 启动并读取 `.stdd.yaml` → 发现 `phase_context_file` 指向 phase-context.md
- **THEN** Agent SHALL 在 1 轮 Read 操作内获取完整上下文（无需翻读 3-5 个独立文件）
- **AND** 如果某决策需要详细信息，Agent SHALL 按章节末尾的"完整上下文文件清单"回溯原文

#### Scenario: 累积文件而非分散文件 <!-- confidence: medium -->

- **GIVEN** change 已完成 Phase 1-3
- **WHEN** 查看 phase-context.md
- **THEN** 所有 3 个 phase 的摘要 SHALL 在同一个文件中
- **AND** 文件总长度 SHALL 不超过 200 行（在 Agent 上下文预算中占比 < 5%）

---

### Requirement: 上下文预算检查 <!-- confidence: high -->

STDD SHALL 在 build.md 和 verify.md 的 Step 0 之前增加上下文预算软检查。

**证据来源**：proposal.md `Capabilities > New > context-budget-check`

#### Scenario: 超阈值建议重置 <!-- confidence: high -->

- **GIVEN** 当前对话已进行 > 80 轮
- **WHEN** Phase 4 BUILD 开始时执行 Step -1 上下文预算检查
- **THEN** AI SHALL 输出上下文重置建议（含 `stdd state --resume` 输出）
- **AND** 用户可选择重置（开启新 session）或继续（跳过建议）

#### Scenario: 未超阈值静默跳过 <!-- confidence: high -->

- **GIVEN** 当前对话仅 20 轮
- **WHEN** Phase 4 BUILD 开始时执行 Step -1
- **THEN** AI SHALL 确认上下文充裕，静默进入 Step 0

#### Scenario: 软建议不阻断 <!-- confidence: high -->

- **GIVEN** 对话 > 80 轮但用户明确选择继续
- **WHEN** AI 输出重置建议后用户回复 "继续"
- **THEN** AI SHALL 直接进入 Step 0，不反复提示

---

### MODIFIED Requirement: resume_context 重定位 <!-- confidence: high -->

STDD SHALL 将 resume_context 从"一句话摘要"重定位为"指针 + phase_context_file 引用"，与 phase-context.md 分工协作。

**证据来源**：proposal.md `Capabilities > Modified > session-resume`

#### Scenario: resume_context 退为指针 <!-- confidence: high -->

- **GIVEN** `.stdd.yaml` 包含 resume_context 字段
- **WHEN** Agent 读取 `.stdd.yaml` 恢复状态
- **THEN** resume_context SHALL 仅包含：当前 phase、最后动作、时间戳、phase_context_file 路径
- **AND** SHALL NOT 包含详细决策描述（那是 phase-context.md 的职责）

#### Scenario: 旧格式向后兼容 <!-- confidence: medium -->

- **GIVEN** `.stdd.yaml` 为 V2.5 格式（resume_context 为自然语言摘要，无 phase_context_file）
- **WHEN** V2.7 Agent 读取该文件
- **THEN** Agent SHALL 识别 phase_context_file 为 null
- **AND** 按旧逻辑从各阶段产物重建上下文
