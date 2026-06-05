# lightweight-mode — 轻量模式

<!-- confidence: high -->
<!-- evidence: proposal.md "轻量模式（P3）" + V2.9_PLAN.md Part B -->

## Requirement: 复杂度评分

LITE-REQ-001: Phase 1 末尾 SHALL 基于 proposal 内容计算复杂度评分。

### Scenario: 微小变更评为 lightweight

<!-- confidence: high -->
GIVEN proposal 描述变更涉及 2 个文件、30 行代码、1 个 capability、低风险
WHEN Phase 1 Step 3.5 执行复杂度评分
THEN SHALL 计算总分在 0-3 范围内
AND SHALL 建议模式为 `lightweight`

### Scenario: 中型变更评为 standard

<!-- confidence: high -->
GIVEN proposal 描述变更涉及 10 个文件、500 行代码、3 个 capability、中风险、涉及 API
WHEN Phase 1 Step 3.5 执行复杂度评分
THEN SHALL 计算总分在 4-7 范围内
AND SHALL 建议模式为 `standard`

### Scenario: 大型变更评为 thorough

<!-- confidence: medium -->
GIVEN proposal 描述变更涉及 25 个文件、1500 行代码、5 个 capability、高风险、涉及安全
WHEN Phase 1 Step 3.5 执行复杂度评分
THEN SHALL 计算总分 >= 8
AND SHALL 建议模式为 `thorough`

## Requirement: Gate 1 模式确认

LITE-REQ-002: Gate 1 SHALL 展示模式建议并等待用户确认。

### Scenario: 用户确认 AI 建议的模式

<!-- confidence: high -->
GIVEN AI 建议模式为 `lightweight`，复杂度评分 2
WHEN Gate 1 向用户展示模式建议
AND 用户确认 `lightweight`
THEN SHALL 写入 `.stdd.yaml` 且 `mode: lightweight, score_confidence: preliminary`
AND 后续 Phase 按 lightweight 缩放表执行

### Scenario: 用户调整为更高级别模式

<!-- confidence: high -->
GIVEN AI 建议模式为 `lightweight`
WHEN 用户选择 `standard`
THEN SHALL 写入 `.stdd.yaml` 且 `mode: standard`
AND 后续 Phase 按 standard 模式执行

## Requirement: Phase 缩放执行

LITE-REQ-003: Phase 2-6 SHALL 根据 `.stdd.yaml` 中的 mode 执行不同深度。

### Scenario: lightweight Phase 2 跳过 design 和 test-plan

<!-- confidence: high -->
GIVEN `.stdd.yaml` 中 `mode: lightweight`
WHEN 执行 Phase 2 SPEC
THEN SHALL 跳过 design.md 生成
AND SHALL 跳过 test-plan.md 生成
AND SHALL 生成 1 个简化 capability spec
AND Gate 2 SHALL 自动通过

### Scenario: lightweight Phase 3 跳过切片分析

<!-- confidence: high -->
GIVEN `.stdd.yaml` 中 `mode: lightweight`
WHEN 执行 Phase 3 SLICE
THEN SHALL 使用 1 个隐式切片（不生成 tasks.md 和 slices.md）

### Scenario: lightweight Phase 4 执行聚焦 TDD

<!-- confidence: high -->
GIVEN `.stdd.yaml` 中 `mode: lightweight`
WHEN 执行 Phase 4 BUILD
THEN SHALL 写 1-2 个聚焦测试（RED）
AND SHALL 最小实现通过测试（GREEN）
AND SHALL 跳过 REFACTOR

### Scenario: lightweight Phase 5 执行核心检查

<!-- confidence: high -->
GIVEN `.stdd.yaml` 中 `mode: lightweight`
WHEN 执行 Phase 5 VERIFY
THEN SHALL 使用单 agent inline review（不启动 3 agent 并行评审）
AND SHALL 仅检查核心 5 类失败模式：(a)(b)(c)(e)(f)
AND SHALL 跳过 pass@k 验证
AND Gate 3 SHALL 强制确认

### Scenario: standard 模式行为与 V2.8 一致

<!-- confidence: high -->
GIVEN `.stdd.yaml` 中 `mode: standard`
WHEN 执行 Phase 2-6
THEN 流程 SHALL 与 V2.8 行为一致（无退化）

### Scenario: Phase 2 中上调模式

<!-- confidence: medium -->
GIVEN `.stdd.yaml` 中 `mode: lightweight, score_confidence: preliminary`
AND Phase 2 分析发现实际复杂度高于初步评估
WHEN AI 提议上调模式
AND 用户确认
THEN SHALL 更新 `.stdd.yaml` 中 mode 为 standard
AND SHALL 按 standard 模式完成后续 Phase 2 步骤

## Requirement: 非代码任务支持

LITE-REQ-004: SHALL 通过 task_type 字段区分不同任务类型的验证策略。

### Scenario: 文档任务使用 markdownlint

<!-- confidence: medium -->
GIVEN `.stdd.yaml` 中 `task_type: documentation`
WHEN 执行 Phase 5 VERIFY
THEN SHALL 使用 markdownlint 验证文档格式
AND SHALL 检查链接有效性

### Scenario: 配置任务使用 yamllint

<!-- confidence: medium -->
GIVEN `.stdd.yaml` 中 `task_type: configuration`
WHEN 执行 Phase 5 VERIFY
THEN SHALL 使用 yamllint 或 schema validator 验证配置文件
