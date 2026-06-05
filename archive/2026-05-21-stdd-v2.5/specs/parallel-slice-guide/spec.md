# Spec: parallel-slice-guide — 并行切片执行指南

> Capability: parallel-slice-guide
> Priority: P1 · 0.5d · Skill 增强

## Requirement: build.md 并行执行策略

`build.md` skill SHALL 包含并行切片执行策略，指导 AI 在支持 delegation 的平台上并行执行独立切片。

### Scenario: 识别可并行切片

GIVEN slices.md 包含 `parallel_group` 列，其中 Slice C 和 Slice D 同在组 2
WHEN AI 在 Phase 4 BUILD 读取 slices.md
THEN AI SHALL 识别出 Slice C 和 Slice D 可并行执行（无相互依赖）
AND 输出计划中 SHALL 标注"Slice C+D: 并行组 2，可同时执行"

### Scenario: 并行执行策略

GIVEN 当前平台支持 subagent delegation
AND Slice C 和 Slice D 同在 parallel_group 2
WHEN AI 开始执行 Phase 4 BUILD
THEN Slice C SHALL 被派发到 subagent 1
AND Slice D SHALL 被派发到 subagent 2
AND 主 agent SHALL 等待两者完成后 merge 结果

### Scenario: 串行降级

GIVEN 当前平台不支持 subagent delegation
AND Slice C 和 Slice D 同在 parallel_group 2
WHEN AI 开始执行 Phase 4 BUILD
THEN Slice C SHALL 先执行
AND Slice D SHALL 在 C 完成后执行
AND 顺序不影响最终结果

### Scenario: 不同 parallel_group 的切片串行执行

GIVEN Slice A 在 parallel_group 1
AND Slice B 在 parallel_group 2（依赖 Slice A）
WHEN AI 开始执行
THEN group 1 的切片 SHALL 全部完成后才开始 group 2
AND 不因并行能力而违反依赖顺序

## Requirement: 并行结果 merge

主 agent SHALL 在并行切片完成后统一执行 REFACTOR 和 merge。

### Scenario: 并行完成后 merge

GIVEN Slice C 和 Slice D 已分别完成 RED→GREEN
WHEN 主 agent 收集两者的产出
THEN 主 agent SHALL 运行全量测试确认无冲突
AND 主 agent SHALL 统一执行 REFACTOR（提取共享逻辑、消除重复）
AND 最终提交 SHALL 包含两者的变更
